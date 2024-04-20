CREATE TYPE weekday AS ENUM ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday');

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
    latitude NUMERIC,
    longitude NUMERIC
);

CREATE TABLE groups (
    id SERIAL PRIMARY KEY,
    name TEXT,
    weekday weekday,  
    time TIME,           
    description TEXT
);

CREATE TABLE park_groups (
    park_id INTEGER REFERENCES Parks(id),
    group_id INTEGER REFERENCES Groups(id),
    PRIMARY KEY (park_id, group_id)
);
