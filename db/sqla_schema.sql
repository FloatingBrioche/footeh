CREATE TABLE users (
        id SERIAL NOT NULL, 
        first_name VARCHAR(100) NOT NULL, 
        last_name VARCHAR(100) NOT NULL, 
        email VARCHAR(200) NOT NULL, 
        created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now() NOT NULL, 
        password_hash VARCHAR(256) NOT NULL, 
        PRIMARY KEY (id), 
        CONSTRAINT email_check CHECK (email LIKE '%%@%%')
);

CREATE TABLE groups (
        id SERIAL NOT NULL, 
        name VARCHAR(100) NOT NULL, 
        join_code VARCHAR(21) NOT NULL, 
        created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now() NOT NULL, 
        status VARCHAR(10) DEFAULT 'active' NOT NULL, 
        game_location TEXT NOT NULL, 
        game_day VARCHAR(10) NOT NULL, 
        game_time TIME WITHOUT TIME ZONE NOT NULL, 
        game_cost NUMERIC(10, 2) NOT NULL, 
        min_players INTEGER, 
        max_players INTEGER, 
        payment_link TEXT, 
        PRIMARY KEY (id), 
        CONSTRAINT game_day_check CHECK (game_day IN ('Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday')), 
        UNIQUE (name)
);

CREATE TABLE memberships (
        id SERIAL NOT NULL, 
        user_id INTEGER NOT NULL, 
        group_id INTEGER NOT NULL, 
        joined_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_DATE NOT NULL, 
        role VARCHAR(20) DEFAULT 'player' NOT NULL, 
        status VARCHAR(10) DEFAULT 'active' NOT NULL, 
        PRIMARY KEY (id), 
        FOREIGN KEY(user_id) REFERENCES users (id) ON DELETE CASCADE, 
        FOREIGN KEY(group_id) REFERENCES groups (id) ON DELETE CASCADE
);

CREATE TABLE leagues (
        id SERIAL NOT NULL, 
        name VARCHAR(100) NOT NULL, 
        group_id INTEGER NOT NULL, 
        start_date DATE DEFAULT CURRENT_DATE NOT NULL, 
        end_date DATE DEFAULT CURRENT_DATE + INTERVAL '6 months' NOT NULL, 
        PRIMARY KEY (id), 
        CONSTRAINT end_date_check CHECK (end_date > start_date), 
        FOREIGN KEY(group_id) REFERENCES groups (id) ON DELETE CASCADE
);

CREATE TABLE games (
        id SERIAL NOT NULL, 
        group_id INTEGER NOT NULL, 
        league_id INTEGER, 
        game_location TEXT NOT NULL, 
        game_date DATE NOT NULL, 
        game_time TIME WITHOUT TIME ZONE NOT NULL, 
        game_cost NUMERIC(10, 2) NOT NULL, 
        min_players INTEGER, 
        max_players INTEGER, 
        team_a_goals INTEGER, 
        team_b_goals INTEGER, 
        PRIMARY KEY (id), 
        FOREIGN KEY(group_id) REFERENCES groups (id) ON DELETE CASCADE, 
        FOREIGN KEY(league_id) REFERENCES leagues (id) ON DELETE SET NULL
);

CREATE TABLE appearances (
        id SERIAL NOT NULL, 
        user_id INTEGER NOT NULL, 
        game_id INTEGER NOT NULL, 
        team VARCHAR(1) NOT NULL, 
        has_paid BOOLEAN DEFAULT false NOT NULL, 
        PRIMARY KEY (id), 
        CONSTRAINT team_check CHECK (team IN ('A','B')), 
        FOREIGN KEY(user_id) REFERENCES users (id) ON DELETE CASCADE, 
        FOREIGN KEY(game_id) REFERENCES games (id) ON DELETE CASCADE
);