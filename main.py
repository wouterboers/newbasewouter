#!/usr/bin/env python
#

import webapp2
import json
import cgi
from google.appengine.ext.webapp.util import run_wsgi_app
import MySQLdb
import os
import logging


def getDb():
    env = os.getenv('SERVER_SOFTWARE')
    if (env and env.startswith('Google App Engine/')):
        # Connecting from App Engine
        db = MySQLdb.connect(
            unix_socket='/cloudsql/newbase-wouter:database',
            user='root',
            db='newbase')
    else:
        db = MySQLdb.connect(
            host='173.194.228.207',
            port=3306,
            user='root',
            passwd='abarth2009',
            db='newbase')
    return db


class MainHandler(webapp2.RequestHandler):
    def get(self):
        # for now direct SQL queries, in the future use django as ORM
        db = getDb();
        cursor = db.cursor()
        cursor.execute('SELECT * from projects')
        output = []
        for row in cursor.fetchall():
            output.append(dict([('id', row[0]),
                                ('name', cgi.escape(row[1]))
            ]))

        self.response.content_type = 'text/json'
        self.response.write(output)
        # other response stuff? https://webapp-improved.appspot.com/guide/response.html

    def post(self):
        name = self.request.get('name')
        logging.info('Inserting project named ' + name)

        db = getDb();
        cursor = db.cursor()
        cursor.execute('INSERT INTO projects (name) VALUES (%s)', [name])
        db.commit()
        db.close()

    def put(self):
        key = int(self.request.get('id'))
        name = self.request.get('name')
        logging.info('Updating project id' + str(key))
        db = getDb();
        cursor = db.cursor()
        cursor.execute('UPDATE projects SET name = (%s) WHERE id = (%s)', [name, key])
        db.commit()
        db.close()

class Projects(webapp2.RequestHandler):
    def delete(self, id):
        logging.info('Deleting project id' + str(id))
        db = getDb();
        cursor = db.cursor()
        response = cursor.execute('DELETE FROM projects WHERE id = (%s)', [id])
        db.commit()
        db.close()
        if response == 0:
            self.response.set_status(404)
            self.response.write(response)
        else:
            self.response.write(response)

    def get(self, id):
        logging.info('Deleting project id' + str(id))



# webapp2: https://webapp-improved.appspot.com/index.html
app = webapp2.WSGIApplication([
                                  ('/', MainHandler),
                                  ('/projects/(\d+)', Projects)
                              ], debug=True)