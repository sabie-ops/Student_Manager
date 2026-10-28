from .database import get_connection


def get_student_count():
    """
    À compléter : Retourne le nombre total d'étudiants.
    """

    pass


def get_general_average():
    """
    Retourne la moyenne générale de tous les étudiants.
    """

    with get_connection() as connection:
        cursor = connection.execute(
            """
            SELECT AVG(grade)
            FROM grades
            """
        )

        result = cursor.fetchone()

        return result[0] if result[0] is not None else 0


def get_class_average(class_name):
    """
    Retourne la moyenne d'une classe.
    """

    with get_connection() as connection:
        cursor = connection.execute(
            """
            SELECT AVG(grades.grade)
            FROM grades
            JOIN students
                ON grades.student_id = students.id
            WHERE students.class_name = ?
            """,
            (class_name,)
        )

        result = cursor.fetchone()

        return result[0] if result[0] is not None else 0