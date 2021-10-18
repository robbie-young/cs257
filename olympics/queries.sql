SELECT DISTINCT noc FROM noc_regions ORDER BY noc;

SELECT DISTINCT athlete_names.name, noc_regions.region
FROM athlete_names, athletes, noc_regions, super_table
WHERE noc_regions.region LIKE 'Kenya'
AND super_table.noc_region_id = noc_regions.id
AND super_table.athlete_id = athletes.id
AND athletes.name_id = athlete_names.id
ORDER BY athlete_names.name;

SELECT athlete_names.name, medals.medal, games.title, events.event
FROM athletes, athlete_names, medals, games, events, super_table
WHERE athlete_names.name LIKE '%Greg%Louganis%'
AND athletes.name_id = athlete_names.id
AND super_table.athlete_id = athletes.id
AND super_table.medal_id = medals.id
AND super_table.game_id = games.id
AND super_table.event_id = events.id
ORDER BY games.year;

SELECT COUNT(medals.medal), noc_regions.noc, medals.medal
FROM noc_regions, medals, super_table
WHERE medals.medal LIKE 'Gold'
AND super_table.medal_id = medals.id
AND super_table.noc_region_id = noc_regions.id
GROUP BY noc_regions.noc, medals.medal
ORDER BY COUNT(medals.medal) desc, noc_regions.noc;