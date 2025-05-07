import json
import random
import string
import tkinter as tk
from tkinter import messagebox
import pyperclip

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = string.ascii_letters
    digits = string.digits
    symbols = string.punctuation

    characters = letters + digits + symbols
    password = ''.join(random.choice(characters) for _ in range(12))
    password_entry.delete(0, tk.END)
    password_entry.insert(0, password)
    pyperclip.copy(password)  # Copy to clipboard


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_password():
    website = website_entry.get().strip()
    email = email_entry.get().strip()
    password = password_entry.get().strip()
    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }

    if not website or not password:
        messagebox.showwarning("Oops", "Please don't leave website or password fields empty!")
        return

    try:
        with open("data.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}

    data.update(new_data)

    with open("data.json", "w") as file:
        json.dump(data, file, indent=4)

    website_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)


# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
    website = website_entry.get().strip()
    try:
        with open("data.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        messagebox.showinfo("Error", "No Data File Found")
        return

    if website in data:
        email = data[website]["email"]
        password = data[website]["password"]
        messagebox.showinfo(website, f"Email: {email}\nPassword: {password}")
        pyperclip.copy(password)
    else:
        messagebox.showinfo("Not Found", f"No details for '{website}' exist.")


# ---------------------------- UI SETUP ------------------------------- #
window = tk.Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

# Labels
tk.Label(text="Website:").grid(row=1, column=0)
tk.Label(text="Email/Username:").grid(row=2, column=0)
tk.Label(text="Password:").grid(row=3, column=0)

# Entries
website_entry = tk.Entry(width=21)
website_entry.grid(row=1, column=1)
website_entry.focus()

email_entry = tk.Entry(width=35)
email_entry.grid(row=2, column=1, columnspan=2)
email_entry.insert(0, "")

password_entry = tk.Entry(width=21)
password_entry.grid(row=3, column=1)

# Buttons
tk.Button(text="Search", width=13, command=find_password).grid(row=1, column=2)
tk.Button(text="Generate Password", command=generate_password).grid(row=3, column=2)
tk.Button(text="Add", width=36, command=save_password).grid(row=4, column=1, columnspan=2)

window.mainloop()
