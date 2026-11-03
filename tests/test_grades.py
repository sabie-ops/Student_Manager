import sqlite3
import pytest

from student_manager.grades import (
    add_grade,
    get_grades_by_student,
    get_student_average
)


@pytest.fixture
def setup_database(tmp_path, monkeypatch):
    """Crée une base de données temporaire pour les tests."""

    db_file = tmp_path / "test.db"

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Tables nécessaires
    cursor.execute("""
        CREATE TABLE students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT,
            last_name TEXT,
            email TEXT,
            class_name TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE subjects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE grades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            subject_id INTEGER,
            grade REAL
        )
    """)

    # Données de test
    cursor.execute("""
        INSERT INTO students
        (first_name, last_name, email, class_name)
        VALUES ('John', 'Doe', 'john@test.com', 'INFO1')
    """)

    cursor.execute("""
        INSERT INTO students
        (first_name, last_name, email, class_name)
        VALUES ('Jane', 'Smith', 'jane@test.com', 'INFO1')
    """)

    cursor.execute("""
        INSERT INTO subjects (name)
        VALUES ('Math')
    """)

    cursor.execute("""
        INSERT INTO subjects (name)
        VALUES ('Python')
    """)

    cursor.execute("""
        INSERT INTO grades (student_id, subject_id, grade)
        VALUES (1, 1, 15)
    """)

    cursor.execute("""
        INSERT INTO grades (student_id, subject_id, grade)
        VALUES (1, 2, 17)
    """)

    conn.commit()
    conn.close()

    def test_connection():
        return sqlite3.connect(db_file)

    monkeypatch.setattr(
        "student_manager.grades.get_connection",
        test_connection
    )

    return db_file


def test_add_grade(setup_database):
    """Vérifie l'ajout d'une note."""

    add_grade(1, 1, 18)

    conn = sqlite3.connect(setup_database)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT grade
        FROM grades
        WHERE student_id = 1
        ORDER BY id DESC
        LIMIT 1
    """)

    result = cursor.fetchone()

    conn.close()

    assert result[0] == 18


def test_get_grades_by_student(setup_database):
    """Vérifie la récupération des notes d'un étudiant."""

    grades = get_grades_by_student(1)

    assert len(grades) == 2


def test_get_student_average(setup_database):
    """Vérifie le calcul de la moyenne."""

    average = get_student_average(1)

    assert average == 16


def test_get_student_average_without_grades(setup_database):
    average = get_student_average(2)

    assert average == 0