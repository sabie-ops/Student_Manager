# Student Manager

## Description

Student Manager est une application Python permettant de gérer des étudiants, leurs matières et leurs notes. L'application utilise une base de données SQLite pour stocker les informations et fournit différentes fonctionnalités de gestion et de statistiques.

## Fonctionnalités principales

- Ajouter un étudiant
- Supprimer un étudiant
- Rechercher un étudiant
- Consulter la liste des matières
- Ajouter une note
- Consulter les notes d'un étudiant
- Calculer la moyenne d'un étudiant
- Afficher le nombre total d'étudiants
- Calculer la moyenne générale
- Afficher la moyenne générale

## Prérequis

Avant d'utiliser l'application, les éléments suivants doivent être installés :

- Python 3.12 ou supérieur
- Poetry
- Git (optionnel)

## Installation

Cloner le projet :

```bash
git clone <url-du-depot>
cd Student_Manager
```

Installer les dépendances :

```bash
poetry install
```

## Lancement de l'application

Exécuter l'application avec :

```bash
poetry run python -m student_manager.main
```

## Exécution des tests

Lancer tous les tests :

```bash
poetry run pytest
```

Lancer un fichier de test spécifique :

```bash
poetry run pytest tests/test_grades.py
```

## Structure du projet

```text
src/
└── student_manager/
    ├── database.py
    ├── students.py
    ├── subjects.py
    ├── grades.py
    ├── statistics.py
    ├── ui.py
    └── main.py

tests/
    ├── test_database.py
    ├── test_students.py
    ├── test_subjects.py
    ├── test_grades.py
    └── test_statistics.py
```
## URL Testpypi

- pip install -i https://test.pypi.org/simple/ student-manager-sac-11-26

## Auteurs

- Sabie Melanie NITEKA
- Celeste Oudjane
- Amandine LENAR