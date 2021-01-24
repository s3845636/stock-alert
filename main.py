from flask import Flask, render_template
from flask_login import LoginManager
from google.cloud import firestore

# initialising Flask app
app = Flask(__name__)



# Registering Blueprints
from login.login import login
app.register_blueprint(login, url_prefix="")
from home.home import home
app.register_blueprint(home, url_prefix="/home")



if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)

