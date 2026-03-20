import sqlite3
import requests
import time
from config import DB_PATH, REQUEST_DELAY

def get_connection():
    # Checks the connection of the db from DB_PATH specified in config.py
    con = sqlite3.connect(DB_PATH)
    return con

def make_request(url):
    time.sleep(REQUEST_DELAY)
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0'}
    r = requests.get(url)
    return r if r.status_code == 200 else None