import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import json
from src.utils import validate_email

class Settings:
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        
        # Default settings
        self.settings = {
            "shop_name": "Cosmetic Shop",
            "owner_name": "",
            "email": "",
            "phone": "",
            "address": "",
            "tax_rate": 0.0,
            "currency": "USD",
            "low_stock_threshold": 10,
            "backup_path": ""
        }
        
        # Load settings
        self.load_settings()
        
        # Create main frame
        self.frame = ttk.Frame(parent)
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(self.frame, text="Settings", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 10), sticky="w")
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.frame)
        self.notebook.grid(row=1, column=0, sticky="nsew")
        
        # Create tabs
        self.create_general_tab()
        self.create_backup_tab()
        self.create_about_tab()
        
        # Configure grid weights
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
    
    def create_general_tab(self):
        """Create general settings tab"""
        general_frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(general_frame, text="General")
        
        # Shop information
        shop_frame = ttk.LabelFrame(general_frame, text="Shop Information", padding=10)
        shop_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Shop name
        ttk.Label(shop_frame, text="Shop Name:").grid(row=0, column=0, sticky="w", pady=5)
        self.shop_name_var = tk.StringVar(value=self.settings["shop_name"])
        ttk.Entry(shop_frame, textvariable=self.shop_name_var, width=30).grid(row=0, column=1, sticky="w", pady=5)
        
        # Owner name
        ttk.Label(shop_frame, text="Owner Name:").grid(row=1, column=0, sticky="w", pady=5)
        self.owner_name_var = tk.StringVar(value=self.settings["owner_name"])
        ttk.Entry(shop_frame, textvariable=self.owner_name_var, width=30).grid(row=1, column=1, sticky="w", pady=5)
        
        # Email
        ttk.Label(shop_frame, text="Email:").grid(row=2, column=0, sticky="w", pady=5)
        self.email_var = tk.StringVar(value=self.settings["email"])
        ttk.Entry(shop_frame, textvariable=self.email_var, width=30).grid(row=2, column=1, sticky="w", pady=5)
        
        # Phone
        ttk.Label(shop_frame, text="Phone:").grid(row=3, column=0, sticky="w", pady=5)
        self.phone_var = tk.StringVar(value=self.settings["phone"])
        ttk.Entry(shop_frame, textvariable=self.phone_var, width=30).grid(row=3, column=1, sticky="w", pady=5)
        
        # Address
        ttk.Label(shop_frame, text="Address:").grid(row=4, column=0, sticky="nw", pady=5)
        self.address_text = tk.Text(shop_frame, width=30, height=3)
        self.address_text.grid(row=4, column=1, sticky="w", pady=5)
        self.address_text.insert(tk.END, self.settings["address"])
        
        # Configure grid weights
        shop_frame.grid_columnconfigure(1, weight=1)
        
        # Business settings
        business_frame = ttk.LabelFrame(general_frame, text="Business Settings", padding=10)
        business_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Tax rate
        ttk.Label(business_frame, text="Tax Rate (%):").grid(row=0, column=0, sticky="w", pady=5)
        self.tax_rate_var = tk.StringVar(value=str(self.settings["tax_rate"] * 100))
        ttk.Entry(business_frame, textvariable=self.tax_rate_var, width=10).grid(row=0, column=1, sticky="w", pady=5)
        
        # Currency
        ttk.Label(business_frame, text="Currency:").grid(row=1, column=0, sticky="w", pady=5)
        self.currency_var = tk.StringVar(value=self.settings["currency"])
        ttk.Combobox(business_frame, textvariable=self.currency_var, width=10,
                    values=["USD", "EUR", "GBP", "CAD", "AUD"]).grid(row=1, column=1, sticky="w", pady=5)
        
        # Low stock threshold
        ttk.Label(business_frame, text="Low Stock Threshold:").grid(row=2, column=0, sticky="w", pady=5)
        self.threshold_var = tk.StringVar(value=str(self.settings["low_stock_threshold"]))
        ttk.Entry(business_frame, textvariable=self.threshold_var, width=10).grid(row=2, column=1, sticky="w", pady=5)
        
        # Configure grid weights
        business_frame.grid_columnconfigure(1, weight=1)
        
        # Save button
        save_button = ttk.Button(general_frame, text="Save Settings", command=self.save_general_settings)
        save_button.pack(pady=10)
    
    def create_backup_tab(self):
        """Create backup settings tab"""
        backup_frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(backup_frame, text="Backup & Restore")
        
        # Backup settings
        settings_frame = ttk.LabelFrame(backup_frame, text="Backup Settings", padding=10)
        settings_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Backup path
        ttk.Label(settings_frame, text="Backup Path:").grid(row=0, column=0, sticky="w", pady=5)
        self.backup_path_var = tk.StringVar(value=self.settings["backup_path"])
        ttk.Entry(settings_frame, textvariable=self.backup_path_var, width=40).grid(row=0, column=1, sticky="ew", pady=5)
        
        # Browse button
        browse_button = ttk.Button(settings_frame, text="Browse", command=self.browse_backup_path)
        browse_button.grid(row=0, column=2, padx=(5, 0), pady=5)
        
        # Configure grid weights
        settings_frame.grid_columnconfigure(1, weight=1)
        
        # Backup and restore buttons
        buttons_frame = ttk.Frame(backup_frame)
        buttons_frame.pack(fill=tk.X, pady=10)
        
        backup_button = ttk.Button(buttons_frame, text="Create Backup", command=self.create_backup)
        backup_button.pack(side=tk.LEFT, padx=(0, 5))
        
        restore_button = ttk.Button(buttons_frame, text="Restore from Backup", command=self.restore_backup)
        restore_button.pack(side=tk.LEFT)
        
        # Save button
        save_button = ttk.Button(backup_frame, text="Save Backup Settings", command=self.save_backup_settings)
        save_button.pack(pady=10)
    
    def create_about_tab(self):
        """Create about tab"""
        about_frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(about_frame, text="About")
        
        # App info
        app_frame = ttk.LabelFrame(about_frame, text="Application Information", padding=10)
        app_frame.pack(fill=tk.X, pady=(0, 10))
        
        # App name
        ttk.Label(app_frame, text="Cosmetic Shop Management System", font=("Arial", 12, "bold")).pack(anchor="w", pady=5)
        
        # Version
        ttk.Label(app_frame, text="Version: 1.0.0").pack(anchor="w", pady=2)
        
        # Developer
        ttk.Label(app_frame, text="Developed by: Your Name").pack(anchor="w", pady=2)
        
        # Contact
        ttk.Label(app_frame, text="Contact: your.email@example.com").pack(anchor="w", pady=2)
        
        # Description
        desc_frame = ttk.LabelFrame(about_frame, text="Description", padding=10)
        desc_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        description = """
        Cosmetic Shop Management System is a comprehensive solution for managing your cosmetic retail business.
        
        Features:
        - Product management
        - Customer management
        - Sales and order processing
        - Inventory tracking
        - Reports and analytics
        - Backup and restore
        
        This application is designed to help cosmetic shop owners streamline their operations and make data-driven decisions.
        """
        
        desc_text = tk.Text(desc_frame, wrap=tk.WORD, height=10)
        desc_text.pack(fill=tk.BOTH, expand=True)
        desc_text.insert(tk.END, description)
        desc_text.config(state=tk.DISABLED)
    
    def load_settings(self):
        """Load settings from file"""
        settings_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "settings.json")
        
        if os.path.exists(settings_path):
            try:
                with open(settings_path, 'r') as f:
                    loaded_settings = json.load(f)
                    # Update settings with loaded values
                    self.settings.update(loaded_settings)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load settings: {e}")
    
    def save_settings(self):
        """Save settings to file"""
        settings_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "settings.json")
        
        try:
            with open(settings_path, 'w') as f:
                json.dump(self.settings, f, indent=4)
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {e}")
            return False
    
    def save_general_settings(self):
        """Save general settings"""
        # Validate inputs
        email = self.email_var.get().strip()
        if email and not validate_email(email):
            messagebox.showerror("Error", "Invalid email format")
            return
        
        try:
            tax_rate = float(self.tax_rate_var.get()) / 100
            if tax_rate < 0:
                raise ValueError("Tax rate cannot be negative")
        except ValueError:
            messagebox.showerror("Error", "Invalid tax rate")
            return
        
        try:
            threshold = int(self.threshold_var.get())
            if threshold < 0:
                raise ValueError("Threshold cannot be negative")
        except ValueError:
            messagebox.showerror("Error", "Invalid low stock threshold")
            return
        
        # Update settings
        self.settings["shop_name"] = self.shop_name_var.get().strip()
        self.settings["owner_name"] = self.owner_name_var.get().strip()
        self.settings["email"] = email
        self.settings["phone"] = self.phone_var.get().strip()
        self.settings["address"] = self.address_text.get(1.0, tk.END).strip()
        self.settings["tax_rate"] = tax_rate
        self.settings["currency"] = self.currency_var.get()
        self.settings["low_stock_threshold"] = threshold
        
        # Save settings
        if self.save_settings():
            messagebox.showinfo("Success", "Settings saved successfully")
    
    def save_backup_settings(self):
        """Save backup settings"""
        backup_path = self.backup_path_var.get().strip()
        
        if backup_path and not os.path.isdir(backup_path):
            messagebox.showerror("Error", "Invalid backup path")
            return
        
        # Update settings
        self.settings["backup_path"] = backup_path
        
        # Save settings
        if self.save_settings():
            messagebox.showinfo("Success", "Backup settings saved successfully")
    
    def browse_backup_path(self):
        """Browse for backup path"""
        backup_path = filedialog.askdirectory()
        if backup_path:
            self.backup_path_var.set(backup_path)
    
    def create_backup(self):
        """Create database backup"""
        backup_path = self.backup_path_var.get().strip()
        
        if not backup_path:
            messagebox.showerror("Error", "Please set a backup path first")
            return
        
        if not os.path.isdir(backup_path):
            messagebox.showerror("Error", "Invalid backup path")
            return
        
        # In a real application, you would implement database backup logic here
        # For this example, we'll just show a success message
        
        backup_file = os.path.join(backup_path, f"cosmetic_shop_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sql")
        
        try:
            # Simulate backup process
            messagebox.showinfo("Success", f"Backup created successfully at:\n{backup_file}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create backup: {e}")
    
    def restore_backup(self):
        """Restore database from backup"""
        backup_path = self.backup_path_var.get().strip()
        
        if not backup_path:
            messagebox.showerror("Error", "Please set a backup path first")
            return
        
        # Ask for backup file
        backup_file = filedialog.askopenfilename(
            initialdir=backup_path,
            title="Select Backup File",
            filetypes=[("SQL Files", "*.sql"), ("All Files", "*.*")]
        )
        
        if not backup_file:
            return  # User cancelled
        
        # Confirm restore
        confirm = messagebox.askyesno(
            "Confirm Restore",
            "Restoring from backup will overwrite the current database. Continue?"
        )
        
        if not confirm:
            return
        
        # In a real application, you would implement database restore logic here
        # For this example, we'll just show a success message
        
        try:
            # Simulate restore process
            messagebox.showinfo("Success", "Database restored successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to restore database: {e}")
