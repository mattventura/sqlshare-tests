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


# Check for settings in file sqlshare_settings.py,
if os.path.isfile("sqlshare_settings.py"):
    from sqlshare_settings import settings
    

# Get Username and password from env if no settings file and from user if no env vars
username = None
password = None
if settings and not ('username' in settings.keys()):
    try:
        username = os.environ['SQLSHARE_USERNAME']
    except KeyError:
        username = input("Username: ")

if settings and not ('password' in settings.keys()):
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

def get_test_class():
    klass = SQLShareTests()

    # Set defualts first
    for attr in default_settings.keys():
        setattr(klass, attr, default_settings[attr])

    # Settings file
    if settings:
        for attr in settings.keys():
            setattr(klass, attr, settings[attr])

    return klass


class SQLShareTests(unittest.TestCase):    

    # Test auxillary methods
    def setUp(self):
        self.driver = getattr(webdriver, self.browser)()
        self.driver.get(self.url)

        self.sqlshare_login()

        
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


    def tearDown(self):
        self.driver.quit()

    # Driver methods
    def get_element(self, selector, by_method=By.CSS_SELECTOR, source=None):
        if source is None:
            source = self.driver
            
        element = WebDriverWait(source, 10).until(EC.presence_of_element_located((by_method, selector)))
        WebDriverWait(source, 10).until(EC.visibility_of(element))
        return element

    def get_elements(self, selector, by_method=By.CSS_SELECTOR, source=None):
        if source is None:
            source = self.driver
            
        elements = WebDriverWait(source, 10).until(EC.presence_of_all_elements_located((by_method, selector)))
        for element in elements:
            try:
                WebDriverWait(source, 2).until(EC.visibility_of(element))
            except TimeoutException:
                elements.remove(element)

        return elements

    
    # Page Interaction
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

        self.get_element("div.form-group textarea#query_sql").send_keys(self.query)
        self.get_element("div.form-group button#run_query").click()

        if not (hasattr(self, 'new_query_action')):
            raise Exception("New query action must be specified")

        if self.new_query_action == 'save':
            self.save_dataset()
            
        elif self.new_query_action == 'download':
            self.download_dataset()
            
        else:
            raise Exception("New query action unknown")


    def download_dataset():
        self.get_element("div.sql-dataset-actions button#download_query").click()
        # to do

    def save_dataset():
        self.get_element("div.sql-dataset-actions button.class btn-sm").click()

        form = self.get_element("form")

        self.get_element("input#blah1", source=form).send_keys(self.dataset_name)
        self.get_element("input#blah2", source=form).send_keys(self.dataset_desc)
        checkbox = self.get_element("div.checkbox input ")
        if (self.dataset_public and not checkbox.is_selected()) or (not self.dataset_public and checkbox.is_selected()):
            checkbox.click()

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
