import logging
import os


def setup_logging():
    """
    Настройка общего логирования.
    """
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)  # Создаём директорию для логов, если её нет

    logging.basicConfig(
        filename=os.path.join(log_dir, "app.log"),
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        encoding="utf-8"
    )


def setup_sqlalchemy_logging(level=logging.WARNING):
    """
    Настраивает уровень логирования для SQLAlchemy.
    По умолчанию показывает только предупреждения и ошибки.
    :param level: Уровень логирования (например, logging.INFO, logging.ERROR).
    """
    logging.getLogger("sqlalchemy.engine").setLevel(level)


def log_error(message):
    """
    Логирует сообщение об ошибке.
    """
    logging.error(message)
    print(f"Ошибка: {message}")


def log_info(message):
    """
    Логирует информационное сообщение.
    """
    logging.info(message)
    print(f"Информация: {message}")


def log_message(message, level="info"):
    """
    Универсальная функция логирования.
    :param message: Сообщение для логирования.
    :param level: Уровень логирования (info, warning, error, critical).
    """
    levels = {
        "info": logging.info,
        "warning": logging.warning,
        "error": logging.error,
        "critical": logging.critical
    }
    log_function = levels.get(level.lower(), logging.info)
    log_function(message)
    print(f"{level.capitalize()}: {message}")
