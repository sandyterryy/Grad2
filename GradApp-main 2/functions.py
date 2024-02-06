import tkinter as tk
from tkinter import ttk

def create_table(parent, columns):
    table = ttk.Treeview(parent, columns=columns, show='headings')
    for col in columns:
        table.heading(col, text=col)
        table.column(col, anchor=tk.CENTER)
    return table
