import tkinter as tk
from tkinter import ttk
import sqlite3
from view.student_tab import create_student_tab
from view.course_tab import create_course_tab
from view.email_tab import create_email_tab
from view.schedule_tab import create_schedule_tab

def main():
    # Database connection
    db_path = './mmis_db.db'  # Update this with the correct path to your database file
    conn = sqlite3.connect(db_path)

    root = tk.Tk()
    root.title("Graduate Course Application")
    root.state('zoomed')

    # Georgia College Colors
    BLUE = '#1C4F9C'
    GREEN = '#1C5438'

    # Configure styles for ttk elements
    style = ttk.Style()
    style.theme_use('clam')
    style.configure('GCSU.TButton', background=GREEN, foreground='white', font=('Helvetica', 10), borderwidth=1)
    style.map('GCSU.TButton', background=[('active', GREEN), ('pressed', GREEN)], foreground=[('pressed', 'white'), ('active', 'white')])
    style.configure('TNotebook.Tab', font=('Helvetica', '14'))

    # Create and add tabs
    notebook = ttk.Notebook(root)
    notebook.pack(fill='both', expand=True)

    student_tab = create_student_tab(notebook, BLUE, GREEN, conn)
    course_tab = create_course_tab(notebook, BLUE, GREEN, conn)
    email_tab = create_email_tab(notebook, BLUE, GREEN, conn)
    schedule_tab = create_schedule_tab(notebook, BLUE, GREEN, conn)

    notebook.add(student_tab, text='Student')
    notebook.add(course_tab, text='Course')
    notebook.add(email_tab, text='Email')
    notebook.add(schedule_tab, text='Schedule')

    root.mainloop()

if __name__ == "__main__":
    main()
