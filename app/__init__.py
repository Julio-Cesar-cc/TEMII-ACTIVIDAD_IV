from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'clave_secreta_super_segura_2026'  # Es necesaria para Flask-Login y las alertas flash
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bd_anuncios.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # Redirige al login si no está autenticado

    from app.models.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # --- 1. IMPORTAR LOS BLUEPRINTS ---
    from app.blueprints.auth import auth_bp
    from app.blueprints.main import main_bp
    from app.blueprints.users import users_bp
    from app.blueprints.categories import categories_bp
    from app.blueprints.ads import ads_bp

    # --- 2. REGISTRAR LOS BLUEPRINTS EN LA APLICACIÓN ---
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(categories_bp, url_prefix='/categories')
    app.register_blueprint(ads_bp, url_prefix='/ads')

    with app.app_context():
        db.create_all() # Genera físicamente las tablas en SQLite

    return app