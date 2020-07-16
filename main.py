from find_links import *
from scrape import *
from database import *
from update_db import *
from database import *
import numpy as np
import pandas as pd

# fetch list of links to scrape
links = links()

# append data from pages
data = scrape(links)

# update database
update_database(data)