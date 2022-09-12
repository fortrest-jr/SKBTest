# -*- coding: utf-8 -*-
import allure
import pytest

from CellList import CellListPage


def refresh_and_get_contact_info(page, index):
    refresh_index = 1 if index == 0 else index - 1
    page.select_contact_from_list(refresh_index)
    page.select_contact_from_list(index)
    return page.get_contact_from_contact_info()


@allure.description('Test loading correct info from selected item in list')
@pytest.mark.parametrize('index_to_get', [0])
def test_get_contact_info_from_list(browser, index_to_get):
    cell_list_page = CellListPage(browser)
    cell_list_page.open()
    
    cell_list_page.select_contact_from_list(index_to_get)
    
    list_contact = cell_list_page.get_contact_from_list(index_to_get)
    info_contact = cell_list_page.get_contact_from_contact_info()
    assert info_contact == list_contact


@allure.description('Test updating info in selected item in list')
@pytest.mark.parametrize('index_to_update', [0])
def test_update_contact(browser, test_contact, index_to_update):
    cell_list_page = CellListPage(browser)
    cell_list_page.open()
    
    cell_list_page.select_contact_from_list(index_to_update)    
    cell_list_page.fill_contact_info(test_contact)
    cell_list_page.update_contact()
    
    list_contact = cell_list_page.get_contact_from_list(index_to_update)
    assert list_contact == test_contact
    info_contact = refresh_and_get_contact_info(cell_list_page, index_to_update)
    assert info_contact == test_contact


@allure.description('Test creating new contact and loading it from list')
def test_create_full_contact(browser, test_contact):
    cell_list_page = CellListPage(browser)
    cell_list_page.open()

    old_total_length = cell_list_page.get_total_list_length()
    cell_list_page.fill_contact_info(test_contact)
    cell_list_page.create_contact()
    
    assert (new_total_length := cell_list_page.get_total_list_length()) == old_total_length + 1
    cell_list_page.scroll_to_list_end()
    list_contact = cell_list_page.get_contact_from_list(new_total_length-1)
    assert list_contact == test_contact
    info_contact = refresh_and_get_contact_info(cell_list_page, new_total_length-1)
    assert info_contact == test_contact


@allure.description('Test no contact is created if all fields are not filled')
def test_empty_contact_creation_attempt_do_not_increment_counter(browser):
    cell_list_page = CellListPage(browser)
    cell_list_page.open()
    
    old_total_length = cell_list_page.get_total_list_length()
    cell_list_page.create_contact()
    
    new_total_length = cell_list_page.get_total_list_length()
    assert new_total_length == old_total_length
