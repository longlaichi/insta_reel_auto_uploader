import json
import os

RECORD_FILE = "posted.json"

def load_posted():
    if os.path.exists(RECORD_FILE):
        with open(RECORD_FILE, "r") as f:
            return json.load(f)
    return []

def save_posted(posted):
    with open(RECORD_FILE, "w") as f:
        json.dump(posted, f, indent=2)
