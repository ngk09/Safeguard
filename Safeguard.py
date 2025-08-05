import os
import webbrowser
from tkinter import Tk, Button, Entry, Label, Listbox, Scrollbar, END, messagebox, PhotoImage
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
import pygame  # Add pygame for sound control

# File to store emergency contacts
CONTACTS_FILE = "emergency_contacts.txt"

# Admin login credentials
ADMIN_USERNAME = "NGK"
ADMIN_PASSWORD = "NGKV123"

# Initialize pygame mixer for sound control
pygame.mixer.init()

# File to store the siren sound
SIREN_FILE = "siren.mp3"
siren_sound = None

# Open Google Maps and show nearby police stations
def open_police_stations():
    sahyadri_location = "12.8665796,74.9253776"
    url = f""
    webbrowser.open(url)

# Function to send email
def send_email(to_email, subject, message):
    sender_email = "raogknandan@gmail.com"
    sender_password = "huuy kpgz uqcj hvbn"  # Use environment variables for sensitive info

    try:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to_email, msg.as_string())
        
        print(f"Email sent successfully to {to_email}!")
    except Exception as e:
        print(f"Failed to send email to {to_email}: {e}")

# Add contact to file
def add_contact(name, email):
    global contact_list
    if not name or not email:
        messagebox.showwarning("Input Error", "Both Name and Email are required!")
        return
    with open(CONTACTS_FILE, "a") as file:
        file.write(f"{name},{email}\n")
    contact_list.insert(END, f"{name} ({email})")
    name_entry.delete(0, END)
    email_entry.delete(0, END)
    messagebox.showinfo("Success", f"Contact {name} added successfully!")

# Load contacts from file
def load_contacts():
    global contact_list
    if not os.path.exists(CONTACTS_FILE):
        return
    with open(CONTACTS_FILE, "r") as file:
        for line in file:
            if line.strip():
                try:
                    name, email = line.strip().split(",")
                    contact_list.insert(END, f"{name} ({email})")
                except ValueError:
                    print(f"Skipping invalid contact line: {line.strip()}")

# Send SOS emails with fixed location (Sahyadri College)
def send_sos():
    # Fixed location for Sahyadri College of Engineering & Management
    google_maps_link = "https://www.google.com/maps/place/Sahyadri+College+Of+Engineering+%26+Management+(Autonomous)/@12.8665796,74.9227973,17z/data=!3m1!4b1!4m6!3m5!1s0x3ba358ff28ef6cf3:0xe93953598f53c53c!8m2!3d12.8665796!4d74.9253776!16s%2Fg%2F11j19z28p8?entry=ttu"
    latitude = 12.8665796
    longitude = 74.9253776

    subject = "SOS Alert"
    message = f"""This is an SOS Alert! I need immediate assistance. 

My current location is: {latitude}, {longitude} (latitude, longitude).

You can view my location here: {google_maps_link}

Please help!"""

    for i in range(contact_list.size()):
        contact = contact_list.get(i)
        name, email = contact.rsplit("(", 1)
        email = email.strip(")")
        try:
            send_email(email, subject, message)
            messagebox.showinfo("Success", f"SOS Alert sent to {name.strip()}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send SOS Alert to {name.strip()}: {e}")

# Play siren
def play_siren():
    global siren_sound
    if not os.path.exists(SIREN_FILE):
        messagebox.showerror("File Not Found", "Siren file not found!")
        return
    if siren_sound is None or not pygame.mixer.get_busy():
        siren_sound = pygame.mixer.Sound(SIREN_FILE)
        siren_sound.play(-1)  # Loop indefinitely until stopped

# Stop siren
def stop_siren():
    global siren_sound
    if siren_sound is not None:
        siren_sound.stop()  # Stop the sound
        siren_sound = None
        messagebox.showinfo("Stop Siren", "Siren stopped successfully!")

# Validate admin login
def validate_admin_login(event=None):
    username = username_entry.get()
    password = password_entry.get()

    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        messagebox.showinfo("Login Success", "Admin login successful!")
        login_window.destroy()
        open_main_app()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password!")

# Admin login window
def open_admin_login():
    global login_window, username_entry, password_entry

    login_window = Tk()
    login_window.title("Admin Login")
    login_window.geometry("300x200")

    Label(login_window, text="Username:", font=("Arial", 12)).pack(pady=5)
    username_entry = Entry(login_window, font=("Arial", 12))
    username_entry.pack(pady=5)

    Label(login_window, text="Password:", font=("Arial", 12)).pack(pady=5)
    password_entry = Entry(login_window, font=("Arial", 12), show="*")
    password_entry.pack(pady=5)

    password_entry.bind("<Return>", validate_admin_login)
    Button(login_window, text="Login", command=validate_admin_login, font=("Arial", 12), bg="#66b3ff").pack(pady=15)

    login_window.mainloop()

# Main application window
def open_main_app():
    global contact_list, name_entry, email_entry

    app = Tk()
    app.title("Safeguard Women Safety App")
    app.geometry("600x600")
    app.config(bg="#f5f5f5")

    font_header = ("Arial", 16, "bold")
    font_button = ("Arial", 12)
    font_input = ("Arial", 12)

    sos_logo = PhotoImage(file="sos_logo.png")
    sos_button = Button(app, image=sos_logo, command=send_sos, bg="#ff4d4d", bd=0, relief="solid", width=100, height=100)
    sos_button.place(x=20, y=20)

    map_logo = PhotoImage(file="map_logo.png")
    map_button = Button(app, image=map_logo, command=open_police_stations, bg="#4d94ff", bd=0, relief="solid", width=100, height=100)
    map_button.place(x=470, y=20)

    Label(app, text="Name:", font=font_header, bg="#f5f5f5").pack(pady=5)
    name_entry = Entry(app, width=30, font=font_input, bd=2)
    name_entry.pack(pady=5)

    Label(app, text="Email:", font=font_header, bg="#f5f5f5").pack(pady=5)
    email_entry = Entry(app, width=30, font=font_input, bd=2)
    email_entry.pack(pady=5)

    Button(app, text="Add Contact", command=lambda: add_contact(name_entry.get(), email_entry.get()), bg="#66b3ff", font=font_button, width=15).pack(pady=15)

    Label(app, text="Emergency Contacts:", font=font_header, bg="#f5f5f5").pack(pady=10)

    scrollbar = Scrollbar(app)
    scrollbar.pack(side="right", fill="y")

    contact_list = Listbox(app, width=50, height=10, yscrollcommand=scrollbar.set, selectmode="multiple", font=font_input, bd=2)
    contact_list.pack(pady=10)
    scrollbar.config(command=contact_list.yview)

    Button(app, text="Play Siren", command=play_siren, bg="#ff9900", font=font_button, width=15).pack(pady=10)
    Button(app, text="Stop Siren", command=stop_siren, bg="#99ff99", font=font_button, width=15).pack(pady=10)

    load_contacts()

    app.mainloop()

# Start the admin login
open_admin_login()
