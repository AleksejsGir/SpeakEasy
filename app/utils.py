import json
import os
import logging

LOG_DIR = "logs/"
LOG_FILE = os.path.join(LOG_DIR, "app.log")

def setup_logging():
    """Настраивает логирование для приложения."""
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    # Настраиваем логгер
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Формат логов
    log_format = "%(asctime)s - %(levelname)s - %(message)s"
    formatter = logging.Formatter(log_format)

    # Логи в файл
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Логи в консоль (только для ошибок)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.ERROR)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    logging.info("Логирование настроено.")

def log_error(error_message):
    """Логирует ошибки в файл."""
    logging.error(error_message)

def load_json(file_path):
    """Загружает данные из JSON файла."""
    if not os.path.exists(file_path):
        return {}
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(file_path, data):
    """Сохраняет данные в JSON файл."""
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
