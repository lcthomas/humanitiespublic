## comparison

### Info

__author__    = 'Lindsay Thomas'
__copyright__ = 'copyright 2021, The WE1S Project'
__license__   = 'MIT'
__version__   = '2.0'
__email__     = 'lindsaythomas@miami.edu'

The code in this module is designed to work with data released in conjunction with the publication "The Humanities in Public" by Lindsay Thomas and Abigail Droge. It is meant to aid in the reproduction of our analysis and is designed with that goal in mind. Our data and code is based on data and code collected and developed for the WE1S project. See the following for more information about the WE1S data and for generalizable versions of our project code designed to work with a variety of data types:
* [WE1S datasets on Zenodo](https://zenodo.org/search?page=3&size=20&q=WhatEvery1Says#)
* [WE1S Workspace template archive on Zenodo](https://zenodo.org/record/5034712#.YVoLt6ApDOQ)

### chi_sq_test.ipynb
This notebook allows you to compare two variables to see if they are related. It implements a chi-square test for independence to determine if distributions of categorical variables differ from one another in a statistically meaningful sense. In our article, we use a chi-square test to test if there is a relationship between the subject an article is about (science or the humanities) and the type of newspaper that article appears in (top-circulating newspapers or student newspapers).

This notebook requires the user to set the 'csv_file' variable. This variable is set by default to upload the contingency table for the comparison we conduct in our article ('chi-sq-contingency-notext.csv'). This file contains only numbers and no labels. We have also included a labeled contingency table ('chi-sq-contingency.csv') that includes labels for the numerical values. The code in this notebook will not work with the labeled contingency table; it is provided for the user's reference.

Results are printed in the notebook.

For a good basic introduction to the chi-square test and to some of the terms used in this notebook, see [this tutorial](https://www.jmp.com/en_us/statistics-knowledge-portal/chi-square-test/chi-square-test-of-independence.html).

The code in this notebook is taken from here: <https://www.geeksforgeeks.org/python-pearsons-chi-square-test/>.

### compare_word_frequencies.ipynb

This noteboook allows you to compare two sets of textual data to one another to discover how, and how much, they differ. The notebook performs this comparison using the Wilcoxon rank sum test, a statistical test that determines if two samples (i.e., the relative frequencies of a specific word in two different datasets) are taken from populations that are significantly different from one another (meaning, if they have different distributions). When used to compare word frequency data from two different datasets, it helps you to determine what the most "significant" words in each dataset are.

For details on the Wilcoxon rank sum test, see [this description](https://data.library.virginia.edu/the-wilcoxon-rank-sum-test/) by the University of Virgina Library.

#### Input Folder

The `input` folder is too big for this repository. To download, go to this article's repository in Dataverse and download the `comparison` module.

The input folder contains all of the derivative files you need to reproduce the Wilcoxon rank sum tests we describe in the article. The 3 subdirectories in this folder are organized by type of comparison. These subdirectories include:

* `hum-sci`: Compare documents about the humanities to documents about science.
* `hum-not-hum`: Compare documents about the humanities to documents containing humanities keywords but that are not classified as being about the humanities.
* `not-hum-not-sci`: Compare documents containing humanities keywords but that are not classified as being about the humanities to documents containing science keywords but that arenot classified as being about science.

Each of these subdirectories includes the derivative files you need (and the files you can create using the code in this module). The files in each subdirectory are named in slightly different ways, but they all follow the same general patterns. The filenames explained below are in the `hum-sci` subdirectory:

* `hum-sci-doc-terms.txt`: A doc-terms file containing the filenames and bags of words for each document classified as being about the humanities and each document classified as being about science.
* `hum-500sample-filenames.txt`: The filenames of the documents we randomly selected from the humanities category.
* `sci-500sample-filenames.txt`: The filenames of the documents we randomly selected from the science category.
* `hum-sci-500sample-min5-vocablist.txt`: A list of all of the words (one per line) from the random samples of documents from both categories we compared.
* `hum-500sample-min5-df-raw.csv`: A sparse dataframe saved to a csv, includes all of the words from the random sample of the humanities category that occur more than 5 times in at least one category and the raw count of the number of times each word appears in each document in the sample.
* `hum-500sample-min5-df-relative.csv`: A sparse dataframe saved to a csv, includes all of the words from the random sample of the humanities category that occur more than 5 times in at least one category and the relative frequency of each word appears in each document in the sample.
* `sci-500sample-min5-df-raw.csv`: A sparse dataframe saved to a csv, includes all of the words from the random sample of the science category that occur more than 5 times in at least one category and the raw count of the number of times each word appears in each document in the sample.
* `sci-500sample-min5-df-relative.csv`: A sparse dataframe saved to a csv, includes all of the words from the random sample of the science category that occur more than 5 times in at least one category and the relative frequency of each word appears in each document in the sample.

#### Results Files

After running section 3 of this notebook, the results of your comparsion will be saved to a csv file in the `results` folder in this module. This csv will include a row for each term included in the test. Each row will display the term, the term's raw count in each category (for example, category 1 might equal articles about the humanities), the term's raw count in category 2 (for example, category 2 might equal articles about science), the difference between the 2 counts (count 1 minus count 2), the percentage change in the counts, the Wilcoxon statistic, and the Wilcoxon p-value. Sorting the csv by the Wilcoxon stat from greatest to least will cause the terms most strongly associated with category 1 to come to the top, while sorting it by the Wilcoxon stat from least to greatest will cause the terms most strongly associated with category 2 to come to the top. The p-value column provides you with information about how confident you can be about each comparison's significance.
