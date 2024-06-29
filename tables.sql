CREATE TABLE "dir_source" (
	"id"	INTEGER NOT NULL,
	"task_name"	TEXT NOT NULL,
	"dir_path"	TEXT NOT NULL,
	"active"	INTEGER NOT NULL,
	"latest_hash"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
)


CREATE TABLE "dir_destination" (
	"id"	INTEGER NOT NULL UNIQUE,
	"dir_source_id"	INTEGER NOT NULL,
	"dir_path"	TEXT NOT NULL,
	"active"	INTEGER NOT NULL,
	"latest_source_hash"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
)