import requests
from rdflib import Graph, Literal, RDF, URIRef
from rdflib.namespace import FOAF, DC

class SolidClient:
    """SolidClient class to interact with Solid PODs"""
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
        """Create a new note in Solid"""
        if not self.login():
            return False

        try:
            note_id = f"note-{len(self.get_notes_from_solid()) + 1}"
            note_url = f'{self.solid_pod_url}/public/{note_id}.ttl'
            note = URIRef(note_url)
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
        """Get all notes from Solid"""
        if not self.login():
            return []

        try:
            notes = []
            response = self.session.get(f'{self.solid_pod_url}/public/')
            if response.status_code != 200:
                return notes

            # Parse each note file
            for note_url in self.extract_note_urls(response.text):
                response = self.session.get(note_url)
                if response.status_code != 200:
                    continue

                graph = Graph()
                graph.parse(data=response.text, format='turtle')

                note_data = {"id": note_url.split('/')[-1]}
                for s, p, o in graph:
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
        except Exception as e:
            print(e)
            return []

    def update_note_in_solid(self, note_id, title, subject, content, date):
        """Update an existing note in Solid"""
        if not self.login():
            return False

        try:
            note_url = f'{self.solid_pod_url}/public/{note_id}.ttl'
            note = URIRef("note_url")
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

    def delete_note_in_solid(self, note_id):
        """Delete a note from Solid"""
        if not self.login():
            return False

        try:
            note_url = f'{self.solid_pod_url}/public/{note_id}.ttl'
            response = self.session.delete(note_url)
            return response.status_code == 200
        except Exception as e:
            print(e)
            return False

    def extract_note_urls(self, html_content):
        """Extract note URLs from HTML content (simplified)"""
        # This function should parse the HTML content and extract URLs of note files
        # Implement based on actual HTML structure, for example:
        # return [url for url in re.findall(r'href=["\'](note-\d+.ttl)["\']', html_content)]
        pass