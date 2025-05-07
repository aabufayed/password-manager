import json
import string
import secrets
import tkinter as tk
from tkinter import messagebox
import pyperclip


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = string.ascii_letters
    digits = string.digits
    symbols = string.punctuation

    # Ensure at least one of each character type
    password = [
        secrets.choice(letters),
        secrets.choice(digits),
        secrets.choice(symbols)
    ]

    # Add remaining characters
    remaining_length = 9  # Total 12 characters
    all_chars = letters + digits + symbols
    password += [secrets.choice(all_chars) for _ in range(remaining_length)]

    # Shuffle to avoid predictable patterns
    secrets.SystemRandom().shuffle(password)
    password = ''.join(password)

    password_entry.delete(0, tk.END)
    password_entry.insert(0, password)
    pyperclip.copy(password)
    messagebox.showinfo("Success", "Password generated and copied to clipboard!")


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_password():
    website = website_entry.get().strip()
    email = email_entry.get().strip()
    password = password_entry.get().strip()

    if not website or not password:
        messagebox.showwarning("Oops", "Please fill in both website and password fields!")
        return

    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }

    try:
        with open("data.json", "r") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = {}
                messagebox.showwarning("Warning", "Corrupted data file. Starting fresh.")
    except FileNotFoundError:
        data = {}

    if website in data:
        if not messagebox.askyesno("Confirm", f"Entry for {website} exists. Overwrite?"):
            return

    data.update(new_data)

    try:
        with open("data.json", "w") as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save data: {str(e)}")
        return

    website_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)
    messagebox.showinfo("Success", "Credentials saved successfully!")


# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
    website = website_entry.get().strip()
    if not website:
        messagebox.showwarning("Oops", "Please enter a website to search.")
        return

    try:
        with open("data.json", "r") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                messagebox.showerror("Error", "Corrupted data file.")
                return
    except FileNotFoundError:
        messagebox.showinfo("Error", "No data file found.")
        return

    if website in data:
        email = data[website]["email"]
        password = data[website]["password"]
        pyperclip.copy(password)
        messagebox.showinfo(website, f"Email: {email}\nPassword: {password}\n\nPassword copied to clipboard!")
    else:
        messagebox.showinfo("Not Found", f"No entry found for '{website}'")


# ---------------------------- UI SETUP ------------------------------- #
window = tk.Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

# Labels
tk.Label(text="Website:").grid(row=1, column=0, sticky="e")
tk.Label(text="Email/Username:").grid(row=2, column=0, sticky="e")
tk.Label(text="Password:").grid(row=3, column=0, sticky="e")

# Entries
website_entry = tk.Entry(width=21)
website_entry.grid(row=1, column=1, sticky="ew")
website_entry.focus()

email_entry = tk.Entry(width=35)
email_entry.grid(row=2, column=1, columnspan=2, sticky="ew")

password_entry = tk.Entry(width=21)
password_entry.grid(row=3, column=1, sticky="ew")

# Buttons
tk.Button(text="Search", width=13, command=find_password).grid(row=1, column=2, sticky="ew")
tk.Button(text="Generate Password", command=generate_password).grid(row=3, column=2, sticky="ew")
tk.Button(text="Add", width=36, command=save_password).grid(row=4, column=1, columnspan=2, sticky="ew")

# Grid configuration
window.columnconfigure(1, weight=1)
window.rowconfigure(4, weight=1)

window.mainloop()