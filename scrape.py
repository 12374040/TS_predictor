import json
import time
import requests
import lxml.html
import numpy as np
import pandas as pd
from datetime import datetime
from find_links import *

def scrape(links):
    data = []
    timestamp = datetime.now(tz=None).strftime("%Y/%m/%d %H:%M:%S")

    for link in links:
        print(link)
        doc = lxml.html.fromstring(requests.get(link).content)

        event_data = dict()
        event_data['name'] = doc.xpath('//*[@id="__next"]/div[1]/div[1]/div[2]/a/h1/text()')[0]

        try:
            event_data['aangeboden'] = int(doc.xpath('//*[@id="__next"]/div[1]/div[1]/div[2]/div[2]/div[1]/span/span[1]/text()')[0])
            event_data['verkocht'] = int(doc.xpath('//*[@id="__next"]/div[1]/div[1]/div[2]/div[2]/div[2]/span/span[1]/text()')[0])
            event_data['gezocht'] = int(doc.xpath('//*[@id="__next"]/div[1]/div[1]/div[2]/div[2]/div[3]/span/span[1]/text()')[0])
        except:
            continue

        event_data['event_date'] = doc.xpath('//*[@id="__next"]/div[1]/div[1]/div[2]/div[3]/div[1]/text()')[0]
        event_data['location'] = doc.xpath('//*[@id="__next"]/div[1]/div[1]/div[2]/div[3]/div[2]/span[2]/a[1]/text()')[0]
        event_data['city'] = doc.xpath('//*[@id="__next"]/div[1]/div[1]/div[2]/div[3]/div[2]/span[2]/a[2]/text()')[0]
        event_data['country'] = doc.xpath('//*[@id="__next"]/div[1]/div[1]/div[2]/div[3]/div[2]/span[2]/text()[2]')[0][2:]

        try:
            event_data['facebook'] = doc.xpath('//*[@id="__next"]/div[1]/div[1]/div[2]/div[1]/div/a')[0].get("href")
        except:
            event_data['facebook'] = 'Nan'

        event_data['link'] = link
        event_data['timestamp'] = timestamp

        data.append(event_data)

    data = pd.DataFrame(data)

    return data
