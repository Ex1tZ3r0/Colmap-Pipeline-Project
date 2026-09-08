from pathlib import Path
from config import print_divider, confirm_binaries_present, read_cache, update_cache, set_current_time
from src.exceptions import MissingBinaries, NoMedia, FileProcessingError
from src.media_utils import scanForMediaFiles
from src.ffmpeg_utils import detect_video_frames, extract_video_frames
from src.colmap_utils import feature_extractor, sequential_matcher, view_graph_calibrator, global_mapper, point_triangulator, point_filtering, model_orientation_aligner, convert_model
from src.executer import run_command

def main():
    print_divider()
    print(f"Video to Blender camera pipline")
    print_divider()
    
    try:
        confirm_binaries_present()
        print("All Required Binaries found, Starting Pipeline...")
    except MissingBinaries as err:
        print(f"ERROR: {err}")
        return
    
    try:
        media_files = scanForMediaFiles()
    except NoMedia as err:
        print(f"ERROR: {err}")
        return
    
    def ask_cuda():
        while True:
            user_input = input("Enable CUDA Acceleration? \n (Y/N)\n").strip().lower()
            
            if user_input in ["y", "yes"]:
                print ("\nCUDA Acceleration Enabled.")
                print_divider()
                update_cache("enable_cuda", True)
                return
            
            if user_input in ["n", "no"]:
                print ("\nCUDA Acceleration Disabled.")
                print_divider()
                update_cache("enable_cuda", False)
                return
            
            print("\nInvalid entry. Please enter 'Y' or 'N'.")
            
    def ask_proxy():
        while True:
            user_input = input(
                               "Enable Proxy Frames?"
                               
                               "\n\nIf Enabled, Proxy frames will be generated alongside full size frames"
                               "\nand used for global positioner"
                               
                               "\n\n(Y/N)\n"
                               ).strip().lower()
            
            if user_input in ["y", "yes"]:
                print("\nProxy Frames Enabled")
                print_divider()
                update_cache("enable_proxies", True)
                return
            
            if user_input in ["n", "no"]:
                print("\nProxy Frames Disabled")
                print_divider()
                update_cache("enable_proxies", False)
                return
            
            print("\nInvalid entry. Please enter 'Y' or 'N'.")
    
    ask_cuda()
    ask_proxy()
    set_current_time()
    
    full_frame_dir = extract_video_frames(media_files, proxy=False)
    proxy_frame_dir = None
    
    if read_cache("enable_proxies"):
        proxy_frame_dir = extract_video_frames(media_files, proxy=True)
        
    feature_extractor(full_frame_dir, proxy_frame_dir)
    
    sequential_matcher()
    
    view_graph_calibrator()
    
    global_mapper()
    
    point_triangulator()
    
    point_filtering()
    
    model_orientation_aligner()
    
    convert_model("TXT")
    convert_model("TXT", parent=True)
    

if __name__ == "__main__":
    main()