CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    role INTEGER
);

CREATE TABLE parks (
    id SERIAL PRIMARY KEY,
    name TEXT,
    has_separate_areas BOOLEAN,
    has_entrance_area BOOLEAN,
    has_beach BOOLEAN

);

CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES Users(id),
    park_id INTEGER REFERENCES Parks(id),
    stars INTEGER,
    comment TEXT
        
);

CREATE TABLE address (
    id SERIAL PRIMARY KEY,
    park_id INTEGER REFERENCES Parks(id),
    street TEXT,
    postal_code VARCHAR(5),
    city TEXT,
    coordinates POINT
);

