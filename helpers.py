import os

def download_next_reel(drive, folder_ids, posted_files):
    for folder_id in folder_ids:
        file_list = drive.ListFile({
            'q': f"'{folder_id}' in parents and trashed=false and mimeType='video/mp4'"
        }).GetList()

        # Sort lexicographically by title
        sorted_files = sorted(file_list, key=lambda x: x['title'])

        for file in sorted_files:
            if file['title'] not in posted_files:
                print(f"Downloading {file['title']} from folder {folder_id}")
                file.GetContentFile(file['title'])
                return file['title']
    return None

def cleanup_downloaded(file_name):
    try:
        os.remove(file_name)
        print(f"Removed local file: {file_name}")
    except FileNotFoundError:
        print(f"File not found: {file_name}")
