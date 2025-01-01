# python imports
from typing import Optional, Dict, Any, List, Generator

# local imports
from .api_client import FUGAClient


class FUGAPublishingHouse:
    """
    Represents a publishing house in the FUGA API.

    Provides methods for CRUD operations and additional functionality such as
    publishing and updating territories.
    """

    def __init__(self, client: FUGAClient, publishing_house_id: Optional[str] = None):
        """
        Initialize the FUGAPublisher instance.

        Args:
            client (FUGAClient): The FUGA API client instance.
            publishing_house_id (Optional[str]): The unique ID of the publishing house, if available.
        """
        self.client: FUGAClient = client
        self.publishing_house_id: Optional[str] = publishing_house_id

    @classmethod
    def fetch_list(
        cls,
        client: FUGAClient,
        page: int = 0,
        page_size: int = 10,
        limit: Optional[int] = None,
    ) -> Generator[Dict[str, Any], None, None]:
        """
        Fetch a paginated list of publishing house from FUGA.

        Args:
            client (FUGAClient): The FUGA API client instance.
            page (int): The page number to start fetching from (default is 1).
            page_size (int): The number of publishing house per page (default is 10).
            limit (Optional[int]): The maximum number of publishing house to fetch (default is None for no limit).

        Yields:
            Generator[Dict[str, Any], None, None]: Each publishing house's details as a dictionary.

        Raises:
            requests.HTTPError: If the API request fails.
        """
        endpoint = "/publishing_houses"
        params = {"page": page, "page_size": page_size}
        fetched_count = 0

        while True:
            response = client.request("GET", endpoint, params=params)
            publishing_house = response.get("publishing_house", [])

            for publishing_house in publishing_house:
                yield publishing_house
                fetched_count += 1
                if limit and fetched_count >= limit:
                    return

            # Break if no more publishing_house
            total = response.get("total", 0)
            if not publishing_house or fetched_count >= total:
                break
            # Otherwise, move to the next page
            params["page"] += 1

    def fetch(self) -> Dict[str, Any]:
        """
        Fetch a single publishing house's details from FUGA.

        Returns:
            Dict[str, Any]: The publishing house object from FUGA

        Raises:
            ValueError: If the publishing house ID is not set.
        """
        if not self.publishing_house_id:
            raise ValueError("Publisher ID is required for retrieval.")
        return self.client.request(
            "GET", f"/publishing_houses/{self.publishing_house_id}"
        )

    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new publishing house in FUGA.

        Args:
            data (Dict[str, Any]): The publishing house data for creation.

        Returns:
            Dict[str, Any]: The publishing house object created in FUGA.
        """
        response = self.client.request("POST", "/publishing_houses", data=data)
        self.publishing_house_id = response["id"]
        return response

    def update(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing publishing house in FUGA.

        Args:
            data (Dict[str, Any]): The publishing house data for update.

        Returns:
            Dict[str, Any]: The updated publishing house object from FUGA.

        Raises:
            ValueError: If the publishing house ID is not set.
        """
        if not self.publishing_house_id:
            raise ValueError("Publisher ID is required for updates.")
        return self.client.request(
            "PUT", f"/publishing_houses/{self.publishing_house_id}", data=data
        )

    def delete(self) -> str:
        """
        Delete a publishing house from FUGA.

        Returns:
            str: The plain text response indicating successful deletion.

        Raises:
            ValueError: If the publishing house ID is not set.
        """
        if not self.publishing_house_id:
            raise ValueError("Publisher ID is required for deletion.")
        return self.client.request(
            "DELETE", f"/publishing_houses/{self.publishing_house_id}"
        )
