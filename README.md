This software is used to analyze a file system to determine the factors that affect the file size.

The software consists of two python scripts:

1. **find.py** This script scan the entire filesystem and creates the dataset containing information about accessible files and directories. The name of the file is *root.csv*.
1. **process.py** This script,
    - Imports the dataset in the file *root.csv*.
    - Performs data wrangling.
