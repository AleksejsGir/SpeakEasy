import logging
from app.models import UserManager
from app.db import get_all_users
from app.utils import log_error


def select_or_create_user():
    """
    Выбирает или создаёт нового пользователя.
    """
    username = input("Введите имя пользователя: ").strip()
    if username:
        user = UserManager(username)
        print(f"Добро пожаловать, {user.username}!")
        logging.info(f"Пользователь {user.username} выбран.")
        return user
    else:
        print("Имя пользователя не может быть пустым.")
        return None


def show_all_users():
    """
    Выводит всех пользователей из базы данных.
    """
    try:
        users = get_all_users()
        if not users:
            print("Нет зарегистрированных пользователей.")
            logging.info("Запрос всех пользователей: данных нет.")
            return

        print("\n--- Все пользователи ---")
        for index, user in enumerate(users, start=1):
            print(f"{index}. {user.username}")
        logging.info("Список пользователей успешно выведен.")
    except Exception as e:
        log_error(f"Ошибка в show_all_users: {e}")
        print(f"Произошла ошибка: {e}.")


def confirm_user_deletion(user):
    """
    Подтверждение удаления пользователя.
    """
    confirm = input(f"Вы уверены, что хотите удалить пользователя {user.username}? (да/нет): ")
    if confirm.lower() == "да":
        user.delete()
        print("Пользователь успешно удалён.")
        return True
    return False


def change_username(user):
    """
    Изменение имени пользователя.
    """
    new_name = input("Введите новое имя пользователя: ").strip()
    if new_name:
        user.change_username(new_name)
