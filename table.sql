CREATE TABLE "dirs_to_hash" (
	"id"	INTEGER NOT NULL,
	"dir_path"	TEXT NOT NULL,
	"active"	INTEGER NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
)


CREATE TABLE "dir_hashes" (
	"id"	INTEGER NOT NULL UNIQUE,
	"dir_path"	TEXT NOT NULL,
	"hash"	TEXT NOT NULL,
	PRIMARY KEY("id")
)