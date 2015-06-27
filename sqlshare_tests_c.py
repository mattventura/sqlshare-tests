# Automation Tests for SQLShare
# - Matt Stone
import os
import unittest
import getpass
import time

from datetime import datetime


from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from selenium.webdriver.common.action_chains import ActionChains as AC

from selenium.webdriver.common.keys import Keys

from sqlshare_settings import settings


        
class DriverMethods:

    def get_element(self, selector, by_method=By.CSS_SELECTOR, source=None, ignore_visibility=True):
        if source is None:
            source = self.driver
            
        element = WebDriverWait(source, 10).until(EC.presence_of_element_located((by_method, selector)))
        
        if not ignore_visibility:
            WebDriverWait(source, 10).until(EC.visibility_of(element))
            
        return element
    

    def get_elements(self, selector, by_method=By.CSS_SELECTOR, source=None, ignore_visibility=True):
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
    

class PageNavigation:

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

    def scroll_to_bottom_of_datasets_page(self):
        current = len(self.get_elements("a.sql-dataset-list-item"))
        prior = -1
        while (prior != current):
            time.sleep(2)
            prior = current            
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            current = len(self.get_elements("a.sql-dataset-list-item"))            


    def open_dataset(self, dataset_name):
        self.click_sidebar_link("All")

        datasets = self.get_datasets()
        for dataset in datasets:
            if dataset['name'].lower() == dataset_name.lower():
                dataset['element'].click()
                return

        raise Exception("Dataset with name \"" + dataset_name + "\" could not be found")
            

class GetMethods:

    def get_datasets(self):
        selectors = {
            'name' : "span.sql-dataset-name",
            'ownr' : "span.sql-dataset-owner",
            'date' : "span.sql-dataset-modified",
            'desc' :  "div.sql-dataset-desc",
        }

        self.scroll_to_bottom_of_datasets_page()
        
        dataset_elements = self.get_elements("a.sql-dataset-list-item")
        
        datasets = []
        for element in dataset_elements:
            dataset = {}
            for detail in selectors.keys():
                dataset[detail] = self.get_element(selectors[detail], source=element).text.strip()
                print(dataset[detail])

            # Convert date to datetime object
            date_string = dataset['date'][10:]
            dataset['date'] = datetime.strptime(date_string, self.date_format)

            dataset['element'] = element
                
            datasets.append(dataset)

        return datasets

    
    def get_recent_datasets(self):
        self.click_sidebar_link("Recent Datasets")
            
        return self.get_datasets()
    

    def get_recent_queries(self):
        self.click_sidebar_link("Recent Queries")

        selectors = {
            'code'  : "span.sql-query-code",
            'date'  : "span.sql-query-date",
            'status': "span.sql-query-status",
        }
        
        query_elements = self.get_elements("div.sql-query-list a.sql-query-list-item")

        queries = []
        for element in query_elements:
            query = {}
            for detail in selectors.keys():
                query[detail] = self.get_element(selector, source=element).text.strip()

            date_string = query['date']
            query['date'] = datetime.strptime(date_string, self.date_format)

            queries.append(query)
            
        return queries
    

    def get_action_buttons(self):
        button_elements = self.get_elements("div.sql-dataset-actions button")
        actions = {}
        for button in button_elements:
            action = self.get_element("i span", source=button).text.strip()
            actions[action] = button

        return actions       


class PageActions:
    
    def new_query(self):
        self.click_sidebar_link("New Query")

        self.get_element("div.CodeMirror").click()
        self.actions.send_keys(self.query).perform()
        self.get_element("form button#run_query").click()

        if not (hasattr(self, 'new_query_action')):
            raise Exception("New query action must be specified")

        if self.new_query_action == 'save':
            self.get_action_buttons()['SAVE DATASET']
            self.save_dataset()
            
        elif self.new_query_action == 'download':
            self.get_action_buttons()['DOWNLOAD'].click()
            
        else:
            raise Exception("New query action unknown")
        

    def upload_dataset(self):
        self.click_sidebar_link("Upload Dataset")

        a_element = self.get_element("a#upload_dataset_browse")
        self.get_element("*", source=a_element).send_keys(self.filename)

        title_element = self.get_element("input#id_dataset_name")
        title_element.clear()
        title_element.send_keys(self.dataset_name)
        
        self.get_element("textarea#id_dataset_description").send_keys(self.dataset_desc)
        
        checkbox = self.get_element("div#final_settings_panel div.checkbox input")
        if (self.dataset_public and not checkbox.is_selected()) or (not self.dataset_public and checkbox.is_selected()):
            checkbox.click()

        self.get_element("button#save_button").click()

        time.sleep(5)
        self.click_sidebar_link("Yours")
        datasets = self.get_datasets()

        names = []
        for dataset in datasets:
            names.append(dataset['name'].lower())

        assert self.dataset_name.lower() in names


    def save_dataset(self):
        form = self.get_element("form")

        self.get_element("input#blah1",    source=form).send_keys(self.dataset_name)
        self.get_element("textarea#blah2", source=form).send_keys(self.dataset_desc)
        checkbox = self.get_element("div.checkbox input", source=form)
        if (self.dataset_public and not checkbox.is_selected()) or (not self.dataset_public and checkbox.is_selected()):
            checkbox.click()

        self.get_element("button", source=form).click()

        
class DatasetActions:

    def private_public_toggle(self):
        actions = self.get_action_buttons()
        for status in ['PRIVATE', 'PUBLIC']:
            if status in actions.keys():
                actions[status].click()
                return

            
    def share_dataset(self):
        self.get_action_buttons()['SHARE'].click()

        for email in self.emails:
            self.get_element("input#exampleInputEmail1").send_keys(email + Keys.ENTER)

        self.get_element("button#save_permissions_button").click()

        
    def delete_dataset(self):
        self.get_action_buttons()['DELETE'].click()
        self.get_element("button#delete_dataset").click()

    def run_query(self):
        self.get_element("button#run_query").click()

    def snapshot_dataset(self):
        self.get_action_buttons()['SNAPSHOT'].click()
        self.save_dataset()

    def download_dataset(self):
        self.get_action_buttons()['DOWNLOAD'].click()



class SQLShareSite(DriverMethods, PageNavigation, PageActions, GetMethods, DatasetActions):
    # This class combines the subclasses listed below
    None


class SQLShareTests(unittest.TestCase, SQLShareSite):

    def setUp(self):
        self.driver = getattr(webdriver, self.browser)()
        self.driver.get(self.url)

        self.actions = AC(self.driver)

        self.sqlshare_login()

        
    def tearDown(self):
        self.driver.quit()
