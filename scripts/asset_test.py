# python imports
import os
from dotenv import load_dotenv

# local imports
from fuga.api_client import FUGAClient
from fuga.asset import FUGAAsset
from fuga.person import FUGAPerson
from fuga.publishing_house import FUGAPublishingHouse

# set variables
load_dotenv()  # Load environment variables from .env file
API_URL = os.getenv("API_URL")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

# Initialize the FUGA API client
client = FUGAClient(API_URL, USERNAME, PASSWORD)
client.login()

# # Fetch all assets with a limit
# for asset in FUGAAsset.fetch_list(client, limit=1):
#     print(asset)

# Create a new asset
asset = FUGAAsset(client)
asset_data = {
    "name": "TEST TRACK",
    "type": "TRACK",
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

# # Fetch asset details
# asset.asset_id = response["id"]
# details = asset.fetch()
# print("Asset Details:", details)

# # Update asset details
# update_data = {"name": "TEST TRACK Updated"}
# updated_asset = asset.update(update_data)
# print("Updated Asset:", updated_asset)

# Create persons for contributors
print("\nCreating new persons...")
person_names = ["TEST PERSON 1", "TEST PERSON 2", "TEST PERSON 3"]
persons = []
for person_name in person_names:
    person = FUGAPerson(client)
    person_data = {"name": person_name}
    created_person = person.create(person_data)
    persons.append(person)
    print(f"Created Person: {created_person['name']}")

# Add contributors to the asset
for person in persons:
    data = {"person": person.person_id, "role": "ENGINEER"}
    asset.add_contributor(data)
    print(f"Added Contributor: {person.person_id} to Asset {asset.asset_id}")

# # update or add contributors to the asset
# print(f"\nUpdating contributors to the asset {asset.asset_id}...")
# credits = [
#     {"person": "1001377563381", "role": "DJ"},
#     {"person": "1001584187208", "role": "DJ"},
# ]
# asset.create_or_update_contributors(credits)

# # Fetch asset contributors
# contributors = asset.fetch_contributors()
# for contributor in contributors:
#     print(
#         f"Contributor: {contributor['id']} | {contributor['person']['name']}| {contributor['role']}"
#     )

# # Clear existing contributors from the asset
# asset.remove_all_contributors()
# print(f"\nRemoved all contributors from Asset {asset.asset_id} for retrying...")

# # Re-add first 2 of contributors to the asset
# for person in persons[:2]:
#     data = {"person": person.person_id, "role": "DJ"}
#     asset.add_contributor(data)
#     print(f"Added Contributor: {person.person_id} to Asset {asset.asset_id}")

# # Fetch asset contributors
# contributors = asset.fetch_contributors()
# for contributor in contributors:
#     print(
#         f"Contributor: {contributor['id']} | {contributor['person']['name']}| {contributor['role']}"
#     )

# Add instrument performers to the asset
print("\nAdding instrument performers to the asset...")
for person in persons:
    data = {"person_id": person.person_id, "instrument": "GUITAR"}
    asset.add_instrument_performer(data)
    print(f"Added instrument performer: {person.person_id} to Asset {asset.asset_id}")

# update or create instrument performers to the asset
print(f"\nUpdating contributors to the asset {asset.asset_id}...")
credits = [
    {"person_id": "1001377563381", "instrument": "PIANO"},
    {"person_id": "1001584187208", "instrument": "PIANO"},
]
asset.create_or_update_instrument_performers(credits)

# # Fetch asset instrument performers
# instrument_performers = asset.fetch_instrument_performers()
# for instrument_performer in instrument_performers:
#     print(
#         f"Instrument performer: {instrument_performer['id']} | {instrument_performer['person']['name']}| {instrument_performer['instrument']}"
#     )

# # Clear existing instrument performers from the asset
# asset.remove_all_instrument_performers()
# print(f"Removed all instrument performers from Asset {asset.asset_id} for testing...")

# # Clear existing publishers (song splits) from the asset
# asset.remove_all_publishers()
# print(f"\nRemoved all publishers from Asset {asset.asset_id} for testing...")

# # Create a new publishing house
# print("Creating a new publishing house...")
# publishing_house = FUGAPublishingHouse(client)
# publishing_house_data = {"name": "TEST PUBLISHER"}
# created_publisher = publishing_house.create(publishing_house_data)
# print(f"Created Publisher: {created_publisher['name']}")

# # Add publishers (song credits) to the asset
# print("Adding publishers to the asset...")
# data = {
#     # "person_id": person.person_id,
#     "publishing_house": publishing_house.publishing_house_id,
# }
# print(f"publisher data: {data}")
# asset.add_publisher(data)
# print(f"Added publisher: {person.person_id} to Asset {asset.asset_id}")

# # Fetch asset publishers (song splits)
# publishers = asset.fetch_publishers()
# for publisher in publishers:
#     print(
#         f"Publishers: {publisher['id']} | {publisher['composer_or_lyricist']}| {publisher['publishing_house']['name']}"
#     )

# Delete the asset
delete_response = asset.delete()
print(f"\nDeleted Asset: {delete_response}")

# Cleanup: Delete the persons
print("\nDeleting the person...")
for person in persons:
    delete_response = person.delete()
    print(f"Deleted Person: {delete_response}")

# # Cleanup: Delete publishing house
# print("\nDeleting the publishing house...")
# delete_response = publishing_house.delete()
# print(f"Deleted publishing house: {delete_response}")
