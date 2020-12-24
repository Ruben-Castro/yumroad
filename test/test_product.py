from flask import url_for
import pytest


from yumroad.extensions import db
from yumroad.models import Product


@pytest.fixture
def sample_book():
    book = Product(name="Sherlock Homes",
                   description="A house hunting detective")
    db.session.add(book)
    db.session.commit()
    return book


def test_product_creation(client, init_database, authenticated_request):
    assert Product.query.count() == 0

    book = Product(name="Sherlock Homes",
                   description="A house hunting detective")
    db.session.add(book)
    db.session.commit()

    assert Product.query.count() == 1
    assert Product.query.first().name == book.name


def test_name_validation(client, init_database):
    with pytest.raises(ValueError):
        Product(name="   a", description="invalid book")


def test_index_page(client, init_database, sample_book):
    response = client.get(url_for('products.index'))
    response_data_str = str(response.data)
    assert response.status_code == 200
    assert 'Yumroad' in response_data_str
    assert sample_book.name in response_data_str

    expected_link = url_for('products.details', product_id=sample_book.id)
    assert expected_link in response_data_str


def test_details_page(client, init_database, sample_book):
    response = client.get(
        url_for('products.details', product_id=sample_book.id))
    assert response.status_code == 200
    assert 'Yumroad' in str(response.data)
    assert "Purchase coming soon" in str(response.data)


def test_not_found_page(client, init_database):
    response = client.get(url_for('products.details', product_id=1))
    assert response.status_code == 404
    expected_url = url_for('products.index')
    assert expected_url in str(response.data)


def test_new_page(client, init_database, authenticated_request):
    response = client.get(url_for('products.create'))
    assert response.status_code == 200
    assert b'Name' in response.data
    assert b'Create' in response.data


def test_creation(client, init_database, authenticated_request):
    response = client.post(url_for('products.create'), data=dict(
        name="test product", description="is persited"), follow_redirects=True)
    assert response.status_code == 200
    assert b'test product' in response.data
    assert b'Purchase' in response.data


def test_edit_page(client, init_database, sample_book, authenticated_request):
    response = client.get(url_for('products.edit', product_id=sample_book.id))
    assert response.status_code == 200
    assert sample_book.description in str(response.data)
    assert sample_book.name in str(response.data)
    assert b'Edit' in response.data


def test_edit_submission(client, init_database, sample_book, authenticated_request):
    old_description = sample_book.description
    old_name = sample_book.name

    response = client.post(url_for('products.edit', product_id=sample_book.id), data={
                           'name': 'test-change', 'description': 'is persited'}, follow_redirects=True)

    assert response.status_code == 200
    assert 'test-change' in str(response.data)
    assert 'is persited' in str(response.data)
    assert old_description not in str(response.data)
    assert old_name not in str(response.data)
    assert b'Edit' not in response.data


def test_invalid_edit_submission(client, init_database, sample_book, authenticated_request):
    old_description = sample_book.description
    old_name = sample_book.name

    response = client.post(url_for('products.edit', product_id=sample_book.id), data={
                           'name': 'br0', 'description': 'is persited'})

    assert response.status_code == 200
    assert 'br0' in str(response.data)
    assert 'Field must be between 4 and 60 characters long' in str(
        response.data)
    assert Product.query.get(sample_book.id).description == old_description
    assert old_description not in str(response.data)
    assert old_name in str(response.data)
    assert b'Edit' in response.data


def test_new_page_unauth(client, init_database):
    response = client.get(url_for('products.create'))
    assert response.status_code == 302
    assert response.location == url_for('user.login', _external=True)
   

