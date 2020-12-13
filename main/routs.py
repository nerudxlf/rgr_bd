from flask import render_template, request, flash, url_for, redirect, g
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash

from main import db, app
from .work_with_db import *


@app.before_request
def before_request():
    g.user = current_user


@app.route('/')
def index():
    return render_template('index.html', title_name="WEB APP")


@app.route('/cabinet', methods=["GET", "POST"])
@login_required
def cabinet():
    user = Customer.query.filter_by(c_login=g.user.c_login).first()
    if request.method == 'POST':
        re_name = request.form.get('name')
        re_surname = request.form.get('surname')
        re_phone = request.form.get('phone')
        if not (re_name, re_surname, re_phone):
            return request
        if re_name:
            user.c_name = re_name
        if re_surname:
            user.c_surname = re_surname
        if re_phone:
            user.c_phone = re_phone
        db.session.commit()
    return render_template('cabinet.html', name=user.c_name, surname=user.c_surname, phone=user.c_phone,
                           title_name="Cabinet")


@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin_page():
    admin = Customer.query.filter_by(c_login=g.user.c_login).first()
    if admin.c_admin == 1:
        return render_template('admin.html', title_name="Admin Page")
    else:
        return redirect(url_for('index'))


@app.route('/delete', methods=['POST'])
@login_required
def delete():
    admin = Customer.query.filter_by(c_login=g.user.c_login).first()
    if admin.c_admin == 1 and request.method == 'POST':
        product_name = request.form.get('product_name')
        product_object = Product.query.filter_by(p_name=product_name).first()
        if not product_object:
            return redirect(url_for('admin_page') + "?msg=not_found")
        else:
            db.session.delete(product_object)
            db.session.commit()
            return redirect(url_for('admin_page') + "?msg=ok")
    return redirect(url_for('index'))


@app.route('/update', methods=['POST'])
@login_required
def update():
    admin = Customer.query.filter_by(c_login=g.user.c_login).first()
    if admin.c_admin == 1 and request.method == 'POST':
        check_name = Product.query.filter_by(p_name=request.form.get('check_name')).first()
        if not check_name:
            return redirect(url_for('admin_page') + "?msg=not_found")
        else:
            new_name = request.form.get('new_name')
            new_description = request.form.get('new_description')
            new_price = request.form.get('new_price')
            new_pic = request.form.get('new_pic')
            if new_name:
                check_name.p_name = new_name
            if new_description:
                check_name.p_description = new_description
            if new_price:
                check_name.p_price = new_price
            if new_pic:
                check_name.p_photo_id = new_pic
            db.session.commit()
            return redirect(url_for('admin_page') + "?msg=ok")
    return redirect(url_for('index'))


@app.route('/add', methods=['POST'])
@login_required
def add():
    admin = Customer.query.filter_by(c_login=g.user.c_login).first()
    if admin.c_admin == 1 and request.method == 'POST':
        product_name = request.form.get('product_name')
        product_description = request.form.get('product_description')
        product_price = request.form.get('product_price')
        product_photo = request.form.get('product_photo')
        if not (product_price or product_description or product_name or product_photo):
            return redirect(url_for('admin_page') + "?msg=fill_fields")
        else:
            new_product = Product(p_name=product_name, p_description=product_description, p_price=product_price,
                                  p_photo_id=product_photo)
            db.session.add(new_product)
            db.session.commit()
            return redirect(url_for('admin_page') + "?msg=ok")
    return redirect(url_for('index'))


@app.route('/product')
def product():
    return render_template('product.html', title_name="Product")


@app.route('/cart', methods=["GET"])
@login_required
def cart():
    return render_template('cart.html', title_name="Cart")


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    login = request.form.get('login')
    password = request.form.get('password')

    if login and password:
        user = Customer.query.filter_by(c_login=login).first()
        if user and check_password_hash(user.c_password, password):
            login_user(user)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('index'))
        else:
            flash('Login or password in not correct')
    else:
        flash('Please fill login and password fields')
    return render_template('login.html', title_name="login")


@app.route('/register', methods=['GET', 'POST'])
def register():
    name = request.form.get('name')
    surname = request.form.get('surname')
    phone = request.form.get('phone')
    login = request.form.get('login')
    password = request.form.get('password')
    password_retype = request.form.get('password_retype')
    if request.method == 'POST':
        if not (name or login or password or password_retype):
            flash('Please, fill all fields')
        elif password != password_retype:
            flash('Passwords are not equal')
        else:
            hash_pwd = generate_password_hash(password)
            new_customer = Customer(c_name=name, c_surname=surname, c_phone=phone, c_login=login, c_password=hash_pwd)
            db.session.add(new_customer)
            db.session.commit()
            return redirect('login')
    return render_template('register.html', title_name="register")


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.errorhandler(401)
def http_401_handler(error):
    return redirect(url_for('login_page') + '?next=' + request.url)
