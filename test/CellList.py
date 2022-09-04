# -*- coding: utf-8 -*-
from selenium.webdriver import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By

from Contacts import ListContact, FullContact


class CellListLocators:
    LOCATOR_CONTACTS = (By.CSS_SELECTOR, '[__idx]')
    LOCATOR_CONTACTS_LIST = (By.CLASS_NAME, 'CMWVMEC-p-b')
    LOCATOR_CONTACTS_LIST_COUNTERS = (By.CSS_SELECTOR, '.CMWVMEC-p-b + .gwt-HTML')
    LOCATOR_FIRST_NAME = (By.XPATH, '//td[contains(text(), "First Name")]/following-sibling::td/input')
    LOCATOR_LAST_NAME = (By.XPATH, '//td[contains(text(), "Last Name")]/following-sibling::td/input')
    LOCATOR_CATEGORY = (By.CSS_SELECTOR, '.CMWVMEC-w-b + td > .gwt-ListBox')
    LOCATOR_BIRTHDAY = (By.CLASS_NAME, 'gwt-DateBox')
    LOCATOR_ADDRESS = (By.CLASS_NAME, 'gwt-TextArea')

    LOCATOR_UPDATE_CONTACT = (By.XPATH, '//button[text()="Update Contact"]')
    LOCATOR_CREATE_CONTACT = (By.XPATH, '//button[text()="Create Contact"]')


class BasePage:

    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url

    def find_element(self, locator, time=5):
        return WebDriverWait(self.driver, time).until(expected_conditions.presence_of_element_located(locator),
                                                      message=f"Can't find element by locator {locator}")

    def find_elements(self, locator, time=5):
        return WebDriverWait(self.driver, time).until(expected_conditions.presence_of_all_elements_located(locator),
                                                      message=f"Can't find elements by locator {locator}")

    def elements_value_contain_text(self, locator, text, time=5):
        return WebDriverWait(self.driver, time).until(
            expected_conditions.text_to_be_present_in_element_value(locator, text_=text),
            message=f"Element by locator {locator} doesn't contain {text} in value")

    def elements_text_contain_text(self, locator, text, time=5):
        return WebDriverWait(self.driver, time).until(
            expected_conditions.text_to_be_present_in_element_attribute(locator, attribute_='textContent', text_=text),
            message=f"Element by locator {locator} doesn't contain {text} in attribute 'textContent'")

    def open(self):
        self.driver.get(self.base_url)


class CellListPage(BasePage):

    def __init__(self, driver):
        base_url = 'https://samples.gwtproject.org/samples/Showcase/Showcase.html#!CwCellList'
        super().__init__(driver, base_url)

    def scroll_list_to_current_list_end(self):
        current_length = self.get_current_list_length()
        self.find_element(CellListLocators.LOCATOR_CONTACTS_LIST).send_keys(Keys.END)
        total_length = self.get_total_list_length()
        expected_length = min(current_length + 20, total_length)
        self.elements_text_contain_text(CellListLocators.LOCATOR_CONTACTS_LIST_COUNTERS, str(expected_length))

    def scroll_to_list_end(self):
        while True:
            current = self.get_current_list_length()
            total = self.get_total_list_length()
            if current == total:
                break

            self.scroll_list_to_current_list_end()

    def get_current_list_length(self):
        element = self.find_element(CellListLocators.LOCATOR_CONTACTS_LIST_COUNTERS)
        counters = element.text.split(' ')
        return int(counters[2])

    def get_total_list_length(self):
        element = self.find_element(CellListLocators.LOCATOR_CONTACTS_LIST_COUNTERS)
        counters = element.text.split(' ')
        return int(counters[-1])

    def select_contact_from_list(self, index):
        contacts = self.find_elements(CellListLocators.LOCATOR_CONTACTS)
        contacts[index].click()
        contact = self.get_contact_from_list(index)
        self.elements_value_contain_text(CellListLocators.LOCATOR_FIRST_NAME, contact.first_name)

    def get_contact_from_list(self, index):
        contacts = self.find_elements(CellListLocators.LOCATOR_CONTACTS)
        contact = contacts[index]
        contact_data = contact.text.split('\n')
        name = contact_data[0].split()
        first_name = name[0]
        last_name = name[1]
        address = contact_data[1]
        return ListContact(first_name, last_name, address)

    def get_contact_from_contact_info(self):
        first_name = self.find_element(CellListLocators.LOCATOR_FIRST_NAME).get_attribute('value')
        last_name = self.find_element(CellListLocators.LOCATOR_LAST_NAME).get_attribute('value')
        category = self.find_element(CellListLocators.LOCATOR_CATEGORY).get_attribute('value')
        birthday = self.find_element(CellListLocators.LOCATOR_BIRTHDAY).get_attribute('value')
        address = self.find_element(CellListLocators.LOCATOR_ADDRESS).get_attribute('value')
        return FullContact(first_name, last_name, category, birthday, address)

    def fill_contact_info(self, contact):
        info_first_name = self.find_element(CellListLocators.LOCATOR_FIRST_NAME)
        info_last_name = self.find_element(CellListLocators.LOCATOR_LAST_NAME)
        info_birthday = self.find_element(CellListLocators.LOCATOR_BIRTHDAY)
        info_address = self.find_element(CellListLocators.LOCATOR_ADDRESS)
        info_category = self.find_element(CellListLocators.LOCATOR_CATEGORY)

        info_first_name.clear()
        info_first_name.send_keys(contact.first_name)
        info_last_name.clear()
        info_last_name.send_keys(contact.last_name)
        info_birthday.clear()
        info_birthday.send_keys(contact.birthday)
        info_birthday.send_keys(Keys.ENTER)
        info_address.clear()
        info_address.send_keys(contact.address)

        Select(info_category).select_by_value(contact.category)

    def update_contact(self):
        return self.find_element(CellListLocators.LOCATOR_UPDATE_CONTACT).click()

    def create_contact(self):
        return self.find_element(CellListLocators.LOCATOR_CREATE_CONTACT).click()
