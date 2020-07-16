import json
import time
import requests
import urllib.request
import numpy as np
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup


def scrape(links):
    '''Haalt informatie uit evenementpagina's via URL'''
    data = []
    for link in links:
        print(link)
        request = requests.get(link)
        soup = BeautifulSoup(request.text, features="html.parser")

        # maakt een dict aan voor de informatie op de event page
        datapoint = dict()

        # voegt hoeveeheid aangeboden, gevraagde en verkochte tickets toe aan dict
        ticket_soup = soup.find_all("span", { "class" : "css-v0hcsa e7cn512" }) 

        for i, feature in enumerate(['aangeboden', 'verkocht', 'gezocht' ]):
            try:
                datapoint[feature] = int(ticket_soup[i].span.text)
            except:
                datapoint[feature] = 0

        # voegt naam van event toe aan dict
        event_json = str(soup.find_all("script", { "type" : "application/ld+json"})[0].string)
        event_soup = json.loads(''.join([event_json[i] for i in range(len(event_json)) if event_json[i] != "\n"]))
        datapoint['name'] = event_soup['itemListElement'][3]['item']['name']
        
        # voegt event datum toe aan dict
        event_date = soup.findAll("div", {"class": "css-102v2t9 ey3w7ki1"})[0].text
        datapoint['event_date'] = event_date.split('}')[-1]

        # voegt locatie toe
        datapoint['location'] = soup.findAll("div", {"class": "css-102v2t9 ey3w7ki1"})[1].text

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
