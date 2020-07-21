import sys
import time
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
    #t = 0
    #while True:
    #    try:
    #        chromedriver.find_element(By.XPATH, '//h4[text()="Laat meer zien"]').click()
    #        time.sleep(0.5)
    #    except:
    #        break


    # append alle links op pagina
    xpath.extend(chromedriver.find_elements(By.XPATH, '//a'))

    for x in xpath:
        links.append(str(x.get_attribute("href")))# append link naar list

    chromedriver.close()

    # filtert op links die naar evenementpagina's verwijzen
    events = [x for x in links if is_event in x]
    
    print('{} links found'.format(len(events)))
    print('scraping...')
    return events
