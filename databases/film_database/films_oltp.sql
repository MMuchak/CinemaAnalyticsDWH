CREATE DATABASE movies_db;

-- Dimension Tables
CREATE TABLE technologies (
    technology_id SERIAL PRIMARY KEY,
    technology_name VARCHAR(255) NOT NULL
);

CREATE TABLE genres (
    genre_id SERIAL PRIMARY KEY,
    genre_name VARCHAR(255) NOT NULL
);

CREATE TABLE categories (
    category_id SERIAL PRIMARY KEY,
    category_name VARCHAR(255) NOT NULL
);

CREATE TABLE film_localizations (
    film_localized_id SERIAL PRIMARY KEY,
    film_id INTEGER REFERENCES films(film_id),
    language VARCHAR(255),
    title VARCHAR(255) NOT NULL,
    description TEXT
);

-- Fact Table
CREATE TABLE films (
    film_id SERIAL PRIMARY KEY,
    duration INTEGER NOT NULL,
    technology_id INTEGER REFERENCES technologies(technology_id),
    genre_id INTEGER REFERENCES genres(genre_id),
    category_id INTEGER REFERENCES categories(category_id)
);


-- Indexing on foreign keys
CREATE INDEX idx_film_localizations_film_id ON film_localizations(film_id);

-- Indexing on frequently filtered or joined columns
CREATE INDEX idx_films_technology_id ON films(technology_id);
CREATE INDEX idx_films_genre_id ON films(genre_id);
CREATE INDEX idx_films_category_id ON films(category_id);
