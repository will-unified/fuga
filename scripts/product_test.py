# python imports
import os
from dotenv import load_dotenv

# local imports
from fuga.api_client import FUGAClient
from fuga.product import FUGAProduct

# set variables
load_dotenv()  # Load environment variables from .env file
API_URL = os.getenv("API_URL")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

# Initialize the FUGA API client
client = FUGAClient(API_URL, USERNAME, PASSWORD)
client.login()

# # Fetch all products with a limit
# for product in FUGAProduct.fetch_list(client, limit=1):
#     print(product)

# Create a new product
product = FUGAProduct(client)
product_data = {"name": "New Album", "release_date": "2024-12-31"}
response = product.create(product_data)
print("Created Product:", response)

# Fetch product details
product.product_id = response["id"]
details = product.fetch()
print("Product Details:", details)

# Update product details
update_data = {"name": "Updated Album Name"}
updated_product = product.update(update_data)
print("Updated Product:", updated_product)

# Update territories
territories = ["US", "CA", "GB"]
updated_territories = product.update_territories(territories)
print("Updated Territories:", updated_territories)

# Assign barcode
barcode_response = product.assign_barcode()
print("Barcode Response:", barcode_response)

# Delete the product
delete_response = product.delete()
print("Delete Response:", delete_response)

# # Fetch live links
# product = FUGAProduct(client, product_id="1002645007453")
# response = product.fetch_live_links()
# print(f"Live Links for Product {product.product_id}:", response)

# # Fetch artworks
# artworks = product.fetch_artworks()
# print(f"Artworks for Product {product.product_id}:", artworks)
