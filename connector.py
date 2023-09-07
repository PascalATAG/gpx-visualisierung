import mysql.connector

class MySQLConnector:
    def __init__(self, user, password, host, database):
        self.config = {
            'user': user,
            'password': password,
            'host': host,
            'database': database
        }

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