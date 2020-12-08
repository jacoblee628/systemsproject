import read_write as rw
import pandas as pd

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
    trace=rw.load_trace(file_path, matrix_type, return_df=True)
    
    # return trace matrix
    return trace
   
