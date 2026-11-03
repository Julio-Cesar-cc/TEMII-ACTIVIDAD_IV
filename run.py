from app import create_app, db
from app.models.models import User

app = create_app()

@app.cli.command("init-db")
def init_db():
    """Crea la base de datos y un usuario administrador inicial."""
    db.create_all()
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin', email='admin@admin.com', is_admin=True)
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print("Base de datos inicializada. Usuario admin creado (admin / admin123).")
    else:
        print("La base de datos ya estaba inicializada.")

if __name__ == '__main__':
    app.run(debug=True)