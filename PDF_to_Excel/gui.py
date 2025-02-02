import customtkinter as ctk
from tkinter import filedialog, messagebox, BOTH, LEFT, END
from logic import start_extraction
from phase1 import phase1_validation
from phase2 import phase2_update_with_reporting
import shutil
import os

class Application(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Metso PDF to Excel")
        self.geometry("800x600")

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        # Initialize the variable to store the Excel file path
        self.excel_file = None

        # Left side of the GUI
        left_frame = ctk.CTkFrame(self)
        left_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)

        # Add the "info" button inside the left_frame
        info_button = ctk.CTkButton(left_frame, text="i", width=20, height=20, command=self.show_contact_info, fg_color="#fc9d30", text_color="#FFFFFF", hover_color="#ff8903")
        info_button.pack(anchor="nw", pady=5, padx=5)

        self.pdf_files_label = ctk.CTkLabel(left_frame, text="No PDF Files Selected")
        self.pdf_files_label.pack()

        select_pdf_button = ctk.CTkButton(left_frame, text="Select PDF Files", command=self.select_pdf_files)
        select_pdf_button.pack(pady=5)

        self.excel_file_label = ctk.CTkLabel(left_frame, text="No Excel File Selected")
        self.excel_file_label.pack()

        select_excel_button = ctk.CTkButton(left_frame, text="Select Excel File", command=self.select_excel_file)
        select_excel_button.pack(pady=5)



        self.extract_button = ctk.CTkButton(left_frame, text="Extract", command=self.extract_data, fg_color="#d3d3d3", text_color="#a9a9a9", hover_color="#c0c0c0", state="disabled")
        self.extract_button.pack(pady=(50, 5))

        self.log_text = ctk.CTkTextbox(left_frame, height=200, state='disabled')
        self.log_text.pack(fill=BOTH, expand=True, pady=5)

        # Right side of the GUI
        right_frame = ctk.CTkFrame(self)
        right_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)

        self.validate_button = ctk.CTkButton(right_frame, text="Validate shipment", command=self.validate_shipment, fg_color="#d3d3d3", text_color="#a9a9a9", hover_color="#c0c0c0", state="disabled")
        self.validate_button.pack(pady=(20, 5))

        self.validation_text = ctk.CTkTextbox(right_frame, height=100, state='normal')
        self.validation_text.pack(fill=BOTH, expand=True, pady=5)
        self.validation_text.configure(state='disabled')

        self.update_button = ctk.CTkButton(right_frame, text="Update the order ledger", command=self.update_order_ledger, fg_color="#d3d3d3", text_color="#a9a9a9", hover_color="#c0c0c0", state="disabled")
        self.update_button.pack(pady=(20, 5))

        self.update_text = ctk.CTkTextbox(right_frame, height=100, state='normal')
        self.update_text.pack(fill=BOTH, expand=True, pady=5)
        self.update_text.configure(state='disabled')

    def show_contact_info(self):
        contact_info = (
            "For support, please contact:\n"
            "Email: "
        )
        messagebox.showinfo("Contact Information", contact_info)

    def select_pdf_files(self):
        self.pdf_files = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
        self.pdf_files_label.configure(text=f"{len(self.pdf_files)} PDF Files Selected")

    def select_excel_file(self):
        self.excel_file = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        self.excel_file_label.configure(text="Excel File Selected")
        self.update_button_states()

    def update_button_states(self):
        if self.excel_file:
            self.extract_button.configure(state="normal", fg_color="#28B463", text_color="#FFFFFF", hover_color="#1E8449")
            self.validate_button.configure(state="normal", fg_color="#1f538d", text_color="#FFFFFF", hover_color="#14375e")
            self.update_button.configure(state="normal", fg_color="#1f538d", text_color="#FFFFFF", hover_color="#14375e")
        else:
            self.extract_button.configure(state="disabled", fg_color="#d3d3d3", text_color="#a9a9a9", hover_color="#c0c0c0")
            self.validate_button.configure(state="disabled", fg_color="#d3d3d3", text_color="#a9a9a9", hover_color="#c0c0c0")
            self.update_button.configure(state="disabled", fg_color="#d3d3d3", text_color="#a9a9a9", hover_color="#c0c0c0")

    def backup_excel_file(self):
        if self.excel_file:
            backup_path = os.path.join(os.path.dirname(self.excel_file), "backup_" + os.path.basename(self.excel_file))
            shutil.copyfile(self.excel_file, backup_path)
            print(f"Backup created at {backup_path}")

    def extract_data(self):
        self.backup_excel_file()
        self.log_text.configure(state='normal')
        self.log_text.insert(END, "Extracting data...\n")
        self.log_text.configure(state='disabled')
        start_extraction(self.pdf_files, self.excel_file, self.log_text)

    def validate_shipment(self):
        self.backup_excel_file()
        try:
            self.validation_text.configure(state='normal')
            self.validation_text.delete(1.0, END)
            phase1_validation(self.excel_file, self.validation_text)
        except Exception as e:
            self.validation_text.configure(state='normal')
            self.validation_text.insert(END, f"Validation error: {str(e)}\n")
            self.validation_text.configure(state='disabled')

    def update_order_ledger(self):
        self.backup_excel_file()
        try:
            self.update_text.configure(state='normal')
            self.update_text.delete(1.0, END)
            
            # Get the new formatted message
            message_parts, message_tags = phase2_update_with_reporting(self.excel_file)
            
            # Insert the message into the update_text widget with tags
            for part, tag in zip(message_parts, message_tags):
                if tag:
                    self.update_text.insert(END, part, tag)
                else:
                    self.update_text.insert(END, part)
            
            # Configure the tags for coloring
            self.update_text.tag_config("full_rows", foreground="#99fc77")
            self.update_text.tag_config("partial_rows", foreground="#fcd465")
            
            self.update_text.configure(state='disabled')
        except Exception as e:
            self.update_text.configure(state='normal')
            self.update_text.insert(END, f"Order ledger update error: {str(e)}\n")
            self.update_text.configure(state='disabled')
      

if __name__ == "__main__":
    app = Application()
    app.mainloop()
