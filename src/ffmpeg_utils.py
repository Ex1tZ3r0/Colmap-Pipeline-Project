from pathlib import Path
from config import VIDEO_DIR, FFMPEG_EXE, FFPROBE_EXE, OUTPUT_DIR, read_cache, set_current_time, ensure_dir_exists
from src.executer import run_command

def detect_video_frames(media_files):
    
    if not isinstance(media_files, list):
        media_files = [media_files]
    
    for file_path in media_files:
        command = [
            str(FFPROBE_EXE),
            "-v",
            "error",
            "-select_streams",
            "v:0",
            "-show_entries",
            "stream=avg_frame_rate,r_frame_rate,nb_frames,width,height",
            str(file_path),
        ]
        run_command(command)
    
def extract_video_frames(media_files, proxy: bool = False):
    
    timestamp = read_cache("timestamp")
    
    if not isinstance(media_files, list):
        media_files = [media_files]
        
    for filepath in media_files:
        command = [
            str(FFMPEG_EXE),
            "-i", str(filepath),
        ]
        
        cuda = read_cache("enable_cuda")
        scale_filter = "scale=1280:1280:force_original_aspect_ratio=decrease"
        
        if cuda:
            command[1:1] = ["-hwaccel", "cuda",]
            
        if proxy:
            image_type = "proxy"
            command.extend(["-vf", scale_filter])
        else:
            image_type = "native"
        
        command.extend(["-q:v", "2"])    
        
        output_pattern = OUTPUT_DIR / f"{timestamp}" / "images" / f"{image_type}" / f"{image_type}_%04d.jpg"    
        
        ensure_dir_exists(output_pattern.resolve().parent)
        
        command.append(str(output_pattern))
        
        exported_frames = output_pattern
        
        run_command(command)
        return exported_frames