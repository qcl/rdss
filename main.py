#!/usr/bin/env python

import os
import jinja2
import webapp2
import json
from datetime import date, timedelta

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
        result = {
            "success": False
        }

        startDate = self.request.get('startDate', None)
        discount = int(self.request.get('discount', 0))

        try:
            today = date.today()
            startYear, startMonth, startDay = startDate.split('-')
            startDate = date(int(startYear), int(startMonth), int(startDay))
            endDate = startDate.replace(int(startYear) + 3) - timedelta(discount)

            timeDiff = endDate - today
            totalDiff = endDate - startDate
            print timeDiff.days

            result['startDate'] = str(startDate)
            result['endDate'] = str(endDate)
            result['today'] = str(today)
            result['discount'] = discount
            result['total'] = totalDiff.days
            result['remain'] = timeDiff.days
            result['passed'] = result['total'] - result['remain']

            result['success'] = True

        except:
            pass

        
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write( json.dumps(result) )

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/api/endDate', RDSSAPIendDateHandeler)
], debug=True)

app.error_handlers[404] = handle_404
app.error_handlers[500] = handle_500
