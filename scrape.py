

# dependencies and setup 
from bs4 import BeautifulSoup as bs
import pandas as pd
from splinter import Browser
import time
from tqdm import tqdm


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    #for windows users
    executable_path = {'executable_path': 'driver/chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=False)
    #For Mac users
    # executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    # return Browser('chrome', **executable_path, headless=False)




def scrape_info():
    browser = init_browser()


# visit the Steamdb ratings url 
    steam_ratings_url = 'https://steamdb.info/stats/gameratings/'
    browser.visit(steam_ratings_url)
    time.sleep(3)




# create HTML object
    html = browser.html

# parse HTML with BeautifulSoup 
    soup = bs(html, 'html.parser')




# # show all highest-rated games on Steam (log in is required)
    browser.find_by_css('select[name=table-apps_length]').click()
    browser.find_by_css('option[value="-1"]').click()
    time.sleep(5)




# create a new soup object with the resulting html after showing all rows
    allrows_html = browser.html
    newsoup = bs(allrows_html, 'html.parser')



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

    


# Visit the top sellers section on the Steam store using splinter
    url="https://store.steampowered.com/search/?filter=topsellers"
    browser.visit(url)
    time.sleep(2)

# Get the html of the page and create a BeautifulSoup object
    html = browser.html
    soup = bs(html, 'html.parser')


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

    return game_ratings,top_sellers

scrape_info()





