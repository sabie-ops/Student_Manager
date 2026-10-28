import sqlite3


DATABASE_NAME = "student_manager.db"


def get_connection():
    """
    Retourne une connexion à la base de données SQLite.
    """

    return sqlite3.connect(DATABASE_NAME)


def init_database():
    """
    Crée les tables et ajoute les matières par défaut.
    """

    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT,
                class_name TEXT
            )
            """
        )

        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS subjects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            )
            """
        )

        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS grades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                subject_id INTEGER NOT NULL,
                grade REAL NOT NULL,
                FOREIGN KEY (student_id) REFERENCES students(id),
                FOREIGN KEY (subject_id) REFERENCES subjects(id)
            )
            """
        )

        subjects = [
            ("Python",),
            ("SQL",),
            ("Réseaux",),
            ("Systèmes",),
            ("Web",)
        ]

        connection.executemany(
            """
            INSERT OR IGNORE INTO subjects (name)
            VALUES (?)
            """,
            subjects
        )