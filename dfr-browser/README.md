## create_dfrbrowser

__authors__   = 'Jeremy Douglass, Scott Kleinman, Lindsay Thomas'  
__copyright__ = 'copyright 2021, The WE1S Project'  
__license__   = 'GPL'  
__version__   = '1.2.1'  
__email__     = 'lindsaythomas@miami.edu'

The code in this module is designed to work with data released in conjunction with the publication "The Humanities in Public" by Lindsay Thomas and Abigail Droge. It is meant to aid in the reproduction of our analysis and is designed with that goal in mind. Our data and code is based on data and code collected and developed for the WE1S project. See the following for more information about the WE1S data and for generalizable versions of our project code designed to work with a variety of data types:
* [WE1S datasets on Zenodo](https://zenodo.org/search?page=3&size=20&q=WhatEvery1Says#)
* [WE1S Workspace template archive on Zenodo](https://zenodo.org/record/5034712#.YVoLt6ApDOQ)

This notebook provides an interface to code that creates Andrew Goldstone's [dfr-browser](https://github.com/agoldst/dfr-browser) from a topic model produced with MALLET. You can use this notebook to produce multiple dfr-browsers for the same collection at once. Dfr-browser code, stored in this module in `scripts/dfrb_scripts`, was written by Andrew Goldstone and adapted for our use and data. We use an older version of Goldstone's code (v0.5.1); see <https://agoldst.github.io/dfr-browser/> for a version history of Goldstone's code. WE1S uses Goldstone's prepare_data.py Python script to prepare the data files (<https://github.com/agoldst/dfr-browser/blob/master/bin/prepare-data>), NOT the R package.
See <https://github.com/agoldst/dfr-browser> for Goldstone's original code and documentation.

You will only be able to create dfr-browsers for topic models you have created using the `topic-modeling` module in this repo. 

### Browser Metadata

This module draws on metadata files located in the `data` directory. This repo comes with the required metadata for collections 33 and 36 (see the repo `README.md` to learn more about collections). In the `data` directory in this repo, you will see the following 2 metadata folders:

* `metadata-c33`
* `metadata-c36`

These folders contain the files our implementation of dfr-browser needs: `meta.csv`, `meta.temp.csv`, and `metadata-dfrb.csv`. These files are all different versions of the same metadata file (sorry about that!). These folders correspond to the topic models we discuss in the article. If you wish to create dfr-browsers for topic models of these collections, you are ready to go. If you wish to create dfr-browsers for other collections, you will need to produce the required metadata files using the `prepare-data` module before proceeding with this module.

### Browser Data

After creating your selected dfr-browsers, subdirectories for each collection you produced browsers for will appear in this module's directory. They will be named by collection (`c33`, for example, for collection 33). Within those subdirectories are folders corresponding to each browser you have produced of that collection. For example, if you produced a browser for a 25-topic model and a 100-topic model of collection 33, you will see the following folders in this module:

* `c33`
    * `topics25`
    * `topics100`

The data for each dfr-browser is located within the `topics` folders.

### Viewing Your Dfr-Browser

Instructions for viewing your dfr-browser on your machine are included in section 2 of the `create_dfrbrowser.ipynb` notebook. These instructions detail how to use Python's `http.server` module to host your browser locally. They require you to use the command line to view your browser.

We have also made dfr-browsers of collections 33 and 36, the topic models we discuss in the article, publicly available:

* [Browser for collection 33](http://harbor.english.ucsb.edu:10002/collections/20200515_1455_us-classification-results-top-newspapers-universitywire-hum-sci/dfr-browser/topics100/) (model discussed in the "Public Discourse About the Humanities" section of the article)
* [Browser for collection 36](http://harbor.english.ucsb.edu:10002/collections/20200522_1900_us-humanities-classification-results-top-newspapers-universitywire-not-hum/dfr-browser/topics150/) (model discussed in the "Humanities Public Discourse" section of the article)
