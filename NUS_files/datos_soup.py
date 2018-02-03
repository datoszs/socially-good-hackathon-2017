# -*- coding: utf-8 -*-
"""
Created on Sat Dec 30 22:55:33 2017

@author: koszt
"""


from bs4 import BeautifulSoup
from bs4.element import Comment
import re
import requests
from retry import retry
from collections import defaultdict
import json
import random
import time

SAVE_DIRECTORY =  "C:/Users/koszt/Documents/Scraperista/Datos"

@retry(Exception, tries=5, delay=0.3)
def append_metadata_dict_to_file(metadata_dict,
                                 save_directory=SAVE_DIRECTORY,
                                 save_filename='datos_metadata.json'):
    with open(save_directory+'/'+save_filename, "a", encoding='utf-8') as json_file:
        json_file.write(json.dumps(metadata_dict, ensure_ascii=False)+'\n')


@retry(Exception, tries=5, delay=0.3)
def create_metadata_dict(html_text):
    soup = BeautifulSoup(html_text, 'lxml')
    table = soup.find_all('tr')
    table_rows = [t.text for t in table if ':' in t.text]
    met_dict = defaultdict(list)
    for row in table_rows:
        print(row)
        key = row.split(':')[0]
        if key == 'ECLI':
            revalue = re.search('\\:.*', row)
            value = revalue.group(0)[1:]
            #value = revalue.string
        else:
            value = row.split(':')[1]
        mult_value = [x.strip() for x in value.split('\n')]
        met_dict[key] = mult_value
    return met_dict

met_dict = create_metadata_dict(text)

def get_ecli_number(met_dict):
    try:
        return met_dict['ECLI'][0].replace(':', '_')
    except:
        return met_dict['Spisová značka'][0].replace('/', '_')

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def text_from_html(body):
    soup = BeautifulSoup(body, 'lxml')
    sub = soup.find_all('div', class_='main_detail')
    texts = sub[0].find_all(text=True)
    #texts = soup.find_all('div', class_='main_detail', text=True)
    visible_texts = filter(tag_visible, texts)  
    return u"\n".join(t.strip() for t in visible_texts)

@retry(Exception, tries=5, delay=0.3)
def save_html_text(html_text, ecli_number, save_directory=SAVE_DIRECTORY):
    save_filename = ecli_number
    with open(save_directory+'/txt_files/'+save_filename+'.txt', "w", encoding='utf-8') as text_file:
        text_file.write(html_text)


with open('html_links.txt') as f:
    html_links = f.readlines()

# you may also want to remove whitespace characters like `\n` at the end of each line
for i in range(28, len(html_links)): 
    print (i)
    html_link = html_links[i]
    req_text = requests.get(html_link.replace('\n', '')).text
    met_dict = create_metadata_dict(req_text)
    append_metadata_dict_to_file(met_dict)
    ecli_number = get_ecli_number(met_dict)
    #html = urllib.request.urlopen(html_link).read()
    save_text = text_from_html(req_text)
    save_html_text(save_text, ecli_number)
    time.sleep(random.random())

save_html_text(save_text, 'romporkas')


html_links[i]

















311*1.2


##############

str(soup)

text

html_link = 'http://www.nsoud.cz/JudikaturaNS_new/judikatura_vks.nsf/WebSearch/0D581861E79E7178C12580400078F6A6?openDocument'
r = requests.get(html_link).text
text = r.text
r.json()
r.headers
r.content

soup = BeautifulSoup(text, 'lxml')
trs = soup.find_all('tr')
trs[0].text.strip()

soup.find_all('div', {'class': 'main_detail'})
main_detail = soup.find_all('div', class_='main_detail')
       
append_metadata_dict_to_file(met_dict)

import urllib.request
import shutil

with urllib.request.urlopen(html_link) as response, open(SAVE_DIRECTORY+'/testerka.txt', 'wb') as out_file:
    shutil.copyfileobj(response, out_file)

urllib.request.urlretrieve(html_link, SAVE_DIRECTORY+'/testerka.txt')
    












        




