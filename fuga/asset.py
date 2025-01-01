# python imports
from typing import Optional, Dict, Any, List, Generator

# local imports
from .api_client import FUGAClient


class FUGAAsset:
    """
    Represents an asset (track / video) in the FUGA API.

    Provides methods for CRUD operations and additional functionality such as
    publishing and updating territories.
    """

    def __init__(self, client: FUGAClient, asset_id: Optional[str] = None):
        """
        Initialize the FUGAAsset instance.

        Args:
            client (FUGAClient): The FUGA API client instance.
            asset_id (Optional[str]): The unique ID of the asset, if available.
        """
        self.client: FUGAClient = client
        self.asset_id: Optional[str] = asset_id

    @classmethod
    def fetch_list(
        cls,
        client: FUGAClient,
        page: int = 0,
        page_size: int = 10,
        limit: Optional[int] = None,
    ) -> Generator[Dict[str, Any], None, None]:
        """
        Fetch a paginated list of assets from FUGA.

        Args:
            client (FUGAClient): The FUGA API client instance.
            page (int): The page number to start fetching from (default is 1).
            page_size (int): The number of assets per page (default is 10).
            limit (Optional[int]): The maximum number of assets to fetch (default is None for no limit).

        Yields:
            Generator[Dict[str, Any], None, None]: Each asset's details as a dictionary.

        Raises:
            requests.HTTPError: If the API request fails.
        """
        endpoint = "/assets"
        params = {"page": page, "page_size": page_size}
        fetched_count = 0

        while True:
            response = client.request("GET", endpoint, params=params)
            assets = response.get("asset", [])

            for asset in assets:
                yield asset
                fetched_count += 1
                if limit and fetched_count >= limit:
                    return

            # Break if no more assets
            total = response.get("total", 0)
            if not assets or fetched_count >= total:
                break
            # Otherwise, move to the next page
            params["page"] += 1

    def fetch(self) -> Dict[str, Any]:
        """
        Fetch a single asset's details from FUGA.

        Returns:
            Dict[str, Any]: The asset object from FUGA

        Raises:
            ValueError: If the asset ID is not set.
        """
        if not self.asset_id:
            raise ValueError("Asset ID is required for retrieval.")
        return self.client.request("GET", f"/assets/{self.asset_id}")

    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new asset in FUGA.

        Args:
            data (Dict[str, Any]): The asset data for creation.

        Returns:
            Dict[str, Any]: The asset object created in FUGA.
        """
        response = self.client.request("POST", "/assets", data=data)
        self.asset_id = response["id"]
        return response

    def update(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing asset in FUGA.

        Args:
            data (Dict[str, Any]): The asset data for update.

        Returns:
            Dict[str, Any]: The updated asset object from FUGA.

        Raises:
            ValueError: If the asset ID is not set.
        """
        if not self.asset_id:
            raise ValueError("Asset ID is required for updates.")
        return self.client.request("PUT", f"/assets/{self.asset_id}", data=data)

    def delete(self) -> str:
        """
        Delete a asset from FUGA.

        Returns:
            str: The plain text response indicating successful deletion.

        Raises:
            ValueError: If the asset ID is not set.
        """
        if not self.asset_id:
            raise ValueError("Asset ID is required for deletion.")
        return self.client.request("DELETE", f"/assets/{self.asset_id}")

    def fetch_contributors(self) -> List[Dict[str, Any]]:
        """
        Fetch the contributors associated with the asset.

        Returns:
            List[Dict[str, Any]]: A list of contributor objects associated with the asset.

        Raises:
            ValueError: If the asset ID is not set.
        """
        if not self.asset_id:
            raise ValueError("Asset ID is required for retrieval.")
        return self.client.request("GET", f"/assets/{self.asset_id}/contributors")

    def add_contributor(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add a contributor to the asset.

        Args:
            person (FUGAPerson): The person object representing the contributor.
            data (Dict[str, Any]): The contributor data including role.

        Returns:
            Dict[str, Any]: The contributor object added to the asset.

        Raises:
            ValueError: If the asset ID is not set.
        """
        if not self.asset_id:
            raise ValueError("Asset ID is required for adding contributors.")
        return self.client.request(
            "POST",
            f"/assets/{self.asset_id}/contributors",
            data=data,
        )

    def remove_contributor(self, contributor_id: str) -> str:
        """
        Remove a contributor from the asset.

        Args:
            contributor_id (str): The unique ID of the contributor to remove.

        Returns:
            str: The plain text response indicating successful removal.

        Raises:
            ValueError: If the asset ID is not set.
        """
        if not self.asset_id:
            raise ValueError("Asset ID is required for removing contributors.")
        return self.client.request(
            "DELETE",
            f"/assets/{self.asset_id}/contributors/{contributor_id}",
        )

    def remove_all_contributors(self) -> str:
        """
        Remove all contributors from the asset.

        Returns:
            str: The plain text response indicating successful removal.

        Raises:
            ValueError: If the asset ID is not set.
        """
        if not self.asset_id:
            raise ValueError("Asset ID is required for removing contributors.")
        contributors = self.fetch_contributors()
        for contributor in contributors:
            self.remove_contributor(contributor["id"])
        return "All contributors removed."

    def fetch_instrument_performers(self) -> List[Dict[str, Any]]:
        """
        Fetch the instrument performers associated with the asset.

        Returns:
            List[Dict[str, Any]]: A list of instrument performer objects associated with the asset.

        Raises:
            ValueError: If the asset ID is not set.
        """
        if not self.asset_id:
            raise ValueError("Asset ID is required for retrieval.")
        return self.client.request(
            "GET", f"/assets/{self.asset_id}/instrument_performers"
        )

    def add_instrument_performer(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add an instrument performer to the asset.

        Args:
            data (Dict[str, Any]): The instrument performer data including person and instrument.

        Returns:
            Dict[str, Any]: The instrument performer object added to the asset.

        Raises:
            ValueError: If the asset ID is not set.
        """
        if not self.asset_id:
            raise ValueError("Asset ID is required for adding instrument performers.")
        return self.client.request(
            "POST",
            f"/assets/{self.asset_id}/instrument_performers",
            data=data,
        )

    def remove_instrument_performer(self, instrument_performer_id: str) -> str:
        """
        Remove an instrument performer from the asset.

        Args:
            instrument_performer_id (str): The unique ID of the instrument performer to remove.

        Returns:
            str: The plain text response indicating successful removal.

        Raises:
            ValueError: If the asset ID is not set.
        """
        if not self.asset_id:
            raise ValueError("Asset ID is required for removing instrument performers.")
        return self.client.request(
            "DELETE",
            f"/assets/{self.asset_id}/instrument_performers/{instrument_performer_id}",
        )

    def remove_all_instrument_performers(self) -> str:
        """
        Remove all instrument performers from the asset.

        Returns:
            str: The plain text response indicating successful removal.

        Raises:
            ValueError: If the asset ID is not set.
        """
        if not self.asset_id:
            raise ValueError("Asset ID is required for removing instrument performers.")
        instrument_performers = self.fetch_instrument_performers()
        for instrument_performer in instrument_performers:
            self.remove_instrument_performer(instrument_performer["id"])
        return "All instrument performers removed."

    def fetch_publishers(self) -> List[Dict[str, Any]]:
        """
        Fetch the publishers associated with the asset.

        Returns:
            List[Dict[str, Any]]: A list of publisher objects associated with the asset.

        Raises:
            ValueError: If the asset ID is not set.
        """
        if not self.asset_id:
            raise ValueError("Asset ID is required for retrieval.")
        return self.client.request("GET", f"/assets/{self.asset_id}/publishers")

    def add_publisher(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add a publisher to the asset.
        Note that a publisher can only feature once on an Asset, so ignore the composer field.

        Args:
            data (Dict[str, Any]): The publisher data and optional composer (person).

        Returns:
            Dict[str, Any]: The publisher object added to the asset.

        Raises:
            ValueError: If the asset ID is not set.
        """
        if not self.asset_id:
            raise ValueError("Asset ID is required for adding publishers.")
        return self.client.request(
            "POST",
            f"/assets/{self.asset_id}/publishers",
            data=data,
        )

    def remove_publisher(self, publisher_id: str) -> str:
        """
        Remove a publisher from the asset.

        Args:
            publisher_id (str): The unique ID of the publisher to remove.

        Returns:
            str: The plain text response indicating successful removal.

        Raises:
            ValueError: If the asset ID is not set.
        """
        if not self.asset_id:
            raise ValueError("Asset ID is required for removing publishers.")
        return self.client.request(
            "DELETE",
            f"/assets/{self.asset_id}/publishers/{publisher_id}",
        )

    def remove_all_publishers(self) -> str:
        """
        Remove all publishers from the asset.

        Returns:
            str: The plain text response indicating successful removal.

        Raises:
            ValueError: If the asset ID is not set.
        """
        if not self.asset_id:
            raise ValueError("Asset ID is required for removing publishers.")
        publishers = self.fetch_publishers()
        for publisher in publishers:
            self.remove_publisher(publisher["id"])
        return "All publishers removed."

    def fetch_audio(self, original: bool = True) -> Dict[str, Any]:
        """
        Fetch the audio details associated with the asset.

        Returns:
            Dict[str, Any]: The audio details object associated with the asset.

        Raises:
            ValueError: If the asset ID is not set.
        """
        if not self.asset_id:
            raise ValueError("Asset ID is required for retrieval.")
        params = {"original": original}
        return self.client.request(
            "GET", f"/assets/{self.asset_id}/audio", params=params
        )

    def upload_audio(
        self,
        audio_path: str,
        is_apple_digital_master: bool = False,
    ) -> Dict[str, Any]:
        """
        Upload an audio file for the asset in FUGA.

        Args:
            audio_path (str): The path to the audio file to upload.
            is_apple_digital_master (bool): Whether the audio file is an Apple Digital Master (default is False).

        Returns:
            Dict[str, Any]: The response from the API.
        """
        if not self.asset_id:
            raise ValueError("Asset ID is required to upload an audio file.")
        data = {
            "id": self.asset_id,
            "type": "audio",
            "overwrite_all": True,
            "clear_all_encodings": True,
        }
        if is_apple_digital_master:
            data["original_encoding"] = "ADM"
        return self.client.upload_file(audio_path, data)

    def upload_video(self, video_path: str) -> Dict[str, Any]:
        """
        Upload a video file for the asset in FUGA.

        Args:
            video_path (str): The path to the video file to upload.

        Returns:
            Dict[str, Any]: The response from the API.
        """
        if not self.asset_id:
            raise ValueError("Asset ID is required to upload a video file.")
        data = {
            "id": self.asset_id,
            "type": "video",
        }
        return self.client.upload_file(video_path, data)

    def upload_video_preview_image(
        self, video_preview_image_id: str, image_path: str
    ) -> Dict[str, Any]:
        """
        Upload a video preview image for the asset in FUGA.

        Args:
            video_preview_image_id (str): The unique ID of the video preview image.
            image_path (str): The path to the image file to upload.

        Returns:
            Dict[str, Any]: The response from the API.
        """
        if not self.asset_id:
            raise ValueError("Asset ID is required to upload a video preview image.")
        data = {
            "id": video_preview_image_id,
            "type": "image",
        }
        return self.client.upload_file(image_path, data)
