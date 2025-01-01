# python imports
import os
from dotenv import load_dotenv

# local imports
from fuga.api_client import FUGAClient
from fuga.person import FUGAPerson

# set variables
load_dotenv()  # Load environment variables from .env file
API_URL = os.getenv("API_URL")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

# Initialize the FUGA API client
client = FUGAClient(API_URL, USERNAME, PASSWORD)
client.login()

# # Fetch all people with a limit
# for people in FUGAPerson.fetch_list(client, limit=1):
#     print(people)

# Create a new person
print("Creating a new person...")
person = FUGAPerson(client)
person_data = {"name": "TEST PERSON"}
created_person = person.create(person_data)
print(f"Created Person: {created_person['name']}\n")

# Fetch the person
fetched_person = person.fetch()
print(f"Fetched Person: {fetched_person['name']}\n")

# Update the person
update_data = {"name": "TEST PERSON UPDATED"}
updated_person = person.update(update_data)
print(f"Updated Person: {updated_person['name']}\n")

# Cleanup: Delete person
print("Deleting the person...")
delete_response = person.delete()
print(f"Deleted Person: {delete_response}")
