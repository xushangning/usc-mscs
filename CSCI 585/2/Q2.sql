-- http://sqlfiddle.com/#!17/9b241/1

CREATE TABLE "enrollment" (
    "SID" INT NOT NULL,
    "ClassName" VARCHAR(32) NOT NULL,
    "Grade" CHAR(1) NOT NULL,
    PRIMARY KEY ("SID", "ClassName")
);

INSERT INTO "enrollment"
    ("SID", "ClassName", "Grade")
VALUES
    (123, 'Processing', 'A'),
    (123, 'Python', 'B'),
    (123, 'Scratch', 'B'),
    (662, 'Java', 'B'),
    (662, 'Python', 'A'),
    (662, 'JavaScript', 'A'),
    (662, 'Scratch', 'B'),
    (345, 'Scratch', 'A'),
    (345, 'JavaScript', 'B'),
    (345, 'Python', 'A'),
    (555, 'Python', 'B'),
    (555, 'JavaScript', 'B'),
    (213, 'JavaScript', 'A')
;

-- Answer:
SELECT "ClassName", COUNT(*) AS "Total"
FROM "enrollment" GROUP BY "ClassName" ORDER BY "Total" DESC;
