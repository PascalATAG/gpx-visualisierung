from flask import Flask, render_template, request, session, redirect, url_for, send_file, request, jsonify
from connector import MySQLConnector

app = Flask(__name__)
app.secret_key = "F"

db = MySQLConnector(user = 'root', password = "Zoralias7", host = "127.0.0.1", database = "gpx_daten")

@app.route('/', methods=['GET'])
def index():
    return redirect(url_for('map'))

@app.route('/import_files', methods=['GET'])
def import_files():
    result = db.import_files()
    return render_template('import_files.html', tracks=result[0], points=result[1])

@app.route('/map', methods=['GET'])
def map():
    try:
        tracks = session['tracks']
    except:
        tracks = []
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
    coordinates = db.get_points(data['tid'])
    return jsonify(coordinates)

@app.route('/search', methods=['POST'])
def search():
    if request.method == "POST":
        user = request.form.get('user')
        vehicle = request.form.get('vehicle')
        start_time = request.form.get('start-time')
        end_time = request.form.get('end-time')
        tracks = db.search_tracks(user=user, vehicle=vehicle, start_time=start_time, end_time=end_time)
        session['tracks'] = tracks
        return redirect(url_for("map"))
    else:
        return render_template('map.html')

@app.route('/nicknames', methods=['GET'])
def nicknames():
    nicknames = db.get_nicknames()
    return jsonify(nicknames)

@app.route('/vehicles', methods=['GET'])
def vehicles():
    vehicles = db.get_vehicles()
    return jsonify(vehicles)