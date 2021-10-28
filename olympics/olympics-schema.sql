CREATE TABLE athletes(
    id SERIAL,
    name_id INT,
    sex TEXT,
    age INT,
    height FLOAT,
    weight FLOAT
);

CREATE TABLE athlete_names(
    id SERIAL,
    name TEXT
);

CREATE TABLE noc_regions(
    id SERIAL,
    team_name TEXT,
    noc TEXT,
    region TEXT
);

CREATE TABLE games(
    id SERIAL,
    title TEXT,
    year INT,
    season_id INT,
    city TEXT
);

CREATE TABLE seasons(
    id SERIAL,
    season TEXT
);

CREATE TABLE events(
    id SERIAL,
    event TEXT,
    sport_id INT
);

CREATE TABLE sports(
    id SERIAL,
    sport TEXT
);

CREATE TABLE medals(
    id SERIAL,
    medal TEXT
);

CREATE TABLE super_table(
    id SERIAL,
    athlete_id INT,
    noc_region_id INT,
    game_id INT,
    event_id INT,
    medal_id INT
);