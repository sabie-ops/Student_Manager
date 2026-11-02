import pytest

from student_manager.statistics import (
    get_student_count,
    get_general_average,
    get_class_average,
)


def insert_student(db, class_name="L2"):
    """Ajoute un étudiant dans la base de test et retourne son id."""
    cursor = db.execute(
        """
        INSERT INTO students (first_name, last_name, email, class_name)
        VALUES ('Prenom', 'Nom', 'mail@test.com', ?)
        """,
        (class_name,)
    )
    return cursor.lastrowid


def insert_grade(db, student_id, grade):
    """Ajoute une note dans la base de test."""
    db.execute(
        "INSERT INTO grades (student_id, grade) VALUES (?, ?)",
        (student_id, grade)
    )


def test_get_student_count_empty(db):
    # Arrange : base vide (fournie par la fixture db)

    # Act
    resultat = get_student_count()

    # Assert
    assert resultat == 0


@pytest.mark.parametrize("nombre", [1, 3, 5])
def test_get_student_count(db, nombre):
    # Arrange
    for _ in range(nombre):
        insert_student(db)

    # Act
    resultat = get_student_count()

    # Assert
    assert resultat == nombre


def test_get_general_average_without_grades(db):
    # Arrange : aucune note dans la base

    # Act
    resultat = get_general_average()

    # Assert
    assert resultat == 0


@pytest.mark.parametrize(
    "notes, attendu",
    [
        ([12], 12),
        ([10, 20], 15),
        ([0, 20], 10),
    ]
)
def test_get_general_average(db, notes, attendu):
    # Arrange
    student_id = insert_student(db)
    for note in notes:
        insert_grade(db, student_id, note)

    # Act
    resultat = get_general_average()

    # Assert
    assert resultat == attendu


def test_get_class_average(db):
    # Arrange
    marie = insert_student(db, "L2")
    paul = insert_student(db, "L3")
    insert_grade(db, marie, 12)
    insert_grade(db, marie, 16)
    insert_grade(db, paul, 4)

    # Act
    resultat = get_class_average("L2")

    # Assert
    assert resultat == 14


def test_get_class_average_unknown_class(db):
    # Arrange
    student_id = insert_student(db, "L2")
    insert_grade(db, student_id, 15)

    # Act
    resultat = get_class_average("M1")

    # Assert
    assert resultat == 0