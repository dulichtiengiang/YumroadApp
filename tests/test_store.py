from yumroad.models import Store
import pytest
from flask.helpers import url_for
from yumroad.models import *

def create_store__with_num_product(name='Example Store', num_product=0): #! Tạo biến mặc định num_product=0
    store = Store(name=name)
    for index in range(num_product):
        product = Product(name='Product {}'.format(index), description='description {}'.format(index), store=store)
        db.session.add(product)
    db.session.add(store)
    db.session.commit()
    return store

#! Unit test
def test__store__creation(client, init_database):
    assert Store.query.count() == 0
    assert Product.query.count() == 0
    store = create_store__with_num_product(num_product=3)
    assert Store.query.count() == 1
    assert Product.query.count() == 3
    for product in Product.query.all():
        assert product.store == store

def test__store_name__validation(client, init_database):
    assert Store.query.count() == 0
    with pytest.raises(ValueError):
        create_store__with_num_product(name='bad')
    assert Store.query.count() == 0

def test__home_redirect(client, init_database):
    response = client.get(url_for('home'))
    assert response.status_code == 302
    assert response.location == url_for('store.index', _external=True)


def test__store_index_page(client, init_database):
    store = create_store__with_num_product(num_product=5)
    response = client.get(url_for('store.index'))
    assert b'Yumroad' in response.data
    assert store.name in str(response.data)

    expected_link = url_for('store.show', store_id=store.id)
    assert expected_link in str(response.data)
    for product in store.products[:3]: #run from 0 to 3
        expected_link = url_for('products.details', product_id=product.id)
        assert expected_link in str(response.data)

    for product in store.products[3:5]:
        expected_link = url_for('products.details', product_id=product.id)
        assert expected_link not in str(response.data)

def test__store_page(client, init_database):
    store = create_store__with_num_product(num_product=3)
    response = client.get(url_for('store.show', store_id = store.id))
    assert response.status_code == 200
    assert b'Yumroad' in response.data
    assert store.name in str(response.data)

    for product in store.products:
        expected_link = url_for('products.details', product_id=product.id)
        assert expected_link in str(response.data)