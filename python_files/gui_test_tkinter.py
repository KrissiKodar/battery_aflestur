import tkinter as tk
import sys
import serial
from serial.tools import list_ports
from serial import Serial
import pandas as pd
import numpy as np
from tkinter_settings import engine, my_db, connection
from tkinter_util_func import gui_to_read_battery
from tkinter import ttk

from sqlalchemy import text



global scanned_input
scanned_input = None

def set_window_icon(window):
    window.iconbitmap('ossur_logo.ico')

def incoming_clicked():
    exit_button.pack_forget()
    incoming_button.pack_forget()
    service_button.pack_forget()
    back_button.pack(side="left", padx=10, pady=5)
    back_button.config(state="normal")
    incoming_label.pack(side="top")
    scan_battery_button.pack(side="left", padx=10, pady=5)
    read_battery_button.pack(side="left", padx=10, pady=5)
    #print("Clicked button:", incoming_button["text"])

def service_clicked():
    exit_button.pack_forget()
    incoming_button.pack_forget()
    service_button.pack_forget()
    back_button.pack(side="left", padx=10, pady=5)
    back_button.config(state="normal")
    service_label.pack(side="top")
    scan_battery_button.pack(side="left", padx=10, pady=5)
    read_battery_button.pack(side="left", padx=10, pady=5)
    #print("Clicked button:", service_button["text"])

def back_clicked():
    incoming_label.pack_forget()
    service_label.pack_forget()
    back_button.pack_forget()
    exit_button.pack(side="left")
    incoming_button.pack(side="left", padx=10, pady=5)
    service_button.pack(side="left", padx=10, pady=5)
    scan_battery_button.pack_forget()
    read_battery_button.pack_forget()
    back_button.config(state="disabled")

def scan_battery_clicked():
    def on_scan_entry(event):
        scanned_data = scan_entry.get()
        print("Scanned data:", scanned_data)
        # if scanned data contains two words with a space in between, only use the second word
        if len(scanned_data.split()) > 1:
            scanned_data = scanned_data.split()[1]
        print("Scanned data:", scanned_data)
        # Store the scanned_data in a global variable for later use
        global scanned_input
        scanned_input = scanned_data
        # Re-enable the scan_battery_button after scanning
        scan_battery_button.config(state="normal")
        # Close the scan_top window after scanning
        scan_top.destroy()

    def on_scan_top_close():
        # Re-enable the scan_battery_button when the window is closed
        scan_battery_button.config(state="normal")
        scan_top.destroy()

    # Disable the scan_battery_button while scanning
    scan_battery_button.config(state="disabled")

    scan_top = tk.Toplevel(root)
    scan_top.title("Scan Battery")
    scan_top.geometry("300x100")
    set_window_icon(scan_top)

    # Bind the custom close function to the Toplevel window
    scan_top.protocol("WM_DELETE_WINDOW", on_scan_top_close)

    scan_label = tk.Label(scan_top, text="Please scan with the scanner:")
    scan_label.pack(padx=10, pady=5)

    scan_entry = tk.Entry(scan_top)
    scan_entry.pack(padx=10, pady=5)
    scan_entry.focus_set()

    # Bind the 'Return' key to the on_scan_entry function
    scan_entry.bind("<Return>", on_scan_entry)

def read_battery_clicked():
    global scanned_input
    if scanned_input != None:
        read_success = gui_to_read_battery(scanned_input)
        scanned_input = None
        if read_success:
            print("Battery read successfully")
        else:
            print("Battery read failed")
    else:
        print("No battery scanned")



def redirect_stdout():
    sys.stdout = StdoutRedirector(text)
    

class StdoutRedirector():
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, string):
        self.text_widget.insert("end", string)
        self.text_widget.see("end")

    def flush(self):
        pass

# Create the main window
root = tk.Tk()
root.title("Össur battery reader")
root.geometry("1000x600")
root.resizable(True, True)

set_window_icon(root)

# Create the frame for the buttons and labels
frame = tk.Frame(root)
frame.pack(side="bottom")

# Create the buttons
incoming_button = tk.Button(frame, text="Incoming", command=incoming_clicked, padx=10, pady=5)
service_button = tk.Button(frame, text="Service", command=service_clicked, padx=10, pady=5)
back_button = tk.Button(frame, text="Back", command=back_clicked, state="disabled", padx=10, pady=5)
exit_button = tk.Button(frame, text="Exit", command=root.destroy, padx=10, pady=5)
# Create the labels
incoming_label = tk.Label(root, text="Incoming screen")
service_label = tk.Label(root, text="Service screen")

# Create the buttons for battery scan and read
scan_battery_button = tk.Button(frame, text="Scan battery", command=scan_battery_clicked, padx=10, pady=5)
read_battery_button = tk.Button(frame, text="Read battery", command=read_battery_clicked, padx=10, pady=5)

# Create the text widget
text = tk.Text(root, wrap="word")
text.pack(side="bottom", fill="both", expand=True)

# Redirect stdout to the text widget
redirect_stdout()

# Add the buttons and labels to the frame
exit_button.pack(side="left", padx=10, pady=5)
incoming_button.pack(side="left", padx=10, pady=5)
service_button.pack(side="left", padx=10, pady=5)


# Start the GUI
root.mainloop()
