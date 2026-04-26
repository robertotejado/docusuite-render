from dotenv import load_dotenv
load_dotenv() # ¡Esto carga las variables del archivo .env automáticamente!

from flask import Flask, redirect, url_for
from flask_login import LoginManager
from src.db.database import get_db_connection, init_db
from src.routes.main_routes import main

app = Flask(__name__)
app.secret_key = 'una_clave_muy_secreta_y_segura' # Cambia esto luego

# Configuración de Flask-Login
login_manager = LoginManager()
login_manager.login_view = 'main.login' # A dónde enviar si no están logueados
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    from src.models.user import User
    return User.get(user_id)

app.register_blueprint(main)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
