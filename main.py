import os
import json
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from instagrapi import Client
from caption_generator import generate_caption
from record_keeper import load_posted, save_posted
from helpers import download_next_reel, cleanup_downloaded

def authenticate_drive():
    gauth = GoogleAuth()
    
    creds_dict = json.loads(os.environ['GOOGLE_SERVICE_ACCOUNT'])
    gauth.credentials = gauth.LoadServiceConfigSettings()
    
    # Write creds to a temporary file
    temp_file = '/tmp/service_account.json'
    with open(temp_file, 'w') as f:
        json.dump(creds_dict, f)

    gauth.LoadCredentialsFile(temp_file)
    gauth.ServiceAuth()  # Use service account
    return GoogleDrive(gauth)

def main():
    print("Authenticating with Google Drive...")
    drive = authenticate_drive()

    print("Authenticating with Instagram...")
    cl = Client()
    cl.login(os.environ['IG_USERNAME'], os.environ['IG_PASSWORD'])

    folder_ids = os.environ['DRIVE_FOLDER_IDS'].split(',')
    posted = load_posted()

    print("Looking for next reel to upload...")
    file_name = download_next_reel(drive, folder_ids, posted)
    if not file_name:
        print("All reels already posted!")
        return

    print("Generating caption...")
    caption = generate_caption(file_name)

    print("Uploading to Instagram...")
    cl.clip_upload(file_name, caption)

    print("Updating records...")
    posted.append(file_name)
    save_posted(posted)

    print("Cleaning up local file...")
    cleanup_downloaded(file_name)
    print("✅ Upload complete!")

if __name__ == '__main__':
    main()
