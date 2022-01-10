import sqlite3

from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash(f'Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Congratulations, now you're one of us!")
        return redirect(url_for('login'))
    return render_template('register.html', title='Registration', form=form)


@app.route('/')
@app.route('/index')
@login_required
def index():
    user = {'username': 'Test Farpost'}
    posts = [
        {
            'author': {'username': 'Pavel'},
            'body': 'Nihil verum est licit omnia'
        },
        {
            'author': {'username': 'Gleb'},
            'body': 'Se vici paceum para bellum'
        }
    ]
    return render_template('index.html', title='Homepage', posts=posts)


@app.route('/cards_rent_br')
@login_required
def get_cards_rent_br():
    con = sqlite3.connect('/Users/vcorvinus/PycharmProjects/far_parsers/data/cards.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM cards_rent_br')
    data = cur.fetchall()

    return render_template('cards_rent_br.html', data=data)


@app.route('/cards_rent_land')
@login_required
def get_cards_rent_land():
    con = sqlite3.connect('/Users/vcorvinus/PycharmProjects/far_parsers/data/cards.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM cards_rent_land')
    data = cur.fetchall()

    return render_template('cards_rent_br.html', data=data)


@app.route('/cards_sell_br')
@login_required
def get_cards_sell_br():
    con = sqlite3.connect('/Users/vcorvinus/PycharmProjects/far_parsers/data/cards.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM cards_sell_br')
    data = cur.fetchall()

    return render_template('cards_sell_br.html', data=data)


@app.route('/cards_sell_land')
@login_required
def get_cards_sell_land():
    con = sqlite3.connect('/Users/vcorvinus/PycharmProjects/far_parsers/data/cards.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM cards_sell_land')
    data = cur.fetchall()

    return render_template('cards_sell_land.html', data=data)