import regex as re
from rich.console import Console
from rich.progress import track
from rich.live import Live
from rich.panel import Panel
from rich.style import Style

console = Console()


# Searches for current_frame "frame= [94]"
ffmpeg_current_frame_regex = re.compile(r"frame=\s*(?P<current_frame>\d+)") #current_frame

# Finds Current Framerate "fps = [22.6]"
ffmpeg_fps_regex = re.compile(r"fps=(?P<fps>\d+\.?\d+)") #fps

ffmpeg_filename_regex = re.compile(r"videos\\(?P<filename>.+\.\w+)") #filename


data = {}

def print_clean_line(line: str):
    clean_line = line.strip()
    if clean_line:
        console.print(clean_line)
        
def broadcast_command(line: str):
    console.print(line, style="b underline")

def basic_parser(line: str):
    print_clean_line(line)
