'''
    convert.py
    Author: Robbie Young
    For use in "olympics" assignment in Carleton College's CS 257 Software Design Class, Fall 2021
'''

import csv

def create_files(): # either creates the file if not found in cd, or clears the files
    with open('athlete_names.csv', 'w') as file:
        file.truncate()
    with open('athletes.csv', 'w') as file:
        file.truncate()
    with open('noc.csv', 'w') as file:
        file.truncate()
    with open('games.csv', 'w') as file:
        file.truncate()
    with open('events.csv', 'w') as file:
        file.truncate()
    with open('event_names.csv', 'w') as file:
        file.truncate()
    with open('medals.csv', 'w') as file:
        file.truncate()
    with open('super_table.csv', 'w') as file:
        file.truncate()

def load(csv_file_name):
    with open(csv_file_name, 'r', newline='') as file:
        next(file)
        reader = csv.reader(file)
        for row in reader: # row string is : [0] ID, [1] Name, [2] Sex, [3] Age, [4] Height, [5] Weight, [6] Team, [7] NOC, [8] Games, [9] Year, [10] Season, [11] City, [12] Sport, [13] Event, [14] Medal
            this_athlete_id = populate_athlete(name=row[1], sex=row[2], age=row[3], height=row[4], weight=row[5])
            this_noc_region_id = populate_noc_region(team_name=row[6], noc_region=row[7])
            this_game_id = populate_game(title=row[8], year=row[9], season=row[10], city=row[11])
            this_event_id = populate_event(sport=row[12], event=row[13])
            this_medal_id = populate_medal(medal=row[14])

            populate_super_table(athlete_id=this_athlete_id, noc_region=this_noc_region_id, game_id=this_game_id, event_id=this_event_id, medal_id=this_medal_id)

# All populate methods do the following: first calls another method to get an idea of a certain field, second reads the existing csv to see if the current data already exists (super_table does not do this) and returns the index/id if so, third if not writes new data and returns index
def populate_athlete(name, sex, age, height, weight):
    athlete_name_id = populate_athlete_name(name)

    with open('athletes.csv', 'r', newline='') as file_read:
        row_num = 1
        reader = csv.reader(file_read)
        for row in reader:
            if row[0] == athlete_name_id and row[1] == sex and row[2] == age and row[3] == height and row[4] == weight:
                return row_num
            row_num += 1
    
    athlete_data = [athlete_name_id, sex, age, height, weight]
    with open('athletes.csv', 'a', newline='') as file_write:
        writer = csv.writer(file_write)
        writer.writerow(athlete_data)
    
    return row_num

def populate_athlete_name(name):
    with open('athlete_names.csv', 'r', newline='') as file_read:
        row_num = 1
        reader = csv.reader(file_read)
        for row in reader:
            if row[0] == name:
                return row_num
            row_num += 1

    name_data = [name]
    with open('athlete_names.csv', 'a', newline='') as file_write:
        writer = csv.writer(file_write)
        writer.writerow(name_data)
    
    return str(row_num)

def populate_noc_region(team_name, noc_region): # implement overwrite if exists in notes
    with open('noc.csv' , 'r', newline='') as file_read:
        row_num = 1
        reader = csv.reader(file_read)
        for row in reader:
            if row[0] == team_name and row[1] == noc_region:
                return row_num
            row_num += 1

    noc_region_data = [team_name, noc_region]
    with open('noc.csv', 'a', newline='') as file_write:
        writer = csv.writer(file_write)
        writer.writerow(noc_region_data)
    
    return str(row_num)

def populate_game(title, year, season, city): # implement id for season?
    with open('games.csv' , 'r', newline='') as file_read:
        row_num = 1
        reader = csv.reader(file_read)
        for row in reader:
            if row[0] == title and row[1] == year and row[2] == season and row[3] == city:
                return row_num
            row_num += 1
    
    game_data = [title, year, season, city]
    with open('games.csv', 'a', newline='') as file_write:
        writer = csv.writer(file_write)
        writer.writerow(game_data)
    
    return str(row_num)

def populate_event(sport, event): # implement id for sport too?
    event_name_id = populate_event_name(event)

    with open('events.csv', 'r', newline='') as file_read:
        row_num = 1
        reader = csv.reader(file_read)
        for row in reader:
            if row[0] == sport and row[1] == event_name_id:
                return row_num
            row_num += 1
    
    event_data = [sport, event_name_id]
    with open('events.csv', 'a', newline='') as file_write:
        writer = csv.writer(file_write)
        writer.writerow(event_data)
    
    return str(row_num)

def populate_event_name(event):
    with open('event_names.csv', 'r', newline='') as file_read:
        row_num = 1
        reader = csv.reader(file_read)
        for row in reader:
            if row[0] == event:
                return row_num
            row_num += 1
    
    event_name_data = [event]
    with open('event_names.csv', 'a', newline='') as file_write:
        writer = csv.writer(file_write)
        writer.writerow(event_name_data)
    
    return str(row_num)

def populate_medal(medal):
    with open('medals.csv', 'r', newline='') as file_read:
        row_num = 1
        reader = csv.reader(file_read)
        for row in reader:
            if row[0] == medal:
                return row_num
            row_num += 1
    
    medal_data = [medal]
    with open('medals.csv', 'a', newline='') as file_write:
        writer = csv.writer(file_write)
        writer.writerow(medal_data)
    
    return str(row_num)

def populate_super_table(athlete_id, noc_region, game_id, event_id, medal_id):
    super_data = [athlete_id, noc_region, game_id, event_id, medal_id]
    with open('super_table.csv', 'a', newline='') as file_write:
        writer = csv.writer(file_write)
        writer.writerow(super_data)

def main():
    create_files()
    load('athlete_events.csv')
    # load('test_athlete_events.csv')

if __name__ == '__main__':
    main()