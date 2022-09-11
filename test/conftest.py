import os

import allure
import pytest

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from Contacts import ListContact, FullContact


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == 'call' and rep.failed:
        mode = 'a' if os.path.exists('failures') else 'w'
        try:
            with open('failures', mode) as f:
                if 'browser' in item.fixturenames:
                    web_driver = item.funcargs['browser']
                else:
                    print('Fail to take screenshot')
                    return
            allure.attach(
                web_driver.get_screenshot_as_png(),
                name='screenshot',
                attachment_type=allure.attachment_type.PNG
            )
        except Exception as e:
            print('Fail to take screenshot: {}'.format(e))


@pytest.fixture(scope='function')
def browser():
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    yield driver
    driver.close()
    driver.quit()


@pytest.fixture(scope='session')
def test_contact():
    return FullContact('John', 'Wick', 'Businesses', 'September 12, 1964', 'Unknown')


def pytest_assertrepr_compare(op, left, right):
    if isinstance(left, ListContact) and isinstance(right, ListContact) and op == "==":
        errors = ["Comparing ListContact instances:"]
        if left.first_name != right.first_name:
            errors.append("   first_names: {} != {}".format(left.first_name, right.first_name))
        if left.last_name != right.last_name:
            errors.append("   last_names: {} != {}".format(left.last_name, right.last_name))
        if left.address != right.address:
            errors.append("   addresses: {} != {}".format(left.address, right.address))

        if isinstance(left, FullContact) and isinstance(right, FullContact):
            if left.category != right.category:
                errors.append("   categories: {} != {}".format(left.category, right.category))
            if left.birthday != right.birthday:
                errors.append("   birthdays: {} != {}".format(left.birthday, right.birthday))

        return errors
