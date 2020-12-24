from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from yumroad.extensions import login_manager
from yumroad.models import User, Store
from yumroad.forms import SignupForm, LoginForm
from flask_login import login_user, current_user, login_required, logout_user
from yumroad.extensions import db

user_bp = Blueprint('user', __name__)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@login_manager.unauthorized_handler
def unauthorized():
    session['after_login'] = request.url
    flash('You need to sign in!', "warning")
    return redirect(url_for('user.login'))



@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash("You are already logged in", "warning")
        return redirect(url_for('products.index'))
    form = SignupForm()
    if form.validate_on_submit():
        user = User.create(form.email.data, form.password.data)
        db.session.add(user)
        store = Store(name= form.store_name.data, user=user)
        db.session.commit()
        login_user(user)
        flash("Registered successfully", "success")
        return redirect(url_for('products.index'))

    return render_template('users/register.html', form=form)


@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash("You are already logged in", "warning")
        return redirect(url_for('products.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).one()
        login_user(user)
        flash("Logged in successfully", "success")
        return redirect(session.get('after_login') or url_for('products.index'))
    flash("Login unsuccessfully", "warning")
    return render_template('users/login.html', form=form)

@user_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('products.index'))



