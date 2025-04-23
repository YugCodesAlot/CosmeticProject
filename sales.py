import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from src.utils import format_currency, format_date

class Sales:
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        
        # Create main frame
        self.frame = ttk.Frame(parent)
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(self.frame, text="Sales Management", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 10), sticky="w")
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.frame)
        self.notebook.grid(row=1, column=0, sticky="nsew")
        
        # Create tabs
        self.create_new_order_tab()
        self.create_orders_list_tab()
        
        # Configure grid weights
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
    
    def create_new_order_tab(self):
        """Create tab for creating new orders"""
        new_order_frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(new_order_frame, text="New Order")
        
        # Split into left and right panes
        left_frame = ttk.Frame(new_order_frame)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        
        right_frame = ttk.Frame(new_order_frame)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
        
        new_order_frame.grid_columnconfigure(0, weight=1)
        new_order_frame.grid_columnconfigure(1, weight=1)
        new_order_frame.grid_rowconfigure(0, weight=1)
        
        # Customer selection (left top)
        customer_frame = ttk.LabelFrame(left_frame, text="Customer Information", padding=10)
        customer_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(customer_frame, text="Select Customer:").grid(row=0, column=0, sticky="w", pady=5)
        self.customer_var = tk.StringVar()
        self.customer_combobox = ttk.Combobox(customer_frame, textvariable=self.customer_var, width=30)
        self.customer_combobox.grid(row=0, column=1, sticky="ew", pady=5)
        
        # Load customers
        self.load_customers()
        
        # Product selection (left middle)
        product_frame = ttk.LabelFrame(left_frame, text="Add Products", padding=10)
        product_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Product category filter
        ttk.Label(product_frame, text="Category:").grid(row=0, column=0, sticky="w", pady=5)
        self.category_var = tk.StringVar()
        self.category_combobox = ttk.Combobox(product_frame, textvariable=self.category_var, width=20)
        self.category_combobox.grid(row=0, column=1, sticky="ew", pady=5)
        self.category_combobox.bind("<<ComboboxSelected>>", self.on_category_selected)
        
        # Load categories
        self.load_categories()
        
        # Product list
        ttk.Label(product_frame, text="Product:").grid(row=1, column=0, sticky="w", pady=5)
        self.product_var = tk.StringVar()
        self.product_combobox = ttk.Combobox(product_frame, textvariable=self.product_var, width=20)
        self.product_combobox.grid(row=1, column=1, sticky="ew", pady=5)
        self.product_combobox.bind("<<ComboboxSelected>>", self.on_product_selected)
        
        # Load products
        self.load_products()
        
        # Quantity
        ttk.Label(product_frame, text="Quantity:").grid(row=2, column=0, sticky="w", pady=5)
        self.quantity_var = tk.StringVar(value="1")
        quantity_entry = ttk.Entry(product_frame, textvariable=self.quantity_var, width=10)
        quantity_entry.grid(row=2, column=1, sticky="w", pady=5)
        
        # Price
        ttk.Label(product_frame, text="Price ($):").grid(row=3, column=0, sticky="w", pady=5)
        self.price_var = tk.StringVar()
        price_entry = ttk.Entry(product_frame, textvariable=self.price_var, width=10)
        price_entry.grid(row=3, column=1, sticky="w", pady=5)
        
        # Stock info
        self.stock_label = ttk.Label(product_frame, text="Available Stock: 0")
        self.stock_label.grid(row=4, column=0, columnspan=2, sticky="w", pady=5)
        
        # Add to order button
        add_button = ttk.Button(product_frame, text="Add to Order", command=self.add_to_order)
        add_button.grid(row=5, column=0, columnspan=2, pady=10)
        
        # Configure grid weights for product frame
        product_frame.grid_columnconfigure(1, weight=1)
        
        # Order summary (right side)
        order_frame = ttk.LabelFrame(right_frame, text="Order Summary", padding=10)
        order_frame.pack(fill=tk.BOTH, expand=True)
        
        # Order items list
        list_frame = ttk.Frame(order_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Treeview for order items
        columns = ("id", "product", "quantity", "price", "total")
        self.order_tree = ttk.Treeview(list_frame, columns=columns, show="headings", 
                                      yscrollcommand=scrollbar.set)
        
        # Configure columns
        self.order_tree.heading("id", text="ID")
        self.order_tree.heading("product", text="Product")
        self.order_tree.heading("quantity", text="Qty")
        self.order_tree.heading("price", text="Price")
        self.order_tree.heading("total", text="Total")
        
        self.order_tree.column("id", width=50)
        self.order_tree.column("product", width=150)
        self.order_tree.column("quantity", width=50)
        self.order_tree.column("price", width=80)
        self.order_tree.column("total", width=80)
        
        self.order_tree.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.order_tree.yview)
        
        # Remove item button
        remove_button = ttk.Button(order_frame, text="Remove Selected Item", command=self.remove_item)
        remove_button.pack(fill=tk.X, pady=(0, 10))
        
        # Total amount
        total_frame = ttk.Frame(order_frame)
        total_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(total_frame, text="Total Amount:", font=("Arial", 11, "bold")).pack(side=tk.LEFT)
        self.total_var = tk.StringVar(value="$0.00")
        ttk.Label(total_frame, textvariable=self.total_var, font=("Arial", 11, "bold")).pack(side=tk.RIGHT)
        
        # Complete order button
        complete_button = ttk.Button(order_frame, text="Complete Order", command=self.complete_order)
        complete_button.pack(fill=tk.X)
        
        # Initialize order items list and total
        self.order_items = []
        self.update_total()
    
    def create_orders_list_tab(self):
        """Create tab for viewing existing orders"""
        orders_frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(orders_frame, text="Orders List")
        
        # Filter frame
        filter_frame = ttk.Frame(orders_frame)
        filter_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Status filter
        ttk.Label(filter_frame, text="Status:").pack(side=tk.LEFT, padx=(0, 5))
        self.status_var = tk.StringVar()
        status_combobox = ttk.Combobox(filter_frame, textvariable=self.status_var, width=15,
                                      values=["", "Pending", "Completed", "Cancelled"])
        status_combobox.pack(side=tk.LEFT, padx=(0, 10))
        
        # Filter button
        filter_button = ttk.Button(filter_frame, text="Filter", command=self.load_orders)
        filter_button.pack(side=tk.LEFT)
        
        # Reset button
        reset_button = ttk.Button(filter_frame, text="Reset", command=self.reset_filters)
        reset_button.pack(side=tk.LEFT, padx=(5, 0))
        
        # Orders list
        list_frame = ttk.Frame(orders_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Treeview for orders
        columns = ("id", "date", "customer", "amount", "status")
        self.orders_tree = ttk.Treeview(list_frame, columns=columns, show="headings", 
                                       yscrollcommand=scrollbar.set)
        
        # Configure columns
        self.orders_tree.heading("id", text="Order ID")
        self.orders_tree.heading("date", text="Date")
        self.orders_tree.heading("customer", text="Customer")
        self.orders_tree.heading("amount", text="Amount")
        self.orders_tree.heading("status", text="Status")
        
        self.orders_tree.column("id", width=70)
        self.orders_tree.column("date", width=150)
        self.orders_tree.column("customer", width=150)
        self.orders_tree.column("amount", width=100)
        self.orders_tree.column("status", width=100)
        
        self.orders_tree.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.orders_tree.yview)
        
        # Bind double-click event
        self.orders_tree.bind("<Double-1>", self.view_order_details)
        
        # Buttons frame
        buttons_frame = ttk.Frame(orders_frame)
        buttons_frame.pack(fill=tk.X)
        
        # View details button
        view_button = ttk.Button(buttons_frame, text="View Details", command=self.view_order_details)
        view_button.pack(side=tk.LEFT)
        
        # Update status button
        update_button = ttk.Button(buttons_frame, text="Update Status", command=self.update_order_status)
        update_button.pack(side=tk.LEFT, padx=(5, 0))
        
        # Load orders
        self.load_orders()
    
    def load_customers(self):
        """Load customers for combobox"""
        self.db.connect()
        self.db.cursor.execute("SELECT id, name FROM customers ORDER BY name")
        customers = self.db.cursor.fetchall()
        self.db.disconnect()
        
        self.customers = {f"{c['name']} (ID: {c['id']})": c['id'] for c in customers}
        self.customer_combobox['values'] = list(self.customers.keys())
    
    def load_categories(self):
        """Load categories for combobox"""
        self.db.connect()
        self.db.cursor.execute("SELECT id, name FROM categories ORDER BY name")
        categories = self.db.cursor.fetchall()
        self.db.disconnect()
        
        self.categories = {c['name']: c['id'] for c in categories}
        category_names = [""] + list(self.categories.keys())
        self.category_combobox['values'] = category_names
    
    def load_products(self, category_id=None):
        """Load products for combobox, optionally filtered by category"""
        self.db.connect()
        if category_id:
            self.db.cursor.execute('''
            SELECT id, name, price, stock_quantity
            FROM products
            WHERE category_id = %s AND stock_quantity > 0
            ORDER BY name
            ''', (category_id,))
        else:
            self.db.cursor.execute('''
            SELECT id, name, price, stock_quantity
            FROM products
            WHERE stock_quantity > 0
            ORDER BY name
            ''')
        products = self.db.cursor.fetchall()
        self.db.disconnect()
        
        self.products = {p['name']: (p['id'], p['price'], p['stock_quantity']) for p in products}
        self.product_combobox['values'] = list(self.products.keys())
    
    def on_category_selected(self, event):
        """Handle category selection"""
        category_name = self.category_var.get()
        if category_name:
            category_id = self.categories.get(category_name)
            self.load_products(category_id)
        else:
            self.load_products()
        
        # Clear product selection
        self.product_var.set("")
        self.price_var.set("")
        self.stock_label.config(text="Available Stock: 0")
    
    def on_product_selected(self, event):
        """Handle product selection"""
        product_name = self.product_var.get()
        if product_name in self.products:
            product_id, price, stock = self.products[product_name]
            self.price_var.set(f"{price:.2f}")
            self.stock_label.config(text=f"Available Stock: {stock}")
        else:
            self.price_var.set("")
            self.stock_label.config(text="Available Stock: 0")
    
    def add_to_order(self):
        """Add product to order"""
        # Validate inputs
        product_name = self.product_var.get()
        if not product_name:
            messagebox.showerror("Error", "Please select a product")
            return
        
        if product_name not in self.products:
            messagebox.showerror("Error", "Invalid product selected")
            return
        
        try:
            quantity = int(self.quantity_var.get())
            if quantity <= 0:
                raise ValueError("Quantity must be positive")
        except ValueError:
            messagebox.showerror("Error", "Invalid quantity")
            return
        
        try:
            price = float(self.price_var.get())
            if price <= 0:
                raise ValueError("Price must be positive")
        except ValueError:
            messagebox.showerror("Error", "Invalid price")
            return
        
        # Check stock
        product_id, _, stock = self.products[product_name]
        if quantity > stock:
            messagebox.showerror("Error", f"Not enough stock. Available: {stock}")
            return
        
        # Add to order items
        total = quantity * price
        
        # Check if product already in order
        for i, item in enumerate(self.order_items):
            if item[0] == product_id:
                # Update quantity and total
                new_quantity = item[2] + quantity
                if new_quantity > stock:
                    messagebox.showerror("Error", f"Not enough stock. Available: {stock}")
                    return
                
                new_total = new_quantity * price
                self.order_items[i] = (product_id, product_name, new_quantity, price, new_total)
                
                # Update treeview
                for child in self.order_tree.get_children():
                    if self.order_tree.item(child)['values'][0] == product_id:
                        self.order_tree.item(child, values=(
                            product_id, product_name, new_quantity, 
                            format_currency(price), format_currency(new_total)
                        ))
                        break
                
                self.update_total()
                return
        
        # Add new item
        self.order_items.append((product_id, product_name, quantity, price, total))
        
        # Add to treeview
        self.order_tree.insert("", "end", values=(
            product_id, product_name, quantity, 
            format_currency(price), format_currency(total)
        ))
        
        # Update total
        self.update_total()
        
        # Reset quantity
        self.quantity_var.set("1")
    
    def remove_item(self):
        """Remove selected item from order"""
        selected_items = self.order_tree.selection()
        if not selected_items:
            messagebox.showinfo("Info", "Please select an item to remove")
            return
        
        # Get the selected item
        item = self.order_tree.item(selected_items[0])
        product_id = item['values'][0]
        
        # Remove from order items
        self.order_items = [i for i in self.order_items if i[0] != product_id]
        
        # Remove from treeview
        self.order_tree.delete(selected_items[0])
        
        # Update total
        self.update_total()
    
    def update_total(self):
        """Update total amount"""
        total = sum(item[4] for item in self.order_items)
        self.total_var.set(format_currency(total))
    
    def complete_order(self):
        """Complete the order and save to database"""
        # Validate customer
        customer_selection = self.customer_var.get()
        if not customer_selection or customer_selection not in self.customers:
            messagebox.showerror("Error", "Please select a valid customer")
            return
        
        # Validate order items
        if not self.order_items:
            messagebox.showerror("Error", "Please add at least one product to the order")
            return
        
        # Get customer ID
        customer_id = self.customers[customer_selection]
        
        # Calculate total
        total_amount = sum(item[4] for item in self.order_items)
        
        try:
            # Create order
            self.db.connect()
            
            # Insert order
            self.db.cursor.execute('''
            INSERT INTO orders (customer_id, total_amount, status)
            VALUES (%s, %s, %s)
            ''', (customer_id, total_amount, "Pending"))
            
            order_id = self.db.cursor.lastrowid
            
            # Insert order items
            for product_id, _, quantity, price, _ in self.order_items:
                self.db.cursor.execute('''
                INSERT INTO order_items (order_id, product_id, quantity, price)
                VALUES (%s, %s, %s, %s)
                ''', (order_id, product_id, quantity, price))
                
                # Update product stock
                self.db.cursor.execute('''
                UPDATE products
                SET stock_quantity = stock_quantity - %s
                WHERE id = %s
                ''', (quantity, product_id))
            
            self.db.conn.commit()
            self.db.disconnect()
            
            messagebox.showinfo("Success", f"Order #{order_id} created successfully")
            
            # Clear form
            self.customer_var.set("")
            self.product_var.set("")
            self.category_var.set("")
            self.price_var.set("")
            self.quantity_var.set("1")
            self.stock_label.config(text="Available Stock: 0")
            
            # Clear order items
            for item in self.order_tree.get_children():
                self.order_tree.delete(item)
            
            self.order_items = []
            self.update_total()
            
            # Reload products (stock has changed)
            self.load_products()
            
            # Switch to orders tab
            self.notebook.select(1)  # Select the second tab (Orders List)
            self.load_orders()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create order: {e}")
    
    def load_orders(self):
        """Load orders into the treeview"""
        # Clear existing items
        for item in self.orders_tree.get_children():
            self.orders_tree.delete(item)
        
        # Get status filter
        status = self.status_var.get()
        
        # Get orders from database
        orders = self.db.get_all_orders(status if status else None)
        
        # Insert orders into treeview
        for order in orders:
            self.orders_tree.insert("", "end", values=(
                order['id'],
                format_date(order['order_date']),
                order['customer_name'] or "Unknown",
                format_currency(order['total_amount']),
                order['status']
            ))
    
    def reset_filters(self):
        """Reset filters and reload orders"""
        self.status_var.set("")
        self.load_orders()
    
    def view_order_details(self, event=None):
        """View details of selected order"""
        selected_items = self.orders_tree.selection()
        if not selected_items:
            messagebox.showinfo("Info", "Please select an order to view")
            return
        
        # Get the selected order ID
        item = self.orders_tree.item(selected_items[0])
        order_id = item['values'][0]
        
        # Get order details
        order, order_items = self.db.get_order_details(order_id)
        
        if not order:
            messagebox.showerror("Error", "Order not found")
            return
        
        # Create details window
        details_window = tk.Toplevel(self.parent)
        details_window.title(f"Order #{order_id} Details")
        details_window.geometry("600x500")
        details_window.minsize(500, 400)
        details_window.transient(self.parent)
        details_window.grab_set()
        
        # Order info frame
        info_frame = ttk.LabelFrame(details_window, text="Order Information", padding=10)
        info_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Order ID
        ttk.Label(info_frame, text="Order ID:").grid(row=0, column=0, sticky="w", pady=2)
        ttk.Label(info_frame, text=str(order['id'])).grid(row=0, column=1, sticky="w", pady=2)
        
        # Order Date
        ttk.Label(info_frame, text="Order Date:").grid(row=1, column=0, sticky="w", pady=2)
        ttk.Label(info_frame, text=format_date(order['order_date'])).grid(row=1, column=1, sticky="w", pady=2)
        
        # Customer
        ttk.Label(info_frame, text="Customer:").grid(row=2, column=0, sticky="w", pady=2)
        ttk.Label(info_frame, text=order['customer_name'] or "Unknown").grid(row=2, column=1, sticky="w", pady=2)
        
        # Status
        ttk.Label(info_frame, text="Status:").grid(row=3, column=0, sticky="w", pady=2)
        ttk.Label(info_frame, text=order['status']).grid(row=3, column=1, sticky="w", pady=2)
        
        # Total Amount
        ttk.Label(info_frame, text="Total Amount:").grid(row=4, column=0, sticky="w", pady=2)
        ttk.Label(info_frame, text=format_currency(order['total_amount'])).grid(row=4, column=1, sticky="w", pady=2)
        
        # Items frame
        items_frame = ttk.LabelFrame(details_window, text="Order Items", padding=10)
        items_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(items_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Treeview for order items
        columns = ("id", "product", "quantity", "price", "total")
        items_tree = ttk.Treeview(items_frame, columns=columns, show="headings", 
                                 yscrollcommand=scrollbar.set)
        
        # Configure columns
        items_tree.heading("id", text="ID")
        items_tree.heading("product", text="Product")
        items_tree.heading("quantity", text="Qty")
        items_tree.heading("price", text="Price")
        items_tree.heading("total", text="Total")
        
        items_tree.column("id", width=50)
        items_tree.column("product", width=200)
        items_tree.column("quantity", width=50)
        items_tree.column("price", width=80)
        items_tree.column("total", width=80)
        
        items_tree.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=items_tree.yview)
        
        # Insert items
        for item in order_items:
            total = item['quantity'] * item['price']
            items_tree.insert("", "end", values=(
                item['product_id'],
                item['product_name'],
                item['quantity'],
                format_currency(item['price']),
                format_currency(total)
            ))
        
        # Close button
        close_button = ttk.Button(details_window, text="Close", command=details_window.destroy)
        close_button.pack(pady=10)
    
    def update_order_status(self):
        """Update status of selected order"""
        selected_items = self.orders_tree.selection()
        if not selected_items:
            messagebox.showinfo("Info", "Please select an order to update")
            return
        
        # Get the selected order ID
        item = self.orders_tree.item(selected_items[0])
        order_id = item['values'][0]
        current_status = item['values'][4]
        
        # Create status window
        status_window = tk.Toplevel(self.parent)
        status_window.title(f"Update Order #{order_id} Status")
        status_window.geometry("300x150")
        status_window.minsize(300, 150)
        status_window.transient(self.parent)
        status_window.grab_set()
        
        # Status frame
        status_frame = ttk.Frame(status_window, padding=20)
        status_frame.pack(fill=tk.BOTH, expand=True)
        
        # Status label
                # Status label
        ttk.Label(status_frame, text="Update Status:").grid(row=0, column=0, sticky="w", pady=10)
        
        # Status combobox
        status_var = tk.StringVar(value=current_status)
        status_combobox = ttk.Combobox(status_frame, textvariable=status_var, width=15,
                                      values=["Pending", "Completed", "Cancelled"])
        status_combobox.grid(row=0, column=1, sticky="ew", pady=10)
        
        # Update button
        def update_status():
            new_status = status_var.get()
            if new_status != current_status:
                try:
                    self.db.update_order_status(order_id, new_status)
                    messagebox.showinfo("Success", f"Order status updated to {new_status}")
                    status_window.destroy()
                    self.load_orders()
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to update status: {e}")
            else:
                status_window.destroy()
        
        update_button = ttk.Button(status_frame, text="Update", command=update_status)
        update_button.grid(row=1, column=0, pady=10)
        
        # Cancel button
        cancel_button = ttk.Button(status_frame, text="Cancel", command=status_window.destroy)
        cancel_button.grid(row=1, column=1, pady=10)
        
        # Configure grid weights
        status_frame.grid_columnconfigure(0, weight=1)
        status_frame.grid_columnconfigure(1, weight=1)
