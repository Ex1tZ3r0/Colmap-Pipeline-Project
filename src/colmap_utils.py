from config import COLMAP_EXE
from pathlib import Path
from config import ensure_dir_exists, update_cache, read_cache, print_divider, read_settings
from src.executer import run_command

def feature_extractor(full_frame_dir, proxy_frame_dir: Path | None = None):
    
    imageset_dir = full_frame_dir
    
    if proxy_frame_dir:
        imageset_dir = proxy_frame_dir
        
    update_cache("imageset_dir", imageset_dir)
        
    
    database_file_path = imageset_dir.resolve().parent / "dataset" / "database.db"
    ensure_dir_exists(database_file_path.resolve().parent)
    
    dataset_dir = database_file_path.resolve().parent
    
    sparse_dir = dataset_dir / "sparse"
    ensure_dir_exists(sparse_dir)
    
    update_cache("database_file", database_file_path)
    update_cache("dataset_dir", dataset_dir)
    update_cache("sparse_dir", sparse_dir)
    
    feature_extraction_type = read_settings("feature_extraction_type")
    feature_extraction_use_gpu = read_settings("feature_extraction_use_gpu")
    image_reader_single_camera = read_settings("image_reader_single_camera")
    sift_extraction_max_num_features = read_settings("sift_extraction_max_num_features")
    
    command = [
        str(COLMAP_EXE), "feature_extractor",
        "--database_path", str(database_file_path),
        "--image_path", str(imageset_dir),
        "--ImageReader.single_camera", str(image_reader_single_camera),
        "--FeatureExtraction.type", str(feature_extraction_type),
        "--FeatureExtraction.use_gpu", str(feature_extraction_use_gpu),
        "--SiftExtraction.max_num_features", str(sift_extraction_max_num_features),
    ]
    
    run_command(command)

def sequential_matcher():
    
    database_file = read_cache("database_file")
    
    sequential_matching_overlap = read_settings("sequential_matching_overlap")
    
    command = [
        str(COLMAP_EXE), "sequential_matcher",
        "--database_path", str(database_file),
        "--SequentialMatching.overlap", str(sequential_matching_overlap)
        
    ]
    run_command(command)
    
def view_graph_calibrator():
    
    database_file = read_cache("database_file")
    
    command = [
        str(COLMAP_EXE), "view_graph_calibrator",
        "--database_path", str(database_file)
    ]
    run_command(command)
    
def global_mapper():
    
    dataset_dir = read_cache("dataset_dir")
    database_file = read_cache("database_file")
    image_dir = read_cache("imageset_dir")
    sparse_dir = read_cache("sparse_dir")
    
    command = [
        str(COLMAP_EXE), "global_mapper",
        "--database_path", str(database_file),
        "--image_path", str(image_dir),
        "--output_path", str(sparse_dir)
    ]
    run_command(command)
    
def point_triangulator():
    
    database_file = read_cache("database_file")
    imageset_dir = read_cache("imageset_dir")
    sparse_dir = read_cache("sparse_dir")
    
    sparse_result_string = (f"{sparse_dir}/0")

    sparse_result = Path(sparse_result_string)
    
    ensure_dir_exists(sparse_result)
    
    update_cache("sparse_result", sparse_result)
    
    command = [
        str(COLMAP_EXE), "point_triangulator",
        "--database_path", str(database_file),
        "--image_path", str(imageset_dir),
        "--input_path", str(sparse_result),
        "--output_path", str(sparse_result)
    ]
    run_command(command)
    
def point_filtering():
    
    sparse_result_dir = read_cache("sparse_result")
    
    command = [
        str(COLMAP_EXE), "point_filtering",
        "--input_path", str(sparse_result_dir),
        "--output_path", str(sparse_result_dir),
    ]
    run_command(command)
    
def model_orientation_aligner():
    
    imageset_dir = read_cache("imageset_dir")
    sparse_result_dir = read_cache("sparse_result")
    
    orientation_method = read_settings("model_orientation_method")
    
    command = [
        str(COLMAP_EXE), "model_orientation_aligner",
        "--image_path", str(imageset_dir),
        "--input_path", str(sparse_result_dir),
        "--output_path", str(sparse_result_dir),
        "--method", str(orientation_method),
    ]
    run_command(command)

def convert_model(filetype: str, parent: bool | None = None):
    
    sparse_result_dir = read_cache("sparse_result")
    sparse_parent_dir = read_cache("sparse_dir")
    
    command = [
        str(COLMAP_EXE), "model_converter",
        "--input_path", str(sparse_result_dir),
        "--output_path"
    ]
    
    if parent:
        command.append(str(sparse_parent_dir))
    else:
        command.append(str(sparse_result_dir))
        
    command.append("--output_type")
    command.append(filetype)
    
    run_command(command)
