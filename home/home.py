from flask import Blueprint, render_template, request, redirect, url_for, session
from google.cloud import firestore
from newsapi import NewsApiClient
import json

#API TOKEN
NEWSAPI_KEY = '4be2b00fc468417f983a710b30edd6ce'


# INITIALISE Firestore
db = firestore.Client()

# Blueprint constructor
home = Blueprint("home", __name__, static_folder="static", static_url_path="/static", template_folder="templates")

# Init
newsapi = NewsApiClient(api_key= NEWSAPI_KEY)


#After successfully logged in. Have to use 'home' in stead 'main.py' is reserved for Datastore connection.
@home.route("/")
def home_user():

    full_name = ''
    stock_list = []

    # Get user id from the url
    url = request.args.get('id')

    #  Read data from collection user and document from input_id
    users = db.collection(u'users').document(url)
    user = users.get()
    full_name = user.to_dict()['name'].capitalize()
    

    #  Read stocks data
    stocks = db.collection(u'users').document(url).collection(u'stocks').stream()
    for stock in stocks:
        stock_list.append(stock.to_dict())
    

    # /v2/top-headlines
    top_headlines = newsapi.get_top_headlines(q='apple', country='us')
    
    
    return render_template("home.html", full_name = full_name, stock_list = stock_list, url = url)



@home.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for('cover.cover_page'))


@home.route("/stocks")
def show():
    #  Read data from collection user and document from input_id
    # users = db.collection(u'users').document(url)
    # user = users.get()
    stock = request.args.get('stock') 

    return render_template("home.html", stock = stock )