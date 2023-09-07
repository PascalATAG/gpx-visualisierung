import mysql.connector
import os

class MySQLConnector:
    def __init__(self, user, password, host, database):
        self.config = {
            'user': user,
            'password': password,
            'host': host,
            'database': database
        }

    def import_files():
        path = '../gpx-tracks'
        for filename in os.listdir(path):
            with open(os.path.join(path, filename), "r") as file:
                file_content = file.read()
                metadata = filename.split("_")
                nickname = metadata[0]
                license = metadata[1]

    def execute_query(self, query, commit, data):
        connection = mysql.connector.connect(**self.config)
        cursor = connection.cursor(prepared = True)
        if data:
            cursor.execute(query, data)
        else:
            cursor.execute(query)
        if commit:
            connection.commit()
        result = cursor.fetchall()
        cursor.close()
        connection.close()
        return result