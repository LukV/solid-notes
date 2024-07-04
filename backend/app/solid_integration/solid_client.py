from .auth import SolidAccountClient
from .notes import SolidNoteClient

class SolidClient:
    def __init__(self, username, password, account_url, pod_url, token_url, container):
        self.username = username
        self.password = password
        self.account_url = account_url
        self.pod_url = pod_url
        self.token_url = token_url
        self.container = container
        self.account_client = SolidAccountClient(username, password, account_url, pod_url)

    async def authenticate(self):
        authorization = await self.account_client.login_to_account()
        my_id, secret, _ = await self.account_client.fetch_client_credential_token(authorization)
        private_key, public_jwk = self.account_client.generate_dpop_key_pair()
        access_token, _ = await self.account_client.request_access_token(my_id, secret, self.token_url, private_key, public_jwk)
        self.note_client = SolidNoteClient(self.pod_url, private_key, public_jwk, self.container)
        return access_token

    async def create_note_in_solid(self, note_id, title, subject, content, date):
        access_token = await self.authenticate()
        return await self.note_client.create_note_in_solid(access_token, note_id, title, subject, content, date)

    async def get_notes_from_solid(self):
        access_token = await self.authenticate()
        return await self.note_client.get_notes_from_solid(access_token)

    async def update_note_in_solid(self, note_id, title, subject, content, date):
        access_token = await self.authenticate()
        return await self.note_client.update_note_in_solid(access_token, note_id, title, subject, content, date)

    async def delete_note_in_solid(self, note_id):
        access_token = await self.authenticate()
        return await self.note_client.delete_note_in_solid(access_token, note_id)
