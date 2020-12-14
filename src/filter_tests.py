import pandas as pd

import read_write as rw

def filter_tests(tests):
    """Filters out any tests with statuses that aren't equal to "Passed" or "Failed"

    Args:
        tests (pandas.DataFrame): the test data; note that there should be a column called "status"
        
    Returns:
        two list or pd.DataFrame: the valid and invalid automated rest_api tests
    """
    valid = tests[(tests['Test Status']=='Passed') | (tests['Test Status']=='Failed')]
    invalid = tests[(tests['Test Status']!='Passed') & (tests['Test Status']!='Failed')]
    return valid, invalid


# def filter_manual_tests(tests):
#     """filter the valid and invalid manual tests
    
#     Args:
#         tests (pandas.DataFrame): the manual test data

#     Returns:
#         two list or pd.DataFrame: the valid and invalid manual tests
#     """
#     # Check test status and write results in valid_manual_tests
#     valid_manual_tests = tests[(tests['status']=='Passed') | (tests['status']=='Failed')]
    
#     # Check test status and write results in invalid_manual_tests
#     invalid_manual_tests = tests[(tests['status']!='Passed') & (tests['status']!='Failed')]
    
#     # Return dataframe of valid and invalid tests
#     return valid_manual_tests, invalid_manual_tests


# def filter_automated_tests(tests):
#     """filter the valid and invalid automated tests
    
#     Args:
#         tests (pandas.DataFrame): the automatic test data (from Rx and/or API Tests)

#     Returns:
#         two list or pd.DataFrame: the valid and invalid automated rest_api tests
#     """
#     # Check test status and write results in valid_rest_api_tests
#     valid_rest_api_tests = tests[(tests['status']=='Passed') | (tests['status']=='Failed')]
    
#     # Check test status and write results in invalid_rest_api_tests
#     invalid_rest_api_tests = tests[(tests['status']!='Passed') & (tests['status']!='Failed')]
        
#     # Return dataframe of valid and invalid tests
#     return valid_rest_api_tests, invalid_rest_api_tests


# def filter_performance_tests(file_path):
#     """filter the valid and invalid automated tests
    
#     Args:
#         file_path (String): path to the performance tests file

#     Returns:
#         two list or pd.DataFrame: the valid and invalid automated performance tests
#     """
#     # Load dataframe from the function load_performance tests
#     performance_tests = rw.read_performance_test_results_by_tc(file_path, return_df=True)
    
#     # Check test status and write results in valid_performance_tests
#     valid_performance_tests = performance_tests[(performance_tests['PASS/FAIL']=='PASS') | (performance_tests['PASS/FAIL']=='FAIL')]
    
#     # Check test status and write results in invalid_performance_tests
#     invalid_performance_tests = performance_tests[(performance_tests['PASS/FAIL']!='PASS') & (performance_tests['PASS/FAIL']!='FAIL')]
    
#     # Return dataframe of valid and invalid tests
#     return valid_performance_tests, invalid_performance_tests


# def filter_component_tests(file_path):
#     """filter the valid and invalid automated tests
    
#     Args:
#         file_path (String): path to the component tests file
 
#     Returns:
#         two list or pd.DataFrame: the valid and invalid automated component tests
#     """
#     # Load dataframe from the function load_component tests
#     component_tests = rw.load_msgateway_results(file_path, return_df=True)
    
#     # Check test status and write results in valid_component_tests
#     valid_component_tests = component_tests[(component_tests['status']=='PASS') | (component_tests['status']=='FAIL')]
    
#     # Check test status and write results in invalid_component_tests
#     invalid_component_tests = component_tests[(component_tests['status']!='PASS') & (component_tests['status']!='FAIL')]
    
#     # Return dataframe of valid and invalid tests
#     return valid_component_tests, invalid_component_tests




    