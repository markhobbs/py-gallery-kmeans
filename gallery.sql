-- IMAGES TABLE
CREATE TABLE images (
    uid INTEGER,
    filename TEXT NOT NULL,
    type TEXT NOT NULL,
    ext TEXT NOT NULL,
    colors BLOB,
    description TEXT,
    Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY("uid" AUTOINCREMENT)
);

CREATE UNIQUE INDEX `idx_uid`
    ON `images` (`uid`);

-- DUMMY DATA
-- INSERT INTO "images" VALUES
-- (null,'test.jpg','image','jpg','colors', 'description', 'timestamp')
