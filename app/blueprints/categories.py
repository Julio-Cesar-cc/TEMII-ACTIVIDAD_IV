from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from app.models.models import Categoria
from app import db

categories_bp = Blueprint('categories', __name__)

@categories_bp.route('/')
@login_required
def index():
    categorias = Categoria.query.all()
    return render_template('categories/list.html', categorias=categorias)

@categories_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        
        nueva_cat = Categoria(nombre=nombre, descripcion=descripcion)
        db.session.add(nueva_cat)
        db.session.commit()
        flash('Categoría creada correctamente.', 'success')
        return redirect(url_for('categories.index'))
        
    return render_template('categories/create.html')

@categories_bp.route('/delete/<int:id>')
@login_required
def delete(id):
    cat = Categoria.query.get_or_404(id)
    db.session.delete(cat)
    db.session.commit()
    flash('Categoría eliminada correctamente.', 'success')
    return redirect(url_for('categories.index'))