import tkinter as tk
import customtkinter as ctk
import sqlite3
from datetime import date
from tkinter import messagebox

conn = sqlite3.connect("money.db")
cursor = conn.cursor()

cursor.execute(
  '''
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY,
        description TEXT,
        amount REAL,
        category TEXT,
        date DATE
    )
  '''
)
conn.commit()

def add_transaction():
    description = entry_description.get()
    amount = entry_amount.get()
    category = entry_category.get()

    if description and amount and category:
        current_date = date.today()
        cursor.execute("INSERT INTO transactions (description, amount, category, date) VALUES(? ,? ,? ,?)", (description, amount, category, current_date))
        conn.commit()
        messagebox.showinfo("Success", "Added Successfully")
        entry_description.delete(0, tk.END)
        entry_amount.delete(0, tk.END)
        entry_category.delete(0, tk.END)
        update_transaction()
    else:
        messagebox.showerror("Error", "Please fill in all fields")

def update_transaction():
    cursor.execute("SELECT * FROM transactions")
    transactions = cursor.fetchall()
    transaction_list.delete(1.0, tk.END)
    for transaction in transactions:
        transaction_list.insert(tk.END, f"\n{transaction[4]} - {transaction[1]} - {transaction[2]} - {transaction[3]}")

root = ctk.CTk()
root.geometry("700x500")
root.title("Finance Tracker")

ctk.set_appearance_mode("dark")

frame = ctk.CTkFrame(root)
frame.pack(fill="x", padx=100)

description_frame = ctk.CTkFrame(frame)
description_frame.pack(padx=100, pady=(20, 5), fill="both")

label_description = ctk.CTkLabel(description_frame, text="Description")
label_description.pack()

entry_description = ctk.CTkEntry(description_frame)
entry_description.pack(padx=20, pady=20)

amount_frame = ctk.CTkFrame(frame)
amount_frame.pack(padx=100, pady=(20, 5), fill="both")

amount_description = ctk.CTkLabel(amount_frame, text="Amount")
amount_description.pack()

entry_amount = ctk.CTkEntry(amount_frame)
entry_amount.pack(padx=20, pady=20)

category_frame = ctk.CTkFrame(frame)
category_frame.pack(padx=100, pady=(20, 5), fill="both")

category_description = ctk.CTkLabel(category_frame, text="Category")
category_description.pack()

entry_category = ctk.CTkEntry(category_frame)
entry_category.pack(padx=20, pady=20)

btn_add = ctk.CTkButton(frame, text="Add Transaction", command=add_transaction)
btn_add.pack(pady=10, fill="x", padx=100)

transaction_list = ctk.CTkTextbox(root, height=100, width=50)
transaction_list.pack(pady=10, padx=10, fill="x")

update_transaction()
root.mainloop()