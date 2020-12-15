# Project Description
The purpose of this trace matrix utility is to take in the following inputs:
* SRS
* PRD
* Use Case Document
* Automation As-Runs
* Manual As-Runs
* List of Historical SRS
* List of Active PRD
* Previous Trace Matrix

The utililty will then process these files and output a new trace matrix based on these files. In addition, the utility will validate the new trace matrix based on these checks:
* All PRD must have at least one SRS
* All SRS must have at least one test
* All SRS must have at least one PRD
* All PRD items referenced by SRS must exist (not obsolete) 
* All SRS referenced by tests must exist (not obsolete)
* All PRD referenced by tests must exist (not obsolete)


# Files Included

# How To Use
