# python imports
import hashlib
import json
import logging
import math
import os
import requests
import urllib3
from typing import Optional, Dict, Any, Union

# third party imports
from google.cloud import storage

# TODO - verify instead of disable warnings
urllib3.disable_warnings()

# Configure logging
logger = logging.getLogger(__name__)


class FUGAClient:
    """
    A client for interacting with the FUGA API.

    Handles authentication, request building, and error handling for API interactions.
    """

    def __init__(
        self,
        api_url: str,
        username: Optional[str] = None,
        password: Optional[str] = None,
        auth_cookie: Optional[str] = None,
    ):
        self.api_url = api_url
        self.auth_cookie: Optional[str] = auth_cookie
        self.auth_cookie_dict: Optional[Dict[str, str]] = None
        self.user: Optional[Dict[str, Any]] = None
        self.user_id: Optional[str] = None

        if not self.auth_cookie:
            if not (username and password):
                raise ValueError(
                    "Either auth_cookie or username/password must be provided"
                )
            self.credentials = {"name": username, "password": password}
            self.login()

    def login(self) -> None:
        """
        Authenticate with the FUGA API and set the session cookies.

        Raises:
            Exception: If authentication fails.
        """
        path = "/login"
        headers = {"accept": "application/json", "Content-Type": "application/json"}

        response = requests.post(
            self._build_url(path),
            headers=headers,
            data=json.dumps(self.credentials),
        )

        if response.status_code != 200:
            raise Exception(
                f"Login failed: {response.status_code} {response.text.encode('utf8')}"
            )

        self.user_id = response.json().get("user", {}).get("id")
        self.user = response.json().get("user")

        # Set authentication cookie
        for cookie in response.cookies:
            self.auth_cookie = f"{cookie.name}={cookie.value}"
            self.auth_cookie_dict = {cookie.name: cookie.value}

    def _build_url(self, path: str) -> str:
        """
        Build the full API URL for a given endpoint path.

        Args:
            path (str): The relative path of the API endpoint.

        Returns:
            str: The full URL for the API endpoint.
        """
        return self.api_url + path

    def request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Union[Dict[str, Any], str]:
        """
        Make an HTTP request to the FUGA API.

        Args:
            method (str): The HTTP method (e.g., "GET", "POST", "PUT", "DELETE").
            endpoint (str): The relative path of the API endpoint.
            data (Optional[Dict[str, Any]]): The request body data (for POST/PUT requests).
            params (Optional[Dict[str, Any]]): Query parameters for the request.

        Returns:
            Union[Dict[str, Any], str]: The parsed JSON response or plain text response for DELETE.

        Raises:
            requests.HTTPError: For 4xx and 5xx responses with detailed error information.
            Exception: For unexpected response formats or request failures.
        """
        headers = {"Cookie": self.auth_cookie}

        try:

            response = requests.request(
                method,
                self._build_url(endpoint),
                headers=headers,
                json=data,
                params=params,
            )

            if not response.ok:  # Handle 4xx and 5xx errors
                try:
                    error_data = response.json()
                    logger.error(f"Error response received: {error_data}")

                    # Handle array or dictionary errors
                    error_message = "Unknown error occurred."
                    if isinstance(error_data.get("error"), list):
                        error_message = "\n".join(
                            [
                                f"Code: {err.get('code', 'No code')}, "
                                f"Message: {err.get('message', 'No message')}, "
                                f"Context: {err.get('original_error', {}).get('error_info', 'No context')}"
                                for err in error_data["error"]
                            ]
                        )
                    elif isinstance(error_data.get("error"), dict):
                        err = error_data["error"]
                        error_message = (
                            f"Code: {err.get('code', 'No code')}, "
                            f"Message: {err.get('message', 'No message')}, "
                            f"Context: {err.get('original_error', {}).get('error_info', 'No context')}"
                        )

                    detailed_error = (
                        f"HTTP {response.status_code} Error:\n" f"{error_message}"
                    )
                except json.JSONDecodeError:
                    detailed_error = (
                        f"HTTP {response.status_code} Error: {response.text}"
                    )
                    logger.error(f"Error decoding JSON response: {detailed_error}")

                raise requests.HTTPError(detailed_error, response=response)

            # Success responses with no content
            if response.status_code in [204, 200] and not response.content.strip():
                logger.info(f"Empty response for {method} request to {endpoint}.")
                return "Success with no content"

            # Handle plain text response for DELETE
            if method == "DELETE" and response.status_code == 200:
                logger.info(f"DELETE request to {endpoint} successful.")
                return response.text

            # Handle audio file response
            if "audio/mpeg" in response.headers.get("Content-Type", ""):
                logger.info(f"Audio response received from {endpoint}.")
                return response.content

            try:
                json_response = response.json()
                logger.debug(f"Response JSON: {json_response}")
                return json_response
            except json.JSONDecodeError:
                logger.error(f"Non-JSON response received: {response.text}")
                raise Exception(f"Unexpected response format: {response.text}")

        except requests.RequestException as e:
            logger.exception("Request failed.")
            raise Exception(f"Request failed: {e}")

    def post_files(
        self, endpoint: str, data: Dict[str, Any], extra_headers: Dict[str, Any] = {}
    ):
        headers = {"Cookie": self.auth_cookie}
        headers.update(extra_headers)
        response = requests.post(
            self._build_url(endpoint),
            headers=headers,
            files=data,
            verify=False,  # TODO - change this to True?
        )
        return response

    def upload_file(self, file_path: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Upload a file to the FUGA API in chunks and finalize the upload.

        If the file is located in GCS, it is first downloaded locally.

        Args:
            file_path (str): The path to the file to upload (local or GCS URL).
            data (Dict[str, Any]): The upload session details.

        Returns:
            Dict[str, Any]: The final upload response data.
        """
        # Step 1: Check if file_path is a GCS URL and download it locally
        if file_path.startswith("https://storage.googleapis.com/"):
            file_path = self._download_file_from_gcs(file_path)

        # Step 2: Start the upload session
        upload_session = self.request("POST", "/upload/start", data)
        upload_id = upload_session["id"]
        file_name = os.path.basename(file_path)

        # Step 3: Upload the file in chunks
        chunk_size = 1024 * 1024 * 5  # 5MB
        file_abs_path = os.path.abspath(file_path)
        total_file_size = os.stat(file_abs_path).st_size
        total_chunks = math.ceil(total_file_size / chunk_size)

        logger.info(f"Uploading file: {file_abs_path}, size: {total_file_size} bytes")

        file_hash = hashlib.md5()

        with open(file_abs_path, "rb") as f:
            for part_index, chunk in enumerate(self._read_in_chunks(f, chunk_size)):
                logger.debug(f"Uploading chunk {part_index + 1}/{total_chunks}")
                offset = part_index * chunk_size
                headers = {
                    "Content-Range": f"bytes {offset}-{offset + len(chunk) - 1}/{total_file_size}"
                }

                # Update the hash
                file_hash.update(chunk)

                data = {
                    "uuid": (None, upload_id),
                    "filename": (None, file_name),
                    "totalfilesize": (None, total_file_size),
                    "partindex": (None, part_index),
                    "partbyteoffset": (None, offset),
                    "totalparts": (None, total_chunks),
                    "file": ("blob", chunk, "application/octet-stream"),
                }

                # Upload the chunk
                response = self.post_files("/upload", data=data, extra_headers=headers)
                if response.status_code != 200:
                    raise Exception(
                        f"Chunk upload failed: {response.status_code} {response.text}"
                    )

                logger.info(f"Uploaded chunk {part_index + 1}/{total_chunks}")

        file_md5sum = file_hash.hexdigest()

        return self.request(
            "POST",
            "/upload/finish",
            {
                "uuid": upload_id,
                "filename": file_name,
                "md5sum": file_md5sum,
            },
        )

    def _download_file_from_gcs(self, public_url: str) -> str:
        """
        Downloads a file from Google Cloud Storage using the public URL and saves it locally.

        Args:
            public_url (str): The GCS public URL of the file.

        Returns:
            str: The local file path of the downloaded file.
        """
        # Parse GCS URL
        bucket_name = public_url.split("/")[3]
        blob_name = "/".join(public_url.split("/")[4:])

        # Initialize GCS client
        client = storage.Client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(blob_name)

        # Save file locally
        temp_file_path = f"/tmp/{os.path.basename(blob_name)}"  # Temporary file path
        blob.download_to_filename(temp_file_path)

        logger.info(f"Downloaded file from GCS: {public_url} -> {temp_file_path}")
        return temp_file_path

    def _read_in_chunks(self, file_object, chunk_size):
        """
        Generator to read a file in chunks.

        Args:
            file_object: The file object to read.
            chunk_size (int): The size of each chunk in bytes.

        Yields:
            bytes: The next chunk of the file.
        """
        while True:
            data = file_object.read(chunk_size)
            if not data:
                break
            yield data
