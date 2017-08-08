import webapp2
import jinja2
import json
import os
import urllib
import urllib2

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template("templates/start.html")
        self.response.write(template.render())




class ResultHandler(webapp2.ResultHandler):
    def post(self):
        base_url = "http://api.giphy.com/v1/gifs/search?"
        url_params = {'q': self.request.get('search'), 'api_key': 'dc6zaTOxFJmzC', 'limit': 10}
        giphy_response = urllib2.urlopen(base_url + urllib.urlencode(url_params)).read()
        parsed_giphy_dictionary = json.loads(giphy_response)
        gif_url = parsed_giphy_dictionary['data'][1]['images']['original']['url']
            "url": gif_url
        }
        results_template = jinja_environment.get_template("templates/main.html")

        self.response.write(results_template.render(template_variables))


app = webapp2.WSGIApplication([
    ('/', MainHandler,
     '/result', ResultHandler)
], debug=True)
template_variables = {
