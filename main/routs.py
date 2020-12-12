from flask import render_template, request, flash, url_for, redirect
from flask_login import login_user, login_required, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from main import db, app
from .work_with_db import *


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/cabinet', methods=["GET", "POST"])
@login_required
def cabinet():
    user_id = request.args.get('id')
    user = Customer.query.filter_by(id=user_id).first()

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
    return render_template('cabinet.html', name=user.c_name, surname=user.c_surname, phone=user.c_phone)


@app.route('/product')
def product():
    return render_template('product.html')


@app.route('/cart', methods=["GET"])
@login_required
def cart():
    return render_template('cart.html')


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    login = request.form.get('login')
    password = request.form.get('password')

    if login and password:
        user = Customer.query.filter_by(c_login=login).first()
        if user and check_password_hash(user.c_password, password):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page + '?id='+str(user.id))
        else:
            flash('Login or password in not correct')
    else:
        flash('Please fill login and password fields')
    return render_template('login.html')


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
    return render_template('register.html')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.errorhandler(401)
def http_401_handler(error):
    return redirect(url_for('login_page') + '?next=' + request.url)
