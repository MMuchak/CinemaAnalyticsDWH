CREATE DATABASE users_db;

-- Dimension Tables
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    phone_number VARCHAR(255),
    email VARCHAR(255) UNIQUE NOT NULL,
    is_verified BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE profiles (
    profile_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id),
    additional_info JSONB
);

CREATE TABLE transactions (
    transaction_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id),
    amount DECIMAL(10, 2) NOT NULL,
    transaction_date TIMESTAMP NOT NULL,
    transaction_type VARCHAR(255)
);

-- Fact Table
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id),
    ticket_id INTEGER REFERENCES tickets(ticket_id),
    transaction_id INTEGER REFERENCES transactions(transaction_id)
);


-- Indexing on foreign keys
CREATE INDEX idx_profiles_user_id ON profiles(user_id);
CREATE INDEX idx_transactions_user_id ON transactions(user_id);
CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_orders_ticket_id ON orders(ticket_id);
CREATE INDEX idx_orders_transaction_id ON orders(transaction_id);

-- Indexing on frequently filtered or joined columns
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_transactions_date ON transactions(transaction_date);