# Структура бази даних | Database Structure

## База з фільмами (movies_db) | Database of Movies (movies_db)

### Fact Table | Основна таблиця

- Фільми | Movies:
  - `film_id` (PK)
  - `duration`
  - `technology_id` (FK)
  - `genre_id` (FK)
  - `category_id` (FK)

### Dimension Tables | Таблиці розмірностей

- Локалізована назва та опис | Localized Title and Description:
  - `film_localized_id` (PK)
  - `film_id` (FK)
  - `language`
  - `title`
  - `description`
- Технології | Technologies:
  - `technology_id` (PK)
  - `technology_name`
- Жанри | Genres:
  - `genre_id` (PK)
  - `genre_name`
- Категорії | Categories:
  - `category_id` (PK)
  - `category_name`

### Індексація | Indexing

- `idx_film_localizations_film_id` на `film_localizations(film_id)`
- `idx_films_technology_id` на `films(technology_id)`
- `idx_films_genre_id` на `films(genre_id)`
- `idx_films_category_id` на `films(category_id)`

## База з розкладом (schedule_db) | Schedule Database (schedule_db)

### Fact Table | Основна таблиця

- Сеанси | Showtimes:
  - `session_id` (PK)
  - `date`
  - `start_time`
  - `end_time`
  - `film_id` (FK)
  - `hall_id` (FK)
  - `cinema_id` (FK)

### Dimension Tables | Таблиці розмірностей

- Кінотеатри | Cinemas:
  - `cinema_id` (PK)
  - `localized_name`
  - `localized_address`
- Кінозали |  Cinema halls:
  - `hall_id` (PK)
  - `cinema_id` (FK)
  - `technology_id` (FK)
  - `status`
  - `available_seats`
- Квитки | Tickets:
  - `ticket_id` (PK)
  - `session_id` (FK)
  - `row`
  - `seat_number`
  - `user_id` (FK)
  - `purchase_time`

### Індексація | Indexing

- `idx_halls_cinema_id` на `halls(cinema_id)`
- `idx_halls_technology_id` на `halls(technology_id)`
- `idx_tickets_session_id` на `tickets(session_id)`
- `idx_tickets_user_id` на `tickets(user_id)`
- `idx_sessions_film_id` на `sessions(film_id)`
- `idx_sessions_hall_id` на `sessions(hall_id)`
- `idx_sessions_cinema_id` на `sessions(cinema_id)`
- `idx_sessions_date` на `sessions(date)`

## База з користувачами (users_db) | Users Database (users_db)

### Fact Table | Основна таблиця

- Замовлення | Order:
  - `order_id` (PK)
  - `user_id` (FK)
  - `ticket_id` (FK) 
  - `transaction_id` (FK)

### Dimension Tables | Таблиці розмірностей

- Користувачі | Users:
  - `user_id` (PK)
  - `phone_number`
  - `email`
  - `is_verified`
- Профілі | Profiles:
  - `profile_id` (PK)
  - `user_id` (FK)
  - `additional_info` (наприклад, дата народження, адреса тощо) | (e.g., date of birth, address, etc.)
- Транзакції | Transactions:
  - `transaction_id` (PK)
  - `user_id` (FK)
  - `amount`
  - `transaction_date`
  - `transaction_type`

### Індексація | Indexing

- `idx_profiles_user_id` на `profiles(user_id)`
- `idx_transactions_user_id` на `transactions(user_id)`
- `idx_orders_user_id` на `orders(user_id)`
- `idx_orders_ticket_id` на `orders(ticket_id)`
- `idx_orders_transaction_id` на `orders(transaction_id)`
- `idx_users_email` на `users(email)`
- `idx_transactions_date` на `transactions(transaction_date)`

## DWH на PostgreSQL | DWH on PostgreSQL

PostgreSQL може використовуватися як OLTP та OLAP система, але тільки на короткий період часу. Через це, я щодня буду відправляти дані до Hive як холодне сховище DWH.

PostgreSQL can be used as both an OLTP and OLAP system, but only for a short period. Because of this, I will be sending data to Hive daily as a cold storage DWH.

### Налаштування сховища даних на PostgreSQL | Setting up the data warehouse on PostgreSQL

#### Dimension Tables (Таблиці розмірностей)

- **UserDim**
  - `user_dim_id` (PK)
  - `user_id`
  - `phone_number`
  - `email`
  - `is_verified`
  - `additional_info`

- **CinemaDim**
  - `cinema_dim_id` (PK)
  - `cinema_id`
  - `localized_name`
  - `localized_address`

- **FilmDim**
  - `film_dim_id` (PK)
  - `film_id`
  - `duration`
  - `technology_name`
  - `genre_name`
  - `category_name`

- **SessionDim**
  - `session_dim_id` (PK)
  - `session_id`
  - `date`
  - `start_time`
  - `end_time`
  - `hall_status`
  - `available_seats`

#### Fact Tables (Основні таблиці)

- **SalesFact**
  - `sales_fact_id` (PK)
  - `cinema_id` (FK)
  - `user_id` (FK)
  - `session_id` (FK)
  - `ticket_id`
  - `transaction_id`
  - `sales_amount`
  - `transaction_date`

- **TicketsFact**
  - `tickets_fact_id` (PK)
  - `session_id` (FK)
  - `cinema_id` (FK)
  - `film_id` (FK)
  - `ticket_id`
  - `purchase_date`


### Індексація | Indexing

Щоб оптимізувати швидкість запитів до бази даних, ми створюємо індекси для ключових полів.

To optimize the speed of database queries, we create indexes for key fields.

- **UserDim**
  - `CREATE INDEX idx_userdim_user_id ON UserDim(user_id);`

- **CinemaDim**
  - `CREATE INDEX idx_cinemadim_cinema_id ON CinemaDim(cinema_id);`

- **FilmDim**
  - `CREATE INDEX idx_filmdim_film_id ON FilmDim(film_id);`

- **SessionDim**
  - `CREATE INDEX idx_sessiondim_session_id ON SessionDim(session_id);`
  - `CREATE INDEX idx_sessiondim_date ON SessionDim(date);`

- **SalesFact**
  - `CREATE INDEX idx_salesfact_cinema_id ON SalesFact(cinema_id);`
  - `CREATE INDEX idx_salesfact_user_id ON SalesFact(user_id);`
  - `CREATE INDEX idx_salesfact_session_id ON SalesFact(session_id);`
  - `CREATE INDEX idx_salesfact_transaction_date ON SalesFact(transaction_date);`

- **TicketsFact**
  - `CREATE INDEX idx_ticketsfact_session_id ON TicketsFact(session_id);`
  - `CREATE INDEX idx_ticketsfact_cinema_id ON TicketsFact(cinema_id);`
  - `CREATE INDEX idx_ticketsfact_film_id ON TicketsFact(film_id);`
  - `CREATE INDEX idx_ticketsfact_purchase_date ON TicketsFact(purchase_date);`



## DWH в Hive | DWH in Hive

Hive є фреймворком для обробки великих масивів даних, що зберігаються в Hadoop. Використовуючи Hive, можна створювати зовнішні таблиці та здійснювати запити до даних, які зберігаються в Hadoop.

Hive is a framework for processing large datasets stored in Hadoop. Using Hive, one can create external tables and query data stored in Hadoop.

### Створення таблиць DWH в Hive | Creating DWH tables in Hive

#### Dimension Tables (Таблиці розмірностей)

- **UserDim**:
  ```
  CREATE EXTERNAL TABLE UserDim (
      user_dim_id BIGINT,
      user_id INT,
      phone_number STRING,
      email STRING,
      is_verified BOOLEAN,
      additional_info STRING
  ) ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t' STORED AS TEXTFILE;
  ```

- **CinemaDim**:
  ```
  CREATE EXTERNAL TABLE CinemaDim (
      cinema_dim_id BIGINT,
      cinema_id INT,
      localized_name STRING,
      localized_address STRING
  ) ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t' STORED AS TEXTFILE;
  ```

- **FilmDim**:
  ```
  CREATE EXTERNAL TABLE FilmDim (
      film_dim_id BIGINT,
      film_id INT,
      duration INT,
      technology_name STRING,
      genre_name STRING,
      category_name STRING
  ) ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t' STORED AS TEXTFILE;
  ```

- **SessionDim**:
  ```
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
  ```

#### Fact Tables (Основні таблиці)

- **SalesFact**:
  ```
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
  ```

- **TicketsFact**:
  ```
  CREATE EXTERNAL TABLE TicketsFact (
      tickets_fact_id BIGINT,
      session_id INT,
      cinema_id INT,
      film_id INT,
      ticket_id INT
  )
  PARTITIONED BY (purchase_date STRING, year INT, month INT)
  ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t' STORED AS TEXTFILE;
  ```

