import os
from pathlib import Path
import sqlite3 as sql
from datetime import datetime as dt

HOME = str(Path(os.getcwd()).parent / "data")

conn = sql.connect(f'{HOME}/database.db')
print("Opened database successfully")

conn.execute('CREATE TABLE loops (date text, wage int, bags int)')
print("Table created successfully")
conn.close()

with sql.connect(f'{HOME}/database.db') as con:
    date = dt.now().strftime("%m-%d")
    cur = con.cursor()

    cur.execute(f"INSERT INTO loops (date, wage,bags) VALUES (?,?,?)", ("01-16",170,1))
    cur.execute(f"INSERT INTO loops (date, wage,bags) VALUES (?,?,?)", ("01-21",290,2))
    cur.execute(f"INSERT INTO loops (date, wage,bags) VALUES (?,?,?)", ("01-22",520,4))
    cur.execute(f"INSERT INTO loops (date, wage,bags) VALUES (?,?,?)", ("01-29",300,2))
    cur.execute(f"INSERT INTO loops (date, wage,bags) VALUES (?,?,?)", ("01-30",125,1))
    cur.execute(f"INSERT INTO loops (date, wage,bags) VALUES (?,?,?)", ("02-11",140,1))
    cur.execute(f"INSERT INTO loops (date, wage,bags) VALUES (?,?,?)", ("02-12",160,1))
    cur.execute(f"INSERT INTO loops (date, wage,bags) VALUES (?,?,?)", ("02-13",220,2))

    con.commit()
