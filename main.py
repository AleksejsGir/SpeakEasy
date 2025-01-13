import argparse
from app.utils import setup_logging, setup_sqlalchemy_logging
from app.db import initialize_database
from app.menu import main_menu
from app.main_fastapi import app  # Подключаем FastAPI
import uvicorn  # Для запуска FastAPI через Uvicorn

if __name__ == "__main__":
    # Настраиваем логирование
    setup_logging()
    setup_sqlalchemy_logging()

    # Инициализируем базу данных
    initialize_database()

    # Добавляем аргументы командной строки для выбора режима работы
    parser = argparse.ArgumentParser(description="Запуск SpeakEasy")
    parser.add_argument(
        "--mode",
        choices=["console", "api"],
        default="console",
        help="Режим работы приложения: console - консольное меню, api - веб-интерфейс",
    )
    args = parser.parse_args()

    if args.mode == "console":
        # Запуск консольного меню
        main_menu()
    elif args.mode == "api":
        # Запуск веб-интерфейса (FastAPI)
        uvicorn.run(app, host="127.0.0.1", port=8000)
