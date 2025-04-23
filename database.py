import mysql.connector
import os
from datetime import datetime

class Database:
    def __init__(self, host='localhost', user='root', password='', database='cosmetic_shop'):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.conn = None
        self.cursor = None
        self.ensure_db_exists()
        
    def ensure_db_exists(self):
        """Ensure database exists and create it if it doesn't"""
        # Connect to MySQL server without specifying a database
        temp_conn = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password
        )
        temp_cursor = temp_conn.cursor()
        
        # Create database if it doesn't exist
        temp_cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
        
        temp_cursor.close()
        temp_conn.close()
        
        # Now connect to the database and create tables
        self.connect()
        self.create_tables()
        self.disconnect()
        
    def connect(self):
        """Connect to the MySQL database"""
        self.conn = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        self.cursor = self.conn.cursor(dictionary=True)
        
    def disconnect(self):
        """Disconnect from the MySQL database"""
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None
            
    def create_tables(self):
        """Create necessary tables if they don't exist"""
        # Create Categories table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL UNIQUE,
            description TEXT
        )
        ''')
        
        # Create Products table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            description TEXT,
            price DECIMAL(10, 2) NOT NULL,
            stock_quantity INT NOT NULL,
            category_id INT,
            image_path VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (category_id) REFERENCES categories (id)
        )
        ''')
        
        # Create Customers table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE,
            phone VARCHAR(20),
            address TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Create Orders table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INT AUTO_INCREMENT PRIMARY KEY,
            customer_id INT,
            order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            total_amount DECIMAL(10, 2) NOT NULL,
            status VARCHAR(20) DEFAULT 'Pending',
            FOREIGN KEY (customer_id) REFERENCES customers (id)
        )
        ''')
        
        # Create Order Items table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS order_items (
            id INT AUTO_INCREMENT PRIMARY KEY,
            order_id INT,
            product_id INT,
            quantity INT NOT NULL,
            price DECIMAL(10, 2) NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders (id),
            FOREIGN KEY (product_id) REFERENCES products (id)
        )
        ''')
        
        # Create Users table for authentication
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) NOT NULL UNIQUE,
            password VARCHAR(100) NOT NULL,
            role VARCHAR(20) DEFAULT 'staff',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Insert default admin user if not exists
        self.cursor.execute('''
        INSERT IGNORE INTO users (username, password, role)
        VALUES ('admin', 'admin123', 'admin')
        ''')
        
        # Insert some default categories
        categories = [
            ('Skincare', 'Products for skin care and treatment'),
            ('Makeup', 'Cosmetic products for face and body'),
            ('Haircare', 'Products for hair care and styling'),
            ('Fragrances', 'Perfumes and body sprays'),
            ('Bath & Body', 'Products for bathing and body care')
        ]
        
        for category in categories:
            try:
                self.cursor.execute('''
                INSERT IGNORE INTO categories (name, description)
                VALUES (%s, %s)
                ''', category)
            except mysql.connector.errors.IntegrityError:
                # Skip if category already exists
                pass
        
        self.conn.commit()
    
    # Product methods
    def add_product(self, name, description, price, stock_quantity, category_id, image_path=None):
        """Add a new product to the database"""
        self.connect()
        self.cursor.execute('''
        INSERT INTO products (name, description, price, stock_quantity, category_id, image_path)
        VALUES (%s, %s, %s, %s, %s, %s)
        ''', (name, description, price, stock_quantity, category_id, image_path))
        product_id = self.cursor.lastrowid
        self.conn.commit()
        self.disconnect()
        return product_id
    
    def update_product(self, product_id, name, description, price, stock_quantity, category_id, image_path=None):
        """Update an existing product"""
        self.connect()
        self.cursor.execute('''
        UPDATE products
        SET name = %s, description = %s, price = %s, stock_quantity = %s, 
            category_id = %s, image_path = %s
        WHERE id = %s
        ''', (name, description, price, stock_quantity, category_id, image_path, product_id))
        self.conn.commit()
        self.disconnect()
    
    def delete_product(self, product_id):
        """Delete a product from the database"""
        self.connect()
        self.cursor.execute('DELETE FROM products WHERE id = %s', (product_id,))
        self.conn.commit()
        self.disconnect()
    
    def get_product(self, product_id):
        """Get a product by ID"""
        self.connect()
        self.cursor.execute('''
        SELECT p.id, p.name, p.description, p.price, p.stock_quantity, 
               p.category_id, c.name as category_name, p.image_path
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.id
        WHERE p.id = %s
        ''', (product_id,))
        product = self.cursor.fetchone()
        self.disconnect()
        return product
    
    def get_all_products(self, category_id=None):
        """Get all products, optionally filtered by category"""
        self.connect()
        if category_id:
            self.cursor.execute('''
            SELECT p.id, p.name, p.description, p.price, p.stock_quantity, 
                   p.category_id, c.name as category_name, p.image_path
            FROM products p
            LEFT JOIN categories c ON p.category_id = c.id
            WHERE p.category_id = %s
            ORDER BY p.name
            ''', (category_id,))
        else:
            self.cursor.execute('''
            SELECT p.id, p.name, p.description, p.price, p.stock_quantity, 
                   p.category_id, c.name as category_name, p.image_path
            FROM products p
            LEFT JOIN categories c ON p.category_id = c.id
            ORDER BY p.name
            ''')
        products = self.cursor.fetchall()
        self.disconnect()
        return products
    
    # Category methods
    def get_all_categories(self):
        """Get all product categories"""
        self.connect()
        self.cursor.execute('SELECT id, name, description FROM categories ORDER BY name')
        categories = self.cursor.fetchall()
        self.disconnect()
        return categories
    
    # Customer methods
    def add_customer(self, name, email, phone, address):
        """Add a new customer"""
        self.connect()
        self.cursor.execute('''
        INSERT INTO customers (name, email, phone, address)
        VALUES (%s, %s, %s, %s)
        ''', (name, email, phone, address))
        customer_id = self.cursor.lastrowid
        self.conn.commit()
        self.disconnect()
        return customer_id
    
    def get_all_customers(self):
        """Get all customers"""
        self.connect()
        self.cursor.execute('SELECT id, name, email, phone, address FROM customers ORDER BY name')
        customers = self.cursor.fetchall()
        self.disconnect()
        return customers
    
    # Order methods
    def create_order(self, customer_id, total_amount, status='Pending'):
        """Create a new order"""
        self.connect()
        self.cursor.execute('''
        INSERT INTO orders (customer_id, total_amount, status)
        VALUES (%s, %s, %s)
        ''', (customer_id, total_amount, status))
        order_id = self.cursor.lastrowid
        self.conn.commit()
        self.disconnect()
        return order_id
    
    def add_order_item(self, order_id, product_id, quantity, price):
        """Add an item to an order"""
        self.connect()
        self.cursor.execute('''
        INSERT INTO order_items (order_id, product_id, quantity, price)
        VALUES (%s, %s, %s, %s)
        ''', (order_id, product_id, quantity, price))
        self.conn.commit()
        
        # Update product stock
        self.cursor.execute('''
        UPDATE products
        SET stock_quantity = stock_quantity - %s
        WHERE id = %s
        ''', (quantity, product_id))
        self.conn.commit()
        self.disconnect()
    
    def get_order_details(self, order_id):
        """Get details of an order"""
        self.connect()
        self.cursor.execute('''
        SELECT o.id, o.customer_id, c.name as customer_name, o.order_date, o.total_amount, o.status
        FROM orders o
        LEFT JOIN customers c ON o.customer_id = c.id
        WHERE o.id = %s
        ''', (order_id,))
        order = self.cursor.fetchone()
        
        self.cursor.execute('''
        SELECT oi.id, oi.product_id, p.name as product_name, oi.quantity, oi.price
        FROM order_items oi
        LEFT JOIN products p ON oi.product_id = p.id
        WHERE oi.order_id = %s
        ''', (order_id,))
        order_items = self.cursor.fetchall()
        
        self.disconnect()
        return order, order_items
    
    def get_all_orders(self, status=None):
        """Get all orders, optionally filtered by status"""
        self.connect()
        if status:
            self.cursor.execute('''
            SELECT o.id, o.customer_id, c.name as customer_name, o.order_date, o.total_amount, o.status
            FROM orders o
            LEFT JOIN customers c ON o.customer_id = c.id
            WHERE o.status = %s
            ORDER BY o.order_date DESC
            ''', (status,))
        else:
            self.cursor.execute('''
            SELECT o.id, o.customer_id, c.name as customer_name, o.order_date, o.total_amount, o.status
            FROM orders o
            LEFT JOIN customers c ON o.customer_id = c.id
            ORDER BY o.order_date DESC
            ''')
        orders = self.cursor.fetchall()
        self.disconnect()
        return orders
    
    def update_order_status(self, order_id, status):
        """Update the status of an order"""
        self.connect()
        self.cursor.execute('''
        UPDATE orders
        SET status = %s
        WHERE id = %s
        ''', (status, order_id))
        self.conn.commit()
        self.disconnect()
    
    # Reporting methods
    def get_sales_report(self, start_date, end_date):
        """Get sales report between two dates"""
        self.connect()
        self.cursor.execute('''
        SELECT o.id, o.order_date, c.name as customer_name, o.total_amount, o.status
        FROM orders o
        LEFT JOIN customers c ON o.customer_id = c.id
        WHERE o.order_date BETWEEN %s AND %s
        ORDER BY o.order_date
        ''', (start_date, end_date))
        sales = self.cursor.fetchall()
        self.disconnect()
        return sales
    
    def get_product_sales_report(self, start_date, end_date):
        """Get product sales report between two dates"""
        self.connect()
        self.cursor.execute('''
        SELECT p.id, p.name, SUM(oi.quantity) as total_quantity, SUM(oi.quantity * oi.price) as total_sales
        FROM order_items oi
        JOIN products p ON oi.product_id = p.id
        JOIN orders o ON oi.order_id = o.id
        WHERE o.order_date BETWEEN %s AND %s
        GROUP BY p.id, p.name
        ORDER BY total_sales DESC
        ''', (start_date, end_date))
        product_sales = self.cursor.fetchall()
        self.disconnect()
        return product_sales
    
    def get_low_stock_products(self, threshold=10):
        """Get products with stock below threshold"""
        self.connect()
        self.cursor.execute('''
        SELECT id, name, stock_quantity
        FROM products
        WHERE stock_quantity < %s
        ORDER BY stock_quantity
        ''', (threshold,))
        low_stock = self.cursor.fetchall()
        self.disconnect()
        return low_stock
