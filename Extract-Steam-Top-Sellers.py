#!/usr/bin/env python
# coding: utf-8

# ### Initial setup
# * Libraries
# * Splinter Browser config

# In[1]:


from bs4 import BeautifulSoup as bs
import pandas as pd
from splinter import Browser
import time
from tqdm import tqdm


# In[2]:


# Windows
# executable_path = {"executable_path": "driver/chromedriver.exe"}
# browser = Browser("chrome", **executable_path)


# In[3]:


# MAC
executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)


# ### Initial Scraping
# This section of code scrapes data for the first page of the website. We noted the below:
# * The website shows all games by infinitely scrolling. We worked around this limitation by inspecting the HTML and finding the pagination div tag.
# * The first page has 50 rows of games and the consequent pages have 25 rows each.
# * However, the 50 rows in  Page 1 include the 25 rows from Page 2 i.e. Page 1 displays games of BOTH Page 1 and Page 2 combined.
# * The game_name, release_date and price are scraped from the 50 rows.
# * After scraping data from this page, we get the URL of Page 3 and use splinter to visit that page to continue scraping. Since Page 1 does not display page numbers, we also retrieve the last page number from Page 3's HTML to use in the for loop coming up.

# In[4]:


# Visit the top sellers section on the Steam store using splinter
url="https://store.steampowered.com/search/?filter=topsellers"
browser.visit(url)
time.sleep(2)

# Get the html of the page and create a BeautifulSoup object
html = browser.html
soup = bs(html, 'html.parser')


# In[5]:


# Create an empty list to append game info
top_sellers = []

# Start the result counter at zero
result_count = 0

# Get the parent div for each game row
results=soup.find_all("div",class_="responsive_search_name_combined")

# Loop over the rows and retrieve game data for the first 50 games
for result in results:
        
    # get the game title
    game_name = result.find("span",class_="title").text
        
    # get the release date
    release_date = result.find("div",class_="col search_released responsive_secondrow").text
        
    # get the price
    price = result.find("div",{"class":["col search_price responsive_secondrow","col search_price discounted responsive_secondrow"]}).text.strip()
        
    # add the key value pairs to python dictionary and append to the list
    top_sellers.append({"game_name": game_name,
                        "release_date": release_date,
                        "price": price })
    
    # increase counter once each result is processed
    result_count += 1


# In[6]:


print(result_count)


# In[7]:


# After the initial scraping, find the pagination parent div on the main page and get the url for page 3 
pagination_div = soup.find('div', class_='search_pagination_right')
page_3_url = pagination_div.find_all('a')[1]['href']

# use splinter to proceed to the url
browser.visit(page_3_url)
time.sleep(2)       
    
# Create a new soup object out of the new html
newhtml = browser.html
newsoup = bs(newhtml, 'html.parser')

# get max page number from the pagination parent div
pagination_div = newsoup.find('div', class_='search_pagination_right')
max_pages = int(pagination_div.find_all('a')[-2].text)


# ### Scraping
# * This section of code goes into a nested for loop for scraping data and will take about **9-11 minutes** to complete.
# * The scraped data is appended to the top_sellers list as a dictionary.
# * We find the next page url and use splinter to visit the url after each page loop.
# 

# In[8]:


page_num = 2

# Loop over each page to scrape until we hit the total number of pages (-2 as we have already scraped p1 & p2)
# tqdm is a progress bar module that tracks progress of a loop
for i in tqdm(range(0, max_pages-2)):
    
    # Create a new soup object out of the new html
    html = browser.html
    soup = bs(html, 'html.parser')  
    
    # get the parent div for each game row
    results=soup.find_all("div",class_="responsive_search_name_combined")

    # loop over each row (25 rows in each page) and retrieve game data
    for result in results:
        
        # get the game title
        game_name = result.find("span",class_="title").text
        
        # get the release date
        release_date = result.find("div",class_="col search_released responsive_secondrow").text
        
        # get the price
        price = result.find("div",{"class":["col search_price responsive_secondrow","col search_price discounted responsive_secondrow"]}).text.strip()
        
        # add the key value pairs to python dictionary and append to the list
        top_sellers.append({"game_name": game_name,
                            "release_date": release_date,
                            "price": price })
        
        # increase counter for results once each result is processed
        result_count += 1
        
    # increase counter for page number once each page is processed
    page_num +=1
        
    if page_num != max_pages:
        # After scraping the 25 results, find the pagination parent div
        pagination_div = soup.find('div', class_='search_pagination_right')
            
        # get the next page url from the second active page link with a class of 'pagebtn' 
        next_page_url = pagination_div.find_all('a', class_='pagebtn')[1]['href']
            
        # use splinter to proceed to the next page's url
        browser.visit(next_page_url)
        time.sleep(1)     
        
    else:
        print(f"Last page (p. {page_num}) reached - no more pages to scrape.")
        break

    
print(f'Scraping Complete! {result_count} top-selling games scraped.')


# In[9]:


print(max_pages)


# In[10]:


# Check list of results
for top in range(len(top_sellers)):
    print(f"{top}. {top_sellers[top]['game_name']} | {top_sellers[top]['release_date']} |          {top_sellers[top]['price']}")


# In[11]:


# Create a dataframe with all the information
top_sellers_df = pd.DataFrame(top_sellers)
top_sellers_df


# In[12]:


# Save dataframe into csv file for reading in transform stage
top_sellers_df.to_csv("data/Steam_top_sellers.csv")

