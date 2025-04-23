import tkinter as tk
from tkinter import ttk, messagebox
from src.models import Customer
from src.utils import validate_email, validate_phone

class CustomerManagement:
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        
        # Create main frame
        self.frame = ttk.Frame(parent)
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(self.frame, text="Customer Management", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 10), sticky="w")
        
        # Create left and right frames
        left_frame = ttk.Frame(self.frame, padding=10)
        left_frame.grid(row=1, column=0, sticky="nsew")
        
        right_frame = ttk.Frame(self.frame, padding=10)
        right_frame.grid(row=1, column=1, sticky="nsew")
        
        # Configure grid weights
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)
        self.frame.grid_rowconfigure(1, weight=1)
        
        # Create customer list (left side)
        self.create_customer_list(left_frame)
        
        # Create customer form (right side)
        self.create_customer_form(right_frame)
        
        # Load customers
        self.load_customers()
    
    def create_customer_list(self, parent):
        """Create the customer list with search"""
        # Search frame
        search_frame = ttk.Frame(parent)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Search
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT, padx=(0, 5))
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=20)
        search_entry.pack(side=tk.LEFT, padx=(0, 10))
        
        # Search button
        search_button = ttk.Button(search_frame, text="Search", command=self.search_customers)
        search_button.pack(side=tk.LEFT)
        
        # Reset button
        reset_button = ttk.Button(search_frame, text="Reset", command=self.reset_search)
        reset_button.pack(side=tk.LEFT, padx=(5, 0))
        
        # Customer list
        list_frame = ttk.Frame(parent)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Treeview for customers
        columns = ("id", "name", "email", "phone")
        self.customer_tree = ttk.Treeview(list_frame, columns=columns, show="headings", 
                                         yscrollcommand=scrollbar.set)
        
        # Configure columns
        self.customer_tree.heading("id", text="ID")
        self.customer_tree.heading("name", text="Customer Name")
        self.customer_tree.heading("email", text="Email")
        self.customer_tree.heading("phone", text="Phone")
        
        self.customer_tree.column("id", width=50)
        self.customer_tree.column("name", width=150)
        self.customer_tree.column("email", width=150)
        self.customer_tree.column("phone", width=100)
        
        self.customer_tree.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.customer_tree.yview)
        
        # Bind select event
        self.customer_tree.bind("<<TreeviewSelect>>", self.on_customer_select)
        
        # Buttons frame
        buttons_frame = ttk.Frame(parent)
        buttons_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Add button
        add_button = ttk.Button(buttons_frame, text="Add New Customer", command=self.add_new_customer)
        add_button.pack(side=tk.LEFT)
        
        # Delete button
        delete_button = ttk.Button(buttons_frame, text="Delete Customer", command=self.delete_customer)
        delete_button.pack(side=tk.LEFT, padx=(5, 0))
    
    def create_customer_form(self, parent):
        """Create the customer form for adding/editing customers"""
        # Form frame
        form_frame = ttk.LabelFrame(parent, text="Customer Details", padding=10)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Customer ID (hidden)
        self.customer_id_var = tk.StringVar()
        
        # Customer Name
        ttk.Label(form_frame, text="Customer Name:").grid(row=0, column=0, sticky="w", pady=5)
        self.name_var = tk.StringVar()
        name_entry = ttk.Entry(form_frame, textvariable=self.name_var, width=30)
        name_entry.grid(row=0, column=1, sticky="ew", pady=5)
        
        # Email
        ttk.Label(form_frame, text="Email:").grid(row=1, column=0, sticky="w", pady=5)
        self.email_var = tk.StringVar()
        email_entry = ttk.Entry(form_frame, textvariable=self.email_var, width=30)
        email_entry.grid(row=1, column=1, sticky="ew", pady=5)
        
        # Phone
        ttk.Label(form_frame, text="Phone:").grid(row=2, column=0, sticky="w", pady=5)
        self.phone_var = tk.StringVar()
        phone_entry = ttk.Entry(form_frame, textvariable=self.phone_var, width=30)
        phone_entry.grid(row=2, column=1, sticky="ew", pady=5)
        
        # Address
        ttk.Label(form_frame, text="Address:").grid(row=3, column=0, sticky="nw", pady=5)
        self.address_text = tk.Text(form_frame, width=30, height=5)
        self.address_text.grid(row=3, column=1, sticky="ew", pady=5)
        
        # Save button
        save_button = ttk.Button(form_frame, text="Save Customer", command=self.save_customer)
        save_button.grid(row=4, column=0, columnspan=2, pady=10)
        
        # Configure grid weights
        form_frame.grid_columnconfigure(1, weight=1)
    
    def load_customers(self):
        """Load all customers into the treeview"""
        # Clear existing items
        for item in self.customer_tree.get_children():
            self.customer_tree.delete(item)
        
        # Get customers from database
        customers = self.db.get_all_customers()
        
        # Insert customers into treeview
        for customer in customers:
            self.customer_tree.insert("", "end", values=(
                customer['id'],
                customer['name'],
                customer['email'] or "",
                customer['phone'] or ""
            ))
    
    def search_customers(self):
        """Search customers based on search term"""
        search_term = self.search_var.get().strip().lower()
        if not search_term:
            self.load_customers()
            return
        
        # Clear existing items
        for item in self.customer_tree.get_children():
            self.customer_tree.delete(item)
        
        # Get all customers and filter
        self.db.connect()
        self.db.cursor.execute('''
        SELECT id, name, email, phone
        FROM customers
        WHERE LOWER(name) LIKE %s OR LOWER(email) LIKE %s OR LOWER(phone) LIKE %s
        ORDER BY name
        ''', (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))
        customers = self.db.cursor.fetchall()
        self.db.disconnect()
        
        # Insert filtered customers into treeview
        for customer in customers:
            self.customer_tree.insert("", "end", values=(
                customer['id'],
                customer['name'],
                customer['email'] or "",
                customer['phone'] or ""
            ))
    
    def reset_search(self):
        """Reset search field and reload all customers"""
        self.search_var.set("")
        self.load_customers()
    
    def on_customer_select(self, event):
        """Handle customer selection in treeview"""
        selected_items = self.customer_tree.selection()
        if not selected_items:
            return
        
        # Get the selected customer ID
        item = self.customer_tree.item(selected_items[0])
        customer_id = item['values'][0]
        
        # Load customer details
        self.db.connect()
        self.db.cursor.execute('''
        SELECT id, name, email, phone, address
        FROM customers
        WHERE id = %s
        ''', (customer_id,))
        customer = self.db.cursor.fetchone()
        self.db.disconnect()
        
        if not customer:
            return
        
        # Update form fields
        self.customer_id_var.set(customer['id'])
        self.name_var.set(customer['name'])
        self.email_var.set(customer['email'] or "")
        self.phone_var.set(customer['phone'] or "")
        
        # Update address
        self.address_text.delete(1.0, tk.END)
        if customer['address']:
            self.address_text.insert(tk.END, customer['address'])
    
    def add_new_customer(self):
        """Clear form for adding a new customer"""
        self.customer_id_var.set("")
        self.name_var.set("")
        self.email_var.set("")
        self.phone_var.set("")
        self.address_text.delete(1.0, tk.END)
    
    def save_customer(self):
        """Save customer to database"""
        # Validate form
        name = self.name_var.get().strip()
        email = self.email_var.get().strip()
        phone = self.phone_var.get().strip()
        address = self.address_text.get(1.0, tk.END).strip()
        
        # Basic validation
        if not name:
            messagebox.showerror("Error", "Customer name is required")
            return
        
        if email and not validate_email(email):
            messagebox.showerror("Error", "Invalid email format")
            return
        
        if phone and not validate_phone(phone):
            messagebox.showerror("Error", "Invalid phone number format")
            return
        
        # Save
          def save_customer(self):
        """Save customer to database"""
        # Validate form
        name = self.name_var.get().strip()
        email = self.email_var.get().strip()
        phone = self.phone_var.get().strip()
        address = self.address_text.get(1.0, tk.END).strip()
        
        # Basic validation
        if not name:
            messagebox.showerror("Error", "Customer name is required")
            return
        
        if email and not validate_email(email):
            messagebox.showerror("Error", "Invalid email format")
            return
        
        if phone and not validate_phone(phone):
            messagebox.showerror("Error", "Invalid phone number format")
            return
        
        # Save to database
        customer_id = self.customer_id_var.get()
        
        try:
            self.db.connect()
            if customer_id:  # Update existing customer
                self.db.cursor.execute('''
                UPDATE customers
                SET name = %s, email = %s, phone = %s, address = %s
                WHERE id = %s
                ''', (name, email, phone, address, customer_id))
                messagebox.showinfo("Success", "Customer updated successfully")
            else:  # Add new customer
                self.db.cursor.execute('''
                INSERT INTO customers (name, email, phone, address)
                VALUES (%s, %s, %s, %s)
                ''', (name, email, phone, address))
                messagebox.showinfo("Success", "Customer added successfully")
            
            self.db.conn.commit()
            self.db.disconnect()
            
            # Refresh customer list
            self.load_customers()
            
            # Clear form
            self.add_new_customer()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save customer: {e}")
    
    def delete_customer(self):
        """Delete selected customer"""
        selected_items = self.customer_tree.selection()
        if not selected_items:
            messagebox.showinfo("Info", "Please select a customer to delete")
            return
        
        # Get the selected customer ID
        item = self.customer_tree.item(selected_items[0])
        customer_id = item['values'][0]
        customer_name = item['values'][1]
        
        # Check if customer has orders
        self.db.connect()
        self.db.cursor.execute("SELECT COUNT(*) as count FROM orders WHERE customer_id = %s", (customer_id,))
        result = self.db.cursor.fetchone()
        has_orders = result['count'] > 0
        self.db.disconnect()
        
        if has_orders:
            messagebox.showerror(
                "Cannot Delete",
                f"Customer '{customer_name}' has orders and cannot be deleted. " +
                "Please delete the orders first or deactivate the customer instead."
            )
            return
        
        # Confirm deletion
        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete the customer '{customer_name}'?"
        )
        
        if confirm:
            try:
                self.db.connect()
                self.db.cursor.execute("DELETE FROM customers WHERE id = %s", (customer_id,))
                self.db.conn.commit()
                self.db.disconnect()
                
                messagebox.showinfo("Success", "Customer deleted successfully")
                self.load_customers()
                self.add_new_customer()  # Clear form
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete customer: {e}")
