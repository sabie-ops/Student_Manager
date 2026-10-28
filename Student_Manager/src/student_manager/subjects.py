from .database import get_connection


def get_subjects():
    """
    Retourne la liste des matières.
    """

    with get_connection() as connection:
        cursor = connection.execute(
            """
            SELECT id, name
            FROM subjects
            ORDER BY name
            """
        )

        return cursor.fetchall()