'''
    convert.py
    Author: Robbie Young
    For use in "olympics" assignment in Carleton College's CS 257 Software Design Class, Fall 2021
'''

import csv

noc_countries_dict = {} # {'noc' : 'region'} only used for creating the noc_regions_dict, this itself does not represent a table

athletes_dict = {} # {'name_id|sex|age|height|weight' : id}
athlete_names_dict = {} # {'name' : id}
noc_regions_dict = {} # {'team_name|noc|region' : id}
games_dict = {} # {'title|year|season_id|city' : id}
seasons_dict = {} # {'season' : id}
events_dict = {} # {'event|sport_id' : id}
event_names_dict = {} # {'event_name' : id}
medals_dict = {} # {'medal' : id}
super_table_dict = {} # {'athlete_id|noc_region_id|game_id|event_id|medal|id' : 1} only dictionary which does not check for duplicate entries

def create_files(): # either creates the file if not found in cd, or clears the files
    with open('athlete_names.csv', 'w') as file:
        file.truncate()
    with open('athletes.csv', 'w') as file:
        file.truncate()
    with open('noc.csv', 'w') as file:
        file.truncate()
    with open('games.csv', 'w') as file:
        file.truncate()
    with open('seasons.csv', 'w') as file:
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

    populate_noc_countries() # reads noc_regions file to populate noc regions and their country names

    with open(csv_file_name, 'r', newline='') as file:
        next(file)
        reader = csv.reader(file)
        for row in reader: # row string is : [0] ID, [1] Name, [2] Sex, [3] Age, [4] Height, [5] Weight, [6] Team, [7] NOC, [8] Games, [9] Year, [10] Season, [11] City, [12] Sport, [13] Event, [14] Medal
            this_athlete_id = populate_athlete(name=row[1], sex=row[2], age=row[3], height=row[4], weight=row[5])
            this_noc_region_id = populate_noc_region(team_name=row[6], noc=row[7])
            this_game_id = populate_game(title=row[8], year=row[9], season=row[10], city=row[11])
            this_event_id = populate_event(sport=row[12], event=row[13])
            this_medal_id = populate_medal(medal=row[14])
            populate_super_table(athlete_id=this_athlete_id, noc_region_id=this_noc_region_id, game_id=this_game_id, event_id=this_event_id, medal_id=this_medal_id)
    
    write_to('athlete_names.csv', athlete_names_dict)
    write_to('athletes.csv', athletes_dict)
    write_to('noc.csv', noc_regions_dict)
    write_to('games.csv', games_dict)
    write_to('seasons.csv', seasons_dict)
    write_to('events.csv', events_dict)
    write_to('event_names.csv', event_names_dict)
    write_to('medals.csv', medals_dict)
    write_to('super_table.csv', super_table_dict)

def populate_noc_countries(): # used to set each noc to a specific region
    with open('noc_regions.csv', 'r', newline='') as file:
        next(file)
        reader = csv.reader(file)
        for row in reader:
            if row[2]:
                noc_countries_dict[row[0]] = row[2]
            else:
                noc_countries_dict[row[0]] = row[1]
    
def populate_athlete(name, sex, age, height, weight):
    name_id = populate_athlete_name(name)
    data = str(name_id)+'|'+sex+'|'+age+'|'+height+'|'+weight
    if data in athletes_dict:
        return athletes_dict[data]
    
    id = len(athletes_dict) + 1
    athletes_dict[data] = id
    return id

def populate_athlete_name(name):
    if name in athlete_names_dict:
        return athlete_names_dict[name]
    
    id = len(athlete_names_dict) + 1
    athlete_names_dict[name] = id
    return id

def populate_noc_region(team_name, noc):
    data = team_name+'|'+noc+'|'+noc_countries_dict[noc] # noc_countries_dict[noc] is the region
    if data in noc_regions_dict:
        return noc_regions_dict[data]

    id = len(noc_regions_dict) + 1
    noc_regions_dict[data] = id
    return id

def populate_game(title, year, season, city):
    season_id = populate_season_id(season)
    data = title+'|'+year+'|'+str(season_id)+'|'+city
    if data in games_dict:
        return games_dict[data]
    
    id = len(games_dict) + 1
    games_dict[data] = id
    return id

def populate_season_id(season):
    if season in seasons_dict:
        return seasons_dict[season]
    
    id = len(seasons_dict) + 1
    seasons_dict[season] = id
    return id

def populate_event(sport, event):
    sport_id = populate_sport_name(sport)
    data = event+'|'+str(sport_id)
    if data in events_dict:
        return events_dict[data]
    
    id = len(events_dict) + 1
    events_dict[data] = id
    return id

def populate_sport_name(event):
    if event in event_names_dict:
        return event_names_dict[event]
    
    id = len(event_names_dict) + 1
    event_names_dict[event] = id
    return id

def populate_medal(medal):
    if medal in medals_dict:
        return medals_dict[medal]
    
    id = len(medals_dict) + 1
    medals_dict[medal] = id
    return id

def populate_super_table(athlete_id, noc_region_id, game_id, event_id, medal_id):
    data = str(athlete_id)+'|'+str(noc_region_id)+'|'+str(game_id)+'|'+str(event_id)+'|'+str(medal_id)
    id = len(super_table_dict) + 1
    super_table_dict[data] = str(id)

def write_to(file, dictionary):
    with open(file, 'a', newline='') as file:
        writer = csv.writer(file)
        for read_data in dictionary:
            write_data = read_data.split('|')
            write_data.insert(0, str(dictionary[read_data]))
            writer.writerow(write_data)

def main():
    create_files()
    load('athlete_events.csv')
    # load('test_athlete_events.csv')

    print('Convert done')

if __name__ == '__main__':
    main()