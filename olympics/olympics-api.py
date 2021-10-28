'''
    olympics-api.py
    Authors: Robbie Young, 28 October 2021
    For use in the 'olympics' project in Carleton's CS257 course, Fall term
'''

import flask
import json
import psycopg2
import argparse
import config
from config import database as config_database
from config import user as config_user
from config import password as config_password

app = flask.Flask(__name__)

def connect(connect_database, connect_user, connect_password):
    try:
        connection = psycopg2.connect(database=connect_database, user=connect_user, password=connect_password)
        return connection
    except Exception as e:
        print(e)
        exit()

@app.route('/')
def base():
    return '''
    [̲̅$̲̅(̲̅5̲̅)̲̅$̲̅][̲̅$̲̅(̲̅5̲̅)̲̅$̲̅][̲̅$̲̅(̲̅5̲̅)̲̅$̲̅][̲̅$̲̅(̲̅5̲̅)̲̅$̲̅][̲̅$̲̅(̲̅5̲̅)̲̅$̲̅][̲̅$̲̅(̲̅5̲̅)̲̅$̲̅][̲̅$̲̅(̲̅5̲̅)̲̅$̲̅][̲̅$̲̅(̲̅5̲̅)̲̅$̲̅][̲̅$̲̅(̲̅5̲̅)̲̅$̲̅][̲̅$̲̅(̲̅5̲̅)̲̅$̲̅][̲̅$̲̅(̲̅5̲̅)̲̅$̲̅][̲̅$̲̅(̲̅5̲̅)̲̅$̲̅][̲̅$̲̅(̲̅5̲̅)̲̅$̲̅][̲̅$̲̅(̲̅5̲̅)̲̅$̲̅][̲̅$̲̅(̲̅5̲̅)̲̅$̲̅][̲̅$̲̅(̲̅5̲̅)̲̅$̲̅][̲̅$̲̅(̲̅5̲̅)̲̅$̲̅][̲̅$̲̅(̲̅5̲̅)̲̅$̲̅][̲̅$̲̅(̲̅5̲̅)̲̅$̲̅][̲̅$̲̅(̲̅5̲̅)̲̅$̲̅]
    '''

@app.route('/games')
def games():
    connection = connect(config_database, config_user, config_password)
    query = '''SELECT games.id, games.year, seasons.season, games.city
                FROM games, seasons
                WHERE games.season_id = seasons.id
                ORDER BY games.year'''

    try:
        cursor = connection.cursor()
        cursor.execute(query)
    except Exception as e:
        print(e)
        exit()

    games_list = []
    for game in cursor:
        game_dict = {}
        game_dict['id'] = game[0]
        game_dict['year'] = game[1]
        game_dict['season'] = game[2]
        game_dict['city'] = game[3]
        
        games_list.append(game_dict)

    connection.close()
    return json.dumps(games_list)

@app.route('/nocs')
def nocs():
    connection = connect(config_database, config_user, config_password)
    query = '''SELECT DISTINCT noc_regions.noc, noc_regions.region
                FROM noc_regions
                ORDER BY noc'''

    try:
        cursor = connection.cursor()
        cursor.execute(query)
    except Exception as e:
        print(e)
        exit()

    noc_list = []
    for noc in cursor:
        noc_dict = {}
        noc_dict['abbreviation'] = noc[0]
        noc_dict['name'] = noc[1]

        noc_list.append(noc_dict)

    connection.close()
    return json.dumps(noc_list)

@app.route('/medalists/games/<games_id>')
def medalists(games_id):
    connection = connect(config_database, config_user, config_password)
    noc = flask.request.args.get('noc')
    query = '''SELECT DISTINCT athletes.id, athlete_names.name, athletes.sex, sports.sport, events.event, medals.medal
                FROM athlete_names, athletes, sports, events, medals, noc_regions, super_table
                WHERE athlete_names.id = athletes.name_id
                AND super_table.athlete_id = athletes.id
                AND sports.id = events.sport_id
                AND super_table.event_id = events.id
                AND super_table.medal_id = medals.id
                AND medals.medal NOT LIKE 'NA'
                AND super_table.game_id = %s'''
    
    try:
        cursor = connection.cursor()
        if noc is not None:
            query += '''AND noc_regions.noc LIKE %s
                        AND super_table.noc_region_id = noc_regions.id'''
            cursor.execute(query, (games_id, noc))
        else:
            cursor.execute(query, (games_id, ))
    except Exception as e:
        print(e)
        exit()

    medalists_list = []
    for medalist in cursor:
        medalist_dict = {}
        medalist_dict['athlete_id'] = medalist[0]
        medalist_dict['athlete_name'] = medalist[1]
        medalist_dict['athlete_sex'] = medalist[2]
        medalist_dict['sport'] = medalist[3]
        medalist_dict['event'] = medalist[4]
        medalist_dict['medal'] = medalist[5]

        medalists_list.append(medalist_dict)

    connection.close()
    return json.dumps(medalists_list)

def main():
    # print(base())
    # print(games())
    # print(nocs())
    # print(medalists(1))
    
    parser = argparse.ArgumentParser('A sample Flask application/API')
    parser.add_argument('host', help='the host on which this application is running')
    parser.add_argument('port', type=int, help='the port on which this application is listening')
    arguments = parser.parse_args()
    app.run(host=arguments.host, port=arguments.port, debug=True)

if __name__ == '__main__':
    main()