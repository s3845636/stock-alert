from flask import Blueprint, render_template, request, redirect, url_for, session
from google.cloud import datastore


# INITIALISE DATASTORE
datastore_client = datastore.Client()

# Blueprint constructor
home = Blueprint("home", __name__, static_folder="static", static_url_path="/static", template_folder="templates")


#After successfully logged in. Have to use 'home' in stead 'main.py' is reserved for Datastore connection.
@home.route("/")
def home_user():

    full_name = ''
    # Get user id from the url
    url = request.args.get('id')
    # return render_template("home.html", full_name = full_name, id = url)

    #Sign out 
    return render_template("home.html", full_name = url.capitalize() )




@home.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for('cover.cover_page'))
