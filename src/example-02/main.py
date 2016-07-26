from google.appengine.api import urlfetch

import jinja2
import json
import os
import webapp2


jinja_environment = jinja2.Environment(loader=
    jinja2.FileSystemLoader(os.path.dirname(__file__)))


class MainHandler(webapp2.RequestHandler):

    def get(self):
        template = jinja_environment.get_template('templates/input.html')
        self.response.write(template.render())

    def post(self):
        template = jinja_environment.get_template('templates/output.html')
        query_text_value = self.request.get('query_text_field')
        query_text_value = query_text_value.replace(' ','+')
        url = "http://api.giphy.com/v1/gifs/search?"
        query = "q=" + query_text_value
        auth = "&api_key=dc6zaTOxFJmzC&limit=10"
        giphy_data_source = urlfetch.fetch(url+query+auth)
        giphy_json_content = giphy_data_source.content
        parsed_giphy_dictionary = json.loads(giphy_json_content)
        gif_images = parsed_giphy_dictionary['data'][0]['images']
        gif_url = gif_images['original']['url']
        response_dict = { 'gif_url': gif_url }
        self.response.write(template.render(response_dict))


app = webapp2.WSGIApplication([
  ('/', MainHandler)
], debug=True)

