import pandas as pd
import requests
import json
import config

response_list = []
API_KEY = config.api_key
df = ""

# create a loop that requests each movie one at a time and appends the response to a list.
for movie_id in range(11,996):
        #send a single GET request to the API,  receive a JSON record
    r = requests.get('https://api.themoviedb.org/3/movie/{}?api_key={}'.format(movie_id, API_KEY))
    response_list.append(r.json())
#print (response_list)

df = pd.DataFrame.from_dict(response_list)
df.to_csv('original_data.csv', index=False)

file = pd.read_csv("original_data.csv")
file.to_html("original_data.html") 