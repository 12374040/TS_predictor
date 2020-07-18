import json
import time
import requests
import lxml.html
import numpy as np
import pandas as pd
import pyodbc
from datetime import datetime
from find_links import *

def scrape():
    data = []
    timestamp = datetime.now(tz=None).strftime("%Y/%m/%d %H:%M:%S")

    conn = pyodbc.connect(access)
    c = conn.cursor()

    link_to_check = c.execute('SELECT link FROM link_data')
    for link in link_to_check:
        print(link)
        doc = lxml.html.fromstring(requests.get(link).content)

        event_data = dict()
        event_data['name'] = doc.xpath('//*[@id="__next"]/div[1]/div[1]/div[2]/a/h1/text()')[0]

        try:
            event_data['aangeboden'] = int(doc.xpath('//*[@id="__next"]/div[1]/div[1]/div[2]/div[2]/div[1]/span/span[1]/text()')[0])
            event_data['verkocht'] = int(doc.xpath('//*[@id="__next"]/div[1]/div[1]/div[2]/div[2]/div[2]/span/span[1]/text()')[0])
            event_data['gezocht'] = int(doc.xpath('//*[@id="__next"]/div[1]/div[1]/div[2]/div[2]/div[3]/span/span[1]/text()')[0])
        except:
            print(link + ':data not found!')
            continue

        event_data['event_date'] = doc.xpath('//*[@id="__next"]/div[1]/div[1]/div[2]/div[3]/div[1]/text()')[0]
        
        event_data['timestamp'] = timestamp

        data.append(event_data)

    data = pd.DataFrame(data)

    return data
