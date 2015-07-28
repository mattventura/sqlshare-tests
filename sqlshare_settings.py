#!/usr/bin/python

# Settings for sqlshare tests located here
# Most config can be handled here

import os

# Prelim config (completes basic test_config and to_upload settings)
csv_file_path = os.getcwd() + '/csv/d3.csv'
existing_dataset_name = "Test Dataset"
to_delete_dataset_name = "Dataset to Delete"
username = "mstone12" # uw login

# Specify which data is to be used by sql tests
test_config = {
    # Datasets
    'existing_dataset'    : existing_dataset_name,
    'to_delete_dataset'   : to_delete_dataset_name,

    # File upload
    'upload_filename'     : csv_file_path,
    'upload_dataset_name' : "File Upload Test Dataset",
    'upload_dataset_desc' : "File uploaded by automation tests",
    'upload_dataset_public' : True,

    # Query
    'working_query' : "SELECT * FROM [" + username + "].[" + existing_dataset_name.upper()  + "]",
    'alt_query'     : "SELECT a FROM [" + username + "].[" + to_delete_dataset_name.upper() + "]",

    # Emails (for share test)
    'emails' : [username + '@u.washington.edu'],
}

# Specify datasets that should be uploaded before running tests
to_upload = [
    {
        'filename' : csv_file_path,
        'dataset_name' : test_config['to_delete_dataset'],
        'dataset_desc' : "This dataset should be deleted by automation tests",
        'dataset_public' : False,
    },

    {
        'filename' : csv_file_path,
        'dataset_name' : test_config['existing_dataset'],
        'dataset_desc' : "Dataset uploaded for automation tests.",
        'dataset_public' : True,
    },
]

# Specify which tests to run
to_run = [
    # View Tests
    'view_your_datasets',
    'view_all_datasets',
    'view_shared_datasets',
    'view_recent_datasets',
    'view_recent_queries',
    
    # Functional Tests
    'dataset_upload',
    'save_new_query',
    'download_new_query',
    'keyword_search',
    
    # Dataset Tests
    'dataset_details',
    'dataset_toggle_privacy',
    'dataset_share',
    'dataset_delete',
    'dataset_download',
    'dataset_snapshot',
    'dataset_new_dataset',
    'dataset_derive',
    'dataset_run',
    'dataset_update',
]

# Various test settings
settings = {
    'url'        : 'https://sqlshare-test.s.uw.edu',
    'date_format': "%a, %d %b %Y %H:%M:%S %Z",
    'login_type' : 'uw',
    #'username'  :
    #'password'  :

    'browser'  : 'Firefox',   # Could be Chrome, Firefox, PhantomJS, etc...
    'headless' : False,        # Should be true for concurrency
    'visible'  : True,        # If headless, use Xephyr
    
    'concurrent_tests' : False, # Set to false for non-concurrency
    
    'driver_timeout' : 1,
    
    'debug' : False,
    
}

# For debug purposes
#to_run = ['download_new_query', 'dataset_update']
#to_upload = [to_upload[1]]
