import mysql.connector
import os
import gpxpy
from datetime import datetime
import re

class MySQLConnector:
    def __init__(self, user, password, host, database):
        self.config = {
            'user': user,
            'password': password,
            'host': host,
            'database': database
        }

    def import_files(self):
        path = './gpx-tracks'
        track_counter = 0
        point_counter = 0
        for filename in os.listdir(path):
            query = "SELECT * FROM track WHERE(dateiname = %s)"
            track = self.execute_query(query, False, False, (filename,))
            if len(track) > 0:
                continue
            track_counter += 1
            metadata = filename.split("_")
            nickname = metadata[0]
            license = metadata[1]

            query = "SELECT * FROM person WHERE(nick = %s)"
            person = self.execute_query(query, False, False, (nickname,))
            if not(len(person) > 0):
                query = "INSERT INTO person(nick) VALUES(%s)"
                pid = self.execute_query(query, True, False, (nickname,))
            else:
                pid = person[0][0]
            
            query = "SELECT * FROM fahrzeug WHERE(polkz = %s)"
            vehicle = self.execute_query(query, False, False, (license,))
            if not(len(vehicle) > 0):
                query = "INSERT INTO fahrzeug(polkz) VALUES(%s)"
                fzid = self.execute_query(query, True, False, (license,))
            else:
                fzid = vehicle[0][0]

            with open(os.path.join(path, filename)) as file:
                gpxfile = file.read()
                # The time was not formatted correctly for a few files
                gpxfile = re.sub(r'<time>(\d{4}-\d{2}-\d{2})T(\d{2}:\d{2})Z</time>', r'<time>\1T\2:00Z</time>', gpxfile)
                gpx = gpxpy.parse(gpxfile)
                point_data = []
                for track in gpx.tracks:
                    query = "INSERT INTO track(dateiname, pid, fzid) VALUES(%s, %s, %s)"
                    tid = self.execute_query(query, True, False, (filename, pid, fzid))
                    
                    for segment in track.segments:
                        for point in segment.points:
                            point_data.extend(((point.latitude, point.longitude, point.elevation, point.time, tid),))
                            point_counter += 1

                query = "INSERT INTO punkt(lat, lon, ele, dt, tid) VALUES(%s, %s, %s, %s, %s)"
                self.execute_query(query, True, True, point_data)
                                   
        return [track_counter, point_counter]
    
    def get_points(self, tid):
        query = "SELECT lat, lon FROM punkt WHERE(tid = %s)"
        result = self.execute_query(query, False, False, (tid,))
        return result
    
    def get_detailed_points(self, tid):
        query = "SELECT lat, lon, dt, ele FROM punkt WHERE(tid = %s)"
        result = self.execute_query(query, False, False, (tid,))
        return result
    
    def get_elevation_data(self, tid):
        query = "SELECT dt, ele FROM punkt WHERE(tid = %s)"
        result = self.execute_query(query, False, False, (tid,))
        data = {}
        for timestamp, value in result:
            timestamp_str = timestamp.strftime('%Y-%m-%d %H:%M:%S')
            data[timestamp_str] = value
        return data

    def get_nicknames(self):
        query = "SELECT nick FROM person"
        result = self.execute_query(query, False, False, False)
        result_list = [item[0] for item in result]
        return result_list
    
    def get_vehicles(self):
        query = "SELECT polkz FROM fahrzeug"
        result = self.execute_query(query, False, False, False)
        result_list = [item[0] for item in result]
        return result_list

    def search_tracks(self, **params):
        # track_query may get conditions attached at the end of the string
        track_query = "SELECT * FROM track WHERE 1 = 1"
        query_params = []

        user_nick = params.get("user")
        if user_nick != '':
            query = "SELECT pid FROM person WHERE nick = %s"
            user_id = self.execute_query(query, False, False, (user_nick,))[0][0]
            track_query += " AND pid = %s"
            query_params.append(user_id)

        vehicle_license = params.get("vehicle")
        if vehicle_license != '':
            query = "SELECT fzid FROM fahrzeug WHERE polkz = %s"
            vehicle_id = self.execute_query(query, False, False, (vehicle_license,))[0][0]
            track_query += " AND fzid = %s"
            query_params.append(vehicle_id)

        tracks = self.execute_query(track_query, False, False, tuple(query_params))
        time_format = "%Y-%m-%dT%H:%M"
        try:
            start_time = datetime.strptime(params.get("start_time"), time_format)
        except:
            start_time = ''
        try:
            end_time = datetime.strptime(params.get("end_time"), time_format)
        except:
            end_time = ''
        detailed_tracks = []
        for track in tracks:
            query = "SELECT MIN(dt) FROM punkt WHERE(tid = %s)"
            start = self.execute_query(query, False, False, (track[0],))[0][0]
            if start_time != '' and start_time > start:
                continue
            query = "SELECT MAX(dt) FROM punkt WHERE(tid = %s)"
            end = self.execute_query(query, False, False, (track[0],))[0][0]
            if end_time != '' and end_time < end:
                continue
            track = track + (start,)
            track = track + (end,)
            detailed_tracks.append(track)
        
        return detailed_tracks


    def execute_query(self, query, commit, many, data):
        connection = mysql.connector.connect(**self.config)
        cursor = connection.cursor(prepared = True)
        # Many is only used for the large gpx file import
        # Data is used to replace placeholders for prepared statements
        if data and not many:
            cursor.execute(query, data)
        elif data and many:
            cursor.executemany(query, data)
        else:
            cursor.execute(query)
        if commit:
            connection.commit()
            id = cursor.lastrowid
        result = cursor.fetchall()
        cursor.close()
        connection.close()
        try:
            return id
        except:
            return result