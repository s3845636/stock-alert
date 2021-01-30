from flask import Blueprint, render_template, request, redirect, url_for, session
from google.cloud import firestore
from newsapi import NewsApiClient
import json
import requests

#API TOKEN
NEWSAPI_KEY = '4be2b00fc468417f983a710b30edd6ce'

#ALPHA VANTAGE TOKEN
ALPHA_VANTAGE_KEY = 'NL3IT30P23YWL055' 
STOCK_ENDPOINT = 'https://www.alphavantage.co/query'

# INITIALISE Firestore
db = firestore.Client()

# Blueprint constructor
home = Blueprint("home", __name__, static_folder="static", static_url_path="/static", template_folder="templates")

# Init
newsapi = NewsApiClient(api_key= NEWSAPI_KEY)
stock_list = []

#After successfully logged in. Have to use 'home' in stead 'main.py' is reserved for Datastore connection.
@home.route("/")
def home_user():
    # Clear list otherwise it will get duplicated after come back from other page
    stock_list.clear()
    full_name = ''

    # Get user id from the url
    url = request.args.get('id')

    #  Read data from collection user and document from input_id
    users = db.collection(u'users').document(url)
    user = users.get()
    full_name = user.to_dict()['name'].capitalize()
    

    #  Read stocks data from GCloud Firestore
    stocks = db.collection(u'users').document(url).collection(u'stocks').stream()
    for stock in stocks:
        stock_name = stock.to_dict()
        if stock_name not in stock_list:
            stock_list.append(stock_name)
            
            #  Stock data from Alpha API DAILY
            stock_data = {
                "function": "TIME_SERIES_DAILY",
                "symbol": stock_name['code'],
                "apikey": ALPHA_VANTAGE_KEY
            }

            response = requests.get(STOCK_ENDPOINT, params=stock_data)
            data = response.json()["Time Series (Daily)"]

            data_list = [value for (key, value) in data.items()]
            # Closing price of yesterday price
            one_day_before_price = data_list[0]["4. close"]
            # Closing price of the day before yesterday
            two_day_before_price = data_list[1]["4. close"]
            # Calculate the difference
            difference = float(one_day_before_price) - float(two_day_before_price)

            if difference < 0:
                performance = "🔴"
            elif difference > 0:
                performance = "🟢"
            else:
                performance = "🟠"

            # stock_name.append({'performance' : performance})
            stock_name['performance'] = performance
            
            
        print(stock_list)

    return render_template("home.html", full_name = full_name, stock_list = stock_list, url = url)



@home.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for('cover.cover_page'))

