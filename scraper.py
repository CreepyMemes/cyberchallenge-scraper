import os
import re
import json
import requests

# ----------- Config -------------

BASE_URL = "https://ctf.cyberchallenge.it" # Olicyber: "https://training.olicyber.it"
EMAIL = ""
PASSWORD  = ""


# ----------- Session and API abstraction class ------------

class Session:
    """
    Session class that authenticates and stores in tokens for requests to the API
    """
    def __init__(self, base_url: str, email: str, password: str):
        self.base_url = base_url
        self.session = requests.Session()
        self.token_auth = {}
        self.token_download = ""
        self.group = ""

        self._login(email, password)
    

    def _login(self, email: str, password: str):
        """
        Authenticates and stores session token and file download token.
        """
        resp = self.session.post(f"{self.base_url}/api/login", json={"email": email, "password": password})
        resp .raise_for_status()
        data = resp.json()

        token = data.get("token")
        files_token = data.get("filesToken")

        self.token_auth = {"authorization": f"Token {token}"}
        self.token_download = f"=&auth={files_token}"

        user_info = self.api_get("currentUser")
        self.group = user_info.get('group')


    def api_get(self, path: str) -> dict:
        """
        Performs an authenticated GET request to the API and returns the JSON response.
        """
        resp = self.session.get(f"{self.base_url}/api/{path}", headers=self.token_auth)
        resp.raise_for_status()

        return resp.json()


    def download_file(self, file_url: str, file_path: str):
        """
        Downloads a single file with the download token.
        """
        if not file_url.lower().startswith('/api/file'):
            return

        with open(file_path, 'wb') as f:
            resp = self.session.get(f"{self.base_url}{file_url}{self.token_download}")
            f.write(resp.content)


# ---------- Utility Functions ----------

def clean_filename(title: str) -> str:
    """
    Cleans the title from trash so it can be safely used as a filename.
    """
    return re.sub(r'[^a-zA-Z0-9_-]', '', title.replace(' ', '_'))


def get_challenge_dir(event: str, section: str, title: str) -> str:
    """
    Returns directory path for a challenge.
    """
    return os.path.join('challenges', clean_filename(event), clean_filename(section), clean_filename(title))


def ensure_dir(path):
    """
    Create a directory if it doesn't exist.
    """
    if not os.path.exists(path):
        os.makedirs(path)    


def save_json(path: str, data: dict):
    """
    Saves the given dict to a json file in the given path
    """
    with open(path, "w") as f:
        json.dump(data, f, indent=4)


# ---------- Challenge Processing ----------

def fetch_and_save_challenges(session: Session) -> dict:
    """
    Fetches and saves the metadata of all challenges in a JSON file.
    """
    data = session.api_get("challenges")
    save_json("challenges.json", data)
    return data


def download_files(session, files_dir, challenge_data, token_download):
    """
    Downloads all files attached to a challenge and saves them in it's subdirectory.
    """
    for challenge_file_data in challenge_data['files']: 
        session.download_file(challenge_file_data, files_dir)


def fetch_challenge_data(session: Session, challenge_id: int) -> dict:
    """
    Fetches challenge metadata from the API in JSON format
    """
    return session.api_get(f"challenges/{challenge_id}")


def fetch_challenge_hints(session: Session, challenge_hints: list) -> list:
    """
    Fetches all hints for the given challenge from the API as a List
    """
    return [session.api_get(f"hint/{hint['id']}") for hint in challenge_hints]


def process_challenge(session: Session, challenge: dict, event: str, section: str):
    """
    Process current given challenge, downloading it's metadata (in JSON format) and any attached files.
    """
    title = challenge["title"]
    challenge_dir = get_challenge_dir(event, section, title)
    ensure_dir(challenge_dir)

    challenge_data = fetch_challenge_data(session, challenge["id"])

    if session.group == "SUPERVISOR":
        challenge_data['hints'] = fetch_challenge_hints(session, challenge_data['hints'])

    save_json(os.path.join(challenge_dir, f"{clean_filename(title)}.json"), challenge_data)

    files_dir = os.path.join(challenge_dir, 'files')

    for file in challenge_data['files']: 
        ensure_dir(files_dir)
        file_path = os.path.join(files_dir, file['name'])
        session.download_file(file['url'], file_path)
    
    print(f'Done downloading: {title}')


def scrape_all(session: Session, challenge_data: dict):
    """
    Iterates through all challenges, downloading their metadata (in JSON format) and any attached files.
    Each challenge is stored in its own subdirectory within a central output folder.
    """
    for event in challenge_data['events']:
        for section in event['sections']:
            for challenge in section['challenges']:   
                process_challenge(session, challenge, event['name'], section['name'])


# ---------- Main ----------

def main():
    """
    Entrypoint for the challenges scraper
    """
    session = Session(BASE_URL, EMAIL, PASSWORD)
    challenges = fetch_and_save_challenges(session)
    scrape_all(session, challenges)


if __name__ == "__main__":
    main()