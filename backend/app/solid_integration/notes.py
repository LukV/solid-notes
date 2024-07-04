"""
This module provides classes to interact with Solid PODs for note handling.
"""
import logging
import uuid
import datetime
from typing import List, Dict, Any
import aiohttp
import jwt # pylint: disable=E0401
import rdflib
from rdflib import Graph, Literal, RDF, URIRef, Namespace
from rdflib.namespace import FOAF, DC
from .utils import normalize_htu, PREFERRED_SIGNING_ALG  

# Define namespaces
LDP = Namespace("http://www.w3.org/ns/ldp#")
POSIX = Namespace("http://www.w3.org/ns/posix/stat#")
IANA = Namespace("http://www.w3.org/ns/iana/media-types/text/turtle#")

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class SolidNoteClient:
    """
    SolidNoteClient class to handle note-related interactions with Solid PODs.
    """

    def __init__(self,
                 solid_pod_url: str,
                 private_key: Any,
                 public_jwk: Dict[str, Any],
                 container: str):
        """
        Initializes the SolidNoteClient.

        :param solid_pod_url: URL of the Solid POD.
        :param private_key: The private key object for DPoP.
        :param public_jwk: The public key as a JWK for DPoP.
        """
        self.solid_pod_url = solid_pod_url
        self.private_key = private_key
        self.public_jwk = public_jwk
        self.container = container

    def create_dpop_header(self, token_url: str, method: str) -> str:
        """
        Creates a DPoP header.

        :param token_url: The URL of the endpoint.
        :param method: HTTP method.
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
        return jwt.encode(dpop_header, self.private_key, algorithm=PREFERRED_SIGNING_ALG[0],
                          headers={"jwk": self.public_jwk, "typ": "dpop+jwt"})

    async def create_note_in_solid(self, access_token: str, note_id: str, title: str, subject: str,
                               content: str, date: str) -> bool:
        """
        Creates a new note in the Solid POD.

        :param access_token: Access token for authentication.
        :param note_id: ID of the note.
        :param title: Title of the note.
        :param subject: Subject of the note.
        :param content: Content of the note.
        :param date: Date of the note.
        :return: True if the note was created successfully, False otherwise.
        """
        try:
            note_url = f'{self.solid_pod_url}{self.container}{note_id}.ttl'
            note = URIRef(note_url)
            graph = Graph()

            # Bind the 'dc' prefix to the DC namespace
            graph.bind('dc', DC)

            # Add the triples
            graph.add((note, RDF.type, FOAF.Document))
            graph.add((note, DC.title, Literal(title)))
            graph.add((note, DC.subject, Literal(subject)))
            graph.add((note, DC.description, Literal(content)))
            graph.add((note, DC.date, Literal(date)))

            # Serialize the graph to Turtle format
            data = graph.serialize(format='turtle')

            dpop_header = self.create_dpop_header(note_url, 'PUT')
            headers = {
                'Content-Type': 'text/turtle',
                'Authorization': f'DPoP {access_token}',
                'DPoP': dpop_header
            }
            async with aiohttp.ClientSession() as session:
                async with session.put(note_url, data=data, headers=headers) as response:
                    return response.status in [201, 205]
        except (aiohttp.ClientError, aiohttp.ClientResponseError) as e:
            logging.error("HTTP client error while creating note: %s", e)
        except (rdflib.exceptions.Error, ValueError) as e:
            logging.error("RDF error while creating note: %s", e)
        return False

    async def get_notes_from_solid(self, access_token: str) -> List[Dict[str, Any]]:
        """
        Retrieves all notes from the Solid POD.

        :param access_token: Access token for authentication.
        :return: List of notes as dictionaries.
        """
        try:
            notes = []
            container_url = f'{self.solid_pod_url}{self.container}'
            dpop_header = self.create_dpop_header(f'{self.solid_pod_url}{self.container}', 'GET')
            async with aiohttp.ClientSession() as session:
                async with session.get(f'{self.solid_pod_url}{self.container}', headers={
                    'Authorization': f'DPoP {access_token}',
                    'DPoP': dpop_header
                }) as response:
                    if response.status != 200:
                        return notes
                    content = await response.text()
                    note_urls_metadata = await self.extract_note_urls(content, container_url)

                    for note_metadata in note_urls_metadata:
                        note_url = note_metadata['url']
                        mtime = note_metadata['mtime']
                        size = note_metadata['size']

                        dpop_header = self.create_dpop_header(note_url, 'GET')
                        async with session.get(note_url, headers={
                            'Authorization': f'DPoP {access_token}',
                            'DPoP': dpop_header
                        }) as note_response:
                            if note_response.status != 200:
                                continue
                            graph = Graph()
                            graph.parse(data=await note_response.text(), format='turtle')
                            note_data = {
                                "id": note_url.split('/')[-1].replace('.ttl', ''),
                                "mtime": mtime,
                                "size": size
                            }
                            for _, p, o in graph:
                                if p == DC.title:
                                    note_data["title"] = str(o)
                                elif p == DC.subject:
                                    note_data["subject"] = str(o)
                                elif p == DC.description:
                                    note_data["content"] = str(o)
                                elif p == DC.date:
                                    note_data["date"] = str(o)
                            notes.append(note_data)
            return notes
        except (aiohttp.ClientError, aiohttp.ClientResponseError) as e:
            logging.error("HTTP client error while fetching notes: %s", e)
        return []

    async def update_note_in_solid(self, access_token: str, note_id: str, title: str, subject: str,
                                   content: str, date: str) -> bool:
        """
        Updates an existing note in the Solid POD.

        :param access_token: Access token for authentication.
        :param note_id: ID of the note.
        :param title: Title of the note.
        :param subject: Subject of the note.
        :param content: Content of the note.
        :param date: Date of the note.
        :return: True if the note was updated successfully, False otherwise.
        """
        try:
            note_url = f'{self.solid_pod_url}{self.container}{note_id}.ttl'
            note = URIRef(note_url)
            graph = Graph()
            graph.add((note, RDF.type, FOAF.Document))
            graph.add((note, DC.title, Literal(title)))
            graph.add((note, DC.subject, Literal(subject)))
            graph.add((note, DC.description, Literal(content)))
            graph.add((note, DC.date, Literal(date)))
            data = graph.serialize(format='turtle')
            dpop_header = self.create_dpop_header(note_url, 'PUT')
            headers = {
                'Content-Type': 'text/turtle',
                'Authorization': f'DPoP {access_token}',
                'DPoP': dpop_header
            }
            async with aiohttp.ClientSession() as session:
                async with session.put(note_url, data=data, headers=headers) as response:
                    r = response.status
                    return response.status in [201, 205]
        except (aiohttp.ClientError, aiohttp.ClientResponseError) as e:
            logging.error("HTTP client error while updating note: %s", e)
        except (rdflib.exceptions.Error, ValueError) as e:
            logging.error("RDF error while updating note: %s", e)
        return False

    async def delete_note_in_solid(self, access_token: str, note_id: str) -> bool:
        """
        Deletes a note from the Solid POD.

        :param access_token: Access token for authentication.
        :param note_id: ID of the note.
        :return: True if the note was deleted successfully, False otherwise.
        """
        try:
            note_url = f'{self.solid_pod_url}{self.container}{note_id}.ttl'
            dpop_header = self.create_dpop_header(note_url, 'DELETE')
            async with aiohttp.ClientSession() as session:
                async with session.delete(note_url, headers={
                    'Authorization': f'DPoP {access_token}',
                    'DPoP': dpop_header
                }) as response:
                    return response.status in [201, 205]
        except (aiohttp.ClientError, aiohttp.ClientResponseError) as e:
            logging.error("HTTP client error while deleting note: %s", e)
        except (rdflib.exceptions.Error, ValueError) as e:
            logging.error("RDF error while deleting note: %s", e)
        return False

    async def extract_note_urls(self, content: str, base_url: str) -> List[Dict[str, Any]]:
        """
        Extracts note URLs along with their mtime and size from the given Turtle content.

        :param content: Turtle content as a string.
        :param base_url: Base URL to resolve relative URLs.
        :return: List of dictionaries containing note URLs and their metadata.
        """
        graph = Graph()
        graph.parse(data=content, format='turtle', publicID=base_url)

        notes_metadata = []

        for _, pred, obj in graph:
            if pred == LDP.contains:
                note_url = str(obj)
                mtime = graph.value(subject=obj, predicate=POSIX.mtime)
                size = graph.value(subject=obj, predicate=POSIX.size)
                notes_metadata.append({
                    'url': note_url,
                    'mtime': str(mtime),
                    'size': str(size)
                })

        return notes_metadata
