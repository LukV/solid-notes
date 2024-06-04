""" SolidClient class to interact with Solid PODs """
import requests
from rdflib import Graph, Literal, RDF, URIRef
from rdflib.namespace import FOAF, DC

class SolidClient:
    def __init__(self, username, password, solid_community_url, solid_pod_url):
        self.session = requests.Session()
        self.solid_community_url = solid_community_url
        self.solid_pod_url = solid_pod_url
        self.username = username
        self.password = password

    def login(self):
        login_url = f'{self.solid_community_url}/login/password'
        data = {
            'username': self.username,
            'password': self.password
        }
        response = self.session.post(login_url, data=data)
        return response.status_code == 200

    def create_note_in_solid(self, title, subject, content, date):
        if not self.login():
            return False

        try:
            note_url = f'{self.solid_pod_url}/public/note.ttl'
            note = URIRef("http://example.org/note")
            graph = Graph()
            graph.add((note, RDF.type, FOAF.Document))
            graph.add((note, DC.title, Literal(title)))
            graph.add((note, DC.subject, Literal(subject)))
            graph.add((note, DC.description, Literal(content)))
            graph.add((note, DC.date, Literal(date)))

            data = graph.serialize(format='turtle')
            headers = {
                'Content-Type': 'text/turtle'
            }
            response = self.session.put(note_url, data=data, headers=headers)
            return response.status_code == 201
        except Exception as e:
            print(e)
            return False

    def get_notes_from_solid(self):
        if not self.login():
            return []

        try:
            note_url = f'{self.solid_pod_url}/public/note.ttl'
            response = self.session.get(note_url)
            if response.status_code != 200:
                return []

            graph = Graph()
            graph.parse(data=response.text, format='turtle')
            notes = []
            for s, p, o in graph:
                if p == DC.title:
                    notes.append({"title": str(o)})
                elif p == DC.subject:
                    notes[-1]["subject"] = str(o)
                elif p == DC.description:
                    notes[-1]["content"] = str(o)
                elif p == DC.date:
                    notes[-1]["date"] = str(o)
            return notes
        except Exception as e:
            print(e)
            return []
