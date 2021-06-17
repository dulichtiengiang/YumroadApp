from itertools import product
from flask import Blueprint
from flask.templating import render_template

from yumroad.extensions import db
from yumroad.models import Store

bp_store = Blueprint('store', __name__)

@bp_store.route('/')
def index():
    stores = Store.query.all()
    return render_template('stores/index.html', stores=stores)

@bp_store.route('/<int:store_id>')
def show(store_id):
    store = Store.query.get_or_404(store_id)
    return render_template('stores/show.html', store=store, products=store.products)