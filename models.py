from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String, unique=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(80), nullable=False)

    def serialize(self):
        return {
            'public_id': self.public_id,
            'name': self.name,
            'email': self.email,
            'password': self.password
        }


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String, unique=True)
    name = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)

    def serialize(self):
        return {
            'public_id': self.public_id,
            'name': self.name,
            'address': self.address,
            'phone': self.phone
        }


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String, unique=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)

    def serialize(self):
        return {
            'public_id': self.public_id,
            'name': self.name,
            'price': self.price
        }


class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String, unique=True)
    customer_id = db.Column(db.String, nullable=False)
    invoice_items = db.relationship('InvoiceItem', backref='invoice', lazy='dynamic')
    discount = db.Column(db.Float, nullable=False)
    total = db.Column(db.Float, nullable=False)

    def serialize(self):
        return {
            'public_id': self.public_id,
            'customer_id': self.customer_id,
            'invoice_items': [i.serialize() for i in self.invoice_items],
            'discount': self.discount,
            'total': self.total
        }


class InvoiceItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String, unique=True)
    invoice_id = db.Column(db.String, db.ForeignKey('invoice.public_id'))
    product_id = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def serialize(self):
        return {
            'public_id': self.public_id,
            'invoice_id': self.invoice_id,
            'product_id': self.product_id,
            'quantity': self.quantity
        }

