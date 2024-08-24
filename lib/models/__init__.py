# lib/config.py
import sqlite3

CONN = sqlite3.connect('sightseeing.db')
CURSOR = CONN.cursor()
