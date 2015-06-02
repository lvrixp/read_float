# Description #

### Directory structure ###

    ├── readme.md           # this file
    ├── src
    │   └── read_float.py   # tool code
    └── test
        └── test_cases.md   # test plan
        └── unit_test.py    # unit test

### Design consieration ###

* Support big file and avoid read too much data at one time
    * use mmap to map the file to gain performance improvement on big file
    * create a generator to process the file in float item base instead of line base (to handle long line)
* Support special format float number like 10,000.0
    * set locale to handle the failure case of built-in float() conversion

### Tool usage ###

    Usage: read_float.py [options]
    
    Options:
      -h, --help            show this help message and exit
      -f FILE_PATH, --filepath=FILE_PATH
                            file path to be read

### Testing ###

* Go to test directory and run:

        python unit_test.py

### Limitation  ###
* All though we've considered big file scenarios: we mmap it and read each item instead of line, we still have limitation in handling big item: think about a float representation of big length, our code still need to read in entire item first, then parse it. We need to consider whether we really want to support it, if we do, we may need to split the item into chunk or think about other solution. If we do not want to support it, we can set a length limit on the item that been read.
