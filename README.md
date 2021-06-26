# About
The framework allows to determine relations of functional embedding on a set of multi-valued logics

for the set of logics you can get results in these views:
* sequence of strings
* csv file
* dot file

# Usage
To the input – a catalog with mvlog files  
At the output – a sequence of lines like:

    <name of logic-1> and <name of logic-2> : relation
 
Input catalog should be placed to the DATA_PATH  
Output files will be saved to the RESULT_PATH

### Interface 

    usage: main.py [-h] [-csv] [-dot] [-aggr] input
    
    positional arguments:
      input       name of dir in DATA_PATH with mvlog files
    
    optional arguments:
      -h, --help  show this help message and exit
      -csv        if you need to generate csv file
      -dot        if you need to generate dot file
      -aggr       if you want to run AggregatedComparator

### Recommendations
You could to use PyPy3 interpreter for a greater speed  
For correct writing of logging you should not to run program exemplars parallel