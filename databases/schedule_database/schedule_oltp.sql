CREATE DATABASE schedule_db;

-- Dimension Tables
CREATE TABLE cinemas (
    cinema_id SERIAL PRIMARY KEY,
    localized_name VARCHAR(255) NOT NULL,
    localized_address TEXT
);

CREATE TABLE halls (
    hall_id SERIAL PRIMARY KEY,
    cinema_id INTEGER REFERENCES cinemas(cinema_id),
    technology_id INTEGER REFERENCES technologies(technology_id),  
    status VARCHAR(255),
    available_seats INTEGER NOT NULL
);

CREATE TABLE tickets (
    ticket_id SERIAL PRIMARY KEY,
    session_id INTEGER,
    row INTEGER NOT NULL,
    seat_number INTEGER NOT NULL,
    user_id INTEGER,
    purchase_time TIMESTAMP
);

-- Fact Table
CREATE TABLE sessions (
    session_id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    film_id INTEGER REFERENCES films(film_id), 
    hall_id INTEGER REFERENCES halls(hall_id),
    cinema_id INTEGER REFERENCES cinemas(cinema_id)
);


-- Indexing on foreign keys
CREATE INDEX idx_halls_cinema_id ON halls(cinema_id);
CREATE INDEX idx_halls_technology_id ON halls(technology_id);
CREATE INDEX idx_tickets_session_id ON tickets(session_id);
CREATE INDEX idx_tickets_user_id ON tickets(user_id);
CREATE INDEX idx_sessions_film_id ON sessions(film_id);
CREATE INDEX idx_sessions_hall_id ON sessions(hall_id);
CREATE INDEX idx_sessions_cinema_id ON sessions(cinema_id);

-- Indexing on frequently filtered or joined columns
CREATE INDEX idx_sessions_date ON sessions(date);
