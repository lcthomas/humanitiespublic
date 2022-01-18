## prepare-data

__authors__   = 'Scott Kleinman, Lindsay Thomas'  
__copyright__ = 'copyright 2021, The WE1S Project'  
__license__   = 'GPL'  
__version__   = '2.1'  
__email__     = 'lindsaythomas@miami.edu'

The code in this module is designed to work with data released in conjunction with the publication "The Humanities in Public" by Lindsay Thomas and Abigail Droge. It is meant to aid in the reproduction of our analysis and is designed with that goal in mind. Our data and code is based on data and code collected and developed for the WE1S project. See the following for more information about the WE1S data and for generalizable versions of our project code designed to work with a variety of data types:
* [WE1S datasets on Zenodo](https://zenodo.org/search?page=3&size=20&q=WhatEvery1Says#)
* [WE1S Workspace template archive on Zenodo](https://zenodo.org/record/5034712#.YVoLt6ApDOQ)

This notebook unpacks json data included in this repo and prepares this data for analysis using the other notebooks in this code repo. All methods that require access to fully unpacked json documents are included in this notebook. 

### Notebook Sections

1. Section 1, "Unzip Json Directory": Unzips `data/json.zip` and creates a directory of unpacked json files (called `data/json`). This directory contains numbered subdirectories of up to 1000 json documents each. 
2. Section 2, "Create Doc-Terms Files Needed for Analysis": Uses the provided list of filenames (`filelist_file`) to select specific files in the unpacked `data/json` directory. Produces a txt document containing the filenames and bag of words data from only those documents listed in `filelist_file`. The conversion script uses the `bag_of_words` field in each json file to produce the dervied file. We call these derived files doc-terms files. A doc-terms file is a line-delimited string of rows, with each row representing one document. Each row is a space-separated list of terms with each term repeated once for the number of times it occurs in the document. The other modules in this repo use these files as input. 
3. Section 3, "Create Metadata": Uses the provided list of filenames (`filelist_file`) to select specific files in the unpacked `data/json` directory to produce the metadata files that the dfr-browser visualization needs. In writing our article, we used dfr-browser to examine topic models of collection 33 and collection 36 (see the repo `README.md` for more information on collections and collection numbers). We have included the metadata information for these dfr-browser visualizations in the 2 `metadata` directories included in this repo (`metadata-c33`, and `metadata-c36`). 