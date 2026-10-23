import sqlite3

DATABASE_NAME = "medical_records.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS medical_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_reference TEXT NOT NULL,
            medical_system TEXT NOT NULL,
            record_type TEXT NOT NULL,
            condition_terms TEXT NOT NULL,
            medicines TEXT NOT NULL,
            notes TEXT
        )
    """)

    connection.commit()
    connection.close()