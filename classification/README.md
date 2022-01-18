## classfication

__authors__   = 'Lindsay Thomas, Ashley Hemm'  
__copyright__ = 'copyright 2021, The WE1S Project'  
__license__   = 'GPL'  
__version__   = '2.1'  
__email__     = 'lindsaythomas@miami.edu'

The code in this module is designed to work with data released in conjunction with the publication "The Humanities in Public" by Lindsay Thomas and Abigail Droge. It is meant to aid in the reproduction of our analysis and is designed with that goal in mind. Our data and code is based on data and code collected and developed for the WE1S project. See the following for more information about the WE1S data and for generalizable versions of our project code designed to work with a variety of data types:
* [WE1S datasets on Zenodo](https://zenodo.org/search?page=3&size=20&q=WhatEvery1Says#)
* [WE1S Workspace template archive on Zenodo](https://zenodo.org/record/5034712#.YVoLt6ApDOQ)

This notebook takes you through the process of training and testing a binary classification model. It uses sklearn's machine learning library. WE1S has created training data for 4 kinds of news documents: obituaries, announcements, articles about the humanities, and articles about science. The training data is located in the appropriately named folders in this module. 

This notebook is written for binary, exclusive classification problems only (i.e., it assumes you are trying to classify documents into one of two classes). Because the notebook was written as an interactive tutorial, unlike other notebooks in this code repo, there is no separate script file. All of the code you need is contained within this notebook itself.

### How to Use this Notebook

This notebook contains 3 sections. The first allows you to use WE1S training data to develop and evaluate a classification model for data for which classifications are already known. Training data documents may or may not be included in the json documents released with this code repo. Ashley Hemm assisted in creating this training data. 

The training data is located in the following directories within this module:
* `humanities`
    * `hum-postive.txt`: A list of filenames of documents manually classified as being about the humanities.
    * `hum-positive.csv`: The filenames and bags of words from documents manually classified as being about the humanities. This file is structured in the way the `classification.ipynb` expects it.
    * `hum-negative.txt`: A list of filenames of documents manually classified as not being about the humanities.
    * `hum-negative.csv`: The filenames and bags of words from documents manually classified as not being about the humanities. This file is structured in the way the `classification.ipynb` expects it.
* `science`
    * `sci-positive.txt`: A list of filenames of documents manually classified as being about science.
    * `sci-positive.csv`: The filenames and bags of words from documents manually classified as being about science. This file is structured in the way the `classification.ipynb` expects it.
    * `sci-negative.txt`: A list of filenames of documents manually classified as not being about science.
    * `hum-negative.csv`: The filenames and bags of words from documents manually classified as not being about science. This file is structured in the way the `classification.ipynb` expects it.
* `announcements`
    * `announce-postive.txt`: A list of filenames of documents manually classified as being event announcements.
    * `announce-positive.csv`: The filenames and bags of words from documents manually classified as being event announcements. This file is structured in the way the `classification.ipynb` expects it.
    * `announce-negative.txt`: A list of filenames of documents manually classified as not event announcements.
    * `announce-negative.csv`: The filenames and bags of words from documents manually classified as not being event announcements. This file is structured in the way the `classification.ipynb` expects it.
* `obits`
    * `obits-postive.txt`: A list of filenames of documents manually classified as being obituaries.
    * `obits-positive.csv`: The filenames and bags of words from documents manually classified as being obituaries. This file is structured in the way the `classification.ipynb` expects it.
    * `obits-negative.txt`: A list of filenames of documents manually classified as not being obituaries.
    * `hum-negative.csv`: The filenames and bags of words from documents manually classified as not being obituaries. This file is structured in the way the `classification.ipynb` expects it.

The second section of the `classification` notebook allows you to use our training data to produce a model and apply it to data for which classifications are not known (i.e., the data in each of the collections discussed in this repo's `README.md`). The third section allows you to save the results of your experiments to disk. Results will be saved to this module's `results` directory.

We used section 1 to assist in deciding which classification models to use on our various data sets, and section 2 to train and test these models against unseen data. 

The results we obtained and that we discuss in our article are included in the `data/tables` directory of this repo. There, we separate our results into 4 lists of filenames: 
* `about-hum-files.txt`: Filenames of all documents classified as being about the humanities 
* `about-sci-all-filenames.txt`: Filenames of all documents classified as being about science
* `not-about-hum-hum-keywords-filenames.txt`: Filenames of all documents containing humanities keywords that were not classified as being about the humanities
* `not-about-sci-sci-keywords-filenames.txt`: Filenames of all documents containing science keywords that were not classified as being about science

### A Note on our Data

How we conducted our classification experiments requires some explanation. We did not classify all of our data at once. In order to conduct more fine-grained analysis using other tools and methods, our data was originally broken up into a series of smaller, overlapping collections based on search keyword and source type. For instance, for this article, we used 4 of these different collections composed of documents from student newspapers and top-circulating US newspapers: `c14`, `c18`, `c20`, and `c21`. 

We have provided this data for you to use as it was originally organized in this repo. Therefore, to replicate our experiments, you should use the derived data from the appropriate collections names above that is stored in `data/doc-terms` as input. These files are further explained in the repo's `README.md` file. This data has been processed from the original json files using the `prepare-data` module in this code repo. 

To replicate our process, you should apply our classification methods to these collections one at a time.
