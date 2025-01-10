from flask import Flask
from .utils import setup_logging

def create_app():
    app = Flask(__name__)

    # Настройка логирования
    setup_logging()

    # Подключение маршрутов
    from .routes import main_bp
    app.register_blueprint(main_bp)

    return app
