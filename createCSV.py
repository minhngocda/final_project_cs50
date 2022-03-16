import pandas as pd
import requests
import json
import config

response_list = []
API_KEY = config.api_key

for movie_id in range(11,13):
    r = requests.get('https://api.themoviedb.org/3/movie/{}?api_key={}'.format(movie_id, API_KEY))
    response_list.append(r.json())

df = pd.DataFrame.from_dict(response_list)
genres_list = df['genres'].tolist()
flat_list = [item for sublist in genres_list for item in sublist]

result = []
for l in genres_list:
    r = []
    for d in l:
        r.append(d['name'])
    result.append(r)
df = df.assign(genres_all=result)

df_genres = pd.DataFrame.from_records(flat_list).drop_duplicates()

df_columns = ['title', 'spoken_languages', 'production_countries', 'vote_average', 'release_date', 'runtime', 'overview']
df_genre_columns = df_genres['name'].to_list()
df_columns.extend(df_genre_columns)
s = df['genres_all'].explode()
df = df.join(pd.crosstab(s.index, s))

df[df_columns].to_csv('tmdb_movies.csv', index=False)
df_genres.to_csv('tmdb_genres.csv', index=False)