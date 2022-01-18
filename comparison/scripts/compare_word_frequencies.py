"""compare_word_frequencies.py.

Compare two datasets to one another using a Wilcoxon rank sum test.

For use with compare_word_frequencies.ipynb v 2.0.

"""

from scipy.stats import mannwhitneyu
from scipy.stats import ranksums
import os
import csv
import json
import collections
from collections import Counter
from collections import defaultdict
import pandas as pd
import statistics
import random

def set_comparison(comparison, reproduce, data_dir):
    '''Sets needed variables with appropriate filenames for the comparison the user wants to run.'''
    if comparison == 'hum-sci':
        # larger collection you want to select from
        collection = 'input/hum-sci/hum-sci-doc-terms.txt'
        if reproduce == True:
            # these are the filenames of the 500 documents from each category that we tested
            filenames_c1 = 'input/hum-sci/hum-500sample-filenames.txt'
            filenames_c2 = 'input/hum-sci/sci-500sample-filenames.txt'
        if reproduce == False:
            # all of the files classified in a certain category
            filenames_c1 = data_dir + '/tables/about-hum-files.txt'
            filenames_c2 = data_dir + '/tables/about-sci-files.txt'
        # files the code will create -- can use provided filenames below or your own
        if reproduce == True:
            docterms_c1 = 'input/hum-sci/hum-500sample-doc-terms-reproduce.txt'
            docterms_c2 = 'input/hum-sci/sci-500sample-doc-terms-reproduce.txt'
        if reproduce == False:
            docterms_c1 = 'input/hum-sci/hum-500sample-doc-terms-new.txt'
            docterms_c2 = 'input/hum-sci/sci-500sample-doc-terms-new.txt'
    elif comparison == 'not-hum-not-sci':
        # larger collection you want to select from
        collection = 'input/not-hum-not-sci/not-hum-not-sci-doc-terms.txt'
        if reproduce == True:
            # these are the filenames of the 500 documents from each category that we tested
            filenames_c1 = 'input/not-hum-not-sci/not-hum-1500sample-filenames.txt'
            filenames_c2 = 'input/not-hum-not-sci/not-sci-1500sample-filenames.txt'
        if reproduce == False:
            # all of the files classified in a certain category
            filenames_c1 = data_dir + '/tables/not-about-hum-hum-keywords-filenames.txt'
            filenames_c2 = data_dir + '/tables/not-about-sci-sci-keywords-filenames.txt'
        # files the code below will create -- can use provided filenames below or your own
        if reproduce == True:
            docterms_c1 = 'input/not-hum-not-sci/not-hum-1500sample-doc-terms-reproduce.txt'
            docterms_c2 = 'input/not-hum-not-sci/not-sci-1500sample-doc-terms-reproduce.txt'
        if reproduce == False:
            docterms_c1 = 'input/not-hum-not-sci/not-hum-1500sample-doc-terms-new.txt'
            docterms_c2 = 'input/not-hum-not-sci/not-sci-1500sample-doc-terms-new.txt'
    elif comparison == 'hum-not-hum':
        # larger collection you want to select from
        collection = 'input/hum-not-hum/hum-not-hum-doc-terms.txt'
        if reproduce == True:
            # these are the filenames of the 500 documents from each category that we tested
            filenames_c1 = 'input/hum-not-hum/hum-1500sample-filenames.txt'
            filenames_c2 = 'input/hum-not-hum/not-hum-1500sample-filenames.txt'
        if reproduce == False:
           # all of the files classified in a certain category
            filenames_c1 = data_dir + '/tables/about-hum-files.txt'
            filenames_c2 = data_dir + '/tables/not-about-hum-hum-keywords-filenames.txt'
        # files the code below will create -- can use provided filenames below or your own
        if reproduce == True:
            docterms_c1 = 'input/hum-not-hum/hum-1500sample-doc-terms-reproduce.txt'
            docterms_c2 = 'input/hum-not-hum/not-hum-1500sample-doc-terms-reproduce.txt'
        if reproduce == False:
            docterms_c1 = 'input/hum-not-hum/hum-1500sample-doc-terms-new.txt'
            docterms_c2 = 'input/hum-not-hum/not-hum-1500sample-doc-terms-new.txt'
    return collection, filenames_c1, filenames_c2, docterms_c1, docterms_c2

def set_df_filenames(comparison, threshold):
    '''Sets names of dataframes that will be saved to disk based on comparison type and minimum threshold.'''
    if comparison == 'hum-sci':
        c1_relative_csv = 'input/hum-sci/hum-500sample-min' + str(threshold) + '-df-relative.csv'
        c2_relative_csv = 'input/hum-sci/sci-500sample-min' + str(threshold) + '-df-relative.csv'
        c1_raw_csv = 'input/hum-sci/hum-500sample-min' + str(threshold) + '-df-raw.csv'
        c2_raw_csv = 'input/hum-sci/sci-500sample-min' + str(threshold) + '-df-raw.csv'
        vocablist = 'input/hum-sci/hum-sci-500sample-min' + str(threshold) + '-vocablist.txt'
    elif comparison == 'not-hum-not-sci':
        c1_relative_csv = 'input/not-hum-not-sci/not-hum-1500sample-min' + str(threshold) + '-df-relative.csv'
        c2_relative_csv = 'input/not-hum-not-sci/not-sci-1500sample-min' + str(threshold) + '-df-relative.csv'
        c1_raw_csv = 'input/not-hum-not-sci/not-hum-1500sample-min' + str(threshold) + '-df-raw.csv'
        c2_raw_csv = 'input/not-hum-not-sci/not-sci-1500sample-min' + str(threshold) + '-df-raw.csv'
        vocablist = 'input/not-hum-not-sci/not-hum-not-sci-1500sample-min' + str(threshold) + '-vocablist.txt'
    elif comparison == 'hum-not-hum':
        c1_relative_csv = 'input/hum-not-hum/hum-1500sample-min' + str(threshold) + '-df-relative.csv'
        c2_relative_csv = 'input/hum-not-hum/not-hum-1500sample-min' + str(threshold) + '-df-relative.csv'
        c1_raw_csv = 'input/hum-not-hum/hum-1500sample-min' + str(threshold) + '-df-raw.csv'
        c2_raw_csv = 'input/hum-not-hum/not-hum-1500sample-min' + str(threshold) + '-df-raw.csv'
        vocablist = 'input/hum-not-hum/hum-not-hum-1500sample-min' + str(threshold) + '-vocablist.txt'
    return c1_relative_csv, c2_relative_csv, c1_raw_csv, c2_raw_csv, vocablist

def set_df_filenames_existing(comparison):
    '''Uses `comparison` variable value to assign appropriate filenames for test.'''
    if comparison == 'hum-sci':
        c1_relative_csv = 'input/hum-sci/hum-500sample-min5-df-relative.csv'
        c2_relative_csv = 'input/hum-sci/sci-500sample-min5-df-relative.csv'
        c1_raw_csv = 'input/hum-sci/hum-500sample-min5-df-raw.csv'
        c2_raw_csv = 'input/hum-sci/sci-500sample-min5-df-raw.csv'
        vocablist = 'input/hum-sci/hum-sci-500sample-min5-vocablist.txt'
    elif comparison == 'not-hum-not-sci':
        c1_relative_csv = 'input/not-hum-not-sci/not-hum-1500sample-min5-df-relative.csv'
        c2_relative_csv = 'input/not-hum-not-sci/not-sci-1500sample-min5-df-relative.csv'
        c1_raw_csv = 'input/not-hum-not-sci/not-hum-1500sample-min5-df-raw.csv'
        c2_raw_csv = 'input/not-hum-not-sci/not-sci-1500sample-min5-df-raw.csv'
        vocablist = 'input/not-hum-not-sci/not-hum-not-sci-1500sample-min5-vocablist.txt'
    elif comparison == 'hum-not-hum':
        c1_relative_csv = 'input/hum-not-hum/hum-1500sample-min5-df-relative.csv'
        c2_relative_csv = 'input/hum-not-hum/not-hum-1500sample-min5-df-relative.csv'
        c1_raw_csv = 'input/hum-not-hum/hum-1500sample-min5-df-raw.csv'
        c2_raw_csv = 'input/hum-not-hum/not-hum-1500sample-min5-df-raw.csv'
        vocablist = 'input/hum-not-hum/hum-not-hum-1500sample-min5-vocablist.txt'
    return c1_relative_csv, c2_relative_csv, c1_raw_csv, c2_raw_csv, vocablist

def get_bags(filenames_c1, filenames_c2, collection, docterms_c1, docterms_c2):
    '''Uses lists of filenames for each category, checks these filenames against those in the provided doc-terms file, and grabs the bags where the filenames match. Produces 2 new doc-terms files including document filenames and bags of words.'''
    # define variables
    f1_list = []
    f2_list = []
    # open provided lists of filenames and add to python lists
    with open(filenames_c1) as f1, open(filenames_c2) as f2:
        for row in f1:
            row = row.strip()
            f1_list.append(row)
        for row in f2:
            row = row.strip()
            f2_list.append(row)
    # create new files to hold bags of words for each selected document in each category
    with open(docterms_c1, 'w') as f3, open(docterms_c2, 'w') as f4:
        # open up file with all bags of words for the collection ("collection" file)
        # if a filename in this file matches one in either of the 2 lists of filenames,
        # grab the bag of words for that filename to print to new doc-terms files
        with open(collection) as f5:
            for row in f5:
                row2 = row.strip()
                row2 = row2.split(' ')
                filename = row2[0]
                for x in f1_list:
                    if x == filename:
                        f3.write(row)
                for y in f2_list:
                    if y == filename:
                        f4.write(row)
            
            if filename in f2_list:
                f4.write(row)

def get_random_sample(selection, filenames_c1, filenames_c2, collection, docterms_c1, docterms_c2):
    '''Uses lists of filenames for each category, randomly selects x number of documents from each, checks these selected filenames against those in the provided doc-terms file, and grabs the bags where the filenames match. Produces 2 new doc-terms files including document filenames and bags of words.''' 
    # define variables
    f1_list = []
    f2_list = []
    # open up the 2 files containing filenames of each document in each category
    # add each filename to a list corresponding to each category
    with open(filenames_c1) as f1, open(filenames_c2) as f2:
        for row in f1:
            row = row.strip()
            f1_list.append(row)
        for row in f2:
            row = row.strip()
            f2_list.append(row)
    # take a random sample of each list based on the number provided by the user
    sample_c1 = random.sample(f1_list, selection)
    sample_c2 = random.sample(f2_list, selection)
    # create new files to hold bags of words for each selected document in each category
    with open(docterms_c1, 'w') as f3, open(docterms_c2, 'w') as f4, open(collection) as f5:
        for row in f5:
            row2 = row.strip()
            row2 = row2.split(' ')
            filename = row2[0]
            for x in sample_c1:
                if x == filename:
                    f3.write(row)
            for y in sample_c2:
                if y == filename:
                    f4.write(row)
    
def findFreq(bags):
    '''Code adapted from https://github.com/rbudac/Text-Analysis-Notebooks/blob/master/Mann-Whitney.ipynb for we1s data. Requires txt file in format of doc-terms files as input. Returns 2 dataframes: one of raw counts of every word in every doc, and one of relative frequencies of every word in every doc.'''
    # define variables
    texts = []
    docs_relative = {}
    docs_freqs = {}
    num_words = 0
    counts = defaultdict(int)    
    num_words = 0
    with open(bags) as f:
        # grab filename and bag of words for every document in txt file.
        for row in f:
            row = row.strip()
            row = row.split(' ')
            filename = row[0]
            x = len(row)
            words = row[2:x]
            # add each word in each doc to a dict of dicts and count raw frequencies
            for word in words:
                counts[word] += 1
            num_words += len(words)
            # create dicts for relative frequencies and for raw frequencies of each word in each doc
            relativefreqs = {}
            freqs = {}
            # add words and frequencies to dictionaries
            for word, rawCount in counts.items():
                relativefreqs[word] = rawCount / float(num_words)
                freqs[word] = rawCount
                # reset counts to use for the next doc
                counts[word] = 0
            # add relative and raw freqs for each doc to overall dictionary for all docs, filenames are keys
            docs_relative[filename] = relativefreqs
            docs_freqs[filename] = freqs
    # convert dicts to pandas dataframes and return dataframes.
    # the dataframes we are creating here are sparse matrices of EVERY word in EVERY doc in the input file.
    # as a result, they can get huge very quickly.
    # loading anything over ~4000 documents and handling via pandas can cause memory problems bc of the large 
    # vocabulary size. this code is therefore not extensible to large datasets.
    # this is why this notebook encourages users to work with small samples of their data. 
    # for large datasets, we recommend rewriting our code to take advantage of the parquet file format 
    # (for more on pandas integration with parquet, see https://pandas.pydata.org/pandas-docs/version/0.21/io.html#io-parquet)
    # or using numpy arrays. Sorry we didn't do this ourselves.
    df_relative = pd.DataFrame(docs_relative)
    df_freqs = pd.DataFrame(docs_freqs)
    return df_relative, df_freqs

def edit_freq_dataframes(df1_relative, df1_freqs, df2_relative, df2_freqs):
    '''Manipulates dataframes returned by findFreq function above in basic ways. Also returns average number of times any word occurs in each dataset. Could be added to findFreqs function but separated out bc of memory use issues.'''
    # fill na values with 0's
    # freqs = x
    df1_freqs = df1_freqs.fillna(0)
    df1_relative = df1_relative.fillna(0)
    df2_freqs = df2_freqs.fillna(0)
    df2_relative = df2_relative.fillna(0)
    # add total_count columns that count of # of times each word occurs across all docs in each dataset
    df1_freqs['total_count'] = df1_freqs.sum(axis=1)
    df2_freqs['total_count'] = df2_freqs.sum(axis=1)
    # sort dataframes in descending order by total_count column
    df1_freqs = df1_freqs.sort_values(by=['total_count'], ascending = False)
    df2_freqs = df2_freqs.sort_values(by=['total_count'], ascending = False)
    # obtaining average total word counts for each dataset
    counts_c1 = list(df1_freqs['total_count'])
    average_c1 = statistics.mean(counts_c1)
    counts_c2 = list(df2_freqs['total_count'])
    average_c2 = statistics.mean(counts_c2)
    print('Average total word count for dataset 1: ' + str(average_c1) + '\n' + 'Average total word count for dataset 2: ' + 
          str(average_c2))
    return df1_relative, df1_freqs, df2_relative, df2_freqs

def match_dataframes_and_save(threshold, df1_freqs, df1_relative, df2_freqs, df2_relative, c1_csv, c2_csv, c1_restrict_csv, c2_restrict_csv):
    '''Uses raw and relative frequency dataframes obtained via edit_freq_dataframes function to 2 create new dataframes of relative frequency data including only those words that occur at least x number of times (where x = threshold). Saves these dataframes to csv files so code doesn't have to be re-run, and also returns them as df1 and df2. Does the same for dataframes of raw counts data. Also returns lists of words in each dataset for use in the get_vocablist function below. Again, this function will produce 2 dataframes of relative (not raw) frequency data that are limited to words that occur at least x number of times. We need the relative frequency dataframes for performing the actual Wilcoxon test, so this is why we do this matching.'''
    # if no threshold is set by user, just rename some variables so it all turns out right in the end
    if threshold == False:
        df1_restrict = df1_freqs
        df2_restrict = df2_freqs
    # otherwise, only grab documents from df1_freqs and df2_freqs dataframes that meet or exceed threshold
    else:
        df1_restrict = df1_freqs[df1_freqs.total_count >= threshold]
        df2_restrict = df2_freqs[df2_freqs.total_count >= threshold]
    # create lists of words in each new dataframe to use in matching
    words_c1 = list(df1_restrict.index)
    words_c2 = list(df2_restrict.index)
    # then create new dataframe consisting of relative frequencies only for words that are included in each list
    df1 = df1_relative[df1_relative.index.isin(words_c1)]
    df2 = df2_relative[df2_relative.index.isin(words_c2)]
    print('Words in dataset 1: ' + str(len(df1)))
    print('Words in dataset 2: ' + str(len(df2)))
    # create csv files
    df1.to_csv(c1_csv)
    df2.to_csv(c2_csv)
    df1_restrict.to_csv(c1_restrict_csv)
    df2_restrict.to_csv(c2_restrict_csv)
    return df1, df2, words_c1, words_c2

def get_vocablist(df1, df2, words_c1, words_c2, vocablist):
    '''Creates a list of all of the unique words across both datasets. Saves to disk as a plain-text file where each word is its 
    own row.'''
    # create vocab list
    words_c1 = list(df1.index)
    words_c2 = list(df2.index)
    words_total = words_c1 + words_c2
    words = set(words_total)
    with open(vocablist, 'w') as fout:
        for word in words:
            fout.write(word + '\n')

def wrs_test(c1_csv, c1_restrict_csv, c2_csv, c2_restrict_csv, vocablist, results_csv):
    '''Requires csv files of 2 datasets for comparison (created in section 2 of compare_word_frequencies notebook), dataframes of raw counts of these datasets (also created in section 2 of the notebook), a list of the unique words across both datasets, and the name of a csv file to save the output to. Performs a Wilcoxon rank sums test on 2 datasets of relative word frequencies. Outputs a csv that lists the raw count of each word in each dataset, the difference between those counts, the percentage change in counts from dataset 1 to dataset 2, and the Wilcoxon statistic and p-value for each comparison. Code adapted from https://github.com/rbudac/Text-Analysis-Notebooks/blob/master/Mann-Whitney.ipynb and modified for we1s data. Also inspired by Andrew Piper's code from chapter 4 of Enumerations. See https://github.com/piperandrew/enumerations/blob/master/04_Fictionality/chap4_Fictionality.R.'''
    # define needed variables
    missingInCorpus1 = []
    missingInCorpus2 = []
    # read in csvs
    df1 = pd.read_csv(c1_csv, index_col=0) 
    df1 = df1.fillna(0) # replace NaNs with zeroes if not already done.
    df1_restrict = pd.read_csv(c1_restrict_csv, index_col=0)
    df1_restrict = df1_restrict.fillna(0)
    df2 = pd.read_csv(c2_csv, index_col=0) 
    df2 = df2.fillna(0) # replace NaNs with zeroes if not already done.
    df2_restrict = pd.read_csv(c2_restrict_csv, index_col=0)
    df2_restrict = df2_restrict.fillna(0)
    #Make "dummy" rows of all zeroes for any words that only appear in one corpus and not the other
    for i in range(0, df1.shape[1]):
        missingInCorpus1.append(0) 
    for i in range(0, df2.shape[1]):
        missingInCorpus2.append(0)
    # perform the test and create the output csv file
    with open(results_csv, 'w', newline='', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['word', 'c1 total count', 'c2 total count', 'difference c1 - c2', '% change', 'wilcoxon statistic', 'wilcoxon p-value'])
        # open vocablist
        with open(vocablist, 'r', encoding="utf-8") as f:
            for word in f:
                word = word.strip()
                # check if the word is in df1. if it is, grab the relative freq.
                # grab total count for word in corresponding df1_restrict dataframe.
                # if not, set counts to 0.
                if (word in df1.index):
                    countsInCorpus1 = df1.loc[word].values
                    c1_count = df1_restrict.loc[word, 'total_count']
                else:
                    countsInCorpus1 = missingInCorpus1
                    c1_count = 0
                # repeat, checking df2 and df2_restrict
                if (word in df2.index):
                    countsInCorpus2 = df2.loc[word].values
                    c2_count = df2_restrict.loc[word, 'total_count']
                else:
                    countsInCorpus2 = missingInCorpus2
                    c2_count = 0
                # now do wilcoxon test by comparing rel freqs of word in c1 to rel freqs of word in c2
                # grab metrics we want to save to results_csv
                try:
                    wrs = ranksums(countsInCorpus1, countsInCorpus2)
                    wrsStat = wrs.statistic
                    wrsP = wrs.pvalue  
                    diff = c1_count - c2_count
                    if c2_count == 0:
                        change = 'NaN'
                    else:
                        change = (diff/c2_count) * 100
                except ValueError: # Was having problems with this earlier, so this is mainly for debugging reasons
                    wrsStat = -1
                    wrsP = -1
                writer.writerow([word, c1_count, c2_count, diff, change, wrsStat, wrsP])

