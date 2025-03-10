import json
import uuid
import sqlite3

DATABASE_FILE = "company_profiles.db"

def create_table():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS profiles (
            id TEXT PRIMARY KEY,
            data TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_profile_data(profile_data):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    profile_id = str(uuid.uuid4())
    cursor.execute('''
        INSERT INTO profiles (id, data) VALUES (?, ?)
    ''', (profile_id, json.dumps(profile_data)))
    conn.commit()
    conn.close()
    return profile_id

def load_profile_data(profile_id):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT data FROM profiles WHERE id = ?
    ''', (profile_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return json.loads(row[0])
    return None

# Create the table when the module is imported
create_table()