import os
import time
from instagrapi import Client
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from caption_generator import generate_caption
from dotenv import load_dotenv

# Load credentials from .env file
load_dotenv()

USERNAME = os.getenv("IG_USERNAME")
PASSWORD = os.getenv("IG_PASSWORD")

if not USERNAME or not PASSWORD:
    raise ValueError("Instagram credentials not set in .env file")

def login_instagram():
    cl = Client()
    cl.login(USERNAME, PASSWORD)
    print("✅ Logged into Instagram (2FA disabled).")
    return cl

def get_authenticated_drive():
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile("mycreds.txt")

    if gauth.credentials is None:
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        gauth.Refresh()
    else:
        gauth.Authorize()

    gauth.SaveCredentialsFile("mycreds.txt")
    drive = GoogleDrive(gauth)
    return drive

def get_ordered_videos_from_drive(drive):
    folder_ids = [
        "1GquOL-1HCnCuUy5-Ia667DSVIuZUrfro", "1TRn31FGxltDk62dc22aCytqchXsjIh0V",
        "1ViVTvGDF2xZBSjMFDqRVA0c144VnkzNX", "1oLunOX7LwtrMUcXuizMYJP4jXwG9G28C",
        "17wLMV5b637nzI58nrEVRx0CTf5rLSgnI", "166SE6ulnfwvD7lYRISzp5-L9WnYEe7o-",
        "1NAW6ICWIAmIpV6U7UKejXrFsNoeB_XBM", "1zT7AfLVXpa6xBNKyytwU3o4E8lmEifGD",
        "1WbmuBYqsfmygSJH0VvdAUeWyozUNGxHX"
    ]

    uploaded_files = set()
    if os.path.exists("uploaded.txt"):
        with open("uploaded.txt", "r") as f:
            uploaded_files = set(line.strip() for line in f)

    for folder_id in folder_ids:
        file_list = drive.ListFile({
            'q': f"'{folder_id}' in parents and trashed=false and mimeType contains 'video'"
        }).GetList()

        sorted_files = sorted(file_list, key=lambda x: x['title'])

        for file in sorted_files:
            if file['id'] not in uploaded_files:
                return file

    return None

def upload_reel_to_instagram(cl, video_path, caption):
    try:
        cl.clip_upload(video_path, caption)
        print("✅ Reel uploaded successfully.")
    except Exception as e:
        print("❌ Failed to upload reel:", e)

def mark_as_uploaded(file_id):
    with open("uploaded.txt", "a") as f:
        f.write(file_id + "\n")

if __name__ == "__main__":
    drive = get_authenticated_drive()
    file = get_ordered_videos_from_drive(drive)

    if file is None:
        print("✅ All videos already uploaded.")
        exit()

    print(f"📥 Downloading: {file['title']}")
    file.GetContentFile("reel.mp4")

    print("🧠 Generating caption...")
    caption = generate_caption("reel.mp4")

    print("🔐 Logging into Instagram...")
    cl = login_instagram()

    print("🚀 Uploading to Instagram...")
    upload_reel_to_instagram(cl, "reel.mp4", caption)

    print("📌 Marking video as uploaded...")
    mark_as_uploaded(file['id'])

    print("🧹 Waiting briefly before cleanup...")
    time.sleep(2)

    try:
        os.remove("reel.mp4")
        print("🧼 Local file deleted.")
    except PermissionError:
        print("⚠️ Could not delete reel.mp4. File may still be in use.")
