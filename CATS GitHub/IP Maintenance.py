import tkinter as tk
from tkinter import ttk, messagebox
import re
import csv
import os

class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.hover)
        self.widget.bind("<Leave>", self.leave)

    def hover(self, event=None):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        label = tk.Label(self.tooltip, text=self.text, background="lightblue", font=("Arial", 24), wraplength=500, relief="solid", borderwidth=3, padx=10)
        label.pack()

    def leave(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()

# File path
file_path = '/home/kali/CATS/MyNetwork.csv'
#file_path = 'C:/kali/CATS/MyNetwork.csv'

# Regular expression for validating an IP Address
ip_pattern = re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$')

def validate_ip(ip):
    """Validate the IP Address using regular expression."""
    return re.match(ip_pattern, ip) is not None

def save_data(ip, mac, name, edit=False, original_data=None):
    """Save or edit data in the comma-delimited text file."""
    if not validate_ip(ip):
        messagebox.showerror("Error", "Invalid IP Address format.")
        return False

    # Ensure the directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    updated = False
    new_data = [ip, mac, name]
    rows = []

    # Read the existing data and update if in edit mode
    if os.path.exists(file_path):
        with open(file_path, 'r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                # Check if the row matches the original data for editing
                if edit and original_data and row == original_data.split(', '):
                    rows.append(new_data)
                    updated = True
                else:
                    rows.append(row)

    if not updated and edit:
        # If supposed to edit but no match found, show error (or decide how to handle this case)
        messagebox.showerror("Error", "Original data not found for edit.")
        return False
    elif not edit:
        # If not in edit mode, append the new data
        rows.append(new_data)

    # Write the data back to the file
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)

    messagebox.showinfo("Success", "Data saved successfully.")
    load_data()  # Refresh the data in the dropdown after saving
    return True

def delete_data():
    """Delete the selected entry from the file."""
    selected = combo_box.get()
    if not selected:
        messagebox.showerror("Error", "No entry selected.")
        return

    original_data = selected.split(', ')
    rows = []
    with open(file_path, 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if row != original_data:
                rows.append(row)

    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)

    messagebox.showinfo("Success", "Entry deleted successfully.")
    load_data()
    clear_entries()

def Add():
    """Handle the Add action from the GUI."""
    ip = ip_entry.get()
    mac = mac_entry.get()
    name = name_entry.get()
    if save_data(ip, mac, name):
        clear_entries()

def clear_entries():
    """Clear input fields."""
    ip_entry.delete(0, tk.END)
    mac_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    combo_box.set('')

def load_data():
    """Load data from the file to the dropdown menu."""
    try:
        with open(file_path, 'r', newline='') as file:
            reader = csv.reader(file)
            data_list = ['{}, {}, {}'.format(*row) for row in reader]
            combo_box['values'] = data_list
    except FileNotFoundError:
        combo_box['values'] = []

def on_select(event):
    """Load selected data into the entry fields for editing."""
    selected = combo_box.get()
    if selected:
        ip, mac, name = selected.split(', ')
        ip_entry.delete(0, tk.END)
        ip_entry.insert(0, ip)
        mac_entry.delete(0, tk.END)
        mac_entry.insert(0, mac)
        name_entry.delete(0, tk.END)
        name_entry.insert(0, name)

def edit_data():
    """Edit the selected entry with new data from the entry fields."""
    selected = combo_box.get()
    if selected:
        original_data = selected
        new_ip = ip_entry.get()
        new_mac = mac_entry.get()
        new_name = name_entry.get()
        if save_data(new_ip, new_mac, new_name, edit=True, original_data=original_data):
            clear_entries()

            # After editing, clear the selection
            combo_box.set('')
            combo_box.selection_clear()

# Set up the GUI
root = tk.Tk()
root.title("Network Data Maintenance")
root.geometry('1000x500+480+300')
root.configure(bg='white')  # Set background color

tk.Label(root, text="IP Address:", font=("Arial", 24), bg='white').place(x=25, y=50)
ip_entry = tk.Entry(root, font=("Arial", 24))
ip_entry.place(x=300, y=50, width=300 )

tk.Label(root, text="MAC Address:", font=("Arial", 24), bg='white').place(x=25, y=100)
mac_entry = tk.Entry(root, font=("Arial", 24))
mac_entry.place(x=300, y=100, width=300)

tk.Label(root, text="Computer Name:", font=("Arial", 24), bg='white').place(x=25, y=150)
name_entry = tk.Entry(root, font=("Arial", 24))
name_entry.place(x=300, y=150, width=300)

Add_btn = tk.Button(root, text="Add", font=("Arial", 24), width=8, height=2, command=Add)
Add_btn.place(x=100, y=235)
#Add_btn.config(height=2, width=10)
Tooltip(Add_btn, "To add a new network device, fill out the form above completely. When you are finished, please press add!")

edit_btn = tk.Button(root, text="Update", font=("Arial", 24), width=8, height=2, command=edit_data)
edit_btn.place(x=300, y=235)
#edit_btn.config(height=2, width=10)
Tooltip(edit_btn, "To update information for a network device, please select it from the drop down menu below. Once you find it, change the information desired in the form above. When you are done updating, please press the Edit button")

delete_btn = tk.Button(root, text="Delete", font=("Arial", 24), width=8, height=2, command=delete_data)
delete_btn.place(x=500, y=235)
Tooltip(delete_btn, "To delete information for a network device, please select it from the drop down menu below. Once you find it, please press the Delete button")

close_btn = tk.Button(root, text="Close", font=("Arial", 24), width=8, height=2, command=root.destroy)
close_btn.place(x=700, y=235)
Tooltip(close_btn, "Utilize this button to close the application and return to the main menu")

tk.Label(root, text="Select entry to update/delete:", font=("Arial", 24), bg='white').place(x=25, y=350)
combo_box = ttk.Combobox(root, font=("Arial", 28), width=45)
combo_box.place(x=10, y=400)
combo_box.bind("<<ComboboxSelected>>", on_select)
combo_box.option_add("*TCombobox*Listbox.font", "Arial 24")
load_data()

root.mainloop()
