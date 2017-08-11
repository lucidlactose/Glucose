import webapp2
import jinja2
import json
import os
import urllib
import urllib2
import random
# import requests

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
#######################################################################################
        dict_url = "https://od-api.oxforddictionaries.com/api/v1/entries/en/" + search.lower()
        # dict_request = requests.get(dict_url, headers = {'app_id': '3a2897b4', "app_key": 'fa87cfff2bc23fc87f8679f9413c61b3'})
        # dict_dict = json.dumps(dict_request.jos())

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

        youtube_search = "https://www.youtube.com/results?search_query="
        youtube_query =""
        hulu_search = "https://www.hulu.com/search?q="
        hulu_query = ""
        for y in search:
            if y == " ":
                youtube_query += "+"
            else:
                youtube_query += y

        youtube_search += youtube_query

        for h in search:
            if h == " ":
                hulu_query += "+"
            else:
                hulu_query += h
        hulu_search += hulu_query
        oxford_search = ""
        haveNew = False
        new_search = []
        for h in search:
            if h == " ":
                new_search = search.split(" ")
                haveNew = True
            else:
                haveNew = False


        if haveNew == True:
            oxford_search = "https://en.oxforddictionaries.com/definition/" + new_search[0]
        else:
            oxford_search = "https://en.oxforddictionaries.com/definition/" + search



######################################################################333
        template_variables = {
            "urls": images,
            "netflix_query" : netflix_search,
            "youtube_query" : youtube_search,
            'hulu_query' : hulu_search,
            'new_search' : oxford_search
        }
        results_template = jinja_environment.get_template("templates/results.html")
        self.response.write(results_template.render(template_variables))


app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
