"""
Main module in to run auth and management of solid pods locally.
"""
import asyncio
import os
from dotenv import load_dotenv
from auth import SolidAccountClient  # pylint: disable=E0401
from notes import SolidNoteClient  # pylint: disable=E0401

# Load environment variables from .env file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../../.env'))

async def main():
    """Main function."""
    username = os.getenv('SOLID_USERNAME')
    password = os.getenv('SOLID_PASSWORD')
    solid_account_url = "http://localhost:3000/.account/"
    solid_pod_url = "http://localhost:3000/pod-2/"
    container = "notes/"

    account_client = SolidAccountClient(username, password, solid_account_url, solid_pod_url)

    authorization = await account_client.login_to_account()
    my_id, secret, _ = await account_client.fetch_client_credential_token(authorization)

    token_url = 'http://localhost:3000/.oidc/token'
    private_key, public_jwk = account_client.generate_dpop_key_pair()

    access_token, expires_in = await account_client. \
        request_access_token(my_id, secret, token_url, private_key, public_jwk)
    print(f"Access Token: {access_token}")
    print(f"Expires In: {expires_in}")

    note_client = SolidNoteClient(solid_pod_url, private_key, public_jwk, container)

    created = await note_client. \
        create_note_in_solid(access_token, "note3", "Sample Title",
                             "Sample Subject", "Sample Content", "2024-07-01")
    print(f"Note created: {created}")

    notes = await note_client.get_notes_from_solid(access_token)
    print(f"Retrieved notes: {notes}")

    updated = await note_client. \
        update_note_in_solid(access_token, "note2", "Updated Title",
                             "Updated Subject", "Updated Content", "2024-07-02")
    print(f"Note updated: {updated}")

    deleted = await note_client.delete_note_in_solid(access_token, "note3")
    print(f"Note deleted: {deleted}")

asyncio.run(main())