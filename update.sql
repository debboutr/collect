create table groups ( group_id INTEGER PRIMARY KEY, name TEXT NOT NULL);
ALTER TABLE loops ADD COLUMN group_id INTEGER;
create table people ( id INTEGER PRIMARY KEY, first_name TEXT NOT NULL, last_name TEXT NOT NULL, notes TEXT, lat REAL, lon REAL, group_id INTEGER NOT NULL);
UPDATE loops set group_id=1 where group_id IS NULL;
INSERT INTO groups (name) VALUES ("unknown");
INSERT INTO people (first_name, last_name, group_id) VALUES ("unknown", "soldier", 1);
