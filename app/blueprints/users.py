from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from app.models.models import User
from app import db

users_bp = Blueprint('users', __name__)

@users_bp.route('/')
@login_required
def index():
    usuarios = User.query.all()
    return render_template('users/list.html', usuarios=usuarios)

@users_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        is_admin = True if request.form.get('is_admin') else False
        
        if User.query.filter_by(username=username).first():
            flash('El nombre de usuario ya existe.', 'danger')
            return redirect(url_for('users.create'))
            
        new_user = User(username=username, email=email, is_admin=is_admin)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash('Usuario creado exitosamente.', 'success')
        return redirect(url_for('users.index'))
        
    return render_template('users/create.html')

@users_bp.route('/delete/<int:id>')
@login_required
def delete(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    flash('Usuario eliminado exitosamente.', 'success')
    return redirect(url_for('users.index'))