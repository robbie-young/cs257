CREATE TABLE athletes(
    id SERIAL,
    athlete_sex TEXT,
    athlete_age INT,
    athlete_height INT,
    weight INT,
    athlete_name_id INT
);

CREATE TABLE athlete_names(
    id SERIAL,
    athlete_name TEXT
);

CREATE TABLE noc_regions(
    id SERIAL,
    team_name TEXT,
    noc_region TEXT
);

CREATE TABLE games(
    id SERIAL,
    title TEXT,
    year INT,
    season TEXT,
    city TEXT
);

CREATE TABLE events(
    id SERIAL,
    sport TEXT,
    event_name_id INT
);

CREATE TABLE event_names(
    id SERIAL,
    event_name TEXT
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