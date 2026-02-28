
# BIS 698 - Assignment 3_Customer Registration Screen by using figma
# Name: Maheswara Reddy Varra
#Global id: varra1m


import customtkinter as ctk
from PIL import Image

ctk.set_appearance_mode("light")

app = ctk.CTk()
app.title("varra1m_Customer_Registration")
app.geometry("900x560")
app.resizable(False, False)

#left 
left_frame = ctk.CTkFrame(app, width=450, height=560, fg_color="white")
left_frame.pack(side="left", fill="both")

# Image
img = ctk.CTkImage(
    light_image=Image.open("login.jpg"),
    size=(280, 280)
)

img_label = ctk.CTkLabel(left_frame, image=img, text="")
img_label.place(relx=0.5, rely=0.5, anchor="center")

#right 
right_frame = ctk.CTkFrame(app, width=450, height=560, fg_color="#CFE9E3")
right_frame.pack(side="right", fill="both")

# Center Form
form = ctk.CTkFrame(right_frame, fg_color="transparent")
form.place(relx=0.5, rely=0.5, anchor="center")

# TITL
title = ctk.CTkLabel(
    form,
    text="Register Customer",
    font=("inter", 22, "bold"),
    text_color="#2F4F4F"
)
title.pack(pady=(0, 20))

# INPUT FIELDS 
ctk.CTkLabel(form, text="First Name").pack(anchor="w")
first_name = ctk.CTkEntry(form, width=280, height=35, placeholder_text="john")
first_name.pack(pady=(5, 10))

ctk.CTkLabel(form, text="Last Name").pack(anchor="w")
last_name = ctk.CTkEntry(form, width=280, height=35, placeholder_text="doe")
last_name.pack(pady=(5, 10))

ctk.CTkLabel(form, text="Email").pack(anchor="w")
email = ctk.CTkEntry(form, width=280, height=35, placeholder_text="johndoe@gmail.com")
email.pack(pady=(5, 15))

# BUTTON 
register_btn = ctk.CTkButton(
    form,
    text="Register",
    width=280,
    height=38,
    fg_color="#2EC4B6",
    hover_color="#28B0A3"
)
register_btn.pack(pady=(0, 10))

# FOOTER 
footer = ctk.CTkLabel(
    form,
    text="Already have an account? click here to log in",
    font=("inter", 10,),
    text_color="#555555"
)
footer.pack()

app.mainloop()


