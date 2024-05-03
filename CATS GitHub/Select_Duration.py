import tkinter as tk
from tkinter import ttk, messagebox
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
        label = tk.Label(self.tooltip, text=self.text, background="lightblue", font=("Arial", 32), wraplength=500, relief="solid", borderwidth=3, padx=10)
        label.pack()

    def leave(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()

def save_choice(event):
    """Extract the numeric value from the selected scan duration and write it to a text file."""
    choice = combo_box.get()
    numeric_value = choice.split()[0]  # Get the first part (number) of the selected duration
    with open('scan_duration.txt', 'w') as file:
        file.write(numeric_value)

# Set up the GUI
root = tk.Tk()
root.title("")
root.geometry('1200x220')
root.configure(bg='white')


style = ttk.Style(root)
# Configure the Combobox style for both the box and the dropdown
style.configure('LargeArrow.TCombobox', arrowsize=30, font=('Arial', 36))  # Adjust the arrow size and set the font for the combobox
style.configure('TCombobox', font=('Arial', 36))  # This ensures the dropdown items have the same font size

scan_durations = ['1 hour', '6 hours', '12 hours', '24 hours', '36 hours', '48 hours']

combo_box = ttk.Combobox(root, values=scan_durations, style='LargeArrow.TCombobox', font=("Arial", 32), width=30)
combo_box.set('Select Scan Duration')  # Set default item as the current value
combo_box.bind("<<ComboboxSelected>>", save_choice)
combo_box.place(x=50, y=80)
root.option_add('*TCombobox*Listbox.font', ("Arial", 32))  # Set font size for the dropdown list items

select_btn = tk.Button(root, text="Confirm/Save", font=("Arial", 32), width=12, height=1, command=root.destroy)
#button = tk.Button(root, text="This is a very long text that needs to be wrapped inside the button",
#                   wraplength=100,  # Wrap text at every 100 pixels
#                   justify='left')  # Justify text to the left
Tooltip(select_btn, "Click here to confirm your selection and close the select screen")
select_btn.place(x=840, y=80)

root.mainloop()
