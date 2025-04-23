        # Average order value
        ttk.Label(summary_frame, text="Average Order Value:", font=("Arial", 11)).pack(side=tk.LEFT)
        self.avg_order_var = tk.StringVar(value="$0.00")
        ttk.Label(summary_frame, textvariable=self.avg_order_var, font=("Arial", 11)).pack(side=tk.LEFT, padx=(5, 0))
        
        # Set default date range to this month
        self.set_date_range("this_month")
    
    def create_product_sales_tab(self):
        """Create tab for product sales reports"""
        product_sales_frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(product_sales_frame, text="Product Sales")
        
        # Date range frame
        date_frame = ttk.LabelFrame(product_sales_frame, text="Date Range", padding=10)
        date_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Start date
        ttk.Label(date_frame, text="Start Date:").grid(row=0, column=0, sticky="w", pady=5)
        self.prod_start_date_var = tk.StringVar()
        start_date_entry = ttk.Entry(date_frame, textvariable=self.prod_start_date_var, width=15)
        start_date_entry.grid(row=0, column=1, sticky="w", pady=5)
        
        # End date
        ttk.Label(date_frame, text="End Date:").grid(row=0, column=2, sticky="w", pady=5, padx=(20, 0))
        self.prod_end_date_var = tk.StringVar()
        end_date_entry = ttk.Entry(date_frame, textvariable=self.prod_end_date_var, width=15)
        end_date_entry.grid(row=0, column=3, sticky="w", pady=5)
        
        # Date presets
        preset_frame = ttk.Frame(date_frame)
        preset_frame.grid(row=1, column=0, columnspan=4, sticky="w", pady=5)
        
        ttk.Button(preset_frame, text="Today", command=lambda: self.set_product_date_range("today")).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(preset_frame, text="This Week", command=lambda: self.set_product_date_range("this_week")).pack(side=tk.LEFT, padx=5)
        ttk.Button(preset_frame, text="This Month", command=lambda: self.set_product_date_range("this_month")).pack(side=tk.LEFT, padx=5)
        ttk.Button(preset_frame, text="Last Month", command=lambda: self.set_product_date_range("last_month")).pack(side=tk.LEFT, padx=5)
        
        # Category filter
        ttk.Label(date_frame, text="Category:").grid(row=2, column=0, sticky="w", pady=5)
        self.prod_category_var = tk.StringVar()
        self.prod_category_combobox = ttk.Combobox(date_frame, textvariable=self.prod_category_var, width=15)
        self.prod_category_combobox.grid(row=2, column=1, sticky="w", pady=5)
        
        # Load categories
        self.load_categories_for_report()
        
        # Generate button
        generate_button = ttk.Button(date_frame, text="Generate Report", command=self.generate_product_sales_report)
        generate_button.grid(row=3, column=0, columnspan=2, pady=10)
        
        # Export button
        export_button = ttk.Button(date_frame, text="Export to CSV", command=lambda: self.export_to_csv("product_sales"))
        export_button.grid(row=3, column=2, columnspan=2, pady=10)
        
        # Report results
        report_frame = ttk.LabelFrame(product_sales_frame, text="Report Results", padding=10)
        report_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(report_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Treeview for product sales report
        columns = ("id", "name", "category", "quantity", "revenue")
        self.product_sales_tree = ttk.Treeview(report_frame, columns=columns, show="headings", 
                                             yscrollcommand=scrollbar.set)
        
        # Configure columns
        self.product_sales_tree.heading("id", text="ID")
        self.product_sales_tree.heading("name", text="Product Name")
        self.product_sales_tree.heading("category", text="Category")
        self.product_sales_tree.heading("quantity", text="Quantity Sold")
        self.product_sales_tree.heading("revenue", text="Revenue")
        
        self.product_sales_tree.column("id", width=50)
        self.product_sales_tree.column("name", width=200)
        self.product_sales_tree.column("category", width=100)
        self.product_sales_tree.column("quantity", width=100)
        self.product_sales_tree.column("revenue", width=100)
        
        self.product_sales_tree.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.product_sales_tree.yview)
        
        # Set default date range to this month
        self.set_product_date_range("this_month")
    
    def create_inventory_report_tab(self):
        """Create tab for inventory reports"""
        inventory_frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(inventory_frame, text="Inventory Report")
        
        # Filter frame
        filter_frame = ttk.LabelFrame(inventory_frame, text="Filters", padding=10)
        filter_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Category filter
        ttk.Label(filter_frame, text="Category:").grid(row=0, column=0, sticky="w", pady=5)
        self.inv_category_var = tk.StringVar()
        self.inv_category_combobox = ttk.Combobox(filter_frame, textvariable=self.inv_category_var, width=15)
        self.inv_category_combobox.grid(row=0, column=1, sticky="w", pady=5)
        
        # Stock filter
        ttk.Label(filter_frame, text="Stock Status:").grid(row=0, column=2, sticky="w", pady=5, padx=(20, 0))
        self.stock_status_var = tk.StringVar()
        self.stock_status_combobox = ttk.Combobox(filter_frame, textvariable=self.stock_status_var, width=15,
                                                values=["All", "In Stock", "Low Stock", "Out of Stock"])
        self.stock_status_combobox.grid(row=0, column=3, sticky="w", pady=5)
        self.stock_status_combobox.current(0)
        
        # Low stock threshold
        ttk.Label(filter_frame, text="Low Stock Threshold:").grid(row=1, column=0, sticky="w", pady=5)
        self.inv_threshold_var = tk.StringVar(value="10")
        threshold_entry = ttk.Entry(filter_frame, textvariable=self.inv_threshold_var, width=10)
        threshold_entry.grid(row=1, column=1, sticky="w", pady=5)
        
        # Generate button
        generate_button = ttk.Button(filter_frame, text="Generate Report", command=self.generate_inventory_report)
        generate_button.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Export button
        export_button = ttk.Button(filter_frame, text="Export to CSV", command=lambda: self.export_to_csv("inventory"))
        export_button.grid(row=2, column=2, columnspan=2, pady=10)
        
        # Report results
        report_frame = ttk.LabelFrame(inventory_frame, text="Report Results", padding=10)
        report_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(report_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Treeview for inventory report
        columns = ("id", "name", "category", "stock", "value")
        self.inventory_tree = ttk.Treeview(report_frame, columns=columns, show="headings", 
                                          yscrollcommand=scrollbar.set)
        
        # Configure columns
        self.inventory_tree.heading("id", text="ID")
        self.inventory_tree.heading("name", text="Product Name")
        self.inventory_tree.heading("category", text="Category")
        self.inventory_tree.heading("stock", text="Stock")
        self.inventory_tree.heading("value", text="Inventory Value")
        
        self.inventory_tree.column("id", width=50)
        self.inventory_tree.column("name", width=200)
        self.inventory_tree.column("category", width=100)
        self.inventory_tree.column("stock", width=80)
        self.inventory_tree.column("value", width=120)
        
        self.inventory_tree.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.inventory_tree.yview)
        
        # Summary frame
        summary_frame = ttk.Frame(report_frame)
        summary_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Total inventory value
        ttk.Label(summary_frame, text="Total Inventory Value:", font=("Arial", 11, "bold")).pack(side=tk.LEFT)
        self.total_inventory_var = tk.StringVar(value="$0.00")
        ttk.Label(summary_frame, textvariable=self.total_inventory_var, font=("Arial", 11, "bold")).pack(side=tk.LEFT, padx=(5, 20))
        
        # Total products
        ttk.Label(summary_frame, text="Total Products:", font=("Arial", 11)).pack(side=tk.LEFT)
        self.total_products_var = tk.StringVar(value="0")
        ttk.Label(summary_frame, textvariable=self.total_products_var, font=("Arial", 11)).pack(side=tk.LEFT, padx=(5, 0))
        
        # Load categories
        self.load_categories_for_report()
        
        # Generate report on load
        self.generate_inventory_report()
    
    def load_categories_for_report(self):
        """Load categories for report filters"""
        self.db.connect()
        self.db.cursor.execute("SELECT id, name FROM categories ORDER BY name")
        categories = self.db.cursor.fetchall()
        self.db.disconnect()
        
        self.categories = {c['name']: c['id'] for c in categories}
        category_names = ["All Categories"] + list(self.categories.keys())
        
        self.prod_category_combobox['values'] = category_names
        self.prod_category_combobox.current(0)
        
        self.inv_category_combobox['values'] = category_names
        self.inv_category_combobox.current(0)
    
    def set_date_range(self, preset):
        """Set date range based on preset"""
        today = datetime.now().date()
        
        if preset == "today":
            start_date = today
            end_date = today
        elif preset == "yesterday":
            yesterday = today - timedelta(days=1)
            start_date = yesterday
            end_date = yesterday
        elif preset == "this_week":
            start_date = today - timedelta(days=today.weekday())
            end_date = today
        elif preset == "last_week":
            start_date = today - timedelta(days=today.weekday() + 7)
            end_date = start_date + timedelta(days=6)
        elif preset == "this_month":
            start_date = today.replace(day=1)
            end_date = today
        elif preset == "last_month":
            last_month = today.month - 1 if today.month > 1 else 12
            last_month_year = today.year if today.month > 1 else today.year - 1
            last_month_days = 31  # Simplified approach
            start_date = datetime(last_month_year, last_month, 1).date()
            end_date = datetime(last_month_year, last_month, last_month_days).date()
            # Adjust if the day doesn't exist in that month
            while True:
                try:
                    end_date = datetime(last_month_year, last_month, last_month_days).date()
                    break
                except ValueError:
                    last_month_days -= 1
        
        self.start_date_var.set(start_date.strftime("%Y-%m-%d"))
        self.end_date_var.set(end_date.strftime("%Y-%m-%d"))
        
        # Generate report with new date range
        self.generate_sales_report()
    
    def set_product_date_range(self, preset):
        """Set date range for product sales report based on preset"""
        today = datetime.now().date()
        
        if preset == "today":
            start_date = today
            end_date = today
        elif preset == "this_week":
            start_date = today - timedelta(days=today.weekday())
            end_date = today
        elif preset == "this_month":
            start_date = today.replace(day=1)
            end_date = today
        elif preset == "last_month":
            last_month = today.month - 1 if today.month > 1 else 12
            last_month_year = today.year if today.month > 1 else today.year - 1
            last_month_days = 31  # Simplified approach
            start_date = datetime(last_month_year, last_month, 1).date()
            end_date = datetime(last_month_year, last_month, last_month_days).date()
            # Adjust if the day doesn't exist in that month
            while True:
                try:
                    end_date = datetime(last_month_year, last_month, last_month_days).date()
                    break
                except ValueError:
                    last_month_days -= 1
        
        self.prod_start_date_var.set(start_date.strftime("%Y-%m-%d"))
        self.prod_end_date_var.set(end_date.strftime("%Y-%m-%d"))
        
        # Generate report with new date range
        self.generate_product_sales_report()
    
    def generate_sales_report(self):
        """Generate sales report based on date range"""
        # Clear existing items
        for item in self.sales_tree.get_children():
            self.sales_tree.delete(item)
        
        # Validate date range
        try:
            start_date = datetime.strptime(self.start_date_var.get(), "%Y-%m-%d").date()
            end_date = datetime.strptime(self.end_date_var.get(), "%Y-%m-%d").date()
            
            if start_date > end_date:
                raise ValueError("Start date cannot be after end date")
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid date format: {e}")
            return
        
        # Get orders within date range
        self.db.connect()
        self.db.cursor.execute('''
        SELECT o.id, o.order_date, o.total_amount, o.status, c.name as customer_name
        FROM orders o
        LEFT JOIN customers c ON o.customer_id = c.id
        WHERE DATE(o.order_date) BETWEEN %s AND %s
        ORDER BY o.order_date DESC
        ''', (start_date, end_date))
        orders = self.db.cursor.fetchall()
        self.db.disconnect()
        
        # Insert orders into treeview
        total_sales = 0
        for order in orders:
            self.sales_tree.insert("", "end", values=(
                order['id'],
                format_date(order['order_date']),
                order['customer_name'] or "Unknown",
                format_currency(order['total_amount']),
                order['status']
            ))
            
            # Add to total if order is completed
            if order['status'] == "Completed":
                total_sales += order['total_amount']
        
        # Update summary
        self.total_sales_var.set(format_currency(total_sales))
        self.order_count_var.set(str(len(orders)))
        
        # Calculate average order value
        avg_order = total_sales / len(orders) if orders else 0
        self.avg_order_var.set(format_currency(avg_order))
    
    def generate_product_sales_report(self):
        """Generate product sales report based on date range and category"""
        # Clear existing items
        for item in self.product_sales_tree.get_children():
            self.product_sales_tree.delete(item)
        
        # Validate date range
        try:
            start_date = datetime.strptime(self.prod_start_date_var.get(), "%Y-%m-%d").date()
            end_date = datetime.strptime(self.prod_end_date_var.get(), "%Y-%m-%d").date()
            
            if start_date > end_date:
                raise ValueError("Start date cannot be after end date")
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid date format: {e}")
            return
        
        # Get category filter
        category = self.prod_category_var.get()
        category_id = self.categories.get(category) if category != "All Categories" else None
        
        # Get product sales within date range
        self.db.connect()
        
        if category_id:
            self.db.cursor.execute('''
            SELECT p.id, p.name, c.name as category_name, 
                   SUM(oi.quantity) as total_quantity,
                   SUM(oi.quantity * oi.price) as total_revenue
            FROM order_items oi
            JOIN orders o ON oi.order_id = o.id
            JOIN products p ON oi.product_id = p.id
            LEFT JOIN categories c ON p.category_id = c.id
            WHERE DATE(o.order_date) BETWEEN %s AND %s
            AND p.category_id = %s
            AND o.status = 'Completed'
            GROUP BY p.id
            ORDER BY total_revenue DESC
            ''', (start_date, end_date, category_id))
        else:
            self.db.cursor.execute('''
            SELECT p.id, p.name, c.name as category_name, 
                   SUM(oi.quantity) as total_quantity,
                   SUM(oi.quantity * oi.price) as total_revenue
            FROM order_items oi
            JOIN orders o ON oi.order_id = o.id
            JOIN products p ON oi.product_id = p.id
            LEFT JOIN categories c ON p.category_id = c.id
            WHERE DATE(o.order_date) BETWEEN %s AND %s
            AND o.status = 'Completed'
            GROUP BY p.id
            ORDER BY total_revenue DESC
            ''', (start_date, end_date))
        
        products = self.db.cursor.fetchall()
        self.db.disconnect()
        
        # Insert products into treeview
        for product in products:
            self.product_sales_tree.insert("", "end", values=(
                product['id'],
                product['name'],
                product['category_name'] or "Uncategorized",
                product['total_quantity'],
                format_currency(product['total_revenue'])
            ))
    
    def generate_inventory_report(self):
        """Generate inventory report based on filters"""
        # Clear existing items
        for item in self.inventory_tree.get_children():
            self.inventory_tree.delete(item)
        
        # Get filters
        category = self.inv_category_var.get()
        category_id = self.categories.get(category) if category != "All Categories" else None
        
        stock_status = self.stock_status_var.get()
        
        try:
            threshold = int(self.inv_threshold_var.get())
            if threshold < 0:
                raise ValueError("Threshold must be positive")
        except ValueError:
            messagebox.showerror("Error", "Invalid threshold")
            return
        
        # Get inventory data
        self.db.connect()
        
        query = '''
        SELECT p.id, p.name, p.price, p.stock_quantity, c.name as category_name
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.id
        '''
        
        params = []
        where_clauses = []
        
        if category_id:
            where_clauses.append("p.category_id = %s")
            params.append(category_id)
        
        if stock_status == "In Stock":
            where_clauses.append("p.stock_quantity > 0")
        elif stock_status == "Low Stock":
            where_clauses.append("p.stock_quantity > 0 AND p.stock_quantity <= %s")
            params.append(threshold)
        elif stock_status == "Out of Stock":
            where_clauses.append("p.stock_quantity = 0")
        
        if where_clauses:
            query += " WHERE " + " AND ".join(where_clauses)
        
        query += " ORDER BY p.name"
        
        self.db.cursor.execute(query, params)
        products = self.db.cursor.fetchall()
        self.db.disconnect()
        
        # Insert products into treeview
        total_value = 0
        for product in products:
            inventory_value = product['price'] * product['stock_quantity']
            total_value += inventory_value
            
            self.inventory_tree.insert("", "end", values=(
                product['id'],
                product['name'],
                product['category_name'] or "Uncategorized",
                product['stock_quantity'],
                format_currency(inventory_value)
            ))
        
        # Update summary
        self.total_inventory_var.set(format_currency(total_value))
        self.total_products_var.set(str(len(products)))
    
    def export_to_csv(self, report_type):
        """Export report data to CSV file"""
        # Determine which report to export
        if report_type == "sales":
            tree = self.sales_tree
            filename = f"sales_report_{self.start_date_var.get()}_to_{self.end_date_var.get()}.csv"
            headers = ["Order ID", "Date", "Customer", "Amount", "Status"]
        elif report_type == "product_sales":
            tree = self.product_sales_tree
            filename = f"product_sales_{self.prod_start_date_var.get()}_to_{self.prod_end_date_var.get()}.csv"
            headers = ["Product ID", "Product Name", "Category", "Quantity Sold", "Revenue"]
        elif report_type == "inventory":
            tree = self.inventory_tree
            filename = f"inventory_report_{datetime.now().strftime('%Y-%m-%d')}.csv"
            headers = ["Product ID", "Product Name", "Category", "Stock", "Inventory Value"]
        else:
            messagebox.showerror("Error", "Invalid report type")
            return
        
        # Check if there's data to export
        if not tree.get_children():
            messagebox.showinfo("Info", "No data to export")
            return
        
        # Ask for save location
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            initialfile=filename
        )
        
        if not file_path:
            return  # User cancelled
        
        try:
            with open(file_path, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                
                # Write headers
                writer.writerow(headers)
                
                # Write data
                for item_id in tree.get_children():
                    values = tree.item(item_id)['values']
                    writer.writerow(values)
            
            messagebox.showinfo("Success", f"Report exported to {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export report: {e}")
