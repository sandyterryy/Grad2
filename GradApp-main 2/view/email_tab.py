import tkinter as tk
from tkinter import ttk

def create_email_tab(notebook, bg_color, btn_color, conn):
    email_tab = tk.Frame(notebook, bg=bg_color)
    email_tab.pack(expand=True, fill='both')

    # Centering content with an inner frame
    inner_frame = tk.Frame(email_tab, bg=bg_color)
    inner_frame.place(relx=0.5, rely=0.5, anchor='center')

    # Email label
    email_label = tk.Label(inner_frame, text="Email Content", bg=bg_color, fg='white', font=('Helvetica', 12))
    email_label.pack(padx=10, pady=10)

    # Send Registration Email button
    reg_email_button = ttk.Button(inner_frame, text="Send Registration Email", style='GCSU.TButton')
    reg_email_button.pack(pady=10)

    # Send Graduation Email button
    grad_email_button = ttk.Button(inner_frame, text="Send Graduation Email", style='GCSU.TButton')
    grad_email_button.pack(pady=10)

    # Search bar
    search_label = tk.Label(inner_frame, text="Student ID:", bg=bg_color, fg='white', font=('Helvetica', 12))
    search_label.pack(padx=10, pady=10)
    search_entry = tk.Entry(inner_frame, font=('Helvetica', 12))
    search_entry.pack(padx=10, pady=10)
    search_button = ttk.Button(inner_frame, text="Search", style='GCSU.TButton', command=lambda: search_student(search_entry.get()))
    search_button.pack(pady=10)

    # Student information display area
    student_info_label = tk.Label(inner_frame, text="", bg=bg_color, fg='white', font=('Helvetica', 12))
    student_info_label.pack(pady=10)

    def search_student(student_id):
        # Implement the logic to search and display student information here
        # For example:
        student_info_label.config(text=f"Information for Student ID: {student_id}")

    return email_tab
