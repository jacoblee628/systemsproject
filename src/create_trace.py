import pandas as pd

import read_write as rw

def create_trace(folder_path, as_run_path, version_num):
    # ----------------
    # 1. Preprocessing
    # ----------------
    # Create a path object (from pathlib) for the vv root folder.
    vv_folder_path = Path(folder_path)
    
    # Check that the user input folder location actually exists
    assert vv_folder_path.exists(), "The specified V&V automatic test data folder does not exist."
    
    # Get the correct folder for the provided version number.
    version_path = [x for x in vv_folder_path.iterdir() if x.is_dir() and x.name == version_num][0]
    
    
    # --------------------------------------------
    # 2. Loading Automated and Manual As-run Tests
    # --------------------------------------------
    # Rest API tests
    
    # Rx tests
    rx_df = rw.read_rx_tests(version_path / "Rx")
    
    # Manual tests
    as_run_df = rw.read_as_run_tests(as_run_path)
    
    # ------------
    # 3. Filtering 
    # ------------
    
    
    # obs_srs = pd.read_csv(obs_srs_file_path)
    # obs_srs_list = obs_srs["Formatted ID"].unique()
    # active_prd = pd.read_csv(active_prd_path)
    # active_prd_list = active_prd["ID"].unique()


def filter_status(tests_df):
    """Filters out any tests with statuses that aren't equal to "Passed" or "Failed"

    Args:
        tests (pandas.DataFrame): the test data; note that there should be a column called "status"
        
    Returns:
        two list or pd.DataFrame: the valid and invalid automated rest_api tests
    """
    valid = tests_df[(tests_df['Test Status']=='Passed') | (tests_df['Test Status']=='Failed')]
    invalid = tests_df[(tests_df['Test Status']!='Passed') & (tests_df['Test Status']!='Failed')]
    return valid, invalid

def process_as_run_tests(as_run_path):
    manual.loc[manual["Test Name"].isin([""])]
    
    # Also add the V&V Test Report info by extracting it from file name
    file_name = Path(as_run_path).stem
    v_v = re.findall("ER([0-9]+ v[0-9]+|[0-9]+v[0-9]+)", file_name)[0].replace("ER", "")
    
def process_rest_api_tests(folder_path, version_num):
    # Read in the tests (naive; no )
    rest_api_df = rw.read_rest_api_tests(version_path / "RestApiTests") # Note: "/" on a pathlib.Path allows navigating into child folders
    
    # 
