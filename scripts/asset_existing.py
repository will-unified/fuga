# python imports
import os
from dotenv import load_dotenv

# local imports
from fuga.api_client import FUGAClient
from fuga.asset import FUGAAsset

# set variables
load_dotenv()  # Load environment variables from .env file
API_URL = os.getenv("API_URL")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

# Initialize the FUGA API client
client = FUGAClient(API_URL, USERNAME, PASSWORD)
client.login()

# Fetch existing asset
asset = FUGAAsset(client, asset_id="1003060685471")
response = asset.fetch()
# print(f"Res: {response}")
# print(f"Fetched Asset: {response['name']}")

# upload video preview image
video_preview_image_id = response["video_preview_image"]["id"]
# video_preview_image_path = "files/spiritual_man_video_preview_image.png"
video_preview_image_path = "files/incorrect_image_size.png"
video_preview_image_response = asset.upload_video_preview_image(
    video_preview_image_id, video_preview_image_path
)
print(f"Video Preview Image Upload Response: {video_preview_image_response}")
