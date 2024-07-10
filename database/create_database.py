import sqlite3
import json

def create_database():
    conn = sqlite3.connect('travel_database.db')
    cursor = conn.cursor()

    # Create tables
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS travel_agents (
        agent_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        phone TEXT,
        website TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS destinations (
        destination_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        country TEXT NOT NULL,
        description TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS travel_packages (
        package_id INTEGER PRIMARY KEY,
        agent_id INTEGER,
        destination_id INTEGER,
        name TEXT NOT NULL,
        description TEXT,
        duration_days INTEGER NOT NULL,
        price DECIMAL(10, 2) NOT NULL,
        FOREIGN KEY (agent_id) REFERENCES travel_agents (agent_id),
        FOREIGN KEY (destination_id) REFERENCES destinations (destination_id)
    )
    ''')

    # Load sample data from JSON file
    with open('sample_data.json', 'r') as f:
        sample_data = json.load(f)

    # Insert sample data
    for agent in sample_data['travel_agents']:
        cursor.execute('''
        INSERT INTO travel_agents (name, email, phone, website)
        VALUES (?, ?, ?, ?)
        ''', (agent['name'], agent['email'], agent['phone'], agent['website']))

    for destination in sample_data['destinations']:
        cursor.execute('''
        INSERT INTO destinations (name, country, description)
        VALUES (?, ?, ?)
        ''', (destination['name'], destination['country'], destination['description']))

    for package in sample_data['travel_packages']:
        cursor.execute('''
        INSERT INTO travel_packages (agent_id, destination_id, name, description, duration_days, price)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (package['agent_id'], package['destination_id'], package['name'], 
              package['description'], package['duration_days'], package['price']))

    conn.commit()
    conn.close()

    print("Database created and sample data inserted successfully.")

if __name__ == "__main__":
    create_database()