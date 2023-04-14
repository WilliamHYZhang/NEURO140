import flask
import sqlite3


connection = sqlite3.connect("database")

c = connection.cursor()

app = flask.Flask(__name__)

@app.route("/")
def index():
    return flask.render_template("index.html")