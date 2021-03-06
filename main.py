#!/usr/bin/env python
#
from __builtin__ import object

import webapp2
import json
import cgi
from google.appengine.ext.webapp.util import run_wsgi_app
import MySQLdb
import os
import logging
import scopes.projects
import jinja2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__) + '/templates'),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


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
        db = getDb()
        cursor = db.cursor()
        cursor.execute('SELECT * from projects')
        output = []
        for row in cursor.fetchall():
            output.append(dict([('id', row[0]),
                                ('name', cgi.escape(row[1])),
                                ('ind_selected', row[2])
            ]))
        self.response.content_type = 'text/json'

        # _object = {
        #     'entry': 'entry',
        #     'number': 12,
        #     'sub': {
        #         'sub1': 'subobject'
        #     }
        #
        # }
        #
        # for i in _object:
        #
        #     # if value is an object, do extra for loop
        #     if type(_object[i]) is dict:
        #
        #         for j in _object[i]:
        #             self.response.write(_object[i][j] + '\n')
        #     else:
        #         self.response.write(str(_object[i]) + '\n')


        self.response.write(json.dumps(output))
        # var = scopes.projects.Projects.test()
        # self.response.write(var)
        # other response stuff? https://webapp-improved.appspot.com/guide/response.html

    def post(self):
        jsonstring = self.request.body
        project = json.loads(jsonstring)
        logging.info('Inserting project named ' + project['name'])

        db = getDb()
        cursor = db.cursor()
        cursor.execute('INSERT INTO projects (name) VALUES (%s)', [project['name']])
        db.commit()
        db.close()

    def put(self):
        jsonstring = self.request.body
        project = json.loads(jsonstring)
        self.response.write(project['id'])
        logging.info('Updating project id' + project['id'])
        db = getDb()
        cursor = db.cursor()
        cursor.execute('UPDATE projects SET name = (%s) WHERE id = (%s)', [project['name'], project['id']])
        db.commit()
        db.close()


class Projects(webapp2.RequestHandler):
    def delete(self, id):
        logging.info('Deleting project id' + str(id))
        db = getDb()
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


class Index(webapp2.RequestHandler):
    def get(self):
        names = {
            'header': 'Header Text Dictionary'
        }
        template_values = {
            'header': names,
            'menu1': 'menu item 1',
            'menu2': 'menu item 2',
            'dashboard_header_1': 'Dashboard 1',
            'dashboard_header_2': 'Dashboard 2',
            'dashboard_header_3': 'Dashboard 3',
            'section_header': 'this is the section header'
        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))

class Form(webapp2.RequestHandler):
    def get(self):
        template_values = {}
        template = JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render(template_values))

class Templates_projects(webapp2.RequestHandler):
    def get(self):
        template_values = {}
        template = JINJA_ENVIRONMENT.get_template('projects.html')
        self.response.write(template.render(template_values))

class Project_edit(webapp2.RequestHandler):
    def get(self):
        template_values = {}
        template = JINJA_ENVIRONMENT.get_template('project_edit.html')
        self.response.write(template.render(template_values))


# webapp2: https://webapp-improved.appspot.com/index.html
app = webapp2.WSGIApplication([
                                  ('/', Form),
                                  # ('/', Index),
                                  ('/projects', Templates_projects),
                                  ('/project_edit', Project_edit),
                                  ('/main', MainHandler),
                                  ('/newbase/(\d+)', Projects)
                              ], debug=True)