import read_write as rw
import pandas as pd

def check_manual(file_path):
    """filter the valid and invalid manual tests
    
    Args:
        file_path (String): path to the manual file

    Returns:
        two list or pd.DataFrame: the valid and invalid manual tests
    """
    
    # Load dataframe from the function load_manual tests
    manual_tests=rw.load_manual_tests(file_path, return_df=True)
    
    # Check test status and write results in valid_manual_tests
    valid_manual_tests=manual_tests[(manual_tests['status']=='Passed') | (manual_tests['status']=='Failed')]
    
    # Check test status and write results in invalid_manual_tests
    invalid_manual_tests=manual_tests[(manual_tests['status']!='Passed') & (manual_tests['status']!='Failed')]
    
    # Return dataframe of valid and invalid tests
    return valid_manual_tests, invalid_manual_tests