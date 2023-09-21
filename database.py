import sqlite3
import os

def create_database():

    if not os.path.exists("portal_db.db"):
        conn = sqlite3.connect('portal_db.db')
        with open('database/schema_portal_db.sql') as f:
            conn.executescript(f.read())
        conn.close()

    if not os.path.exists("descomplica_db.db"):
        conn = sqlite3.connect('descomplica_db.db')
        with open('database/schema_descomplica_db.sql') as f:
            conn.executescript(f.read())
        conn.close()