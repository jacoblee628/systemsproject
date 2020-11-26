import docx
import openpyxl as pyxl
import pandas as pd
from docx import Document
from openpyxl import Workbook


def load_trace(file_path, matrix_type, return_df=True):
    """Loads trace matrix .xlsx file and extracts data
    
    Args:
        file_path (String): path to the trace file
        matrix_type (String): "CO" or "PSC"
        return_df (bool, optional): If true (default), returns a pandas dataframe. Else, returns list of lists.

    Returns:
        list or pd.DataFrame: the trace data
    """
    print(f"Loading {matrix_type} from: {file_path}")

    # Some asserts to make sure inputs are valid
    assert ".xlsx" in file_path, "Trace file must be a .xlsx file"
    matrix_type = matrix_type.upper()
    assert matrix_type in ["CO", "PSC"], "Trace matrix type must be either 'CO' or 'PSC'"
    
    # Load in the actual excel file
    wb = pyxl.load_workbook(file_path)
    
    # Get the appropriate matrix from the workbook
    if matrix_type == "CO":
        ws = wb['CO Trace Matrix']
    else:
        ws = wb['PSC Trace Matrix']
        
    # get title of workbook
    title = ws['A1'].value
    print(f"Loading in worksheet titled: {title}")
    
    # extract headers for the table
    headers = [cell.value for cell in ws['A3':'E3'][0]]
    
    # load in the data row by row
    data = []
    for row in ws.iter_rows(min_row=4, max_col=5, values_only=True):
        row_data = [cell for cell in row]
        
        # Stop if all the row data is none
        # apparently the blank rows in the bottom of the worksheet are populated...
        if all([cell == None for cell in row_data]):
            break
        data.append(row_data)

    # Returns either pandas dataframe or a list of lists
    if return_df:
        return pd.DataFrame(data, columns=headers)
    else:
        return data
