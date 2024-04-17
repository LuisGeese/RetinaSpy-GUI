import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox

# Setting appearance and color theme
ctk.set_appearance_mode("dark")  # 'dark', 'light', 'system'
ctk.set_default_color_theme("green")  # Themes like 'blue', 'green', 'dark-blue'

app = ctk.CTk()
app.geometry("480x288")  # Adjusted size for better layout
app.title("RetinaSpy")

app.overrideredirect(True)

# Variable to keep track of the currently active entry field
current_active_entry = None

def login():
    username = "retinaspy"
    password = "12345"

    if user_entry.get() == username and user_pass.get() == password:
        messagebox.showinfo(title="Login Successful", message="You have logged in Successfully")
    elif user_entry.get() == username and user_pass.get() != password:
        messagebox.showwarning(title='Wrong password', message='Please check your password')
    elif user_entry.get() != username and user_pass.get() == password:
        messagebox.showwarning(title='Wrong username', message='Please check your username')
    else:
        messagebox.showerror(title="Login Failed", message="Invalid Username and password")

def set_current_active_entry(entry_widget):
    global current_active_entry
    current_active_entry = entry_widget

def keyboard_action(key):
    if current_active_entry:
        if key == "Backspace":
            current_text = current_active_entry.get()[:-1]
        elif key == "Space":
            current_text = current_active_entry.get() + " "
        else:
            current_text = current_active_entry.get() + key
        current_active_entry.delete(0, tk.END)
        current_active_entry.insert(0, current_text)

frame = ctk.CTkFrame(master=app)
frame.pack(pady=20, padx=40, fill='both', expand=True)

user_entry = ctk.CTkEntry(master=frame, placeholder_text="Username")
user_entry.pack(pady=5, padx=10)
user_entry.bind("<FocusIn>", lambda event: set_current_active_entry(user_entry))

user_pass = ctk.CTkEntry(master=frame, placeholder_text="Password", show="*")
user_pass.pack(pady=5, padx=10)
user_pass.bind("<FocusIn>", lambda event: set_current_active_entry(user_pass))

button = ctk.CTkButton(master=frame, text='Login', command=login)
button.pack(pady=5, padx=10)

def create_keyboard(frame):
    keys = [
        ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-'],
        ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '='],
        ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'Backspace'],
        ['z', 'x', 'c', 'v', 'b', 'n', 'm', 'Space']
    ]

    for i, row in enumerate(keys):
        row_frame = ctk.CTkFrame(master=frame)
        row_frame.pack(fill='x', padx=5, pady=2)
        for key in row:
            btn = ctk.CTkButton(master=row_frame, text=key, width=100 if key in ["Space", "Backspace"] else 30, height=30,
                                command=lambda k=key: keyboard_action(k))
            btn.pack(side='left', expand=True if key in ["Space", "Backspace"] else False, fill='x' if key in ["Space", "Backspace"] else None, padx=2)

# Create a keyboard
create_keyboard(frame)

app.mainloop()
