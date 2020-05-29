import json
import time
import copy
import sqlite3
import requests
import urllib.request
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from datetime import datetime


def scrape(links):
    data = []
    for link in links:
        data.append(collect_data(link))
    
    features = ['aangeboden', 'verkocht', 'gezocht', 'name']
    
    data = pd.DataFrame(data).fillna(0)
    data.loc[:, ['aangeboden', 'verkocht', 'gezocht']] = data.loc[:, ['aangeboden', 'verkocht', 'gezocht']].astype('int')
    
    return data



def find_links():
    driver = webdriver.Chrome('chromedriver.exe')
    driver.get('https://www.ticketswap.nl/festivals')
    time.sleep(4)

    x = 6
    while True:
        try:
            driver.find_element_by_xpath('//*[@id="__next"]/div[3]/div/div/div[{}]/button'.format(x)).click()
            time.sleep(2)
            x+= 12
        except:
            break

    i = 1
    links = []
    while True:
        try:
            links.append(driver.find_element_by_xpath('//*[@id="__next"]/div[3]/div/div/div[{}]/a'.format(i)).get_attribute("href"))
            i+= 1
        except: 
            break
    
    return links



def collect_data(url):
    request = requests.get(url)
    soup = BeautifulSoup(request.text, features="html.parser")
    ticket_data = collect_ticket_data(soup)
    event_data = collect_event_data(soup)

    return {**ticket_data, **event_data} 
    
    
    
def collect_ticket_data(soup):
    # find data
    ticket_data = soup.find_all("span", { "class" : "css-v0hcsa e7cn512" })
    
    # structuring dict
    ticket_data = {features[i] : ticket_data[i].span.text for i in range(len(ticket_data))}
    
    return ticket_data
    
    
    
def collect_event_data(soup):
    # find data and put it in dict
    event_data = str(soup.find_all("script", { "type" : "application/ld+json"})[0].string)
    event_data = json.loads(''.join([event_data[i] for i in range(len(event_data)) if event_data[i] != "\n"]))

    event_data = {'name' : event_data['itemListElement'][3]['item']['name']}
    
    return event_data



def create():
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    
    hours = ", ".join(['hour'+str(i) + " int default 0" for i in range(24)])
    c.execute("CREATE TABLE IF NOT EXISTS base (name varchar(255) PRIMARY KEY, aangeboden int, verkocht int, gezocht int, " + hours + ');')
    
    conn.commit()
    conn.close()



def difference():    
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    
    old_base = pd.read_sql_query('SELECT name, aangeboden, verkocht FROM base;', conn)
    difference = data.loc[:, ['aangeboden', 'verkocht']] - old_base.loc[:, ['aangeboden', 'verkocht']]
    difference['change'] = difference['aangeboden'] - difference['verkocht']
    difference['name'] = data.loc[:, 'name']
    
    conn.commit()
    conn.close()
    
    return difference.dropna()



def update_values():    
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    
    new_values = [tuple(row) for row in data.loc[:, ['name', 'aangeboden', 'verkocht', 'gezocht']].itertuples(index=False)]
    c.executemany('REPLACE INTO base (name, aangeboden, verkocht, gezocht) VALUES (?, ?, ?, ?);', new_values)

    conn.commit()
    conn.close()



def update_change():
    conn = sqlite3.connect('test.db')
    c = conn.cursor()

    change = [x for x in difference.loc[:, 'change']]
    names = [x for x in difference.loc[:, 'name']]
    
    insert = []
    for name, change in zip(names, change):
        insert.append((change, name))
    
    hour = 'hour' + str(datetime.now().hour)
    query = "UPDATE base SET {} = {} + ? WHERE name = ?;".format(hour, hour)
    
    c.executemany(query, insert)
    
    conn.commit()
    conn.close()



features = ['aangeboden', 'verkocht', 'gezocht', 'name']
data = scrape(find_links())
create()
difference = difference()
update_values()
update_change()


def print_database():
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    hours = [str(x) for x in range(24)]
    cols = ['name', 'aangeboden', 'verkocht', 'gezocht']
    for h in hours:
        cols.append(h)
    print(pd.DataFrame(c.execute('SELECT * FROM base;'), columns = cols))

    conn.commit()
    conn.close()

print_database()