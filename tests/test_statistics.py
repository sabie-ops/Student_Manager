import sqlite3

import pytest

from student_manager.statistics import (
    get_student_count,
    get_general_average,
    get_class_average,
)


@pytest.fixture
def setup_database(tmp_path, monkeypatch):
    """Crée une base temporaire avec des données de test."""
    db_path = tmp_path / "test.db"

    connection = sqlite3.connect(db_path)
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

    connection.executemany(
        """
        INSERT INTO students (first_name, last_name, email, class_name)
        VALUES (?, ?, ?, ?)
        """,
        [
            ("Marie", "Dupont", "marie@mail.com", "L2"),
            ("Paul", "Martin", "paul@mail.com", "L2"),
            ("Lea", "Durand", "lea@mail.com", "L3"),
            ("Tom", "Petit", "tom@mail.com", "M1"),
        ]
    )
    connection.executemany(
        "INSERT INTO grades (student_id, grade) VALUES (?, ?)",
        [
            (1, 12),
            (1, 16),
            (2, 10),
            (2, 14),
            (3, 8),
        ]
    )
    connection.commit()
    connection.close()

    monkeypatch.setattr(
        "student_manager.statistics.get_connection",
        lambda: sqlite3.connect(db_path)
    )


def test_get_student_count(setup_database):
    # Arrange : 4 étudiants insérés par la fixture

    # Act
    resultat = get_student_count()

    # Assert
    assert resultat == 4


def test_get_general_average(setup_database):
    # Arrange : notes 12, 16, 10, 14, 8 -> 60 / 5

    # Act
    resultat = get_general_average()

    # Assert
    assert resultat == 12


def test_get_class_average(setup_database):
    # Arrange : L2 = Marie (12, 16) et Paul (10, 14) -> 52 / 4

    # Act
    resultat = get_class_average("L2")

    # Assert
    assert resultat == 13


def test_get_class_average_without_grades(setup_database):
    # Arrange : Tom est en M1 et n'a aucune note

    # Act
    resultat = get_class_average("M1")

    # Assert
    assert resultat == 0