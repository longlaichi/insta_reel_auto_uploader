import os
import json
import random
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

POSTED_REELS_RECORD = "posted.json"

DRIVE_FOLDER_IDS = [
    "1GquOL-1HCnCuUy5-Ia667DSVIuZUrfro",
    "1TRn31FGxltDk62dc22aCytqchXsjIh0V",
    "1ViVTvGDF2xZBSjMFDqRVA0c144VnkzNX",
    "1oLunOX7LwtrMUcXuizMYJP4jXwG9G28C",
    "17wLMV5b637nzI58nrEVRx0CTf5rLSgnI",
    "166SE6ulnfwvD7lYRISzp5-L9WnYEe7o-",
    "1NAW6ICWIAmIpV6U7UKejXrFsNoeB_XBM",
    "1zT7AfLVXpa6xBNKyytwU3o4E8lmEifGD",
    "1WbmuBYqsfmygSJH0VvdAUeWyozUNGxHX"
]

def load_posted_files():
    if not os.path.exists(POSTED_REELS_RECORD):
        return []
    with open(POSTED_REELS_RECORD, "r") as f:
        return json.load(f)

def save_posted_file(filename):
    posted = load_posted_files()
    posted.append(filename)
    with open(POSTED_REELS_RECORD, "w") as f:
        json.dump(posted, f)

def authorize_drive():
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    return GoogleDrive(gauth)

def get_next_reel(posted_list):
    drive = authorize_drive()
    posted_set = set(posted_list)

    for folder_id in DRIVE_FOLDER_IDS:
        file_list = drive.ListFile({
            'q': f"'{folder_id}' in parents and trashed=false and mimeType contains 'video'"
        }).GetList()

        # Sort by name like reel1.mp4, reel2.mp4...
        sorted_files = sorted(file_list, key=lambda x: x['title'])

        for file in sorted_files:
            if file['title'] not in posted_set:
                local_path = os.path.join("downloads", file['title'])
                if not os.path.exists("downloads"):
                    os.makedirs("downloads")
                file.GetContentFile(local_path)
                return local_path, file['title']

    return None, None

def generate_caption_from_filename(filename):
    base_caption = [
        "Push your limits every single day.",
        "This is your sign to never give up.",
        "You’re capable of more than you know.",
        "Small steps, big dreams.",
        "Discipline > Motivation.",
        "If not now, then when?",
        "Hustle in silence, let success make the noise.",
        "You vs You — that’s the real game.",
        "Stay focused, stay hungry.",
        "Be legendary."
    ]
    hashtags = "#motivation #reels #inspiration #success #mindset #grind #focus #12to25"
    return random.choice(base_caption) + " " + hashtags
