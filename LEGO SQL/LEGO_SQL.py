import sqlite3
import os

# Get the directory of this script
project_dir = os.path.dirname(os.path.abspath(__file__))

# Database file path
db_path = os.path.join(project_dir, "LEGO_sql_database.db")

# Connect to the database (it will create the file if it doesn't exist)
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("PRAGMA foreign_keys = ON")

# Example: Create a table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Kits (
    KitID INTEGER PRIMARY KEY,
    Name TEXT NOT NULL,
    Theme TEXT NOT NULL,
    Subtheme TEXT NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Minifigures (
    MinifigureID INTEGER PRIMARY KEY,
    Name TEXT NOT NULL,
    Variation TEXT NOT NULL,
    Quantity INTEGER
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS KitMinifigures (
    MinifigureID INTEGER NOT NULL,
    KitID INTERGER NOT NULL,
    FOREIGN KEY (MinifigureID) REFERENCES Minifigures(MinifigureID)
        ON DELETE CASCADE
        ON UPDATE CASCADE
    FOREIGN KEY (KitID) REFERENCES Kits(KitID)
        ON DELETE CASCADE
        ON UPDATE CASCADE
)
''')

# Commit and close the connection
conn.commit()
conn.close()

print(f"Database created at: {db_path}")
