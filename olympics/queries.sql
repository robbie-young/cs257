SELECT * FROM noc_regions ORDER BY noc_regions;

SELECT athlete_name
FROM athletes, athlete_names, noc_regions, super_table
WHERE noc_regions.team_name = 'Kenya'
AND super_table.noc_region_id = noc_regions.id
AND super_table.athlete_id = athletes.id;

SELECT medals
FROM athletes, athlete_names, medals, super_table, games
WHERE super_table.athlete_id = athletes.id
AND athletes_name_id = athlete_names.id
AND athlete_names.athlete_name = 'Greg Louganis'
BY ;