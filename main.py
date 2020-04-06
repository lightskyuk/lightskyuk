#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os
import jinja2
import webapp2
from google.appengine.api import urlfetch
from google.appengine.api import memcache

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

        
class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render({}))

class SiteList(webapp2.RequestHandler):
    def get(self):
        result = urlfetch.fetch('http://datapoint.metoffice.gov.uk/public/data/val/wxfcs/all/json/sitelist?key=7c51034d-2e4b-407f-a264-9a204ca22e8b')
        self.response.write(result.content)

class Forecast(webapp2.RequestHandler):
    def get(self,siteid):
        result = urlfetch.fetch('http://datapoint.metoffice.gov.uk/public/data/val/wxfcs/regionalforecast/json/'+siteid+'?res=3hourly&key=7c51034d-2e4b-407f-a264-9a204ca22e8b')
        self.response.write(result.content)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/sitelist', SiteList),
    ('/forecast/(.*)', Forecast)
], debug=True)
