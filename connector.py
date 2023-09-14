import mysql.connector
import os
import gpxpy

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
            track = self.execute_query(query, False, (filename,))
            if len(track) > 0:
                continue
            track_counter += 1
            metadata = filename.split("_")
            nickname = metadata[0]
            license = metadata[1]

            query = "SELECT * FROM person WHERE(nick = %s)"
            person = self.execute_query(query, False, (nickname,))
            if not(len(person) > 0):
                query = "INSERT INTO person(nick) VALUES(%s)"
                pid = self.execute_query(query, True, (nickname,))
            else:
                pid = person[0][0]
            
            query = "SELECT * FROM fahrzeug WHERE(polkz = %s)"
            vehicle = self.execute_query(query, False, (license,))
            if not(len(vehicle) > 0):
                query = "INSERT INTO fahrzeug(polkz) VALUES(%s)"
                fzid = self.execute_query(query, True, (license,))
            else:
                fzid = vehicle[0][0]

            with open(os.path.join(path, filename)) as file:
                gpxfile = file.read()
                gpx = gpxpy.parse(gpxfile)
                for track in gpx.tracks:
                    query = "INSERT INTO track(dateiname, pid, fzid) VALUES(%s, %s, %s)"
                    tid = self.execute_query(query, True, (filename, pid, fzid))
                    
                    for segment in track.segments:
                        for point in segment.points:
                            query = "INSERT INTO punkt(lat, lon, ele, dt, tid) VALUES(%s, %s, %s, %s, %s)"
                            self.execute_query(query, True, (point.latitude, point.longitude, point.elevation, point.time, tid))
                            point_counter += 1

        return [track_counter, point_counter]

    def execute_query(self, query, commit, data):
        connection = mysql.connector.connect(**self.config)
        cursor = connection.cursor(prepared = True)
        if data:
            cursor.execute(query, data)
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