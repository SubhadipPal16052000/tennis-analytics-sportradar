--=================================================================================
-- COMPETITIONS & CATEGORIES
--=================================================================================

-- 1. List all competitions along with their category name.
CREATE VIEW All_competitions_with_category AS
SELECT c.competition_id, c.competition_name, cat.category_name
FROM competitions c
JOIN categories cat 
	ON c.category_id = cat.category_id;

SELECT * FROM All_competitions_with_category;

-- 2. Count the number of competitions in each category.

CREATE VIEW Number_of_competitions_in_each_category AS
SELECT cat.category_name,
	COUNT(c.competition_id) AS total_competitions
FROM competitions c
JOIN categories cat 
	ON c.category_id = cat.category_id
GROUP BY cat.category_name
ORDER BY total_competitions DESC;

SELECT * FROM Number_of_competitions_in_each_category;

-- 3. Find all competitions of type 'doubles'.

CREATE VIEW Double_type_competitions AS
SELECT competition_id, competition_name, type, gender
FROM competitions
WHERE LOWER(type) = 'doubles';

SELECT * FROM Double_type_competitions;

-- 4. Get competitions that belong to a specific category.

CREATE VIEW Specific_category_competitions AS
SELECT c.competition_id, c.competition_name
FROM competitions c
JOIN categories cat 
	ON c.category_id = cat.category_id
WHERE cat.category_name = 'ITF Men';

SELECT * FROM Specific_category_competitions;

-- 5. Identify parent competitions and their sub-competitions.

CREATE VIEW Parent_child_competitions AS
SELECT 
	parent.competition_name AS parent_competition,
	child.competition_name AS sub_competition
FROM competitions child
JOIN competitions parent 
	ON child.parent_id = parent.competition_id
ORDER BY parent_competition;

SELECT * FROM Parent_child_competitions;

-- 6. Analyze the distribution of competition types by category.

CREATE VIEW Distribution_of_competition_types_by_category AS
SELECT cat.category_name, c.type,
	COUNT(*) AS competition_count
FROM competitions c
JOIN categories cat 
	ON c.category_id = cat.category_id
GROUP BY cat.category_name, c.type
ORDER BY cat.category_name, competition_count DESC;

SELECT * FROM Distribution_of_competition_types_by_category;

-- 7. List all competitions with no parent (top-level competitions).

CREATE VIEW Top_level_competitions AS
SELECT competition_id, competition_name
FROM competitions
WHERE parent_id IS NULL;

SELECT * FROM Top_level_competitions; 

--==================================================================================
-- COMPLEXES & VENUES
--==================================================================================
-- 8. List all venues along with their associated complex name.

CREATE VIEW Associated_venue_complex_name AS
SELECT v.venue_id, v.venue_name, c.complex_name
FROM venues v
JOIN complexes c 
	ON v.complex_id = c.complex_id;

SELECT * FROM Associated_venue_complex_name;

-- 9. Count the number of venues in each complex.

CREATE VIEW Number_of_venues_in_each_complex AS
SELECT c.complex_name,
	COUNT(v.venue_id) AS venue_count
FROM venues v
JOIN complexes c 
	ON v.complex_id = c.complex_id
GROUP BY c.complex_name
ORDER BY venue_count DESC;

SELECT * FROM Number_of_venues_in_each_complex;

-- 10. Get details of venues in a specific country.

CREATE VIEW Specific_country_venue_details AS
SELECT venue_id, venue_name, city_name, timezone
FROM venues
WHERE country_name = 'Chile';

SELECT * FROM Specific_country_venue_details;

-- 11. Identify all venues and their timezones.

CREATE VIEW All_venues_with_timezones AS
SELECT venue_name, timezone
FROM venues
ORDER BY venue_name;

SELECT * FROM All_venues_with_timezones;

-- 12. Find complexes that have more than one venue.

CREATE VIEW Complexes_more_than_one_venue AS
SELECT c.complex_name,
	COUNT(v.venue_id) AS total_venues
FROM venues v
JOIN complexes c 
	ON v.complex_id = c.complex_id
GROUP BY c.complex_name
HAVING COUNT(v.venue_id) > 1
ORDER BY total_venues DESC;

SELECT * FROM Complexes_more_than_one_venue;

-- 13. List venues grouped by country(TIMEZONES).

CREATE OR REPLACE VIEW All_venues_by_country_timezone AS
SELECT
    timezone,
    COUNT(*) AS venue_count
FROM venues
GROUP BY timezone
ORDER BY venue_count DESC;

SELECT * FROM All_venues_by_country_timezone;

-- 14. Find all venues for a specific complex.

CREATE OR REPLACE VIEW Venues_by_specific_complex AS
SELECT
    c.complex_name,
    COUNT(v.venue_id) AS total_venues
FROM complexes c
JOIN venues v
ON c.complex_id = v.complex_id
WHERE c.complex_name = 'Nacional'
GROUP BY c.complex_name
ORDER BY total_venues DESC;

SELECT * FROM Venues_by_specific_complex ;



--===========================================================================
-- COMPETITORS & RANKINGS
--===========================================================================

-- 15. Get all competitors with their rank and points

CREATE VIEW Competitors_rank_and_points AS
SELECT comp.name, comp.country, r.rank, r.points
FROM competitor_rankings r
JOIN competitors comp 
	ON r.competitor_id = comp.competitor_id
ORDER BY r.rank;

SELECT * FROM Competitors_rank_and_points;

-- 16. Find competitors ranked in the top 5.

CREATE VIEW Top_5_competitors_ranked AS
SELECT comp.name, r.rank, r.points
FROM competitor_rankings r
JOIN competitors comp 
	ON r.competitor_id = comp.competitor_id
WHERE r.rank <= 5
ORDER BY r.rank;

SELECT * FROM Top_5_competitors_ranked;

-- 17. List competitors with no rank movement (stable rank).

CREATE VIEW Stable_rank_competitors AS
SELECT comp.name, r.rank, r.movement
FROM competitor_rankings r
JOIN competitors comp 
ON r.competitor_id = comp.competitor_id
WHERE r.movement = 0
ORDER BY r.rank;

SELECT * FROM Stable_rank_competitors;

-- 18. Get total points of competitors from a specific country.

CREATE VIEW Competitors_Total_points_from_specific_country AS
SELECT comp.country,
    SUM(r.points) AS total_points
FROM competitor_rankings r
JOIN competitors comp 
    ON r.competitor_id = comp.competitor_id
WHERE comp.country = 'Croatia'
GROUP BY comp.country;

SELECT * FROM Competitors_Total_points_from_specific_country;

-- 19. Count the number of competitors per country.

CREATE VIEW Number_of_competitors_per_country AS
SELECT country,
    COUNT(*) AS competitor_count
FROM competitors
GROUP BY country
ORDER BY competitor_count DESC;

SELECT * FROM Number_of_competitors_per_country;

-- 20. Find competitors with the highest points in the current week.

CREATE VIEW Current_week_competitors_highest_points AS
SELECT comp.name, r.rank, r.points
FROM competitor_rankings r
JOIN competitors comp 
    ON r.competitor_id = comp.competitor_id
WHERE r.ranking_week = (SELECT MAX(ranking_week) FROM competitor_rankings)
ORDER BY r.points DESC
LIMIT 10;

SELECT * FROM Current_week_competitors_highest_points;


--===============================================================
-- 21. Find all venues for with complex name.

CREATE OR REPLACE VIEW All_venues_by_complex AS
SELECT
    c.complex_name,
    COUNT(v.venue_id) AS total_venues
FROM complexes c
JOIN venues v
ON c.complex_id = v.complex_id
GROUP BY c.complex_name
ORDER BY total_venues DESC;

SELECT * FROM  All_venues_by_complex;
--=======================================================
-- 22. Count competitions by gender.

CREATE VIEW Competitions_by_gender AS
SELECT
    gender,
    COUNT(*) AS total_competitions
FROM competitions
GROUP BY gender
ORDER BY total_competitions DESC;

SELECT * FROM Competitions_by_gender;

-- 23. Find categories with more than 10 competitions.

CREATE VIEW Categories_with_many_competitions AS
SELECT
    cat.category_name,
    COUNT(c.competition_id) AS competition_count
FROM categories cat
JOIN competitions c
    ON cat.category_id = c.category_id
GROUP BY cat.category_name
HAVING COUNT(c.competition_id) > 10
ORDER BY competition_count DESC;

SELECT * FROM Categories_with_many_competitions;

-- 24. Distribution of competitions by type only.

CREATE VIEW Competition_type_distribution AS
SELECT
    type,
    COUNT(*) AS total_competitions
FROM competitions
GROUP BY type
ORDER BY total_competitions DESC;

SELECT * FROM Competition_type_distribution;

-- 25. List venues missing city information.

CREATE VIEW Venues_missing_city AS
SELECT
    venue_id,
    venue_name,
    complex_id
FROM venues
WHERE city_name = 'Unknown';

SELECT * FROM  Venues_missing_city;

-- 26. Venue distribution percentage by timezone.

CREATE VIEW Venue_distribution_percentage AS
SELECT
    timezone,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS percentage_share
FROM venues
GROUP BY timezone
ORDER BY percentage_share DESC;

SELECT * FROM Venue_distribution_percentage;

-- 27. Best ranked competitor per country.

CREATE VIEW Best_ranked_competitor_per_country AS
SELECT DISTINCT ON (comp.country)
    comp.country,
    comp.name,
    r.rank
FROM competitor_rankings r
JOIN competitors comp
    ON r.competitor_id = comp.competitor_id
ORDER BY comp.country, r.rank;

SELECT * FROM Best_ranked_competitor_per_country;

-- 28. Competitors who improved ranking.

CREATE VIEW Improved_rank_competitors AS
SELECT
    comp.name,
    r.rank,
    r.movement
FROM competitor_rankings r
JOIN competitors comp
    ON r.competitor_id = comp.competitor_id
WHERE r.movement > 0
ORDER BY r.movement DESC;

SELECT * FROM Improved_rank_competitors;

-- 29. Average points by country.

CREATE VIEW Avg_points_by_country AS
SELECT
    comp.country,
    ROUND(AVG(r.points), 2) AS avg_points
FROM competitor_rankings r
JOIN competitors comp
    ON r.competitor_id = comp.competitor_id
GROUP BY comp.country
ORDER BY avg_points DESC;

SELECT * FROM Avg_points_by_country;

-- 30. Competitors with highest competitions played.

CREATE VIEW Most_active_competitors AS
SELECT
    comp.name,
    r.competitions_played
FROM competitor_rankings r
JOIN competitors comp
    ON r.competitor_id = comp.competitor_id
ORDER BY r.competitions_played DESC
LIMIT 10;

SELECT * FROM Most_active_competitors;

