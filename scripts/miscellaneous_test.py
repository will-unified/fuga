# python imports
import os
from dotenv import load_dotenv

# local imports
from fuga.api_client import FUGAClient
from fuga.miscellaneous import FUGAMisc

# set variables
load_dotenv()  # Load environment variables from .env file
API_URL = os.getenv("API_URL")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

# Initialize the FUGA API client
client = FUGAClient(API_URL, USERNAME, PASSWORD)
client.login()

# Init the misc class
misc = FUGAMisc(client)

# # Fetch all genres
# genres = misc.fetch_genres()
# for genre in genres:
#     print(genre)

# # Fetch all subgenres with a limit
# for subgenre in FUGAMisc.subgenre_list(client, limit=50):
#     print(subgenre)

# # Create a subgenre
# data = {"name": "TEST SUBGENRE"}
# res = misc.create_subgenre(data)
# print(res)
# subgenre_id = res["id"]

# # Delete the subgenre
# res = misc.delete_subgenre(subgenre_id)
# print(res)

# # Fetch all languages
# languages = misc.fetch_languages()
# for language in languages:
#     print(language)

# # Fetch all audio locales
# audio_locales = misc.fetch_audio_locales()
# for audio_locale in audio_locales:
#     print(audio_locale)

# # Fetch all contributor roles
# contributor_roles = misc.fetch_contributor_roles()
# for contributor_role in contributor_roles:
#     print(contributor_role)

# # Fetch all catalog tiers
# catalog_tiers = misc.fetch_catalog_tiers()
# for catalog_tier in catalog_tiers:
#     print(catalog_tier)

# # Fetch all instruments
# instruments = misc.fetch_instruments()
# for instrument in instruments:
#     print(instrument)

# # Fetch all territories
# territories = misc.fetch_territories()
# for territory in territories:
#     print(territory)

# # Fetch all encodings
# encodings = misc.fetch_encodings()
# for encoding in encodings:
#     print(encoding)

# # Fetch all lead times
# lead_times = misc.fetch_lead_times()
# for lead_time in lead_times:
#     print(lead_time)
