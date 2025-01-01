# python imports
import os
from dotenv import load_dotenv

# local imports
from fuga.api_client import FUGAClient
from fuga.asset import FUGAAsset
from fuga.product import FUGAProduct

# set variables
load_dotenv()  # Load environment variables from .env file
API_URL = os.getenv("API_URL")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

# Initialize the FUGA API client
client = FUGAClient(API_URL, USERNAME, PASSWORD)
client.login()

# Create a new product
print("Creating a new product...")
product = FUGAProduct(client)
product_data = {"name": "New Album", "release_date": "2024-12-31"}
created_product = product.create(product_data)
print(f"Created Product: {created_product['name']}\n")

# Create and link assets to the product
print("Creating and linking assets to the product...")
track_names = ["TEST TRACK 1", "TEST TRACK 2", "TEST TRACK 3"]
assets = []

# Create assets
for track_name in track_names:
    asset = FUGAAsset(client)
    asset_data = {"name": track_name, "type": "TRACK"}
    created_asset = asset.create(asset_data)
    assets.append(created_asset)
    print(f"Created Asset: {created_asset['name']}")

# Add assets to the product with sequence numbers
for sequence, asset_data in enumerate(assets, start=1):
    asset = FUGAAsset(client, asset_data["id"])
    product.add_asset(asset, sequence=sequence)
    print(
        f"Linked Asset: {asset_data['name']} to Product {product.product_id} with Sequence {sequence}"
    )

# Create additional asset
new_asset = FUGAAsset(client)
new_asset_data = {"name": "TEST TRACK NEW", "type": "TRACK"}
created_new_asset = new_asset.create(new_asset_data)
assets.append(
    created_new_asset
)  # append new asset to the list of assets for deletion later
print(f"Created New Asset: {created_new_asset['name']}")

# Reorder the tracks
new_tracks = [
    {"id": assets[0]["id"], "sequence": 3},
    {"id": assets[1]["id"], "sequence": 2},
    {"id": created_new_asset["id"], "sequence": 1},
]
product.update_tracks(new_tracks)

print("\nFetching product assets...")
# Fetch and print product assets
product_assets = product.fetch_assets()
for asset in product_assets.get("asset", []):
    print(f"Sequence: {asset['sequence']} | Track Name: {asset['name']}")

# Cleanup: Delete assets and product
print("\nDeleting the product...")
delete_response = product.delete()
print(f"Deleted Product: {delete_response}")

print("\nDeleting all assets...")
for asset_data in assets:
    asset = FUGAAsset(client, asset_data["id"])
    delete_response = asset.delete()
    print(f"Deleted Asset: {asset_data['name']}")
