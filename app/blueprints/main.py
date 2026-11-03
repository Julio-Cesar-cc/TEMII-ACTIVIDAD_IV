from flask import Blueprint, render_template
from flask_login import login_required
from app.models.models import Anuncio, Categoria

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@login_required
def index():
    anuncios = Anuncio.query.all()
    categorias = Categoria.query.all()
    return render_template('main/index.html', anuncios=anuncios, categorias=categorias)