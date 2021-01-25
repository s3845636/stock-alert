from flask import Flask, render_template
from flask_login import LoginManager
from google.cloud import firestore

# initialising Flask app
app = Flask(__name__)



# Registering Blueprints
from cover.cover import cover
app.register_blueprint(cover, url_prex="")
from login.login import login
app.register_blueprint(login, url_prefix="/login")
from home.home import home
app.register_blueprint(home, url_prefix="/home")
from signup.signup import signup
app.register_blueprint(signup, url_prefix='/signup')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)

