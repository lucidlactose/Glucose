import webapp2
import jinja2
import json
import os
import urllib
import urllib2
import random

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template("templates/start.html")
        self.response.write(template.render())


    def post(self):
        base_url = "http://api.giphy.com/v1/gifs/search?"
        search = self.request.get('search')
        url_params = {'q': search, 'api_key': 'dc6zaTOxFJmzC', 'limit': 10}
        giphy_response = urllib2.urlopen(base_url + urllib.urlencode(url_params)).read()
        parsed_giphy_dictionary = json.loads(giphy_response)

        used = []
        random_gif = random.randint(0,9)
        images = []

        while len(images) < 10:
            if random_gif in used:
                random_gif = random.randint(0,9)
            else:
                images.append(parsed_giphy_dictionary['data'][random_gif]['images']['original']['url'])
                used.append(random_gif)

        template_variables = {
            "urls": images
        }
        results_template = jinja_environment.get_template("templates/results.html")

        self.response.write(results_template.render(template_variables))

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
