#CATSMenu5

import tkinter as tk
from tkinter import messagebox, Toplevel, PhotoImage, ttk
import subprocess
import threading
import time
import sys
import os

class CustomMessageBox(tk.Toplevel):
    def __init__(self, parent, title="Message", message="Your message here", width=500, height=300, font=("Arial", 24), wraplength=400, background='white'):
        super().__init__(parent)
        self.geometry(f"{width}x{height}")
        self.title(title)
        self.transient(parent)
        self.grab_set()
        self.configure(bg=background)

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x_coordinate = int((screen_width / 2) - (width / 2))
        y_coordinate = int((screen_height / 2) - (height / 2))
        self.geometry(f"+{x_coordinate}+{y_coordinate}")

        message_label = tk.Label(self, text=message, font=font, wraplength=wraplength, bg=background)
        message_label.pack(expand=True, padx=20, pady=20)

        ok_button = tk.Button(self, text="OK", command=self.destroy, font=("Arial", 24), bg=background)
        ok_button.pack(pady=20, padx=10, ipadx=20, ipady=10)

def show_splash_screen(duration, image_path):
    splash_root = tk.Tk()
    splash_root.attributes('-fullscreen', True)
    splash_root.title("Splash Screen")
    img = PhotoImage(file=image_path)
    screen_width = splash_root.winfo_screenwidth()
    screen_height = splash_root.winfo_screenheight()
    x_coordinate = int((screen_width / 2) - (img.width() / 2))
    y_coordinate = int((screen_height / 2) - (img.height() / 2))
    splash_root.geometry(f"{img.width()}x{img.height()}+{x_coordinate}+{y_coordinate}")
    canvas = tk.Canvas(splash_root, height=img.height(), width=img.width(), bd=0, highlightthickness=10)
    canvas.pack()
    canvas.create_image(0, 0, anchor=tk.NW, image=img)
    splash_root.after(duration, splash_root.destroy)
    splash_root.overrideredirect(True)
    splash_root.mainloop()

def progress_bar_window():
    bar = tk.Toplevel()
    bar.title("Working...")
    bar.geometry('800x150')
    bar.configure(background='white')

    bar_title_label = tk.Label(bar, text="Please Be Patient. I Am Working On Your Request", bg='white', font=("Arial", 24))
    bar_title_label.pack(pady=10)

    elapsed_time_label = tk.Label(bar, text="Elapsed Time: 0 seconds", bg='white', font=("Arial", 24))
    elapsed_time_label.pack()

    style = ttk.Style()
    style.configure('TProgressbar', troughcolor='lightblue', thickness=20)

    progress_bar = ttk.Progressbar(bar, mode='indeterminate', style='TProgressbar')
    progress_bar.pack(fill=tk.X, expand=True, padx=20)
    progress_bar.start(10)

    return bar, progress_bar, elapsed_time_label

class ToolTip(object):
    def __init__(self, widget, text='widget info'):
        self.widget = widget
        self.text = text
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0
        widget.bind("<Enter>", self.showtip)
        widget.bind("<Leave>", self.hidetip)

    def showtip(self, event=None):
        self.x = event.x + self.widget.winfo_rootx() + 20
        self.y = event.y + self.widget.winfo_rooty() + 20
        if self.tipwindow or not self.text:
            return
        self.tipwindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry("+%d+%d" % (self.x, self.y))
        label = tk.Label(tw, text=self.text, justify=tk.LEFT, background="light blue", relief=tk.SOLID, borderwidth=1,
                         font=("Arial", "24", "normal"), wraplength=500, padx=20, pady=20)
        label.pack(ipadx=1)

    def hidetip(self, event=None):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

def run_long_running_task(task_number, bar, progress_bar, elapsed_time_label, app, buttons, is_first_run):
    start_time = time.time()

    def update_elapsed_time():
        elapsed_time = int(time.time() - start_time)
        elapsed_time_label.config(text=f"Elapsed Time: {elapsed_time} seconds")
        bar.after(1000, update_elapsed_time)

    update_elapsed_time()

    if task_number == 1:
        
        command_line = 'soffice --accept="socket,host=localhost,port=2002;urp;" --norestore --nologo --nodefault' #Adjust to command line
        script_path = "./Discovery.sh"  # Adjust to script path
        python_path = "Discovery_Report_MakerV2.py"  # Adjust to python program path
        python_path2 = "MAC Lookup and Replacement.py"  # Adjust to python program path
        
        try:
            subprocess.run(command_line, check=True, shell=True, stdout=subprocess.PIPE)
            subprocess.run(script_path, check=True, shell=True) 
            subprocess.run([sys.executable, python_path], check=True)
            subprocess.run([sys.executable, python_path2], check=True)
            CustomMessageBox(app, "Success!", "We Have Successfully Conducted A Discovery Scan On Your Network.", 500, 300, ("Arial", 24), 400, background='yellow')
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            progress_bar.stop()
            bar.destroy()
            if is_first_run:
                # Re-enable all buttons after Task 1 completion on first run
                for btn in buttons.values():
                    app.after(0, lambda b=btn: b.config(state=tk.NORMAL))
            pass

    elif task_number == 2:
        
        command_line = 'soffice --accept="socket,host=localhost,port=2002;urp;" --norestore --nologo --nodefault' #Adjust to command line
        script_path = "./vulners.sh"  # Adjust to script path
        python_path1 = "Select_IP.py"  # Adjust to python program path
        python_path2 = "Vulnerability_Report_Maker.py"  # Adjust to python program path
        
        try:
            
            subprocess.run(command_line, check=True, shell=True, stdout=subprocess.PIPE)
            subprocess.run([sys.executable, python_path1], check=True)
            subprocess.run(script_path, check=True, shell=True) 
            subprocess.run([sys.executable, python_path2], check=True)
            CustomMessageBox(app, "Success!", "We Have Successfully Scanned Your Network For Vulnerabilities.", 500, 300, ("Arial", 24), 400, background='yellow')
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            progress_bar.stop()
            bar.destroy()
            pass
  
    elif task_number == 3:
        
        command_line = 'libreoffice --accept="socket,host=localhost,port=2002;urp;" --norestore --nologo --headless' #Adjust to command line
        script_path = "./RunFTP.sh"  # Adjust to script path
        python_path1 = "Select_IP.py"  # Adjust to python program path
        
        try:
            subprocess.run(command_line, check=True, shell=True, stdout=subprocess.PIPE)
            subprocess.run([sys.executable, python_path1], check=True)
            subprocess.run(script_path, check=True, shell=True)
            CustomMessageBox(app, "Success!", "We Have Successfully Scanned Your Network For The FTP Vulnerability.", 500, 300, ("Arial", 24), 400, background='lightgreen')
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            progress_bar.stop()
            bar.destroy()
            pass
        
    elif task_number == 4:
                
        command_line = 'soffice --accept="socket,host=localhost,port=2002;urp;" --norestore --nologo --nodefault' #Adjust to command line
        script_path = "./malwaretest.sh"  # Adjust to script path
        python_path1 = "Select_IP.py"  # Adjust to python program path
        python_path2 = "SMTP_Report.py"  # Adjust to python program path
        
        try:
            subprocess.run(command_line, check=True, shell=True, stdout=subprocess.PIPE)
            subprocess.run([sys.executable, python_path1], check=True)
            subprocess.run(script_path, check=True, shell=True) 
            subprocess.run([sys.executable, python_path2], check=True)
            CustomMessageBox(app, "Success!", "We Have Successfully Conducted An SMTP Malware Scan On Your Network.", 500, 300, ("Arial", 24), 400, background='yellow')
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            progress_bar.stop()
            bar.destroy()
            if is_first_run:
                # Re-enable all buttons after Task 1 completion on first run
                for btn in buttons.values():
                    app.after(0, lambda b=btn: b.config(state=tk.NORMAL))
            pass
                
    elif task_number == 5:

        command_line = 'soffice --accept="socket,host=localhost,port=2002;urp;" --norestore --nologo --nodefault' #Adjust to command line
        script_path = './RunNMAP.sh' # Adjust to script path
        python_path1 = "Select_IP.py"  # Adjust to python program path
        
        try:
            subprocess.run(command_line, check=True, shell=True, stdout=subprocess.PIPE)
            subprocess.run([sys.executable, python_path1], check=True)
            subprocess.run(script_path, check=True, shell=True)
            CustomMessageBox(app, "Success!", "We Have Successfully Scanned A Device On Your Network.", 500, 300, ("Arial", 24), 400, background='yellow')
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            progress_bar.stop()
            bar.destroy()
            if is_first_run:
                # Re-enable all buttons after Task 1 completion on first run
                for btn in buttons.values():
                    app.after(0, lambda b=btn: b.config(state=tk.NORMAL))
            pass
        
    elif task_number == 6:
        
        script_path = './Network_Traffic_Scan.sh' # Adjust to script path
        python_path1 = "Select_Duration.py"  # Adjust to python program path
        
        try:
            #subprocess.run(command_line, check=True, shell=True, stdout=subprocess.PIPE)
            subprocess.run([sys.executable, python_path1], check=True)
            subprocess.run(script_path, check=True, shell=True)
            CustomMessageBox(app, "Success!", "We Have Successfully Measured The Traffic On Your Network.", 500, 300, ("Arial", 24), 400, background='yellow')
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            progress_bar.stop()
            bar.destroy()
            if is_first_run:
                # Re-enable all buttons after Task 1 completion on first run
                for btn in buttons.values():
                    app.after(0, lambda b=btn: b.config(state=tk.NORMAL))
            pass
 
                       
    elif task_number == 7:
            
        command_line = 'sudo find /home/kali/Documents -type f -name "*.odt" ! -name "test.odt" -exec basename {} \; > /home/kali/CATS/reports.csv'
        python_path = "View-Print-Report.py"
            
        subprocess.run(command_line, check=True, shell=True)
        subprocess.run([sys.executable, python_path], check=True)
        CustomMessageBox(app, "Success!", "We have successfully reviewed your reports!", 500, 300, ("Arial", 24), 400, background='red')
        progress_bar.stop()
        bar.destroy()
        
    elif task_number == 8:
            
        python_path = "IP Maintenance.py"
            
        subprocess.run([sys.executable, python_path], check=True)
        CustomMessageBox(app, "Success!", "Add/Update/Delete Program Executed Successfully.", 500, 300, ("Arial", 24), 400, background='skyblue')
        progress_bar.stop()
        bar.destroy()
        pass
    
    elif task_number == 9:
            
        python_path = "MAC Lookup and Replacement.py"
       
        subprocess.run([sys.executable, python_path], check=True)
        CustomMessageBox(app, "Success!", "Add/Edit/Delete Program Executed Successfully.", 500, 300, ("Arial", 24), 400, background='orange')
        progress_bar.stop()
        bar.destroy()
            
    elif task_number == 10:
            
        subprocess.run("sudo shutdown now", check=True, shell=True) #exit program and shutdown the RasPad
           
    else:
        messagebox.showinfo("Success", f"Task {task_number} executed (simulated).")

def create_task_button(frame, text, command, tooltips, i):
    btn = tk.Button(frame, text=text, padx=20, pady=10, command=command, width=40, bg='white', font=("Arial", 24))
    btn.pack(pady=(10, 0))
    ToolTip(btn, text=tooltips[i-1])
    return btn

def setup_buttons(app, frame, button_texts, button_tooltips, buttons, is_first_run):
    for i, text in enumerate(button_texts, start=1):
        command = lambda i=i: run_task(i, app, buttons, is_first_run)
        btn = create_task_button(frame, text, command, button_tooltips, i)
        buttons[i] = btn
        #Disable all buttons except task 1 on first run
        if is_first_run and i != 1:
            btn.config(state=tk.DISABLED)

def main_app():
    app = tk.Tk()
    app.title("Cyber Automated Tool Suite")
    app.geometry("1910x1076")
    app.attributes('-fullscreen', True)

    first_run_file_path = "first_run_done.txt"
    is_first_run = not os.path.isfile(first_run_file_path)

    background_image = PhotoImage(file="/home/kali/CATS/Slide1 1910-1076.png")
    background_label = tk.Label(app, image=background_image, highlightthickness=10)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    title_label = tk.Label(app, text="Cyber Automated Tool Suite", font=("Arial", 36), padx=20, pady=10, bg='white')
    title_label.pack(pady=20)

    button_frame = tk.Frame(app, bg='black')
    button_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    button_texts = ["What devices are connected to my network?",
                    "Is my system vulnerable?",
                    "Are my files vulnerable when being transferred?",
                    "Is my email secure?",
                    "Tell me more about my devices",
                    "How busy is my network?",
                    "View/Print Reports",
                    "Add/Update/Delete My Network Devices",
                    "Refresh My Network Devices",
                    "Exit Program"]

    button_tooltips = ["This task locates devices attached to your network.",
                       "This task will search your system for vulnerabilities and generate a report",
                       "Searches to see if your files may be vulnerable during transfer",
                       "Conducts a scan for malware attacking your email",
                       "This choice will provide detailed information about a device located on your network",
                       "This task will monitor network traffic",
                       "This will allow you to view/print reports from any scan category",
                       "Use this task to add/update/delete any informatio about a network connected device",
                       "This task will refresh the information about devives connected to your network",
                       "Exit the program and shutdown the CATS device"]
    
    buttons = {}
    setup_buttons(app, button_frame, button_texts, button_tooltips, buttons, is_first_run)

    if is_first_run:
        CustomMessageBox(app, "", "CATS has determined that this is your first time running the system. Please run - What devices are connected to my network? - to initialize the system.", 700, 275, ("Arial", 24), 600, 'orange')
        with open(first_run_file_path, 'w') as file:
            file.write("First run completed.")

    app.mainloop()

def run_task(task_number, app, buttons, is_first_run):
    bar, progress_bar, elapsed_time_label = progress_bar_window()
    thread_stop_event = threading.Event()  # Create the stop event
    task_thread = threading.Thread(target=run_long_running_task, args=(task_number, bar, progress_bar, elapsed_time_label, app, buttons, is_first_run), daemon=True)
    task_thread.start()
 
if __name__ == "__main__":
    splash_image_path = "/home/kali/CATS/CATS Logo New 1910-1076.png"
    show_splash_screen(5000, splash_image_path)
    main_app()
   \
     
     