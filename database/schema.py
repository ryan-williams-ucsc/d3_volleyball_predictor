import sqlite3
from utils.utils import get_connection
from utils.config import SEASON_IDS

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

def insert_team(team_id, team_name):
    con = get_connection()
    cur = con.cursor()
    cur.execute('INSERT OR IGNORE INTO teams VALUES (?, ?)', (team_id, team_name))
    con.commit()
    con.close()

def insert_match(match_id, season_id, game_stats):
    con = get_connection()
    cur = con.cursor()
    cur.execute('INSERT OR IGNORE INTO matches VALUES (?, ?, ?, ?, ?, ?, ?, ?)', 
                (match_id, game_stats['date'], SEASON_IDS[season_id], game_stats['team1_id'], game_stats['team2_id'], game_stats['winner_id'], game_stats['team1_sets'],
                 game_stats['team2_sets']))
    con.commit()
    con.close()


def insert_team_stats(match_id, team_id, game_stats):
    # Need to determine, are we team1 or team2 for this match
    team_stats = 'team1_stats'
    if team_id == game_stats['team2_id']:
        team_stats = 'team2_stats'
    con = get_connection()
    cur = con.cursor()
    cur.execute('INSERT OR IGNORE INTO team_stats VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', 
                (match_id, team_id, game_stats[team_stats]['kills'], game_stats[team_stats]['errors'], game_stats[team_stats]['attacks'], game_stats[team_stats]['hitting_pct'], 
                 game_stats[team_stats]['digs'], game_stats[team_stats]['blocks'], game_stats[team_stats]['aces'], game_stats[team_stats]['service_errors']))
    con.commit()
    con.close()

if __name__ == '__main__':
    create_tables()