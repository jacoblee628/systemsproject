import docx
import openpyxl as pyxl
import pandas as pd
from docx import Document
from openpyxl import Workbook


def load_trace(file_path, return_df=True):
    """Loads trace matrix .xlsx file and extracts data
    
    for now, only loads in CO; can be modified to extract PRD

    Args:
        file_path (String): path to the trace file
        return_df (bool, optional): If true (default), returns a pandas dataframe. Else, returns list of lists.

    Returns:
        list or pd.DataFrame: the trace data
    """
    assert ".xlsx" in file_path, "Trace file must be a .xlsx file"
    
    # Load in the actual excel file
    wb = pyxl.load_workbook(file_path)
    
    # Just get the CO matrix for now TODO: write in option for loading PRD (should be simple)
    ws = wb['CO Trace Matrix']
    
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
