#!/usr/bin/env python

import os
import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__),'views')),
    extensions=['pyjade.ext.jinja.PyJadeExtension'],
    autoescape=True)

def handle_404(request, response, exception):
    template = JINJA_ENVIRONMENT.get_template('error.jade')
    response.write(template.render({'message': exception,
                                    'error': {
                                        'status': 404
                                    }
                                    }))
    response.set_status(404)

def handle_500(request, response, exception):
    template = JINJA_ENVIRONMENT.get_template('error.jade')
    response.write(template.render({'message': exception,
                                    'error': {
                                        'status': 500
                                    }
                                    }))
    response.set_status(500)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('index.jade')
        self.response.write(template.render({'title':'RDSS API'}))

class RDSSAPIendDateHandeler(webapp2.RequestHandler):
    def get(self):
        startDate = self.request.get('startDate', None)
        discount = self.request.get('discount', 0)

        self.response.headers['Content-Type'] = 'application/json'

        if startDate == None:
            self.response.write('{"success":false}')
        else:
            # TODO
            self.response.write('{"success":true}')

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/api/endDate', RDSSAPIendDateHandeler)
], debug=True)

app.error_handlers[404] = handle_404
app.error_handlers[500] = handle_500
