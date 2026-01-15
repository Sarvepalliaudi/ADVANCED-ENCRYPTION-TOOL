"""
GUI Interface for AES-256 Encryption Tool
User-friendly tkinter interface for file encryption and decryption
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import threading
from encryption_engine import EncryptionEngine


class EncryptionGUI:
    """GUI for encryption/decryption tool"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Encryption Tool - AES-256")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        self.input_file = tk.StringVar()
        self.output_file = tk.StringVar()
        self.password = tk.StringVar()
        self.password_confirm = tk.StringVar()
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title = ttk.Label(main_frame, text="AES-256 File Encryption Tool", 
                         font=('Arial', 14, 'bold'))
        title.pack(pady=10)
        
        # Input file section
        ttk.Label(main_frame, text="Select File to Encrypt/Decrypt:", 
                 font=('Arial', 10, 'bold')).pack(anchor='w', pady=(10, 5))
        
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Entry(input_frame, textvariable=self.input_file, 
                 width=50).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(input_frame, text="Browse", 
                  command=self.browse_input).pack(side=tk.LEFT, padx=5)
        
        # Output file section
        ttk.Label(main_frame, text="Output File Path:", 
                 font=('Arial', 10, 'bold')).pack(anchor='w', pady=(10, 5))
        
        output_frame = ttk.Frame(main_frame)
        output_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Entry(output_frame, textvariable=self.output_file, 
                 width=50).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(output_frame, text="Browse", 
                  command=self.browse_output).pack(side=tk.LEFT, padx=5)
        
        # Password section
        ttk.Label(main_frame, text="Password:", 
                 font=('Arial', 10, 'bold')).pack(anchor='w', pady=(10, 5))
        ttk.Entry(main_frame, textvariable=self.password, 
                 show="•", width=50).pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(main_frame, text="Confirm Password:", 
                 font=('Arial', 10, 'bold')).pack(anchor='w', pady=(10, 5))
        ttk.Entry(main_frame, textvariable=self.password_confirm, 
                 show="•", width=50).pack(fill=tk.X, pady=(0, 15))
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=20)
        
        ttk.Button(button_frame, text="Encrypt File", 
                  command=self.encrypt_action).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Decrypt File", 
                  command=self.decrypt_action).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear", 
                  command=self.clear_fields).pack(side=tk.LEFT, padx=5)
        
        # Status/Log area
        ttk.Label(main_frame, text="Status:", 
                 font=('Arial', 10, 'bold')).pack(anchor='w', pady=(10, 5))
        
        self.log_text = tk.Text(main_frame, height=8, width=60, 
                               font=('Courier', 9), state=tk.DISABLED)
        self.log_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Scrollbar for log
        scrollbar = ttk.Scrollbar(self.log_text, command=self.log_text.yview)
        self.log_text['yscrollcommand'] = scrollbar.set
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.pack(fill=tk.X, pady=(0, 10))
    
    def browse_input(self):
        """Browse for input file"""
        filename = filedialog.askopenfilename(
            title="Select file to encrypt/decrypt",
            filetypes=[("All Files", "*.*")]
        )
        if filename:
            self.input_file.set(filename)
            # Auto-generate output filename
            if filename.endswith('.enc'):
                self.output_file.set(filename.replace('.enc', '_decrypted'))
            else:
                self.output_file.set(filename + '.enc')
    
    def browse_output(self):
        """Browse for output file"""
        filename = filedialog.asksaveasfilename(
            title="Save encrypted/decrypted file as",
            filetypes=[("All Files", "*.*")]
        )
        if filename:
            self.output_file.set(filename)
    
    def log_message(self, message):
        """Add message to log"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + '\n')
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
    
    def clear_log(self):
        """Clear log messages"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)
    
    def clear_fields(self):
        """Clear all input fields"""
        self.input_file.set('')
        self.output_file.set('')
        self.password.set('')
        self.password_confirm.set('')
        self.clear_log()
    
    def validate_inputs(self, operation):
        """Validate user inputs"""
        if not self.input_file.get():
            messagebox.showerror("Error", "Please select an input file")
            return False
        
        if not self.output_file.get():
            messagebox.showerror("Error", "Please specify an output file")
            return False
        
        if not self.password.get():
            messagebox.showerror("Error", "Please enter a password")
            return False
        
        if operation == "encrypt":
            if self.password.get() != self.password_confirm.get():
                messagebox.showerror("Error", "Passwords do not match")
                return False
            
            if len(self.password.get()) < 8:
                messagebox.showwarning("Warning", 
                    "Password is less than 8 characters. Stronger passwords recommended.")
        
        return True
    
    def encrypt_action(self):
        """Handle encryption action"""
        if not self.validate_inputs("encrypt"):
            return
        
        # Run encryption in separate thread to prevent UI freeze
        thread = threading.Thread(target=self._encrypt_thread)
        thread.start()
    
    def _encrypt_thread(self):
        """Encryption in background thread"""
        try:
            self.progress.start()
            self.clear_log()
            self.log_message("Starting encryption...")
            self.log_message(f"Input: {self.input_file.get()}")
            self.log_message(f"Output: {self.output_file.get()}")
            self.log_message("Encrypting with AES-256-CBC...")
            
            result = EncryptionEngine.encrypt_file(
                self.input_file.get(),
                self.output_file.get(),
                self.password.get()
            )
            
            if result["status"] == "success":
                self.log_message(f"\n✓ {result['message']}")
                self.log_message(f"Original size: {result['input_size']:,} bytes")
                self.log_message(f"Encrypted size: {result['output_size']:,} bytes")
                messagebox.showinfo("Success", "File encrypted successfully!")
            else:
                self.log_message(f"\n✗ Error: {result['message']}")
                messagebox.showerror("Error", result['message'])
            
            self.progress.stop()
        
        except Exception as e:
            self.log_message(f"\n✗ Unexpected error: {str(e)}")
            messagebox.showerror("Error", f"Unexpected error: {str(e)}")
            self.progress.stop()
    
    def decrypt_action(self):
        """Handle decryption action"""
        if not self.input_file.get():
            messagebox.showerror("Error", "Please select an input file")
            return
        
        if not self.output_file.get():
            messagebox.showerror("Error", "Please specify an output file")
            return
        
        if not self.password.get():
            messagebox.showerror("Error", "Please enter the password")
            return
        
        # Run decryption in separate thread
        thread = threading.Thread(target=self._decrypt_thread)
        thread.start()
    
    def _decrypt_thread(self):
        """Decryption in background thread"""
        try:
            self.progress.start()
            self.clear_log()
            self.log_message("Starting decryption...")
            self.log_message(f"Input: {self.input_file.get()}")
            self.log_message(f"Output: {self.output_file.get()}")
            self.log_message("Decrypting with AES-256-CBC...")
            
            result = EncryptionEngine.decrypt_file(
                self.input_file.get(),
                self.output_file.get(),
                self.password.get()
            )
            
            if result["status"] == "success":
                self.log_message(f"\n✓ {result['message']}")
                self.log_message(f"Decrypted size: {result['output_size']:,} bytes")
                messagebox.showinfo("Success", "File decrypted successfully!")
            else:
                self.log_message(f"\n✗ Error: {result['message']}")
                messagebox.showerror("Error", result['message'])
            
            self.progress.stop()
        
        except Exception as e:
            self.log_message(f"\n✗ Unexpected error: {str(e)}")
            messagebox.showerror("Error", f"Unexpected error: {str(e)}")
            self.progress.stop()


def run_gui():
    """Run the GUI application"""
    root = tk.Tk()
    gui = EncryptionGUI(root)
    root.mainloop()


if __name__ == "__main__":
    run_gui()
