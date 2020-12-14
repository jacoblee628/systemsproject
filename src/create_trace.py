import pandas as pd

import read_write as rw

def create_trace(folder_path, version_num):
    # -------------
    # 1. Preprocessing
    # -------------
    # Create a path object (from pathlib) for the vv root folder.
    vv_folder_path = Path(folder_path)
    
    # Check that the user input folder location actually exists
    assert vv_folder_path.exists(), "The specified V&V automatic test data folder does not exist."

    # Extract the V&V info string from the folder name 
    v_v = re.findall("ER[0-9]+ v[0-9]+", vv_folder_path.name)[0].replace("ER", "")

    # Get the correct folder for the provided version number.
    version_path = [x for x in vv_folder_path.iterdir() if x.is_dir() and x.name == version_num][0]
    
    
    # -------------
    # 2. Loading Automated Tests
    # -------------
    # Rest API tests
    # Note: "/" on a pathlib.Path allows navigating into child folders
    rest_api_df = rw.read_rest_api_tests(version_path / "RestApiTests") 
    
    # Rx tests
    rx_df = rw.read_rx_tests(version_path / "Rx")
    
    # obs_srs = pd.read_csv(obs_srs_file_path)
    # obs_srs_list = obs_srs["Formatted ID"].unique()
    # active_prd = pd.read_csv(active_prd_path)
    # active_prd_list = active_prd["ID"].unique()