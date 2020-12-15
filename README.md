# Trace Matrix Utility Description
The purpose of this trace matrix utility is to take in set of inputs and output a validated trace matrix.

The utility will take in the following inputs:
* SRS
* PRD
* Use Case Document
* Automation As-Runs
* Manual As-Runs
* List of Historical SRS
* List of Active PRD
* Previous Trace Matrix
* Release Number

The utility will then **process these files and output a new trace matrix** based on these files. In addition, the utility will **validate** the new trace matrix based on these checks:
* Manual tests are pass or fail
* Automated tests are pass or fail
* All PRD must have at least one SRS
* All SRS must have at least one test
* All SRS must have at least one PRD
* All PRD items referenced by SRS must exist (not obsolete) 
* All SRS referenced by tests must exist (not obsolete)
* All PRD referenced by tests must exist (not obsolete)

After the validation step, the utility will output an **error log** in a csv file with the rows that have been invalidated by the checks.


## Files Included
* `create_trace.py`
  * contains functions for creating the new trace matrix and validating manual and automatic tests
* `read_write.py`
  * contains functions for reading in input files
* `run.py`
* `select_file.py`
  * contains functions for creating a user interface
* `validate_trace.py`
  * contains functions for validating the new trace matrix

## Pipeline Description
`run.py/run()` is the main pipeline method.

On a high level it runs four main steps:
1. Read/parse data
2. Combine into trace matrix
3. Validate
4. Output

In more detail:
1. The method receives arguments (file paths, etc) from either UI (``select_file.py``) or command line (parsed in `run.py/main()`).
2. The method calls `create_trace.py/create_trace()`, which reads each dataset/document to a `pandas.DataFrame` (`read_write.py`) and processes it.
3. During this process, errors/invalid data are also gathered.
4. The DataFrame for each document is concatenated into a single DataFrame, which is the new trace matrix. This new trace and the list of invalid data DataFrames is then returned back to `run.py/main()`.
5. Validation. Trace is passed to `validate_trace.py/validate_trace()`, where it goes through each test and is returned, along with any invalid entries that were filtered out
6. Exporting trace and error log (`read_write.py/write_error_log()`) to `.csv`. 

## Installation
1. Download this folder using the green button labeled `Code` on the top right of the page. Unzip if needed.
2. Install [Anaconda](https://www.anaconda.com/products/individual) that has Python version>= 3.7. 
3. Now we need to install two small libraries in order to read Excel and Word files.

In command line, (search `cmd.exe` in Windows, `bash` in Linux, or `terminal` in Mac), `cd` to this folder and run this command:

```
pip install -r requirements.txt
```

Alternatively, you can run these commands without needing to navigate to the folder:

```
pip install python-docx
pip install openpyxl
```
You're done!

## How to Run Script

You can run this using either UI or command line.

**UI (Currently Windows only):**
1. Double click `start.exe` in this folder
2. Click select buttons to select corresponding files/folders
3. Input the version number in the pattern of #.#.#
4. Select srs prefix from the dropdown list
5. Click start button to start processing

**Command line (Works on all platforms):**
1. In your console, `cd` into this folder.
2. You can either modify the command in `run.sh` then call `./run.sh`, or run the script directly yourself:
```
python src/run.py -o "desired_trace_name.csv" -m "path/to/ER2228014 v51 ATT1 Manual As-Runs.docx" -s "data/Obsolete SRS_Test Cases_11.16 pull.csv" -p "data/1.33 PRD.xlsx" -a "data/ER2228014 v51 ATT2 Automated as-run" -v "1.33.0"
```

## Remaining/Incomplete Tasks
* Filling in these missing columns. 

![Sample Trace Matrix](sample_preview.png)

We commented out validation for now; should reenable once these have been added back.

* Verifying that current logic and process is correct
    * Particularly while formatting data in `create_trace.py`. 
* Writing more validation tests
