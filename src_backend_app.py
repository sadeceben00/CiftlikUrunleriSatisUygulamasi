from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@localhost/dbname'
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), nullable=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    order_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(50), nullable=False)

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(username=data['username'], email=data['email'], password=hashed_password, role=data['role'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity={'username': user.username, 'role': user.role})
        return jsonify({'token': access_token}), 200
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    output = []
    for product in products:
        product_data = {'id': product.id, 'name': product.name, 'description': product.description, 'price': product.price, 'stock': product.stock}
        output.append(product_data)
    return jsonify({'products': output}), 200

@app.route('/product', methods=['POST'])
@jwt_required()
def add_product():
    current_user = get_jwt_identity()
    if current_user['role'] != 'çiftlik_sahibi':
        return jsonify({'message': 'Permission denied'}), 403
    data = request.get_json()
    new_product = Product(name=data['name'], description=data['description'], price=data['price'], stock=data['stock'], owner_id=current_user['id'])
    db.session.add(new_product)
    db.session.commit()
    return jsonify({'message': 'Product added successfully'}), 201

@app.route('/order', methods=['POST'])
@jwt_required()
def place_order():
    current_user = get_jwt_identity()
    data = request.get_json()
    new_order = Order(user_id=current_user['id'], product_id=data['product_id'], quantity=data['quantity'], total_price=data['total_price'], order_date=datetime.utcnow(), status='Beklemede')
    db.session.add(new_order)
    db.session.commit()
    return jsonify({'message': 'Order placed successfully'}), 201

if __name__ == '__main__':
    app.run(debug=True)