from pathlib import Path
from config import VIDEO_DIR
from src.exceptions import NoMedia

def scanForMediaFiles():
    
    print("Searching for compatible Media Files")
    compatible_formats = [".mp4", ".mkv", ".mov", ".avi"]
    media_files = []
    
    for video in VIDEO_DIR.iterdir():
        if video.is_file() and video.suffix.lower() in compatible_formats:
            media_files.append(video)
            print(f"Found {video.name}")
    
    if not media_files:
        raise NoMedia(f"No compatible media files found")

    return media_files