from flask import render_template, request, redirect, session
from flask_app import app
from flask_app.models.admin import Admin
from flask import flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/admin/login/')
def display_admin_login_page():
    return render_template('admin_login.html')


@app.route('/register/admin', methods=['POST'])
def admin_reg():

    if not Admin.validate_reg(request.form):
        return redirect('/become_a_trekker')

    data = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email'],
        'password' : bcrypt.generate_password_hash(request.form['password'])
    }

    admin_id = Admin.register_new_admin(data)
    session['admin_id'] = admin_id
    session['first_name'] = request.form['first_name']
    session['email'] = request.form['email']
    return redirect('/home')

@app.route('/login', methods=['POST'])
def admin_login():

    admins = Admin.check_admin_by_email({request.form['email']})
    if len(admins) != 1:
        flash("Username or password is not correct, please check your spelling and try again.",'error_login_email')
        return redirect('/login')

    admin = admins[0]

    if not bcrypt.check_password_hash(admin.password,request.form['password']):
        flash('Invalid password, please check your spelling and try again','error_login_password')
        return redirect('/register')
    
    session['admin_id'] = admin.id
    session['first_name'] = admin.first_name
    session['last_name'] = admin.last_name
    session['admin_email'] = admin.email
    return redirect('/book')
