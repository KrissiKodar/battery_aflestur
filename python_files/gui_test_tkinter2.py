import tkinter as tk
import sys
from tkinter_util_func import gui_to_read_battery
import time

from sqlalchemy import text

class StdoutRedirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, string):
        self.text_widget.insert("end", string)
        self.text_widget.see("end")
        self.text_widget.update_idletasks()  # Force the Tkinter event loop to update the display immediately

    def flush(self):
        pass


class BatteryReaderApp(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Össur battery reader")
        self.master.geometry("800x600")
        self.master.resizable(True, True)
        self.set_window_icon(self.master)

        # Initialize the radio button variables
        self.status_var = tk.StringVar(value="")
        self.product_type_var = tk.StringVar(value="")
        self.selected_status = ""
        self.selected_product_type = ""
        self.scanned_input = None
        self.all_product_types =['Powerknee', 'Rheo', 'Navi']
        self.line_len = 65

        self.create_widgets()
        # Redirect standard output to the text widget
        sys.stdout = StdoutRedirector(self.text)
        self.instructions()

        
    def instructions(self):
        print("-"*self.line_len)
        print("1. Select Incoming or Service\n")
        print("2. Select Product", end=" ")
        for product_type in self.all_product_types:
             # if not last item in list
             if product_type != self.all_product_types[-1]:
                print("{}".format(product_type), end=", ")
             else:
                print("or {}".format(product_type), end=" ")
        print("\n")
        print("3. Then press the scan button and scan the battery QR code\n")
        print("4. After that press the read button to read the battery\n")
        print("5. Wait until the read operation is finished\n")
        print("-"*self.line_len)
        
    def set_window_icon(self, window):
        window.iconbitmap('ossur_logo.ico')

    def clear_text_widget(self, text_widget):
        text_widget.delete("1.0", tk.END)

    def create_widgets(self):
        # Create the frame for the status radio buttons
        status_frame = tk.LabelFrame(self.master, text="Status")
        status_frame.pack(side="left", padx=10, pady=10)

        # Create the status radio buttons
        incoming_radio = tk.Radiobutton(status_frame, text="Incoming", variable=self.status_var, value="Incoming", command=self.check_buttons)
        incoming_radio.pack(padx=10, pady=5)
        service_radio = tk.Radiobutton(status_frame, text="Service", variable=self.status_var, value="Service", command=self.check_buttons)
        service_radio.pack(padx=10, pady=5)

        # Create the frame for the product type radio buttons
        product_frame = tk.LabelFrame(self.master, text="Product Type")
        product_frame.pack(side="right", padx=10, pady=10)

        # Create the product type radio buttons
        """ product_a_radio = tk.Radiobutton(product_frame, text="Product A", variable=self.product_type_var, value="Product A", command=self.check_buttons)
        product_a_radio.pack(padx=10, pady=5)
        product_b_radio = tk.Radiobutton(product_frame, text="Product B", variable=self.product_type_var, value="Product B", command=self.check_buttons)
        product_b_radio.pack(padx=10, pady=5)
        product_c_radio = tk.Radiobutton(product_frame, text="Product C", variable=self.product_type_var, value="Product C", command=self.check_buttons)
        product_c_radio.pack(padx=10, pady=5) """

        # Create the product type radio buttons from self.all_product_types 
        for product_type in self.all_product_types:
            product_radio = tk.Radiobutton(product_frame, text="{}".format(product_type), variable=self.product_type_var, value="{}".format(product_type), command=self.check_buttons)
            product_radio.pack(padx=10, pady=5)

        # Create the scan button (initially greyed out)
        self.scan_button = tk.Button(self.master, text="Scan", state="disabled", padx=10, pady=5, command=self.on_scan)
        self.scan_button.pack(side="bottom", pady=10)

        # Create the read battery button (initially greyed out)
        self.read_battery_button = tk.Button(self.master, text="Read Battery", state="disabled", padx=10, pady=5, command=self.on_read_battery)
        self.read_battery_button.pack(side="bottom", pady=10)

        # Create the text widget
        self.text = tk.Text(self.master, wrap="word")
        self.text.pack(side="bottom", fill="both", expand=True)
        
    def check_buttons(self):
        """Enable the scan button when both radio buttons are selected."""
        status = self.status_var.get()
        product_type = self.product_type_var.get()
        if status and product_type:
            self.scan_button.config(state="normal")
            self.selected_status = status
            self.selected_product_type = product_type

    def scan_battery_clicked(self):
        def on_scan_entry(event):
            scanned_data = scan_entry.get()
            print("-"*self.line_len)
            print(f"QR code: {scanned_data}")
            print("-"*self.line_len, end = "\n")
            # if scanned data contains two words with a space in between, only use the second word
            if len(scanned_data.split()) > 1:
                scanned_data = scanned_data.split()[1]
            self.scanned_input = scanned_data
            # Re-enable the scan_battery_button after scanning
            self.scan_button.config(state="normal")
            # Close the scan_top window after scanning
            scan_top.destroy()

        def on_scan_top_close():
            # Re-enable the scan_battery_button when the window is closed
            self.scan_button.config(state="normal")
            scan_top.destroy()

        # Disable the scan_battery_button while scanning
        self.scan_button.config(state="disabled")

        scan_top = tk.Toplevel(self.master)
        scan_top.title("Scan Battery")
        scan_top.geometry("300x100")
        #set_window_icon(scan_top)

        # Bind the custom close function to the Toplevel window
        scan_top.protocol("WM_DELETE_WINDOW", on_scan_top_close)

        scan_label = tk.Label(scan_top, text="Please scan with the scanner:")
        scan_label.pack(padx=10, pady=5)

        scan_entry = tk.Entry(scan_top)
        scan_entry.pack(padx=10, pady=5)
        scan_entry.focus_set()

        # Bind the 'Return' key to the on_scan_entry function
        scan_entry.bind("<Return>", on_scan_entry)


    def on_scan(self):
        """Enable the read battery button when scan button is clicked."""
        self.clear_text_widget(self.text)
        self.instructions()
        self.read_battery_button.config(state="normal")
        self.scan_battery_clicked()

        

    def on_read_battery(self):
        """TODO: Implement the read battery functionality here."""
        #self.clear_text_widget(self.text)
        print("Reading battery.......\n")
        print("Selected status:      ", self.selected_status)
        print("Selected product type:", self.selected_product_type)
        print("QR code:              ", self.scanned_input)
        print("\n")
        read_success = gui_to_read_battery(self.scanned_input , self.selected_status, self.selected_product_type)
        scanned_input = None
        if read_success:
            print("Battery read successfully\n")
        else:
            print("Battery read failed\n")
        print("-"*self.line_len, end = '\n')
        

        # Disable the "Read Battery" button after it has been clicked
        self.read_battery_button.config(state="disabled")


def main():
    root = tk.Tk()
    app = BatteryReaderApp(master=root)
    app.mainloop()


if __name__ == "__main__":
    main()
