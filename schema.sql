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
    description TEXT
);

CREATE TABLE park_groups (
    park_id INTEGER REFERENCES Parks(id),
    group_id INTEGER REFERENCES Groups(id),
    PRIMARY KEY (park_id, group_id)
);

-- Example data

INSERT INTO users (username, password, role)
VALUES ('viiru', 'Password', 1);


INSERT INTO parks (id, name, has_separate_areas, has_entrance_area, has_beach) VALUES
(DEFAULT, 'Tervasaaren koira-aitaus', true, false, true),
(DEFAULT, 'Tokoinrannan koira-aitaus', true, false, false),
(DEFAULT, 'Pengerpuiston koira-aitaus', false, false, false),
(DEFAULT, 'Brahenpuistikon koira-aitaus', false, false, false),
(DEFAULT, 'Väinö Vähäkallion puiston koira-aitaus', true, false, false),
(DEFAULT, 'Alppipuiston koira-aitaus', true, false, false),
(DEFAULT, 'Mustikkamaan koira-aitaus', true, true, false),
(DEFAULT, 'Rajasaaren koira-aitaus', false, false, true);

INSERT INTO reviews (id, user_id, park_id, stars, comment) VALUES
(DEFAULT, 1, 7, 5, 'Kiva puisto rauhallisella paikalla. Korkeat aidat'),
(DEFAULT, 1, 8, 3, 'Hau'),
(DEFAULT, 1, 6, 3, 'Pienehkö. Rauhallinen ympäristö'),
(DEFAULT, 1, 4, 3, 'Peruspuisto ja vähän meluinen paikka'),
(DEFAULT, 1, 3, 2, 'Täällä käy pelottava husky joka kävi kerran Siiri-shiban kimppuun ja Siiri joutui eläinlääkäriin.');

INSERT INTO address (id, park_id, street, postal_code, city, latitude, longitude) VALUES
(DEFAULT, 1, 'Tervasaarenkannas 3', '00170', 'Helsinki', 60.173264, 24.967426),
(DEFAULT, 2, 'Eläintarhantie 14', '00530', 'Helsinki', 60.180702, 24.939562),
(DEFAULT, 3, 'Pengerkatu 14', '00500', 'Helsinki', 60.185356, 24.958001),
(DEFAULT, 4, 'Itäinen Brahenkatu 2', '00510', 'Helsinki', 60.189745, 24.949039),
(DEFAULT, 5, 'Sörnäisten rantatie 21', '00530', 'Helsinki', 60.183050, 24.963985),
(DEFAULT, 6, 'Viipurinkatu 31', '00520', 'Helsinki', 60.192129, 24.934546),
(DEFAULT, 7, 'Mustikkamaanpolku', '00570', 'Helsinki', 60.181149, 24.985516),
(DEFAULT, 8, 'Rajasaarenpenger 9', '00250', 'Helsinki', 60.181968, 24.905033);

INSERT INTO groups (id, name, description) VALUES
(DEFAULT, 'Luonnonläheiset puistot', 'Näissä puistoissa on koiralle paljon tutkitavaa sekä rauhallinen ympäristö'),
(DEFAULT, 'Juoksijoiden suosikit', 'Puistot koirille, jotka juoksevat paljon ja katsovat eteensä vähän.');

INSERT INTO park_groups (park_id, group_id) VALUES
(7, 1),
(8, 1),
(1, 2),
(7, 2);
