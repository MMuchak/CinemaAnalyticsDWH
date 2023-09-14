-- Dimension Tables

CREATE TABLE UserDim (
    user_dim_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL UNIQUE,
    phone_number VARCHAR(15),
    email VARCHAR(100),
    is_verified BOOLEAN,
    additional_info TEXT
);

CREATE TABLE CinemaDim (
    cinema_dim_id SERIAL PRIMARY KEY,
    cinema_id INT NOT NULL UNIQUE,
    localized_name VARCHAR(255),
    localized_address TEXT
);

CREATE TABLE FilmDim (
    film_dim_id SERIAL PRIMARY KEY,
    film_id INT NOT NULL UNIQUE,
    duration INT,
    technology_name VARCHAR(100),
    genre_name VARCHAR(100),
    category_name VARCHAR(100)
);

CREATE TABLE SessionDim (
    session_dim_id SERIAL PRIMARY KEY,
    session_id INT NOT NULL UNIQUE,
    date DATE,
    start_time TIME,
    end_time TIME,
    hall_status VARCHAR(50),
    available_seats INT
);

-- Fact Tables

CREATE TABLE SalesFact (
    sales_fact_id SERIAL PRIMARY KEY,
    cinema_id INT REFERENCES CinemaDim(cinema_id),
    user_id INT REFERENCES UserDim(user_id),
    session_id INT REFERENCES SessionDim(session_id),
    ticket_id INT NOT NULL,
    transaction_id INT NOT NULL,
    sales_amount DECIMAL(10, 2),
    transaction_date DATE
);

CREATE TABLE TicketsFact (
    tickets_fact_id SERIAL PRIMARY KEY,
    session_id INT REFERENCES SessionDim(session_id),
    cinema_id INT REFERENCES CinemaDim(cinema_id),
    film_id INT REFERENCES FilmDim(film_id),
    ticket_id INT NOT NULL,
    purchase_date DATE
);


-- For UserDim
CREATE INDEX idx_userdim_user_id ON UserDim(user_id);

-- For CinemaDim
CREATE INDEX idx_cinemadim_cinema_id ON CinemaDim(cinema_id);

-- For FilmDim
CREATE INDEX idx_filmdim_film_id ON FilmDim(film_id);

-- For SessionDim
CREATE INDEX idx_sessiondim_session_id ON SessionDim(session_id);
CREATE INDEX idx_sessiondim_date ON SessionDim(date);

-- For SalesFact
CREATE INDEX idx_salesfact_cinema_id ON SalesFact(cinema_id);
CREATE INDEX idx_salesfact_user_id ON SalesFact(user_id);
CREATE INDEX idx_salesfact_session_id ON SalesFact(session_id);
CREATE INDEX idx_salesfact_transaction_date ON SalesFact(transaction_date);

-- For TicketsFact
CREATE INDEX idx_ticketsfact_session_id ON TicketsFact(session_id);
CREATE INDEX idx_ticketsfact_cinema_id ON TicketsFact(cinema_id);
CREATE INDEX idx_ticketsfact_film_id ON TicketsFact(film_id);
CREATE INDEX idx_ticketsfact_purchase_date ON TicketsFact(purchase_date);

