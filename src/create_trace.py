import re
from pathlib import Path

import numpy as np
import pandas as pd

import read_write as rw


def create_trace(vv_folder_path, as_run_path, version_num, srs_prefix="TC"):
    """ Function for processing manual and automatic tests
    
    Args:
        vv_folder_path (String): folder path of root folder
        as_run_path (String): file path of as_runs
        version_num (String): version number
        srs_prefix (String): string that SRS starts with
        
    Returns:
        pd.DataFrame(dfs) (List): list of valid data frames
        invalid_dfs (List): list of invalid data frames
    """
    
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
    
    # TODO: Load previous traces (for backfilling if needed)
    
    # ----------------------------------------------------
    # 2. Parsing and processing manual and automatic tests
    # ----------------------------------------------------
    invalid_dfs = []
    dfs = []
    
    # Get the manual as run results
    df, invalid = _process_as_run_tests(as_run_path, srs_prefix)
    invalid_dfs.extend(invalid)
    dfs.append(df)
    
    # Get the automatic (Rest API and Rx) test results
    df, invalid = _process_automatic_tests(version_path, srs_prefix)
    invalid_dfs.extend(invalid)
    dfs.append(df)
    
    # TODO: Implement input from more test info sources

    return pd.DataFrame(dfs), invalid_dfs
    

def _filter_status(tests_df):
    """Filters out any tests with statuses that aren't equal to "Passed" or "Failed"

    Args:
        tests (pandas.DataFrame): the test data; note that there should be a column called "status"
        
    Returns:
        two list or pd.DataFrame: the valid and invalid automated rest_api tests
    """
    valid = tests_df[(tests_df['Test Status']=='Passed') | (tests_df['Test Status']=='Failed')]
    invalid = tests_df[(tests_df['Test Status']!='Passed') & (tests_df['Test Status']!='Failed')]
    return valid, invalid


def _process_as_run_tests(as_run_path, srs_prefix="TC"):
    """ Function for processing as runs
    
    Args:
        as_run_path (String): file path of as_runs
        srs_prefix (String): string that SRS starts with
        
    Returns:
        pd.DataFrame(new_trace) (DataFrame): new trace matrix with valid tests
        invalid_dfs (List): list of invalid data frames
    """
    
    # Load in dataset (mostly unprocessed)
    as_run_df = rw.read_as_run_tests(as_run_path)
    
    # ----------
    # Filtering
    # ----------
    invalid_dfs = []

    # Filter out if Test Status != "Passed" or "Failed"
    as_run_df, invalid_df = _filter_status(as_run_df)
    if len(invalid_df) > 0:
        invalid_df.insert(0, "Error:", f"Manual as-run entry invalid status for trace")
        invalid_dfs.append(invalid_df)

    # Filter out tests with blank names (name wasnt in original document; just the run id)
    invalid_df = as_run_df.loc[as_run_df["Test Name"].isin([""])]
    invalid_df.insert(0, "Error:", f"Name not found in {as_run_path}")
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
    new_trace = []
    for row in as_run_df.values:
        test_name = row[0]

        tcs = re.findall(f"{srs_prefix}[0-9]+", test_name)
        # prds = re.findall(f"{srs_prefix}[0-9]+", test_name)

        # for prd in prds:
        for tc in tcs:
            entry = {
                "PRD": np.nan, # TODO: Fix by finding out where prd can be looked up
                "SRS ID": np.nan, # TODO: Fix by finding out where SRS ID (ESA) can be looked up
                "Method": "Manual",
                "Test Name": test_name,
                "V&V Test Report": row[6],
                "TC ID": tc,
                "Test Status": row[2],
                "Release": row[3],
                "Name": np.nan, # TODO: Fix by finding out where name can be looked up
                "Owner": row[5],
                "Application": row[4]
            }
            new_trace.append(entry)

    return pd.DataFrame(new_trace), invalid_dfs
    
    
def _process_automatic_tests(version_path, srs_prefix="TC"):
    """ Function for processing automatic tests
    
    Args:
        version_path (String): file path
        srs_prefix (String): string that SRS starts with
        
    Returns:
        pd.DataFrame(new_trace) (DataFrame): new trace matrix with valid tests
        invalid_dfs (List): list of invalid data frames
    """
    
    # Load in dataset (mostly unprocessed)
    api_df = rw.read_rest_api_tests(version_path / "RestApiTests") # Note: "/" on a pathlib.Path allows navigating into child folders
    rx_df = rw.read_rx_tests(version_path / "Rx")
    
    # Can concatenate these two and process together; similar data format
    df = pd.concat([api_df, rx_df])
    
    # ----------
    # Filtering
    # ----------
    invalid_dfs = []

    # Filter out if Test Status != "Passed" or "Failed"
    df, invalid_df = _filter_status(df)
    if len(invalid_df) > 0:
        invalid_df.insert(0, "Error:", f"Automatic test entry invalid status for trace")
        invalid_dfs.append(invalid_df)
    
    # Filter out entries that won't go in the trace
    invalid_df = df.loc[~df["Test Name"].str[0:2].isin(["TC", "ES"])]
    invalid_df.insert(0, "Error:", "Automatic test not part of trace")
    invalid_dfs.append(invalid_df)

    # ---------------------------------
    # Formatting and filling in columns
    # ---------------------------------
    new_trace = []
    for row in df.values:
        test_name = row[0]

        tcs = re.findall(f"{srs_prefix}[0-9]+", test_name)
        # prds = re.findall(f"{srs_prefix}[0-9]+", test_name)

        # for prd in prds:
        for tc in tcs:
            entry = {
                "PRD": np.nan, # TODO: Fix by finding out where prd can be looked up
                "SRS ID": np.nan, # TODO: Fix by finding out where SRS ID (ESA) can be looked up
                "Method": "Automatic",
                "Test Name": test_name,
                "V&V Test Report": row[3],
                "TC ID": tc,
                "Test Status": row[1],
                "Release": row[2],
                "Name": np.nan, # TODO: Fix by finding out where name can be looked up
                "Owner": row[5],
                "Application": "Sapphire" # TODO: These may not all be sapphire; may need to fix
            }
            new_trace.append(entry)

    return pd.DataFrame(new_trace), invalid_dfs
