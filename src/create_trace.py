import pandas as pd
from pathlib import Path

import read_write as rw

def create_trace(prev_trace, vv_folder_path, as_run_path, version_num):
    # ----------------
    # 1. Preprocessing
    # ----------------
    # Create a path object (from pathlib) for the vv root folder.
    if isinstance(vv_folder_path, str):
        vv_folder_path = Path(vv_folder_path)
    
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
    # Load in dataset (mostly unprocessed)
    as_run_df = rw.read_as_run_tests(as_run_path)
    
    # ----------
    # Filtering
    # ----------
    invalid_dfs = []

    # Filter out if Test Status != "Passed" or "Failed"
    as_run_df, invalid_df = filter_status(as_run_df)
    if len(invalid_df) > 0:
        invalid_dfs.append(invalid_df)

    # Filter out tests with blank names (name wasnt in original document; just the run id)
    invalid_df = as_run_df.loc[as_run_df["Test Name"].isin([""])]
    invalid_df.insert(0, "Error:", f"Name not found in {file_name}")
    invalid_dfs.append(invalid_df)
    as_run_df = as_run_df.loc[~as_run_df["Test Name"].isin([""])]
    
    # Filter out entries that won't go in the trace
    invalid_df = as_run_df.loc[~as_run_df["Test Name"].str[0:3].isin(["PRD", "SRS"])]
    invalid_df.insert(0, "Error:", "Manual test not part of trace")
    invalid_dfs.append(invalid_df)
    as_run_df = as_run_df.loc[as_run_df["Test Name"].str[0:3].isin(["PRD", "SRS"])]

    # ---------------------------------
    # Formatting and filling in columns
    # ---------------------------------
    
    
def process_rest_api_tests(folder_path, version_num):
    # Read in the tests (naive; no )
    rest_api_df = rw.read_rest_api_tests(version_path / "RestApiTests") # Note: "/" on a pathlib.Path allows navigating into child folders
    
    # 
    valid 