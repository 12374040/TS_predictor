import json
import time
import copy
import sqlite3
import requests
import sys
import urllib.request
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from datetime import datetime

def get_driver():
    platforms = {
        'linux' : './chromedriver',
        'win32' : 'chromedriver.exe'
    }
    if sys.platform not in platforms:
        return sys.platform
    
    return platforms[sys.platform]

def get_href(url):
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(get_driver(), options=options)
    driver.get(url)
    print(str(url))
    visited_links.append(url)
    time.sleep(2)
    xpath = []
    links = []
    events = []
    move_next = []
    is_event = '/event/'
    is_help = 'help'
    is_content = 'content/'
    is_ticketswap = 'ticketswap.nl'
    
    try:
        driver.find_element(By.XPATH, '//h4[text()="Laat meer zien"]').click() # click load more
        time.sleep(1)
    except:
        print('no load more')
    

    xpath.extend(driver.find_elements(By.XPATH, '//a'))
    
    for x in xpath:
        links.append(str(x.get_attribute("href")))# append link to list
        # print(str(x.get_attribute("href")))
    # print('links = ' + str(links))

    driver.close()
    events = [x for x in links if is_event in x]
    # print('events = ' + str(events))

    move_next = [x for x in links if is_ticketswap in x and is_event not in x and is_help not in x and is_content not in x and x not in visited_links] # search for more links to traverse
    # print('nextmove = ' + str(move_next))

    for x in move_next:
        events.extend(get_href(x))# recursive call 

    return events

def create_link_db():
    conn = sqlite3.connect('links.db')
    c = conn.cursor()
    
    
    c.execute("CREATE TABLE IF NOT EXISTS base (link varchar(255));")
    
    conn.commit()
    conn.close()

def update_link_values(data): 
    print('updating...')
    conn = sqlite3.connect('links.db')
    c = conn.cursor()
    new_values =[tuple(x) for x in data]
    for value in new_values:
        c.executemany('INSERT INTO base (link) VALUES (?);', value)

    conn.commit()
    conn.close()

event_links = []
visited_links = []
create_link_db()
event_links = get_href('https://www.ticketswap.nl/')
print('event links = ')
for x in event_links:
    print(x)

update_link_values(event_links)
# TO_DO:
# in een file zetten









