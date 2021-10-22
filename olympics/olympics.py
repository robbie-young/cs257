'''
    olympics.py
    Author: Robbie Young
    For use in the "olympics" assignment in Carleton's CS 257 Software Design Class, Fall 2021
    Credits: Jeff Ondich, psycopg2-sample.py
'''

import argparse
import psycopg2
import os
import random
import config
from config import database as config_database
from config import user as config_user
from config import password as config_password

def get_parsed_arguments():
    parser = argparse.ArgumentParser(add_help=False)

    parser.add_argument('--help', '-h', action='store_true')
    parser.add_argument('--names', '-n')
    parser.add_argument('--gold', '-g', action='store_true')
    parser.add_argument('--search', '-s')
    parser.add_argument('--countries', '-c', action='store_true')

    return parser.parse_args()

def connect(connect_database, connect_user, connect_password):
    try:
        connection = psycopg2.connect(database=connect_database, user=connect_user, password=connect_password)
        return connection
    except Exception as e:
        print(e)
        exit()

def print_cursor(cursor):
    print('\nHere are the first 10 results. Please hit enter to view the next 10 items.\n\n=====')
    line_count = 0
    for row in cursor:
        print(row)
        line_count += 1
        if line_count % 10 == 0: # allows for printing only 10 items at once
            next_line = input("=====\n\nEnter 'q' to quit\n")
            if next_line=='q':
                quit()
            print('=====')
    print('\n')

def query_names(connection, noc):
    query = '''SELECT DISTINCT athlete_names.name, noc_regions.region
                FROM athlete_names, athletes, noc_regions, super_table
                WHERE noc_regions.noc LIKE %s
                AND super_table.noc_region_id = noc_regions.id
                AND super_table.athlete_id = athletes.id
                AND athletes.name_id = athlete_names.id
                ORDER BY athlete_names.name;'''
    try:
        cursor = connection.cursor()
        cursor.execute(query, (noc,))
        return cursor
    except Exception as e:
        print(e)
        exit()

def query_gold(connection):
    try:
        cursor = connection.cursor()
        query = '''SELECT COUNT(medals.medal), noc_regions.region, medals.medal
                    FROM noc_regions, medals, super_table
                    WHERE medals.medal LIKE 'Gold'
                    AND super_table.medal_id = medals.id
                    AND super_table.noc_region_id = noc_regions.id
                    GROUP BY noc_regions.region, medals.medal
                    ORDER BY COUNT(medals.medal) desc, noc_regions.region;'''
        cursor.execute(query)
        return cursor
    except Exception as e:
        print(e)
        exit()

def query_search(connection, search):
    query = '''SELECT DISTINCT athlete_names.name, noc_regions.region
                FROM athlete_names, athletes, noc_regions, super_table
                WHERE noc_regions.region LIKE %s
                AND super_table.noc_region_id = noc_regions.id
                AND super_table.athlete_id = athletes.id
                AND athletes.name_id = athlete_names.id
                ORDER BY athlete_names.name;'''
    try:
        cursor = connection.cursor()
        cursor.execute(query, (search,))
        return cursor
    except Exception as e:
        print(e)
        exit()

# returns all available countries, useful for query_search as search string has to be exact
def query_countries(connection):
    try:
        cursor = connection.cursor()
        query = '''SELECT DISTINCT noc_regions.region
                    FROM noc_regions, super_table
                    WHERE super_table.noc_region_id = noc_regions.id
                    ORDER BY noc_regions.region;'''
        cursor.execute(query)
        return cursor
    except Exception as e:
        print(e)
        exit()
 
def main():
    arguments = get_parsed_arguments()
    connection = connect(config_database, config_user, config_password)
    if arguments.help:
        file = open('usage.txt', 'r')
        print(file.read())
    elif arguments.names is not None:
        cursor = query_names(connection, arguments.names)
        print_cursor(cursor)
    elif arguments.gold:
        cursor = query_gold(connection)
        print_cursor(cursor)
    elif arguments.search is not None:
        cursor = query_search(connection, arguments.search)
        print_cursor(cursor)
    elif arguments.countries:
        cursor = query_countries(connection)
        print_cursor(cursor)
    else:
        print('No specified query found in arguments. Please use the --help flag for usage.')
    
    connection.close()

if __name__ == '__main__':
    main()