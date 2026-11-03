from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models.models import Anuncio, Categoria
from app import db

ads_bp = Blueprint('ads', __name__)

@ads_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    categorias = Categoria.query.all()
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        contenido = request.form.get('contenido')
        categoria_id = request.form.get('categoria_id')
        
        nuevo_anuncio = Anuncio(
            titulo=titulo,
            contenido=contenido,
            categoria_id=categoria_id,
            usuario_id=current_user.id
        )
        db.session.add(nuevo_anuncio)
        db.session.commit()
        flash('Anuncio publicado con éxito.', 'success')
        return redirect(url_for('main.index'))
        
    return render_template('ads/create.html', categorias=categorias)

@ads_bp.route('/delete/<int:id>')
@login_required
def delete(id):
    anuncio = Anuncio.query.get_or_404(id)
    if anuncio.usuario_id != current_user.id and not current_user.is_admin:
        flash('No tienes permisos para eliminar este anuncio.', 'danger')
        return redirect(url_for('main.index'))
        
    db.session.delete(anuncio)
    db.session.commit()
    flash('Anuncio eliminado.', 'success')
    return redirect(url_for('main.index'))