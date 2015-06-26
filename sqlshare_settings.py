# Settings for sqlshare tests located here
# Most config can be handled here

# Specify which data is to be used by sql tests
test_config = {
    # Datasets
    'existing_dataset' : "Test Dataset",
    'delete_dataset'   : "Dataset to Delete",

    # File upload
    'filename'     : "/home/matt/sqlshare/csv/d3.csv",
    'upload_dataset_name' : "File Upload Test Dataset",
    'upload_dataset_desc' : "File uploaded by automation tests",
    'upload_dataset_public' : True,

    # Query
    'working_query' : "SELECT * FROM [mstone12].[TEST DATASET]",
}

# Specify datasets that should be uploaded before running tests
to_upload = [
    {
        'filename' : "/home/matt/sqlshare/dsv/d3.csv",
        'dataset_name' : "Dataset to Delete",
        'dataset_desc' : "This dataset should be deleted by automation tests",
        'dataset_public' : False,
    },

    {
        'filename' : "/home/matt/sqlshare/dsv/d3.csv",
        'dataset_name' : "Test Dataset",
        'dataset_desc' : "Dataset uploaded for automation tests.",
        'dataset_public' : True,
    },
]

# Specify which tests to run
to_run = [
    'view_your_datasets',
    'view_all_datasets',
    'view_recent_datasets',
    'view_recent_queries',
    'dataset_upload',
    'save_new_query',
    'download_new_query',
    'toggle_privacy',
    'share_dataset',
    'delete_dataset',
    'download_dataset',
    'snapshot_dataset',
]

# Various test settings
settings = {
    'browser'    : 'Chrome', # Could be Chrome, Firefox, PhantomJS, etc...
    'url'        : 'https://sqlshare-test.s.uw.edu',
    'date_format': "%a, %d %b %Y %H:%M:%S %Z",
    'login_type' : 'uw',
    #'username' :
    #'password' :    
}


