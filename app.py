from flask import Flask, render_template, request, session, redirect, url_for, send_file, request, jsonify
from connector import MySQLConnector

app = Flask(__name__)
app.secret_key = "F"

db = MySQLConnector(user = 'root', password = "Zoralias7", host = "127.0.0.1", database = "gpx_daten")

@app.route('/', methods=['GET'])
def index():
    session['user_id'] = 9
    return render_template('index.html', user=True)

@app.route('/import_files', methods=['GET'])
def import_files():
    result = db.import_files()
    return render_template('import_files.html', tracks=result[0], points=result[1])

@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

@app.route('/map', methods=['GET'])
def map():
    tracks = db.get_tracks(session['user_id'])
    return render_template('map.html', tracks=tracks)

@app.route('/leaflet_css')
def leaflet_css():
    file_path = './node_modules/leaflet/dist/leaflet.css'
    return send_file(file_path)

@app.route('/leaflet_js')
def leaflet_js():
    file_path = './node_modules/leaflet/dist/leaflet.js'
    return send_file(file_path)

@app.route('/draw_path', methods=['POST'])
def draw_path():
    data = request.get_json()
    print(data)
    coordinates = db.get_points(data['tid'])
    return jsonify(coordinates)

@app.route('/search', methods=['GET', 'POST'])
def search():
    return render_template('search.html')