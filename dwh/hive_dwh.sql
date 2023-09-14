-- Dimension Tables

CREATE EXTERNAL TABLE UserDim (
    user_dim_id BIGINT,
    user_id INT,
    phone_number STRING,
    email STRING,
    is_verified BOOLEAN,
    additional_info STRING
) ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t' STORED AS TEXTFILE;

CREATE EXTERNAL TABLE CinemaDim (
    cinema_dim_id BIGINT,
    cinema_id INT,
    localized_name STRING,
    localized_address STRING
) ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t' STORED AS TEXTFILE;

CREATE EXTERNAL TABLE FilmDim (
    film_dim_id BIGINT,
    film_id INT,
    duration INT,
    technology_name STRING,
    genre_name STRING,
    category_name STRING
) ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t' STORED AS TEXTFILE;

CREATE EXTERNAL TABLE SessionDim (
    session_dim_id BIGINT,
    session_id INT,
    date STRING, 
    start_time STRING,
    end_time STRING,
    hall_status STRING,
    available_seats INT
)
PARTITIONED BY (year INT, month INT)
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t' STORED AS TEXTFILE;

-- Fact Tables

CREATE EXTERNAL TABLE SalesFact (
    sales_fact_id BIGINT,
    cinema_id INT,
    user_id INT,
    session_id INT,
    ticket_id INT,
    transaction_id INT,
    sales_amount DOUBLE
)
PARTITIONED BY (transaction_date STRING, year INT, month INT)
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t' STORED AS TEXTFILE;



CREATE EXTERNAL TABLE TicketsFact (
    tickets_fact_id BIGINT,
    session_id INT,
    cinema_id INT,
    film_id INT,
    ticket_id INT
)
PARTITIONED BY (purchase_date STRING, year INT, month INT)
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t' STORED AS TEXTFILE;

