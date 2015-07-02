# Tests for sqlshare as listed in jira.cac.washington.edu
# - Matt Stone

from sqlshare_tests_c import SQLShareTests
from sqlshare_settings import *

import os
import unittest


class SQLShare(SQLShareTests):

    # View Tests
    def view_your_datasets(self):
        self.click_sidebar_link("Yours")
        self.get_datasets()

    def view_all_datasets(self):
        self.click_sidebar_link("All")
        self.get_datasets()

    def view_recent_datasets(self):
        self.get_recent_datasets()

    def view_recent_queries(self):
        self.get_recent_queries()


    # Functional Tests
    def dataset_upload(self):
        self.filename = self.filename
        self.dataset_name = self.upload_dataset_name
        self.dataset_desc = self.upload_dataset_desc
        self.dataset_public = self.upload_dataset_public

        self.upload_dataset()

        self.open_dataset(self.dataset_name)
        self.delete_dataset()

        self.assert_dataset_deleted(self.dataset_name)

    def save_new_query(self):
        self.query = "Working Query"
        self.new_query_action = "save"
        self.dataset_name = "New Query Dataset"
        self.dataset_desc = "New query dataset save result."
        self.dataset_public = False

        self.new_query()

        self.open_dataset("New Query Dataset")
        self.delete_dataset()

        self.assert_dataset_deleted("New Query Dataset")

    def download_new_query(self):
        self.query = self.working_query
        self.new_query_action = "download"

        self.new_query()

        
    # Dataset Tests
    def toggle_privacy(self):
        self.open_dataset(self.existing_dataset)
        self.public_private_toggle()

    def share_dataset(self):
        self.open_dataset(self.existing_dataset)
        self.share_dataset()

    def delete_dataset(self):
        self.open_dataset(self.delete_dataset)
        self.delete_dataset()

        self.click_sidebar_link("All")
        datasets =self.get_datasets()
        names = []
        for dataset in datasets:
            names.append(dataset['name'])

        assert self.delete_dataset not in names

    def download_dataset(self):
        self.open_dataset(self.existing_dataset)
        self.get_action_buttons()['DOWNLOAD'].click()

        assert os.path.isfile("query_results.csv")
        os.remove("query_results.csv")        

    def snapshot_dataset(self):
        self.dataset_name = "Snapshot Dataset"
        self.dataset_desc = "Snapshot of a dataset for automation testing."
        self.dataset_public = False
        
        self.open_dataset(self.existing_dataset)
        self.dataset_snapshot()

        self.delete_dataset("Snapshot Dataset")
        self.assert_dataset_deleted("Snapshot Dataset")

    def assert_dataset_deleted(self, dataset_name):
        self.click_sidebar_link("All")
        datasets = self.get_datasets()
        names = []
        for dataset in datasets:
            names.append(dataset['name'])

        assert dataset_name not in names

    # To Do
    # Derive, New Dataset, Run, Update
    

### Main Program

# Get Username and password from env if no settings file and from user if no env vars

username = None
password = None
if not ('username' in settings.keys()):
    try:
        settings['username'] = os.environ['SQLSHARE_USERNAME']
    except KeyError:
        settings['username'] = input("Username: ")

if not ('password' in settings.keys()):
    try:
        settings['password'] = os.environ['SQLSHARE_PASSWORD']
    except KeyError:    
        settings['password'] = getpass.getpass()


# Apply Attributes to sql class
for setting in [settings, test_config]:
    for attr in setting.keys():
        setattr(SQLShare, attr, setting[attr])

# Upload Datasets
sql = SQLShare()
sql.setUp()
for dataset in to_upload:
    for attr in dataset.keys():
        setattr(sql, attr, dataset[attr])
        sql.upload_dataset()

# Create suite and add tests
suite = unittest.TestSuite()
for test in to_run:
    suite.addTest(SQLShare(test))

# Run Tests
result = unittest.TestResult()
suite.run(result)

# Delete Uploaded Datasets
for dataset in to_upload:
    sql.delete_dataset(to_upload['name'])

    
