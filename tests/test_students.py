import pytest

# ne peut pas trouver le fichier data donc block tout les fichier test, il faut bien cherché ou il est plassé
from student_manager.database import get_connection
from student_manager.students import (
# aussi pour cette ligne
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
        "student_manager.students.get_connection",
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
   add_student("Maxine", "Mayfield", "maxine@example.com", "L1")
   add_student("Lucas", "Sinclair", "lucas@example.com", "L2")

   students = get_students()
   assert len(students) == 2
   assert students[0][1] == "Maxine" 
   assert students[0][2] == "Mayfield"
   assert students[1][1] == "Lucas"
   assert students[1][2] == "Sinclair"                                                                                                                 
   

def test_delete_student(setup_database):
    # vérifier la suppression d’un étudiant.
    mike_id = add_student("Mike", "Wheeler", "mike@example.com", "L1")
    add_student("Dustin", "Henderson", "dustin@example.com", "L1")

    delete_student(mike_id)

    students = get_students()
    assert len(students) == 1
    assert students[0][1] == "Dustin"
    assert students[0][2] == "Henderson"


def test_search_students(setup_database):
    # vérifier la recherche d’étudiants à partir d’un nom ou d'un prénom.
    add_student("Mike", "Wheeler", "mike@example.com", "L1")
    add_student("Dustin", "Henderson", "dustin@example.com", "L1")
    add_student("Will", "Byers", "will@example.com", "L2")

    # Recherche par nom
    results = search_students("Wheeler")
    assert len(results) == 1
    assert results[0][1] == "Mike"

    # Recherche par prénom
    results = search_students("Dustin")
    assert len(results) == 1
    assert results[0][2] == "Henderson"

def test_search_students_no_result(setup_database):
    # vérifier le comportement de la recherche lorsqu’aucun étudiant ne correspond au critère indiqué.
    add_student("Mike", "Wheeler", "mike@example.com", "L1")
    add_student("Eleven", "Hopper", "eleven@example.com", "L1")

    results = search_students("Vecna")

    assert results == []