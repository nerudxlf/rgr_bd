from flask_login import UserMixin

from main import db, manager


class Customer(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    c_name = db.Column(db.String(16), nullable=False)
    c_surname = db.Column(db.String(16))
    c_phone = db.Column(db.String(16))
    c_login = db.Column(db.String(32), nullable=False)
    c_password = db.Column(db.String(32), nullable=False)


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    c_customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"), nullable=False)
    c_customer = db.relationship("Customer", backref=db.backref('carts', lazy=True))


class CartProduct(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cp_cart_id = db.Column(db.Integer, db.ForeignKey("cart.id"), nullable=False)
    cp_cart = db.relationship("Cart", backref=db.backref("carts"), lazy=True)
    cp_product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    cp_product = db.relationship("Product", backref=db.backref('products'), lazy=True)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    p_name = db.Column(db.String(32), nullable=False)
    p_description = db.Column(db.String(512), nullable=False)
    p_price = db.Column(db.String(8), nullable=False)
    p_type_of_goods = db.Column(db.String(16), nullable=False)
    p_photo_id = db.Column(db.Integer, db.ForeignKey("product_photo.id"), nullable=False)
    p_photo = db.relationship("ProductPhoto", backref=db.backref('photo', lazy=True))


class ProductPhoto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pp_url = db.Column(db.String(64), nullable=False)


@manager.user_loader
def load_user(user_id):
    return Customer.query.get(user_id)

