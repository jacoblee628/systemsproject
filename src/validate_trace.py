import re

import numpy as np
import pandas as pd

import read_write as rw


def validate_trace(trace, obs_srs_file_path, active_prd_path, prd_prefix="US", srs_prefix="TC"):
    # Load lists of obsolete srs and active prd  
    obs_srs = pd.read_csv(obs_srs_file_path)
    obs_srs_list = obs_srs["Formatted ID"].unique()
    active_prd = pd.read_excel(active_prd_path)
    active_prd_list = active_prd["ID"].unique()
    
    # Gather all the errors into this list of dfs
    invalid_dfs = []
    
    # Run the tests
    trace, invalid = _check_prd_has_srs(trace, prd_prefix, srs_prefix) 
    invalid_dfs.extend(invalid)
    
    trace, invalid = _check_srs_has_test(trace, prd_prefix, srs_prefix)
    invalid_dfs.extend(invalid)
    
    trace, invalid = _check_srs_has_prd(trace, prd_prefix, srs_prefix)
    invalid_dfs.extend(invalid)
    
    trace, invalid = _check_prd_ref_by_srs_exists(trace, active_prd_list, prd_prefix, srs_prefix)
    invalid_dfs.extend(invalid)
    
    trace, invalid = _check_srs_exists(trace, obs_srs_list, prd_prefix, srs_prefix)
    invalid_dfs.extend(invalid)
    
    trace, invalid = _check_prd_exists(trace, active_prd_list, prd_prefix, srs_prefix)
    invalid_dfs.extend(invalid)
    
    return trace, invalid_dfs
    
def _check_prd_has_srs(trace, prd_prefix, srs_prefix):
    """check whether each PRD has SRS
       invalid data frame will contain rows where PRDs do not have SRS
    
    Args:
        trace (pd.DataFrame): trace matrix
        prd_prefix (str): string that PRD starts with
        srs_prefix (str): string that SRS starts with
        
    Returns:
        valid_df (pd.DataFrame): data frame with all valid rows of trace matrix
        invalid_df (pd.DataFrame): data frame with all invalid rows of trace matrix
    """
    # Get rid of n/a values
    valid_df = trace.loc[-trace['PRD'].str.startswith(prd_prefix)]
    trace = trace.loc[trace['PRD'].str.startswith(prd_prefix)]
    
    for val in trace['SRS ID']:
        val=str(val)
        if not val.startswith(srs_prefix):
            val = np.nan
    
    # Get number of unique SRS for each PRD
    group = trace.groupby('PRD')['SRS ID'].nunique()
    num_unique = pd.DataFrame({'PRD':group.index, 'SRS ID':group.values})
    
    # Get df of rows where PRD exists but SRS does not
    invalid = num_unique.loc[num_unique["SRS ID"] == 0]
    invalid = pd.DataFrame(invalid, columns=['PRD', 'SRS ID'])
    invalid_df = pd.DataFrame()
    for val in invalid['PRD']:
        invalid_df = invalid_df.append(trace[trace['PRD'] == val])
    invalid_df = invalid_df.sort_index()
        
    valid = num_unique.loc[num_unique["SRS ID"] != 0]
    valid = pd.DataFrame(valid, columns=['PRD', 'SRS ID'])
    for val in valid['PRD']:
        valid_df = valid_df.append(trace[trace['PRD'] == val])
    valid_df = valid_df.sort_index()

    invalid_df.insert(0, "Error:",  "PRD does not have SRS")
    
    return valid_df, invalid_df
    
    
def _check_srs_has_test(trace, prd_prefix, srs_prefix):
    """check whether each SRS has a test
       invalid data frame will contain rows where SRSs do not have a test
    
    Args:
        trace (DataFrame): trace matrix
        prd_prefix (string): string that PRD starts with
        srs_prefix (string): string that SRS starts with
        
    Returns:
        valid_df (DataFrame): data frame with all valid rows of trace matrix
        invalid_df (DataFrame): data frame with all invalid rows of trace matrix
    """
    
    # Get rid of n/a values
    valid_df = trace.loc[-trace['SRS ID'].str.startswith(prd_prefix)]
    trace = trace.loc[trace['SRS ID'].str.startswith(srs_prefix)]
    
    for val in trace['Test Name']:
        val = str(val)
        if not len(val) > 5:
            val = np.nan

    # Get number of unique tests for each SRS
    group = trace.groupby('SRS ID')['Test Name'].nunique()
    num_unique = pd.DataFrame({'SRS ID':group.index, 'Test Name':group.values})
    
    # Get df of rows where SRS exists but test does not
    invalid = num_unique.loc[num_unique["Test Name"] == 0]
    invalid = pd.DataFrame(invalid, columns=['SRS ID', 'Test Name'])
    invalid_df = pd.DataFrame()
    for val in invalid['SRS ID']:
        invalid_df = invalid_df.append(trace[trace['SRS ID'] == val])
    invalid_df = invalid_df.sort_index()
    
    # create valid df
    valid = num_unique.loc[num_unique["Test Name"] != 0]
    valid = pd.DataFrame(valid, columns=['SRS ID', 'Test Name'])
    for val in valid['SRS ID']:
        valid_df = valid_df.append(trace[trace['SRS ID'] == val])
    valid_df = valid_df.sort_index()
    
    invalid_df.insert(0, "Error:", "SRS does not have test")

    return valid_df, invalid_df
    
    
def _check_srs_has_prd(trace, prd_prefix, srs_prefix):
    """check whether each SRS has PRD
       invalid rows will contain rows where SRSs do not have a PRD
        
    Args:
        trace (DataFrame): trace matrix
        prd_prefix (string): string that PRD starts with
        srs_prefix (string): string that SRS starts with
        
    Returns:
        valid_df (DataFrame): data frame with all valid rows of trace matrix
        invalid_df (DataFrame): data frame with all invalid rows of trace matrix
    """
    
    # Get rid of n/a values
    valid_df = trace.loc[-trace['SRS ID'].str.startswith(prd_prefix)]
    trace = trace.loc[trace['SRS ID'].str.startswith(srs_prefix)]
    
    for val in trace['PRD']:
        val=str(val)
        if not val.startswith(prd_prefix):
            val = np.nan
    
    # Get number of unique PRD for each SRS
    group = trace.groupby('SRS ID')['PRD'].nunique()
    num_unique = pd.DataFrame({'SRS ID':group.index, 'PRD':group.values})
    
    # Get df of rows where SRS exists but PRD does not
    invalid = num_unique.loc[num_unique["PRD"] == 0]
    invalid = pd.DataFrame(invalid, columns=['SRS ID', 'PRD'])
    invalid_df = pd.DataFrame()
    for val in invalid['SRS ID']:
        invalid_df = invalid_df.append(trace[trace['SRS ID'] == val])
    invalid_df = invalid_df.sort_index()
    
    # Create valid df
    valid = num_unique.loc[num_unique["PRD"] != 0]
    valid = pd.DataFrame(valid, columns=['SRS ID', 'PRD'])
    for val in valid['SRS ID']:
        valid_df = valid_df.append(trace[trace['SRS ID'] == val])
    valid_df = valid_df.sort_index()
    
    invalid_df.insert(0, "Error:", "SRS does not have PRD")

    return valid_df, invalid_df
    

def _check_prd_ref_by_srs_exists(trace, active_prd_list, prd_prefix, srs_prefix):
    """check whether all PRD referenced by SRS exist
       invalid rows will contain rows where PRDs referenced by SRSs do not exist
        
    Args:
        trace (DataFrame): trace matrix
        active_prd_list (list): list of PRDs that are active
        prd_prefix (string): string that PRD starts with
        srs_prefix (string): string that SRS starts with
        
    Returns:
        valid_df (DataFrame): data frame with all valid rows of trace matrix
        invalid_df (DataFrame): data frame with all invalid rows of trace matrix
    """
    
    trace["PRD_clean"] = trace["PRD"]
    
    # function to clean PRD column
    def _get_req_list(string, prefix):
        string = string.replace(",", " ")
        test_list = string.split()
        req_list = []

        for val in test_list:
            if val.startswith(prefix) & val[-1].isdigit():
                req_list.append(val)
        return req_list
    
    
    trace["PRD_clean"] = trace["PRD_clean"].apply(lambda row: get_req_list(row, prd_prefix))
    
    # Valid if PRDs are all in active list
    trace["valid"] = trace["PRD_clean"].apply(lambda lst: all((True for x in lst if x in active_prd_list)))
    
    invalid_df = trace[(trace['valid'] == False) & (trace['PRD_clean'].str.len() != 0)]
    invalid_df = invalid_df.drop(columns=['PRD_clean', 'valid'])
    
    # create valid df by subtracting invalid from trace
    if (len(invalid_df.index) == 0):
        valid_df = trace
        valid_df = valid_df.drop(columns=['PRD_clean', 'valid'])
    else:
        valid_df = trace.merge(invalid_df, how='left', indicator=True)
        valid_df = valid_df[valid_df['_merge'] == 'left_only']
        valid_df = valid_df.drop(columns=['_merge', 'PRD_clean', 'valid'])
    
    valid_df = valid_df.sort_index()
    
    invalid_df.insert(0, "Error:",  "PRD referenced by SRS does not exist")

    return valid_df, invalid_df
    
    
def _check_srs_exists(trace, obs_srs_list, prd_prefix, srs_prefix):
    """check whether all SRSs referenced by tests exist
       invalid rows will contain rows where SRSs referenced by tests do not exist
        
    Args:
        trace (DataFrame): trace matrix
        obs_srs_list (list): list of SRS that are obsolete
        prd_prefix (string): string that PRD starts with
        srs_prefix (string): string that SRS starts with
        
    Returns:
        valid_df (DataFrame): data frame with all valid rows of trace matrix
        invalid_df (DataFrame): data frame with all invalid rows of trace matrix
    """
    
    trace["srs_list"] = trace["Test Name"]
    
    # function to clean column and put into list
    def _get_req_list(string, prefix):
        test_list = string.split()
        req_list = []

        for val in test_list:
            if val.startswith(prefix):
                req_list.append(val)
        return req_list
    
    trace["srs_list"] = trace["Test Name"].apply(lambda row: get_req_list(row, srs_prefix))
    
    # Valid if SRS are all not in obsolete list
    trace["invalid"] = trace["srs_list"].apply(lambda lst: all((True for x in lst if x in obs_srs_list)))
    
    # Create valid and invalid dfs
    valid_df = trace[trace['invalid'] == False]
    valid_df = valid_df.drop(columns=['srs_list', 'invalid'])
    
    invalid_df = trace[trace['invalid'] == True]
    invalid_df = invalid_df.drop(columns=['srs_list', 'invalid'])
    
    invalid_df.insert(0, "Error:", "Test references obsolete SRS")
    
    return valid_df, invalid_df
   
    
def _check_prd_exists(trace, active_prd_list, prd_prefix, srs_prefix):
    """check whether all PRD referenced by tests exist
       invalid rows will contain rows where PRDs referenced by tests are not active
        
    Args:
        trace (DataFrame): trace matrix
        active_prd_list (list): list of PRDs that are active
        prd_prefix (string): string that PRD starts with
        srs_prefix (string): string that SRS starts with
        
    Returns:
        valid_df (DataFrame): data frame with all valid rows of trace matrix
        invalid_df (DataFrame): data frame with all invalid rows of trace matrix
    """
    
    trace["prd_list"] = trace["Test Name"]
    
    # function to clean column and put into list
    def _get_req_list(string, prefix):
        test_list = string.split()
        req_list = []

        for val in test_list:
            if val.startswith(prefix) & val[-1].isdigit():
                req_list.append(val)
        return req_list
    
    trace["prd_list"] = trace["prd_list"].apply(lambda row: get_req_list(row, prd_prefix))
    
    # Valid if PRD are all in active list
    trace["valid"] = trace["prd_list"].apply(lambda lst: all((True for x in lst if x in active_prd_list)))
    
    # Create invalid and valid dfs
    invalid_df = trace[(trace['valid'] == False) & (trace['prd_list'].str.len() != 0)]
    invalid_df = invalid_df.drop(columns=['prd_list', 'valid'])
    
    if (len(invalid_df.index) == 0):
        valid_df = trace
        valid_df = valid_df.drop(columns=['prd_list', 'valid'])
    else:
        valid_df = trace.merge(invalid_df, how='left', indicator=True)
        valid_df = valid_df[valid_df['_merge'] == 'left_only']
        valid_df = valid_df.drop(columns=['_merge', 'prd_list', 'valid'])
    
    invalid_df.insert(0, "Error:", "PRD referenced by test does not exist")
    
    return valid_df, invalid_df
  
