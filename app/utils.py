import json
import os
import logging

LOG_DIR = "logs/"
LOG_FILE = os.path.join(LOG_DIR, "app.log")

def setup_logging():
    """Настраивает логирование для приложения."""
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        encoding="utf-8"  # Указание кодировки UTF-8 для корректного сохранения
    )
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
