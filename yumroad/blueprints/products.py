from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_login import login_required
from yumroad.models import Product
from yumroad.extensions import db
from yumroad.forms import ProductForm


products = Blueprint('products', __name__)


@products.route('/')
def index():
    print(session)
    all_products = Product.query.all()
    return render_template('products/index.html', products=all_products)


@products.route('/<int:product_id>')
def details(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('products/details.html', product=product)


@products.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = ProductForm()

    if form.validate_on_submit():
        product = Product(
            name=form.name.data, description=form.description.data)
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('products.details', product_id=product.id))
    
    return render_template('products/create.html', form=form)


@products.route('/<int:product_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(product_id):

    product = Product.query.get_or_404(product_id)

    form = ProductForm(obj=product)

    if form.validate_on_submit():
        product.name = form.name.data
        product.description = form.description.data
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('products.details', product_id=product.id))

    return render_template('products/edit.html', product=product, form=form)


@products.errorhandler(404)
def not_found(exception):
    return render_template('products/404.html'), 404
