# ETL-Project: Top Seller Steam Game Ratings

Our project looks at the ETL process of the top selling Steam game ratings. We created a separate Jupyter Notebook for each stage.
We also created a Flask API that returns a Jsonified dictionary on Local host.
**Note: Due to large volume of original data source, scraping will take about 10 minutes.**

## Team
Our team consists of:
- Feng Wang
- Olive Sun
- Jaehong Kwon
- XiongFei (Frank) Shi
- Neha Nayeem

## Extract
Original Data Sources: 
1.	Steam official website: https://store.steampowered.com/search/?filter=topsellers
2.	Top rated games on Steam: https://steamdb.info/stats/gameratings/

Steps:
*	Web scraping to extract the top sellers from the first data source and extracted ratings from the second source. 
*	Libraries used: Pandas, BeautifulSoup, Splinter, Time and tqdm(progress bar tracker for loops).
*	Both of the original data sources are in HTML format. We saved the resulting data to DataFrames and then saved as csv files to be used for the transform stage.

Challenges :
First data source (Steam official Website): 
*	This website shows all games by infinitely scrolling. We worked around this limitation by inspecting the HTML and finding the pagination div tag. 
*	We appended our scraped data to the top_sellers list as a dictionary. We then find the next page url and use splinter to visit the url after each page loop.

Second data source (Top rated games on Steam)
* This data sources only shows 200 result without signing in steam. We worked around this challenge by  manually signing in after Browser.Visit(url) step. Note: Sign In is required to get information on all games (37,000 results)

## Transform

Steps:
* 	Read csv files from previous step into DataFrames
*	Merged the two DataFrames on game_name
*	Cleaned the Merged DataFrames by
*	Drop the NA rows (the rows where Release_date were empty)
* Reset Index 
* Formatted the Price columns by using .split() and .replace() to get the regular and discounted price
* Renamed Columns for clarity 
*  Saved as a new csv file for the load stage


## Load
We chose MongoDB for the load stage as our data has an indefinite structure. For example: only some of the games have a discounted price.

Steps:
*	Read csv file from the previous step into a DataFrame 
*	Set up MongoDB connection 
*	Declared Database as steam_db
*	Declared collection top_seller_ratings
*	Converted DataFrame to dictionary called data for inserting into MongoDB
*	Inserted rows into the collection using insert_many(data)
*	Printed results and checked MongoDB to ensure successful loading

## Flask API

Steps:

* Created python files from Jupyter notebooks for the scraping and transforming process
* Created app.py and called Scrape function in the previous step and returned two dictionaries from each data source
* Called the transform function to clean and merge into DataFrames
* Connected to MongoDB and inserted data into database
* Returned Jsonified result in local host






