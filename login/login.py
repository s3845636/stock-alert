from flask import Blueprint, render_template, request, redirect, url_for, session
from google.cloud import datastore
from google.cloud import firestore
import datetime



# Blueprint constructor
login = Blueprint("login", __name__, static_folder="static", static_url_path="/static", template_folder="templates")

db  = firestore.Client()

docs = db.collection(u'users')


@login.route("/")
def login_user():
    now = datetime.datetime.now()
    a = []
    # a = doc_ref.get()
    # a = a.to_dict()

    a = docs.where(u'name', u'==', u'Louis')
    return render_template("index.html", year = a)
    # return render_template("index.html", year = now.year)




@login.route("/", methods=['POST','GET'])
def login_post():
    result = ''
    db_id = ''
    db_password = ''
    input_id = ''
    input_password = ''

    if request.method == 'POST':
        input_id = request.form.get('username')
        input_password = request.form.get('password')

        # for doc in docs:
        #     if doc.id == input_id:
        #         return redirect(url_for('home.home_user', id = 'admin'))
        #     else:
        #         result = 'User Id or password is invalid!'


        if input_id == 'admin' and input_password == 'admin':
                return redirect(url_for('home.home_user', id = 'admin'))
        else:
            result = 'User Id or password is invalid!'
            
        


        # result = fetch_users(input_id) 
        # No match result from database
        # if result == None:
        #     result = 'User Id or password is invalid!'
        # else:
        #     db_id = result['id']
        #     db_password = result['password']
        #     # Comapre user id and password with the stored data in DataStore
        #     if input_id == db_id and input_password == str(db_password):
        #         result = "Success"
        #         return redirect(url_for('home.home_user', id = db_id))
        #     else:
        #         result = 'User Id or password is invalid!'


    return render_template("index.html", result = result)

