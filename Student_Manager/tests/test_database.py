import sqlite3

import pytest

from student_manager_az import database


@pytest.fixture
def setup_database(tmp_path, monkeypatch):
    """Configure une base de données temporaire."""

    database_file = tmp_path / "test_database.db"

    monkeypatch.setattr(
        database,
        "DATABASE_NAME",
        str(database_file),
    )

    return database_file


def test_get_connection(setup_database):
    connection = database.get_connection()

    assert isinstance(connection, sqlite3.Connection)

    connection.close()


def test_init_database_creates_tables(setup_database):
    database.init_database()

    with database.get_connection() as connection:
        cursor = connection.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
        """)

        tables = [row[0] for row in cursor.fetchall()]

    assert "students" in tables
    assert "subjects" in tables
    assert "grades" in tables


def test_init_database_inserts_default_subjects(setup_database):
    database.init_database()

    with database.get_connection() as connection:
        cursor = connection.execute("""
            SELECT name
            FROM subjects
            ORDER BY name
        """)

        subjects = [row[0] for row in cursor.fetchall()]

    assert subjects == [
        "Python",
        "Réseaux",
        "SQL",
        "Systèmes",
        "Web",
    ]


def test_init_database_is_idempotent(setup_database):
    database.init_database()
    database.init_database()

    with database.get_connection() as connection:
        cursor = connection.execute(
            "SELECT COUNT(*) FROM subjects"
        )

        subject_count = cursor.fetchone()[0]

    assert subject_count == 5