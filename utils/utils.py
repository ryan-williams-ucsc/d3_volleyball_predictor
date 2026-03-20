import sqlite3
#import requests
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from utils.config import DB_PATH, REQUEST_DELAY, BASE_URL


def get_connection():
    # Checks the connection of the db from DB_PATH specified in config.py
    con = sqlite3.connect(DB_PATH)
    con.execute('PRAGMA foreign_keys = ON')
    return con

def make_request(url):
    time.sleep(REQUEST_DELAY)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)
    html = driver.page_source
    driver.quit()
    return html