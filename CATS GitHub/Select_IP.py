import tkinter as tk
from tkinter import ttk, messagebox
import re
import csv
import os
import sys

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
file_path = '/home/kali/CATS/MyNetwork.csv'  # Make sure this path is correct

# Regular expression for validating an IP Address
ip_pattern = re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$')

def load_data():
    """Load data from the file to the dropdown menu and add a default item."""
    try:
        with open(file_path, 'r', newline='') as file:
            reader = csv.reader(file)
            #data_list = ['Select the dessired IP from this drop down menu']  # Add default item
            data_list = ['{}, {}, {}'.format(*row) for row in reader]
            combo_box['values'] = data_list
            combo_box.set('Select the desired IP from this drop down menu')  # Set default item as the current value
    except FileNotFoundError:
        messagebox.showerror("Error", "File not found.")
        
def on_select(event):
    """Load selected data into the entry fields for editing and set the IP as an environment variable."""
    selected = combo_box.get()
    if selected:
        ip, mac, name = selected.split(', ')
        ip_entry.delete(0, tk.END)
        ip_entry.insert(0, ip)
        mac_entry.delete(0, tk.END)
        mac_entry.insert(0, mac)
        name_entry.delete(0, tk.END)
        name_entry.insert(0, name)
        # Set the environment variable
        os.environ['SELECTED_IP'] = ip


def on_select(event):
    """Load selected data into the entry fields for editing and set the IP as an environment variable."""
    selected = combo_box.get()
    if selected:
        ip, mac, name = selected.split(', ')
        ip_entry.delete(0, tk.END)
        ip_entry.insert(0, ip)
        mac_entry.delete(0, tk.END)
        mac_entry.insert(0, mac)
        name_entry.delete(0, tk.END)
        name_entry.insert(0, name)
        
        # Write parameter to a file
        parameter = ip
        with open('/home/kali/CATS/selected_ip.txt', 'w') as f:
            f.write(parameter)

# Set up the GUI
root = tk.Tk()
root.title("IP Selection")
root.geometry('900x350')
root.configure(bg='white')

style = ttk.Style()
style.configure('LargeArrow.TCombobox', arrowsize=30)  # Adjust the arrow size by increasing padding

tk.Label(root, text="IP Address:", font=("Arial", 24), bg='white').place(x=25, y=50)
ip_entry = tk.Entry(root, font=("Arial", 24))
ip_entry.place(x=300, y=50, width=300)

tk.Label(root, text="MAC Address:", font=("Arial", 24), bg='white').place(x=25, y=100)
mac_entry = tk.Entry(root, font=("Arial", 24))
mac_entry.place(x=300, y=100, width=300)

tk.Label(root, text="Computer Name:", font=("Arial", 24), bg='white').place(x=25, y=150)
name_entry = tk.Entry(root, font=("Arial", 24))
name_entry.place(x=300, y=150, width=300)

combo_box = ttk.Combobox(root, style='LargeArrow.TCombobox', font=("Arial", 24), width=45)
combo_box.place(x=25, y=250)
combo_box.bind("<<ComboboxSelected>>", on_select)
root.option_add('*TCombobox*Listbox.font', ("Arial", 24))  # Set font size for the dropdown list items

select_btn = tk.Button(root, text="Select", font=("Arial", 24), width=8, height=2, command=root.destroy)
select_btn.place(x=660, y=75)
Tooltip(select_btn, "Click here to select this IP and close this part of the application")

load_data()  # Load the data into the dropdown when the application starts

root.mainloop()
