from app.utils import setup_logging, setup_sqlalchemy_logging
from app.db import initialize_database
from app.menu import main_menu

if __name__ == "__main__":
    # Настраиваем общее логирование
    setup_logging()

    # Настраиваем логирование SQLAlchemy
    setup_sqlalchemy_logging()

    # Инициализируем базу данных
    initialize_database()

    # Запускаем главное меню
    main_menu()
