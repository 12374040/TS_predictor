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
from selenium.webdriver.common.by import By
from datetime import datetime


def get_driver():
    '''Detecteerd OS en past chromedriver aan'''
    platforms = {
        'linux' : './chromedriver',
        'win32' : 'chromedriver.exe'
    }
    if sys.platform not in platforms:
        return sys.platform
    
    return platforms[sys.platform]



def scrape(links):
    '''Haalt informatie uit evenementpagina's via URL'''
    data = []
    for link in links:
        print(link)
        request = requests.get(link)
        soup = BeautifulSoup(request.text, features="html.parser")

        # maakt een dict aan voor de informatie uit de event page
        datapoint = dict()

        # voegt hoeveeheid aangeboden, gevraagde en verkochte tickets toe aan dict
        ticket_soup = soup.find_all("span", { "class" : "css-v0hcsa e7cn512" }) 

        for i, feature in enumerate(['aangeboden', 'verkocht', 'gezocht' ]):
            try:
                datapoint[feature] = int(ticket_soup[i].span.text)
            except:
                datapoint[feature] = np.nan

        # voegt naam van event toe aan dict
        event_json = str(soup.find_all("script", { "type" : "application/ld+json"})[0].string)
        event_soup = json.loads(''.join([event_json[i] for i in range(len(event_json)) if event_json[i] != "\n"]))
        datapoint['name'] = event_soup['itemListElement'][3]['item']['name']
        
        # voegt event datum toe aan dict
        event_date = soup.findAll("div", {"class": "css-102v2t9 ey3w7ki1"})[0].text
        datapoint['event_date'] = event_date.split('}')[-1]

        # voegt locatie toe
        datapoint['location'] = soup.findAll("div", {"class": "css-102v2t9 ey3w7ki1"})[1].text # locatie

        # voegt facebook link toe indien beschikbaar
        try:
            datapoint['facebook'] = soup.find("div", {"class": "css-1fwnys8 e1tolpgy2"}).find('a').get('href')
        except:
            datapoint['facebook'] = 'None'

        # voegt ticketswap link toe
        datapoint['link'] = link


        data.append(datapoint)

    # zet lijst van dicts om naar dataframe
    df = pd.DataFrame(data)

    # voeg het huidige tijdstip toe aan df
    df['timestamp'] = [datetime.now(tz=None).strftime("%Y/%m/%d %H:%M:%S") for i in range(len(df))] 

    return df





def links():
    '''Verzamelt links van de ticketswap festival pagina'''
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(get_driver(), options=options)
    driver.get('https://www.ticketswap.nl/festivals')
    xpath = []
    links = []
    events = []
    is_event = '/event/'

    # klikt op de 'laat meer zien' knop tot alle evenementen vertoond worden
    #t = 0
    #while True:
    #    try:
    #        driver.find_element(By.XPATH, '//h4[text()="Laat meer zien"]').click()
    #        time.sleep(0.5)

    #    except:
    #        print('no load more')
    #        break


    # append alle links op pagina
    xpath.extend(driver.find_elements(By.XPATH, '//a'))

    for x in xpath:
        links.append(str(x.get_attribute("href")))# append link naar list

    driver.close()

    # filtert op links die naar evenementpagina's verwijzen
    events = [x for x in links if is_event in x]
    
    print('{} links found'.format(len(events)))
    print('scraping...')
    return events





def create():
    '''Create db if it does not exist yet'''
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS base (
    aangeboden int, 
    verkocht int, 
    gezocht int, 
    name varchar(255), 
    event_date varchar(255), 
    location varchar(255), 
    facebook varchar(255), 
    link varchar(255),
    timestamp varchar(255)
    );''')
    
    conn.commit()
    conn.close()



def update_values(data): 
    '''Update db with scraped data'''
    print('updating...')
    conn = sqlite3.connect('test.db')
    c = conn.cursor()

    new_values = [tuple(row) for row in data.itertuples(index=False)]

    c.executemany('INSERT INTO base (aangeboden, verkocht, gezocht, name, event_date, location, facebook, link, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);', new_values)

    conn.commit()
    conn.close()

driver = get_driver()
print(driver)
create()
data = scrape(links())
update_values(data)