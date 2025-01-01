# python imports
from typing import Optional, Dict, Any, Generator

# local imports
from .api_client import FUGAClient


class FUGAArtist:
    """
    Represents an artist in the FUGA API.

    Provides methods for CRUD operations and managing artist identifiers.
    """

    def __init__(self, client: FUGAClient, artist_id: Optional[str] = None):
        """
        Initialize the FUGAArtist instance.

        Args:
            client (FUGAClient): The FUGA API client.
            artist_id (Optional[str]): The ID of the artist, if available.
        """
        self.client: FUGAClient = client
        self.artist_id: Optional[str] = artist_id

    @classmethod
    def fetch_list(
        cls,
        client: FUGAClient,
        page: int = 0,
        page_size: int = 10,
        limit: Optional[int] = None,
    ) -> Generator[Dict[str, Any], None, None]:
        """
        Fetch a paginated list of artists from FUGA.

        Args:
            client (FUGAClient): The FUGA API client instance.
            page (int): The page number to start fetching from (default is 1).
            page_size (int): The number of artists per page (default is 10).
            limit (Optional[int]): The maximum number of artists to fetch (default is None for no limit).

        Yields:
            Generator[Dict[str, Any], None, None]: Each artist's details as a dictionary.

        Raises:
            requests.HTTPError: If the API request fails.
        """
        endpoint = "/artists"
        params = {"page": page, "page_size": page_size}
        fetched_count = 0

        while True:
            response = client.request("GET", endpoint, params=params)
            artists = response.get("artist", [])

            for artist in artists:
                yield artist
                fetched_count += 1
                if limit and fetched_count >= limit:
                    return

            # Break if no more artists
            total = response.get("total", 0)
            if not artists or fetched_count >= total:
                break
            # Otherwise, move to the next page
            params["page"] += 1

    def fetch(self) -> Dict[str, Any]:
        """
        Fetch a single artist's details from FUGA.

        Returns:
            Dict[str, Any]: The artist's details.

        Raises:
            ValueError: If the artist ID is not set.
        """
        if not self.artist_id:
            raise ValueError("artist ID is required for retrieval.")
        return self.client.request("GET", f"/artists/{self.artist_id}")

    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new artist in FUGA.

        Args:
            data (Dict[str, Any]): The artist data for creation.

        Returns:
            Dict[str, Any]: The response from the API.
        """
        response = self.client.request("POST", "/artists", data=data)
        self.artist_id = response["id"]
        return response

    def update(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing artist in FUGA.

        Args:
            data (Dict[str, Any]): The artist data for update.

        Returns:
            Dict[str, Any]: The response from the API.

        Raises:
            ValueError: If the artist ID is not set.
        """
        if not self.artist_id:
            raise ValueError("artist ID is required for updates.")
        return self.client.request("PUT", f"/artists/{self.artist_id}", data=data)

    def delete(self) -> str:
        """
        Delete an artist from FUGA.

        Returns:
            str: The plain text response from the API.

        Raises:
            ValueError: If the artist ID is not set.
        """
        if not self.artist_id:
            raise ValueError("artist ID is required for deletion.")
        return self.client.request("DELETE", f"/artists/{self.artist_id}")

    def fetch_identifiers(self) -> Dict[str, Any]:
        """
        Fetch all identifiers for the artist.

        Returns:
            Dict[str, Any]: The identifiers for the artist.

        Raises:
            ValueError: If the artist ID is not set.
        """
        if not self.artist_id:
            raise ValueError("artist ID is required for retrieval.")
        return self.client.request("GET", f"/artists/{self.artist_id}/identifier")

    def fetch_identifier(self, identifier_id: str) -> Dict[str, Any]:
        """
        Fetch a single identifier for the artist.

        Args:
            identifier_id (str): The ID of the identifier to fetch.

        Returns:
            Dict[str, Any]: The identifier details.

        Raises:
            ValueError: If the artist ID is not set.
        """
        if not self.artist_id:
            raise ValueError("artist ID is required for retrieval.")
        return self.client.request(
            "GET", f"/artists/{self.artist_id}/identifier/{identifier_id}"
        )

    def create_identifier(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new identifier for the artist.

        Args:
            data (Dict[str, Any]): The identifier data for creation.

        Returns:
            Dict[str, Any]: The response from the API.

        Raises:
            ValueError: If the artist ID is not set.
        """
        if not self.artist_id:
            raise ValueError("artist ID is required for identifier creation.")
        return self.client.request(
            "POST", f"/artists/{self.artist_id}/identifier", data=data
        )

    def update_identifier(
        self, identifier_id: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update an existing identifier for the artist.

        Args:
            identifier_id (str): The ID of the identifier to update.
            data (Dict[str, Any]): The identifier data for update.

        Returns:
            Dict[str, Any]: The response from the API.

        Raises:
            ValueError: If the artist ID is not set.
        """
        if not self.artist_id:
            raise ValueError("artist ID is required for identifier updates.")
        return self.client.request(
            "PUT", f"/artists/{self.artist_id}/identifier/{identifier_id}", data=data
        )

    def delete_identifier(self, identifier_id: str) -> str:
        """
        Delete an identifier for the artist.

        Args:
            identifier_id (str): The ID of the identifier to delete.

        Returns:
            str: The plain text response from the API.

        Raises:
            ValueError: If the artist ID is not set.
        """
        if not self.artist_id:
            raise ValueError("artist ID is required for identifier deletion.")
        return self.client.request(
            "DELETE", f"/artists/{self.artist_id}/identifier/{identifier_id}"
        )
