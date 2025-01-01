# python imports
from typing import Optional, Dict, Any, Generator

# local imports
from .api_client import FUGAClient


class FUGAReleaseProject:
    """
    Represents a release project in the FUGA API.

    Provides methods for CRUD operations and managing release project identifiers.
    """

    def __init__(self, client: FUGAClient, release_project_id: Optional[str] = None):
        """
        Initialize the FUGAReleaseProject instance.

        Args:
            client (FUGAClient): The FUGA API client.
            release_project_id (Optional[str]): The ID of the release project, if available.
        """
        self.client: FUGAClient = client
        self.release_project_id: Optional[str] = release_project_id

    @classmethod
    def fetch_list(
        cls,
        client: FUGAClient,
        page: int = 0,
        page_size: int = 10,
        limit: Optional[int] = None,
    ) -> Generator[Dict[str, Any], None, None]:
        """
        Fetch a paginated list of release projects from FUGA.

        Args:
            client (FUGAClient): The FUGA API client instance.
            page (int): The page number to start fetching from (default is 1).
            page_size (int): The number of release projects per page (default is 10).
            limit (Optional[int]): The maximum number of release projects to fetch (default is None for no limit).

        Yields:
            Generator[Dict[str, Any], None, None]: Each release project's details as a dictionary.

        Raises:
            requests.HTTPError: If the API request fails.
        """
        endpoint = "/release_projects"
        params = {"page": page, "page_size": page_size}
        fetched_count = 0

        while True:
            response = client.request("GET", endpoint, params=params)
            release_projects = response.get("release_project", [])

            for release_project in release_projects:
                yield release_project
                fetched_count += 1
                if limit and fetched_count >= limit:
                    return

            # Break if no more release projects
            total = response.get("total", 0)
            if not release_projects or fetched_count >= total:
                break
            # Otherwise, move to the next page
            params["page"] += 1

    def fetch(self) -> Dict[str, Any]:
        """
        Fetch a single release project's details from FUGA.

        Returns:
            Dict[str, Any]: The release project's details.

        Raises:
            ValueError: If the release project ID is not set.
        """
        if not self.release_project_id:
            raise ValueError("release project ID is required for retrieval.")
        return self.client.request(
            "GET", f"/release_projects/{self.release_project_id}"
        )

    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new release project in FUGA.

        Args:
            data (Dict[str, Any]): The release project data for creation.

        Returns:
            Dict[str, Any]: The response from the API.
        """
        response = self.client.request("POST", "/release_projects", data=data)
        self.release_project_id = response["id"]
        return response

    def update(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing release project in FUGA.

        Args:
            data (Dict[str, Any]): The release project data for update.

        Returns:
            Dict[str, Any]: The response from the API.

        Raises:
            ValueError: If the release project ID is not set.
        """
        if not self.release_project_id:
            raise ValueError("release project ID is required for updates.")
        return self.client.request(
            "PUT", f"/release_projects/{self.release_project_id}", data=data
        )

    def delete(self) -> str:
        """
        Delete a release project from FUGA.

        Returns:
            str: The plain text response from the API.

        Raises:
            ValueError: If the release project ID is not set.
        """
        if not self.release_project_id:
            raise ValueError("release project ID is required for deletion.")
        return self.client.request(
            "DELETE", f"/release_projects/{self.release_project_id}"
        )

    def fetch_products(
        self,
        page: int = 0,
        page_size: int = 10,
        limit: Optional[int] = None,
    ) -> Generator[Dict[str, Any], None, None]:
        """
        Fetch a paginated list of release project products from FUGA.

        Args:
            page (int): The page number to start fetching from (default is 1).
            page_size (int): The number of products per page (default is 10).
            limit (Optional[int]): The maximum number of products to fetch (default is None for no limit).

        Yields:
            Generator[Dict[str, Any], None, None]: Each release project's products details as a dictionary.

        Raises:
            requests.HTTPError: If the API request fails.
        """
        endpoint = f"/release_projects/{self.release_project_id}/products"
        params = {"page": page, "page_size": page_size}
        fetched_count = 0

        while True:
            response = self.client.request("GET", endpoint, params=params)
            release_projects = response.get("product", [])

            for release_project in release_projects:
                yield release_project
                fetched_count += 1
                if limit and fetched_count >= limit:
                    return

            # Break if no more release projects
            total = response.get("total", 0)
            if not release_projects or fetched_count >= total:
                break
            # Otherwise, move to the next page
            params["page"] += 1

    def add_products(self, product_ids: list[str]) -> Dict[str, Any]:
        """
        Add products to a release project in FUGA.

        Args:
            product_ids (list[str]): The list of product IDs to add.

        Returns:
            Dict[str, Any]: The response from the API.

        Raises:
            ValueError: If the release project ID is not set.
        """
        if not self.release_project_id:
            raise ValueError("release project ID is required for adding products.")
        data = {"products_ids": product_ids}
        return self.client.request(
            "POST",
            f"/release_projects/{self.release_project_id}/products",
            data=data,
        )

    def remove_products(self, product_ids: list[str]) -> Dict[str, Any]:
        """
        Remove products from a release project in FUGA.

        Args:
            product_ids (list[str]): The list of product IDs to remove.

        Returns:
            Dict[str, Any]: The response from the API.

        Raises:
            ValueError: If the release project ID is not set.
        """
        if not self.release_project_id:
            raise ValueError("release project ID is required for removing products.")
        data = {"products_ids": product_ids}
        return self.client.request(
            "DELETE",
            f"/release_projects/{self.release_project_id}/products",
            data=data,
        )
