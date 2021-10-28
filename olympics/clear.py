'''
    convert.py
    Author: Robbie Young
    For use in "olympics" assignment in Carleton College's CS 257 Software Design Class, Fall 2021
    Credits: https://stackoverflow.com/questions/10840533/most-pythonic-way-to-delete-a-file-which-may-not-exist
'''

import os

def clear(filename):
    try:
        os.remove(filename)
    except OSError:
        pass

def main():
    clear('athletes.csv')
    clear('athlete_names.csv')
    clear('noc.csv')
    clear('games.csv')
    clear('seasons.csv')
    clear('events.csv')
    clear('sports.csv')
    clear('medals.csv')
    clear('super_table.csv')
    
    print("All files deleted")

if __name__ == '__main__':
    main()