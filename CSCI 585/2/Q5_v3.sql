-- http://sqlfiddle.com/#!17/27a57/24
SELECT DISTINCT "Instructor" FROM "Candidates" AS t1    -- For each instructor,
WHERE NOT EXISTS (
    VALUES ('JavaScript'), ('Scratch'), ('Python')      -- given the table of subjects,
    EXCEPT ALL
    -- if they don't teach cover all subjects, there will be rows left for the EXISTS query.
    SELECT "Subject" FROM "Candidates" WHERE "Instructor" = t1."Instructor"
)
