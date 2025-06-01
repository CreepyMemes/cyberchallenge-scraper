import os
import re
import json

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
