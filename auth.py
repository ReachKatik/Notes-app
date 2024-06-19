from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from .import db
from flask_login import login_user, login_required, logout_user, current_user

# define blueprint for our application i.e. different menu URLS
auth = Blueprint('auth', __name__)


# page for login
@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('You\'re logged in.', category='success')
                # user logged in
                login_user(user, remember=True)
                return redirect(url_for('views.home'))                
                
            elif len(password) == 0:
                flash('Password can\'t be empty', category='error')
            else:
                flash('Incorrect password, try again.', category='error')
        elif len(email) == 0:
            flash('E-mail can\'t be empty', category='error')
        else:
            flash(f'E-mail, {email} does not exist. You can signup.', category='error')
                
        
    return render_template("login.html", user=current_user)


# page for logout
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You\'re logged out.', category='success')
    return redirect(url_for('auth.login'))


# page for logout
@auth.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        fname = request.form.get('fname')    
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        
        user = User.query.filter_by(email=email).first()
        
        if user:
            flash('E-mail already exists. Please login.', category='error')
        elif len(email) == 0:
            flash('E-mail can\'t be empty', category='error')
        elif len(email) < 4:
            flash('E-mail must be greater than 3 characters.', category='error')
        elif len(fname) < 2:
            flash('First Name must be greater than 1 character', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match', category='error')
        elif len(password1) < 7:
            flash('Passwords must be at least 6 characters', category='error')
        else:
            # add user to the database
            new_user = User(email=email, fname=fname, password=generate_password_hash(password1, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            # set the user to the new user
            user = new_user 
            login_user(user, remember=True)
            flash (f'{fname}, You\'re signed up successfully, start adding notes!', category='success')
            return redirect(url_for('views.home'))
            
        
    return render_template("signup.html", user=current_user)

