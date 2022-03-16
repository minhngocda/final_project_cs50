import pandas as pd
import requests
import json
import config

response_list = []
API_KEY = config.api_key
#send a single GET request to the API,  receive a JSON record
# create a loop that requests each movie one at a time and appends the response to a list.
for movie_id in range(11,996):
    r = requests.get('https://api.themoviedb.org/3/movie/{}?api_key={}'.format(movie_id, API_KEY))
    response_list.append(r.json())

#Create a pandas dataframe from the records
df = pd.DataFrame.from_dict(response_list)
#create a separate table for genres and a column of lists to explode out
genres_list = df['genres'].tolist()
#flat_list = [item for sublist in genres_list for item in sublist]
flat_list = []
for sublist in genres_list:
    if isinstance(sublist, list):
        for item in sublist:
            flat_list.append(item)
print(flat_list)

"""
result = []
for l in genres_list:
    r = []
    for d in l:
        r.append(d['name'])
    result.append(r)
df = df.assign(genres_all=result)

df_genres = pd.DataFrame.from_records(flat_list).drop_duplicates()
#create a list of column names called df_columns that allows us to select the columns we want from the main dataframe.
df_columns = ['title', 'spoken_languages', 'production_countries', 'vote_average', 'release_date', 'runtime', 'overview']
df_genre_columns = df_genres['name'].to_list()
df_columns.extend(df_genre_columns)
s = df['genres_all'].explode()
df = df.join(pd.crosstab(s.index, s))

df[df_columns].to_csv('tmdb_movies.csv', index=False)
df_genres.to_csv('tmdb_genres.csv', index=False)
"""