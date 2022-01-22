from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User, CardsRentBr, CardsRentLand, CardsSellBr, CardsSellLand


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('get_cards_rent_br'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash(f'Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('get_cards_rent_br')
        return redirect(next_page)

    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()

    return redirect(url_for('get_cards_rent_br'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('get_cards_rent_br'))
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
@app.route('/cards_rent_br')
@login_required
def get_cards_rent_br():
    search = request.args.get('search')

    if search:
        search = request.args.get('search').strip()
        page = request.args.get('page', 1, type=int)
        cards = CardsRentBr.query.filter(
            CardsRentBr.title.contains(search) | CardsRentBr.contacts.contains(search) |
            CardsRentBr.author_card.contains(search) | CardsRentBr.region_address.contains(search) |
            CardsRentBr.street_address.contains(search) | CardsRentBr.card_number.contains(search)
        )
        pages = cards.paginate(page, app.config['POSTS_PER_PAGE'], False)
        next_url = url_for('get_cards_rent_br', page=pages.next_num) \
            if pages.has_next else None
        prev_url = url_for('get_cards_rent_br', page=pages.prev_num) \
            if pages.has_prev else None

        return render_template('cards_rent_br.html', pages=pages, next_url=next_url, prev_url=prev_url)

    else:
        page = request.args.get('page', 1, type=int)
        cards = CardsRentBr.query.order_by(CardsRentBr.card_id.desc())
        pages = cards.paginate(page, app.config['POSTS_PER_PAGE'], False)
        next_url = url_for('get_cards_rent_br', page=pages.next_num) \
            if pages.has_next else None
        prev_url = url_for('get_cards_rent_br', page=pages.prev_num) \
            if pages.has_prev else None

        return render_template('cards_rent_br.html', pages=pages, next_url=next_url, prev_url=prev_url)


@app.route('/cards_rent_br/<card_number>')
@login_required
def cards_rent_br_extend(card_number):
    card = CardsRentBr.query.filter_by(card_number=card_number).first_or_404()
    return render_template('cards_rent_br_extend.html', card=card)


@app.route('/cards_rent_land')
@login_required
def get_cards_rent_land():
    search = request.args.get('search')

    if search:
        search = request.args.get('search').strip()
        page = request.args.get('page', 1, type=int)
        cards = CardsRentLand.query.filter(
            CardsRentLand.title.contains(search) | CardsRentLand.contacts.contains(search) |
            CardsRentLand.author_card.contains(search) | CardsRentLand.placement.contains(search) |
            CardsRentLand.water.contains(search) | CardsRentLand.electricity.contains(search) |
            CardsRentLand.roads.contains(search)
        )
        pages = cards.paginate(page, app.config['POSTS_PER_PAGE'], False)
        next_url = url_for('get_cards_rent_land', page=pages.next_num) \
            if pages.has_next else None
        prev_url = url_for('get_cards_rent_land', page=pages.prev_num) \
            if pages.has_prev else None

        return render_template('cards_rent_land.html', pages=pages, next_url=next_url, prev_url=prev_url)

    else:
        page = request.args.get('page', 1, type=int)
        cards = CardsRentLand.query.order_by(CardsRentLand.date_post.desc())
        pages = cards.paginate(page, app.config['POSTS_PER_PAGE'], False)
        next_url = url_for('get_cards_rent_land', page=pages.next_num) \
            if pages.has_next else None
        prev_url = url_for('get_cards_rent_land', page=pages.prev_num) \
            if pages.has_prev else None

        return render_template('cards_rent_land.html', pages=pages, next_url=next_url, prev_url=prev_url)


@app.route('/cards_sell_br')
@login_required
def get_cards_sell_br():
    search = request.args.get('search')

    if search:
        search = request.args.get('search').strip()
        page = request.args.get('page', 1, type=int)
        cards = CardsSellBr.query.filter(
            CardsSellBr.title.contains(search) | CardsSellBr.contacts.contains(search) |
            CardsSellBr.author_card.contains(search) | CardsSellBr.region_address.contains(search) |
            CardsSellBr.street_address.contains(search)
        )
        pages = cards.paginate(page, app.config['POSTS_PER_PAGE'], False)
        next_url = url_for('get_cards_sell_br', page=pages.next_num) \
            if pages.has_next else None
        prev_url = url_for('get_cards_sell_br', page=pages.prev_num) \
            if pages.has_prev else None

        return render_template('cards_sell_br.html', pages=pages, next_url=next_url, prev_url=prev_url)

    else:
        page = request.args.get('page', 1, type=int)
        cards = CardsSellBr.query.order_by(CardsSellBr.date_post.desc())
        pages = cards.paginate(page, app.config['POSTS_PER_PAGE'], False)
        next_url = url_for('get_cards_sell_br', page=pages.next_num) \
            if pages.has_next else None
        prev_url = url_for('get_cards_sell_br', page=pages.prev_num) \
            if pages.has_prev else None

        return render_template('cards_sell_br.html', pages=pages, next_url=next_url, prev_url=prev_url)


@app.route('/cards_sell_land')
@login_required
def get_cards_sell_land():
    search = request.args.get('search')

    if search:
        search = request.args.get('search').strip()
        page = request.args.get('page', 1, type=int)
        cards = CardsSellLand.query.filter(
            CardsSellLand.title.contains(search) | CardsSellLand.contacts.contains(search) |
            CardsSellLand.author_card.contains(search) | CardsSellLand.placement.contains(search) |
            CardsSellLand.water.contains(search) | CardsSellLand.electricity.contains(search) |
            CardsSellLand.roads.contains(search)
        )
        pages = cards.paginate(page, app.config['POSTS_PER_PAGE'], False)
        next_url = url_for('get_cards_sell_land', page=pages.next_num) \
            if pages.has_next else None
        prev_url = url_for('get_cards_sell_land', page=pages.prev_num) \
            if pages.has_prev else None

        return render_template('cards_sell_land.html', pages=pages, next_url=next_url, prev_url=prev_url)

    else:
        page = request.args.get('page', 1, type=int)
        cards = CardsSellLand.query.order_by(CardsSellLand.date_post.desc())
        pages = cards.paginate(page, app.config['POSTS_PER_PAGE'], False)
        next_url = url_for('get_cards_sell_land', page=pages.next_num) \
            if pages.has_next else None
        prev_url = url_for('get_cards_sell_land', page=pages.prev_num) \
            if pages.has_prev else None
        return render_template('cards_sell_land.html', pages=pages, next_url=next_url, prev_url=prev_url)
