from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login.utils import login_user, logout_user, current_user

from yumroad.extensions import db, login_manager
from yumroad.models import User, Store
from yumroad.forms import LoginForm, SignupForm

from yumroad.email import send_basic_welcome_message 

bp_user = Blueprint('user', __name__)
#user loader take in a User ID and return out
#User object
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@login_manager.unauthorized_handler
def unauthorized():
    flash('__flash__You need to login', 'warning')
    session['after_login'] = request.url #Flash into url => session co flash, du cho flash nam tren hay nam duoi session['after]
    print(session)
    return redirect( url_for('user.login') )

@bp_user.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash("__flash__You are already logged in", "warning")
        return redirect(url_for('products.index'))
    form = SignupForm()
    if form.validate_on_submit():
        #create a user
        user = User.create(form.email.data, form.password.data)
        db.session.add(user)
        #! store = Store(name=form.store_name.data, user_id=user.id)
        store = Store(name=form.store_name.data, user=user) #! dùng relationship nên
        db.session.commit()

        #Dang nhap san
        login_user(user)
        send_basic_welcome_message(user.email)
        flash('__flash__Registered successfully', 'success')
        #we need to tell flask_login How to know that a Cookie belongs to a specific user (User cu the) 
        return redirect(url_for('products.index'))
    return render_template('/users/register.html', form=form)

@bp_user.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    #if current User is login
    if current_user.is_authenticated:
        flash("__flash__You are already logged in", "warning")
        return redirect(url_for('products.index'))
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).one() #one = gap la dung tim
        if user:
            login_user(user=user)
        flash('__flash__Logged in successfully', 'success')
        #we need to tell flask_login How to know that a Cookie belongs to a specific user (User cu the)
        #Neu login xong thi quay lai vi tri url truoc hoac ve index
        return redirect(session.get('after_login') or url_for('products.index'))
    return render_template('/users/login.html', form=form)

@bp_user.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('products.index'))