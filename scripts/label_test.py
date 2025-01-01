# python imports
import os
from dotenv import load_dotenv

# local imports
from fuga.api_client import FUGAClient
from fuga.label import FUGALabel

# set variables
load_dotenv()  # Load environment variables from .env file
API_URL = os.getenv("API_URL")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
ORG_ID = os.getenv("ORG_ID")
APPLE_MUSIC_FUGA_ID = "1330598"

# local imports
from fuga.api_client import FUGAClient
from fuga.label import FUGALabel

# Initialize the FUGA API client
client = FUGAClient(API_URL, USERNAME, PASSWORD)
client.login()

# # Fetch all labels with a limit
# for label in FUGALabel.fetch_list(client, limit=50):
#     print(label)

# Create a new label
label = FUGALabel(client)
label_data = {
    "name": "TEST 1",
    "proprietary_id": "CM-ID-123",
    "organization_id": ORG_ID,
}
response = label.create(label_data)
print("Created Label:", response)

# Fetch label details
label.label_id = response["id"]
details = label.fetch()
print("Label Details:", details)

# Update label details
update_data = {"name": "TEST 1 Updated"}
updated_label = label.update(update_data)
print("Updated Label:", updated_label)

# Delete the label
delete_response = label.delete()
print("Delete Response:", delete_response)
