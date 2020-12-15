import re

import numpy as np
import pandas as pd

import read_write as rw


def check_prd_has_srs(trace, prd_prefix, srs_prefix):
    """check whether each PRD has SRS
       invalid data frame will contain rows where PRDs do not have SRS
    
    Args:
        trace (DataFrame): trace matrix
        prd_prefix (string): string that PRD starts with
        srs_prefix (string): string that SRS starts with
        
    Returns:
        valid_df (DataFrame): data frame with all valid rows of trace matrix
        invalid_df (DataFrame): data frame with all invalid rows of trace matrix
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
    
    
def check_srs_has_test(trace, prd_prefix, srs_prefix):
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
        
    valid = num_unique.loc[num_unique["Test Name"] != 0]
    valid = pd.DataFrame(valid, columns=['SRS ID', 'Test Name'])
    for val in valid['SRS ID']:
        valid_df = valid_df.append(trace[trace['SRS ID'] == val])
    valid_df = valid_df.sort_index()
    
    invalid_df.insert(0, "Error:", "SRS does not have test")

    return valid_df, invalid_df
    
    
def check_srs_has_prd(trace, prd_prefix, srs_prefix):
    """check whether each SRS has PRD
       invalid rows will contain rows where SRSs do not have a PRD
        
    Args:
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
        
    valid = num_unique.loc[num_unique["PRD"] != 0]
    valid = pd.DataFrame(valid, columns=['SRS ID', 'PRD'])
    for val in valid['SRS ID']:
        valid_df = valid_df.append(trace[trace['SRS ID'] == val])
    valid_df = valid_df.sort_index()
    
    invalid_df.insert(0, "Error:", "SRS does not have PRD")

    return valid_df, invalid_df
    

def check_prd_ref_by_srs_exists(trace, active_prd_list, prd_prefix, srs_prefix):
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
    def get_req_list(string, prefix):
        string = string.replace(",", " ")
        test_list = string.split()
        req_list = []

        for val in test_list:
            if val.startswith(prefix) & val[-1].isdigit():
                req_list.append(val)
        return req_list
    
    
    trace["PRD_clean"] = trace["PRD_clean"].apply(lambda row: get_req_list(row, prd_prefix))
    
    trace["valid"] = trace["PRD_clean"].apply(lambda lst: any((True for x in lst if x in active_prd_list)))
    
    invalid_df = trace[(trace['valid'] == False) & (trace['PRD_clean'].str.len() != 0)]
    invalid_df = invalid_df.drop(columns=['PRD_clean', 'valid'])
    
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
    
    
def check_srs_exists(trace, obs_srs_list, prd_prefix, srs_prefix):
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
    
    def get_req_list(string, prefix):
        test_list = string.split()
        req_list = []

        for val in test_list:
            if val.startswith(prefix):
                req_list.append(val)
        return req_list
    
    trace["srs_list"] = trace["Test Name"].apply(lambda row: get_req_list(row, srs_prefix))
    
    trace["invalid"] = trace["srs_list"].apply(lambda lst: any((True for x in lst if x in obs_srs_list)))
    
    valid_df = trace[trace['invalid'] == False]
    valid_df = valid_df.drop(columns=['srs_list', 'invalid'])
    
    invalid_df = trace[trace['invalid'] == True]
    invalid_df = invalid_df.drop(columns=['srs_list', 'invalid'])
    
    invalid_df.insert(0, "Error:", "Test references obsolete SRS")
    
    return valid_df, invalid_df
   
    
def check_prd_exists(trace, active_prd_list, prd_prefix, srs_prefix):
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
    
    def get_req_list(string, prefix):
        test_list = string.split()
        req_list = []

        for val in test_list:
            if val.startswith(prefix) & val[-1].isdigit():
                req_list.append(val)
        return req_list
    
    trace["prd_list"] = trace["prd_list"].apply(lambda row: get_req_list(row, prd_prefix))
    
    trace["valid"] = trace["prd_list"].apply(lambda lst: any((True for x in lst if x in active_prd_list)))
    
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
    
    
def check_tests_traced_to_reqs(trace, prd_prefix, srs_prefix):
    """check whether each test has been traced to all requirements they reference
    
    Args:
        file_path (String): path to the trace matrix
        matrix_type (String): "CO" or "PSC"
        
    Returns:
        String "Passed" if all tests have been traced to all requirements
        Error message if a test hasn't been traced to all requirements
        list of tests not traced
    """
    
    trace["srs_list"] = trace["Test Name"]
    trace["prd_list"] = trace["Test Name"]
    
    
    def get_req_list(string, prefix):
        test_list = string.split()
        req_list = []

        for val in test_list:
            if val.startswith(prefix):
                req_list.append(val)
        return req_list
    
    
    trace["srs_list"] = trace["Test Name"].apply(lambda row: get_req_list(row, srs_prefix))
    trace["prd_list"] = trace["Test Name"].apply(lambda row: get_req_list(row, prd_prefix))
    
    invalid = []
    valid = []
    
    for index, row in trace.iterrows():
        for val in row["srs_list"]:
            if ((trace["SRS ID"] == val) & (trace["Test Name"] == row["Test Name"])).any() == False:
                invalid.append(row["Test Name"])
            else:
                valid.append(row["Test Name"])

        for val in row["prd_list"]:
            if ((trace["PRD"] == val) & (trace["Test Name"] == row["Test Name"])).any() == False:
                invalid.append(row["Test Name"])
            else:
                valid.append(row["Test Name"])
    
        
    return set(valid), set(invalid)
        
