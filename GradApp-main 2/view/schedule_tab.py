import tkinter as tk
from tkinter import ttk
from functions import create_table

def create_schedule_tab(notebook, bg_color, btn_color, conn):
    schedule_tab = tk.Frame(notebook, bg=bg_color)
    schedule_tab.pack(expand=True, fill='both')

    # Centering content with an inner frame
    inner_frame = tk.Frame(schedule_tab, bg=bg_color)
    inner_frame.place(relx=0.5, rely=0.5, anchor='center')

    # Create and place table
    schedule_table = create_table(inner_frame, ["Semester", "Year", "Course Name", "Info"])
    schedule_table.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

    # Example button for schedule update
    schedule_button = ttk.Button(inner_frame, text="Update Schedule", style='GCSU.TButton')
    schedule_button.grid(row=1, column=0, padx=10, pady=10)

    return schedule_tab
