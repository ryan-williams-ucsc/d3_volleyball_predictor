import sqlite3
from utils.utils import get_connection

def create_tables():
    # Get the connection to the DB, get the cursor
    con = get_connection()
    cur = con.cursor()

    # Create the pages we need in the DB
    cur.execute('''
        CREATE TABLE IF NOT EXISTS teams (
            team_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        )
    ''')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS matches (
            match_id INTEGER PRIMARY KEY,
            date TEXT,
            season TEXT,
            team1_id INTEGER,
            team2_id INTEGER,
            winner_id INTEGER,
            sets_team1 INTEGER,
            sets_team2 INTEGER,
            FOREIGN KEY (team1_id) REFERENCES teams(team_id),
            FOREIGN KEY (team2_id) REFERENCES teams(team_id),
            FOREIGN KEY (winner_id) REFERENCES teams(team_id)
        )
    ''')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS team_stats (
            match_id INTEGER,
            team_id INTEGER,
            kills INTEGER,
            errors INTEGER,
            attacks INTEGER,
            hitting_pct REAL,
            digs INTEGER,
            blocks REAL,
            aces INTEGER,
            service_errors INTEGER,
            PRIMARY KEY (match_id, team_id),
            FOREIGN KEY (match_id) REFERENCES matches(match_id),
            FOREIGN KEY (team_id) REFERENCES teams(team_id)
        )
    ''')

    # Send the changes
    con.commit()

if __name__ == '__main__':
    create_tables()