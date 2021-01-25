from flask import Blueprint, render_template, request, redirect, url_for, session
from google.cloud import datastore


# INITIALISE DATASTORE
datastore_client = datastore.Client()

# Blueprint constructor
home = Blueprint("home", __name__, static_folder="static", static_url_path="/static", template_folder="templates")


#After successfully logged in. Have to use 'home' in stead 'main.py' is reserved for Datastore connection.
@home.route("/", methods=['GET','POST'])
def home_user():

    full_name = ''
    # Get user id from the url
    url = request.args.get('id')

    # # Retrieve data of an user with the id collected from the url
    # key = datastore_client.key("user", url)
    # full_name = datastore_client.get(key)['name']
    
    # # Direct to either change name or change password page
    # if request.method == 'POST':
    #     if request.form.get("submit_name"):
    #         return redirect(url_for('name.name_user', id = url))
    #     elif request.form.get("submit_password"):
    #         return redirect(url_for('password.password_user', id = url))


    # return render_template("home.html", full_name = full_name, id = url)
    return render_template("home.html", full_name = url.capitalize() )