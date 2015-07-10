# Settings for sqlshare tests located here
# Most config can be handled here

import os

# Specify which data is to be used by sql tests
csv_file_path = "/home/matt/Work/sqlshare_tests/csv/d3.csv"

test_config = {
    # Datasets
    'existing_dataset' : "Test Dataset",
    'to_delete_dataset'   : "Dataset to Delete",

    # File upload
    'upload_filename'     : csv_file_path,
    'upload_dataset_name' : "File Upload Test Dataset",
    'upload_dataset_desc' : "File uploaded by automation tests",
    'upload_dataset_public' : True,

    # Query
    'working_query' : "SELECT * FROM [mstone12].[TEST DATASET]",

    # Emails (for share test)
    'emails' : ['mstone12@u.washington.edu'],
}

# Specify datasets that should be uploaded before running tests
to_upload = [
    {
        'filename' : csv_file_path,
        'dataset_name' : "Dataset to Delete",
        'dataset_desc' : "This dataset should be deleted by automation tests",
        'dataset_public' : False,
    },

    {
        'filename' : csv_file_path,
        'dataset_name' : "Test Dataset",
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
]

# Various test settings
settings = {
    'browser'    : 'Chrome', # Could be Chrome, Firefox, PhantomJS, etc...
    'url'        : 'https://sqlshare-test.s.uw.edu',
    'date_format': "%a, %d %b %Y %H:%M:%S %Z",
    'login_type' : 'uw',
    #'username' :
    #'password' :
    'browser_options' : { "download.default_directory" : os.getcwd() },
    'headless' : True,
    'driver_timeout' : 1,
    'debug' : False
}


