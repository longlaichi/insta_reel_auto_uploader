import os

def download_next_reel(drive, folder_ids, posted_ids):
    # posted_ids must be list of Drive file IDs (strings)
    for folder_id in folder_ids:
        file_list = drive.ListFile({
            "q": f"'{folder_id}' in parents and trashed=false and mimeType contains 'video'"
        }).GetList()

        # order by file name like reel1.mp4, reel2.mp4...
        sorted_files = sorted(file_list, key=lambda x: x["title"])

        for file in sorted_files:
            if file["id"] not in posted_ids:
                os.makedirs("downloads", exist_ok=True)
                local_path = os.path.join("downloads", file["title"])
                print(f"Downloading {file['title']} ({file['id']}) from folder {folder_id}")
                file.GetContentFile(local_path)
                # return id (for history), local file path (to upload), and human title (for caption)
                return file["id"], local_path, file["title"]
    return None, None, None

def cleanup_downloaded(file_path):
    try:
        os.remove(file_path)
        print(f"Removed local file: {file_path}")
    except FileNotFoundError:
        print(f"File not found for cleanup: {file_path}")
