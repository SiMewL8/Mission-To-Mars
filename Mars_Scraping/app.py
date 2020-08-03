from flask import Flask, render_template
from flask_pymongo import PyMongo
import scraping


app = Flask(__name__)

# flask_pymongo to connect/modify to mongo db

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"

# Uniform Resource Identifier(tell python app connects to Mongo using URI, akin to URL)
# the url identifies how to reach mongo


mongo = PyMongo(app)

@app.route('/')
# home page

def index():
# index.html

    mars = mongo.db.mars.find_one()
#    uses pymongo to find mars collection in our current db (mars_app)

    return render_template("index.html", mars=mars)
#    returns an html template, python uses mars collection in mongodb

# links visual representation of web app to the code

@app.route("/scrape")

def scrape():
    
    mars = mongo.db.mars
#     access mongodb

    mars_data = scraping.scrape_all()
#     scrape new(current) data from scraping.py and holds it

    mars.update({}, mars_data, upsert=True)
#     update(insert new data) db, upsert creats new document if not already
    
    return "Scraping Successful!!"


# run flask
if __name__ == "__main__":
   app.run()




    