import sqlite3

import pytest

from student_manager import statistics


@pytest.fixture
def db(monkeypatch):
    """Crée une base vide en mémoire et la substitue à la vraie base."""
    connection = sqlite3.connect(":memory:")

    connection.execute(
        """
        CREATE TABLE students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT,
            last_name TEXT,
            email TEXT,
            class_name TEXT
        )
        """
    )
    connection.execute(
        """
        CREATE TABLE grades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            grade REAL
        )
        """
    )

    # statistics.py utilisera cette connexion au lieu de la vraie base
    monkeypatch.setattr(statistics, "get_connection", lambda: connection)

    yield connection
    connection.close()


def test_get_student_count_empty(db):
    assert statistics.get_student_count() == 0


def test_get_student_count(db):
    db.execute("INSERT INTO students (first_name, last_name, email, class_name) VALUES ('Marie', 'Dupont', 'm@mail.com', 'L2')")
    db.execute("INSERT INTO students (first_name, last_name, email, class_name) VALUES ('Paul', 'Martin', 'p@mail.com', 'L2')")

    assert statistics.get_student_count() == 2


def test_get_general_average_without_grades(db):
    assert statistics.get_general_average() == 0


def test_get_general_average(db):
    db.execute("INSERT INTO grades (student_id, grade) VALUES (1, 10)")
    db.execute("INSERT INTO grades (student_id, grade) VALUES (1, 20)")

    assert statistics.get_general_average() == 15


def test_get_class_average(db):
    db.execute("INSERT INTO students (first_name, last_name, email, class_name) VALUES ('Marie', 'Dupont', 'm@mail.com', 'L2')")
    db.execute("INSERT INTO students (first_name, last_name, email, class_name) VALUES ('Paul', 'Martin', 'p@mail.com', 'L3')")
    db.execute("INSERT INTO grades (student_id, grade) VALUES (1, 12)")  # Marie, L2
    db.execute("INSERT INTO grades (student_id, grade) VALUES (1, 16)")  # Marie, L2
    db.execute("INSERT INTO grades (student_id, grade) VALUES (2, 4)")   # Paul, L3

    assert statistics.get_class_average("L2") == 14



