import sqlite3
import pandas as pd

def create_database():
    # Conectar a la base de datos (crea 'database.db' si no existe)
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Eliminar la tabla "patients" si ya existe para evitar problemas con las columnas
    cursor.execute('DROP TABLE IF EXISTS patients')

    # Crear la tabla de pacientes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            gender TEXT,
            age REAL,
            hypertension INTEGER,
            heart_disease INTEGER,
            ever_married TEXT,
            work_type TEXT,
            residence_type TEXT,
            avg_glucose_level REAL,
            bmi REAL,
            smoking_status TEXT,
            stroke INTEGER
        )
    ''')

    # Crear la tabla de usuarios si no existe
    cursor.execute('DROP TABLE IF EXISTS users') # Asegurarse de eliminar la tabla users antes de recrearla
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            patient_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (patient_id) REFERENCES patients (id)
        )
    ''')

    # Confirmar los cambios en la estructura de las tablas
    conn.commit()

    # Leer el archivo CSV usando pandas
    csv_file_path = 'healthcaredataset-stroke-data.csv'
    data = pd.read_csv(csv_file_path)

    # Insertar los datos del archivo CSV en la tabla "patients"
    for _, row in data.iterrows():
        cursor.execute('''
            INSERT INTO patients (gender, age, hypertension, heart_disease, ever_married, work_type, residence_type, avg_glucose_level, bmi, smoking_status, stroke)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            row['gender'],
            row['age'],
            row['hypertension'],
            row['heart_disease'],
            row['ever_married'],
            row['work_type'],
            row['Residence_type'],
            row['avg_glucose_level'],
            row['bmi'],
            row['smoking_status'],
            row['stroke']
        ))

    # Confirmar los cambios e insertar los datos
    conn.commit()
    conn.close()

    print("Base de datos creada y datos importados correctamente.")

# Ejecutar la función para crear la base de datos y cargar los datos
if __name__ == '__main__':
    create_database()
