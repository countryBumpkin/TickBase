![TickBaseLogo](https://tickbase.net/wp-content/uploads/2021/01/TickBase-Logo-Horizontal_white-e1610842190868.png)
# TickBase
Data storage for web crawler results from TickBase project, summer 2021. The project aimed to:
1. Automate keyword searches of online article and dataset publishers. Allow users to input individual keyword searches or a CSV file of keywords to be used.
2. Use REST APIs provided by the publishers to compile article metadata.
3. Prevent duplicate resource accumulation. Many sources overlapping coverage so duplicates are removed using DOI comparisons. A record of all DOIs seen is maintained for future searches assuming that the user does not lose data once collected.
4. Allow accumulated data to be formatted and exported. The options for export are CSV file and DSpace items. CSV files are the default and will be created if no other option is selected. DSpace items may be created but depend on a DSpace host site to upload to.

# Code Usage
Code from this repository may only be used with the permission of Garrett Wells.

## Directory Contents
Here is some information for navigating the folders above and understanding their purpose.

### /code
Contains source [Python 3](https://www.python.org/downloads/) code. This code is a combination of APIs for interfacing with various web sources and crawling the web. It also contains the source code for [_**tickpicker.py**_: a command line application](https://github.com/countryBumpkin/TickBase/blob/main/code/tickpicker.py) which provides the quick access point to executing queries and collecting data. Use it to:
1. Run single keyword searches from 10 online data repositories such as PubMed, Mendeley, Figshare, NEON, and LTER. **NOTE** Google access may not be functional currently because code needed for exploring pages of data(spiders) is not included yet.
2. Run individual searches for every keyword provided in a CSV file.
3. Export stored data from this device to DSpace.
4. Manage the data collected on this machine.

#### Configuration
After cloning this repository, make sure there is a folder nameed _**data_dump**_ inside the _**code**_ folder. Output from the command line app will be placed in this folder.

#### Running tickpicker.py
    # after cloning repository...
    # and installing python3...
    # and any other necessary libraries as prompted...
    $ python3 tickpicker.py

### /data_dump
This folder contains some example output from searches on various databases. Each output file name contains the source, search keyword, and date of search. **Warning** this folder may not always be populated as it does not contain functional code is not part of any dependency tree.

### /searches
Contains example CSV files full of search keywords (mostly pertaining to ticks :)). Use these for testing or examples of how to construct your own search files.
