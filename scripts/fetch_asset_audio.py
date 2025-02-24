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

# fetch existing asset
asset = FUGAAsset(client, asset_id="1001377699749")

# fetch asset audio - this is a binary file that you can upload to a cloud storage service
asset_audio = asset.fetch_audio()


# Check audio format
def identify_audio_format(file_binary):
    # Read the first 12 bytes of the file
    header = file_binary[:12]

    # Check for WAV format
    if header[:4] == b"RIFF" and header[8:12] == b"WAVE":
        return "WAV"

    # Check for MP3 format (ID3 header or sync bytes)
    if header[:3] == b"ID3" or header[:2] == b"\xFF\xFB" or header[:2] == b"\xFF\xF3":
        return "MP3"

    return "Unknown format"


file_format = identify_audio_format(asset_audio)
print(f"The audio file format is: {file_format}")

# # Download file to /output dir (create if it doesn't exist)
# output_dir = "output"
# os.makedirs(output_dir, exist_ok=True)
# output_path = os.path.join(output_dir, "asset_audio2.WAV")
# with open(output_path, "wb") as f:
#     f.write(asset_audio)
#     print(f"\nAsset Audio downloaded to {output_path}")
