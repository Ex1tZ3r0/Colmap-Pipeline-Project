import json
import datetime as dt
from pathlib import Path
from src.exceptions import MissingBinaries


#Project Root
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
BIN_DIR = BASE_DIR / "bin"
SRC_DIR = BASE_DIR / "src"

VIDEO_DIR = BASE_DIR / "videos"
OUTPUT_DIR = BASE_DIR / "exports"

FFMPEG_DIR = BIN_DIR / "ffmpeg"
COLMAP_DIR = BIN_DIR / "colmap"
FFMPEG_EXE = FFMPEG_DIR / "bin" / "ffmpeg.exe"
FFPROBE_EXE = FFMPEG_DIR / "bin" / "ffprobe.exe"
COLMAP_EXE = COLMAP_DIR / "bin" / "colmap.exe"

CACHE_FILE = DATA_DIR / "cache.json"

#Create directories if missing function
def ensure_dir_exists(*directories: Path):
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)        

ensure_dir_exists(FFMPEG_DIR, COLMAP_DIR, DATA_DIR, VIDEO_DIR, OUTPUT_DIR)

#Basic IO for variable caching
def update_cache(key: str, value) -> None:
    """Sets a cache variable and returns None"""
    data = {}
    if CACHE_FILE.exists():
        with open(CACHE_FILE, "r", encoding="utf-8") as file_handle:
            try:
                data = json.load(file_handle)
            except json.JSONDecodeError:
                data = {}
    if isinstance(value, Path):
        value = str(value)
        
    data[key] = value
    
    ensure_dir_exists(CACHE_FILE.parent)
    with open(CACHE_FILE, "w", encoding="utf-8") as file_handle:
        json.dump(data, file_handle, indent=2)
        
def read_cache(key: str, default=None):
    """Reads cache.json and retrieves given key"""
    if not CACHE_FILE.exists():
        return default

    with open(CACHE_FILE, "r", encoding="utf-8") as file_handle:
        try:
            data = json.load(file_handle)
            return data.get(key, default)
        except json.JSONDecodeError:
            return default

def print_divider():
    print("\n" + "=" * 50 + "\n")
    
    
def confirm_binaries_present():
    required_bins = [COLMAP_EXE, FFMPEG_EXE, FFPROBE_EXE]
    print("Checking for required Binaries")
    for binary in required_bins:
        if not binary.exists():
            raise MissingBinaries(f"Could not find required binary: {binary.name}")
        else:
            print(f"Found {binary.name}")
            
def set_current_time():
    current_time = dt.datetime.now().strftime("%m-%d-%Y-%I_%M")
    update_cache("timestamp", current_time)