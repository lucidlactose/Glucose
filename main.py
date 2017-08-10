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
# app_id  	3a2897b4
        dict_base_url = "https://od-api.oxforddictionaries.com/api/v1/entries/en/"
        dict_url_params = {'q': search, 'api_key': 'fa87cfff2bc23fc87f8679f9413c61b3'}
        # dict_base_url = "http://www.dictionaryapi.com/api/v1/references/collegiate/xml/"
        # dict_url_params = {'': search, 'key': 'ed36c100-f856-46ac-8be5-0fd11b43872b'}
        # dict_xml = urllib2.urlopen(dict_base_url + urllib.urlencode(dict_url_params)).read()

        used = []
        random_gif = random.randint(0,6)
        images = []

        while len(images) < 7:
            if random_gif in used:
                random_gif = random.randint(0,6)
            else:
                images.append(parsed_giphy_dictionary['data'][random_gif]['images']['original']['url'])
                used.append(random_gif)



        netflix_search ="https://www.netflix.com/search?q="
        netflix_query = ""
        for i in search:
            if i == " ":
                netflix_query += "%20"
            else:
                netflix_query += i

        netflix_search += netflix_query

        template_variables = {
            "urls": images,
            "netflix_query" : netflix_search
        }

        results_template = jinja_environment.get_template("templates/results.html")

        self.response.write(results_template.render(template_variables))


app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
