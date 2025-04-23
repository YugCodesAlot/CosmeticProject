import os
import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedTk
from src.database import Database
from src.ui.dashboard import Dashboard

class CosmeticShopApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cosmetic Shop Management System")
        self.root.geometry("1200x700")
        self.root.minsize(1000, 600)
        
        # Set theme
        self.style = ttk.Style()
        self.style.theme_use("clam")  # You can try different themes like 'arc', 'equilux', etc.
        
        # Configure colors
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TLabel", background="#f0f0f0", font=("Arial", 10))
        self.style.configure("TButton", font=("Arial", 10))
        self.style.configure("Heading.TLabel", font=("Arial", 16, "bold"))
        
        # Initialize database
        self.db = Database(
            host='localhost',
            user='root',
            password='',  # Replace with your MySQL password
            database='cosmetic_shop'
        )
        
        # Create necessary directories
        self.create_directories()
        
        # Start with login screen
        self.show_login()
    
    def create_directories(self):
        """Create necessary directories for the application"""
        directories = [
            os.path.join(os.getcwd(), "images"),
            os.path.join(os.getcwd(), "images", "product_images"),
            os.path.join(os.getcwd(), "reports")
        ]
        
        for directory in directories:
            if not os.path.exists(directory):
                os.makedirs(directory)
    
    def show_login(self):
        """Show login screen"""
        # Clear current window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Create login frame
        login_frame = ttk.Frame(self.root, padding=20)
        login_frame.pack(expand=True)
        
        # Title
        title_label = ttk.Label(login_frame, text="Cosmetic Shop Management System", 
                               font=("Arial", 18, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Username
        ttk.Label(login_frame, text="Username:").grid(row=1, column=0, sticky="w", pady=5)
        username_var = tk.StringVar()
        username_entry = ttk.Entry(login_frame, textvariable=username_var, width=30)
        username_entry.grid(row=1, column=1, pady=5)
        username_entry.focus()
        
        # Password
        ttk.Label(login_frame, text="Password:").grid(row=2, column=0, sticky="w", pady=5)
        password_var = tk.StringVar()
        password_entry = ttk.Entry(login_frame, textvariable=password_var, show="*", width=30)
        password_entry.grid(row=2, column=1, pady=5)
        
        # Login button
        login_button = ttk.Button(login_frame, text="Login", 
                                 command=lambda: self.login(username_var.get(), password_var.get()))
        login_button.grid(row=3, column=0, columnspan=2, pady=20)
        
        # Bind Enter key to login
        self.root.bind("<Return>", lambda event: self.login(username_var.get(), password_var.get()))
    
    def login(self, username, password):
        """Handle login process"""
        # For simplicity, we're using a direct comparison
        # In a real application, you should use proper password hashing
        self.db.connect()
        self.db.cursor.execute(
            "SELECT * FROM users WHERE username = %s AND password = %s",
            (username, password)
        )
        user = self.db.cursor.fetchone()
        self.db.disconnect()
        
        if user:
            self.current_user = user
            self.show_dashboard()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")
    
    def show_dashboard(self):
        """Show main dashboard after successful login"""
        # Clear current window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Unbind previous events
        self.root.unbind("<Return>")
        
        # Create and show dashboard
        dashboard = Dashboard(self.root, self.db, self.current_user, self.logout)
    
    def logout(self):
        """Log out and return to login screen"""
        self.current_user = None
        self.show_login()

if __name__ == "__main__":
    root = ThemedTk(theme="arc")  # You can try different themes
    app = CosmeticShopApp(root)
    root.mainloop()
