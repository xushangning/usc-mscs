-- http://sqlfiddle.com/#!17/2e308/2
CREATE TABLE "Sections" (
    "SectionID" SERIAL PRIMARY KEY,
    "Instructor" VARCHAR(32) NOT NULL,
    "Subject" VARCHAR(32) NOT NULL
);

INSERT INTO "Sections" VALUES
    (1, 'Aleph', 'Scratch'),
    (2, 'Aleph', 'Java'),
    (3, 'Aleph', 'Processing'),
    (4, 'Bit', 'Python'),
    (5, 'Bit', 'JavaScript'),
    (6, 'Bit', 'Java')
;

CREATE TABLE "Enrollment" (
    "SID" INT NOT NULL,
    "SectionID" INT NOT NULL REFERENCES "Sections",
    PRIMARY KEY ("SID", "SectionID")
);

INSERT INTO "Enrollment"
VALUES
    (123, 3),
    (123, 4),   -- A student enrolls in more than one section.
    (123, 1),
    (662, 2),
    (662, 4),
    (662, 5),
    (662, 1),
    (345, 1),
    (345, 5),
    (345, 4),
    (555, 4),
    (555, 5),
    (213, 5)
;
-- Aleph has 5 students and Bit has 8 students.

-- Answer:
SELECT "Instructor", 15 * COUNT(*) * 0.1 AS "Bonus"
FROM "Enrollment" JOIN "Sections" USING ("SectionID")
GROUP BY "Instructor" ORDER BY "Bonus" DESC LIMIT 1;
