import json
import time
import numpy as np
import pandas as pd
import requests
import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver

ticket_features = ['aangeboden', 'verkocht', 'gezocht']
event_features = ['category', 'city', 'location', 'name', 'ticket']

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
    ticket_data = {ticket_features[i] : ticket_data[i].span.text for i in range(len(ticket_data))}
    
    return ticket_data
    
def collect_event_data(soup):
    # find data and put it in dict
    event_data = str(soup.find_all("script", { "type" : "application/ld+json"})[0].string)
    event_data = json.loads(''.join([event_data[i] for i in range(len(event_data)) if event_data[i] != "\n"]))
    
    # structuring dict
    event_data = {event_features[i] : event_data['itemListElement'][i]['item']['name'] for i in range(len(event_data['itemListElement']))}
    
    return event_data


def find_links():
    driver = webdriver.Chrome('chromedriver.exe')
    driver.get('https://www.ticketswap.nl/festivals')
    time.sleep(5)

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


def scrape(links):
    data = []
    for link in links:
        data.append(collect_data(link))
    
    return data

links = find_links()
data = scrape(links)
print(pd.DataFrame(data))





