from app.menu import main_menu
from app.utils import setup_logging

if __name__ == "__main__":
    # Настраиваем логирование
    setup_logging()

    # Запускаем главное меню
    main_menu()
