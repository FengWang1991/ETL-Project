import pandas as pd
from flask_pymongo import PyMongo
import scrape
from flask import Flask,jsonify
import numpy as np
from flask.json import JSONEncoder

app=Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/steam_db")

@app.route("/")
def scrape_transform():
    game_ratings,top_sellers=scrape.scrape_info()
    clean_data=scrape.transform(game_ratings,top_sellers)

    # Declare the collection
    collection = mongo.db.top_seller_ratings

    # Drop collection to reset database
    collection.drop()

    # Convert pandas dataframe to dictionary for inserting into MongoDB
    data = clean_data.to_dict(orient='records')

    # Insert rows into collection
    collection.insert_many(data)

    game_list=[]
    for x in collection.find({}, {"_id": 0}):
        game_list.append(x)  

    return jsonify(game_list)

if __name__ == "__main__":
    app.run(debug=True)