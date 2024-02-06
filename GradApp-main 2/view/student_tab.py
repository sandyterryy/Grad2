import tkinter as tk
from tkinter import ttk
from functions import create_table

def fetch_student_data(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT Student_id, Fname, Lname FROM student")
    return cursor.fetchall()

def search_student(student_id, conn, student_info_label):
    cursor = conn.cursor()
    cursor.execute("SELECT Fname, Lname FROM student WHERE Student_id=?", (student_id,))
    student_data = cursor.fetchone()

    if student_data:
        student_info_label.config(text=f"Information for Student ID: {student_id}\n"
                                       f"First Name: {student_data[0]}\n"
                                       f"Last Name: {student_data[1]}")
    else:
        student_info_label.config(text="Student not found")

def create_student(conn, entry_widgets, student_table, student_info_label):
    cursor = conn.cursor()

    # Assuming the order of entry widgets corresponds to the table columns
    data = tuple(entry_widgets[key].get() for key in entry_widgets)

    cursor.execute("INSERT INTO student (FName, Lname, Personal_email, Bobcat_email, Phone, GC_ID, Advisor_Hold, start_date, Grad_date, Double_Bobcat) VALUES (?,?,?,?,?,?,?,?,?,?)", data)
    conn.commit()

    # Fetching the last inserted Student ID
    cursor.execute("SELECT last_insert_rowid()")
    student_id = cursor.fetchone()[0]

    # Update the Treeview with the new data
    student_table.insert('', 'end', values=(student_id, entry_widgets["First Name"].get(), entry_widgets["Last Name"].get()))

    # Displaying student information in the display area
    student_info_label.config(text=f"Information for Student ID: {student_id}\n"
                                   f"First Name: {entry_widgets['First Name'].get()}\n"
                                   f"Last Name: {entry_widgets['Last Name'].get()}")

def update_student(conn, student_id, entry_widgets, student_table, student_info_label):
    cursor = conn.cursor()

    # Assuming the order of entry widgets corresponds to the table columns
    data = tuple(entry_widgets[key].get() for key in entry_widgets)

    cursor.execute("UPDATE student SET FName=?, Lname=?, Personal_email=?, Bobcat_email=?, Phone=?, GC_ID=?, Advisor_Hold=?, start_date=?, Grad_date=?, Double_Bobcat=? WHERE Student_id=?", (*data, student_id))
    conn.commit()

    # Fetch the updated data from the database
    cursor.execute("SELECT FName, Lname FROM student WHERE Student_id=?", (student_id,))
    updated_data = cursor.fetchone()

    # Update the Treeview with the updated data
    for item in student_table.selection():
        student_table.item(item, values=(student_id, updated_data[0], updated_data[1]))

    # Displaying student information in the display area with updated data
    student_info_label.config(text=f"Information for Student ID: {student_id}\n"
                                   f"First Name: {updated_data[0]}\n"
                                   f"Last Name: {updated_data[1]}")




def delete_student(conn, student_id, student_table, student_info_label):
    cursor = conn.cursor()

    cursor.execute("DELETE FROM student WHERE Student_id=?", (student_id,))
    conn.commit()

    # Remove the selected student from the Treeview
    for item in student_table.selection():
        student_table.delete(item)

    # Clear student information in the display area
    student_info_label.config(text="")

def create_student_tab(notebook, bg_color, btn_color, conn):
    student_tab = tk.Frame(notebook, bg=bg_color)
    student_tab.pack(expand=True, fill='both')

    # Centering content with an inner frame
    inner_frame = tk.Frame(student_tab, bg=bg_color)
    inner_frame.place(relx=0.5, rely=0.5, anchor='center')

    # Input fields and labels
    labels = ["First Name", "Last Name", "Personal Email", "Bobcats Email", "Phone Number", "GC ID", "Advisor Hold", "Start Date", "Grad Date", "Double Bobcat"]
    entry_widgets = {}
    for i, label in enumerate(labels):
        label_widget = tk.Label(inner_frame, text=label, bg=bg_color, fg='white', font=('Helvetica', 12))
        entry_widget = tk.Entry(inner_frame, font=('Helvetica', 12))
        label_widget.grid(row=i, column=0, padx=10, pady=5, sticky="e")
        entry_widget.grid(row=i, column=1, padx=10, pady=5, sticky="w")
        entry_widgets[label] = entry_widget

    # Create Student button
    create_student_btn = ttk.Button(inner_frame, text="Create Student", style='GCSU.TButton',
                                    command=lambda: create_student(conn, entry_widgets, student_table, student_info_label))
    create_student_btn.grid(row=len(labels), column=1, padx=10, pady=10)

    # Student table
    columns = ("Student ID", "First Name", "Last Name")
    student_table = create_table(inner_frame, columns)
    student_table.grid(row=0, column=2, rowspan=len(labels) + 1, padx=10, pady=10, sticky='ns')

    # Fetch and display initial student data
    initial_data = fetch_student_data(conn)
    for data in initial_data:
        student_table.insert('', 'end', values=(data[0], data[1], data[2]))

    # Search bar
    search_label = tk.Label(inner_frame, text="Student ID:", bg=bg_color, fg='white', font=('Helvetica', 12))
    search_label.grid(row=len(labels) + 1, column=0, padx=10, pady=10, sticky="e")
    search_entry = tk.Entry(inner_frame, font=('Helvetica', 12))
    search_entry.grid(row=len(labels) + 1, column=1, padx=10, pady=10, sticky="w")

    def search_student_wrapper():
        search_student(search_entry.get(), conn, student_info_label)

    # Search button
    search_button = ttk.Button(inner_frame, text="Search", style='GCSU.TButton', command=search_student_wrapper)
    search_button.grid(row=len(labels) + 1, column=1, padx=10, pady=10)

    # Student information display area
    student_info_label = tk.Label(inner_frame, text="", bg=bg_color, fg='white', font=('Helvetica', 12))
    student_info_label.grid(row=len(labels) + 2, column=1, padx=10, pady=10)

    # Function to get selected student ID
    def get_selected_student_id():
        selected_item = student_table.selection()
        if selected_item:
            student_id = student_table.item(selected_item, 'values')[0]
            return student_id
        else:
            return None

    # Update button
    def update_student_wrapper():
        student_id = get_selected_student_id()
        if student_id:
            update_student(conn, student_id, entry_widgets, student_table, student_info_label)
        else:
            tkinter.messagebox.showerror("Error", "Please select a student to update")

    update_student_btn = ttk.Button(inner_frame, text="Update Student", style='GCSU.TButton', command=update_student_wrapper)
    update_student_btn.grid(row=len(labels) + 3, column=0, padx=10, pady=10)

    # Delete button
    def delete_student_wrapper():
        student_id = get_selected_student_id()
        if student_id:
            delete_student(conn, student_id, student_table, student_info_label)
        else:
            tkinter.messagebox.showerror("Error", "Please select a student to delete")

    delete_student_btn = ttk.Button(inner_frame, text="Delete Student", style='GCSU.TButton', command=delete_student_wrapper)
    delete_student_btn.grid(row=len(labels) + 3, column=1, padx=10, pady=10)

    return student_tab
