import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import date

# Function to create the SQLite database and tables
def create_database():
    conn = sqlite3.connect('blood_donation.db')
    cursor = conn.cursor()

    # Create donors table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS donors (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            phone TEXT NOT NULL,
            blood_group TEXT NOT NULL
        )
    ''')

    # Create donations table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS donations (
            id INTEGER PRIMARY KEY,
            donor_id INTEGER NOT NULL,
            donation_date DATE NOT NULL,
            amount_ml INTEGER NOT NULL,
            FOREIGN KEY (donor_id) REFERENCES donors(id)
        )
    ''')

    conn.commit()
    conn.close()

# Function to retrieve donor names from the database
def get_donor_names():
    conn = sqlite3.connect('blood_donation.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM donors')
    donors = [row[0] for row in cursor.fetchall()]
    conn.close()
    return donors

# Function to retrieve all donations with donor details from the database
def get_all_donations():
    conn = sqlite3.connect('blood_donation.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT donations.donation_date, donations.amount_ml, donors.name, donors.age, donors.phone, donors.blood_group
        FROM donations
        INNER JOIN donors ON donations.donor_id = donors.id
    ''')
    donations = cursor.fetchall()
    conn.close()
    return donations

# Function to display all recorded donations in a message box
def display_all_donations():
    donations = get_all_donations()
    if not donations:
        messagebox.showinfo('No Donations', 'No donations recorded yet.')
        return

    message = 'All Recorded Donations:\n\n'
    for donation in donations:
        donation_date, amount_ml, donor_name, donor_age, donor_phone, donor_blood_group = donation
        message += f'Date: {donation_date}\n'
        message += f'Donor Name: {donor_name}\n'
        message += f'Age: {donor_age}\n'
        message += f'Phone: {donor_phone}\n'
        message += f'Blood Group: {donor_blood_group}\n'
        message += f'Amount (ml): {amount_ml}\n'
        message += '-' * 30 + '\n'

    messagebox.showinfo('Recorded Donations', message)

# Function to add a new donor
def add_donor():
    name = name_entry.get()
    age = age_entry.get()
    phone = phone_entry.get()
    blood_group = blood_group_entry.get()

    if name == '' or age == '' or phone == '' or blood_group == '':
        messagebox.showerror('Error', 'Please fill in all fields')
        return

    try:
        age = int(age)  # Convert age to integer
        conn = sqlite3.connect('blood_donation.db')
        cursor = conn.cursor()

        # Insert new donor into the database
        cursor.execute('''
            INSERT INTO donors (name, age, phone, blood_group)
            VALUES (?, ?, ?, ?)
        ''', (name, age, phone, blood_group))

        conn.commit()
        conn.close()

        messagebox.showinfo('Success', 'Donor added successfully')

        # Refresh donor names in OptionMenu
        update_donor_dropdown()

        # Clear input fields after adding donor
        name_entry.delete(0, tk.END)
        age_entry.delete(0, tk.END)
        phone_entry.delete(0, tk.END)
        blood_group_entry.delete(0, tk.END)

    except ValueError:
        messagebox.showerror('Error', 'Invalid age. Please enter a valid number')

# Function to record a new donation
def record_donation():
    donor_name = donor_name_entry.get()
    amount_ml = amount_ml_entry.get()

    if donor_name == '' or amount_ml == '':
        messagebox.showerror('Error', 'Please select a donor and enter amount donated')
        return

    try:
        amount_ml = int(amount_ml)  # Convert amount to integer
        conn = sqlite3.connect('blood_donation.db')
        cursor = conn.cursor()

        # Retrieve donor id based on donor name
        cursor.execute('SELECT id FROM donors WHERE name = ?', (donor_name,))
        donor_id = cursor.fetchone()

        if donor_id:
            donor_id = donor_id[0]

            # Insert donation record into the database
            cursor.execute('''
                INSERT INTO donations (donor_id, donation_date, amount_ml)
                VALUES (?, ?, ?)
            ''', (donor_id, date.today(), amount_ml))

            conn.commit()
            conn.close()

            messagebox.showinfo('Success', 'Donation recorded successfully')

            # Clear input fields after recording donation
            amount_ml_entry.delete(0, tk.END)

        else:
            messagebox.showerror('Error', 'Donor not found')

    except ValueError:
        messagebox.showerror('Error', 'Invalid amount. Please enter a valid number')

# Function to update donor names in the OptionMenu
def update_donor_dropdown():
    donor_names = get_donor_names()
    donor_name_entry.set('')  # Clear the current selection
    menu = donor_name_dropdown["menu"]
    menu.delete(0, "end")  # Clear existing menu items

    if donor_names:
        for name in donor_names:
            menu.add_command(label=name, command=tk._setit(donor_name_entry, name))

# Create the database and tables if they don't exist
create_database()

# Create main Tkinter window
window = tk.Tk()
window.title('Blood Donation Management System')

# Add Donor Section
tk.Label(window, text='Add New Donor').pack(pady=10)

tk.Label(window, text='Name:').pack()
name_entry = tk.Entry(window)
name_entry.pack()

tk.Label(window, text='Age:').pack()
age_entry = tk.Entry(window)
age_entry.pack()

tk.Label(window, text='Phone:').pack()
phone_entry = tk.Entry(window)
phone_entry.pack()

tk.Label(window, text='Blood Group:').pack()
blood_group_entry = tk.Entry(window)
blood_group_entry.pack()

add_donor_button = tk.Button(window, text='Add Donor', command=add_donor)
add_donor_button.pack(pady=10)


# Dropdown to select donor
tk.Label(window, text='Select Donor:').pack()

# Create a StringVar to hold the selected donor name
donor_name_entry = tk.StringVar(window)

# Initialize donor names in OptionMenu
donor_name_dropdown = tk.OptionMenu(window, donor_name_entry, 'No donors found. Please add donors first.')
donor_name_dropdown.pack()

tk.Label(window, text='Amount (ml):').pack()
amount_ml_entry = tk.Entry(window)
amount_ml_entry.pack()

record_donation_button = tk.Button(window, text='Record Donation', command=record_donation)
record_donation_button.pack(pady=10)

# Button to display all recorded donations
show_donations_button = tk.Button(window, text='Show All Donations', command=display_all_donations)
show_donations_button.pack(pady=10)

# Update donor dropdown initially
update_donor_dropdown()

# Run Tkinter main loop
window.mainloop()

 # type: ignore