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

# Create a new product
product = FUGAProduct(client)
product_data = {"name": "TEST 1", "release_date": "2024-12-31"}
response = product.create(product_data)

# Upload a cover image
cover_image_id = response["cover_image"]["id"]
image_path = "files/LANKS_inoue.jpg"
image_response = product.upload_cover_image(cover_image_id, image_path)
print(f"Cover Image Upload Response: {image_response}")

# Replace with a new cover image
image_path = "https://storage.googleapis.com/cm-user-bucket/images/6a5213bc-5896-4527-98c4-2bb0bdfa1478.jpg"
image_response = product.upload_cover_image(cover_image_id, image_path)
print(f"Cover Image Replacement Upload Response: {image_response}")

# Delete the product
delete_response = product.delete()
print(f"Product Deletion Response: {delete_response}")

# # Fetch image - this is a binary file that you can upload to a cloud storage service
# product = FUGAProduct(client, product_id="1002645007453")
# response = product.fetch_image()
# print(f"Image for Product {product.product_id} fetched")
