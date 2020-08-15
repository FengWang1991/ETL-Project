#!/usr/bin/env python
# coding: utf-8

# In[12]:


# dependencies and setup 
from bs4 import BeautifulSoup
import pandas as pd
from splinter import Browser
import time
from tqdm import tqdm


# In[26]:


# create a browser instance using splinter (FOR MAC) 
# executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
# browser = Browser('chrome', **executable_path, headless=False)
# time.sleep(1)

# For Windows 
executable_path = {'executable_path': 'driver/chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)


# In[27]:


# visit the Steamdb ratings url 
steam_ratings_url = 'https://steamdb.info/stats/gameratings/'
browser.visit(steam_ratings_url)
time.sleep(3)


# In[30]:


# create HTML object
html = browser.html

# parse HTML with BeautifulSoup 
soup = BeautifulSoup(html, 'html.parser')


# In[38]:


# # show top 5000 highest-rated games on Steam (log in is required)
browser.find_by_css('select[name=table-apps_length]').click()
browser.find_by_css('option[value="-1"]').click()
time.sleep(5)


# In[33]:


# create a new soup object with the resulting html after showing all rows
allrows_html = browser.html
newsoup = BeautifulSoup(allrows_html, 'html.parser')


# In[34]:


# get all rows in the top rated games table with a class of 'app'
all_trs = newsoup.find_all('tr', class_='app')

# create a base url to append to the game url
base_url = 'https://steamdb.info'

# create an empty list to append each game's info
game_ratings = []

# for loop to iterate over each row and retrieve game data (tqdm for progress-bar)
for tr in tqdm(all_trs):
    
    # get all columns in each row
    td_tags = tr.find_all('td')
    
    # get the game title located in column 3 (index 2)
    game_name = td_tags[2].text
    
    # get the game url located in column 2 (index 1) and append to the base url to complete it
    url = td_tags[1].find('a')['href']
    game_url = base_url + url
    
    # get the game rating located in column 6 (index 5)
    steam_rating = td_tags[5].text
    
    # create a dictionary of the retrieved values and append to list
    game_ratings.append({'game_name':game_name,
                         'game_url':game_url,
                         'steam_rating':steam_rating
                        })

print("Scraping Complete")


# In[35]:


game_ratings_df = pd.DataFrame(game_ratings)
game_ratings_df


# In[37]:


# Export the DataFrame to csv file
game_ratings_df.to_csv("data/Steam_games_ratings.csv")

