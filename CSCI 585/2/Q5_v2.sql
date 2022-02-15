-- http://sqlfiddle.com/#!17/27a57/17
SELECT "Instructor"
-- Pick out instructors that teach at least one of the three subjects.
FROM "Candidates" WHERE "Subject" IN (VALUES ('JavaScript'), ('Scratch'), ('Python'))
GROUP BY "Instructor"   -- Count the number of the three subjects each instructor teaches.
-- Filter out instructors that don't teach all three subjects.
HAVING COUNT(*) = (SELECT COUNT(*) FROM (VALUES ('JavaScript'), ('Scratch'), ('Python')) AS t1)
