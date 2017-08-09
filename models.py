from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String, unique=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(80))

    def __repr__(self):
        return '<User %r>' % self.name

    def serialize(self):
        return {
            'public_id': self.public_id,
            'name': self.name,
            'email': self.email,
            'password': self.password
        }


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)

    def __init__(self, name, address, phone):
        self.name = name,
        self.address = address,
        self.phone = phone

    def __repr__(self):
        return '<Customer %r>' % self.name

    def serialize(self):
        return {
            'name': self.name,
            'address': self.address,
            'phone': self.phone
        }


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Integer, nullable=False)

    def __init__(self, name, price):
        self.name = name,
        self.price = price

    def __repr__(self):
        return '<Product %r>' % self.name

    def serialize(self):
        return {
            'name': self.name,
            'price': self.price
        }


class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, nullable=False)
    discount = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Integer, nullable=False)

    def __init__(self, customer_id, discount, total):
        self.customer_id = customer_id
        self.discount = discount
        self.total = total

    def __repr__(self):
        return '<Invoice>'

    def serialize(self):
        return {
            'customer_id': self.customer_id,
            'discount': self.discount,
            'total': self.total
        }


class InvoiceItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def __init__(self, invoice_id, product_id, quantity):
        self.invoice_id = invoice_id
        self.product_id = product_id
        self.quantity = quantity

    def __repr__(self):
        return '<InvoiceItem>'

    def serialize(self):
        return {
            'invoice_id': self.invoice_id,
            'product_id': self.product_id,
            'quantity': self.quantity
        }