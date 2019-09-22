# TABLE EXPORT
# connects to the established local database, passes through SQL requests, and saves the requested tables to a csv

# imports
import sqlite3
import pandas as pd
import os

# parameters ===========================================================================================================
database = r'./database/2019_highest_grossing.sqlite'


# basic database preview ===============================================================================================
def print_database(database):
    conn = sqlite3.connect(str(database))

    movies = pd.read_sql_query('SELECT * FROM Movies ', conn)
    print('Movies' + ('-' * 100))
    print(movies.columns)
    print()

    actors = pd.read_sql_query('SELECT * FROM Actors ', conn)
    print('Actors' + ('-' * 100))
    print(actors.columns)
    print()

    directors = pd.read_sql_query('SELECT * FROM Directors ', conn)
    print('Directors' + ('-' * 100))
    print(directors.columns)
    print()

    writers = pd.read_sql_query('SELECT * FROM Writers ', conn)
    print('Writers' + ('-' * 100))
    print(writers.columns)
    print()

    conn.close()


# Function to request SQL input from the user and return a csv =========================================================
def save_as_csv(database):
    conn = sqlite3.connect(str(database))

    # SQL request input loop

    while True:
        request = str(input('Please input the SQL request (omit the ";" or exit with "quit") :'))
        print('Processing...')

        # allowing for a quit function
        if request.lower() == 'quit':
            break

        # cleaning input to disallow for updating or deleting
        if request.split(' ')[0] != 'SELECT':
            print('INVALID: Only SELECT queries may be made.')

        else:
            try:

                df = pd.read_sql_query(request, conn)
                print(df.head())

                confirmation = str(input('\n' + 'Is this the table you are looking to save? [Y/N]:'))

                if confirmation.lower() == 'y':
                    filename = input('\n' + 'Please input a filename for the table:')

                    try:
                        os.chdir(r'./tables')
                    except:
                        os.mkdir(r'./tables')
                        os.chdir(r'./tables')

                    df.to_csv(filename)
                    break
                else:
                    pass

            except:
                print('Error: Invalid SQL Request')
                pass

    conn.close()


# Calling Functions ====================================================================================================
print_database(database)
save_as_csv(database)
