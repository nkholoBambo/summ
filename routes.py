from flask import Blueprint, render_template, redirect, url_for, request, flash
from .db import get_db_connection
from .forms import ProfileForm
import sqlite3

bp = Blueprint('routes', __name__)

@bp.route('/', methods=['GET', 'POST'])
def index():
    db = get_db_connection(current_app.config['DATABASE'])
    users = db.execute('SELECT * FROM users').fetchall()
    db.close()
    return render_template('index.html', users=users)

import sqlite3
from flask import flash, redirect, url_for, current_app, render_template

@bp.route('/register', methods=['GET', 'POST'])
def register(): 
    form = ProfileForm()
    if form.validate_on_submit():
        
        username = form.username.data
        email = form.email.data
        age = form.age.data
        bio = form.bio.data
        
        db = get_db_connection(current_app.config['DATABASE'])
        try:
            db.execute(
                'INSERT INTO users (username, email, age, bio) VALUES (?, ?, ?, ?)',
                (username, email, age, bio)
            )
            db.commit()
            flash('Profile created successfully!', 'success')
            return redirect(url_for('routes.index'))
        except sqlite3.IntegrityError:
            
            flash('Error: Could not create profile. A user with this username/email might already exist.', 'danger')
        finally:
            db.close()
    return render_template('register.html', form=form)

@bp.route('/profile/<int:user_id>')
def profile(user_id):
    db = get_db_connection(current_app.config['DATABASE'])
    user = db.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    db.close()
    if not user:
        flash('User not found!', 'danger')
        return redirect(url_for('main.index'))
    return render_template('profile.html', user=user)

@bp.route('/update/<int:user_id>', methods=['GET', 'POST'])
def update(user_id):
    db = get_db_connection(current_app.config['DATABASE'])
    user = db.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    
    if not user:
        flash('User not found!', 'danger')
        db.close()
        return redirect(url_for('main.index'))
    
    form = ProfileForm()
    if request.method == 'GET':
        form.username.data = user['username']
        form.email.data = user['email']
        form.age.data = user['age']
        form.bio.data = user['bio']
    elif form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        age = form.age.data
        bio = form.bio.data
        
        try:
            db.execute(
                'UPDATE users SET username = ?, email = ?, age = ?, bio = ? WHERE id = ?',
                (username, email, age, bio, user_id)
            )
            db.commit()
            flash('User updated successfully!', 'success')
            return redirect(url_for('routes.profile', user_id=user_id))
        except sqlite3.IntegrityError:
            flash('Error: Could not update profile. A user with this username/email might already exist.', 'error')
    
    db.close()
    return render_template('update.html', form=form, user_id=user_id)