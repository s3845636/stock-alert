from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from google.cloud import firestore
import datetime



# Blueprint constructor
login = Blueprint("login", __name__, static_folder="static", static_url_path="/static", template_folder="templates")

db  = firestore.Client()


@login.route("/")
def login_user():
    now = datetime.datetime.now()
    return render_template("login.html", year = now.year)




@login.route("/", methods=['POST','GET'])
def login_post():
    result = ''
    input_id = ''
    input_password = ''


    if request.method == 'POST':
        input_id = request.form.get('username')
        input_password = request.form.get('password')

        # Read data from collection user and document from input_id
        # then check if the user if existed, if yes, compare password
        doc_ref = db.collection(u'users').document(input_id)
        user = doc_ref.get()


        if user.exists:
            if user.to_dict()['password'] == input_password:
                return redirect(url_for('home.home_user', id = user.id))
            else:
                result = "The username or password you entered is incorrect."
        else:
            result = "Your account is not found. Create an account, it's free (:"


    return render_template("login.html", result = result)

