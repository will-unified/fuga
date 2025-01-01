# python imports
from typing import Optional, Dict, Any, List, Generator

# local imports
from .api_client import FUGAClient
from .asset import FUGAAsset


class FUGAProduct:
    """
    Represents a product in the FUGA API.

    Provides methods for CRUD operations and additional functionality such as
    publishing and updating territories.
    """

    def __init__(self, client: FUGAClient, product_id: Optional[str] = None):
        """
        Initialize the FUGAProduct instance.

        Args:
            client (FUGAClient): The FUGA API client instance.
            product_id (Optional[str]): The unique ID of the product, if available.
        """
        self.client: FUGAClient = client
        self.product_id: Optional[str] = product_id

    @classmethod
    def fetch_list(
        cls,
        client: FUGAClient,
        page: int = 0,
        page_size: int = 10,
        limit: Optional[int] = None,
    ) -> Generator[Dict[str, Any], None, None]:
        """
        Fetch a paginated list of products from FUGA.

        Args:
            client (FUGAClient): The FUGA API client instance.
            page (int): The page number to start fetching from (default is 1).
            page_size (int): The number of products per page (default is 10).
            limit (Optional[int]): The maximum number of products to fetch (default is None for no limit).

        Yields:
            Generator[Dict[str, Any], None, None]: Each product's details as a dictionary.

        Raises:
            requests.HTTPError: If the API request fails.
        """
        endpoint = "/products"
        params = {"page": page, "page_size": page_size}
        fetched_count = 0

        while True:
            response = client.request("GET", endpoint, params=params)
            products = response.get("product", [])

            for product in products:
                yield product
                fetched_count += 1
                if limit and fetched_count >= limit:
                    return

            # Break if no more products
            total = response.get("total", 0)
            if not products or fetched_count >= total:
                break
            # Otherwise, move to the next page
            params["page"] += 1

    def fetch(self) -> Dict[str, Any]:
        """
        Fetch a single product's details from FUGA.

        Returns:
            Dict[str, Any]: The product object from FUGA

        Raises:
            ValueError: If the product ID is not set.
        """
        if not self.product_id:
            raise ValueError("Product ID is required for retrieval.")
        return self.client.request("GET", f"/products/{self.product_id}")

    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new product in FUGA.

        Args:
            data (Dict[str, Any]): The product data for creation.

        Returns:
            Dict[str, Any]: The product object created in FUGA.
        """
        response = self.client.request("POST", "/products", data=data)
        self.product_id = response["id"]
        return response

    def update(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing product in FUGA.

        Args:
            data (Dict[str, Any]): The product data for update.

        Returns:
            Dict[str, Any]: The updated product object from FUGA.

        Raises:
            ValueError: If the product ID is not set.
        """
        if not self.product_id:
            raise ValueError("Product ID is required for updates.")
        return self.client.request("PUT", f"/products/{self.product_id}", data=data)

    def delete(self) -> str:
        """
        Delete a product from FUGA.

        Returns:
            str: The plain text response indicating successful deletion.

        Raises:
            ValueError: If the product ID is not set.
        """
        if not self.product_id:
            raise ValueError("Product ID is required for deletion.")
        return self.client.request("DELETE", f"/products/{self.product_id}")

    def publish(self) -> Dict[str, Any]:
        """
        Publish a product in FUGA and mark it as ready for delivery.

        Returns:
            Dict[str, Any]: The published product object from FUGA.

        Raises:
            ValueError: If the product ID is not set.
        """
        if not self.product_id:
            raise ValueError("Product ID is required for publishing.")
        return self.client.request("POST", f"/products/{self.product_id}/publish")

    def assign_barcode(self) -> Dict[str, Any]:
        """
        Assign a barcode to a product in FUGA.

        Returns:
            Dict[str, Any]: The product object with a freshly assigned barcode.

        Raises:
            ValueError: If the product ID is not set.
        """
        if not self.product_id:
            raise ValueError("Product ID is required for assigning a barcode.")
        return self.client.request("POST", f"/products/{self.product_id}/barcode")

    def fetch_image(self, size: str = "full_size") -> Dict[str, Any]:
        """
        Fetch the image associated with a product in FUGA.

        Returns:
            Dict[str, Any]: The image object associated with the product.

        Raises:
            ValueError: If the product ID is not set.
        """
        if not self.product_id:
            raise ValueError("Product ID is required for retrieval.")
        return self.client.request("GET", f"/products/{self.product_id}/image/{size}")

    def fetch_artworks(self):
        """
        Fetch the artworks for a product in FUGA.

        Returns:
            Dict[str, Any]: The artworks for the product.

        Raises:
            ValueError: If the product ID is not set.
        """
        if not self.product_id:
            raise ValueError("Product ID is required for retrieval.")
        return self.client.request("GET", f"/products/{self.product_id}/artworks")

    def fetch_live_links(self):
        """
        Fetch the live links for a product in FUGA.

        Returns:
            Dict[str, Any]: The live links for the product.

        Raises:
            ValueError: If the product ID is not set.
        """
        if not self.product_id:
            raise ValueError("Product ID is required for retrieval.")
        return self.client.request("GET", f"/products/{self.product_id}/live_links")

    def update_territories(self, territories: List[str]) -> Dict[str, Any]:
        """
        Update the territories for a product in FUGA.

        Args:
            territories (List[str]): A list of territory codes to assign to the product.

        Returns:
            Dict[str, Any]: The updated territories information from the API.

        Raises:
            ValueError: If the product ID is not set.
        """
        if not self.product_id:
            raise ValueError("Product ID is required for updating territories.")
        return self.client.request(
            "PUT", f"/products/{self.product_id}/territories", data=territories
        )

    def fetch_assets(self) -> List[Dict[str, Any]]:
        """
        Fetch the assets associated with a product in FUGA.

        Returns:
            List[Dict[str, Any]]: The list of assets associated with the product.

        Raises:
            ValueError: If the product ID is not set.
        """
        if not self.product_id:
            raise ValueError("Product ID is required for retrieval.")
        return self.client.request("GET", f"/products/{self.product_id}/assets")

    def add_asset(self, asset: FUGAAsset, sequence: int) -> Dict[str, Any]:
        """
        Add an asset to a product in FUGA.

        Args:
            asset_id (str): The unique ID of the asset to add to the product.

        Returns:
            Dict[str, Any]: The updated product object with the added asset.

        Raises:
            ValueError: If the product ID is not set.
        """
        if not self.product_id:
            raise ValueError("Product ID is required for adding an asset.")
        return self.client.request(
            "POST",
            f"/products/{self.product_id}/assets",
            data={"id": asset.asset_id, "sequence": sequence},
        )

    def update_tracks(self, new_tracks: List[Dict[str, Any]]) -> None:
        """
        Update the tracks (assets) for the product in FUGA.

        This method handles:
        - Adding new tracks that are not currently associated with the product.
        - Removing tracks that are no longer in the new order.
        - Reordering tracks based on the new order.

        Args:
            new_tracks (List[Dict[str, Any]]): A list of dictionaries representing the desired state of tracks.
                Each dictionary should have:
                    - `id` (str): The ID of the track.
                    - `sequence` (int): The desired sequence number.

        Raises:
            ValueError: If the product ID is not set.
        """
        if not self.product_id:
            raise ValueError("Product ID is required to update tracks.")

        # Fetch current assets
        current_assets = self.fetch_assets()["asset"]
        current_ids = {asset["id"] for asset in current_assets}

        # Determine tracks to add, remove, and reorder
        new_ids = {track["id"] for track in new_tracks}
        tracks_to_add = [
            track for track in new_tracks if track["id"] not in current_ids
        ]
        tracks_to_remove = [
            asset["id"] for asset in current_assets if asset["id"] not in new_ids
        ]
        tracks_to_reorder = [
            track for track in new_tracks if track["id"] in current_ids
        ]

        # Add new tracks
        for track in tracks_to_add:
            self.add_asset(FUGAAsset(self.client, track["id"]), track["sequence"])
            print(f"Added track {track['id']} with sequence {track['sequence']}.")

        # Remove tracks no longer in the list
        for track_id in tracks_to_remove:
            self.remove_asset(track_id)
            print(f"Removed track {track_id}.")

        # Reorder existing tracks
        for track in tracks_to_reorder:
            self.update_asset_sequence(track["id"], track["sequence"])
            print(f"Reordered track {track['id']} to sequence {track['sequence']}.")

    def add_asset(self, asset: FUGAAsset, sequence: int) -> Dict[str, Any]:
        """
        Add an asset (track) to the product in FUGA.

        Args:
            asset (FUGAAsset): The asset to add to the product.
            sequence (int): The sequence number for the asset.

        Returns:
            Dict[str, Any]: The response from the API.

        Raises:
            ValueError: If the product ID is not set.
        """
        if not self.product_id:
            raise ValueError("Product ID is required to add an asset.")
        return self.client.request(
            "POST",
            f"/products/{self.product_id}/assets",
            data={"id": asset.asset_id, "sequence": sequence},
        )

    def remove_asset(self, asset_id: str) -> str:
        """
        Remove an asset (track) from the product in FUGA.

        Args:
            asset_id (str): The ID of the asset to remove.

        Returns:
            str: The response from the API.

        Raises:
            ValueError: If the product ID is not set.
        """
        if not self.product_id:
            raise ValueError("Product ID is required to remove an asset.")
        return self.client.request(
            "DELETE", f"/products/{self.product_id}/assets/{asset_id}"
        )

    def update_asset_sequence(self, asset_id: str, sequence: int) -> Dict[str, Any]:
        """
        Update the sequence number of a specific asset (track) in the product.

        Args:
            asset_id (str): The ID of the asset to update.
            sequence (int): The new sequence number.

        Returns:
            Dict[str, Any]: The response from the API.

        Raises:
            ValueError: If the product ID is not set.
        """
        if not self.product_id:
            raise ValueError("Product ID is required to update asset sequence.")
        endpoint = f"/products/{self.product_id}/assets/{asset_id}/position/{sequence}"
        return self.client.request("PUT", endpoint, data={})

    def upload_cover_image(self, entity_id: str, image_path: str) -> Dict[str, Any]:
        """
        Upload an image for the product in FUGA.

        Args:
            entity_id (str): The ID of the cover_image entity to associate the image with.
            image_path (str): The path to the image file to upload.

        Returns:
            Dict[str, Any]: The response from the API.
        """
        if not self.product_id:
            raise ValueError("Product ID is required to upload an image.")
        data = {
            "id": entity_id,
            "type": "image",
        }
        return self.client.upload_file(image_path, data)
