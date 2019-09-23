# FILM RETRIEVAL
# for accessing the OMDB SITE and saving the retrieved JSON data to a SQLite database

# imports
# import omdb, I'm aware an OMDB api exists but thought it useful to familiarize myself with JSON
import sqlite3
import json
import os
import urllib.request, urllib.parse, urllib.error

# API KEY ==============================================================================================================
# Request your own here: http://www.omdbapi.com/apikey.aspx
api_key_raw = 'Get_Your_Own.jpg'

# setting API
service = 'http://www.omdbapi.com/?'
api_key = '&apikey=' + api_key_raw

# Parameters ===========================================================================================================

database_name = r'./database/2019_highest_grossing.sqlite'


# initializing the database ============================================================================================

def create_database(filename):
    try:
        os.chdir(r'./database')
    except:
        os.mkdir(r'./database')
        os.chdir(r'./database')

    if filename.split('.')[-1] != 'sqlite':
        filename = filename + ".sqlite"

    conn = sqlite3.connect(str(filename))
    conn.close()


# saving the posters to the posters directory ==========================================================================

def save_poster(json_data):
    title = json_data['Title']
    poster_url = json_data['Poster']

    # apparently the poster url ends in '.' before the filetype
    poster_file_extension = poster_url.split('.')[-1]

    # gets the image
    poster_data = urllib.request.urlopen(poster_url).read()

    save_location = os.getcwd() + r'./posters/'

    filename = save_location + str(title) + '.' + poster_file_extension

    if not os.path.isdir(save_location):
        os.mkdir(save_location)

    f = open(filename, 'wb')
    f.write(poster_data)
    f.close()


# initializing the database and saving the json data to it =============================================================

def save_in_database(json_data, filename):
    conn = sqlite3.connect(str(filename))
    cur = conn.cursor()

    title = json_data['Title']

    # scrubbing the movies info and passing in attributes in to the movie table
    if json_data['Year'] != 'N/A' and type(json_data['Year']) != str:
        year = int(json_data['Year'])
    if json_data['Rated'] != 'N/A':
        rated = json_data['Rated']
    if json_data['Runtime'] != 'N/A':
        runtime = int(json_data['Runtime'].split()[0])
    if json_data['Country'] != 'N/A':
        country = json_data['Country']
    if json_data['Genre'] != 'N/A':
        genre = json_data['Genre']
    if json_data['Plot'] != 'N/A':
        plot = json_data['Plot']
    if json_data['Metascore'] != 'N/A':
        metascore = float(json_data['Metascore'])
    else:
        metascore = -1
    if json_data['imdbRating'] != 'N/A':
        imdb_rating = float(json_data['imdbRating'])
    else:
        imdb_rating = -1

    # creating/updating the movie table
    cur.execute('''CREATE TABLE IF NOT EXISTS Movies
       (Title TEXT, Year INTEGER, Rated TEXT ,Runtime INTEGER, Country TEXT, Genre TEXT, Plot TEXT, 
       Metascore REAL, IMDBRating REAL)''')

    # Checking if the entry already exists, otherwise inputting
    cur.execute('SELECT Title FROM Movies WHERE Title = ? ', (title,))
    row = cur.fetchone()

    if row is None:
        try:
            cur.execute('''INSERT INTO Movies (Title, Year, Rated, Runtime, Country, Genre, Plot,
             Metascore, IMDBRating) VALUES (?,?,?,?,?,?,?,?,?)''', (title, year, rated, runtime, country, genre, plot,
                                                                    metascore, imdb_rating))
        except:
            pass
    else:
        print("Record already found in Movies. No update made.")

    # creating and saving to the actors table
    cur.execute('''CREATE TABLE IF NOT EXISTS Actors (Title TEXT, Actor TEXT)''')

    if json_data['Actors'] != 'N/A':
        actors = json_data['Actors'].split(',')

        for actor in actors:

            # Checking if the entry already exists, otherwise inputting

            cur.execute('SELECT Actor FROM Actors WHERE Title = ? AND Actor = ? ', (title, actor))
            row = cur.fetchone()

            if row is None:
                cur.execute('''INSERT INTO Actors (Title, Actor) VALUES (?,?)''', (title, actor))

            else:
                print('Record for {} in {} already found.'.format(actor, title))

    # creating and saving to the directors table
    cur.execute('''CREATE TABLE IF NOT EXISTS Directors (Title TEXT, Director TEXT)''')

    if json_data['Director'] != 'N/A':
        directors = json_data['Director'].split(',')

        for director in directors:
            cur.execute('SELECT Director FROM Directors WHERE Title = ? AND Director = ? ', (title, director))
            row = cur.fetchone()

            if row is None:
                cur.execute('''INSERT INTO Directors (Title, Director) VALUES (?,?)''', (title, director))

            else:
                print('Record for {} directing {} already found.'.format(director, title))

    # creating and saving to the writers table
    cur.execute('''CREATE TABLE IF NOT EXISTS Writers (Title TEXT, Writer TEXT)''')

    if json_data['Writer'] != 'N/A':
        writers = json_data['Writer'].split(',')

        for writer in writers:
            cur.execute('SELECT Writer FROM Writers WHERE Title = ? AND Writer = ? ', (title, writer))
            row = cur.fetchone()

            if row is None:
                cur.execute('''INSERT INTO Writers (Title, Writer) VALUES (?,?)''', (title, writer))

            else:
                print('Record for {} writing {} already found.'.format(writer, title))

    # Commits the change and close the connection to the database
    conn.commit()
    conn.close()


# printing data retrieved from OMDB ====================================================================================

def print_json(json_data):
    list_keys = ['Title', 'Year', 'Rated', 'Released', 'Runtime', 'Genre', 'Director', 'Writer',
                 'Actors', 'Plot', 'Language', 'Country', 'Awards', 'Ratings',
                 'Metascore', 'imdbRating', 'imdbVotes', 'imdbID']
    print('-' * 50)
    for k in list_keys:
        if k in list(json_data.keys()):
            print(f'{k}:{json_data[k]}')
        print('-' * 50)


# Searching manually for an individual movie on omdb ===================================================================

def search_movie(title, filename):
    try:
        url = service + urllib.parse.urlencode({'t': title}) + api_key
        print(f'Retrieving {title} data')

        uh = urllib.request.urlopen(url)

        data = uh.read()
        json_data = json.loads(data)

        # useful to call print json data if you're looking to add individual movies, otherwise just eats up space
        # print_json(jasn_data)

        if json_data['Response'] == 'True':

            save_in_database(json_data, filename)

            if json_data['Poster'] != 'N/A':
                save_poster(json_data)

        else:
            print('Error encountered: ' + json_data['Error'])
    except urllib.error.URLError as e:
        print(f'Error: {e.reason}')

# Calling the functions ================================================================================================

# create_database(database_name)

# search_movie('Avengers: Endgame',database_name)
