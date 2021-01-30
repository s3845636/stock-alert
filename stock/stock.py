from flask import Blueprint, render_template, request, redirect, url_for, session
from google.cloud import firestore
from newsapi import NewsApiClient
import json
import requests
from datetime import datetime, timedelta


#API TOKEN
NEWSAPI_KEY = '4be2b00fc468417f983a710b30edd6ce'

#ALPHA VANTAGE TOKEN
ALPHA_VANTAGE_KEY = 'NL3IT30P23YWL055' 
STOCK_ENDPOINT = 'https://www.alphavantage.co/query'


db = firestore.Client()


stock = Blueprint("stock", __name__, static_folder="static", static_url_path="/static", template_folder="templates")

# Init NEWS API
newsapi = NewsApiClient(api_key= NEWSAPI_KEY)



@stock.route("/", methods=['POST','GET'])
def stock_data():
    daily_prices_dict = {}
    url = request.args.get('id')

    stock_symbol = ''
    stock_name = ''
    stock_desc = ''
    stock_exchange = ''
    stock_country = ''
    stock_sector = ''
    saved = False

    # Check if the request come from the SEARCH BAR or SIDE BAR
    if request.args.get('type') == 'search':
        search_stock = request.form.get('search')
        saved = False
    else:
        search_stock = request.args.get('search')
        saved = True 

    # Get data of the searched stock from API Alpha Vantage  
    # GET Company overviewW
    stock_data = {
    "function": "OVERVIEW",
    "symbol": search_stock,
    "apikey": ALPHA_VANTAGE_KEY }
    
    response = requests.get(STOCK_ENDPOINT, params=stock_data)
    response_json = response.json()
    
    if len(response_json) > 0:  
        stock_symbol = response_json["Symbol"] 
        stock_name = response_json["Name"]
        stock_desc = response_json["Description"]
        stock_exchange = response_json["Exchange"]
        stock_country = response_json["Country"]
        stock_sector = response_json["Sector"]

        stocks = db.collection(u'users').document(url).collection(u'stocks').document(stock_symbol.lower())
        stock = stocks.get()

        # Check if stock existed in database 
        if stock.exists:
            print("Exisited")
            saved = True      
    else:
        data = None

    #  Stock data from Alpha API DAILY
    stock_data_daily = {
        "function": "TIME_SERIES_DAILY",
        "symbol": search_stock,
        "apikey": ALPHA_VANTAGE_KEY
    }

    response_daily = requests.get(STOCK_ENDPOINT, params=stock_data_daily)
    data_daily = response_daily.json()["Time Series (Daily)"]
    

    data_list = [value for (key, value) in data_daily.items()]
    # Closing price of yesterday price
    one_day_before_open = data_list[0]["1. open"]
    one_day_before_high = data_list[0]["2. high"]
    one_day_before_low = data_list[0]["3. low"]
    one_day_before_close = data_list[0]["4. close"]
    # Closing price of the day before yesterday
    two_day_before_open = data_list[1]["1. open"]
    two_day_before_high = data_list[1]["2. high"]
    two_day_before_low = data_list[1]["3. low"]
    two_day_before_close = data_list[1]["4. close"]
    # Calculate the difference

    difference = float(one_day_before_close) - float(two_day_before_close)
    difference_percent = (difference/float(one_day_before_close)) * 100

    if difference < 0:
        performance = "🔴"
    elif difference > 0:
        performance = "🟢"
    else:
        performance = "🟠"

    daily_prices_dict = { \
        "one_day_before_date" : (datetime.now() - timedelta(1)).strftime('%d-%m-%Y'),
        'one_day_before_open' : round(float(one_day_before_open), 2),
        'one_day_before_high' : round(float(one_day_before_high), 2),
        'one_day_before_low' : round(float(one_day_before_low), 2),
        'one_day_before_close' : round(float(one_day_before_close), 2),
        'two_day_before_date' : (datetime.now() - timedelta(2)).strftime('%d-%m-%Y'),
        'two_day_before_open' : round(float(two_day_before_open), 2),
        'two_day_before_high' : round(float(two_day_before_high), 2),
        'two_day_before_low' : round(float(two_day_before_low), 2),
        'two_day_before_close' : round(float(two_day_before_close), 2),
        'difference' : round(float(difference), 2),
        'difference_percent' : round(float(difference_percent), 2),
        'performance' : performance
    }



    # /v2/top-headlines
    all_articles = newsapi.get_everything(q=stock_name,
                                      language='en',
                                      sort_by='relevancy',
                                      page=2)



    daily_news_dict = { \
        "article_one_title" : all_articles['articles'][0]['title'],
        "article_one_author" : all_articles['articles'][0]['author'],
        "article_one_desc" : all_articles['articles'][0]['description'],
        "article_one_url" : all_articles['articles'][0]['url'],
        "article_one_date" : all_articles['articles'][0]['publishedAt'].split('T')[0],
        "article_two_title" : all_articles['articles'][1]['title'],
        "article_two_author" : all_articles['articles'][1]['author'],
        "article_two_desc" : all_articles['articles'][1]['description'],
        "article_two_url" : all_articles['articles'][1]['url'],
        "article_two_date" : all_articles['articles'][1]['publishedAt'].split('T')[0],
        "article_3_title" : all_articles['articles'][2]['title'],
        "article_3_author" : all_articles['articles'][2]['author'],
        "article_3_desc" : all_articles['articles'][2]['description'],
        "article_3_url" : all_articles['articles'][2]['url'],
        "article_3_date" : all_articles['articles'][2]['publishedAt'].split('T')[0],
        "article_4_title" : all_articles['articles'][3]['title'],
        "article_4_author" : all_articles['articles'][3]['author'],
        "article_4_desc" : all_articles['articles'][3]['description'],
        "article_4_url" : all_articles['articles'][3]['url'],
        "article_4_date" : all_articles['articles'][3]['publishedAt'].split('T')[0]     
    }
    print(all_articles['articles'][0]['publishedAt'].split('T')[0])
    return render_template("stock.html", daily_news = daily_news_dict, daily_prices = daily_prices_dict, name=stock_name, symbol=stock_symbol, desc=stock_desc, exchange=stock_exchange, country=stock_country, sector=stock_sector, saved=saved, url = url)



@stock.route("/post", methods=['POST','GET'])
def stock_post():
        
    # Save stock info to database 
        if request.method == 'POST':
            url = request.args.get('id')
            stock_symbol = request.args.get('symbol')
            stock_name = request.args.get('name')
            stock_sector = request.args.get('sector')
            if request.form.get("save_stock"):
                data = {\
                    u'code': stock_symbol,
                    u'name': stock_name,
                    u'sector': stock_sector
                    }
                db.collection(u'users').document(url).collection('stocks').document(stock_symbol.lower()).set(data)
                print(stock_symbol)
                return redirect(url_for('home.home_user', id = url))  

            if request.form.get("delete_stock"):
                db.collection(u'users').document(url).collection('stocks').document(stock_symbol.lower()).delete()
                return redirect(url_for('home.home_user', id = url))
    
       
    
   