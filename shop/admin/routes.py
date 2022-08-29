from flask import render_template, session, request, redirect, url_for, flash

from shop import app, db, bcrypt
from shop.admin.forms import RegistrationForm, LoginForm
from shop.admin.models import User



@app.route('/admin')
def admin():
    if 'email' not in session:
        flash(f'Please login first', 'danger')
        return redirect(url_for('login'))
    products = []
    return render_template('admin/index.html', title='Admin Page', products=products)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form=RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        user = User(name=form.name.data, username=form.username.data, email=form.email.data, password=hash_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Welcome, {form.name.data}. Thanks for registring', 'success')
        return redirect(url_for('login'))
    return render_template('admin/register.html', form=form, title='Registration page')




@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            session['email'] = form.email.data 
            flash(f"Welcome, {form.email.data}. You're logedin now", 'success')
            return redirect(request.args.get('next') or url_for('admin'))
        else:
            flash(f'Wrong password plese try again', 'danger')
    return render_template('admin/login.html', form=form, title='Login Page')