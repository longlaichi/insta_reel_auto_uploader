# record_keeper.py
import json, os

POSTED_FILE = "posted.json"

def load_posted():
    if os.path.exists(POSTED_FILE):
        try:
            with open(POSTED_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_posted(posted_list):
    with open(POSTED_FILE, "w") as f:
        json.dump(posted_list, f, indent=2)
