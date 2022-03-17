from email.utils import decode_rfc2231
import pandas as pd
import requests
import json
import config

response_list = []
API_KEY = config.api_key
df = ""

def get_response_list():
# create a loop that requests each movie one at a time and appends the response to a list.
    for movie_id in range(995,996):
        #send a single GET request to the API,  receive a JSON record
        r = requests.get('https://api.themoviedb.org/3/movie/{}?api_key={}'.format(movie_id, API_KEY))
        response_list.append(r.json())

def get_genres(genres_list):
    #create a separate table for genres and a column of lists to explode out
    #genres_list = df['genres'].tolist()
    flat_list = []
    for sublist in genres_list:
        if isinstance(sublist, list):
            for item in sublist:
                flat_list.append(item)
    #create a pandas dataframe from unique genres
    df_genres = pd.DataFrame.from_records(flat_list).drop_duplicates()
    #create csv file from table genres
    df_genres.to_csv('tmdb_genres.csv', index=False)

    result = []
    for l in genres_list:
        if isinstance(l,list):
            r = []
            for d in l:
                r.append(d['name'])
            result.append(r)
        else:
            result.append(["none"])    
    # add column genres_all to df (only genres)
    return result


def get_spoken_languages(languages):
#handle spoken languages to be simple
 
    spoken_languages = []
    for l in languages:
        if isinstance(l,list):
            r = []
            for d in l:
                r.append(d['english_name'])
            spoken_languages.append(r)
        else:
            spoken_languages.append(["none"])   
    return spoken_languages           



def production_countries():
    #handle production_countries to be simple
    countries = df['production_countries'].tolist()
    country = []
    for l in countries:
        if isinstance(l,list):
            r = []
            for d in l:
                r.append(d['name'])
            country.append(r)
        else:
            country.append(["none"])        
    # update column production_countries (just name)
    df = df.assign(production_countries=country)

def column():
    #create a list of column names called df_columns that allows us to select the columns we want from the main dataframe.
    df_columns = ['title', 'spoken_languages','production_countries', 'vote_average', 'release_date', 'runtime', 'overview']
    #add column genres name
    df_genre_columns = df_genres['name'].to_list()
    df_columns.extend(df_genre_columns)
    #break the [genres] into peaces
    s = df['genres_all'].explode()
    #make 0,1 in to each genres
    df = df.join(pd.crosstab(s.index, s))
    #create csv file from table columns
    df[df_columns].to_csv('tmdb_movies_infomation.csv', index=False)


#main
get_response_list()
#Create a pandas dataframe from the records
df = pd.DataFrame.from_dict(response_list)

genres_list = df['genres'].tolist()
df = df.assign(genres_all=get_genres(genres_list))

# update column spoken_languages (just language)
languages = df['spoken_languages'].tolist()
df = df.assign(spoken_languages=get_spoken_languages(languages))

