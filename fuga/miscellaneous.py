# python imports
from typing import Dict, Any, List, Generator, Optional

# local imports
from .api_client import FUGAClient


class FUGAMisc:
    """
    A class for interacting with miscellaneous FUGA API endpoints.
    """

    def __init__(self, client: FUGAClient):
        """
        Initialize the FUGAMisc instance.

        Args:
            client (FUGAClient): The FUGA API client instance.
        """
        self.client: FUGAClient = client

    def fetch_genres(self) -> List[Dict[str, Any]]:
        """
        Fetch all genres available in the FUGA system.

        Returns:
            List[Dict[str, Any]]: A list of genre dictionaries.
        """
        path = "/miscellaneous/genres"
        return self.client.request("GET", path)

    @classmethod
    def subgenre_list(
        cls,
        client: FUGAClient,
        page: int = 0,
        page_size: int = 10,
        limit: Optional[int] = None,
    ) -> Generator[Dict[str, Any], None, None]:
        """
        Fetch a paginated list of subgenres from FUGA.

        Args:
            client (FUGAClient): The FUGA API client instance.
            page (int): The page number to start fetching from (default is 1).
            page_size (int): The number of subgenres per page (default is 10).
            limit (Optional[int]): The maximum number of subgenres to fetch (default is None for no limit).

        Yields:
            Generator[Dict[str, Any], None, None]: Each subgenre's details as a dictionary.

        Raises:
            requests.HTTPError: If the API request fails.
        """
        endpoint = "/miscellaneous/subgenres"
        params = {"page": page, "page_size": page_size}
        fetched_count = 0

        while True:
            response = client.request("GET", endpoint, params=params)
            subgenres = response.get("subgenre", [])

            for subgenre in subgenres:
                yield subgenre
                fetched_count += 1
                if limit and fetched_count >= limit:
                    return

            # Break if no more subgenres
            total = response.get("total", 0)
            if not subgenres or fetched_count >= total:
                break
            # Otherwise, move to the next page
            params["page"] += 1

    def create_subgenre(self, subgenre_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new subgenre in the FUGA system.

        Args:
            subgenre_data (Dict[str, Any]): The subgenre data.

        Returns:
            Dict[str, Any]: The new subgenre object.
        """
        path = "/miscellaneous/subgenres"
        return self.client.request("POST", path, data=subgenre_data)

    def delete_subgenre(self, subgenre_id: str) -> Dict[str, Any]:
        """
        Delete a subgenre from the FUGA system.

        Args:
            subgenre_id (str): The unique ID of the subgenre.

        Returns:
            Dict[str, Any]: The response from the API.
        """
        path = f"/miscellaneous/subgenres/{subgenre_id}"
        return self.client.request("DELETE", path)

    def fetch_languages(self) -> List[Dict[str, Any]]:
        """
        Fetch all languages available in the FUGA system.

        Returns:
            List[Dict[str, Any]]: A list of language dictionaries.
        """
        path = "/miscellaneous/languages"
        return self.client.request("GET", path)

    def fetch_audio_locales(self) -> List[Dict[str, Any]]:
        """
        Fetch all audio locales available in the FUGA system.

        Returns:
            List[Dict[str, Any]]: A list of audio locale dictionaries.
        """
        path = "/miscellaneous/audio_locales"
        return self.client.request("GET", path)

    def fetch_contributor_roles(self) -> List[Dict[str, Any]]:
        """
        Fetch all contributor roles available in the FUGA system.

        Returns:
            List[Dict[str, Any]]: A list of contributor role dictionaries.
        """
        path = "/miscellaneous/contributor_roles"
        return self.client.request("GET", path)

    def fetch_catalog_tiers(self) -> List[Dict[str, Any]]:
        """
        Fetch all catalog tiers available in the FUGA system.

        Returns:
            List[Dict[str, Any]]: A list of catalog tier dictionaries.
        """
        path = "/miscellaneous/catalog-tiers"
        return self.client.request("GET", path)

    def fetch_instruments(self) -> List[Dict[str, Any]]:
        """
        Fetch all instruments available in the FUGA system.

        Returns:
            List[Dict[str, Any]]: A list of instrument dictionaries.
        """
        path = "/miscellaneous/instruments"
        return self.client.request("GET", path)

    def fetch_territories(self) -> List[Dict[str, Any]]:
        """
        Fetch all territories available in the FUGA system.

        Returns:
            List[Dict[str, Any]]: A list of territory dictionaries.
        """
        path = "/miscellaneous/territories"
        return self.client.request("GET", path)

    def fetch_encodings(self) -> List[Dict[str, Any]]:
        """
        Fetch all encodings available in the FUGA system.

        Returns:
            List[Dict[str, Any]]: A list of encoding dictionaries.
        """
        path = "/miscellaneous/encodings"
        return self.client.request("GET", path)

    def fetch_lead_times(self) -> List[Dict[str, Any]]:
        """
        Fetch all lead times available in the FUGA system.

        Returns:
            List[Dict[str, Any]]: A list of lead time dictionaries.
        """
        path = "/miscellaneous/lead_times"
        return self.client.request("GET", path)
