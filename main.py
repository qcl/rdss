#!/usr/bin/env python

import os
import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__),'views')),
    extensions=['pyjade.ext.jinja.PyJadeExtension'],
    autoescape=True)


class JadeHandler(webapp2.RequestHandler):
    @staticmethod
    def jade_factory(app):
        j = jinja2.Jinja2(app)
        j.environment.add_extension('pyjade.ext.jinja.PyJadeExtension')
        return j

    @webapp2.cached_property
    def jinja2(self):
        return jinja2.get_jinja2(app=self.app, factory=JadeHandler.jade_factory)

    def render_response(self, _template, **context):
        rv = self.jinja2.render_template(_template, **context)
        self.response.write(rv)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('index.jade')
        self.response.write(template.render({'title':'RDSS API'}))

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
