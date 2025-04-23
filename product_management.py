import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
from src.models import Product, Category
from src.utils import load_image, format_currency

class ProductManagement:
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        
        # Create main frame
        self.frame = ttk.Frame(parent)
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(self.frame, text="Product Management", font=("Arial", 16, "bold"))
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
        
        # Create product list (left side)
        self.create_product_list(left_frame)
        
        # Create product form (right side)
        self.create_product_form(right_frame)
        
        # Load products
        self.load_products()
        
        # Load categories for the form
        self.load_categories()
    
    def create_product_list(self, parent):
        """Create the product list with search and filter options"""
        # Search and filter frame
        filter_frame = ttk.Frame(parent)
        filter_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Search
        ttk.Label(filter_frame, text="Search:").pack(side=tk.LEFT, padx=(0, 5))
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(filter_frame, textvariable=self.search_var, width=20)
        search_entry.pack(side=tk.LEFT, padx=(0, 10))
        
        # Category filter
        ttk.Label(filter_frame, text="Category:").pack(side=tk.LEFT, padx=(0, 5))
        self.category_filter_var = tk.StringVar()
        self.category_filter = ttk.Combobox(filter_frame, textvariable=self.category_filter_var, width=15)
        self.category_filter.pack(side=tk.LEFT, padx=(0, 10))
        
        # Search button
        search_button = ttk.Button(filter_frame, text="Search", command=self.load_products)
        search_button.pack(side=tk.LEFT)
        
        # Reset button
        reset_button = ttk.Button(filter_frame, text="Reset", command=self.reset_filters)
        reset_button.pack(side=tk.LEFT, padx=(5, 0))
        
        # Product list
        list_frame = ttk.Frame(parent)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Treeview for products
        columns = ("id", "name", "category", "price", "stock")
        self.product_tree = ttk.Treeview(list_frame, columns=columns, show="headings", 
                                        yscrollcommand=scrollbar.set)
        
        # Configure columns
        self.product_tree.heading("id", text="ID")
        self.product_tree.heading("name", text="Product Name")
        self.product_tree.heading("category", text="Category")
        self.product_tree.heading("price", text="Price")
        self.product_tree.heading("stock", text="Stock")
        
        self.product_tree.column("id", width=50)
        self.product_tree.column("name", width=150)
        self.product_tree.column("category", width=100)
        self.product_tree.column("price", width=80)
        self.product_tree.column("stock", width=80)
        
        self.product_tree.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.product_tree.yview)
        
        # Bind select event
        self.product_tree.bind("<<TreeviewSelect>>", self.on_product_select)
        
        # Buttons frame
        buttons_frame = ttk.Frame(parent)
        buttons_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Add button
        add_button = ttk.Button(buttons_frame, text="Add New Product", command=self.add_new_product)
        add_button.pack(side=tk.LEFT)
        
        # Delete button
        delete_button = ttk.Button(buttons_frame, text="Delete Product", command=self.delete_product)
        delete_button.pack(side=tk.LEFT, padx=(5, 0))
    
    def create_product_form(self, parent):
        """Create the product form for adding/editing products"""
        # Form frame
        form_frame = ttk.LabelFrame(parent, text="Product Details", padding=10)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Product ID (hidden)
        self.product_id_var = tk.StringVar()
        
        # Product Name
        ttk.Label(form_frame, text="Product Name:").grid(row=0, column=0, sticky="w", pady=5)
        self.name_var = tk.StringVar()
        name_entry = ttk.Entry(form_frame, textvariable=self.name_var, width=30)
        name_entry.grid(row=0, column=1, sticky="ew", pady=5)
        
        # Category
        ttk.Label(form_frame, text="Category:").grid(row=1, column=0, sticky="w", pady=5)
        self.category_var = tk.StringVar()
        self.category_combobox = ttk.Combobox(form_frame, textvariable=self.category_var, width=28)
        self.category_combobox.grid(row=1, column=1, sticky="ew", pady=5)
        
        # Price
        ttk.Label(form_frame, text="Price ($):").grid(row=2, column=0, sticky="w", pady=5)
        self.price_var = tk.StringVar()
        price_entry = ttk.Entry(form_frame, textvariable=self.price_var, width=30)
        price_entry.grid(row=2, column=1, sticky="ew", pady=5)
        
        # Stock Quantity
        ttk.Label(form_frame, text="Stock Quantity:").grid(row=3, column=0, sticky="w", pady=5)
        self.stock_var = tk.StringVar()
        stock_entry = ttk.Entry(form_frame, textvariable=self.stock_var, width=30)
        stock_entry.grid(row=3, column=1, sticky="ew", pady=5)
        
        # Description
        ttk.Label(form_frame, text="Description:").grid(row=4, column=0, sticky="nw", pady=5)
        self.description_text = tk.Text(form_frame, width=30, height=5)
        self.description_text.grid(row=4, column=1, sticky="ew", pady=5)
        
        # Product Image
        ttk.Label(form_frame, text="Product Image:").grid(row=5, column=0, sticky="w", pady=5)
        image_frame = ttk.Frame(form_frame)
        image_frame.grid(row=5, column=1, sticky="ew", pady=5)
        
        self.image_path_var = tk.StringVar()
        self.image_label = ttk.Label(image_frame, text="No image selected")
        self.image_label.pack(side=tk.LEFT)
        
        browse_button = ttk.Button(image_frame, text="Browse...", command=self.browse_image)
        browse_button.pack(side=tk.LEFT, padx=(5, 0))
        
        # Image preview
        self.image_preview = ttk.Label(form_frame)
        self.image_preview.grid(row=6, column=0, columnspan=2, pady=10)
        
        # Save button
        save_button = ttk.Button(form_frame, text="Save Product", command=self.save_product)
        save_button.grid(row=7, column=0, columnspan=2, pady=10)
        
        # Configure grid weights
        form_frame.grid_columnconfigure(1, weight=1)
    
    def load_products(self):
        """Load products into the treeview"""
        # Clear existing items
        for item in self.product_tree.get_children():
            self.product_tree.delete(item)
        
        # Get filter values
        search_term = self.search_var.get()
        category_filter = self.category_filter_var.get()
        
        # Get products from database
        self.db.connect()
        
        if category_filter:
            # Get category ID
            self.db.cursor.execute("SELECT id FROM categories WHERE name = %s", (category_filter,))
            category_id = self.db.cursor.fetchone()
            
            if category_id:
                category_id = category_id['id']
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
            else:
                self.db.cursor.execute('''
                SELECT p.id, p.name, p.price, p.stock_quantity, c.name as category_name
                FROM products p
                LEFT JOIN categories c ON p.category_id = c.id
                ORDER BY p.name
                ''')
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
            self.product_tree.insert("", "end", values=(
                product['id'],
                product['name'],
                product['category_name'] or "Uncategorized",
                format_currency(product['price']),
                product['stock_quantity']
            ))
    
    def load_categories(self):
        """Load categories for comboboxes"""
        self.db.connect()
        self.db.cursor.execute("SELECT name FROM categories ORDER BY name")
        categories = self.db.cursor.fetchall()
        self.db.disconnect()
        
        category_names = [""] + [category['name'] for category in categories]
        self.category_combobox['values'] = category_names
        self.category_filter['values'] = category_names
    
    def reset_filters(self):
        """Reset search and filter fields"""
        self.search_var.set("")
        self.category_filter_var.set("")
        self.load_products()
    
    def on_product_select(self, event):
        """Handle product selection in treeview"""
        selected_items = self.product_tree.selection()
        if not selected_items:
            return
        
        # Get the selected product ID
        item = self.product_tree.item(selected_items[0])
        product_id = item['values'][0]
        
        # Load product details
        self.db.connect()
        self.db.cursor.execute('''
        SELECT p.*, c.name as category_name
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.id
        WHERE p.id = %s
        ''', (product_id,))
        product = self.db.cursor.fetchone()
        self.db.disconnect()
        
        if not product:
            return
        
        # Update form fields
        self.product_id_var.set(product['id'])
        self.name_var.set(product['name'])
        self.category_var.set(product['category_name'] or "")
        self.price_var.set(product['price'])
        self.stock_var.set(product['stock_quantity'])
        
        # Update description
        self.description_text.delete(1.0, tk.END)
        if product['description']:
            self.description_text.insert(tk.END, product['description'])
        
        # Update image
        self.image_path_var.set(product['image_path'] or "")
        if product['image_path'] and os.path.exists(product['image_path']):
            self.image_label.config(text=os.path.basename(product['image_path']))
            self.display_image(product['image_path'])
        else:
            self.image_label.config(text="No image selected")
            self.image_preview.config(image=None, text="No image")
    
    def add_new_product(self):
        """Clear form for adding a new product"""
        self.product_id_var.set("")
        self.name_var.set("")
        self.category_var.set("")
        self.price_var.set("")
        self.stock_var.set("")
        self.description_text.delete(1.0, tk.END)
        self.image_path_var.set("")
        self.image_label.config(text="No image selected")
        self.image_preview.config(image=None, text="No image")
    
    def browse_image(self):
        """Open file dialog to select product image"""
        filetypes = [("Image files", "*.png *.jpg *.jpeg *.gif")]
        image_path = filedialog.askopenfilename(filetypes=filetypes)
        
        if image_path:
            # Create product_images directory if it doesn't exist
            images_dir = os.path.join(os.getcwd(), "images", "product_images")
            os.makedirs(images_dir, exist_ok=True)
            
            # Copy image to product_images directory
            filename = os.path.basename(image_path)
            new_path = os.path.join(images_dir, filename)
            
            # If file already exists, add a timestamp to make it unique
            if os.path.exists(new_path) and image_path != new_path:
                import time
                name, ext = os.path.splitext(filename)
                filename = f"{name}_{int(time.time())}{ext}"
                new_path = os.path.join(images_dir, filename)
            
            # Only copy if it's not already in the right location
            if image_path != new_path:
                import shutil
                shutil.copy2(image_path, new_path)
            
            self.image_path_var.set(new_path)
            self.image_label.config(text=filename)
            self.display_image(new_path)
    
    def display_image(self, image_path):
        """Display image in the preview label"""
        try:
            img = Image.open(image_path)
            img = img.resize((150, 150), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            self.image_preview.config(image=photo, text="")
            self.image_preview.image = photo  # Keep a reference
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image: {e}")
            self.image_preview.config(image=None, text="Failed to load image")
    
    def save_product(self):
        """Save product to database"""
        # Validate form
        name = self.name_var.get().strip()
        category = self.category_var.get().strip()
        price_str = self.price_var.get().strip()
        stock_str = self.stock_var.get().strip()
        description = self.description_text.get(1.0, tk.END).strip()
        image_path = self.image_path_var.get()
        
        # Basic validation
        if not name:
            messagebox.showerror("Error", "Product name is required")
            return
        
        try:
            price = float(price_str)
            if price < 0:
                raise ValueError("Price must be positive")
        except ValueError:
            messagebox.showerror("Error", "Invalid price value")
            return
        
        try:
            stock = int(stock_str)
            if stock < 0:
                raise ValueError("Stock must be positive")
        except ValueError:
            messagebox.showerror("Error", "Invalid stock quantity")
            return
        
        # Get category ID
        category_id = None
        if category:
            self.db.connect()
            self.db.cursor.execute("SELECT id FROM categories WHERE name = %s", (category,))
            category_result = self.db.cursor.fetchone()
            self.db.disconnect()
            
            if category_result:
                category_id = category_result['id']
        
        # Save to database
        product_id = self.product_id_var.get()
        
        try:
            if product_id:  # Update existing product
                self.db.update_product(
                    product_id, name, description, price, stock, category_id, image_path
                )
                messagebox.showinfo("Success", "Product updated successfully")
            else:  # Add new product
                self.db.add_product(
                    name, description, price, stock, category_id, image_path
                )
                messagebox.showinfo("Success", "Product added successfully")
            
            # Refresh product list
            self.load_products()
            
            # Clear form
            self.add_new_product()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save product: {e}")
    
    def delete_product(self):
        """Delete selected product"""
        selected_items = self.product_tree.selection()
        if not selected_items:
            messagebox.showinfo("Info", "Please select a product to delete")
            return
        
        # Get the selected product ID
        item = self.product_tree.item(selected_items[0])
        product_id = item['values'][0]
        product_name = item['values'][1]
        
        # Confirm deletion
        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete the product '{product_name}'?"
        )
        
        if confirm:
            try:
                self.db.delete_product(product_id)
                messagebox.showinfo("Success", "Product deleted successfully")
                self.load_products()
                self.add_new_product()  # Clear form
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete product: {e}")
