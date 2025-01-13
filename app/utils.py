import logging

def setup_logging():
    """
    Настройка общего логирования.
    """
    logging.basicConfig(
        filename="logs/app.log",
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
