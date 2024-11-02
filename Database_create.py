import sqlite3

def create_database():
    # Connect to the SQLite database (it will create 'database.db' if it doesn't exist)
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Create the patients table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            gender TEXT,
            age INTEGER,
            hypertension INTEGER,
            heart_disease INTEGER,
            ever_married TEXT,
            work_type TEXT,
            average_glucose REAL,
            bmi REAL,
            smoking_status TEXT,
            stroke INTEGER
        )
    ''')

    # Create the users table with a foreign key referencing the patients table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            patient_id INTEGER,
            FOREIGN KEY (patient_id) REFERENCES patients (id)
        )
    ''')
    
    

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

# Run the function to create the database and tables
create_database()
