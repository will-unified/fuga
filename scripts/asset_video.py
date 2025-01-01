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

# Create a new asset
asset = FUGAAsset(client)
asset_data = {
    "name": "TEST VIDEO",
    "type": "MUSIC_VIDEO",
    #   "isrc": "string",
    #   "artists": [
    #     {
    #       "id": 0,
    #       "primary": true
    #     }
    #   ],
    #   "display_artist": "string",
    #   "asset_version": "string",
    #   "asset_catalog_tier": "BACK",
    #   "p_line_year": 0,
    #   "p_line_text": "string",
    #   "language": "string",
    #   "genre": "string",
    #   "subgenre": 0,
    #   "alternate_genre": "string",
    #   "alternate_subgenre": 0,
    #   "parental_advisory": "true",
    #   "recording_year": 0,
    #   "recording_location": "string",
    #   "audio_recording_isrc": "string",
    #   "rights_holder_name": "string",
    #   "country_of_recording": "string",
    #   "country_of_comissioning": "string",
    #   "rights_ownership_name": "string",
    #   "rights_contract_begin_date": "2024-12-30",
    #   "rights_claim": "NONE",
    #   "lyrics": "string",
    #   "preview_start": 0,
    #   "preview_length": 0,
    #   "audio_locale": "string",
    #   "mfit_email_address": "string",
    #   "movement_title": "string",
    #   "movement_number": 0,
    #   "classical_catalog": "string",
    #   "key": "string",
    #   "work": 0,
    #   "video_crop_top": 0,
    #   "video_crop_right": 0,
    #   "video_crop_bottom": 0,
    #   "video_crop_left": 0,
    #   "extra_1": "string",
    #   "extra_2": "string",
    #   "extra_3": "string",
    #   "extra_4": "string",
    #   "extra_5": "string",
    #   "extra_6": "string",
    #   "extra_7": "string",
    #   "extra_8": "string",
    #   "extra_9": "2024-12-30",
    #   "extra_10": "2024-12-30",
    #   "asset_release_date": "2024-12-30",
    #   "ratings": [
    #     {
    #       "value": "SPOTIFY_18_PLUS"
    #     }
    #   ]
}
created_asset = asset.create(asset_data)
print(f"Created Asset: {created_asset['name']}")

# Upload a video file
video_file_path = "files/spiritual_man_video.mov"
video_file_response = asset.upload_video(video_file_path)
print(f"Video Upload Response: {video_file_response}")

# upload video preview image
video_preview_image_id = created_asset["video_preview_image"]["id"]
video_preview_image_path = "files/spiritual_man_video_preview_image.png"
video_preview_image_response = asset.upload_video_preview_image(
    video_preview_image_id, video_preview_image_path
)
print(f"Video Preview Image Upload Response: {video_preview_image_response}")

# # Delete the asset
# delete_response = asset.delete()
# print(f"\nDeleted Asset: {delete_response}")
