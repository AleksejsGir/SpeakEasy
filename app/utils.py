import logging


def setup_logging(log_level=logging.INFO, to_console=False):
    """
    Настройка общего логирования.
    :param log_level: Уровень логирования (например, logging.INFO, logging.DEBUG).
    :param to_console: Выводить ли логи в консоль.
    """
    logging.basicConfig(
        filename="logs/app.log",
        level=log_level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        encoding="utf-8"
    )

    if to_console:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
        console_handler.setFormatter(console_formatter)
        logging.getLogger().addHandler(console_handler)

    logging.info("Логирование настроено на уровень %s.", logging.getLevelName(log_level))



def setup_sqlalchemy_logging(level=logging.WARNING):
    """
    Настраивает уровень логирования для SQLAlchemy.
    По умолчанию показывает только предупреждения и ошибки.
    :param level: Уровень логирования (например, logging.INFO, logging.ERROR).
    """
    logging.getLogger("sqlalchemy.engine").setLevel(level)
    logging.info("SQLAlchemy логирование настроено на уровень %s.", logging.getLevelName(level))


def log_debug(message):
    """
    Логирует сообщение уровня DEBUG.
    :param message: Сообщение для логирования.
    """
    logging.debug(message)


def log_info(message):
    """
    Логирует сообщение уровня INFO.
    :param message: Сообщение для логирования.
    """
    logging.info(message)


def log_warning(message):
    """
    Логирует сообщение уровня WARNING.
    :param message: Сообщение для логирования.
    """
    logging.warning(message)


def log_error(message):
    """
    Логирует сообщение уровня ERROR.
    :param message: Сообщение для логирования.
    """
    logging.error(message)


def log_critical(message):
    """
    Логирует сообщение уровня CRITICAL.
    :param message: Сообщение для логирования.
    """
    logging.critical(message)
