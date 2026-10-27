from .database import get_connection


def get_students():
    """
    Retourne la liste de tous les étudiants.
    """

    with get_connection() as connection:
        cursor = connection.execute(
            """
            SELECT id, first_name, last_name, email, class_name
            FROM students
            ORDER BY last_name, first_name
            """
        )

        return cursor.fetchall()


def add_student(first_name, last_name, email, class_name):
    """
    À compléter : Ajoute un nouvel étudiant dans la base de données.
    """

    pass


def delete_student(student_id):
    """
    À compléter : Supprime un étudiant.
    """

    pass


def search_students(name):
    """
    À compléter : Recherche un étudiant par son nom ou son prénom.
    """

    pass