class Product:
    def __init__(self, id=None, name="", description="", price=0.0, stock_quantity=0, 
                 category_id=None, category_name="", image_path=None):
        self.id = id
        self.name = name
        self.description = description
        self.price = price
        self.stock_quantity = stock_quantity
        self.category_id = category_id
        self.category_name = category_name
        self.image_path = image_path
    
    @classmethod
    def from_db_row(cls, row):
        if not row:
            return None
        return cls(
            id=row['id'],
            name=row['name'],
            description=row['description'],
            price=row['price'],
            stock_quantity=row['stock_quantity'],
            category_id=row['category_id'],
            category_name=row.get('category_name', ''),
            image_path=row['image_path']
        )

class Category:
    def __init__(self, id=None, name="", description=""):
        self.id = id
        self.name = name
        self.description = description
    
    @classmethod
    def from_db_row(cls, row):
        if not row:
            return None
        return cls(
            id=row['id'],
            name=row['name'],
            description=row['description']
        )

class Customer:
    def __init__(self, id=None, name="", email="", phone="", address=""):
        self.id = id
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address
    
    @classmethod
    def from_db_row(cls, row):
        if not row:
            return None
        return cls(
            id=row['id'],
            name=row['name'],
            email=row['email'],
            phone=row['phone'],
            address=row['address']
        )

class Order:
    def __init__(self, id=None, customer_id=None, customer_name="", 
                 order_date=None, total_amount=0.0, status="Pending", items=None):
        self.id = id
        self.customer_id = customer_id
        self.customer_name = customer_name
        self.order_date = order_date
        self.total_amount = total_amount
        self.status = status
        self.items = items or []
    
    @classmethod
    def from_db_row(cls, row, items=None):
        if not row:
            return None
        return cls(
            id=row['id'],
            customer_id=row['customer_id'],
            customer_name=row.get('customer_name', ''),
            order_date=row['order_date'],
            total_amount=row['total_amount'],
            status=row['status'],
            items=items or []
        )

class OrderItem:
    def __init__(self, id=None, order_id=None, product_id=None, 
                 product_name="", quantity=0, price=0.0):
        self.id = id
        self.order_id = order_id
        self.product_id = product_id
        self.product_name = product_name
        self.quantity = quantity
        self.price = price
    
    @classmethod
    def from_db_row(cls, row):
        if not row:
            return None
        return cls(
            id=row['id'],
            order_id=row.get('order_id'),
            product_id=row['product_id'],
            product_name=row.get('product_name', ''),
            quantity=row['quantity'],
            price=row['price']
        )

class User:
    def __init__(self, id=None, username="", password="", role="staff"):
        self.id = id
        self.username = username
        self.password = password
        self.role = role
    
    @classmethod
    def from_db_row(cls, row):
        if not row:
            return None
        return cls(
            id=row['id'],
            username=row['username'],
            password=row['password'],
            role=row['role']
        )
