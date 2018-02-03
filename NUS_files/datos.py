# -*- coding: utf-8 -*-
"""
Created on Sat Dec 30 16:45:14 2017

@author: koszt
"""

from urllib.request import urlopen, urlretrieve, quote
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re
from collections import defaultdict
import json
import random
import time
from selenium.webdriver.common.keys import Keys # scrolling keys up down
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from retry import retry


time.sleep(0.5)

SAVE_DIRECTORY =  "C:/Users/koszt/Documents/Scraperista/Datos"


def wait_between(base_delay=5):
    seconds = base_delay + (random.random() * base_delay)

def increase_date():
    pass

def get_court_list(driver):
    courts = driver.find_element_by_id('soud')
    nostrip = courts.text.split('\n')
    ystrip = [x.strip() for x in nostrip][2:-1]
    
    # select court from list
    from selenium.webdriver.support.ui import Select
    select = Select(driver.find_element_by_id('soud'))
    select.select_by_visible_text(ystrip[0])

    # search button and submit
    search = driver.find_element_by_class_name('search')
    search.click()
    
def get_datefields_list(driver):
    datefield_list = driver.find_elements_by_class_name('v-datefield-textfield')
    dateod = driver.find_element_by_id('dateOd')
    dateod.click()
    dateod.send_keys('20.12.2017')
    dateod.clear()
    return datefield_list
    
def fill_in_dates(driver, datefield_list, start_date, end_date):
    driver.implicitly_wait(10)
    start_field = datefield_list[0]
    end_field = datefield_list[1]
    start_field.clear()
    end_field.clear()
    end_field.send_keys(end_date)
    start_field.send_keys(start_date)

def click_submit_button(driver):
    submit_button = driver.find_elements_by_class_name('v-button-caption')
    return submit_button[0].click()

def click_back_button(driver):
    driver.find_element_by_xpath("""//*[@id="v-USSRDmsSearch_WAR_ussrintranetportlet_LAYOUT_11255"]/div/div[2]/div/div[7]/div/div/div/span/span""").click()

@retry(Exception, tries=5, delay=0.4)
def click_nextpage_button(driver):
    try:
        next_button = driver.find_element_by_xpath("""//*[@id="v-USSRDmsSearch_WAR_ussrintranetportlet_LAYOUT_11255"]/div/div[2]/div/div[5]/div/div/div[2]/div/div[2]/div/div/div[2]/div/div[13]/div/span/span""")
        driver.execute_script("arguments[0].scrollIntoView(false);", next_button)
        assert isinstance(next_button, object)
    except:
        raise Exception
    next_button.click()


    
    

    
def download_all_pdf(driver, pdfs_list, save_directory=SAVE_DIRECTORY):
#    for pdf_link in pdfs_list:
#        print (pdf_link, pdf_link.text)
#        pdf_link.click()
    for i in range(len(pdfs_list)):
        driver.implicitly_wait(10)
        pdfs_list[i].click()
        wait_between(base_delay=0.3)
        
def get_number_of_files(driver):
    numres = driver.find_element_by_xpath("""//*[@id="v-USSRDmsSearch_WAR_ussrintranetportlet_LAYOUT_11255"]/div/div[2]/div/div[5]/div/div/div[2]/div/div[3]/div""")
    results_found = re.search('(\d+)(?!.*\d)', numres.text)
    return int(results_found.group())

@retry(Exception, tries=5, delay=0.3)
def create_showmore_buttons_list(driver):
    """you must have results already on page"""
    time.sleep(0.2)
    try:
        click_buttons = driver.find_elements_by_class_name('v-button-caption')
        showmore_text = [el.text for el in click_buttons]
        show_more_elements = [click_buttons[i] for i in range(len(showmore_text)) 
                              if showmore_text[i] in ['Zobraziť viac', 'Zobraziť menej']]
        assert len(show_more_elements) > 0
    except AssertionError:
        raise Exception
    return show_more_elements
  
@retry(Exception, tries=5, delay=0.4)
def get_showless_button(driver):
    driver.implicitly_wait(10)
    try:
        click_buttons = driver.find_elements_by_class_name('v-button-caption')
        time.sleep(0.4)
        slbut_text = [el.text for el in click_buttons]
        time.sleep(0.3)
        slbut = [click_buttons[i] for i in range(len(slbut_text))
                       if slbut_text[i] == 'Zobraziť menej']
        assert len(slbut) > 0
    except:
        raise Exception
    return slbut[0]

@retry(Exception, tries=5, delay=0.4)       
def click_showless_button(driver, showless_button):
    time.sleep(0.2)
    driver.execute_script("arguments[0].scrollIntoView(false);", showless_button)
    time.sleep(0.4)
    showless_button.click()

@retry(Exception, tries=5, delay=0.3)
def click_show_more_button(driver, showmore_button):
    time.sleep(0.2)
    driver.execute_script("arguments[0].scrollIntoView(false);", showmore_button)
    time.sleep(0.3)
    showmore_button.click()

@retry(Exception, tries=5, delay=0.3)
def get_html_view_button(driver):
    time.sleep(0.2)
    try:
        click_buttons = driver.find_elements_by_class_name('v-button-caption')
        html_button_text = [el.text for el in click_buttons]
        html_button = [click_buttons[i] for i in range(len(html_button_text))
                       if html_button_text[i] == 'HTML náhľad textu']
        assert len(html_button) == 1
    except AssertionError:
        raise Exception
    return html_button[0]

@retry(Exception, tries=5, delay=0.3)
def click_html_view_button(driver, html_button):
    time.sleep(0.2)
    driver.execute_script("arguments[0].scrollIntoView(false);", html_button)
    time.sleep(0.2)
    try:
        html_button.click()
    except:
        raise Exception
    
@retry(Exception, tries=5, delay=0.3)
def get_html_view_text(driver):
    # must be at html view details page
    return driver.find_element_by_class_name('v-panel-content-contentpanel').text

@retry(Exception, tries=5, delay=0.3)
def save_html_text(html_text, save_tuple, save_directory=SAVE_DIRECTORY):
    ecli, ecs = save_tuple
    ecli = ecli.replace(':', '_')
    ecs = ecs.replace('/', '_')
    if len(ecli) > 0:
        save_filename = ecli
    else:
        save_filename = ecs
    print(save_filename)
    with open(save_directory+'/txt_files/'+save_filename+'.txt', "w", encoding='utf-8') as text_file:
        text_file.write(html_text)
        

    
@retry(Exception, tries=5, delay=0.3)
def click_back_from_html_view(driver):
    """Make sure you are in html view mode
    There should be 2 buttons and both are back to search."""
    click_button = driver.find_elements_by_class_name('v-button-caption')
    time.sleep(0.2)
    click_button[1].click()

def write_number_of_results(start_date, number_of_results,
                            save_directory=SAVE_DIRECTORY,
                            numbers_file='number_of_results.txt'):
    """create file with append and write number of results for each month"""
    numres_dict = {start_date: number_of_results}
    with open(save_directory+'/'+numbers_file, "a") as json_file:
        json_file.write(json.dumps(numres_dict)+'\n')
  
#def create_metadata_columns(driver):
#    elements = driver.find_elements_by_class_name('v-slot-propertylbl')
#    return [el.text for el in elements]
#
#def create_metadata_values(driver):   
#    column_values = driver.find_elements_by_class_name('v-slot-valuelbl')
#    return [cv.text for cv in column_values]

@retry(Exception, tries=5, delay=0.3)
def create_metadata_dict(driver):
    time.sleep(0.2)
    try:
        metadata_columns = driver.find_elements_by_class_name('v-slot-propertylbl')
        metadata_values = driver.find_elements_by_class_name('v-slot-valuelbl')
        time.sleep(0.1)
        mc = [mc.text for mc in metadata_columns]
        mv = [mv.text for mv in metadata_values]
        assert mc[0] == 'ECLI'
    except:
        raise Exception
    metadata_dict = dict(zip(mc, mv))
    try:
        ecs_number = driver.find_element_by_class_name('v-button-filereference').text
        time.sleep(0.2)
        assert len(ecs_number) > 0
    except:
        raise Exception
    metadata_dict['ecs'] = ecs_number
    return metadata_dict

@retry(Exception, tries=5, delay=0.3)
def append_metadata_dict_to_file(metadata_dict,
                                 save_directory=SAVE_DIRECTORY,
                                 save_filename='US_metadata.json'):
    with open(save_directory+'/'+save_filename, "a", encoding='utf-8') as json_file:
        json_file.write(json.dumps(metadata_dict, ensure_ascii=False)+'\n')
  
@retry(Exception, tries=3)  
def find_and_download_pdfs(driver):
    time.sleep(0.5)
    pdfs_list = find_all_pdf(driver)
    time.sleep(1.5)
    driver.execute_script("arguments[0].scrollIntoView(false);", pdfs_list[0])
    time.sleep(1)
    download_all_pdf(driver, pdfs_list)

@retry(Exception, tries=5, delay=0.3)     
def get_ecli_ecs_number(metadata_dict):
    return (metadata_dict['ECLI'], metadata_dict['ecs'])


    # select court from list
    from selenium.webdriver.support.ui import Select
    select = Select(driver.find_element_by_id('soud'))
    select.select_by_visible_text(ystrip[0])









@retry(Exception, tries=5, delay=0.3)
def get_nextpage_button(driver):
    previous_next = driver.find_elements_by_class_name('all_news')
    nextpage = [x for x in previous_next if x.text == 'Další rozhodnutí >>']
    return nextpage

@retry(Exception, tries=5, delay=0.3)
def get_court_list(driver):
    courts = driver.find_element_by_id('soud')
    nostrip = courts.text.split('\n')
    cstrip = [x.strip() for x in nostrip][2:-1]
    return cstrip

@retry(Exception, tries=5, delay=0.3)
def submit_court(driver, court_name):
    select = Select(driver.find_element_by_id('soud'))
    time.sleep(0.3)
    select.select_by_visible_text(court_name)
    

@retry(Exception, tries=5, delay=0.3)
def click_search(driver):
    # search button and submit
    search = driver.find_element_by_class_name('search')
    time.sleep(0.3)
    search.click()

@retry(Exception, tries=5, delay=0.3)
def save_html_links(html_links, save_directory=SAVE_DIRECTORY):
    with open(save_directory+'/html_links.txt', "a", encoding='utf-8') as text_file:
        for link in html_links:
            text_file.write("%s\n" % link)

@retry(Exception, tries=5, delay=0.3)
def find_all_document_links(driver):
    try:
        documents = driver.find_elements_by_css_selector('a[href*=openDocument]')
        time.sleep(0.3)
        document_links = [x.get_attribute('href') for x in documents]
        assert len(document_links) > 0
    except:
        raise Exception
    return document_links

@retry(Exception, tries=5, delay=0.3)
def click_to_homepage(driver):
    back_button = driver.find_element_by_class_name('res_back')
    time.sleep(0.3)
    back_button.click()

dls = find_all_document_links(driver)
len(dls)



courts_list = get_court_list(driver)
# court = courts_list[1]
for court in courts_list:
    submit_court(driver, court)
    click_search(driver)
    has_nextpage = True
    while has_nextpage: 
        html_links = find_all_document_links(driver)
        save_html_links(html_links)
        nextpage = get_nextpage_button(driver)
        if nextpage:
            nextpage[0].click()
        else:
            has_nextpage = False
    click_to_homepage(driver)
    
    


# parse html text to file
bt = driver.find_element_by_id('box-table-a')
bt.text

main_detail = driver.find_element_by_class_name('main_detail')
main_detail.text

#@retry(Exception, tries=5, delay=0.3)
#def create_metadata_dict(driver):
#    table = driver.find_elements_by_tag_name('tr')
#    table_rows = [t.text for t in table]
#    met_dict = defaultdict(list)
#    for row in table_rows:
#        key = row.split(':')[0]
#        value = row.split(':')[1]
#        mult_value = [x.strip() for x in value.split('\n')]
#        met_dict[key] = mult_value
#    return met_dict





    
    
met_dict['test'] = 'fda'

ttsplit = tts[5].split(':')
ttsplit[1].split('\n')

import ast
ast.literal_eval(tts[0])



chrome_options = Options()
prefs = {"download.default_directory" : SAVE_DIRECTORY+"/files"}
chrome_options.add_experimental_option("prefs",prefs)
chrome_path = r"chromedriver.exe"

driver = webdriver.Chrome(chrome_path, chrome_options=chrome_options)
driver.implicitly_wait(10)

driver.get("http://www.nsoud.cz/JudikaturaNS_new/judikatura_vks.nsf/WebSpreadSearch")


            
        
        

            
        
        