# python imports
import os
from dotenv import load_dotenv

# local imports
from fuga.api_client import FUGAClient
from fuga.product import FUGAProduct
from fuga.release_project import FUGAReleaseProject

# set variables
load_dotenv()  # Load environment variables from .env file
API_URL = os.getenv("API_URL")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
ORG_ID = os.getenv("ORG_ID")

# Initialize the FUGA API client
client = FUGAClient(API_URL, USERNAME, PASSWORD)
client.login()

# # Fetch all release projects with a limit
# for release_project in FUGAReleaseProject.fetch_list(client, limit=20):
#     print(release_project)

# Create a new release project
release_project = FUGAReleaseProject(client)
release_project_data = {
    "name": "TEST RELEASE PROJECT",
    "organization_id": ORG_ID,
    "code": "TEST CODE",
    # "description": "string",
    # "start_date": "2024-12-31",
    # "artist_id": 0,
}
response = release_project.create(release_project_data)
print(f"Created Release Project: {response['name']}\n")

# # Fetch release project details
# details = release_project.fetch()
# print("Release Project Details:", details)

# # Update release project details
# update_data = {"name": "TEST 1 Updated"}
# updated_release_project = release_project.update(update_data)
# print("Updated Release Project:", updated_release_project)

# Create Products
products = []
for i in range(3):
    product = FUGAProduct(client)
    product_data = {
        "name": f"TEST PRODUCT {i}",
    }
    created_product = product.create(product_data)
    products.append(product)
    print(f"Created Product: {created_product['name']}")

# Add both products to the release project
product_ids = [product.product_id for product in products]
added_products_res = release_project.add_products(product_ids)
print(f"\nAdded Products to Release Project: {added_products_res}")

# Remove the first product from the release project
print("\nTesting removing products from release project...")
removed_product_res = release_project.remove_products([product_ids[0]])
print(f"Removed Product from Release Project: {removed_product_res}\n")

# Fetch all release project products
for product in release_project.fetch_products():
    print(f"Currents Products: {product['name']}")

# Delete the release project
print("\nCleaning up...")
delete_response = release_project.delete()
print("Delete Release Project:", delete_response)

# Delete all the products
for product in products:
    delete_response = product.delete()
    print("Delete Response:", delete_response)
