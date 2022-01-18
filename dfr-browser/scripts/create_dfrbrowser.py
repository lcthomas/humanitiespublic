"""create_dfrbrowser.py.

Creates files necessary to produce a dfr-browser visualization for exploring topic models. Dfr-browser code, stored in this module in `dfrb_scripts`, was written by Andrew Goldstone and adapted for our use and data. See https://github.com/agoldst/dfr-browser for Goldstone's original code and documentation. Also see https://agoldst.github.io/dfr-browser/ for a version history of Goldstone's code. We use an older version of Goldstone's code (v0.5.1), and we use his prepare_data.py Python script to prepare the data files, NOT the R package. This script includes functions for preparing WE1S data for use with Goldstone's code and for creating dfr-browser visualizations.

For use with create_dfrbrowser.ipynb v 2.0.

"""

# Python imports
import csv
import os
import string
import unidecode
import json
import re
from pathlib import Path
import subprocess
from subprocess import STDOUT
import shutil
from IPython.display import display, HTML
from zipfile import ZipFile

def check_metadata(metadata_dir):
    '''Checks to make sure the metadata files you need already exist.'''
    if os.path.exists(metadata_dir):
        files = [file for file in os.listdir(metadata_dir)]
        if 'meta.csv' in files and 'meta.temp.csv' in files and 'metadata-dfrb.csv':
            output = 'Metadata files for selected collection exist. Ready to create browser.' 
            display(HTML('<p><strong>' + output + '</strong></p>'))
        else:
            output = 'You are missing at least one metadata file for this collection. Check metadata directory and module README.md.' 
            display(HTML('<p style="color: red;">' + output + '</p>'))
    else:
        output = 'Metadata directory does not exist for this collection. Use prepare-data module to create it. See module README.md.' 
        display(HTML('<p style="color: red;">' + output + '</p>'))

def get_model_state(collection, selection, model_dir):
    """Get model state.

    This function assumes your project folder is set up according to WE1S
    format (and was therefore created using our `new_project_from_archive`
    notebook). It looks for the models you have selected to create
    dfr-browsers for in your project's models directory and then grabs those
    models' state and scaled files, or, if it fails to find them, it alerts
    you to their absence. To produce dfr-browsers for all of your project's
    models, the selection variable should be set to 'None'. To run the
    create_dfrbrowser() you need lists of the names of the model subdirectories
    you want to create (in subdir_list), the state files from each of those
    models (in state_file_list), and the scaled files from each of those
    models (in scaled_file_list). You may set these values manually in the
    notebook.
    """
    # Define variables
    subdir_list = []
    state_file_list = []
    scaled_file_list = []
    # Set `selection` to `All` or `None` if you want to make dfr-browsers for ALL existing models
    if get_selection(selection) is None:
        # For each model subdirectory, add the model state file and model scaled file to a list
        for subdir in os.listdir(model_dir):
            if subdir == collection:
                subdir_path1 = model_dir + '/' + subdir
                for x in os.listdir(subdir_path1):
                    subdir_path = model_dir + '/' + subdir + '/' + x
                    subdir_list.append(x)
                    num = re.search(r'\d+', x).group()
                    for file in os.listdir(subdir_path):
                        if file.endswith('.gz') and num in file:
                            state_file = subdir_path + '/' + file
                            state_file_list.append(state_file)
                        if file.endswith('.csv'):
                            scaled_file = subdir_path + '/' + file
                            scaled_file_list.append(scaled_file)
        # User feedback in the notebook
        msg = '<p><strong>Will create visualizations for all models in <code>models</code> directory: ' + str(subdir_list) +'</strrong></p>'
        display(HTML(msg))
        lsub = len(subdir_list)
        lstate = len(state_file_list)
        lscaled = len(scaled_file_list)
        # Display how many state and scaled files were discovered for how many models
        msg = '<p><strong>Found ' + str(lstate) + ' state files and ' + str(lscaled) + ' scaled files for ' + str(lsub) + ' models</strong></p>'
        display(HTML(msg))
        # If they all match, you are golden
        if lsub == lstate == lscaled:
            display(HTML('<p><strong>Ready to create visualizations</strong></p>'))
        # If they don't all match, you need to check your `models` directory
        # to make sure each one contains a state and a scaled file.
        else:
            msg = '<p style="color: red;">Incorrect number of state or scaled files! Check your <code>model</code> directory</p>'
            display(HTML(msg))
    # If selection is not `None`, process selected models
    else:
        subdir_list = selection
        # For each selected model, add the model state and scaled files to a list
        for subdir in subdir_list:
            subdir_path = model_dir + '/' + collection + '/' + subdir
            num = re.search(r'\d+', subdir).group()
            for file in os.listdir(model_path):
                if file.endswith('.gz') and num in file:
                    state_file = subdir_path + '/' + file
                    state_file_list.append(state_file)
                if file.endswith('.csv'):
                    scaled_file = subdir_path + '/' + file
                    scaled_file_list.append(scaled_file)
        # User feedback in the notebook
        msg = '<p><strong>Will create visualizations for the following models: ' + str(subdir_list) +'</strong></p>'
        display(HTML(msg))
        lsub = len(subdir_list)
        lstate = len(state_file_list)
        lscaled = len(scaled_file_list)
        # Display how many state and scaled files were discovered for how many models
        msg = '<p><strong>Found ' + str(lstate) + ' state files and ' + str(lscaled) + ' scaled files for ' + str(lsub) + 'models</strong></p>'
        display(HTML(msg))
        # If they all match, you are golden
        if lsub == lstate == lscaled:
            display(HTML('<p><strong>Ready to create visualizations</strong></p>'))
        # If they don't all match, you need to check your `models` directory to
        # make sure each one contains a state and a scaled file.
        else:
            msg = '<p style="color: red;">Incorrect number of state or scaled files! Check your <code>model</code> directory</p>'
            display(HTML(msg))
    return subdir_list, state_file_list, scaled_file_list

def create_dfrbrowser(collection, subdir_list, state_file_list, scaled_file_list,
                      browser_meta_file, current_dir):
    """Create a dfr-browser visualization.

    This notebook creates dfr-browser visualizations for all models selected
    via the `get_models()` function above. It is configured to work with
    multiple models at once organized in the WE1S default format. After
    moving a lot of data around to various appropriate subfolders, it uses
    Andrew Goldstone's prepare_data.py script to create the necessary files
    for a dfr-browser visualization (NOTE: WE1S does not use Goldstone's
    dfrbrowser R package, because we wanted to keep everything in Python).
    We've also included some small tweaks of the language in some dfr-browser
    files so that they accord with WE1S json data (and not JSTOR data).
    """
    # Take the lists of model subdirectories, state files, and scaled files
    # created via the get_models() function and iterate through each to
    # create the appropriate subdirectories for the dfrbrowser visualizations
    # within the dfr_browser module.
    for subdir, state, scaled in zip(subdir_list, state_file_list, scaled_file_list):
        num = re.search(r'\d+', subdir).group()
        browse_path = current_dir + '/' + collection + '/topics' + num
        existing = os.path.exists(browse_path)
        if existing == True:
            shutil.rmtree(browse_path)
            os.makedirs(browse_path)
        else:
            os.makedirs(browse_path)
        # make browser subdirectory
        # sb_path = browse_path + '/topics'
        sb_path = browse_path
        existing = os.path.exists(sb_path)
        if existing == True:
            shutil.rmtree(sb_path)
        # copy dfrbrowser template from scripts to project browser folder
        dfrb_scripts = current_dir + '/dfrb_scripts'
        shutil.copytree(dfrb_scripts, sb_path)
        # move and rename customized js file
        min_js = sb_path + '/js/dfb.min.js.custom'
        min_js_new = sb_path + '/js/dfb.min.js'
        shutil.move(min_js, min_js_new)
        # make data dir
        bdata_dir = sb_path + '/data'
        os.makedirs(bdata_dir)
        # create dfr-browser files using python script
        prepare_data_script = sb_path + '/bin/prepare-data'
        tw = sb_path + '/data/tw.json'
        dt = sb_path +'/data/dt.json.zip'
        info = sb_path + '/data/info.json'
        # using check_output to preserve prepare_data.py output
        output = subprocess.check_output([prepare_data_script, 'convert-state', state, '--tw', tw, '--dt', dt],
                                         stderr=STDOUT,
                                         universal_newlines=True)
        print(output)
        output = subprocess.check_output([prepare_data_script, 'info-stub', '-o', info],
                                         stderr=STDOUT,
                                         universal_newlines=True)
        print(output)
        # copy scaled file into data dir
        shutil.copy(scaled, bdata_dir)
        # move metadata-dfrb to {sb_path}/data, zip up and rename, delete meta.csv copy
        meta_zip = bdata_dir + '/meta.csv.zip'
        existing = os.path.exists(meta_zip)
        if existing == True:
            os.remove(meta_zip)
        shutil.copy(browser_meta_file, bdata_dir)
        try:
            shutil.make_archive(os.path.join(bdata_dir, 'meta.csv'), 'zip', bdata_dir, 'meta.csv')
        except OSError as err:
            print('Error writing meta.csv.zip')
            print(err)

            
def get_selection(selection):
    """Return a valid model selection."""
    if not isinstance(selection, str) and not isinstance(selection, list):
        raise TypeError('The selection setting must be a string or a list.')
    if isinstance(selection, str):
        if selection.lower() == 'all' or selection == '':
            selection = None
        elif selection.startswith('topics'):
            selection = [selection]
    return selection
        
