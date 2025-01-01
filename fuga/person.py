# python imports
from typing import Optional, Dict, Any, List, Generator

# local imports
from .api_client import FUGAClient


class FUGAPerson:
    """
    Represents a person in the FUGA API.

    Provides methods for CRUD operations and additional functionality such as
    publishing and updating territories.
    """

    def __init__(self, client: FUGAClient, person_id: Optional[str] = None):
        """
        Initialize the FUGAPerson instance.

        Args:
            client (FUGAClient): The FUGA API client instance.
            person_id (Optional[str]): The unique ID of the person, if available.
        """
        self.client: FUGAClient = client
        self.person_id: Optional[str] = person_id

    @classmethod
    def fetch_list(
        cls,
        client: FUGAClient,
        page: int = 0,
        page_size: int = 10,
        limit: Optional[int] = None,
    ) -> Generator[Dict[str, Any], None, None]:
        """
        Fetch a paginated list of people from FUGA.

        Args:
            client (FUGAClient): The FUGA API client instance.
            page (int): The page number to start fetching from (default is 1).
            page_size (int): The number of people per page (default is 10).
            limit (Optional[int]): The maximum number of people to fetch (default is None for no limit).

        Yields:
            Generator[Dict[str, Any], None, None]: Each person's details as a dictionary.

        Raises:
            requests.HTTPError: If the API request fails.
        """
        endpoint = "/people"
        params = {"page": page, "page_size": page_size}
        fetched_count = 0

        while True:
            response = client.request("GET", endpoint, params=params)
            people = response.get("person", [])

            for person in people:
                yield person
                fetched_count += 1
                if limit and fetched_count >= limit:
                    return

            # Break if no more people
            total = response.get("total", 0)
            if not people or fetched_count >= total:
                break
            # Otherwise, move to the next page
            params["page"] += 1

    def fetch(self) -> Dict[str, Any]:
        """
        Fetch a single person's details from FUGA.

        Returns:
            Dict[str, Any]: The person object from FUGA

        Raises:
            ValueError: If the person ID is not set.
        """
        if not self.person_id:
            raise ValueError("Person ID is required for retrieval.")
        return self.client.request("GET", f"/people/{self.person_id}")

    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new person in FUGA.

        Args:
            data (Dict[str, Any]): The person data for creation.

        Returns:
            Dict[str, Any]: The person object created in FUGA.
        """
        response = self.client.request("POST", "/people", data=data)
        self.person_id = response["id"]
        return response

    def update(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing person in FUGA.

        Args:
            data (Dict[str, Any]): The person data for update.

        Returns:
            Dict[str, Any]: The updated person object from FUGA.

        Raises:
            ValueError: If the person ID is not set.
        """
        if not self.person_id:
            raise ValueError("Person ID is required for updates.")
        return self.client.request("PUT", f"/people/{self.person_id}", data=data)

    def delete(self) -> str:
        """
        Delete a person from FUGA.

        Returns:
            str: The plain text response indicating successful deletion.

        Raises:
            ValueError: If the person ID is not set.
        """
        if not self.person_id:
            raise ValueError("Person ID is required for deletion.")
        return self.client.request("DELETE", f"/people/{self.person_id}")
