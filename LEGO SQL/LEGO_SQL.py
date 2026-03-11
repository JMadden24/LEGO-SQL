import sqlite3
from pathlib import Path
import sys
from token import NAME


def get_app_directory():
    """
    Returns the directory where the script or executable lives.
    Works for both .py and PyInstaller .exe.
    """
    if getattr(sys, "frozen", False):  # running as packaged exe
        return Path(sys.executable).parent
    else:  # running as script
        return Path(__file__).parent


def initialize_database():
    # Create folder next to executable
    base_dir = get_app_directory()
    db_folder = base_dir / "LEGO Database"
    db_folder.mkdir(exist_ok=True)

    db_path = db_folder / "lego.db"

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Create tables
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Sets (
        set_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        theme TEXT,
        subtheme TEXT,
        piece_count INTEGER,
        minifigure_count INTEGER,
        instruction_book_count INTEGER
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS Minifigures (
        fig_id INTEGER PRIMARY KEY AUTOINCREMENT,
        set_id TEXT NOT NULL,
        name TEXT NOT NULL,
        variant TEXT,
        FOREIGN KEY(set_id) REFERENCES Sets(set_id)
    )
    """)

    conn.commit()
    conn.close()

    return db_path

def AddNewKit():

    db_path = Path("LEGO Database") / "lego.db"
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    set_id = input("Enter set ID: ")
    name = input("Enter set name: ")
    theme = input("Enter set theme: ")
    subtheme = input("Enter set subtheme: ")
    pieces = int(input("Enter number of pieces: "))
    figs = int(input("Enter number of minifigures: "))
    books = int(input("Enter number of instruction books: "))
    cur.execute(
        "INSERT INTO Sets VALUES (?, ?, ?, ?, ?, ?, ?)",
        (set_id, name, theme, subtheme, pieces, figs, books)
    )
    conn.commit()

    for _ in range(figs):
        AddMinifigure(set_id)

def AddMinifigure(set_id):
    db_path = Path("LEGO Database") / "lego.db"
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    mini_name = input("Enter Minifigure name: ")
    variant = input("Enter Minifigure variation: ")
    cur.execute(
        "INSERT INTO Minifigures (set_id, name, variant) VALUES (?, ?, ?)",
        (set_id, mini_name, variant)
    )
    conn.commit()

def viewData():
    db_path = Path("LEGO Database") / "lego.db"
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT * FROM Sets")
    result=cur.fetchall()

    print("\n\nSets Table:")

    for row in result:
        print(row)

    print("\n\nMinifigures Table:")

    cur.execute("SELECT * FROM Minifigures")
    result=cur.fetchall()

    for row in result:
        print(row)

def Menu():
    while True:
        print("LEGO SQL Database \n1: Manage database \n2: View database")
        menuOption = input("Enter number (1-2): ")
        if menuOption == "1":
            print("Manage Database:\n1: Add new kit \n2: Add new minifigure \n3: Add broken piece \n4: Back")
            menu2Option = input("Enter number (1-4): ")
            if menu2Option == "1":
                AddNewKit()
            elif menu2Option == "2":
                AddMinifigure(input("Enter set ID: "))
            elif menu2Option == "3":
                print("Need to add borken pieces table")
            elif menu2Option == "4":
                continue
            else:
                print("Invalid input.\n\n\n")
        elif menuOption == "2":
            viewData()
        else:
            print("\n\nPlease enter a valid option:\n")
    
if __name__ == "__main__":  
    db_path = Path("LEGO Database") / "lego.db"

    if db_path.exists():
        print("Database already exists.")
    else:
        print("Creating database...")
        path = initialize_database()
        print("Database created.")

    Menu()

    
    