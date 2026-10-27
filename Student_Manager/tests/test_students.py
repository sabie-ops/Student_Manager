import pytest

from student_manager_az.database import get_connection
from student_manager_az.students import (
    get_students,
    add_student,
    delete_student,
    search_students,
)


@pytest.fixture
def setup_database(tmp_path, monkeypatch):
    """Prépare une base SQLite temporaire pour les tests."""

    database_file = tmp_path / "test_students.db"

    def get_test_connection():
        import sqlite3
        return sqlite3.connect(database_file)

    monkeypatch.setattr(
        "student_manager_az.students.get_connection",
        get_test_connection,
    )

    with get_test_connection() as connection:
        connection.execute("""
            CREATE TABLE students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT,
                class_name TEXT
            )
        """)

    return database_file


def test_add_student(setup_database):
    """ vérifier l’ajout d’un étudiant """
    student_id = add_student(
        "Alice", "Martin", "alice@example.com", "BTS SIO"
    )

    assert student_id == 1


def test_get_students(setup_database):
    # À compléter :  vérifier la récupération de la liste des étudiants.


def test_delete_student(setup_database):
    # À compléter : vérifier la suppression d’un étudiant.


def test_search_students(setup_database):
    # À compléter : vérifier la recherche d’étudiants à partir d’un nom ou d'un prénom.


def test_search_students_no_result(setup_database):
    # À compléter : vérifier le comportement de la recherche lorsqu’aucun étudiant ne correspond au critère indiqué.