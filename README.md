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

The utililty will then **process these files and output a new trace matrix** based on these files. In addition, the utility will **validate** the new trace matrix based on these checks:
* Manual tests are pass or fail
* Automated tests are pass or fail
* All PRD must have at least one SRS
* All SRS must have at least one test
* All SRS must have at least one PRD
* All PRD items referenced by SRS must exist (not obsolete) 
* All SRS referenced by tests must exist (not obsolete)
* All PRD referenced by tests must exist (not obsolete)

After the validation step, the utility will output an **error log** in a csv file with the rows that have been invalidated by the checks.


# Files Included
* **create_trace.py**
  * contains functions for creating the new trace matrix and validating manual and automatic tests
* **read_write.py**
  * contains functions for reading in input files
* **run.py**
* **select_file.py**
  * contains functions for creating a user interface
* **validate_trace.py**
  * contains functions for validating the new trace matrix

# How To Use
