import tkinter as tk
from tkinter import messagebox
import sqlite3
conn = sqlite3.connect("library.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
)
""")

conn.commit()
def add_book():
    book = entry.get()
    if book == "":
        messagebox.showwarning("Warning", "Book name cannot be empty")
        return

    cur.execute("INSERT INTO books (name) VALUES (?)", (book,))
    conn.commit()
    entry.delete(0, tk.END)
    show_books()
    messagebox.showinfo("Success", "Book added successfully")


def show_books():
    listbox.delete(0, tk.END)
    cur.execute("SELECT * FROM books")
    records = cur.fetchall()

    for row in records:
        listbox.insert(tk.END, f"{row[0]} - {row[1]}")


def delete_book():
    selected = listbox.curselection()
    if not selected:
        messagebox.showwarning("Warning", "Select a book to delete")
        return

    book_id = listbox.get(selected).split(" - ")[0]
    cur.execute("DELETE FROM books WHERE id=?", (book_id,))
    conn.commit()
    show_books()
    messagebox.showinfo("Deleted", "Book removed successfully")


def search_book():
    book = entry.get()
    listbox.delete(0, tk.END)

    cur.execute("SELECT * FROM books WHERE name LIKE ?", ('%' + book + '%',))
    records = cur.fetchall()

    if records:
        for row in records:
            listbox.insert(tk.END, f"{row[0]} - {row[1]}")
    else:
        messagebox.showinfo("Result", "Book not found")


def count_books():
    cur.execute("SELECT COUNT(*) FROM books")
    total = cur.fetchone()[0]
    messagebox.showinfo("Total Books", f"Total books in library: {total}")
root = tk.Tk()
root.title("Library Management System")
root.geometry("500x450")
root.resizable(False, False)

title = tk.Label(root, text="📚 Library Management System", font=("Arial", 16, "bold"))
title.pack(pady=10)

entry = tk.Entry(root, font=("Arial", 14), width=30)
entry.pack(pady=10)

btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Add Book", width=12, command=add_book).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Search Book", width=12, command=search_book).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="Delete Book", width=12, command=delete_book).grid(row=1, column=0, padx=5, pady=5)
tk.Button(btn_frame, text="Count Books", width=12, command=count_books).grid(row=1, column=1, padx=5, pady=5)

listbox = tk.Listbox(root, width=50, height=10, font=("Arial", 12))
listbox.pack(pady=10)

show_books()
root.mainloop()
