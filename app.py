from flask import Flask, render_template, request, session, redirect, url_for
from connector import MySQLConnector

app = Flask(__name__)
app.secret_key = "F"

db = MySQLConnector(user = 'root', password = "Zoralias7", host = "127.0.0.1", database = "gpx_daten")

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/import_files', methods=['GET'])
def import_files():
    return render_template('import_files.html')

@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

@app.route('/map', methods=['GET'])
def map():
    return render_template('map.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    return render_template('search.html')