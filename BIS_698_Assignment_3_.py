# BIS 698 - Assignment 3: Customer Registration Screen (Figma)
# Name: Maheswara Reddy Varra
# Global ID: varra1m

import re
import customtkinter as ctk
from PIL import Image
import mysql.connector
from mysql.connector import Error
from tkinter import messagebox

        # APP CONFIG 
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

APP_TITLE = "varra1m_Customer_Registration"
APP_SIZE = "900x560"

RIGHT_BG = "#CFE9E3"
BTN_COLOR = "#2EC4B6"
BTN_HOVER = "#28B0A3"

IMAGE_PATH = "login.jpg"
IMAGE_SIZE = (280, 280)

        #  DB CONFIG
DB_CONFIG = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "Mahi$123",
    "database": "BUS698"
}

        #  REGEX 
NAME_RE = re.compile(r"^[A-Za-z]+(?:[ '-][A-Za-z]+)*$")  # allows spaces/hyphen/apostrophe
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def get_connection():
    """Create and return a new DB connection."""
    return mysql.connector.connect(**DB_CONFIG)


def normalize_inputs(fname: str, lname: str, mail: str):
    """Clean and standardize user inputs."""
    fname = fname.strip().title()
    lname = lname.strip().title()
    mail = mail.strip().lower()
    return fname, lname, mail


def validate_inputs(fname: str, lname: str, mail: str) -> bool:
    """Validate user inputs and show error messages if invalid."""
    if not fname:
        messagebox.showerror("Validation Error", "First Name is required.")
        return False
    if not NAME_RE.fullmatch(fname):
        messagebox.showerror("Validation Error", "First Name must contain only letters.")
        return False

    if not lname:
        messagebox.showerror("Validation Error", "Last Name is required.")
        return False
    if not NAME_RE.fullmatch(lname):
        messagebox.showerror("Validation Error", "Last Name must contain only letters.")
        return False

    if not mail:
        messagebox.showerror("Validation Error", "Email is required.")
        return False
    if not EMAIL_RE.fullmatch(mail):
        messagebox.showerror("Validation Error", "Please enter a valid email address.")
        return False

    return True


def email_exists(mail: str) -> bool:
    """Check if an email already exists in the customer table."""
    query = "SELECT 1 FROM customer WHERE email = %s LIMIT 1"
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (mail,))
            return cur.fetchone() is not None


def insert_customer(fname: str, lname: str, mail: str):
    """Insert a customer record into the database."""
    query = "INSERT INTO customer (first_name, last_name, email) VALUES (%s, %s, %s)"
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (fname, lname, mail))
            conn.commit()


def clear_fields():
    first_name.delete(0, "end")
    last_name.delete(0, "end")
    email.delete(0, "end")
    first_name.focus()


def register_customer():
    fname, lname, mail = normalize_inputs(first_name.get(), last_name.get(), email.get())

    if not validate_inputs(fname, lname, mail):
        return

    try:
        # Option 1: app-level duplicate check (nice UX)
        if email_exists(mail):
            messagebox.showerror("Duplicate Email", "This email is already registered.")
            return

        insert_customer(fname, lname, mail)
        messagebox.showinfo("Success", "Customer Registered Successfully ✅")
        clear_fields()

    except Error as e:
        # Option 2: handle UNIQUE constraint error (professional)
        if getattr(e, "errno", None) == 1062:
            messagebox.showerror("Duplicate Email", "This email is already registered.")
        else:
            messagebox.showerror("Database Error", f"Error: {e}")


#  USER INTERFACE 
app = ctk.CTk()
app.title(APP_TITLE)
app.geometry(APP_SIZE)
app.resizable(False, False)

# Left frame
left_frame = ctk.CTkFrame(app, width=450, height=560, fg_color="white", corner_radius=0)
left_frame.pack(side="left", fill="both")

# Image load
try:
    pil_img = Image.open(IMAGE_PATH)
    img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=IMAGE_SIZE)
    ctk.CTkLabel(left_frame, image=img, text="").place(relx=0.5, rely=0.5, anchor="center")
except Exception:
    ctk.CTkLabel(left_frame, text="Image not found").place(relx=0.5, rely=0.5, anchor="center")

# Right frame
right_frame = ctk.CTkFrame(app, width=450, height=560, fg_color=RIGHT_BG, corner_radius=0)
right_frame.pack(side="right", fill="both")

# Form container
form = ctk.CTkFrame(right_frame, fg_color="transparent")
form.place(relx=0.5, rely=0.5, anchor="center")

# Title
ctk.CTkLabel(
    form,
    text="Register Customer",
    font=("Inter", 22, "bold"),
    text_color="#2F4F4F"
).pack(pady=(0, 20))

# Inputs
ctk.CTkLabel(form, text="First Name").pack(anchor="w")
first_name = ctk.CTkEntry(form, width=280, height=35, placeholder_text="John")
first_name.pack(pady=(5, 10))

ctk.CTkLabel(form, text="Last Name").pack(anchor="w")
last_name = ctk.CTkEntry(form, width=280, height=35, placeholder_text="Doe")
last_name.pack(pady=(5, 10))

ctk.CTkLabel(form, text="Email").pack(anchor="w")
email = ctk.CTkEntry(form, width=280, height=35, placeholder_text="johndoe@gmail.com")
email.pack(pady=(5, 15))

# Buttons
ctk.CTkButton(
    form,
    text="Register",
    width=280,
    height=38,
    fg_color=BTN_COLOR,
    hover_color=BTN_HOVER,
    command=register_customer
).pack(pady=(0, 10))

ctk.CTkButton(
    form,
    text="Clear",
    width=280,
    height=35,
    fg_color="gray",
    command=clear_fields
).pack(pady=(0, 10))

# Footer (UI only)
ctk.CTkLabel(
    form,
    text="Already have an account? Click here to log in",
    font=("Inter", 10),
    text_color="#555555"
).pack()

# UX: press Enter to register
app.bind("<Return>", lambda e: register_customer())

# Focus first field
first_name.focus()

app.mainloop()

