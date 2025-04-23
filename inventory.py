import tkinter as tk
from tkinter import ttk, messagebox
from src.utils import format_currency

class Inventory:
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        
        # Create main frame
        self.frame = ttk.Frame(parent)
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(self.frame, text="Inventory Management", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 10), sticky="w")
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.frame)
        self.notebook.grid(row=1, column=0, sticky="nsew")
        
        # Create tabs
        self.create_stock_levels_tab()
        self.create_stock_adjustment_tab()
        self.create_low_stock_tab()
        
        # Configure grid weights
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
    
    def create_stock_levels_tab(self):
        """Create tab for viewing current stock levels"""
        stock_frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(stock_frame, text="Stock Levels")
        
        # Filter frame
        filter_frame = ttk.Frame(stock_frame)
        filter_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Search
        ttk.Label(filter_frame, text="Search:").pack(side=tk.LEFT, padx=(0, 5))
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(filter_frame, textvariable=self.search_var, width=20)
        search_entry.pack(side=tk.LEFT, padx=(0, 10))
        
        # Category filter
        ttk.Label(filter_frame, text="Category:").pack(side=tk.LEFT, padx=(0, 5))
        self.category_var = tk.StringVar()
        self.category_combobox = ttk.Combobox(filter_frame, textvariable=self.category_var, width=15)
        self.category_combobox.pack(side=tk.LEFT, padx=(0, 10))
        
        # Load categories
        self.load_categories()
        
        # Search button
        search_button = ttk.Button(filter_frame, text="Search", command=self.load_stock_levels)
        search_button.pack(side=tk.LEFT)
        
        # Reset button
        reset_button = ttk.Button(filter_frame, text="Reset", command=self.reset_filters)
        reset_button.pack(side=tk.LEFT, padx=(5, 0))
        
        # Stock list
        list_frame = ttk.Frame(stock_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Treeview for stock levels
        columns = ("id", "name", "category", "price", "stock")
        self.stock_tree = ttk.Treeview(list_frame, columns=columns, show="headings", 
                                      yscrollcommand=scrollbar.set)
        
        # Configure columns
        self.stock_tree.heading("id", text="ID")
        self.stock_tree.heading("name", text="Product Name")
        self.stock_tree.heading("category", text="Category")
        self.stock_tree.heading("price", text="Price")
        self.stock_tree.heading("stock", text="Stock")
        
        self.stock_tree.column("id", width=50)
        self.stock_tree.column("name", width=200)
        self.stock_tree.column("category", width=100)
        self.stock_tree.column("price", width=80)
        self.stock_tree.column("stock", width=80)
        
        self.stock_tree.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.stock_tree.yview)
        
        # Load stock levels
        self.load_stock_levels()
    
    def create_stock_adjustment_tab(self):
        """Create tab for adjusting stock levels"""
        adjustment_frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(adjustment_frame, text="Stock Adjustment")
        
        # Product selection frame
        selection_frame = ttk.LabelFrame(adjustment_frame, text="Select Product", padding=10)
        selection_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Product search
        ttk.Label(selection_frame, text="Search Product:").grid(row=0, column=0, sticky="w", pady=5)
        self.product_search_var = tk.StringVar()
        product_search_entry = ttk.Entry(selection_frame, textvariable=self.product_search_var, width=30)
        product_search_entry.grid(row=0, column=1, sticky="ew", pady=5)
        
        # Search button
        search_button = ttk.Button(selection_frame, text="Search", 
                                  command=self.search_products_for_adjustment)
        search_button.grid(row=0, column=2, padx=(5, 0), pady=5)
        
        # Product list
        list_frame = ttk.Frame(selection_frame)
        list_frame.grid(row=1, column=0, columnspan=3, sticky="nsew", pady=5)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Treeview for products
        columns = ("id", "name", "category", "stock")
        self.product_tree = ttk.Treeview(list_frame, columns=columns, show="headings", 
                                        yscrollcommand=scrollbar.set, height=6)
        
        # Configure columns
        self.product_tree.heading("id", text="ID")
        self.product_tree.heading("name", text="Product Name")
        self.product_tree.heading("category", text="Category")
        self.product_tree.heading("stock", text="Current Stock")
        
        self.product_tree.column("id", width=50)
        self.product_tree.column("name", width=200)
        self.product_tree.column("category", width=100)
        self.product_tree.column("stock", width=100)
        
        self.product_tree.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.product_tree.yview)
        
        # Bind select event
        self.product_tree.bind("<<TreeviewSelect>>", self.on_product_select_for_adjustment)
        
        # Configure grid weights
        selection_frame.grid_columnconfigure(1, weight=1)
        selection_frame.grid_rowconfigure(1, weight=1)
        
        # Adjustment frame
        adjustment_details_frame = ttk.LabelFrame(adjustment_frame, text="Stock Adjustment", padding=10)
        adjustment_details_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Selected product
        ttk.Label(adjustment_details_frame, text="Selected Product:").grid(row=0, column=0, sticky="w", pady=5)
        self.selected_product_var = tk.StringVar()
        ttk.Label(adjustment_details_frame, textvariable=self.selected_product_var, font=("Arial", 10, "bold")).grid(
            row=0, column=1, sticky="w", pady=5)
        
        # Current stock
        ttk.Label(adjustment_details_frame, text="Current Stock:").grid(row=1, column=0, sticky="w", pady=5)
        self.current_stock_var = tk.StringVar()
        ttk.Label(adjustment_details_frame, textvariable=self.current_stock_var).grid(
            row=1, column=1, sticky="w", pady=5)
        
        # Adjustment type
        ttk.Label(adjustment_details_frame, text="Adjustment Type:").grid(row=2, column=0, sticky="w", pady=5)
        self.adjustment_type_var = tk.StringVar(value="Add")
        ttk.Radiobutton(adjustment_details_frame, text="Add Stock", variable=self.adjustment_type_var, 
                       value="Add").grid(row=2, column=1, sticky="w", pady=5)
        ttk.Radiobutton(adjustment_details_frame, text="Remove Stock", variable=self.adjustment_type_var, 
                       value="Remove").grid(row=3, column=1, sticky="w", pady=5)
        
        # Adjustment quantity
        ttk.Label(adjustment_details_frame, text="Quantity:").grid(row=4, column=0, sticky="w", pady=5)
        self.adjustment_quantity_var = tk.StringVar()
        quantity_entry = ttk.Entry(adjustment_details_frame, textvariable=self.adjustment_quantity_var, width=10)
        quantity_entry.grid(row=4, column=1, sticky="w", pady=5)
        
        # Reason
        ttk.Label(adjustment_details_frame, text="Reason:").grid(row=5, column=0, sticky="nw", pady=5)
        self.reason_text = tk.Text(adjustment_details_frame, width=30, height=4)
        self.reason_text.grid(row=5, column=1, sticky="ew", pady=5)
        
        # Apply button
        apply_button = ttk.Button(adjustment_details_frame, text="Apply Adjustment", 
                                 command=self.apply_stock_adjustment)
        apply_button.grid(row=6, column=0, columnspan=2, pady=10)
        
        # Configure grid weights
        adjustment_details_frame.grid_columnconfigure(1, weight=1)
        
        # Initialize
        self.selected_product_id = None
        self.load_products_for_adjustment()
    
    def create_low_stock_tab(self):
        """Create tab for viewing low stock products"""
        low_stock_frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(low_stock_frame, text="Low Stock")
        
        # Threshold frame
        threshold_frame = ttk.Frame(low_stock_frame)
        threshold_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Threshold
        ttk.Label(threshold_frame, text="Low Stock Threshold:").pack(side=tk.LEFT, padx=(0, 5))
        self.threshold_var = tk.StringVar(value="10")
        threshold_entry = ttk.Entry(threshold_frame, textvariable=self.threshold_var, width=10)
        threshold_entry.pack(side=tk.LEFT, padx=(0, 10))
        
        # Apply button
        apply_button = ttk.Button(threshold_frame, text="Apply", command=self.load_low_stock)
        apply_button.pack(side=tk.LEFT)
        
        # Low stock list
        list_frame = ttk.Frame(low_stock_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Treeview for low stock
        columns = ("id", "name", "category", "stock", "threshold")
        self.low_stock_tree = ttk.Treeview(list_frame, columns=columns, show="headings", 
                                          yscrollcommand=scrollbar.set)
        
        # Configure columns
        self.low_stock_tree.heading("id", text="ID")
        self.low_stock_tree.heading("name", text="Product Name")
        self.low_stock_tree.heading("category", text="Category")
        self.low_stock_tree.heading("stock", text="Current Stock")
        self.low_stock_tree.heading("threshold", text="Threshold")
        
        self.low_stock_tree.column("id", width=50)
        self.low_stock_tree.column("name", width=200)
        self.low_stock_tree.column("category", width=100)
        self.low_stock_tree.column("stock", width=100)
        self.low_stock_tree.column("threshold", width=80)
        
        self.low_stock_tree.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.low_stock_tree.yview)
        
        # Load low stock products
        self.load_low_stock()
    
    def load_categories(self):
        """Load categories for combobox"""
        self.db.connect()
        self.db.cursor.execute("SELECT id, name FROM categories ORDER BY name")
        categories = self.db.cursor.fetchall()
        self.db.disconnect()
        
        self.categories = {c['name']: c['id'] for c in categories}
        category_names = [""] + list(self.categories.keys())
        self.category_combobox['values'] = category_names
    
    def load_stock_levels(self):
        """Load stock levels into the treeview"""
        # Clear existing items
        for item in self.stock_tree.get_children():
            self.stock_tree.delete(item)
        
        # Get filter values
        search_term = self.search_var.get().strip()
        category = self.category_var.get()
        
        # Get products from database
        self.db.connect()
        
        if category and category in self.categories:
            category_id = self.categories[category]
            if search_term:
                self.db.cursor.execute('''
                SELECT p.id, p.name, p.price, p.stock_quantity, c.name as category_name
                FROM products p
                LEFT JOIN categories c ON p.category_id = c.id
                WHERE p.category_id = %s AND p.name LIKE %s
                ORDER BY p.name
                ''', (category_id, f'%{search_term}%'))
            else:
                self.db.cursor.execute('''
                SELECT p.id, p.name, p.price, p.stock_quantity, c.name as category_name
                FROM products p
                LEFT JOIN categories c ON p.category_id = c.id
                WHERE p.category_id = %s
                ORDER BY p.name
                ''', (category_id,))
        elif search_term:
            self.db.cursor.execute('''
            SELECT p.id, p.name, p.price, p.stock_quantity, c.name as category_name
            FROM products p
            LEFT JOIN categories c ON p.category_id = c.id
            WHERE p.name LIKE %s
            ORDER BY p.name
            ''', (f'%{search_term}%',))
        else:
            self.db.cursor.execute('''
            SELECT p.id, p.name, p.price, p.stock_quantity, c.name as category_name
            FROM products p
            LEFT JOIN categories c ON p.category_id = c.id
            ORDER BY p.name
            ''')
        
        products = self.db.cursor.fetchall()
        self.db.disconnect()
        
        # Insert products into treeview
        for product in products:
            self.stock_tree.insert("", "end", values=(
                product['id'],
                product['name'],
                product['category_name'] or "Uncategorized",
                format_currency(product['price']),
                product['stock_quantity']
            ))
    
    def reset_filters(self):
        """Reset search and filter fields"""
        self.search_var.set("")
        self.category_var.set("")
        self.load_stock_levels()
    
    def load_products_for_adjustment(self):
        """Load products for stock adjustment"""
        # Clear existing items
        for item in self.product_tree.get_children():
            self.product_tree.delete(item)
        
        # Get products from database
        self.db.connect()
        self.db.cursor.execute('''
        SELECT p.id, p.name, p.stock_quantity, c.name as category_name
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.id
        ORDER BY p.name
        ''')
        products = self.db.cursor.fetchall()
        self.db.disconnect()
        
        # Insert products into treeview
        for product in products:
            self.product_tree.insert("", "end", values=(
                product['id'],
                product['name'],
                product['category_name'] or "Uncategorized",
                product['stock_quantity']
            ))
    
    def search_products_for_adjustment(self):
        """Search products for stock adjustment"""
        search_term = self.product_search_var.get().strip()
        if not search_term:
            self.load_products_for_adjustment()
            return
        
        # Clear existing items
        for item in self.product_tree.get_children():
            self.product_tree.delete(item)
        
        # Search products
        self.db.connect()
        self.db.cursor.execute('''
        SELECT p.id, p.name, p.stock_quantity, c.name as category_name
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.id
        WHERE p.name LIKE %s
        ORDER BY p.name
        ''', (f'%{search_term}%',))
        products = self.db.cursor.fetchall()
        self.db.disconnect()
        
        # Insert products into treeview
        for product in products:
            self.product_tree.insert("", "end", values=(
                product['id'],
                product['name'],
                product['category_name'] or "Uncategorized",
                product['stock_quantity']
            ))
    
    def on_product_select_for_adjustment(self, event):
        """Handle product selection for stock adjustment"""
        selected_items = self.product_tree.selection()
        if not selected_items:
            return
        
        # Get the selected product
        item = self.product_tree.item(selected_items[0])
        product_id = item['values'][0]
        product_name = item['values'][1]
        current_stock = item['values'][3]
        
        # Update form fields
        self.selected_product_id = product_id
        self.selected_product_var.set(product_name)
        self.current_stock_var.set(str(current_stock))
    
    def apply_stock_adjustment(self):
        """Apply stock adjustment"""
        if not self.selected_product_id:
            messagebox.showerror("Error", "Please select a product")
            return
        
        # Validate quantity
        try:
            quantity = int(self.adjustment_quantity_var.get())
            if quantity <= 0:
                raise ValueError("Quantity must be positive")
        except ValueError:
            messagebox.showerror("Error", "Invalid quantity")
            return
        
        # Get adjustment type
        adjustment_type = self.adjustment_type_var.get()
        
        # Get reason
        reason = self.reason_text.get(1.0, tk.END).strip()
        if not reason:
            messagebox.showerror("Error", "Please provide a reason for the adjustment")
            return
        
        # Get current stock
        current_stock = int(self.current_stock_var.get())
        
        # Calculate new stock
        if adjustment_type == "Add":
            new_stock = current_stock + quantity
        else:  # Remove
            if quantity > current_stock:
                messagebox.showerror("Error", f"Cannot remove {quantity} units. Only {current_stock} in stock.")
                return
            new_stock = current_stock - quantity
        
        # Update stock
        try:
            self.db.connect()
            self.db.cursor.execute('''
            UPDATE products
            SET stock_quantity = %s
            WHERE id = %s
            ''', (new_stock, self.selected_product_id))
            self.db.conn.commit()
            
            # Log the adjustment (in a real app, you might want to store this in a table)
            messagebox.showinfo("Success", f"Stock adjusted successfully. New stock: {new_stock}")
            
            # Clear form
            self.selected_product_id = None
            self.selected_product_var.set("")
            self.current_stock_var.set("")
            self.adjustment_quantity_var.set("")
            self.reason_text.delete(1.0, tk.END)
            
            # Reload products
            self.load_products_for_adjustment()
            self.load_stock_levels()
            self.load_low_stock()
            
            self.db.disconnect()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to adjust stock: {e}")
    
    def load_low_stock(self):
        """Load low stock products"""
        # Clear existing items
        for item in self.low_stock_tree.get_children():
            self.low_stock_tree.delete(item)
        
        # Get threshold
        try:
            threshold = int(self.threshold_var.get())
            if threshold < 0:
                raise ValueError("Threshold must be positive")
        except ValueError:
            messagebox.showerror("Error", "Invalid threshold")
            return
        
        # Get low stock products
        self.db.connect()
        self.db.cursor.execute('''
        SELECT p.id, p.name, p.stock_quantity, c.name as category_name
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.id
        WHERE p.stock_quantity <= %s
        ORDER BY p.stock_quantity, p.name
        ''', (threshold,))
        products = self.db.cursor.fetchall()
        self.db.disconnect()
        
        # Insert products into treeview
        for product in products:
            self.low_stock_tree.insert("", "end", values=(
                product['id'],
                product['name'],
                product['category_name'] or "Uncategorized",
                product['stock_quantity'],
                threshold
            ))
