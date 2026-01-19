-- ==============================
-- Tennis Analytics Database Schema
-- ==============================

-- Categories
CREATE TABLE IF NOT EXISTS categories (
    category_id VARCHAR(50) PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL
);

-- Competitions
CREATE TABLE IF NOT EXISTS competitions (
    competition_id VARCHAR(50) PRIMARY KEY,
    competition_name VARCHAR(150) NOT NULL,
    parent_id VARCHAR(50),
    type VARCHAR(30),
    gender VARCHAR(20),
    category_id VARCHAR(50) NOT NULL,
    CONSTRAINT fk_category
        FOREIGN KEY (category_id)
        REFERENCES categories(category_id),
    CONSTRAINT fk_parent_competition
        FOREIGN KEY (parent_id)
        REFERENCES competitions(competition_id)
);

-- Complexes
CREATE TABLE IF NOT EXISTS complexes (
    complex_id VARCHAR(50) PRIMARY KEY,
    complex_name VARCHAR(150) NOT NULL
);

-- Venues
CREATE TABLE IF NOT EXISTS venues (
    venue_id VARCHAR(50) PRIMARY KEY,
    venue_name VARCHAR(150) NOT NULL,
    city_name VARCHAR(100) NOT NULL,
    country_name VARCHAR(100) NOT NULL,
    country_code CHAR(3) NOT NULL,
    timezone VARCHAR(100) NOT NULL,
    complex_id VARCHAR(50) NOT NULL,
    CONSTRAINT fk_complex
        FOREIGN KEY (complex_id)
        REFERENCES complexes(complex_id)
);

-- Competitors
CREATE TABLE IF NOT EXISTS competitors (
    competitor_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    country VARCHAR(100) NOT NULL,
    country_code CHAR(3) NOT NULL,
    abbreviation VARCHAR(20) NOT NULL
);

-- Competitor Rankings 
CREATE TABLE IF NOT EXISTS competitor_rankings (
    rank_id SERIAL PRIMARY KEY,
    rank INT NOT NULL,
    movement INT NOT NULL,
    points INT NOT NULL,
    competitions_played INT NOT NULL,
    competitor_id VARCHAR(50) NOT NULL,
    ranking_week DATE,
    CONSTRAINT fk_competitor
        FOREIGN KEY (competitor_id)
        REFERENCES competitors(competitor_id)
);

-- indexes for analytics
CREATE INDEX IF NOT EXISTS idx_competitor_rankings_week
    ON competitor_rankings(ranking_week);

CREATE INDEX IF NOT EXISTS idx_competitor_rankings_rank
    ON competitor_rankings(rank);





SELECT * FROM categories;
SELECT * FROM competitions;
SELECT * FROM complexes;
SELECT * FROM venues;
SELECT * FROM competitors;
SELECT * FROM competitor_rankings;

SELECT current_database();
TRUNCATE competitions, categories CASCADE;


SELECT table_schema, table_name
FROM information_schema.tables
WHERE table_name ILIKE '%competition%';



















