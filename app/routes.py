from app import app, db
import models

from flask import jsonify, request, send_from_directory, render_template
import jwt
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from functools import wraps

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/js/<js_file>', methods=['GET'])
def serve_js(js_file):
    return send_from_directory('static/js', js_file)


@app.route('/css/<css_file>', methods=['GET'])
def serve_css(css_file):
    return send_from_directory('static/css', css_file)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({'message': 'Token is missing!'}), 403

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'],)
        except:
            return jsonify({'message': 'Token is invalid'}), 403

        return f(*args, **kwargs)

    return decorated


@app.route('/api/user', methods=['POST'])
def create_user():
    data = request.get_json()

    hashed_password = generate_password_hash(data['password'], method='sha256')

    new_user = models.User(public_id=str(uuid.uuid4()), name=data['name'], email=data['email'], password=hashed_password)

    db.session.add(new_user)
    db.session.commit()

    token = jwt.encode({
        'public_id': new_user.public_id,
        'name': new_user.name,
        'email': new_user.email,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
    }, app.config['SECRET_KEY'])

    return jsonify({'message': 'New user created!', 'token': token.decode('UTF-8')})


@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    user = models.User.query.filter_by(email=data['email']).first()

    if data and user:
        unhashed_password = check_password_hash(pwhash=user.password, password=data['password'])

        if unhashed_password:
            token = jwt.encode({
                'public_id': user.public_id,
                'name': user.name,
                'email': user.email,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
            }, app.config['SECRET_KEY'])

            return jsonify({'token': token.decode('UTF-8')})

        return jsonify({'message': 'User not registered'}), 404

    return jsonify({'message': 'No matches'}), 401


# Customer routes

@app.route('/api/customers', methods=['GET'])
@token_required
def fetch_all_customers():
    customers = models.Customer.query.all()
    return jsonify([e.serialize() for e in customers])


@app.route('/api/customers', methods=['POST'])
@token_required
def create_customer():
    data = request.get_json()

    if data['name'] and data['address'] and data['phone']:
        customer = models.Customer(
            public_id=str(uuid.uuid4()),
            name=data['name'],
            address=data['address'],
            phone=data['phone']
        )

        db.session.add(customer)
        db.session.commit()

        if customer:
            return jsonify({'message': 'Customer successfully created!', 'customer': customer.serialize()}), 201

        else:
            return jsonify({'message': 'Customer was not created! Something wrong on server'}), 502

    else:
        return jsonify({'message': 'All fields required!'}), 400


@app.route('/api/customers', methods=['PUT'])
@token_required
def update_customer():
    data = request.get_json()

    if data and data.get('public_id'):
        customer = models.Customer.query.filter_by(public_id=data['public_id']).first()

        if data.get('name'):
            customer.name = data['name']

        if data.get('address'):
            customer.address = data['address']

        if data.get('phone'):
            customer.phone = data['phone']

        db.session.commit()

        return jsonify({'message': 'Customers changes saved!'}), 200

    else:
        return jsonify({'message': 'Request body is empty or no public_id passed'}), 502


@app.route('/api/customers/<string:customer_id>', methods=['DELETE'])
@token_required
def delete_customer(customer_id):
    db.session.query(models.Customer).filter(models.Customer.public_id == customer_id).delete()
    db.session.commit()

    customer = models.Customer.query.filter_by(public_id=customer_id).first()

    if customer is None:
        return jsonify({'message': 'Customer was deleted'}), 200

    return jsonify({'message': 'Customer is not deleted'}), 500


# Product routes

@app.route('/api/products', methods=['GET'])
@token_required
def fetch_all_products():
    products = models.Product.query.all()

    if products is not None:
        return jsonify([i.serialize() for i in products])

    return jsonify({'message': 'Can\'t get products, DB error!'}), 500


@app.route('/api/products', methods=['POST'])
@token_required
def create_product():
    data = request.get_json()

    if data and data.get('name') and data.get('price'):
        product = models.Product(public_id=str(uuid.uuid4()), name=data['name'], price=data['price'])

        db.session.add(product)
        db.session.commit()

        return jsonify({'message': 'Product successfully created!', 'product': product.serialize()}), 201

    return jsonify({'message': 'All parameter are required!'}), 502


@app.route('/api/products', methods=['PUT'])
@token_required
def update_product():
    data = request.get_json()

    if data and data.get('public_id'):
        product = models.Product.query.filter_by(public_id=data['public_id']).first()

        if product:
            if data.get('name'):
                product.name = data['name']

            if data.get('price'):
                product.price = data['price']

            db.session.commit()
        else:
            return jsonify({'message': 'Product not found in DB!'}), 404

        return jsonify({'message': 'Product successfully updated'}), 200

    return jsonify({'message': 'public_id is required parameter!'}), 502


@app.route('/api/products/<string:product_id>', methods=['DELETE'])
@token_required
def delete_product(product_id):
    if product_id:
        db.session.query(models.Product).filter(models.Product.public_id == product_id).delete()
        db.session.commit()

        if models.Product.query.filter_by(public_id=product_id).first() is None:
            return jsonify({'message': 'Product was successfully deleted!'}), 200

        return jsonify({'message': 'Product not deleted, DB error!'}), 500

    return jsonify({'message': 'product_id parameter is required!'}), 502


# Invoice routes

@app.route('/api/invoices', methods=['GET'])
@token_required
def fetch_all_invoices():
    invoices = models.Invoice.query.all()
    return jsonify([e.serialize() for e in invoices])


@app.route('/api/invoices/<string:invoice_id>', methods=['GET'])
@token_required
def fetch_invoice(invoice_id):
    invoice = models.Invoice.query.filter_by(public_id=invoice_id).first()

    return jsonify({'invoice': invoice.serialize()})


@app.route('/api/invoices', methods=['POST'])
@token_required
def create_invoice():
    data = request.get_json()

    if data and data.get('customerId') is not None \
            and data.get('discount') is not None \
            and data.get('total') is not None \
            and len(data.get('invoiceItems')) is not 0:
        invoice = models.Invoice(
            public_id=str(uuid.uuid4()),
            customer_id=data['customerId'],
            discount=data['discount'],
            total=data['total']
        )
        db.session.add(invoice)
        db.session.commit()

        for item in data['invoiceItems']:
            if item and item['productId'] and item['quantity']:
                item = models.InvoiceItem(
                    public_id=str(uuid.uuid4()),
                    product_id=item['productId'],
                    invoice=invoice,
                    quantity=item['quantity']
                )
                db.session.add(item)
                db.session.commit()
            else:
                return jsonify({'message': 'Product and quantity for each invoice item is required!'}), 503

        return jsonify({'message': 'Invoice created successfully!'}), 201

    return jsonify({'message': 'All fields for invoice is required!'}), 503


@app.route('/api/invoices', methods=['PUT'])
@token_required
def update_invoice():
    data = request.get_json()

    if data and data.get('publicId'):
        invoice = models.Invoice.query.filter_by(public_id=data['publicId'])

        if data.get('customerId'):
            invoice.customer_id = data['customerId']

        if data.get('discount'):
            invoice.discount = data['discount']

        if data.get('total'):
            invoice.total = data['total']

    return jsonify({'message': 'public_id is required!'}), 502


@app.route('/api/invoices/<string:invoice_id>', methods=['DELETE'])
@token_required
def delete_invoice(invoice_id):
    invoice = db.session.query(models.Invoice).filter(models.Invoice.public_id == invoice_id)
    invoice.invoice_items = []
    invoice.delete()
    db.session.commit()

    invoice = models.Invoice.query.filter_by(public_id=invoice_id).first()

    if invoice is None:
        return jsonify({'message': 'Customer was deleted'}), 200

    return jsonify({'message': 'Customer is not deleted'}), 500

