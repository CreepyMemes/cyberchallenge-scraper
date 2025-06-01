import os
from session import Session
from utils import clean_filename, ensure_dir, save_json, get_challenge_dir

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
