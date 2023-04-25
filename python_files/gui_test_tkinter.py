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

def get_table_names():
    query = f"SELECT table_name FROM information_schema.tables WHERE table_type = 'BASE TABLE' AND table_catalog = '{my_db}';"
    table_names = pd.read_sql_query(query, connection)
    return table_names['table_name'].tolist()


def show_all_clicked():
    def on_table_select(event):
        selected_table = table_listbox.get(table_listbox.curselection())
        query = f"SELECT * FROM {selected_table}"
        battery_data = pd.read_sql_query(query, connection)

        # Clear the treeview before inserting new data
        for item in tree.get_children():
            tree.delete(item)

        # Update the column headings and insert the data into the Treeview
        tree["columns"] = list(battery_data.columns)
        for col in battery_data.columns:
            tree.heading(col, text=col)

        for index, row in battery_data.iterrows():
            tree.insert("", "end", values=row.tolist())

    table_names = get_table_names()

    # Create a new Toplevel window to display the data
    show_all_top = tk.Toplevel(root)
    show_all_top.title("All Batteries")
    show_all_top.geometry("1200x800")
    set_window_icon(show_all_top)

    # Create a Listbox for table selection
    table_listbox = tk.Listbox(show_all_top, selectmode="browse")
    table_listbox.pack(side="left", padx=10, pady=5, fill="y")
    

    for table in table_names:
        table_listbox.insert("end", table)

    table_listbox.bind("<<ListboxSelect>>", on_table_select)

    # Create a frame to hold the Treeview and its scrollbars
    tree_frame = tk.Frame(show_all_top)
    tree_frame.pack(side="right", fill="both", expand=True)

    # Add horizontal and vertical scrollbars
    h_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal")
    h_scrollbar.pack(side="bottom", fill="x")
    v_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical")
    v_scrollbar.pack(side="right", fill="y")

    # Create a Treeview to display the data
    tree = ttk.Treeview(tree_frame, show="headings", xscrollcommand=h_scrollbar.set, yscrollcommand=v_scrollbar.set)
    tree.pack(side="left", fill="both", expand=True)

    # Configure the scrollbars to work with the Treeview widget
    v_scrollbar.config(command=tree.yview)
    h_scrollbar.config(command=tree.xview)

def compare_two_tables(table1, table2):
    # if streing before first underscore is the same, then it is the same battery 
    # if not then return None
    if table1.split("_")[0] != table2.split("_")[0]:
        return None

    table1_data = pd.read_sql_query(f"SELECT * FROM {table1}", connection)
    # table2_data will contain the golden files later
    table2_data = pd.read_sql_query(f"SELECT * FROM {table2}", connection)

    if table1_data.shape[1] != table2_data.shape[1]:
        return None

    diff = table1_data["MEASURED VALUE"] != table2_data["MEASURED VALUE"]
    if "SUBCLASS" in table1_data.columns:
        # Select the desired columns and create separate columns for the "MEASURED VALUE" from each table
        diff_df = table1_data.loc[diff, ["CLASS", "SUBCLASS", "NAME", "MEASURED VALUE"]]
        diff_df["MEASURED VALUE (Table 2)"] = table2_data.loc[diff, "MEASURED VALUE"]
        # add "UNIT" column
        diff_df["UNIT"] = table1_data.loc[diff, "UNIT"]
    else:
        diff_df = table1_data.loc[diff, ["SBS CMD", "NAME", "MEASURED VALUE"]]
        diff_df["MEASURED VALUE (Table 2)"] = table2_data.loc[diff, "MEASURED VALUE"]
        # add "UNIT" column
        diff_df["UNIT"] = table1_data.loc[diff, "UNIT"]
    return diff_df


def compare_tables_clicked():
    def on_compare_button_click():
        if not table1_listbox.curselection() or not table2_listbox.curselection():
                error_message = "Please select a table from both listboxes before comparing."
                print(error_message)
                error_label.config(text=error_message)
                return

        table1 = table1_listbox.get(table1_listbox.curselection())
        table2 = table2_listbox.get(table2_listbox.curselection())

        diff_df = compare_two_tables(table1, table2)

        if diff_df is None:
            error_message = f"Cannot compare {table1} and {table2} as they have a different number of columns."
            print(error_message)
            error_label.config(text=error_message)
            return
        
       # Create a new Toplevel window to display the differences
        diff_top = tk.Toplevel(compare_top)
        diff_top.title(f"Differences between {table1} and {table2}")
        diff_top.geometry("1200x800")
        set_window_icon(diff_top)

        # Create a frame to hold the Treeview and its scrollbars
        tree_frame = tk.Frame(diff_top)
        tree_frame.pack(fill="both", expand=True)

        # Add horizontal and vertical scrollbars
        h_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal")
        h_scrollbar.pack(side="bottom", fill="x")
        v_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical")
        v_scrollbar.pack(side="right", fill="y")

        # Create a Treeview to display the data
        tree = ttk.Treeview(tree_frame, show="headings", xscrollcommand=h_scrollbar.set, yscrollcommand=v_scrollbar.set)
        tree.pack(side="left", fill="both", expand=True)

        # Configure the scrollbars to work with the Treeview widget
        v_scrollbar.config(command=tree.yview)
        h_scrollbar.config(command=tree.xview)

        # Update the column headings and insert the data into the Treeview
        tree["columns"] = list(diff_df.columns)
        for col in diff_df.columns:
            tree.heading(col, text=col)

        for index, row in diff_df.iterrows():
            tree.insert("", "end", values=row.tolist())

    compare_top = tk.Toplevel(root)
    compare_top.title("Compare Tables")
    compare_top.geometry("500x300")
    set_window_icon(compare_top)

    table_names = get_table_names()

    # Configure the columns and rows to resize with the window
    compare_top.grid_columnconfigure(0, weight=1)
    compare_top.grid_columnconfigure(1, weight=1)
    compare_top.grid_rowconfigure(0, weight=1)

    # Create two Listboxes for table selection
    table1_listbox = tk.Listbox(compare_top, selectmode="browse", exportselection=False)
    table1_listbox.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")

    table2_listbox = tk.Listbox(compare_top, selectmode="browse", exportselection=False)
    table2_listbox.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")


    for table in table_names:
        table1_listbox.insert("end", table)
        table2_listbox.insert("end", table)
    error_label = tk.Label(compare_top, text="", fg="red")
    error_label.grid(row=2, column=0, columnspan=2, pady=5)

    compare_button = tk.Button(compare_top, text="Compare", command=on_compare_button_click)
    compare_button.grid(row=1, column=0, columnspan=2, pady=10)


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
show_all_button = tk.Button(frame, text="Show all", command=show_all_clicked, padx=10, pady=5)
show_all_button.pack(side="left", padx=10, pady=5)
compare_button = tk.Button(frame, text="Compare", command=compare_tables_clicked, padx=10, pady=5)
compare_button.pack(side="left", padx=10, pady=5)


# Start the GUI
root.mainloop()
