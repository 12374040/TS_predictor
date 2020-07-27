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
    timestamp = datetime.now(tz=None).strftime("%Y-%m-%d %H:%M:%S")

    conn = mysql.connector.connect(**access)
    c = conn.cursor()

    c.execute('SELECT link,ID FROM link_data')# TODO add it so that it doesnt search links that have past
    link_to_check = [row for row in c]
    
    for link in link_to_check:
        go_link = link[0]
        doc = lxml.html.fromstring(requests.get(go_link).content)

        event_data = dict()
        event_data['ID'] = link[1]

        try:
            event_data['aangeboden'] = int(doc.xpath('/html/body/div/div[3]/div/div[1]/p[1]/text()')[0])
            event_data['verkocht'] = int(doc.xpath('/html/body/div/div[3]/div/div[2]/p[1]/text()')[0])
            event_data['gezocht'] = int(doc.xpath('/html/body/div/div[3]/div/div[3]/p[1]/text()')[0])
        except:
            print(link)
            print(':data not found!')
            continue
        
        if event_data['aangeboden'] != 0:
            try:
                event_data['laagste_prijs'] = (doc.xpath('/html/body/div/div[4]/div[1]/ul/li/a/div/div/div/footer/strong/text()')[0])
            except:
                event_data['laagste_prijs'] = 'NaN'
        else:
            try:
                event_data['laagste_prijs'] = (doc.xpath('/html/body/div/div[4]/div[2]/ul/li[1]/a/div/div/div/footer/strong/text()')[0])
            except:
                print('not able to get price of last sold ticket')
                print(go_link)
                event_data['laagste_prijs'] = '0'
            
        
        # event_data['timestamp'] = timestamp
        
        data.append(event_data)

    data = pd.DataFrame(data)

    return data
