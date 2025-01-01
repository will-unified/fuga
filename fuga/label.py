# python imports
from typing import Optional, Dict, Any, Generator

# local imports
from .api_client import FUGAClient


class FUGALabel:
    """
    Represents a label in the FUGA API.

    Provides methods for CRUD operations and managing label identifiers.
    """

    def __init__(self, client: FUGAClient, label_id: Optional[str] = None):
        """
        Initialize the FUGALabel instance.

        Args:
            client (FUGAClient): The FUGA API client.
            label_id (Optional[str]): The ID of the label, if available.
        """
        self.client: FUGAClient = client
        self.label_id: Optional[str] = label_id

    @classmethod
    def fetch_list(
        cls,
        client: FUGAClient,
        page: int = 0,
        page_size: int = 10,
        limit: Optional[int] = None,
    ) -> Generator[Dict[str, Any], None, None]:
        """
        Fetch a paginated list of labels from FUGA.

        Args:
            client (FUGAClient): The FUGA API client instance.
            page (int): The page number to start fetching from (default is 1).
            page_size (int): The number of labels per page (default is 10).
            limit (Optional[int]): The maximum number of labels to fetch (default is None for no limit).

        Yields:
            Generator[Dict[str, Any], None, None]: Each label's details as a dictionary.

        Raises:
            requests.HTTPError: If the API request fails.
        """
        endpoint = "/labels"
        params = {"page": page, "page_size": page_size}
        fetched_count = 0

        while True:
            response = client.request("GET", endpoint, params=params)
            labels = response.get("label", [])

            for label in labels:
                yield label
                fetched_count += 1
                if limit and fetched_count >= limit:
                    return

            # Break if no more labels
            total = response.get("total", 0)
            if not labels or fetched_count >= total:
                break
            # Otherwise, move to the next page
            params["page"] += 1

    def fetch(self) -> Dict[str, Any]:
        """
        Fetch a single label's details from FUGA.

        Returns:
            Dict[str, Any]: The label's details.

        Raises:
            ValueError: If the label ID is not set.
        """
        if not self.label_id:
            raise ValueError("label ID is required for retrieval.")
        return self.client.request("GET", f"/labels/{self.label_id}")

    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new label in FUGA.

        Args:
            data (Dict[str, Any]): The label data for creation.

        Returns:
            Dict[str, Any]: The response from the API.
        """
        response = self.client.request("POST", "/labels", data=data)
        self.label_id = response["id"]
        return response

    def update(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing label in FUGA.

        Args:
            data (Dict[str, Any]): The label data for update.

        Returns:
            Dict[str, Any]: The response from the API.

        Raises:
            ValueError: If the label ID is not set.
        """
        if not self.label_id:
            raise ValueError("label ID is required for updates.")
        return self.client.request("PUT", f"/labels/{self.label_id}", data=data)

    def delete(self) -> str:
        """
        Delete a label from FUGA.

        Returns:
            str: The plain text response from the API.

        Raises:
            ValueError: If the label ID is not set.
        """
        if not self.label_id:
            raise ValueError("label ID is required for deletion.")
        return self.client.request("DELETE", f"/labels/{self.label_id}")
