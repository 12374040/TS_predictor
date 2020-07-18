import sys
import time
import requests
import lxml.html
from update_db import update_links
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def get_driver():
    '''Detecteerd OS en past chromedriver aan'''
    platforms = {
        'linux' : './chromedriver',
        'win32' : 'chromedriver.exe'
    }
    if sys.platform not in platforms:
        return sys.platform
    
    return platforms[sys.platform]

def links():
    '''Verzamelt links van de ticketswap festival pagina'''
    options = Options()
    options.headless = True
    chromedriver = webdriver.Chrome(get_driver(), options=options)
    chromedriver.get('https://www.ticketswap.nl/festivals')
    xpath = []
    links = []
    events = []
    is_event = '/event/'


    # klikt op de 'laat meer zien' knop tot alle evenementen vertoond worden
    t = 0
    # while True:
    #     try:
    #         chromedriver.find_element(By.XPATH, '//h4[text()="Laat meer zien"]').click()
    #         time.sleep(0.5)
    #     except:
    #         break


    # append alle links op pagina
    xpath.extend(chromedriver.find_elements(By.XPATH, '//a'))

    for x in xpath:
        links.append(str(x.get_attribute("href")))# append link naar list

    chromedriver.close()

    # filtert op links die naar evenementpagina's verwijzen
    events = [x for x in links if is_event in x]
    
    print('{} links found'.format(len(events)))
    
    get_link_data(events)

def get_link_data(links):
    link_list = []

    for link in list(set(links)):
        print(link)
        doc = lxml.html.fromstring(requests.get(link).content)

        link_data = {
            'name':'',
            'event_date':'',
            'location':'',
            'city':'',
            'country':'',
            'facebook':'',
            'link':''
        }
        link_data['name'] = doc.xpath('//*[@id="__next"]/div[1]/div[1]/div[2]/a/h1/text()')[0]
        try:
            doc.xpath('//*[@id="__next"]/div[1]/div[1]/div[2]/div[2]/div[3]/span/span[1]/text()')[0]
        except:
            print(link + ':data not found!')
            continue
        
        link_data['event_date'] = doc.xpath('//*[@id="__next"]/div[1]/div[1]/div[2]/div[3]/div[1]/text()')[0]
        link_data['location'] = doc.xpath('//*[@id="__next"]/div[1]/div[1]/div[2]/div[3]/div[2]/span[2]/a[1]/text()')[0]
        link_data['city'] = doc.xpath('//*[@id="__next"]/div[1]/div[1]/div[2]/div[3]/div[2]/span[2]/a[2]/text()')[0]
        link_data['country'] = doc.xpath('//*[@id="__next"]/div[1]/div[1]/div[2]/div[3]/div[2]/span[2]/text()[2]')[0][2:]

        try:
            link_data['facebook'] = doc.xpath('//*[@id="__next"]/div[1]/div[1]/div[2]/div[1]/div/a')[0].get("href")
        except:
            link_data['facebook'] = 'Nan'

        link_data['link'] = link

        link_list.append(link_data)

    link_list = pd.DataFrame(link_list)
    update_links(link_list)
