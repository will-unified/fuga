# python imports
import os
from dotenv import load_dotenv

# local imports
from fuga.api_client import FUGAClient
from fuga.publishing_house import FUGAPublishingHouse

# set variables
load_dotenv()  # Load environment variables from .env file
API_URL = os.getenv("API_URL")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

# Initialize the FUGA API client
client = FUGAClient(API_URL, USERNAME, PASSWORD)
client.login()

# # Fetch all publishing houses with a limit
# for publisher in FUGAPublishingHouse.fetch_list(client, limit=1):
#     print(publisher)

# Create a new publishing house
print("Creating a new publishing house...")
publishing_house = FUGAPublishingHouse(client)
publishing_house_data = {"name": "TEST PUBLISHER"}
created_publisher = publishing_house.create(publishing_house_data)
print(f"Created Publisher: {created_publisher['name']}\n")

# Fetch the publishing house
fetched_publisher = publishing_house.fetch()
print(f"Fetched Publisher: {fetched_publisher['name']}\n")

# Update the publishing house
update_data = {"name": "TEST PUBLISHER UPDATED"}
updated_publisher = publishing_house.update(update_data)
print(f"Updated Publisher: {updated_publisher['name']}\n")

# Cleanup: Delete publishing house
print("Deleting the publishing house...")
delete_response = publishing_house.delete()
print(f"Deleted publishing house: {delete_response}")
