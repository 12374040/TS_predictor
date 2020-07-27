from find_links import *
from scrape import *
from database import *
from update_db import *
from database import *
import numpy as np
import pandas as pd

# fetch list of links to scrape
beginurl = 'https://www.ticketswap.nl/festivals'
visited_links = []
gather_links(beginurl, visited_links)

# append data from pages
data = scrape()

# update database
update_database(data)