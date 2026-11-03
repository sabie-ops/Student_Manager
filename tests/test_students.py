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
     # ajoute l'étudiant alice martin et récupère son id
    student_id = add_student(
        "Alice", "Martin", "alice@example.com", "BTS SIO"
    )
     # récupère la liste de tous les étudiants de la base
    students = get_students()
    # vérifie qu'il y a un seul étudiant, avec le prénom alice (index 1) et le nom martin (index 2)
    if len(students) == 1 and students[0][1] == "Alice" and students[0][2] == "Martin":
        print("Test réussi L'étudiant Alice a bien été ajouté.")
    else:
        print("Test échoué L'étudiant n'a pas été trouvé correctement.")
        print(f"Étudiants actuels dans la base : {students}")

    

def test_get_students(setup_database):
   add_student("Maxine", "Mayfield", "maxine@example.com", "L1")
   add_student("Lucas", "Sinclair", "lucas@example.com", "L2")
    # récupère la liste de tous les étudiants
   students = get_students()
   # vérifie que la base contient exactement 2 étudiants
   assert len(students) == 2
   # vérifie que le prénom du premier étudiant est maxine
   assert students[0][1] == "Maxine" 
   assert students[0][2] == "Mayfield"
   assert students[1][1] == "Lucas"
   assert students[1][2] == "Sinclair"                                                                                                                 
   

def test_delete_student(setup_database):
    # vérifier la suppression d’un étudiant.
    mike_id = add_student("Mike", "Wheeler", "mike@example.com", "L1")
    add_student("Dustin", "Henderson", "dustin@example.com", "L1")

    delete_student(mike_id)
     # récupère la liste de tous les étudiants de la base
    students = get_students()
     # vérifie qu'il ne reste qu'un étudiant et que c'est bien dustin henderson
    if len(students) == 1 and students[0][1] == "Dustin" and students[0][2] == "Henderson":
        print("le test est réussi : Mike à été supprimé")
    else:
        print("les test a échoué : Mike est toujours dans la Base de Données")


def test_search_students(setup_database):
    # vérifier la recherche d'étudiants à partir d'un nom ou d'un prénom.
    add_student("Mike", "Wheeler", "mike@example.com", "L1")
    add_student("Dustin", "Henderson", "dustin@example.com", "L1")
    add_student("Will", "Byers", "will@example.com", "L2")

    # Recherche par prénom
    results_prenom = search_students("Dustin")

   # vérifie qu'un seul étudiant correspond au prénom "dustin"
    # sinon, affiche le nombre de résultats obtenus et leur contenu
    assert len(results_prenom) == 1, (
        f"Recherche par prénom (Dustin) : 1 résultat attendu, "
        f"{len(results_prenom)} obtenu(s). Résultats : {results_prenom}"
    )

    # sinon, affiche le nom réellement obtenu
    assert results_prenom[0][2] == "Henderson", (
        f"Recherche par prénom (Dustin) : nom attendu 'Henderson', "
        f"obtenu '{results_prenom[0][2]}'."
    )

    # message de confirmation (affiché uniquement si les deux assert ci-dessus réussissent)
    print("Test réussi : Recherche par prénom (Dustin).")

    # recherche par nom
    results_nom = search_students("Wheeler")
    # vérifie qu'un seul étudiant correspond au nom wheeler
    assert len(results_nom) == 1, (
        f"Recherche par nom (Wheeler) : 1 résultat attendu, "
        f"{len(results_nom)} obtenu(s). Résultats : {results_nom}"
    )
    # vérifie que l'étudiant trouvé a bien le prénom "mike" (colonne d'index 1)
    assert results_nom[0][1] == "Mike", (
        f"Recherche par nom (Wheeler) : prénom attendu 'Mike', "
        f"obtenu '{results_nom[0][1]}'."
    )
    print("Test réussi : Recherche par nom (Wheeler).")


def test_search_students_no_result(setup_database):
    # vérifier le comportement lorsqu'aucun étudiant ne correspond au critère.
    add_student("Mike", "Wheeler", "mike@example.com", "L1")
    add_student("Eleven", "Hopper", "eleven@example.com", "L1")
    # lance la recherche avec un nom qui n'existe pas dans la base
    results = search_students("Vecna")

    # vérifie que la liste de résultats est vide
    # sinon, affiche les étudiants trouvés par erreur
    assert results == [], (
        f"Aucun résultat attendu pour 'Vecna', mais des étudiants ont été "
        f"trouvés : {results}"
    )
    print("Test réussi : Aucun étudiant trouvé pour un critère inexistant.")