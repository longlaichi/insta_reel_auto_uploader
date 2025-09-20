# main.py
import os, json
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from instagrapi import Client
from caption_generator import generate_caption
from record_keeper import load_posted, save_posted
from helpers import download_next_reel, cleanup_downloaded

def authenticate_drive():
    from oauth2client.service_account import ServiceAccountCredentials
    creds_dict = json.loads(os.environ["GOOGLE_SERVICE_ACCOUNT"])
    scope = ["https://www.googleapis.com/auth/drive"]
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    gauth = GoogleAuth()
    gauth.credentials = credentials
    return GoogleDrive(gauth)

def main():
    print("Authenticating with Google Drive...")
    drive = authenticate_drive()

    print("Authenticating with Instagram (using saved session)...")
    cl = Client()
    session_str = os.environ.get("IG_SESSION")
    if not session_str:
        raise ValueError("No IG_SESSION provided in GitHub Secrets.")
    with open("session.json", "w") as f:
        f.write(session_str)
    cl.load_settings("session.json")
    cl.get_timeline_feed()  # validate
    print("✅ IG session OK.")

    # Folders from secrets, comma separated
    folder_ids = os.environ["DRIVE_FOLDER_IDS"].split(",")

    # Posted list = Drive file IDs
    posted_ids = load_posted()

    print("Looking for next reel to upload...")
    file_id, local_path, file_title = download_next_reel(drive, folder_ids, posted_ids)
    if not file_id:
        print("All reels already posted! ✅")
        return

    print("Generating caption...")
    caption = generate_caption(file_title)

    print(f"Uploading to Instagram: {file_title}")
    cl.clip_upload(local_path, caption)

    print("Updating history (posted.json)...")
    posted_ids.append(file_id)
    save_posted(posted_ids)

    print("Cleaning up local file...")
    cleanup_downloaded(local_path)

    # Quick check
    if os.path.exists("posted.json"):
        print("✅ posted.json saved.")
    else:
        print("⚠️ posted.json not found after save!")

    print("✅ Done.")

if __name__ == "__main__":
    main()
