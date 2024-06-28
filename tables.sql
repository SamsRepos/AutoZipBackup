CREATE TABLE "dirs" (
	"id"	INTEGER NOT NULL,
	"task_name"	TEXT NOT NULL,
	"dir_path"	TEXT NOT NULL,
	"active"	INTEGER NOT NULL,
	"destination_paths"	TEXT NOT NULL,
	"latest_hash"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
)