from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from attrdict import AttrDict
from datetime import datetime
from pytz import timezone
from re import findall
from time import sleep
from csv import writer
import hashlib
import os
import yaml
import tempfile
import pandas as pd


class BasePage(object):

    def __init__(self, driver):
        self.driver = driver
        self.element = None
        self.elements = None
        self.locator_name = None
        self.locator = None

    def open_web(self, url):
        self.driver.get(url)

    def scroll_page_to_element(self, locator):
        element = self.find_web_element(locator)
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        self.driver.execute_script("arguments[0].scrollIntoView();", element)

    def find_web_element(self, locator, timeout=20, err=None, trap=True):
        self.locator_name, self.locator = locator
        self.element = None
        try:
            if self.locator_name == 'id':
                self.element = WebDriverWait(self.driver, timeout).until(
                    EC.presence_of_element_located((By.ID, self.locator)), "%s not present" % self.locator
                )
            elif self.locator_name == 'class':
                self.element = WebDriverWait(self.driver, timeout).until(
                    EC.presence_of_element_located((By.CLASS_NAME, self.locator)), "%s not present" % self.locator
                )
            elif self.locator_name == 'css':
                self.element = WebDriverWait(self.driver, timeout).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, self.locator)), "%s not present" % self.locator
                )
            elif self.locator_name == 'link':
                self.element = WebDriverWait(self.driver, timeout).until(
                    EC.presence_of_element_located((By.LINK_TEXT, self.locator)), "%s not present" % self.locator
                )
            elif self.locator_name == 'xpath':
                self.element = WebDriverWait(self.driver, timeout).until(
                    EC.presence_of_element_located((By.XPATH, self.locator)), "%s not present" % self.locator
                )
        except TimeoutException as e:
            if trap:
                raise TimeoutException(err if err else "%s" % e.msg)
        except NoSuchElementException:
            if trap:
                raise NoSuchElementException(err if err else "%s not present" % self.locator)
            # print '%s is not present' % self.locator
        return self.element

    def element_present(self, locator):
        self.element = False
        try:
            self.element = self.find_web_element(locator)
        except TimeoutException:
            print('\t%s Time out exception' % self.locator)
            return self.element

    def find_web_elements(self, locator, timeout=2):
        self.elements = None
        self.locator_name, self.locator = locator
        try:
            if self.locator_name == 'id':
                # self.elements = self.driver.find_elements(By.ID, self.locator)
                by = By.ID
            elif self.locator_name == 'class':
                # self.elements = self.driver.find_elements(By.CLASS_NAME, self.locator)
                by = By.CLASS_NAME
            elif self.locator_name == 'css':
                # self.elements = self.driver.find_elements(By.CSS_SELECTOR, self.locator)
                by = By.CSS_SELECTOR
            elif self.locator_name == 'link':
                # self.elements = self.driver.find_elements(By.LINK_TEXT, self.locator)
                by = By.LINK_TEXT
            elif self.locator_name == 'tag':
                # self.elements = self.driver.find_elements(By.TAG_NAME, self.locator)
                by = By.TAG_NAME
            elif self.locator_name == 'xpath':
                # self.elements = self.driver.find_elements(By.XPATH, self.locator)
                by = By.XPATH
            self.elements = WebDriverWait(self.driver, timeout).until(EC.visibility_of_any_elements_located(
                (by, self.locator)), "%s not present" % self.locator)
        except WebDriverException as e:
            print('Element not present \n %s' % e)
        return self.elements

    def options_list(self, locator):
        drop_down_list = Select(self.find_web_element(locator)).options
        return [item.text for item in drop_down_list]  # if item.text != u'None']

    def select_drop_down(self, locator, visible_text):
        Select(self.find_web_element(locator)).select_by_visible_text(visible_text)

    def get_selected_option(self, locator):
        return Select(self.find_web_element(locator)).first_selected_option.text

    def get_first_option(self, locator):
        Select(self.find_web_element(locator)).select_by_index(0)

    def select_check_box(self, locator):
        self.find_web_element(locator).click()

    def check_box_status(self, locator):
        return self.find_web_element(locator).is_selected()

    def get_text_box_value(self, locator):
        return self.find_web_element(locator).get_attribute('value')

    def wait_for_element_to_be_visible(self, locator, timeout=5, msg=None):
        self.locator_name, self.locator = locator
        self.element = None
        try:
            if self.locator_name == 'id':
                self.element = WebDriverWait(self.driver, timeout). \
                    until(EC.visibility_of_element_located((By.ID, self.locator)), msg)
            elif self.locator_name == 'class':
                self.element = WebDriverWait(self.driver, timeout). \
                    until(EC.visibility_of_element_located((By.CLASS_NAME, self.locator)), msg)
            elif self.locator_name == 'link':
                self.element = WebDriverWait(self.driver, timeout). \
                    until(EC.visibility_of_element_located((By.LINK_TEXT, self.locator)), msg)
            elif self.locator_name == 'css':
                self.element = WebDriverWait(self.driver, timeout). \
                    until(EC.visibility_of_element_located((By.CSS_SELECTOR, self.locator)), msg)
            elif self.locator_name == 'xpath':
                self.element = WebDriverWait(self.driver, timeout). \
                    until(EC.visibility_of_element_located((By.XPATH, self.locator)), msg)
        except TimeoutException as e:
            print('Time out \n %s' % e)
        return self.element

    def wait_for_element_to_not_be_visible(self, locator, timeout=5, msg=None):
        self.locator_name, self.locator = locator
        self.element = None
        try:
            if self.locator_name == 'id':
                self.element = WebDriverWait(self.driver, timeout). \
                    until(EC.invisibility_of_element_located((By.ID, self.locator)), msg)
            elif self.locator_name == 'class':
                self.element = WebDriverWait(self.driver, timeout). \
                    until(EC.invisibility_of_element_located((By.CLASS_NAME, self.locator)), msg)
            elif self.locator_name == 'link':
                self.element = WebDriverWait(self.driver, timeout). \
                    until(EC.visibility_of_element_located((By.LINK_TEXT, self.locator)), msg)
            elif self.locator_name == 'css':
                self.element = WebDriverWait(self.driver, timeout). \
                    until(EC.visibility_of_element_located((By.CSS_SELECTOR, self.locator)), msg)
            elif self.locator_name == 'xpath':
                self.element = WebDriverWait(self.driver, timeout). \
                    until(EC.visibility_of_element_located((By.XPATH, self.locator)), msg)
        except TimeoutException as e:
            print('Time out \n %s' % e)
        return self.element

    def double_click(self, locator):
        actionChains = ActionChains(self.driver)
        actionChains.double_click(locator).perform()

    def wait_click(self, locator, err=None, trap=True):
        self.locator_name, self.locator = locator
        self.element = None
        try:
            if self.locator_name == 'id':
                self.element = WebDriverWait(self.driver, timeout=20).until(
                    EC.element_to_be_clickable((By.ID, self.locator)), f"{self.locator} not clickable"
                )

            elif self.locator_name == 'class':
                self.element = WebDriverWait(self.driver, timeout=20).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, self.locator)), f"{self.locator} not clickable"
                )

            elif self.locator_name == 'xpath':
                self.element = WebDriverWait(self.driver, timeout=20).until(
                    EC.element_to_be_clickable((By.XPATH, self.locator)), f"{self.locator} not clickable"
                )
        except TimeoutException as e:
            if trap:
                raise TimeoutException(err if err else f"{e.msg}")
        except NoSuchElementException:
            if trap:
                raise NoSuchElementException(err if err else f"{self.locator}")
        except ElementClickInterceptedException:
            if trap:
                raise ElementClickInterceptedException(err if err else f"{self.locator}")
        return self.element

    def wait_visibility(self, locator, err=None, trap=True):
        self.locator_name, self.locator = locator
        self.element = None
        try:
            if self.locator_name == 'id':
                self.element = WebDriverWait(self.driver, timeout=20).until(
                    EC.visibility_of_element_located((By.ID, self.locator)), f"{self.locator} not visible"
                )

            elif self.locator_name == 'class':
                self.element = WebDriverWait(self.driver, timeout=20).until(
                    EC.visibility_of_element_located((By.CLASS_NAME, self.locator)), f"{self.locator} not visible"
                )

            elif self.locator_name == 'xpath':
                self.element = WebDriverWait(self.driver, timeout=20).until(
                    EC.visibility_of_element_located((By.XPATH, self.locator)), f"{self.locator} not visible"
                )
        except TimeoutException as e:
            if trap:
                raise TimeoutException(err if err else f"{e.msg}")
        except NoSuchElementException:
            if trap:
                raise NoSuchElementException(err if err else f"{self.locator}")
        return self.element

    def replace_value_in_locator(self, locator, value):
        locator_path = locator[1].replace('value_in_locator', value)
        locator_name = locator[0]
        locator = (locator_name, locator_path)
        return locator

    def replace_id_and_value_in_locator(self, locator, id, value):
        locator_id = locator[1].replace('number_id_on_page', id)
        locator_path = locator_id.replace('value_in_locator', value)
        locator_name = locator[0]
        locator = (locator_name, locator_path)
        return locator

    def clear_input_with_keys(self, selector):
        self.double_click(selector)
        selector.send_keys(Keys.BACKSPACE)