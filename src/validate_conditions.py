import read_write as rw
import pandas as pd
import numpy as np

prd_prefix = "US"
srs_prefix = "TC"

obs_srs=pd.read_csv(file_path_srs)
obs_srs_list=obs_srs["Formatted ID"].unique()

def check_prd_has_srs(file_path, matrix_type):
    """check whether each prd has srs
    
    Args:
        file_path (String): path to the trace matrix
        matrix_type (String): "CO" or "PSC"
        
    Returns:
        Error message if a prd does not have srs
        list of prds without srs
    """
    
    # Load trace matrix
    trace=load_trace(file_path, matrix_type, return_df=True)
    
    # Get rid of n/a values
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
    valid = num_unique.loc[num_unique["SRS ID"] != 0]
    
    # return trace matrix
    if invalid.shape[0] == 0 :
        return "Passed"
    else :
        return "Failed", invalid
    
    
def check_srs_has_test(file_path, matrix_type):
    """check whether each srs has a test
    
    Args:
        file_path (String): path to the trace matrix
        matrix_type (String): "CO" or "PSC"
        
    Returns:
        String "Passed" if all srs has test
        Error message if a srs does not have a test
        df of srs without tests
    """
    
    # Load trace matrix
    trace=load_trace(file_path, matrix_type, return_df=True)
    
    # Get rid of n/a values
    trace = trace.loc[trace['SRS ID'].str.startswith(srs_prefix)]
    
    for val in trace['Test Name']:
        val=str(val)
        if not len(val) > 5:
            val = np.nan

    # Get number of unique tests for each SRS
    group = trace.groupby('SRS ID')['Test Name'].nunique()
    num_unique = pd.DataFrame({'SRS ID':group.index, 'Test Name':group.values})
    
    # Get df of rows where SRS exists but test doe not
    invalid = num_unique.loc[num_unique["Test Name"] == 0]
    valid = num_unique.loc[num_unique["Test Name"] != 0]
    
    # return trace matrix
    if invalid.shape[0] == 0 :
        return "Passed"
    else :
        return "Failed", invalid
    
    
def check_srs_has_prd(file_path, matrix_type):
    """check whether each srs has prd
    
    Args:
        file_path (String): path to the trace matrix
        matrix_type (String): "CO" or "PSC"
        
    Returns:
        String "Passed" if all srs has prd
        Error message if a srs does not have a prd
        list of srs without prd
    """
    
    # Load trace matrix
    trace=load_trace(file_path, matrix_type, return_df=True)
    
    # Get rid of n/a values
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
    valid = num_unique.loc[num_unique["PRD"] != 0]
    
    # return pass/fail and invalid srs
    if invalid.shape[0] == 0 :
        return "Passed"
    else :
        return "Failed", invalid  
    

def check_prd_refby_srs_exists(file_path_trace, active_prd_list, matrix_type):
    """check whether all prd referenced by srs exist
    
    Args:
        file_path_trace (String): path to the trace matrix
        active_prd_list (List): list of active PRD
        matrix_type (String): "CO" or "PSC"
        
    Returns:
        String "Passed" if all prd exist
        String "Failed" if there is an obsolete prd referenced
        list of obsolete prd
    """
    
    # Load trace matrix
    trace=load_trace(file_path, matrix_type, return_df=True)
     
    # Get rid of n/a values
    trace = trace.loc[trace['SRS ID'].str.startswith(srs_prefix)]
    trace = trace.loc[trace['PRD'].str.startswith(prd_prefix)]
    
    # Get unique PRD for each SRS
    group = trace.groupby('SRS ID')['PRD'].unique()
    unique_prd = pd.DataFrame({'SRS ID':group.index, 'PRD':group.values})
    
    # Get list of obsolete PRD
    passed = True
    invalid = []
    
    for lst in unique_prd["PRD"]:
        for val in lst:
            if val not in active_prd_list:
                passed = False
                invalid.append(val)
    
    invalid = set(invalid)

    # return trace matrix
    if invalid.shape[0] == 0 :
        return "Passed"
    else :
        return "Failed", invalid
    
    
def check_srs_exists(file_path_trace, obs_srs_list, matrix_type):
    """check whether all srs referenced by tests exist
    
    Args:
        file_path_trace (String): path to the trace matrix
        obs_srs_list (List): list of obsolete SRS
        matrix_type (String): "CO" or "PSC"
        
    Returns:
        String "Passed" if all srs exist
        String "Failed" if there is an obsolete srs referenced
        list of obsolete srs
    """
    
    # Load trace matrix
    trace=load_trace(file_path_trace, matrix_type, return_df=True)
    
    trace["srs_list"] = trace["Test Name"]
    
    def get_req_list(string, prefix):
        test_list = string.split()
        req_list = []

        for val in test_list:
            if val.startswith(prefix):
                req_list.append(val)
        return req_list
    
    trace["srs_list"] = trace["srs_list"].apply(lambda row: get_req_list(row, srs_prefix))
    
    # Check if srs in obsolete list
    passed = True
    invalid = []
    
    for lst in trace["srs_list"]:
        for val in lst:
            if val in obs_srs_list:
                passed = False
                invalid.append(val)
    
    invalid = set(invalid)
    
    if passed:
        return "Passed"
    else:
        return "Failed", invalid
   
    
def check_prd_exists(file_path_trace, file_path_prd, matrix_type):
    """check whether all prd referenced by tests exist
    
    Args:
        file_path_trace (String): path to the trace matrix
        file_path_prd (String): path to the csv of obsolete prd
        matrix_type (String): "CO" or "PSC"
        
    Returns:
        String "Passed" if all prd exist
        Error message if there is an obsolete prd referenced
        list of obsolete prd
    """
    
    # Load trace matrix
    trace=load_trace(file_path_trace, matrix_type, return_df=True)
    
    trace["prd_list"] = trace["Test Name"]
    
    def get_req_list(string, prefix):
        test_list = string.split()
        req_list = []

        for val in test_list:
            if val.startswith(prefix):
                req_list.append(val)
        return req_list
    
    trace["prd_list"] = trace["prd_list"].apply(lambda row: get_req_list(row, "US"))
    
    #load obsolete csv
    obs_prd=pd.read_csv(file_path_prd)
    obs_prd_list=obs_prd["Formatted ID"].unique()
    
    
    passed = True
    invalid = []
    
    for lst in trace["prd_list"]:
        for val in lst:
            if val in obs_prd_list:
                passed = False
                invalid.append(val)
    
    invalid = set(invalid)
    
    if passed:
        return "Passed"
    else:
        return "Failed", invalid    
    def get_req_list(string, prefix):
        test_list = string.split()
        req_list = []

        for val in test_list:
            if val.startswith(prefix):
                req_list.append(val)
        return req_list
    
    trace["srs_list"] = trace["srs_list"].apply(lambda row: get_req_list(row, "TC"))
    
    #load obsolete csv
    obs_srs=pd.read_csv(file_path_srs)
    obs_srs_list=obs_srs["Formatted ID"].unique()
    
    
    passed = True
    invalid = []
    
    for lst in trace["srs_list"]:
        for val in lst:
            if val in obs_srs_list:
                passed = False
                invalid.append(val)
    
    invalid = set(invalid)
    
    if passed:
        return "Passed"
    else:
        return "Failed", invalid
