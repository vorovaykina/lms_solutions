CREATE TABLE rooms (
    id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE students (
    id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    birthday TIMESTAMP NOT NULL,
    sex CHAR(1) NOT NULL,
    room_id INT REFERENCES rooms(id) ON DELETE CASCADE
);