from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Integer)
    image = db.Column(db.String(100))
    description = db.Column(db.String(255))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    phone = db.Column(db.String(20))
    password = db.Column(db.String(100))
    is_admin = db.Column(db.Boolean, default=False)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100))
    product_name = db.Column(db.String(100))
    status = db.Column(db.String(50), default="Beklemede")















