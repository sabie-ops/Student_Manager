
import pytest

from student_manager import database
from student_manager import subjects


@pytest.fixture
def setup_database(tmp_path, monkeypatch):
    """Configure une base de données temporaire."""

    database_file = tmp_path / "test_subjects.db"

    monkeypatch.setattr(
        database,
        "DATABASE_NAME",
        str(database_file),
    )

    database.init_database()

    return database_file


def test_get_subjects(setup_database):
    with database.get_connection() as connection:
        connection.execute(
            "DELETE FROM subjects"
        )

        connection.executemany(
            "INSERT INTO subjects (name) VALUES (?)",
            [
                ("Python",),
                ("Java",),
                ("SQL",),
            ],
        )

    result = subjects.get_subjects()

    assert [row[1] for row in result] == [
        "Java",
        "Python",
        "SQL",
    ]


def test_get_subjects_empty(setup_database):
    with database.get_connection() as connection:
        connection.execute(
            "DELETE FROM subjects"
        )

    result = subjects.get_subjects()

    assert result == []
