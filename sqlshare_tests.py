# Automation Tests for SQLShare
# - Matt Stone

import os
import unittest
import getpass

from datetime import datetime


from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from selenium.webdriver.common.action_chains import ActionChains as AC


# Check for settings in file sqlshare_settings.py,
if os.path.isfile("sqlshare_settings.py"):
    from sqlshare_settings import settings
else:
    settings = {}
    

# Get Username and password from env if no settings file and from user if no env vars
username = None
password = None
if not ('username' in settings.keys()):
    try:
        username = os.environ['SQLSHARE_USERNAME']
    except KeyError:
        username = input("Username: ")

if not ('password' in settings.keys()):
    try:
        password = os.environ['SQLSHARE_PASSWORD']
    except KeyError:    
        password = getpass.getpass()

        
default_settings = {
    'browser'    : 'Chrome', # Could be Chrome, Firefox, PhantomJS, etc...
    'url'        : 'https://sqlshare-test.s.uw.edu',
    'login_type' : 'uw',
    'username'   : username,
    'password'   : password,
    'date_format': "%a, %d %b %Y %H:%M:%S %Z",
    
}

test_new_query_params = {
    'query' : "SELECT * FROM [charlon].[IM ON A BUS]",
    'new_query_action' : "save",
    'dataset_name' : "Test Dataset",
    'dataset_desc' : "Test description",
    'dataset_public': False,
}

test_file_upload_params = {
    'filename' : "/home/matt/sqlshare/csv/d3.csv",
    'dataset_name' : "Upload Test",
    'dataset_desc' : "Upload description",
    'dataset_public' : True
}
    

def get_test_class(test_params=None):
    klass = SQLShareTests()

    # Settings to be added in order (defaults, file, test params)
    to_add = [default_settings, settings, test_params]
    for attr_set in to_add:
        for attr in attr_set.keys():
            setattr(klass, attr, attr_set[attr])

    return klass



class SQLShareSite:

    # Driver methods
    def get_element(self, selector, by_method=By.CSS_SELECTOR, source=None, ignore_visibility=False):
        if source is None:
            source = self.driver
            
        element = WebDriverWait(source, 10).until(EC.presence_of_element_located((by_method, selector)))
        
        if not ignore_visibility:
            WebDriverWait(source, 10).until(EC.visibility_of(element))
            
        return element

    def get_elements(self, selector, by_method=By.CSS_SELECTOR, source=None, ignore_visibility=False):
        if source is None:
            source = self.driver
            
        elements = WebDriverWait(source, 10).until(EC.presence_of_all_elements_located((by_method, selector)))
        
        if not ignore_visibility:
            for element in elements:
                try:
                    WebDriverWait(source, 2).until(EC.visibility_of(element))
                except TimeoutException:
                    elements.remove(element)

        return elements

    # Page interaction
    def sqlshare_login(self):
        # Logs into the sqlshare login page
        buttons = self.get_elements("div.sql-wayf-login button")
        if self.login_type == 'uw':
            buttons[0].click()

            self.get_element("input#weblogin_netid").send_keys(self.username)
            self.get_element("input#weblogin_password").send_keys(self.password)
            self.get_element("ul.submit input").click()

            self.get_element("input.btn-primary").click()
            
        elif self.login_type == 'google':
            buttons[1].click()

        else:
            raise Exception("No login type specified")
    
    def click_sidebar_link(self, link_text):
        links = self.get_elements("div.sql-sidebar-actions a")
        for link in links:
            if link.text.lower().strip() == link_text.lower():
                link.click()
                return
                                        
        raise Exception('Link "' + link_text + '" not found in sidebar')

    def get_databases(self):
        database_elements = self.get_elements("div.sql-dataset-list a.sql-dataset-list-item")
        
        databases = []
        for element in database_elements:
            name = self.get_element("span.sql-dataset-name",           source=element).text
            ownr = self.get_element("span.sql-dataset-owner-modified", source=element).text
            desc = self.get_element( "div.sql-dataset-desc",           source=element).text

            index = ownr.index(' ')
            date_string = ownr[(index + 1):]
            date = datetime.strptime(date_string, self.date_format)

            databases.append({'name':name, 'ownr':ownr[:index], 'desc':desc, 'date':date})

        return databases

    def new_query(self):
        self.click_sidebar_link("New Query")

        self.get_element("div.CodeMirror").click()
        self.actions.send_keys(self.query).perform()
        self.get_element("form button#run_query").click()

        if not (hasattr(self, 'new_query_action')):
            raise Exception("New query action must be specified")

        if self.new_query_action == 'save':
            self.save_dataset()
            
        elif self.new_query_action == 'download':
            self.download_dataset()
            
        else:
            raise Exception("New query action unknown")

    def upload_dataset(self):
        self.click_sidebar_link("Upload Dataset")

        a_element = self.get_element("a#upload_dataset_browse")
        self.get_element("*", source=a_element, ignore_visibility=True).send_keys(self.filename)

        title_element = self.get_element("input#id_dataset_name")
        title_element.clear()
        title_element.send_keys(self.dataset_name)
        
        self.get_element("textarea#id_dataset_description").send_keys(self.dataset_desc)
        
        checkbox = self.get_element("div#final_settings_panel div.checkbox input")
        if (self.dataset_public and not checkbox.is_selected()) or (not self.dataset_public and checkbox.is_selected()):
            checkbox.click()

        self.get_element("button#save_button").click()


    def download_dataset(self):
        self.get_element("div.sql-dataset-actions button#download_query").click()
        # to do

    def save_dataset(self):
        self.get_element("div.sql-dataset-actions button.btn-sm").click()

        form = self.get_element("form")

        self.get_element("input#blah1",    source=form).send_keys(self.dataset_name)
        self.get_element("textarea#blah2", source=form).send_keys(self.dataset_desc)
        checkbox = self.get_element("div.checkbox input", source=form)
        if (self.dataset_public and not checkbox.is_selected()) or (not self.dataset_public and checkbox.is_selected()):
            checkbox.click()

        self.get_element("button", source=form).click()

    def get_recent_datasets(self):
        self.click_sidebar_link("Recent Datasets")
            
        return self.get_databases()

    def get_recent_queries(self):
        self.click_sidebar_link("Recent Queries")

        query_elements = self.get_elements("div.sql-query-list a.sql-query-list-item")

        queries = []
        for element in query_elements:
            code   = self.get_element("span.sql-query-code",   source=element).text.strip()
            date   = self.get_element("span.sql-query-date",   source=element).text.strip()
            status = self.get_element("span.sql-query-status", source=element).text.strip()

            _date = datetime.strptime(date, self.date_format)

            queries.append({'code':code, 'date':_date, 'status':status})

        return queries



class SQLShareTests(unittest.TestCase, SQLShareSite):
    # Tests are located in this class

    # Test auxillary methods
    def setUp(self):
        self.driver = getattr(webdriver, self.browser)()
        self.driver.get(self.url)

        self.actions = AC(self.driver)

        self.sqlshare_login()

    def tearDown(self):
        self.driver.quit()

