from flask import render_template, request, redirect, session
from flask_app import app
from flask_app.models.user import User
from flask import flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/become_a_trekker')
def become_a_trekker():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def user_reg():

    if not User.valid_reg(request.form):
        return redirect('/become_a_trekker')

    data = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email'],
        'password' : bcrypt.generate_password_hash(request.form['password']),
        'is_admin' : request.form['is_admin']
    }

    user_id = User.register_new_user(data)
    session['user_id'] = user_id
    return redirect('/home')

@app.route('/login', methods=['POST'])
def user_login():

    users = User.get_email({'email' : request.form['email']})
    if len(users) != 1:
        flash("Username or password is not correct, please check your spelling and try again.",'error_login_email')
        return redirect('/login')

    user = users[0]

    if not bcrypt.check_password_hash(user.password,request.form['password']):
        flash('Invalid password, please check your spelling and try again','error_login_password')
        return redirect('/register')
    
    # session['is_admin'] = user.is_admin
    # session['email'] = user.email
    session['user_id'] = user.id
    return redirect('/book')

@app.route('/home')
def display_home():
    return render_template('home.html')

@app.route('/book')
def display_book():
    user = session['user_id']
    return render_template('book.html', user = user)

@app.route('/about')
def display_about():
    return render_template('about.html')

@app.route('/community')
def display_community():
    return render_template('community.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
