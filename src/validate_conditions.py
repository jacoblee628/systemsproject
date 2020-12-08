import read_write as rw
import pandas as pd

def check_prd_has_srs(file_path, matrix_type):
    """check whether each prd has srs
    
    Args:
        file_path (String): path to the trace matrix
        matrix_type (String): "CO" or "PSC"
        
    Returns:
        String "Passed" if all prd has srs
        Error message if a prd does not have srs
        df of prds without srs
    """
    
    # Load trace matrix
    trace=load_trace(file_path, matrix_type, return_df=True)
    
    # Get rid of n/a values
    trace = trace[trace.PRD != "N/A"]
    trace = trace[trace.PRD != "n/a"]
    
    trace = trace[trace['SRS ID'] != "N/A"]
    trace = trace[trace['SRS ID'] != "n/a"]
    
    # Get number of unique SRS for each PRD
    group = trace.groupby('PRD')['SRS ID'].nunique()
    num_unique = pd.DataFrame({'PRD':group.index, 'SRS ID':group.values})
    
    # Get df of rows where PRD exists but SRS does not
    invalid = num_unique.loc[num_unique["SRS ID"] == 0]
    
    # return pass/fail
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
    trace = trace[trace['SRS ID'] != "N/A"]
    trace = trace[trace['SRS ID'] != "n/a"]
    
    trace = trace[trace['Test Name'] != "N/A"]
    trace = trace[trace['Test Name'] != "n/a"]
    
    # Get number of unique tests for each SRS
    group = trace.groupby('SRS ID')['Test Name'].nunique()
    num_unique = pd.DataFrame({'SRS ID':group.index, 'Test Name':group.values})
    
    # Get df of rows where SRS exists but test does not
    invalid = num_unique.loc[num_unique["Test Name"] == 0]
    
    # return pass/fail
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
    trace = trace[trace['SRS ID'] != "N/A"]
    trace = trace[trace['SRS ID'] != "n/a"]
    
    trace = trace[trace['PRD'] != "N/A"]
    trace = trace[trace['PRD'] != "n/a"]
    
    # Get number of unique PRD for each SRS
    group = trace.groupby('SRS ID')['PRD'].nunique()
    num_unique = pd.DataFrame({'SRS ID':group.index, 'PRD':group.values})
    
    # Get df of rows where SRS exists but PRD does not
    invalid = num_unique.loc[num_unique["PRD"] == 0]
    
    # return pass/fail
    if invalid.shape[0] == 0 :
        return "Passed"
    else :
        return "Failed", invalid    
