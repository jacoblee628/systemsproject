import docx
import openpyxl as pyxl
import pandas as pd
from docx import Document
from openpyxl import Workbook
import pathlib
from pathlib import Path

def read_trace(file_path, matrix_type, return_df=True):
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

def load_manual_tests(file_path, return_df=True):
    """Loads in the test statuses from the manual tests document. Document must be in .docx format.

    Args:
        file_path (String): path to the file
        return_df (bool, optional): If true, returns pandas dataframe. Else dict. Defaults to True.

    Returns:
        pd.DataFrame or dict: Test names and corresponding statuses
    """
    # Make sure file is in docx format, not doc
    assert ".docx" in file_path, "File must be converted from .doc to .docx. Do this in Microsoft Word by selecting 'File -> Save As -> .docx'"

    # Open the file and read with python-docx package 
    with open(file_path, 'rb') as f:
        document = Document(f)

    # Get the test statuses
    statuses = []
    for i, table in enumerate(document.tables):
        if table.cell(0,0).text == "Status:":
            statuses.append(table.cell(0,1).text)
    
    # Get the test names
    test_names = []
    for i, paragraph in enumerate(document.paragraphs):
        if "Run ID" in paragraph.text:
            test_names.append(document.paragraphs[i-1].text)
            
    # Make sure same number of test names and statuses
        assert len(test_names) == len(statuses), "Error: Couldn't parse same number of test names and test statuses.\n# test names: {len(test_names)}, # statuses: {len(statuses)}"


    # Output as either pandas dataframe or dict, depending on return_df setting.
    data = {"test_name":test_names, "status":statuses}

    if return_df:
        return pd.DataFrame(data)
    else:
        return data
    
def load_msgateway_results(file_path, return_df=True):
    """Loads in the test statuses from the automatic MSGateway tests document. Document must be in .docx format.

    Args:
        file_path (String): path to the file
        return_df (bool, optional): If true, returns pandas dataframe. Else dict. Defaults to True.

    Returns:
        pd.DataFrame or dict: Test names and corresponding statuses
    """
    # Read the document
    with open(file_path, 'rb') as f:
        document = Document(f)

    # Get the names of the tests
    test_names = []
    for p in document.paragraphs:
        if "Test:" in p.text and "\t" not in p.text:
            test_names.append(p.text)

    statuses = []
    for table in document.tables:
        if "Execution Status" in table.cell(0,0).text:
            statuses.append(table.cell(1,0).text)
    
    # Make sure same number of test names and statuses
    assert len(test_names) == len(statuses), "Error: Couldn't parse same number of test names and test statuses.\n# test names: {len(test_names)}, # statuses: {len(statuses)}"

    # Output as either pandas dataframe or dict, depending on return_df setting.
    data = {"test_name":test_names, "status":statuses}

    if return_df:
        return pd.DataFrame(data)
    else:
        return data
    
def read_performance_test_results_by_tc(file_path, return_df=True):
    """Loads in the test statuses from the automatic PerformanceTestResultsByTC excel sheet.
    Document must be in .xlsx format.
    
    NOTE: Noticed it's manually filled out, so this may break.
          You can change the column names, and add/remove columns,
          but don't leave any blank rows between data you want to have processed.

    Args:
        file_path (String): path to the file
        return_df (bool, optional): If true, returns pandas dataframe. Else dict. Defaults to True.

    Returns:
        pd.DataFrame or dict: Test names and corresponding statuses
    """
    # Load workbook
    wb = pyxl.load_workbook(file_path)

    # Read table values (includes header at row 1)
    contents = []
    for row in wb.worksheets[0].values:
        # Break if all the values in the row are empty
        if all([value is None for value in row]):
            break
        contents.append(row)
    
    df = pd.DataFrame(contents[1:], columns=contents[0])

    # Return pandas dataframe if specified, otherwise return a list of dicts
    if return_df:
        return df
    else:
        return df.to_dict('records')
    
def read_rest_api_tests(folder_path, return_df=True):
    """Reads in all the rest api automatic test .txt files. 
    
    Will recursively go through the folders and read in .txt files.
    Make sure everything is unzipped first; in future can add functionality to
    unzip automatically if needed.
    
    Args:
        folder_path (String): path to the main RestApiTests folder.
        return_df (bool, optional): If true, returns pandas dataframe. Else dict. Defaults to True.

    Returns:
        pd.DataFrame or dict: Test names and corresponding statuses
    """
    if isinstance(folder_path, str):
        folder_path = Path(folder_path)
    
    # Read all .txt files recursively in the folders
    file_list = list(folder_path.glob("*/*/*.txt"))

    # Load in the data from each file, add to a single list
    data = []
    for file_name in file_list:
        data.extend(_read_group_by_method_txt(file_name, return_df=False))
    
    if return_df:
        return pd.DataFrame(data)
    else:
        return data
    
def _read_group_by_method_txt(file_path, return_df=True):
    """Reads in a single rest api automatic test .txt file. 
    
    Mostly just for the `read_rest_api_tests()` method. Usually won't need to call
    
    Args:
        folder_path (String): path to the main RestApiTests folder.
        return_df (bool, optional): If true, returns pandas dataframe. Else dict. Defaults to True.

    Returns:
        pd.DataFrame or dict: Test names and corresponding statuses
    """
    # If receive str, convert to pathlib object
    if isinstance(file_path, str):
        file_path = Path(file_path) 

    # Read in file using pathlib method, split on new line symbols
    lines = file_path.read_text().split("\n")

    # Remove blank lines
    lines = [line for line in lines if len(line) > 0]

    data = []
    for line in lines:
        # split on the | char; should only be one of them
        line_data = line.split("|")

        # For some reason if theres multiple of that char, only consider the last one
        if len(line_data) > 2:
            print(f"found line with multiple '|' chars: {line}")
            line_data = "".join(line_data[:-1]) + [line_data[-1]]
        
        # Store data in list
        data.append({
            'test_name':line_data[0],
            'status':line_data[1],
            'rc': file_path.parts[-3],
            'name': file_path.parts[-2],
            'file_name': file_path.parts[-1]
        })

    if return_df:
        return pd.DataFrame(data)
    else:
        return data