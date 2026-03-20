DROP TABLE IF EXISTS games_users;
DROP TABLE IF EXISTS games;
DROP TABLE IF EXISTS groups_users;
DROP TABLE IF EXISTS groups;
DROP TABLE IF EXISTS users;

---------------------------------------- CREATE

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(200) UNIQUE NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    password_hash text NOT NULL
);

CREATE TABLE groups (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    created_at timestamptz NOT NULL DEFAULT NOW(),
    status varchar(10) NOT NULL DEFAULT 'active',
    game_location text,
    game_day varchar(10) NOT NULL,
    game_time time NOT NULL,
    game_cost numeric NOT NULL,
    min_players int,
    max_players int,
    payment_link text
);

CREATE TABLE groups_users (
    user_id int,
    group_id int,
    role varchar(30) NOT NULL,
    CONSTRAINT gu_user_id FOREIGN KEY (user_id) 
        REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT gu_group_id FOREIGN KEY (group_id) 
        REFERENCES groups(id) ON DELETE CASCADE,
    PRIMARY KEY (user_id, group_id)
);

CREATE TABLE games (
    id SERIAL PRIMARY KEY,
    group_id int,
    game_location text NOT NULL,
    game_date date NOT NULL,
    game_time time NOT NULL,
    game_cost numeric NOT NULL,
    min_players int NOT NULL,
    max_players int NOT NULL,
    team_a_goals int,
    team_b_goals int,
    CONSTRAINT games_group_id FOREIGN KEY (group_id) 
        REFERENCES groups(id) ON DELETE CASCADE
);

CREATE TABLE games_users (
    user_id int,
    game_id int,
    team varchar(1) NOT NULL,
    has_paid bool NOT NULL
);

---------------------------------------- INSERT

INSERT INTO users
    (first_name, last_name, email)
VALUES
    ('Egg', '1', 'egg@man.com'),
    ('Egg', '2', 'egg1@man.com'),
    ('Egg', '3', 'egg2@man.com'),
    ('Egg', '4', 'egg3@man.com'),
    ('Egg', '5', 'egg4@man.com'),
    ('Egg', '6', 'egg5@man.com'),
    ('Egg', '7', 'egg6@man.com'),
    ('Egg', '8', 'egg7@man.com'),
    ('Egg', '9', 'egg8@man.com'),
    ('Egg', '10', 'egg9@man.com'),
    ('Egg', '11', 'egg10@man.com'),
    ('Egg', '12', 'egg11@man.com'),
    ('Egg', '13', 'egg12@man.com'),
    ('Egg', '14', 'egg13@man.com');


INSERT INTO groups
    (name, game_location, game_day, game_time, game_cost, min_players, max_players, payment_link)
VALUES
    ('Old Man Football', 'Ardwick', 'Monday', '20:00:00', 80, 14, 16, 'paypal');


INSERT INTO groups_users
    (user_id, group_id, role)
VALUES
    (1, 1, 'organiser'),
    (2, 1, 'player'),
    (3, 1, 'player'),
    (4, 1, 'player'),
    (5, 1, 'player'),
    (6, 1, 'player'),
    (7, 1, 'player'),
    (8, 1, 'player'),
    (9, 1, 'player'),
    (10, 1, 'player'),
    (11, 1, 'player'),
    (12, 1, 'player'),
    (13, 1, 'player'),
    (14, 1, 'player');


INSERT INTO games 
    (group_id, game_location, game_date, game_time, game_cost, min_players, max_players, team_a_goals, team_b_goals)
VALUES
    (1, 'Ardwick', '2025-12-29', '20:00:00', 80, 14, 16, 10, 8),
    (1, 'Ardwick', '2026-01-05', '20:00:00', 80, 14, 16, 8, 8),
    (1, 'Ardwick', '2026-01-12', '20:00:00', 80, 14, 16, 5, 8),
    (1, 'Ardwick', '2026-01-19', '20:00:00', 80, 14, 16, 10, 4);
    -- (1, 'Ardwick', '2026-01-26', '20:00:00', 80, 14, 16, 10, 13),
    -- (1, 'Ardwick', '2026-02-02', '20:00:00', 80, 14, 16, 10, 8),
    -- (1, 'Ardwick', '2026-02-09', '20:00:00', 80, 14, 16, 2, 5),
    -- (1, 'Ardwick', '2026-02-16', '20:00:00', 80, 14, 16, 10, 8),
    -- (1, 'Ardwick', '2026-02-23', '20:00:00', 80, 14, 16, 4, 7),
    -- (1, 'Ardwick', '2026-03-02', '20:00:00', 80, 14, 16, 8, 6);


INSERT INTO games_users 
    (user_id, game_id, team, has_paid)
VALUES
    (1, 1, 'a', True),
    (2, 1, 'a', True),
    (3, 1, 'a', True),
    (4, 1, 'a', True),
    (5, 1, 'a', True),
    (6, 1, 'a', True),
    (7, 1, 'a', True),
    (8, 1, 'b', True),
    (9, 1, 'b', True),
    (10, 1, 'b', True),
    (11, 1, 'b', True),
    (12, 1, 'b', True),
    (13, 1, 'b', True),
    (14, 1, 'b', True),

    (1, 2, 'a', True),
    (2, 2, 'a', True),
    (3, 2, 'a', True),
    (4, 2, 'a', True),
    (5, 2, 'a', True),
    (6, 2, 'a', True),
    (7, 2, 'a', True),
    (8, 2, 'b', True),
    (9, 2, 'b', True),
    (10, 2, 'b', True),
    (11, 2, 'b', True),
    (12, 2, 'b', True),
    (13, 2, 'b', True),
    (14, 2, 'b', True),


    (1, 3, 'a', True),
    (2, 3, 'a', True),
    (3, 3, 'a', True),
    (4, 3, 'a', True),
    (5, 3, 'a', True),
    (6, 3, 'a', True),
    (7, 3, 'a', True),
    (8, 3, 'b', True),
    (9, 3, 'b', True),
    (10, 3, 'b', True),
    (11, 3, 'b', True),
    (12, 3, 'b', True),
    (13, 3, 'b', True),
    (14, 3, 'b', True),

    (1, 4, 'a', True),
    (2, 4, 'a', True),
    (3, 4, 'a', True),
    (4, 4, 'a', True),
    (5, 4, 'a', True),
    (6, 4, 'a', True),
    (7, 4, 'a', True),
    (8, 4, 'b', True),
    (9, 4, 'b', True),
    (10, 4, 'b', True),
    (11, 4, 'b', True),
    (12, 4, 'b', True),
    (13, 4, 'b', True),
    (14, 4, 'b', True);