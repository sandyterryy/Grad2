# view/course_tab.py

import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Database interaction functions
def fetch_course_data(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT Course_ID, Course_name, Course_prefix, \"Required/Elective\", Semester_offerred FROM Courses")
    return cursor.fetchall()

def add_course(conn, course_data, course_table):
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Courses (Course_name, Course_prefix, \"Required/Elective\", Semester_offerred) VALUES (?, ?, ?, ?)", course_data)
        conn.commit()
        course_table.delete(*course_table.get_children())
        for data in fetch_course_data(conn):
            course_table.insert('', 'end', values=data)
            refresh_course_table(course_table, conn)
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", str(e))

def update_course(conn, entry_widgets, course_table):
    try:
        # Get the course ID from the selected item in the Treeview
        selected_item = course_table.selection()[0]
        course_id = course_table.item(selected_item)['values'][0]

        # Get the updated data from the input fields
        updated_data = [entry.get() for entry in entry_widgets]

        cursor = conn.cursor()
        cursor.execute("UPDATE Courses SET Course_name=?, Course_prefix=?, \"Required/Elective\"=?, Semester_offerred=? WHERE Course_ID=?",
                       (*updated_data, course_id))
        conn.commit()
        refresh_course_table(course_table, conn)
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", str(e))
    except IndexError:
        messagebox.showwarning("Selection Error", "No course selected for update.")

def delete_course(conn, course_table):
    try:
        selected_item = course_table.selection()[0]  # Get selected item
        course_id = course_table.item(selected_item)['values'][0]  # Get the Course_ID

        cursor = conn.cursor()
        cursor.execute("DELETE FROM Courses WHERE Course_ID=?", (course_id,))
        conn.commit()
        refresh_course_table(course_table, conn)
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", str(e))
    except IndexError:
        messagebox.showwarning("Selection Error", "No course selected for deletion.")

def refresh_course_table(course_table, conn):
    course_table.delete(*course_table.get_children())
    for data in fetch_course_data(conn):
        course_table.insert('', 'end', values=data)

# GUI function for creating the course tab
def create_course_tab(notebook, bg_color, btn_color, conn):
    courses_tab = tk.Frame(notebook, bg=bg_color)
    courses_tab.pack(expand=True, fill='both')

    # Centering content with an inner frame
    inner_frame = tk.Frame(courses_tab, bg=bg_color)
    inner_frame.place(relx=0.5, rely=0.5, anchor='center')

    # Input fields and labels on the left
    labels = ["Course Name", "Course Prefix", "Required/Elective", "Semester Offered"]
    entry_widgets = []
    for i, label in enumerate(labels):
        label_widget = tk.Label(inner_frame, text=label, bg=bg_color, fg='white', font=('Helvetica', 12))
        entry_widget = tk.Entry(inner_frame, font=('Helvetica', 12))
        label_widget.grid(row=i, column=0, padx=10, pady=5, sticky="e")
        entry_widget.grid(row=i, column=1, padx=10, pady=5, sticky="w")
        entry_widgets.append(entry_widget)

    # Course ID entry for update and delete
    course_id_label = tk.Label(inner_frame, text="Course ID", bg=bg_color, fg='white', font=('Helvetica', 12))
    course_id_label.grid(row=len(labels), column=0, padx=10, pady=5, sticky="e")
    course_id_entry = tk.Entry(inner_frame, font=('Helvetica', 12))
    course_id_entry.grid(row=len(labels), column=1, padx=10, pady=5, sticky="w")

    # Buttons for Add, Update, Delete
    add_btn = tk.Button(inner_frame, text="Add Course", bg=btn_color, fg='white', font=('Helvetica', 10),
                        command=lambda: add_course(conn, [e.get() for e in entry_widgets], course_table))
    add_btn.grid(row=len(labels) + 1, column=0, columnspan=2, padx=10, pady=10)

    update_btn = tk.Button(inner_frame, text="Update Course", bg=btn_color, fg='white', font=('Helvetica', 10),
                           command=lambda: update_course(conn, entry_widgets, course_table))
    update_btn.grid(row=len(labels) + 2, column=0, columnspan=2, padx=10, pady=10)

    delete_btn = tk.Button(inner_frame, text="Delete Course", bg=btn_color, fg='white', font=('Helvetica', 10),
                           command=lambda: delete_course(conn, course_table))
    delete_btn.grid(row=len(labels) + 3, column=0, columnspan=2, padx=10, pady=10)

    # Course table on the right
    columns = ("Course_ID", "Course Name", "Course Prefix", "Required/Elective", "Semester Offered")
    course_table = ttk.Treeview(inner_frame, columns=columns, show='headings')
    for col in columns:
        course_table.heading(col, text=col)
        course_table.column(col, anchor=tk.CENTER)
    course_table.grid(row=0, column=2, rowspan=len(labels)+4, padx=10, pady=10, sticky='nsew')

    # Fetch and display initial course data
    initial_data = fetch_course_data(conn)
    for data in initial_data:
        course_table.insert('', 'end', values=data)

    return courses_tab
