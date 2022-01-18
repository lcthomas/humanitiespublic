# The Humanities in Public Code and Data Repository

__authors__   = 'Lindsay Thomas, Abigail Droge'
__copyright__ = 'copyright 2021, The WE1S Project'
__license__   = 'GPL'
__version__   = '2.1'
__email__     = 'lindsaythomas@miami.edu'

The code in this repository is designed to work with data released in conjunction with the publication "The Humanities in Public: A Computational Analysis of US National and Campus Newspapers" by Lindsay Thomas and Abigail Droge, published in *The Journal of Cultural Analytics*. It is meant to aid in the reproduction of our analysis and is designed with that goal in mind. Our data and code is based on data and code collected and developed for the WhatEvery1Says project (WE1S). See the following for more information about the WE1S data and for generalizable versions of our project code designed to work with a variety of data types:
* [WE1S datasets on Zenodo](https://zenodo.org/search?page=3&size=20&q=WhatEvery1Says#)
* [WE1S Workspace template archive on Zenodo](https://zenodo.org/record/5034712#.YVoLt6ApDOQ)

This repo includes a `data` folder and 5 folders that each correspond to a different method of analysis or exploration we employ in our article. We call these folders "modules." Modules and data are each described below.

The code in this repo expects the repo to be organized as we have organized it here. If you rename included folders or files or move them around, the included code may not function as expected without redefining file paths.

## Acknowledgments

The code, data, and documentation in this repository was prepared for use in conjunction with this article by Lindsay Thomas. However, because the code and data we use in this article is based on that developed for WE1S, it was originally collected, written, and refined through the efforts of a large number of people who participated in WE1S over several years. Individual module README.md files include the names of individuals who contributed directly to the creation of the code or data used in that module. Participants who contributed to the collection and curation of the WE1S data used in this article include Alan Liu, Jeremy Douglass, Scott Kleinman, Lindsay Thomas, Abigail Droge, Rebecca Baker, Francesca Battista, Kristin Cornelius, Suchismita Dutta, Ashley Hemm, Kyle Duncan, Helen Foley, Jessica Gang, Naz Keynejad, Sara Lafia, Alexandria Morgan, Dieyun Song, Leila Stegemoeller, Ruth Trego, Amy Windham, and Greg Janée. A full list of WE1S participants can be found on the [project participants page](https://we1s.ucsb.edu/about/team/).

## Modules

Modules are organized by method or process. Module folders include:

* `prepare-data`: Methods for unzipping `json.zip` and preparing data for use in other modules. Any process that requires full access to document json data is included here. As described below, our repo also includes all deriviative files you will need to reproduce the analyses we perform in the article. Therefore, you only need to use this module if you want to replicate these files for yourself or if you want to create files for analyses other than those we discuss in the article.
* `classification`: Classify documents into one of 2 categories. We used these processes to classify documents as being about the humanities or about science.
* `comparison`: This module includes 2 notebooks: `compare_word_frequencies.ipynb` and `chi_sq_test.ipynb`. `compare_word_frequencies.ipynb` includes methods for comparing two groups of documents to one another using a Wilcoxon rank sum test. We used this method to compare documents about the humanities to documents about science, documents containing humanities keywords but not classified as being about the humanities to documents containing science keywords but not classified as being about science, and documents about the humanities to documents containing humanities keywords but not classified as being about the humanities. `chi_sq_test.ipynb` includes methods for using a chi-square test for independence to compare two variables to see if they are related. We use a chi-square test to test if there is a relationship between the subject an article is about (science or the humanities) and the type of newspaper that article appears in (top-circulating newspapers or student newspapers).
* `topic-modeling`: Topic model a collection. You may produce one or multiple topic models. In our article, we discuss topic models of collections 33 and 36 (see below for more on collections).
* `dfr-browser`: Produce a dfr-browser using Andrew Goldstone's dfr-browser Python implementation. We used dfr-browser to explore the topic models we discuss in the article.

Each module includes the following:

* A `README.md` detailing information and instructions specific to that module.
* At least one Jupyter notebook that provides an interface to the code for that module.
* Modules may also include:
    * One or mutiple `scripts` folders that include classes and functions called in the notebook.
    * Folders containing derivative data used in that module.
    * Folders where the results of the analyses performed in that module will be stored.

## Data

The data directory is too large for this repository. To download, go to [this article's repository in Dataverse](https://doi.org/10.7910/DVN/BD9CE8) and download `data.tgz`.

### About our data

The data we discuss in this article was downloaded from the LexisNexis API by publication using keyword searches. We used 3 groupings of keywords to collect this data:

* humanities keywords: We gathered this data by searching for documents containing "humanities" or "liberal arts".
* science keywords: We gathered this data by searching for documents containing "science" and "sciences".
* comparison keywords: WE1S gathered this data using keyword searches of 3 of the most common words in the English language (based on a well-known analysis of the Oxford English Corpus) that LexisNexis indexes and thus makes available for search: “person,” “say,” and “good”. We excluded the word "humanities" from our search in collecting these documents. For more information about our comparison corpus data, see "comparison-not-humanities" on this page: <https://we1s.ucsb.edu/research/we1s-materials/datasets/>.

Except for documents collected using our comparison keywords, we did not use exclusive keyword searches to collect our data. This means that a document collected in a search for documents containing "science" or "sciences" might also contain the word "humanities," and vice versa.

We also collected many duplicate documents from LexisNexis. To sort out these duplicates, WE1S applies a de-duplication algorithm to its data. The de-duplication process found 4,602 duplicate documents, giving us 142,602 total "unique" documents. We count as "duplicates" any document that is 63% similar to another document. We found through experimentation that this fairly aggressive approach to de-duplication allows us to capture not only exact duplicates, but also updated articles, which include maybe just a new line or two, and articles published by a different outlet with only a few new or different lines (but often different metadata). We consider all of these different cases to be "duplicates."

The rest of this section describes the contents of the `data` directory.

### json.zip

The 147,204 documents we analyze in our article are included in this repo in `json.zip`. This zip file includes 148 zipped, numbered subdirectories; 147 of these subdirectories contain json documents of 1000 documents each; 1 contains 204 json documents. This file is about 1 GB compressed; uncompressed it's about 18 GB.

Json documents do not contain full-text data (content). They contain transformed full-text data, as described below. Json documents are structured and formatted according to the WE1S manifest schema. You can learn more about the schema and about json documents in general on ["The WE1S Manifest Schema"](https://whatevery1says.github.io/manifest/) documentation site. Each json document includes the following fields (field values are scraped from the LexisNexis API unless otherwise indicated):

* pub: The document's publication title. For the top newspaper documents in our data, this is the title of the newspaper (e.g., *The New York Times*, and for our student newspapers this is "University Wire." University wire is a campus newspaper aggregation service.
* pub_date: The document's publication date in datetime format.
* length: The number of words in the document's content pre-tokenization by spaCy (see "features" below for more on spaCy).
* section: The section of the paper the article appeared in.
* author: The document author.
* title: The title of the document.
* copyright: The copyright holder of the document.
* name: The filename of the document (added by WE1S). The filename is structured in a specific way. Here is an example filename: `172244_172244_universitywire_bodyliberalpre1pluralartsorhleadliberalpre1pluralarts_1998-01-01_1998-12-31_38_36_0`. Its parts include:
    * `172244_172244`: The pub index number (from LexisNexis)
    * `universitywire`: The pub title (added by WE1S)
    * `bodyliberalpre1pluralartsorhleadliberalpre1pluralarts`: The search term WE1S used to collect the document. In this case it's "liberal arts".
    * `1998-01-01_1998-12-31`: The year used to collect the document (added by WE1S).
    * `38_36_0`: Iterators added to the document during collection (added by WE1S).
* database: The service the document was collected from (added by WE1S).
* features: A list of lists containing each token in the document content and associated metadata (added by WE1S). Processed using spaCy's language model in the WE1S preprocessing pipeline. See the [spaCy documentation](https://spacy.io/usage/spacy-101) for more information on the language model. Each token list includes the following information:
    * token: the token
    * norm: the normalized version of the token
    * lemma: the token lemma
    * pos: the simplified UPOS token part-of-speech tag
    * tag: the detailed part-of-speech tag
    * stopword: Boolean describing if the token is a stopword or not
    * entities: named entity tag
* bag_of_words: A dictionary containing each token from the document content and the number of times it appears (added by WE1S).
* word_count: The number of words in the document as counted by spaCy (added by WE1S).
* source: The standardized source name given to the document publication by WE1S researchers. Because LexisNexis does not standardize publication titles, resulting in multiple variations of the same title, WE1S manually standardized publication titles.
* tags: The metadata tags describing a document's publication (added by WE1S).
* keyword: The search term used in to collect the document (added by WE1S).

### doc-terms

This folder contains what we call doc-terms files corresponding to the different collections of our data we analyze in the article. A doc-terms file is a line-delimited string of rows, with each row representing one document. Each row is a space-separated list of alphabetized terms with each term repeated once for the number of times it occurs in the document.

Each doc-terms file corresponds to a WE1S collection. We have preserved the WE1S collection numbers; materials published on the WE1S website also use these collection numbers. More information on WE1S collections is available on the ["Key Collections" page](https://we1s.ucsb.edu/research/we1s-materials/collections-topic-models/) on our site.

We include doc-terms files for the following collections:

* `c14-doc-terms`: Documents from US student newspaper sources collected using 'humanities' and 'liberal arts' as search terms.
* `c18-doc-terms`: Documents from US student newspaper sources collected using 'science' or 'sciences' as search terms.
* `c20-doc-terms`: Documents from US top-circulating newspapers collected using 'humanities' or our comparison keywords as search terms.
* `c21-doc-terms`: Documents from US top-circulating newspapers collected using 'humanities,' 'science,' or 'sciences' as search terms.
* `c33-doc-terms`: Documents classified as being about the humanities or about science from US top-circulating newspapers and student newspapers. We discuss a topic model of this collection in the "Public Discourse About the Humanities" section in our article.
* `c36-doc-terms`: Documents containing the word "humanities" but that were classified as not being about the humanities. We discuss a topic model of this collection in the "Humanities Public Discourse" section in our article.
* `c36a-doc-terms`: Documents containing humanities keywords ("humanities" or "liberal arts") but that were classifed as not being about the humanities.
* `c37-doc-terms`: Documents containing science keywords ("science" or "sciences") but that were classified as not being about science.

### filelists

This folder contains lists of filenames included in the above collections. It also includes the following 2 lists:

* `all-noduplicates-filenames.txt`: The filenames of all of the unique documents in our data (142,602 documents).
* `duplicates-filenames.txt`: The filenames of all of the duplicate documents in our data (4,602 documents).

### metadata-c33 and metadata-c36

These folders contain the metadata files needed to produce dfr-browsers for collections 33 and 36. We discuss models of these collections in the article. Each folder contains files our implementation of dfr-browser needs: `meta.csv`, `meta.temp.csv`, and `metadata-dfrb.csv`. These files are all different versions of the same metadata file (sorry about that!).

### tables

This folder contains information about the files we used in creating the tables that appear in the article. It also includes information about any files referenced in the article's notes. This folder includes its own `README.md`, which contains information about each file.
