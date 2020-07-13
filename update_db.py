import json
import time
import copy
import sys
import sqlite3
import requests
import urllib.request
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import datetime

api_key = 'EAARj9Kx1ZCdIBAPQaszyaLc3kujJaZAHZCYSuXeZB1jjWCKswtkb3ZBtQ9QjpNdcOLZCHgklGT6YGHFTcuFdtZCecnRMVkBCKFcD5DZAPnfFchGDqRptFFImsjAQyGENSTAnNBs9apdwSnpikdehJnCCy6doORP3uCg860Nq4CzN0kIKFizJFdhzedXUI3Lab7ZBRZAEM3hZAR0vC4n01jayYAMwF5ElMrHtnGMOHV2e8POAgZDZD'

def get_driver():
    platforms = {
        'linux' : './chromedriver',
        'win32' : 'chromedriver.exe'
    }
    if sys.platform not in platforms:
        return sys.platform
    
    return platforms[sys.platform]

def scrape(links):
    data = []
    for link in links:
        request = requests.get(link)
        soup = BeautifulSoup(request.text, features="html.parser")

        ticket_features = ['aangeboden', 'verkocht', 'gezocht' ]
        ticket_soup = soup.find_all("span", { "class" : "css-v0hcsa e7cn512" })
        ticket_data = {ticket_features[i] : ticket_soup[i].span.text for i in range(len(ticket_soup))}
        
        event_soup = str(soup.find_all("script", { "type" : "application/ld+json"})[0].string)
        event_datapoint = json.loads(''.join([event_soup[i] for i in range(len(event_soup)) if event_soup[i] != "\n"]))
        ticket_data['name'] = event_datapoint['itemListElement'][3]['item']['name']

        ticket_data['event_date'] = soup.findAll("div", {"class": "css-102v2t9 ey3w7ki1"})[0].text

        ticket_data['location'] = soup.findAll("div", {"class": "css-102v2t9 ey3w7ki1"})[1].text
        try:
            ticket_data['facebook'] = soup.find("div", {"class": "css-1fwnys8 e1tolpgy2"}).find('a').get('href')
        except:
            ticket_data['facebook'] = 'None'
        ticket_data['link'] = link
        data.append(ticket_data)


    df = pd.DataFrame(data).fillna(0)
    df.loc[:, ['aangeboden', 'verkocht', 'gezocht']] = df.loc[:, ['aangeboden', 'verkocht', 'gezocht']].astype('int')
    df['date'] = [datetime.now(tz=None).strftime("%Y/%m/%d %H:%M:%S") for i in range(len(df))]
    
    return df


def links():
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(get_driver(), options=options)
    driver.get('https://www.ticketswap.nl/festivals')

    time.sleep(4)

    x = 6
    while True:
        try:
            driver.find_element_by_xpath('//*[@id="__next"]/div[3]/div/div/div[{}]/button'.format(x)).click()
            time.sleep(1)
            x+= 12
        except:
            break

    x = 1
    links = []
    while True:
        try:
            links.append(driver.find_element_by_xpath('//*[@id="__next"]/div[3]/div/div/div[{}]/a'.format(x)).get_attribute("href"))
            x+= 1
        except: 
            break
    
    print('{} links found'.format(len(links)))
    print('scraping...')
    return links



def create():
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS base (
    name varchar(255), event_date varchar(255), location varchar(255), facebook varchar(255), link varchar(255), aangeboden int, verkocht int, gezocht int, timestamp varchar(255)
    );''')
    
    conn.commit()
    conn.close()



def update_values(data): 
    print('updating...')
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    
    new_values = [tuple(row) for row in data.itertuples(index=False)]
    c.executemany('INSERT INTO base (name, event_date, location, facebook, link, aangeboden, verkocht, gezocht, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);', new_values)

    conn.commit()
    conn.close()

driver = get_driver()
print(driver)
create()
data = scrape(links())
update_values(data)