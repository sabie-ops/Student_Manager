from student_manager.database import init_database
from student_manager.ui import create_main_window


def main():
    """
    Point d'entrée de l'application.
    """

    init_database()
    create_main_window()


if __name__ == "__main__":
    main()