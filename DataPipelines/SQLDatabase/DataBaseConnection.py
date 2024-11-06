from ..Base.Connection import Connection
import psycopg2
import datetime
import csv

class DatabaseConnection(Connection):
    def __init__(self, credentials, query):
        self.dbname = credentials['dbname']
        self.user = credentials['user']
        self.password = credentials['password']
        self.host = credentials['host']
        self.port = credentials['port']
        self.query = query

    def connect(self):
        self.conn = psycopg2.connect(dbname=self.dbname, user=self.user, password=self.password, host=self.host, port=self.port)
        self.cur = self.conn.cursor()
        self.connectionStartTime = datetime.now()

    def close(self):
        self.cur.close()
        self.conn.close()
        self.connectionEndTime = datetime.now()
        self.connectionDuration = self.connectionEndTime - self.connectionStartTime

    def executeQuery(self, headers=True, read_only=True):
        if read_only:
            # Execute the query without committing
            self.cur.execute(self.query)
        else:
            # Execute the query and commit changes
            self.cur.execute(self.query)
            self.conn.commit()
        
        if headers:
            return self.cur.description, self.cur.fetchall()
        else:
            return self.cur.fetchall()

    def storeSessionData(self, csv_file_path):
        with open(csv_file_path, 'w') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(['Connection Start Time', 'Connection End Time', 'Connection Duration', 'Query'])
            csv_writer.writerow([self.connectionStartTime, self.connectionEndTime, self.connectionDuration, self.query])