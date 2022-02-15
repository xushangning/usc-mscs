-- http://sqlfiddle.com/#!17/960ff/2
CREATE TABLE "ProjectStatus" (
    "PID" VARCHAR(8) NOT NULL,
    "Step" INT NOT NULL,
    "Status" CHAR(1) NOT NULL
);
    
INSERT INTO "ProjectStatus"
    ("PID", "Step", "Status")
VALUES
    ('P100', 0, 'C'),
    ('P100', 1, 'W'),
    ('P100', 2, 'W'),
    ('P201', 0, 'C'),
    ('P201', 1, 'C'),
    ('P333', 0, 'W'),
    ('P333', 1, 'W'),
    ('P333', 2, 'W'),
    ('P333', 3, 'W')
;

-- Answer:
SELECT "PID" FROM "ProjectStatus"
    WHERE "Step" = 0 AND "Status" = 'C'
EXCEPT ALL SELECT "PID" FROM "ProjectStatus"
    WHERE "Step" = 1 AND "Status" = 'C';
