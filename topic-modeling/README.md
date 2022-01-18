## topic-modeling

__authors__   = 'Scott Kleinman, Dan Baciu, Jeremy Douglass, Lindsay Thomas'  
__copyright__ = 'copyright 2021, The WE1S Project'  
__license__   = 'GPL'  
__version__   = '2.1'  
__email__     = 'lindsaythomas@miami.edu'

The code in this module is designed to work with data released in conjunction with the publication "The Humanities in Public" by Lindsay Thomas and Abigail Droge. It is meant to aid in the reproduction of our analysis and is designed with that goal in mind. Our data and code is based on data and code collected and developed for the WE1S project. See the following for more information about the WE1S data and for generalizable versions of our project code designed to work with a variety of data types:
* [WE1S datasets on Zenodo](https://zenodo.org/search?page=3&size=20&q=WhatEvery1Says#)
* [WE1S Workspace template archive on Zenodo](https://zenodo.org/record/5034712#.YVoLt6ApDOQ)

To run the code in this notebook, you will need to install MALLET on your machine. See the [MALLET documentation](http://mallet.cs.umass.edu/download.php) for more information on installation.

This notebook uses MALLET to topic model doc-terms files (those located in `data/doc-terms`). You can produce multiple topic models at a time for each collection or just one. It also produces the topic scaling metadata required by dfr-browser.

WE1S uses MALLET's `random_seed` parameter to make our models reproducible. The random seed for all of our topic models is set to 10. Models produced using this notebook use this setting as well.

### Models directory

The topic models you produce using this notebook will be stored in a folder named `data/models`. This folder will be created the first time you run this notebook. Within that directory, you will see subdirectories for each collection you have modeled. Within those subdirectories are folders corresponding to each model you have produced of that collection. For example, if you produced a 25-topic model and a 100-topic model of collection 33, you will see the following folders in `data/models`:

* `c33`
    * `topics25`
    * `topics100`
    
These folders contain the default outputs of MALLET's topic modeling process (and step 4 in this notebook):

* composition file
* diagnostics file
* keys file
* topic-docs file
* topic-state file
* topics_counts file
* topic-scaled file
* .mallet file

For more information on these outputs, see [MALLET's documentation](http://mallet.cs.umass.edu/topics.php). 