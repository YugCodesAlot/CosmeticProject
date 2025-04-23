import tkinter as tk
from tkinter import ttk
from .product_management import ProductManagement
from .customer_management import CustomerManagement
from .sales import Sales
from .inventory import Inventory
from .reports import Reports

class Dashboard:
    def __init__(self, root, db, user, logout_callback):
        self.root = root
        self.db = db
        self.user = user
        self.logout_callback = logout_callback
        
        # Create main frame
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create header frame
        self.create_header()
        
        # Create sidebar and content area
        self.create_sidebar()
        
        # Create content frame
        self.content_frame = ttk.Frame(self.main_frame, padding=10)
        self.content_frame.grid(row=1, column=1, sticky="nsew")
        
        # Configure grid weights
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)
        
        # Show default page (products)
        self.show_products()
    
    def create_header(self):
        """Create header with app title and user info"""
        header_frame = ttk.Frame(self.main_frame, padding=10, style="Header.TFrame")
        header_frame.grid(row=0, column=0, columnspan=2, sticky="ew")
        
        # App title
        title_label = ttk.Label(header_frame, text="Cosmetic Shop Management", 
                               font=("Arial", 16, "bold"))
        title_label.pack(side=tk.LEFT)
        
        # User info and logout
        user_frame = ttk.Frame(header_frame)
        user_frame.pack(side=tk.RIGHT)
        
        user_label = ttk.Label(user_frame, text=f"Logged in as: {self.user['username']} ({self.user['role']})")
        user_label.pack(side=tk.LEFT, padx=10)
        
        logout_button = ttk.Button(user_frame, text="Logout", command=self.logout_callback)
        logout_button.pack(side=tk.LEFT)
        
        # Configure style for header
        style = ttk.Style()
        style.configure("Header.TFrame", background="#e0e0e0")
        style.configure("Header.TLabel", background="#e0e0e0")
    
    def create_sidebar(self):
        """Create sidebar with navigation buttons"""
        sidebar_frame = ttk.Frame(self.main_frame, padding=10, width=200)
        sidebar_frame.grid(row=1, column=0, sticky="ns")
        sidebar_frame.grid_propagate(False)  # Prevent frame from shrinking
        
        # Style for sidebar buttons
        style = ttk.Style()
        style.configure("Sidebar.TButton", font=("Arial", 11), width=20)
        
        # Navigation buttons
        buttons = [
            ("Products", self.show_products),
            ("Customers", self.show_customers),
            ("Sales", self.show_sales),
            ("Inventory", self.show_inventory),
            ("Reports", self.show_reports)
        ]
        
        for i, (text, command) in enumerate(buttons):
            btn = ttk.Button(sidebar_frame, text=text, command=command, style="Sidebar.TButton")
            btn.grid(row=i, column=0, pady=5, sticky="ew")
        
        # Make sure sidebar maintains its width
        sidebar_frame.grid_columnconfigure(0, weight=1)
    
    def clear_content(self):
        """Clear the content frame"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def show_products(self):
        """Show product management page"""
        self.clear_content()
        ProductManagement(self.content_frame, self.db)
    
    def show_customers(self):
        """Show customer management page"""
        self.clear_content()
        CustomerManagement(self.content_frame, self.db)
    
    def show_sales(self):
        """Show sales management page"""
        self.clear_content()
        Sales(self.content_frame, self.db)
    
    def show_inventory(self):
        """Show inventory management page"""
        self.clear_content()
        Inventory(self.content_frame, self.db)
    
    def show_reports(self):
        """Show reports page"""
        self.clear_content()
        Reports(self.content_frame, self.db)
