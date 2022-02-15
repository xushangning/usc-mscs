-- http://sqlfiddle.com/#!17/27a57/15
CREATE TABLE "Candidates" (
    "Instructor" VARCHAR(5) NOT NULL,
    "Subject" VARCHAR(10) NOT NULL,
    PRIMARY KEY ("Instructor", "Subject")
);
    
INSERT INTO "Candidates"
    ("Instructor", "Subject")
VALUES
    ('Aleph', 'Scratch'),
    ('Aleph', 'Java'),
    ('Aleph', 'Processing'),
    ('Bit', 'Python'),
    ('Bit', 'JavaScript'),
    ('Bit', 'Java'),
    ('CRC', 'Python'),
    ('CRC', 'JavaScript'),
    ('Dat', 'Scratch'),
    ('Dat', 'Python'),
    ('Dat', 'JavaScript'),
    ('Emscr', 'Scratch'),
    ('Emscr', 'Processing'),
    ('Emscr', 'JavaScript'),
    ('Emscr', 'Python')
;

-- Answer:
-- We implement the quotient relational algebra operator here.
-- (5) A table of all instructors, same as (1)
SELECT DISTINCT "Instructor" FROM "Candidates"
-- (6) Remove, from all instructors, the instructors that don't teach all three subjects, yielding the final result.
EXCEPT ALL
SELECT DISTINCT "Instructor" FROM (
    SELECT * FROM   -- (3) Construct all combinaton of instructors and the three subjects.
        (SELECT DISTINCT "Instructor" FROM "Candidates") AS t1,             -- (1) A table of all instructors
        (VALUES ('JavaScript'), ('Scratch'), ('Python')) AS t2 ("Subject")  -- (2) All subjects we are looking for
    -- (4) Remove instructors that teach all three subjects, leaving instructors that teach don't teach all subjects.
    EXCEPT ALL
    SELECT * FROM "Candidates"
) AS t3;
