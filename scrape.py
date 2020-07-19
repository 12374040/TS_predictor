import json
import time
import requests
import lxml.html
import numpy as np
import pandas as pd
import mysql.connector
from datetime import datetime
from find_links import *
from database import *

def scrape():
    print('Scraping...')
    data = []
    # timestamp = datetime.now(tz=None).strftime("%Y/%m/%d %H:%M:%S")

    conn = mysql.connector.connect(**access)
    c = conn.cursor()

    c.execute('SELECT link,ID FROM link_data')
    link_to_check = [row for row in c]
    
    for link in link_to_check:
        go_link = link[0]
        doc = lxml.html.fromstring(requests.get(go_link).content)

        event_data = dict()
        event_data['ID'] = link[1]

        try:
            event_data['aangeboden'] = int(doc.xpath('//*[@id="__next"]/div[1]/div[1]/div[2]/div[2]/div[1]/span/span[1]/text()')[0])
            event_data['verkocht'] = int(doc.xpath('//*[@id="__next"]/div[1]/div[1]/div[2]/div[2]/div[2]/span/span[1]/text()')[0])
            event_data['gezocht'] = int(doc.xpath('//*[@id="__next"]/div[1]/div[1]/div[2]/div[2]/div[3]/span/span[1]/text()')[0])
        except:
            print(link + ':data not found!')
            continue
        
        if event_data['aangeboden'] is not 0:
            try:
                event_data['laagste_prijs'] = (doc.xpath('/html/body/div[1]/div[2]/div[2]/ul/li[1]/a/div/div/div/footer/strong/text()')[0])
            except:
                event_data['laagste_prijs'] = 'NaN'
        else:
            event_data['laagste_prijs'] = '0'
        
        # event_data['timestamp'] = timestamp
        
        data.append(event_data)

    data = pd.DataFrame(data)

    return data
