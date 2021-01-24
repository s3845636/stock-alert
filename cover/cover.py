from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from google.cloud import firestore
import datetime

cover = Blueprint("cover", __name__, static_folder="static", static_url_path="/static", template_folder="templates")


@cover.route("/")
def cover_page():
    now = datetime.datetime.now()
    return render_template("index.html", year = now.year)