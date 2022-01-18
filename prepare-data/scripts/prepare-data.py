"""prepare-data.py

Uses `bag_of_words` field in publicly released json documents to generate the text file needed to reproduce analysis performed in the article. The text file generated is a line-delimited string of rows,
one per document in the collection. Each row is a space-separated, alphabetized list of terms with each term repeated once for the number of times it occurs in the document.

Sample usage:
prepare_data(json_dir, import_file_path, strip_digits, stoplist_file, log_file, filelist_file=None)

For use with prepare-data.ipynb v 2.1.
"""

import json
import os
import re
import shutil
import csv
import string
import unidecode
from zipfile import ZipFile
from IPython.display import display, HTML

def extract_data(json_zip, data_dir):
    """Unpack json.zip and its subdirectories."""
    os.makedirs(json_dir_new)
    shutil.unpack_archive(json_zip, extract_dir=json_dir_new)
    for item in os.listdir(json_dir_new):
        item_path = json_dir_new + '/' + item
        subdir_path = json_dir_new + '/' + item.replace('.zip', '')
        if not os.path.exists(subdir_path):
            os.makedirs(subdir_path)
        shutil.unpack_archive(item_path, extract_dir=subdir_path)
        os.remove(item_path)
    display(HTML('<h4>Done!</h4>'))
    
def prepare_data(json_dir, import_file_path, strip_digits, stoplist_file, log_file, filelist_file):
    """Prepare a file or directory for import."""
    log = []
    stoplist, log = load_stoplist(stoplist_file, log)
    if os.path.exists(import_file_path):
        os.remove(import_file_path)
    if filelist_file is not None:
        filelist = []
        with open(filelist_file) as fin:
            for file in fin:
                file = file.strip()
                filelist.append(file)      
        files_all = []
        for item in os.listdir(json_dir):
            item_path = json_dir + '/' + item
            for file in os.listdir(item_path):
                file_path = item_path + '/' + file
                files_all.append(file_path)
        files = sorted(f for f in files_all if os.path.basename(f) in filelist and f.endswith('.json'))
        filenames = [os.path.basename(f) for f in files]
        missing = [x for x in filelist if x not in filenames]
        if len(missing) > 0:
            for x in missing:
                log.append(x + ',Could not find file in json directory.\n')
                display(HTML('<p style="color: red;">Error! Could not find file in json directory. See log file for more details.</p>'))
    else:
        files = []
        for item in os.listdir(json_dir):
            item_path = json_dir + '/' + item
            for file in os.listdir(item_path):
                file_path = item_path + '/' + file
                files.append(file_path)
    for i, file in enumerate(files):
        doc, log = read_manifest(file, log)
        log = prepare_data_file(doc, file, i, strip_digits, stoplist, import_file_path, log)
    if len(log) > 0:
        print(str(len(log)) + ' total errors. See log file for more details.')
        log = ''.join(log)
        with open(log_file, 'w') as f:
            f.write(log)
    display(HTML('<h4>Done!</h4>'))
    
def load_stoplist(stoplist_file, log):
    """Load the stoplist.

    Parameters:
    - stoplist_file (str): The path to the stoplist file.
    """
    if stoplist_file is not None:
        try:
            with open(stoplist_file, 'r', encoding='utf-8') as f:
                stoplist = f.read().split('\n')
        except IOError:
            log.append(stoplist_file + ',Could not read stoplist file.\n')
            display(HTML('<p style="color: red;">Error! Could not read stoplist file. See log file for more details.</p>'))
    else:
        stoplist = []
    return stoplist, log
    
def read_manifest(filepath, log):
    """Read the manifest file."""
    try:
        with open(filepath, 'rb') as f:
            doc = json.loads(f.read())
    except (FileNotFoundError, ValueError):
        log.append(filepath + ',Could not read file.\n')
        display(HTML('<p style="color: red;">Error! Could not read file. See log file for more details.</p>'))
        doc = None
    return doc, log

def prepare_data_file(doc, filepath, index, strip_digits, stoplist, import_file_path, log):
    """Prepare a single file for import."""
    filename = os.path.basename(filepath)
    if doc is not None:
        bag = doc['bag_of_words']
    else:
        bag = None
    # Create a row and save it to the import file
    bow_row, log = get_bow_row(filename, index, bag, strip_digits, stoplist, log)
    log = save(bow_row, import_file_path, log)
    return log

def get_bow_row(filename, index, bag, strip_digits, stoplist, log):
    """Convert a dictionary bag of words to a sequence of terms based on term counts.

    Parameters:
    - filename (str): The name of the file to head the row.
    - index (int): The index to be attached to the file row.
    - bag (dict): A bag of words dict of the format `{word: count}`.
    """
    row = filename + ' ' + str(index) + ' '
    if bag is not None:
        try:
            for k, v in bag.items():
                # Another check on stray punctuation
                if not k.isalnum():
                    pass
                # Do not include digits
                elif strip_digits and k.isdigit():
                    pass
                # Otherwise, handle stop words and add the row
                else:
                    # hack to handle 'May' error in collection 33 data
                    # this is necessary because of an error in the code we used to process collection 33 
                    # data originally. the code did not properly handle the month of May.
                    # the below hack is necessary in order to reproduce our analysis.
                    if k == 'May':
                        term = k.replace(' ', '_') + ' '
                        terms = (term * v)
                        row += terms
                    elif k.lower() not in stoplist:
                        term = k.replace(' ', '_') + ' '
                        term = re.sub('the_|a_|an_', '', term)
                        terms = (term * v)
                        row += terms
                    else:
                        pass
                    bow_row = row.strip()
        except (RuntimeError, TypeError):
            log.append(filename + ',Could not generate row from bag of words.\n')
            display(HTML('<p style="color: red;">Error! Could not generate row from bag of words. See log file for more details.</p>'))
    else:
        bow_row = None
    return bow_row, log

def save(bow_row, import_file_path, log):
    """Append the row to the import file."""
    if bow_row is not None:
        try:
            with open(import_file_path, 'a', encoding='utf-8') as f:
                f.write(bow_row.strip() + '\n')
        except IOError:
            log.append(import_file_path + ',Could not append row to import file.\n')
            display(HTML('<p style="color: red;">Error! Could not append row to import file. See log file for more details.</p>'))
    else:
        pass
    return log

def year_from_fpath(file):
    """Return the publication year of a document.

    Given a json filename (in WE1S format), return the publication year
    of the document using the document filename. For use when Lexis Nexis
    does not provide publication date information. Function depends on
    WE1S file format. Stamps files with obviously incorrect publication
    year of 1900 if all else fails.
    """
    # If the filename begins with a digit, grab the relevant publication year.
    # Otherwise, assign it a dummy date.
    year = ''
    if re.match(r'^\d', file):
        try:
            match = re.search(r'_(\d\d\d\d)-\d\d-\d\d', file)
            year = match.group(1)
        except AttributeError:
            year = '1900'
    # If the filename begins with `we1schomp` or `chomp`, grab the pub year.
    # Otherwise, assign it a dummy date.
    if re.match('^we1schomp_', file) or re.match('^chomp_', file):
        try:
            match = re.search(r'_(\d\d\d\d)\d\d\d\d_', file)
            year = match.group(1)
        except AttributeError:
            year = '1900'
    if year == '':
        year = '1900'
    return year

def dfrb_metadata(metadata_dir, metadata_csv_file, browser_meta_file_temp,
                  browser_meta_file, json_dir, filelist_file):
    """Produce dfr-browser metadata csvs.

    Takes a list of files and a directory of json files as input. Produces three different versions
    of dfr-browser metadata csvs including metadata only for files included on list. This function  will 
    delete existing metadata folder (`project_data/metadata`) if it exists and create a new metadata
    folder. Otherwise, it will just create a metadata folder in `project_data`.
    If you do not want to delete your metadata directory every time you run
    this code and your metadata folder already exists, comment out lines 76-80. If you don't want to use
    a list of files, set `filelist` to None.
    """
    # MAP FIELDS FROM JSON TO DFRB METADATA
    # id, publication, pubdate, title, articlebody, author, docUrl, wordcount
    # idx       ->  id
    # title     ->  title
    #           ->  author
    # pub       ->  publication
    #           ->  docUrl
    # length    ->  wordcount
    # pub_date  ->  pubdate
    # content   ->  articlebody
    existing = os.path.exists(metadata_dir)
    if existing == True:
        shutil.rmtree(metadata_dir)
        os.makedirs(metadata_dir)
    else:
        os.makedirs(metadata_dir)
    csv.field_size_limit(100000000)
    # Original column order
    # 'id', 'publication', 'pubdate', 'title', 'articlebody', 'pagerange', 'author', 'docUrl', 'wordcount'
    # New column order
    # 'id', 'title', 'author', 'publication', 'docUrl', 'wordcount', 'pubdate', 'pagerange'
    with open(metadata_csv_file, 'w') as csvfile:
        row = ['id'] + ['title'] + ['author'] + ['journaltitle'] + ['volume'] + ['issue'] + ['pubdate'] + ['pagerange']
        csvwriter = csv.writer(csvfile, delimiter=',')
        csvwriter.writerow(row)
        if filelist_file == None:
            files = []
            for item in os.listdir(json_dir):
                item_path = json_dir + '/' + item
                for file in os.listdir(item_path):
                    file_path = item_path + '/' + file
                    files.append(file_path)
            sorted_json = sorted(files)
        else:
            files = []
            with open(filelist_file) as fin:
                for row in fin:
                    filename = row.strip('\n')
                    files.append(filename)
            files_all = []
            for item in os.listdir(json_dir):
                item_path = json_dir + '/' + item
                for file in os.listdir(item_path):
                    file_path = item_path + '/' + file
                    files_all.append(file_path)
            sorted_json = sorted(f for f in files_all if os.path.basename(f) in files and f.endswith('.json'))
        idx=0
        for filename in sorted_json:
            # log: preview the first and last files only to prevent log overflow
            if(idx < 5 or idx > len(sorted_json) - 5):
                print(idx, ':', filename, '\n')
            if(idx == 5 and len(sorted_json) > 10):
                print('...\n')
            with open(os.path.join(json_dir, filename)) as f:
                oe = False
                try:
                    j = json.loads(f.read())
                except:
                    oe = True
                    print(filename + ' could not be loaded.')
                if not 'pagerange' in j:
                    j['pagerange'] = 'no-pg'
                if not 'author' in j:
                    j['author'] = 'unknown'
                if not 'volume'in j:
                    j['volume'] = 'no-vol'
                if not 'issue' in j:
                    j['issue'] = 'no-issue'
                if not 'pub_date' in j:
                    try:
                        j['pub_date'] = j['pub_year'] + '-01-01'
                    except KeyError:
                        year = year_from_fpath(filename)
                        j['pub_date'] = year + '-01-01'
                if j['pub_date'] == '':
                    try:
                        j['pub_date'] = j['pub_year'] + '-01-01'
                    except KeyError:
                        year = year_from_fpath(filename)
                        j['pub_date'] = year + '-01-01'
                if not 'length' in j:
                    try:
                        # j['length'] = len(j['bag_of_words'].split())
                        j['length'] = len(j['bag_of_words'])
                    except KeyError:
                        try:
                            tokens = [feature[0] for feature in j['features'][1:]]
                            j['length'] = len(tokens)
                        except KeyError:
                            j['length'] = len(j['content'].split())
                # write article metadata to csv
                if oe == True:
                    testrow = [filename] + [j['title']] + [j['author']] + [j['pub']] + [j['volume']] + [j['issue']] +[j['pub_date']] + [j['length']]
                    print(testrow)
                csvwriter.writerow([filename] + [j['title']] + [j['author']] + [j['pub']] + [j['volume']] +
                                   [j['issue']] + [j['pub_date']] + [j['length']])
                oe = False
            idx = idx + 1
    # Spreadsheet manipulation and meddling to make it work with dfr-browser
    with open(metadata_csv_file, 'r') as csv_in:
        csvreader = csv.reader(csv_in, delimiter=',')
        next(csvreader)  # skip header row
        with open(browser_meta_file_temp, 'w') as csv_out:
            # enforce quoted fields
            csvwriter = csv.writer(csv_out, delimiter=',', quoting=csv.QUOTE_ALL)
            for row in csvreader:
                csvwriter.writerow(row)
    with open(browser_meta_file_temp, 'r') as fin:
        with open(browser_meta_file, 'w') as fout:
            for line in fin:
                fout.write(line.replace(',"",', ',NA,'))


