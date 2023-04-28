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

global status
status = None # status is either 'Incoming' or 'Service'

global product_type
product_type = None # product_type is either 'Powerknee' or 'Rheo' or 'Navi

def set_window_icon(window):
    window.iconbitmap('ossur_logo.ico')

def product_type_clicked(product):
    global product_type
    product_type = product
    print(f"Selected product_type: {product_type}")

    # Hide product type buttons
    product_Powerknee_button.pack_forget()
    product_Rheo_button.pack_forget()
    product_Navi_button.pack_forget()

    # Show scan_battery_button and read_battery_button
    scan_battery_button.pack(side="left", padx=10, pady=5)
    read_battery_button.pack(side="left", padx=10, pady=5)

    # Change the back button behavior to go back to product type selection
    back_button.config(command=lambda: back_clicked(to_main_screen=False))

def reset_product_type():
    global product_type
    product_type = None

def incoming_clicked():
    exit_button.pack_forget()
    incoming_button.pack_forget()
    service_button.pack_forget()
    back_button.pack(side="left", padx=10, pady=5)
    back_button.config(state="normal")
    incoming_label.pack(side="top")
    # Hide the scan_battery_button and read_battery_button
    scan_battery_button.pack_forget()
    read_battery_button.pack_forget()
    #print("Clicked button:", incoming_button["text"])
    global status
    status = 'Incoming'
    # Add product type buttons
    product_Powerknee_button.pack(side="left", padx=10, pady=5)
    product_Rheo_button.pack(side="left", padx=10, pady=5)
    product_Navi_button.pack(side="left", padx=10, pady=5)

def service_clicked():
    exit_button.pack_forget()
    incoming_button.pack_forget()
    service_button.pack_forget()
    back_button.pack(side="left", padx=10, pady=5)
    back_button.config(state="normal")
    service_label.pack(side="top")
    # Hide the scan_battery_button and read_battery_button
    scan_battery_button.pack_forget()
    read_battery_button.pack_forget()
    #print("Clicked button:", service_button["text"])
    global status
    status = 'Service'
    # Add product type buttons
    product_Powerknee_button.pack(side="left", padx=10, pady=5)
    product_Rheo_button.pack(side="left", padx=10, pady=5)
    product_Navi_button.pack(side="left", padx=10, pady=5)

def back_clicked(to_main_screen = True):
    incoming_label.pack_forget()
    service_label.pack_forget()
    back_button.pack_forget()
    exit_button.pack(side="left")

    # Hide scan_battery_button and read_battery_button
    scan_battery_button.pack_forget()
    read_battery_button.pack_forget()

    if to_main_screen:
        incoming_button.pack(side="left", padx=10, pady=5)
        service_button.pack(side="left", padx=10, pady=5)
        back_button.config(state="disabled")
        product_Powerknee_button.pack_forget()
        product_Rheo_button.pack_forget()
        product_Navi_button.pack_forget()
    else:
        back_button.pack(side="left", padx=10, pady=5)
        back_button.config(state="normal")

        # Add product type buttons
        product_Powerknee_button.pack(side="left", padx=10, pady=5)
        product_Rheo_button.pack(side="left", padx=10, pady=5)
        product_Navi_button.pack(side="left", padx=10, pady=5)
        reset_product_type()

    #back_button.config(state="disabled")

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
    global status
    if scanned_input != None:
        read_success = gui_to_read_battery(scanned_input, status)
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
back_button = tk.Button(frame, text="Back", command=lambda: back_clicked(to_main_screen=True), state="disabled", padx=10, pady=5)
exit_button = tk.Button(frame, text="Exit", command=root.destroy, padx=10, pady=5)
# Create the labels
incoming_label = tk.Label(root, text="Incoming screen")
service_label = tk.Label(root, text="Service screen")

# Create the buttons for battery scan and read
scan_battery_button = tk.Button(frame, text="Scan battery", command=scan_battery_clicked, padx=10, pady=5)
read_battery_button = tk.Button(frame, text="Read battery", command=read_battery_clicked, padx=10, pady=5)


# Add the buttons and labels to the frame
exit_button.pack(side="left", padx=10, pady=5)
incoming_button.pack(side="left", padx=10, pady=5)
service_button.pack(side="left", padx=10, pady=5)

product_Powerknee_button = tk.Button(frame, text="Powerknee", command=lambda: product_type_clicked('Powerknee'), padx=10, pady=5)
product_Rheo_button = tk.Button(frame, text="Rheo", command=lambda: product_type_clicked('Rheo'), padx=10, pady=5)
product_Navi_button = tk.Button(frame, text="Navi", command=lambda: product_type_clicked('Navi'), padx=10, pady=5)


# Create the text widget
text = tk.Text(root, wrap="word")
text.pack(side="bottom", fill="both", expand=True)

# Redirect stdout to the text widget
redirect_stdout()




# Start the GUI
root.mainloop()
