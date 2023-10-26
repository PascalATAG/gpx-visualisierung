from flask import Flask, render_template, request, session, redirect, url_for, send_file, request, jsonify, send_from_directory
from connector import MySQLConnector
import analysis

app = Flask(__name__)
app.secret_key = "F"

db = MySQLConnector(user = 'root', password = "", host = "127.0.0.1", database = "gpx_daten")

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

@app.route('/analyse', methods=['GET'])
def analyse():
    tid = request.args.get("id")
    filename = request.args.get("name")
    points = db.get_points(tid)
    detailed_points = db.get_detailed_points(tid)
    speed_and_distance = analysis.speed_and_distance(detailed_points)
    speed, distance, max_speed = speed_and_distance
    elevation = analysis.elevation(detailed_points)
    if elevation:
        avg_elevation, max_elevation = elevation
        return render_template("analysis.html", distance=distance, name=filename, speed=speed, tid=tid, max_speed=max_speed, elevation=avg_elevation, max_elevation=max_elevation)
    else:
        return render_template("analysis.html", distance=distance, name=filename, speed=speed, tid=tid, max_speed=max_speed)

@app.route('/elevation', methods=['GET'])
def elevation():
    tid = request.args.get("id")
    result = db.get_elevation_data(tid)
    return jsonify(result)

@app.route('/images/<path:image_filename>')
def images(image_filename):
    return send_from_directory('./node_modules/leaflet/dist/images', image_filename)