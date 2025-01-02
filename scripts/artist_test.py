# python imports
import os
from dotenv import load_dotenv

# local imports
from fuga.api_client import FUGAClient
from fuga.artist import FUGAArtist

# set variables
load_dotenv()  # Load environment variables from .env file
API_URL = os.getenv("API_URL")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
ORG_ID = os.getenv("ORG_ID")
SPOTIFY_FUGA_ID = "746109"
APPLE_MUSIC_FUGA_ID = "1330598"

# local imports
from fuga.api_client import FUGAClient
from fuga.artist import FUGAArtist

# Initialize the FUGA API client
client = FUGAClient(API_URL, USERNAME, PASSWORD)
client.login()

# # Fetch all artists with a limit
# for artist in FUGAArtist.fetch_list(client, limit=50):
#     print(artist)

# Create a new artist
artist = FUGAArtist(client)
artist_data = {
    "name": "TEST 1",
    "proprietary_id": "CM-ID-123",
    "organization_id": ORG_ID,
}
response = artist.create(artist_data)
print(f"Create artist: {response['name']}")

# # Fetch artist details
# artist.artist_id = response["id"]
# details = artist.fetch()
# print("Artist Details:", details)

# # Update artist details
# update_data = {"name": "TEST 1 Updated"}
# updated_artist = artist.update(update_data)
# print("Updated Artist:", updated_artist)

# Create artist identifier
identifier_data = {
    "issuingOrganization": APPLE_MUSIC_FUGA_ID,
    "identifier": "123456789",
    "newForIssuingOrg": False,
}
identifier_response = artist.create_identifier(identifier_data)
print(
    f"Created identifer {identifier_response['identifier']} for platform {identifier_response['issuingOrganization']['name']} (is new for issuing org: {identifier_response['newForIssuingOrg']})"
)
identifier_id = identifier_response["id"]

# # update artist identifier
# update_identifier_data = {"identifier": "412778295", "newForIssuingOrg": False}
# updated_identifier = artist.update_identifier(identifier_id, update_identifier_data)
# print("Updated Identifier:", updated_identifier)

# # Fetch artist identifiers
# identifiers = artist.fetch_identifiers()
# print("Identifiers:", identifiers)

# # Fetch artist identifier
# identifier = artist.fetch_identifier(identifier_id)
# print("Identifier Details:", identifier)

# Create or update artist identifiers
print("\nCreating or updating identifiers to the asset...")
data = [
    {
        "issuingOrganization": SPOTIFY_FUGA_ID,  # Create Spotify
        "identifier": None,
        "newForIssuingOrg": True,
    },
    {
        "issuingOrganization": APPLE_MUSIC_FUGA_ID,  # Skip as it's the same as FUGA
        "identifier": None,
        "newForIssuingOrg": True,
    },
]
res = artist.update_or_create_identifiers(data)
print("\nCreate or Update Identifiers Response:", res)

# Delete artist identifiers
delete_identifiers_response = artist.delete_identifiers()
print("\nDelete Identifiers Response:", delete_identifiers_response)

# Delete the artist
delete_response = artist.delete()
print("Delete Response:", delete_response)
