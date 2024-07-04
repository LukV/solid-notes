"""
This module provides the class to interact with Solid PODs 
for authentication and account management.
"""
import json
import base64
import datetime
import uuid
from typing import Tuple, Dict, Any
import aiohttp
import jwt # pylint: disable=E0401
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.ec import SECP256R1
from .utils import normalize_htu, PREFERRED_SIGNING_ALG # pylint: disable=E0401

class SolidAccountClient:
    """
    SolidAccountClient class to handle account-related interactions with Solid PODs.
    """
    def __init__(self, username: str, password: str, solid_account_url: str, solid_pod_url: str):
        """
        Initializes the SolidAccountClient.

        :param username: Username for the Solid account.
        :param password: Password for the Solid account.
        :param solid_account_url: URL of the Solid account endpoint.
        :param solid_pod_url: URL of the Solid POD.
        """
        self.username = username
        self.password = password
        self.solid_account_url = solid_account_url
        self.solid_pod_url = solid_pod_url

    async def register_account(self) -> str:
        """
        Register a user account.

        :return: Authorization token as a string.
        """
        async with aiohttp.ClientSession() as session:
            # Get the account creation URL
            async with session.get(self.solid_account_url) as index_response:
                if index_response.status != 200:
                    print(f"Failed to fetch account creation URL. Status code: {index_response.status}")
                    return None
                
                index_data = await index_response.json()
                controls = index_data['controls']
                create_url = controls['account']['create']

                # Initial POST request to create the account
                headers = {
                    'Content-Type': 'application/json'
                }
                data = {}

                async with session.post(create_url, headers=headers, json=data) as response:
                    response_data = await response.json()

                    if response.status == 200:  # Adjusted based on the success response from curl
                        authorization = response_data.get('authorization')
                        return authorization
                    else:
                        return None
        
    async def register_password(self, authorization: str) -> tuple:
        """
        Registers authentication credentials.

        :param authorization: Authorization token.
        :return: Tuple containing a boolean indicating success and a dictionary with the response details.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(self.solid_account_url,
                                headers={'authorization': f'CSS-Account-Token {authorization}'}) as index_response:
                index_data = await index_response.json()
                controls = index_data['controls']
            
            password_url = controls['password']['create']
            payload = {
                'email': self.username,
                'password': self.password
            }
            
            async with session.post(password_url, 
                                    headers={'content-type': 'application/json', 
                                            'authorization': f'CSS-Account-Token {authorization}'},
                                    data=json.dumps(payload)) as response:
                password_data = await response.json()
            
            if response.status == 200:
                return (True, {'name': 'PasswordCreated', 'message': 'Successfully created password for this e-mail address.', 'statusCode': 200, 'errorCode': None, 'details': {}})
            else:
                return (False, password_data)
    
    async def login_to_account(self) -> str:
        """
        Logs into the Solid account and retrieves the authorization token.

        :return: Authorization token as a string.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(self.solid_account_url) as index_response:
                index_data = await index_response.json()
                controls = index_data['controls']
            login_url = controls['password']['login']
            login_payload = {
                'email': self.username,
                'password': self.password
            }
            async with session.post(login_url, headers={'content-type': 'application/json'},
                                    data=json.dumps(login_payload)) as response:
                login_data = await response.json()
                authorization = login_data['authorization']
            return authorization

    async def fetch_client_credential_token(self, authorization: str) -> Tuple[str, str, str]:
        """
        Requests a token from the Solid account.

        :param authorization: Authorization token.
        :return: Tuple containing the token ID, secret, and resource URL.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(self.solid_account_url,
                    headers={'authorization': f'CSS-Account-Token {authorization}'}) \
                        as index_response:
                index_data = await index_response.json()
                controls = index_data['controls']
            token_url = controls['account']['clientCredentials']
            token_payload = {
                'name': 'token',
                'webId': f'{self.solid_pod_url}profile/card#me'
            }
            async with session.post(token_url,
                                    headers={'authorization': f'CSS-Account-Token {authorization}',
                                             'content-type': 'application/json'},
                                    data=json.dumps(token_payload)) as response:
                token_data = await response.json()
                return token_data['id'], token_data['secret'], token_data['resource']

    def generate_dpop_key_pair(self) -> Tuple[Any, Dict[str, Any]]:
        """
        Generates a DPoP key pair.

        :return: Tuple containing the private key object and the public key as a JWK.
        """
        private_key = ec.generate_private_key(SECP256R1())
        public_key = private_key.public_key()
        public_numbers = public_key.public_numbers()
        public_jwk = {
            "kty": "EC",
            "crv": "P-256",
            "x": base64.urlsafe_b64encode(public_numbers.x.to_bytes(32, byteorder="big")) \
                .decode("utf-8").rstrip("="),
            "y": base64.urlsafe_b64encode(public_numbers.y.to_bytes(32, byteorder="big")) \
                .decode("utf-8").rstrip("="),
            "alg": PREFERRED_SIGNING_ALG[0],
            "use": "sig"
        }
        return private_key, public_jwk

    def create_dpop_header(self, token_url: str, method: str, private_key: Any,
                           public_jwk: Dict[str, Any]) -> str:
        """
        Creates a DPoP header.

        :param token_url: The URL of the token endpoint.
        :param method: HTTP method.
        :param private_key: The private key object.
        :param public_jwk: The public key as a JWK.
        :return: DPoP header as a string.
        """
        jti = str(uuid.uuid4())
        iat = int(datetime.datetime.now().timestamp())
        dpop_header = {
            "htu": normalize_htu(token_url),
            "htm": method.upper(),
            "jti": jti,
            "iat": iat
        }
        return jwt.encode(dpop_header, private_key, algorithm=PREFERRED_SIGNING_ALG[0],
                          headers={"jwk": public_jwk, "typ": "dpop+jwt"})

    async def request_access_token(self, my_id: str, secret: str, token_url: str, private_key: Any,
                                   public_jwk: Dict[str, Any]) -> Tuple[str, int]:
        """
        Requests an access token from the Solid account.

        :param id: Token ID.
        :param secret: Token secret.
        :param token_url: Token endpoint URL.
        :param private_key: DPoP private key object.
        :param public_jwk: DPoP public key as a JWK.
        :return: Tuple containing the access token and its expiration time in seconds.
        """
        auth_string = f"{my_id}:{secret}"
        auth_base64 = base64.b64encode(auth_string.encode()).decode()
        dpop_header = self.create_dpop_header(token_url, 'POST', private_key, public_jwk)
        body = 'grant_type=client_credentials&scope=webid'
        async with aiohttp.ClientSession() as session:
            async with session.post(token_url, headers={
                'authorization': f'Basic {auth_base64}',
                'content-type': 'application/x-www-form-urlencoded',
                'dpop': dpop_header
            }, data=body) as response:
                access_data = await response.json()
                return access_data['access_token'], access_data['expires_in']
