import os
import json
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from instagrapi import Client
from caption_generator import generate_caption
from record_keeper import load_posted, save_posted
from helpers import download_next_reel, cleanup_downloaded


def authenticate_drive():
    from oauth2client.service_account import ServiceAccountCredentials

    creds_dict = json.loads(os.environ['GOOGLE_SERVICE_ACCOUNT'])
    scope = ['https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)

    gauth = GoogleAuth()
    gauth.credentials = credentials
    return GoogleDrive(gauth)


def main():
    print("Authenticating with Google Drive...")
    drive = authenticate_drive()

    print("Authenticating with Instagram...")
    cl = Client()
    session_str = os.environ.get("IG_SESSION")
    if session_str:
        with open("session.json", "w") as f:
            f.write(session_str)
        cl.load_settings("session.json")
        cl.get_timeline_feed()  # Validate session
        print("✅ Logged in using session.")
    else:
        raise ValueError("No IG_SESSION provided.")

    folder_ids = os.environ['DRIVE_FOLDER_IDS'].split(',')
    posted = load_posted()

    print("Looking for next reel to upload...")
    file_id, file_name = download_next_reel(drive, folder_ids, posted)
    if not file_id:
        print("All reels already posted!")
        return

    
    print("Generating caption...")
    caption = generate_caption(file_name)

    print("Uploading to Instagram...")
    cl.clip_upload(file_name, caption)

    print("Updating records...")
    posted.append(file_id)
    save_posted(posted)

    print("Cleaning up local file...")
    cleanup_downloaded(file_name)

    # ✅ New debug step to verify file creation (important for GitHub Actions)
    if os.path.exists("posted.json"):
        print("✅ posted.json saved successfully.")
    else:
        print("⚠️ Error: posted.json not found after saving!")

    print("✅ Upload complete!")


if __name__ == '__main__':
    main()
