
import tkinter as tk
from tkinter import ttk, messagebox

from .database import init_database
from .students import (
    get_students,
    add_student,
    delete_student,
    search_students,
)
from .subjects import get_subjects
from .grades import (
    add_grade,
    get_grades_by_student,
    get_student_average,
)
from .statistics import (
    get_student_count,
    get_general_average,
    get_class_average,
)


# ==========================================================
# CONFIGURATION
# ==========================================================

BLUE = "#2878E8"
DARK_BLUE = "#24466B"
LIGHT_BLUE = "#EDF4FC"
WHITE = "#FFFFFF"
RED = "#E94355"
GREEN = "#15966A"
BORDER = "#D5E3F3"


class StudentManagerUI:

    def __init__(self, root):
        self.root = root
        self.root.title("Student Manager")
        self.root.geometry("1280x780")
        self.root.minsize(1000, 650)
        self.root.configure(bg=LIGHT_BLUE)

        self.student_choices = {}
        self.subject_choices = {}
        self.selected_student_id = None

        self.setup_style()
        self.create_header()
        self.create_tabs()

        self.refresh_students()
        self.refresh_subjects()
        self.refresh_statistics()

    # ======================================================
    # STYLE
    # ======================================================

    def setup_style(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "TNotebook",
            background=LIGHT_BLUE,
            borderwidth=0,
        )

        style.configure(
            "TNotebook.Tab",
            padding=(22, 12),
            font=("Segoe UI", 10, "bold"),
            background="#E6EEF8",
            foreground=DARK_BLUE,
        )

        style.map(
            "TNotebook.Tab",
            background=[("selected", WHITE)],
            foreground=[("selected", BLUE)],
        )

        style.configure(
            "TFrame",
            background=WHITE,
        )

        style.configure(
            "TLabel",
            background=WHITE,
            foreground=DARK_BLUE,
            font=("Segoe UI", 10),
        )

        style.configure(
            "TLabelframe",
            background=WHITE,
            bordercolor=BORDER,
        )

        style.configure(
            "TLabelframe.Label",
            background=WHITE,
            foreground=DARK_BLUE,
            font=("Segoe UI", 11, "bold"),
        )

        style.configure(
            "TEntry",
            padding=7,
        )

        style.configure(
            "TCombobox",
            padding=7,
        )

        style.configure(
            "Treeview",
            background=WHITE,
            foreground=DARK_BLUE,
            fieldbackground=WHITE,
            rowheight=32,
            font=("Segoe UI", 10),
        )

        style.configure(
            "Treeview.Heading",
            background="#E5EEF9",
            foreground=DARK_BLUE,
            font=("Segoe UI", 10, "bold"),
            padding=9,
        )

        style.map(
            "Treeview",
            background=[("selected", "#D4E5FF")],
            foreground=[("selected", DARK_BLUE)],
        )

        style.configure(
            "Primary.TButton",
            background=BLUE,
            foreground=WHITE,
            padding=9,
            font=("Segoe UI", 10, "bold"),
        )

        style.map(
            "Primary.TButton",
            background=[("active", "#1765CF")],
        )

        style.configure(
            "Danger.TButton",
            background=RED,
            foreground=WHITE,
            padding=9,
            font=("Segoe UI", 10, "bold"),
        )

        style.map(
            "Danger.TButton",
            background=[("active", "#CF3042")],
        )

        style.configure(
            "StatValue.TLabel",
            font=("Segoe UI", 23, "bold"),
            foreground=BLUE,
        )

        style.configure(
            "GreenValue.TLabel",
            font=("Segoe UI", 23, "bold"),
            foreground=GREEN,
        )

    # ======================================================
    # HEADER
    # ======================================================

    def create_header(self):
        header = tk.Frame(
            self.root,
            bg=DARK_BLUE,
            height=100,
        )
        header.pack(fill="x")
        header.pack_propagate(False)

        left = tk.Frame(header, bg=DARK_BLUE)
        left.pack(side="left", padx=25, pady=15)

        tk.Label(
            left,
            text="🎓  Student Manager",
            font=("Segoe UI", 23, "bold"),
            bg=DARK_BLUE,
            fg=WHITE,
        ).pack(anchor="w")

        tk.Label(
            left,
            text="Gestion des étudiants, des notes et des statistiques",
            font=("Segoe UI", 11),
            bg=DARK_BLUE,
            fg="#DCE9F8",
        ).pack(anchor="w", pady=(4, 0))

        tk.Label(
            header,
            text="▤  Base de données : student_manager.db",
            font=("Segoe UI", 10),
            bg=DARK_BLUE,
            fg=WHITE,
        ).pack(side="right", padx=22)

    # ======================================================
    # NOTEBOOK
    # ======================================================

    def create_tabs(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(
            fill="both",
            expand=True,
            padx=18,
            pady=18,
        )

        self.students_tab = ttk.Frame(
            self.notebook,
            padding=12,
        )
        self.grades_tab = ttk.Frame(
            self.notebook,
            padding=12,
        )
        self.statistics_tab = ttk.Frame(
            self.notebook,
            padding=12,
        )

        self.notebook.add(
            self.students_tab,
            text="  ♟  Étudiants  ",
        )
        self.notebook.add(
            self.grades_tab,
            text="  ▤  Notes  ",
        )
        self.notebook.add(
            self.statistics_tab,
            text="  ▥  Statistiques  ",
        )

        self.create_students_tab()
        self.create_grades_tab()
        self.create_statistics_tab()

    # ======================================================
    # OUTILS COMMUNS
    # ======================================================

    def create_field(self, parent, label, row, column):
        frame = ttk.Frame(parent, padding=4)
        frame.grid(
            row=row,
            column=column,
            sticky="ew",
            padx=4,
            pady=5,
        )

        ttk.Label(
            frame,
            text=label,
        ).pack(anchor="w", pady=(0, 6))

        entry = ttk.Entry(frame)
        entry.pack(fill="x")

        return entry

    def create_tree(self, parent, columns, headings, widths):
        container = ttk.Frame(parent)
        container.pack(fill="both", expand=True)

        container.columnconfigure(0, weight=1)
        container.rowconfigure(0, weight=1)

        tree = ttk.Treeview(
            container,
            columns=columns,
            show="headings",
            selectmode="browse",
        )

        for column in columns:
            tree.heading(
                column,
                text=headings[column],
            )
            tree.column(
                column,
                width=widths[column],
                anchor="w",
            )

        scrollbar = ttk.Scrollbar(
            container,
            orient="vertical",
            command=tree.yview,
        )

        tree.configure(
            yscrollcommand=scrollbar.set,
        )

        tree.grid(
            row=0,
            column=0,
            sticky="nsew",
        )
        scrollbar.grid(
            row=0,
            column=1,
            sticky="ns",
        )

        return tree

    def clear_tree(self, tree):
        for item in tree.get_children():
            tree.delete(item)

    # ======================================================
    # ONGLET ÉTUDIANTS
    # ======================================================

    def create_students_tab(self):
        tab = self.students_tab

        # Trois colonnes : formulaire, tableau, détails.
        tab.columnconfigure(0, weight=0, minsize=260)
        tab.columnconfigure(1, weight=3, minsize=350)
        tab.columnconfigure(2, weight=1, minsize=210)
        tab.rowconfigure(0, weight=1)

        # ---------------- FORMULAIRE À GAUCHE ----------------

        form = ttk.LabelFrame(
            tab,
            text="Ajouter un étudiant",
            padding=12,
        )
        form.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 10),
        )

        form.columnconfigure(0, weight=1)

        self.first_name_entry = self.create_field(
            form, "Prénom *", 0, 0
        )
        self.last_name_entry = self.create_field(
            form, "Nom *", 1, 0
        )
        self.email_entry = self.create_field(
            form, "Email", 2, 0
        )
        self.class_entry = self.create_field(
            form, "Classe", 3, 0
        )

        ttk.Button(
            form,
            text="＋ Ajouter l'étudiant",
            style="Primary.TButton",
            command=self.on_add_student,
        ).grid(
            row=4,
            column=0,
            sticky="ew",
            padx=4,
            pady=(15, 5),
        )

        ttk.Label(
            form,
            text="* Champs obligatoires",
        ).grid(
            row=5,
            column=0,
            sticky="w",
            padx=4,
            pady=8,
        )

        # ---------------- CENTRE : RECHERCHE ET TABLEAU ----------------

        center = ttk.Frame(tab)
        center.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(0, 10),
        )

        center.columnconfigure(0, weight=1)
        center.rowconfigure(1, weight=1)

        search_frame = ttk.Frame(center, padding=(0, 0, 0, 10))
        search_frame.grid(
            row=0,
            column=0,
            sticky="ew",
        )
        search_frame.columnconfigure(0, weight=1)

        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=(0, 6),
        )
        self.search_entry.bind(
            "<Return>",
            lambda event: self.on_search_students(),
        )

        ttk.Button(
            search_frame,
            text="Rechercher",
            style="Primary.TButton",
            command=self.on_search_students,
        ).grid(row=0, column=1, padx=3)

        ttk.Button(
            search_frame,
            text="Actualiser",
            command=self.refresh_students,
        ).grid(row=0, column=2, padx=3)

        table_frame = ttk.LabelFrame(
            center,
            text="Liste des étudiants",
            padding=10,
        )
        table_frame.grid(
            row=1,
            column=0,
            sticky="nsew",
        )
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)

        self.students_tree = self.create_tree(
            table_frame,
            (
                "id",
                "first_name",
                "last_name",
                "email",
                "class_name",
            ),
            {
                "id": "ID",
                "first_name": "Prénom",
                "last_name": "Nom",
                "email": "Email",
                "class_name": "Classe",
            },
            {
                "id": 45,
                "first_name": 100,
                "last_name": 100,
                "email": 170,
                "class_name": 100,
            },
        )

        self.students_tree.bind(
            "<<TreeviewSelect>>",
            self.on_student_selected,
        )

        self.student_count_text = ttk.Label(
            table_frame,
            text="0 étudiant",
        )
        self.student_count_text.pack(
            anchor="w",
            pady=(7, 0),
        )

        actions = ttk.Frame(center, padding=(0, 10, 0, 0))
        actions.grid(
            row=2,
            column=0,
            sticky="ew",
        )
        actions.columnconfigure((0, 1), weight=1)

        ttk.Button(
            actions,
            text="Supprimer",
            style="Danger.TButton",
            command=self.on_delete_student,
        ).grid(
            row=0,
            column=0,
            sticky="ew",
            padx=(0, 5),
        )

        ttk.Button(
            actions,
            text="Actualiser",
            command=self.refresh_students,
        ).grid(
            row=0,
            column=1,
            sticky="ew",
            padx=(5, 0),
        )

        # ---------------- DÉTAILS À DROITE ----------------

        details = ttk.LabelFrame(
            tab,
            text="Détails de l'étudiant",
            padding=14,
        )
        details.grid(
            row=0,
            column=2,
            sticky="nsew",
        )
        details.columnconfigure(0, weight=1)

        self.detail_values = {}

        for index, field in enumerate(
            ("Prénom", "Nom", "Email", "Classe")
        ):
            ttk.Label(
                details,
                text=f"{field} :",
            ).grid(
                row=index,
                column=0,
                sticky="w",
                pady=10,
            )

            value = ttk.Label(
                details,
                text="—",
                wraplength=180,
            )
            value.grid(
                row=index,
                column=1,
                sticky="w",
                padx=(8, 0),
                pady=10,
            )

            self.detail_values[field] = value

    def on_student_selected(self, event=None):
        selection = self.students_tree.selection()

        if not selection:
            return

        values = self.students_tree.item(
            selection[0],
            "values",
        )

        self.selected_student_id = int(values[0])

        fields = ("Prénom", "Nom", "Email", "Classe")
        student_values = values[1:]

        for field, value in zip(fields, student_values):
            self.detail_values[field].config(
                text=value or "—",
            )

        # Synchronise l'étudiant sélectionné avec l'onglet Notes.
        display_name = self.student_display_name(
            self.selected_student_id
        )

        if display_name in self.student_choices:
            self.grade_student_combo.set(display_name)
            #self.stats_student_combo.set(display_name)
            self.refresh_grades()

    def student_display_name(self, student_id):
        for display_name, identifier in self.student_choices.items():
            if identifier == student_id:
                return display_name

        return ""

    def refresh_students(self, students=None):
        if not hasattr(self, "students_tree"):
            return

        if students is None:
            students = get_students()

        self.clear_tree(self.students_tree)

        for student in students:
            self.students_tree.insert(
                "",
                "end",
                values=student,
            )

        count = len(students)

        self.student_count_text.config(
            text=f"{count} étudiant(s) affiché(s)",
        )

        self.refresh_student_choices()

    def on_add_student(self):
        first_name = self.first_name_entry.get().strip()
        last_name = self.last_name_entry.get().strip()
        email = self.email_entry.get().strip()
        class_name = self.class_entry.get().strip()

        if not first_name or not last_name:
            messagebox.showwarning(
                "Champs obligatoires",
                "Le prénom et le nom sont obligatoires.",
            )
            return

        try:
            add_student(
                first_name,
                last_name,
                email,
                class_name,
            )
        except Exception as error:
            messagebox.showerror(
                "Erreur",
                f"Impossible d'ajouter l'étudiant :\n{error}",
            )
            return

        for entry in (
            self.first_name_entry,
            self.last_name_entry,
            self.email_entry,
            self.class_entry,
        ):
            entry.delete(0, tk.END)

        self.search_entry.delete(0, tk.END)
        self.refresh_students()
        self.refresh_statistics()

        messagebox.showinfo(
            "Succès",
            "L'étudiant a été ajouté.",
        )

    def on_search_students(self):
        name = self.search_entry.get().strip()

        if not name:
            self.refresh_students()
            return

        try:
            results = search_students(name)
            self.refresh_students(results)
        except Exception as error:
            messagebox.showerror(
                "Erreur",
                f"Erreur de recherche :\n{error}",
            )

    def on_delete_student(self):
        selection = self.students_tree.selection()

        if not selection:
            messagebox.showwarning(
                "Sélection requise",
                "Sélectionnez un étudiant dans le tableau.",
            )
            return

        values = self.students_tree.item(
            selection[0],
            "values",
        )
        student_id = int(values[0])

        confirm = messagebox.askyesno(
            "Confirmation",
            "Voulez-vous vraiment supprimer cet étudiant ?",
        )

        if not confirm:
            return

        try:
            delete_student(student_id)
        except Exception as error:
            messagebox.showerror(
                "Erreur",
                f"Impossible de supprimer l'étudiant :\n{error}",
            )
            return

        self.selected_student_id = None

        for label in self.detail_values.values():
            label.config(text="—")

        self.refresh_students()
        self.refresh_grades()
        self.refresh_statistics()

    # ======================================================
    # ONGLET NOTES
    # ======================================================

    def create_grades_tab(self):
        tab = self.grades_tab

        # Trois colonnes : formulaire, notes, moyenne.
        tab.columnconfigure(0, weight=0, minsize=250)
        tab.columnconfigure(1, weight=3, minsize=350)
        tab.columnconfigure(2, weight=1, minsize=210)
        tab.rowconfigure(0, weight=1)

        # ---------------- FORMULAIRE À GAUCHE ----------------

        form = ttk.LabelFrame(
            tab,
            text="Ajouter une note",
            padding=12,
        )
        form.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 10),
        )
        form.columnconfigure(0, weight=1)

        ttk.Label(
            form,
            text="Étudiant *",
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=4,
            pady=(8, 4),
        )

        self.grade_student_combo = ttk.Combobox(
            form,
            state="readonly",
        )
        self.grade_student_combo.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=4,
            pady=(0, 12),
        )
        self.grade_student_combo.bind(
            "<<ComboboxSelected>>",
            lambda event: self.refresh_grades(),
        )

        ttk.Label(
            form,
            text="Matière *",
        ).grid(
            row=2,
            column=0,
            sticky="w",
            padx=4,
            pady=(4, 4),
        )

        self.subject_combo = ttk.Combobox(
            form,
            state="readonly",
        )
        self.subject_combo.grid(
            row=3,
            column=0,
            sticky="ew",
            padx=4,
            pady=(0, 12),
        )

        ttk.Label(
            form,
            text="Note sur 20 *",
        ).grid(
            row=4,
            column=0,
            sticky="w",
            padx=4,
            pady=(4, 4),
        )

        self.grade_entry = ttk.Entry(form)
        self.grade_entry.grid(
            row=5,
            column=0,
            sticky="ew",
            padx=4,
            pady=(0, 12),
        )

        ttk.Button(
            form,
            text="＋ Ajouter la note",
            style="Primary.TButton",
            command=self.on_add_grade,
        ).grid(
            row=6,
            column=0,
            sticky="ew",
            padx=4,
            pady=(8, 5),
        )

        ttk.Label(
            form,
            text="La note doit être comprise entre 0 et 20.",
            wraplength=220,
        ).grid(
            row=7,
            column=0,
            sticky="w",
            padx=4,
            pady=8,
        )

        # ---------------- TABLEAU AU CENTRE ----------------

        content = ttk.LabelFrame(
            tab,
            text="Notes de l'étudiant",
            padding=10,
        )
        content.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(0, 10),
        )
        content.columnconfigure(0, weight=1)
        content.rowconfigure(0, weight=1)

        self.grades_tree = self.create_tree(
            content,
            ("id", "subject", "grade"),
            {
                "id": "ID",
                "subject": "Matière",
                "grade": "Note",
            },
            {
                "id": 55,
                "subject": 200,
                "grade": 100,
            },
        )

        # ---------------- MOYENNE À DROITE ----------------

        average_card = ttk.LabelFrame(
            tab,
            text="Moyenne de l'étudiant",
            padding=15,
        )
        average_card.grid(
            row=0,
            column=2,
            sticky="nsew",
        )
        average_card.columnconfigure(0, weight=1)

        ttk.Label(
            average_card,
            text="Étudiant sélectionné",
            wraplength=180,
        ).grid(
            row=0,
            column=0,
            sticky="w",
            pady=(5, 8),
        )

        self.average_student_name = ttk.Label(
            average_card,
            text="—",
            wraplength=180,
        )
        self.average_student_name.grid(
            row=1,
            column=0,
            sticky="w",
            pady=(0, 15),
        )

        ttk.Separator(
            average_card,
            orient="horizontal",
        ).grid(
            row=2,
            column=0,
            sticky="ew",
            pady=10,
        )

        ttk.Label(
            average_card,
            text="Moyenne :",
        ).grid(
            row=3,
            column=0,
            pady=(15, 5),
        )

        self.average_value = ttk.Label(
            average_card,
            text="—",
            style="StatValue.TLabel",
        )
        self.average_value.grid(
            row=4,
            column=0,
            pady=5,
        )

        ttk.Label(
            average_card,
            text="sur 20",
        ).grid(
            row=5,
            column=0,
            pady=(0, 10),
        )

    def refresh_student_choices(self):
        students = get_students()

        self.student_choices = {
            f"{student[1]} {student[2]} (ID {student[0]})": student[0]
            for student in students
        }

        choices = list(self.student_choices.keys())

        if hasattr(self, "grade_student_combo"):
            current = self.grade_student_combo.get()
            self.grade_student_combo["values"] = choices

            if current not in choices:
                self.grade_student_combo.set("")

        if hasattr(self, "stats_student_combo"):
            current = self.stats_student_combo.get()
            self.stats_student_combo["values"] = choices

            if current not in choices:
                self.stats_student_combo.set("")

    def refresh_subjects(self):
        subjects = get_subjects()

        self.subject_choices = {
            subject[1]: subject[0]
            for subject in subjects
        }

        if hasattr(self, "subject_combo"):
            self.subject_combo["values"] = list(
                self.subject_choices.keys()
            )

    def on_add_grade(self):
        student_name = self.grade_student_combo.get()
        subject_name = self.subject_combo.get()
        grade_text = self.grade_entry.get().strip()

        if not student_name or not subject_name or not grade_text:
            messagebox.showwarning(
                "Champs obligatoires",
                "Sélectionnez un étudiant, une matière et une note.",
            )
            return

        try:
            grade_value = float(
                grade_text.replace(",", ".")
            )
        except ValueError:
            messagebox.showerror(
                "Note invalide",
                "Saisissez une note numérique.",
            )
            return

        if not 0 <= grade_value <= 20:
            messagebox.showwarning(
                "Note invalide",
                "La note doit être comprise entre 0 et 20.",
            )
            return

        student_id = self.student_choices[student_name]
        subject_id = self.subject_choices[subject_name]

        try:
            add_grade(
                student_id,
                subject_id,
                grade_value,
            )
        except Exception as error:
            messagebox.showerror(
                "Erreur",
                f"Impossible d'ajouter la note :\n{error}",
            )
            return

        self.grade_entry.delete(0, tk.END)
        self.refresh_grades()
        self.refresh_statistics()

        messagebox.showinfo(
            "Succès",
            "La note a été ajoutée.",
        )

    def refresh_grades(self):
        if not hasattr(self, "grades_tree"):
            return

        self.clear_tree(self.grades_tree)

        student_name = self.grade_student_combo.get()

        if not student_name:
            self.average_student_name.config(text="—")
            self.average_value.config(text="—")
            return

        student_id = self.student_choices[student_name]

        try:
            grades = get_grades_by_student(student_id)
            average = get_student_average(student_id)
        except Exception as error:
            messagebox.showerror(
                "Erreur",
                f"Impossible de récupérer les notes :\n{error}",
            )
            return

        for grade in grades:
            self.grades_tree.insert(
                "",
                "end",
                values=grade,
            )

        self.average_student_name.config(
            text=student_name,
        )

        self.average_value.config(
            text=f"{average:.2f}",
        )

    # ======================================================
    # ONGLET STATISTIQUES
    # ======================================================

    def create_statistics_tab(self):
        tab = self.statistics_tab

        tab.columnconfigure(0, weight=1)
        tab.rowconfigure(1, weight=1)

        # ---------------- CARTES STATISTIQUES ----------------

        cards = ttk.Frame(tab)
        cards.grid(
            row=0,
            column=0,
            sticky="ew",
            pady=(0, 15),
        )

        for column in range(3):
            cards.columnconfigure(column, weight=1)

        self.student_count_label = self.create_stat_card(
            cards,
            "Nombre d'étudiants",
            "—",
            0,
        )

        self.general_average_label = self.create_stat_card(
            cards,
            "Moyenne générale",
            "—",
            1,
            green=True,
        )

        class_card = ttk.LabelFrame(
            cards,
            text="Moyenne de la classe",
            padding=14,
        )
        class_card.grid(
            row=0,
            column=2,
            sticky="nsew",
            padx=6,
        )
        class_card.columnconfigure(0, weight=1)

        self.class_combo = ttk.Combobox(
            class_card,
            state="readonly",
        )
        self.class_combo.grid(
            row=0,
            column=0,
            sticky="ew",
            pady=(5, 10),
        )

        self.class_average_label = ttk.Label(
            class_card,
            text="—",
            style="StatValue.TLabel",
        )
        self.class_average_label.grid(
            row=1,
            column=0,
            pady=5,
        )

        ttk.Button(
            class_card,
            text="Calculer",
            command=self.update_class_average,
        ).grid(
            row=2,
            column=0,
            sticky="ew",
            pady=(10, 0),
        )

        # ---------------- TABLEAU DES MOYENNES PAR CLASSE ----------------

        table_frame = ttk.LabelFrame(
            tab,
            text="Moyennes par classe",
            padding=12,
        )
        table_frame.grid(
            row=1,
            column=0,
            sticky="nsew",
        )
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)

        self.class_tree = self.create_tree(
            table_frame,
            ("class_name", "average"),
            {
                "class_name": "Classe",
                "average": "Moyenne",
            },
            {
                "class_name": 300,
                "average": 150,
            },
        )

        ttk.Button(
            tab,
            text="Actualiser les statistiques",
            style="Primary.TButton",
            command=self.refresh_statistics,
        ).grid(
            row=2,
            column=0,
            sticky="w",
            pady=(12, 0),
        )

    def create_stat_card(
        self,
        parent,
        title,
        value,
        column,
        green=False,
    ):
        card = ttk.LabelFrame(
            parent,
            text=title,
            padding=15,
        )
        card.grid(
            row=0,
            column=column,
            sticky="nsew",
            padx=6,
        )

        style = (
            "GreenValue.TLabel"
            if green
            else "StatValue.TLabel"
        )

        label = ttk.Label(
            card,
            text=value,
            style=style,
        )
        label.pack(
            expand=True,
            pady=12,
        )

        return label

    def refresh_statistics(self):
        count = get_student_count()
        general_average = get_general_average()

        self.student_count_label.config(
            text=str(count),
        )

        self.general_average_label.config(
            text=f"{general_average:.2f}",
        )

        students = get_students()

        classes = sorted({
            student[4]
            for student in students
            if student[4]
        })

        self.class_combo["values"] = classes

        if self.class_combo.get() not in classes:
            self.class_combo.set("")

        self.clear_tree(self.class_tree)

        for class_name in classes:
            average = get_class_average(class_name)

            self.class_tree.insert(
                "",
                "end",
                values=(
                    class_name,
                    f"{average:.2f}",
                ),
            )

        self.refresh_student_choices()

        if self.class_combo.get():
            self.update_class_average()
        else:
            self.class_average_label.config(text="—")

    def update_class_average(self):
        class_name = self.class_combo.get()

        if not class_name:
            messagebox.showwarning(
                "Classe requise",
                "Sélectionnez une classe.",
            )
            return

        average = get_class_average(class_name)

        self.class_average_label.config(
            text=f"{average:.2f}",
        )


# ==========================================================
# POINT D'ENTRÉE DE L'INTERFACE
# ==========================================================

def create_main_window():
    root = tk.Tk()
    StudentManagerUI(root)
    root.mainloop()


if __name__ == "__main__":
    init_database()
    create_main_window()
