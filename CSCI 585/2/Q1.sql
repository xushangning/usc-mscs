-- http://sqlfiddle.com/#!17/462e1/1
DROP TABLE IF EXISTS ProjectRoomBookings;

CREATE TABLE ProjectRoomBookings (
    id SERIAL PRIMARY KEY,
    groupName CHAR(10) NOT NULL,
    at7 INT UNIQUE,     -- Number of the room to reserve at 7. Same for columns below.
    at8 INT UNIQUE,
    at9 INT UNIQUE,
    at10 INT UNIQUE,
    at11 INT UNIQUE,
    at12 INT UNIQUE,
    at13 INT UNIQUE,
    at14 INT UNIQUE,
    at15 INT UNIQUE,
    at16 INT UNIQUE,
    at17 INT UNIQUE
);

INSERT INTO ProjectRoomBookings (groupName, at7, at8, at9) VALUES ('Early Bird', 1, 1, 1);

-- Correctness
-- Book a different room.
INSERT INTO ProjectRoomBookings (groupName, at8, at9, at10) VALUES ('Different', 2, 2, 2);
-- Book another time slot by the same group
INSERT INTO ProjectRoomBookings (groupName, at15) VALUES ('Early Bird', 1);

-- Intersecting intervals
INSERT INTO ProjectRoomBookings (groupName, at8, at9) VALUES ('Subset', 1, 1);
INSERT INTO ProjectRoomBookings (groupName, at9, at10) VALUES ('Not Subset', 1, 1);

-- Reserving time out of the 7-18 time range is impossible.
