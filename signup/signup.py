from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from google.cloud import firestore
import datetime
import time



# Blueprint constructor
signup = Blueprint("signup", __name__, static_folder="static", static_url_path="/static", template_folder="templates")

db  = firestore.Client()


@signup.route("/")
def signup_user():
    now = datetime.datetime.now()
    return render_template("signup.html", year = now.year)




@signup.route("/", methods=['POST','GET'])
def signup_post():
    result = ''
    # input_username = ''
    # input_email = ''
    # input_password = ''
    # input_phone = ''


    if request.method == 'POST':  
        input_username = request.form.get('username')
        input_password = request.form.get('password')
        input_email = request.form.get('email')
        input_phone = request.form.get('phone')
        input_fullname = request.form.get('fullname')

    # Read data from collection 'users' check if document existed (compared with input_username)
        users = db.collection(u'users').document(input_username)
        user = users.get()

        if user.exists:
            result = 'Your account is existed, try to log in again'
            time.sleep(1)
            return render_template("signup.html", result = result)
        else:
            # Check if user has used the mail to sign up with different username
            docs = db.collection(u'users').stream()
            for doc in docs:
                if doc.to_dict()['email'] == input_email:
                    result = 'This email has been used to register, please use another email'
                    time.sleep(1)
                    return render_template("signup.html", result = result)

            # get data from form
            data = { \
                u'name': input_fullname.lower(),
                u'email': input_email.lower(),
                u'password': input_password,
                u'phone': input_phone }
            # Add a new doc in collection 'users' with ID from user input_username
            db.collection(u'users').document(input_username.lower()).set(data)
            result = 'You have succesfully created a new account. Log in now.'
            time.sleep(1)
            return render_template("login.html", result = result)

    return render_template("signup.html", result = result)

