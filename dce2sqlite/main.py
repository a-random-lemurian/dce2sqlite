import ijson
import sqlite3
import argparse
import json

def create_indexes(db, cur):
    cur.execute(
        """
            CREATE INDEX idx_messages ON messages (
                authorname ASC,
                authordiscrim ASC,
                authornick ASC,
                content ASC
            );
        """
    )

def main(args, infile, outfile):
    db = sqlite3.connect(outfile)
    cur = db.cursor()

    if not args.append:
        cur.execute("DROP TABLE IF EXISTS messages")
        cur.execute(
            """
                CREATE TABLE IF NOT EXISTS messages (
                id INTEGER,
                type TEXT,
                timestamp TEXT,
                timestampEdited TEXT,
                callEndedTimestamp TEXT,
                isPinned INTEGER,
                content TEXT,

                authorid INTEGER,
                authorname TEXT,
                authordiscrim INTEGER,
                authornick TEXT,
                authorisbot INTEGER,
                authoravatarurl TEXT,
                authornamecolor TEXT,

                rawJSON TEXT,
                numID INTEGER PRIMARY KEY AUTOINCREMENT
            );
            """
        )

    f = open(infile, "r")
    objects = ijson.items(f, "messages.item")
    obj = iter(objects)

    print("Lemuria / dcejson -> sqlite")
    print("Conversion in progress.....")
    for i, itm in enumerate(obj):
        print(f"Processed message {i}                              ", end="\r")
        author = itm.get("author")
        cur.execute(
            """
         INSERT INTO messages (
            id,
            type,
            timestamp,
            timestampEdited,
            callEndedTimestamp,
            isPinned,
            content,

            authorid,
            authorname,
            authordiscrim,
            authornick,
            authorisbot,
            authoravatarurl,
            authornamecolor,

            rawJSON
         )
         VALUES (
             ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?
         )
         """,
            (
                itm.get("id"),
                itm.get("type"),
                itm.get("timestamp"),
                itm.get("timestampEdited"),
                itm.get("callEndedTimestamp"),
                itm.get("isPinned"),
                itm.get("content"),
                author.get("id"),
                author.get("name"),
                author.get("discriminator"),
                author.get("nickname"),
                author.get("isBot"),
                author.get("avatarUrl"),
                author.get("color"),
                json.dumps(itm),
            ),
        )
    print(f"Processed {i} messages.")

    if args.index:
        print("Creating index")
        create_indexes(db, cur)

    db.commit()


def entry():
    parser = argparse.ArgumentParser(
        description="Convert DCE .json output files into SQLite databases."
    )
    parser.add_argument("input", help="Path to input file.")
    parser.add_argument("-f", "--infile", help="Path to input file")
    parser.add_argument(
        "-o",
        "--output",
        help="Path to output file",
        default="ExportedDiscordMessages.db",
    )
    parser.add_argument(
        "-a",
        "--append",
        help="Append to already existing SQLite database (specified with -o)",
        action="store_true"
    )
    parser.add_argument(
        "-i",
        "--index",
        help="Create an index on the resulting database",
        action="store_true"
    )

    args = parser.parse_args()
    main(args, args.input, args.output)

if __name__ == '__entry__':
    entry()
