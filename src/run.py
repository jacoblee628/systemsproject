import argparse

from create_trace import create_trace
from validate_trace import validate_trace


def run(params):
    """Code that's run when run.sh or python src/run.py is called"""
    print("Running script")
    
    # Keep track of all errors as pd.DataFrame's of the error entries in a list
    invalid_dfs = []

    # 1. Create trace matrix based on test data files
    trace, invalid = create_trace(vv_folder_path, as_run_path, version_num, srs_prefix)
    invalid_dfs.extend(invalid)
    
    # 2. Validate trace matrix
    trace, invalid = validate_trace(trace, obs_srs_path, active_prd_path, prd_prefix, srs_prefix)
    invalid_dfs.extend(invalid)
    
    # 3. Export trace matrix and error log
    trace.to_csv(params["out_path"], index=False)
    
    print("Script finished")
    
    

if __name__ == "__main__":
    """This method allows for you to call this script from the console 
    
    >>> python run.py -o "output_file.xlsx" -m "path/to/manual_as_runs.docx" -s "obsolete_tests.csv" <CONTINUED; all the other args, listed below> 
    """
    parser = argparse.ArgumentParser(description='Trace matrix generation and validation. "
                                     "Can run this python script `run.py` in console, providing arguments "
                                     "that will be parsed')

    parser.add_argument("-o", "--out_path",
                        help="Output path of new trace matrix. Should have `.xlsx` in it",
                        default="new_trace.xlsx", required=False)
    parser.add_argument("-m", "--manual_as_runs",
                        help="Path to manual as-runs `.docx` document. NOTE: `.doc` will not work. You must convert it by doing `Save As` in Word",
                        required=True)
    parser.add_argument("-s", "--obs_srs_path",
                        help="Path to output from Rally containing all obsolete tests in a `.csv` file",
                        required=True)
    parser.add_argument("-p", "--active_prd_path",
                        help="Path to `.xlsx` containing a list of active prds",
                        required=True)
    parser.add_argument("-a", "--automated_tests_path",
                        help="Path to folder (named `ER####### v##` etc) containing the automated tests",
                        required=True)
    parser.add_argument("-v", "--version_num",
                        help="Version number, with two periods in it (i.e. 1.33.0)",
                        required=True)
    parser.add_argument("--prd_prefix",
                        help="PRD prefix (probably US)",
                        default="US",
                        required=False)
    parser.add_argument("--srs_prefix",
                        help="SRS prefix (TC or ESA-)",
                        default="US",
                        required=False)
    parser.add_argument("--verbose",
                        action="store_true",
                        help="If this flag is specified, will save to error log all errors AND tests filtered out during processing",
                        default=True,
                        required=False)
    
    # Get args from console input and convert to dict
    args = vars(parser.parse_args())
    
    # Run the script
    run(args)
