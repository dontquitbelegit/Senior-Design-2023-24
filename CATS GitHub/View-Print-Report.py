#View-Print-Report.py
import tkinter as tk
from tkinter import ttk
import subprocess
import csv
import os
from subprocess import Popen, PIPE

def open_with_libreoffice(file_path):
    file_path = os.path.join('/home/kali/Documents', file_path)
    subprocess.run(["libreoffice", "--writer", file_path], check=True)


def print_document(file_path):
    
    document_path = os.path.join('/home/kali/Documents', file_path)
    printer_name = "HP_ENVY_6000_series"  # Use the exact printer name; update if necessary
    
    # Command to print the document using LibreOffice in headless mode
    command = f"libreoffice --headless --pt {printer_name} \"{document_path}\""
    # Execute the command
    process = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    
    # Command to send a form feed to the printer
    form_feed_command = f"echo -e '\\f' | lp -d {printer_name}"
    
    # Execute the command
    os.system(form_feed_command)

def execute_find_command(filter_parameter):
    #command = f"sudo find /home/kali/Documents -type f -name '*{filter_parameter}*.odt' ! -name 'FTP_Template.odt' ! -name 'Vulnerability_Template.odt' ! -name 'Discovery_Template.odt' -exec basename {{}} \; | sort > /home/kali/CATS/reports.csv"
    command = f"sudo find /home/kali/Documents -type f -name '*{filter_parameter}*.odt' ! -name '*_Template.odt' -exec basename {{}} \; | sort > /home/kali/CATS/reports.csv"
    subprocess.run(command, check=True, shell=True)

def read_filtered_file_names():
    try:
        with open("/home/kali/CATS/reports.csv", newline='') as csvfile:
            filereader = csv.reader(csvfile)
            return [row[0] for row in filereader if row]
    except FileNotFoundError:
        return []

def read_categories(csv_file_path):
    with open(csv_file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        return [row[0] for row in reader]

def create_file_selection_gui(filter_parameter):
    execute_find_command(filter_parameter)
    file_names = read_filtered_file_names()
    
    # Add the default dropdown prompt to the list
    file_names.insert(0, "Select desired report file from this drop down menu")

    root = tk.Tk()
    root.title("")
    root.geometry('1050x200')
    root.configure(background='white')
    root.option_add("*TCombobox*Listbox.font", "Arial 24")

    style = ttk.Style()
    style.theme_use('default')
    style.configure('Thick.TCombobox', font=('Arial', 24), arrowsize=30, padding="5 5 5 5")
    style.configure('TButton', font=('Arial', 24), foreground='black', background='white')

    selected_file = tk.StringVar(value=file_names[0])
    dropdown = ttk.Combobox(root, textvariable=selected_file, width=42, font=('Arial', 24), style='Thick.TCombobox', values=file_names)
    dropdown.grid(column=0, row=0, padx=10, pady=10)

    open_button = ttk.Button(root, text="Open", style='TButton', command=lambda: open_with_libreoffice(selected_file.get()) if selected_file.get() != file_names[0] else None)
    open_button.grid(column=2, row=0, padx=10, pady=10)

    print_double_sided_button = ttk.Button(root, text="Print", style='TButton', command=lambda: print_document(selected_file.get()) if selected_file.get() != file_names[0] else None)
    print_double_sided_button.grid(column=2, row=1, padx=10, pady=10)

    close_button = ttk.Button(root, text="Close", style='TButton', command=lambda: root.destroy())
    close_button.grid(column=2, row=2, padx=10, pady=10)

    root.mainloop()
    
def create_category_selection_gui(csv_file_path_categories):
    root = tk.Tk()
    root.title("")
    root.geometry('1100x150')
    root.configure(background='white')
    root.option_add("*TCombobox*Listbox.font", "Arial 24")

    style = ttk.Style()
    style.theme_use('default')
    style.configure('Thick.TCombobox', font=('Arial', 24), arrowsize=30, padding="5 5 5 5")
    style.configure('TButton', font=('Arial', 24), foreground='black', background='white')

    categories = read_categories(csv_file_path_categories)
    categories.insert(0, "Select the report category from this drop down menu")
    filter_parameter_var = tk.StringVar(value=categories[0])
    filter_parameter_dropdown = ttk.Combobox(root, textvariable=filter_parameter_var, width=42, font=('Arial', 24), style='Thick.TCombobox', values=categories)
    filter_parameter_dropdown.grid(row=0, column=0, padx=10)
    
    def on_select_category():
        selected_category = filter_parameter_var.get()
        if selected_category != categories[0]:
            root.destroy()
            create_file_selection_gui(selected_category)

    select_category_button = ttk.Button(root, text="Select Category", style='TButton', command=on_select_category)
    select_category_button.grid(row=0, column=2, pady=20, padx=10)

    root.mainloop()
 
csv_file_path_categories = "/home/kali/CATS/categories.csv"
create_category_selection_gui(csv_file_path_categories)
