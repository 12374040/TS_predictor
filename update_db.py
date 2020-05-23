import json
import time
import sqlite3
import numpy as np
import pandas as pd
import requests
import urllib.request
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver


def scrape(links):
    data = []
    for link in links:
        data.append(collect_data(link))
    
    return pd.DataFrame(data)



def find_links():
    driver = webdriver.Chrome('chromedriver.exe')
    driver.get('https://www.ticketswap.nl/festivals')
    time.sleep(4)

    #x = 6
    #while True:
     #   try:
      #      driver.find_element_by_xpath('//*[@id="__next"]/div[3]/div/div/div[{}]/button'.format(x)).click()
       #     time.sleep(2)
        #    x+= 12
        #except:
         #   break

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



def update_db():    
    conn = sqlite3.connect('test.db')
    c = conn.cursor()


    c.execute('CREATE TABLE IF NOT EXISTS base (name varchar(255), aangeboden int, verkocht int, gezocht int);')
    c.execute('CREATE TABLE IF NOT EXISTS change (name varchar(255), change int, hour int);')

    old = pd.read_sql_query('SELECT name, aangeboden, verkocht, gezocht FROM base;', conn)

    difference = data - old.loc[:, ['aangeboden', 'verkocht', 'gezocht']]
    difference['name'] = data['name']
    difference['change'] = difference['aangeboden'] - difference['gezocht']
    difference['hour'] = datetime.now().hour
    change_values = [row for row in difference.loc[:, ['name', 'change', 'hour']].itertuples(index=False)]
    c.executemany('INSERT INTO change (name, change, hour) VALUES (?,?,?);', change_values)


    c.execute('DELETE FROM base;')
    base_values = [tuple(row) for row in data.itertuples(index=False)]
    c.executemany('INSERT INTO base (name, aangeboden, verkocht, gezocht) VALUES (?,?,?,?);', base_values)


    base_query = pd.read_sql_query('SELECT * FROM base;', conn)
    change_query = pd.read_sql_query('SELECT * FROM change;', conn)
    print(base_query)
    print()
    print(change_query)

    conn.commit()
    conn.close()

features = ['aangeboden', 'verkocht', 'gezocht', 'name']
data = scrape(find_links())
data = data.fillna(0)
data.loc[:, ['aangeboden', 'verkocht', 'gezocht']] = data.loc[:, ['aangeboden', 'verkocht', 'gezocht']].astype('int')

update_db()