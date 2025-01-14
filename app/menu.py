import logging
from app.user_actions import (
    select_or_create_user,
    show_all_users,
    confirm_user_deletion,
    change_username
)
from app.quiz_logic import start_quiz, select_language, show_detailed_results
from app.utils import log_error


def main_menu():
    """
    Главное меню программы.
    """
    current_user = None
    logging.info("Запуск главного меню.")
    print("\nДобро пожаловать в программу \"SpeakEasy\"!")

    while True:
        try:
            if current_user:
                current_user = handle_user_menu(current_user)
            else:
                current_user = handle_main_menu()
        except Exception as e:
            log_error(f"Ошибка в main_menu: {e}")
            print(f"Произошла ошибка: {e}. Попробуйте снова.")


def handle_main_menu():
    """
    Логика главного меню.
    """
    print("\n--- Главное меню ---")
    print("1. Выбрать или добавить пользователя")
    print("2. Просмотреть всех пользователей")
    print("3. Выйти")

    choice = input("Ваш выбор: ")
    if choice == "1":
        return select_or_create_user()
    elif choice == "2":
        show_all_users()
    elif choice == "3":
        print("Выход из программы...")
        logging.info("Программа завершена.")
        exit(0)
    else:
        print("Неверный выбор. Попробуйте снова.")
        return None


def handle_user_menu(current_user):
    """
    Логика меню пользователя.
    """
    print(f"\n--- Меню пользователя {current_user.username} ---")
    print("1. Пройти викторину")
    print("2. Посмотреть детализированные результаты игр")
    print("3. Изменить имя пользователя")
    print("4. Удалить пользователя")
    print("5. Вернуться в главное меню")

    choice = input("Ваш выбор: ")
    if choice == "1":
        language = select_language()
        start_quiz(current_user.username, language)
    elif choice == "2":
        show_detailed_results(current_user.username)
    elif choice == "3":
        change_username(current_user)
    elif choice == "4":
        if confirm_user_deletion(current_user):
            return None  # Выход из меню пользователя после удаления
    elif choice == "5":
        current_user.close_session()
        logging.info("Возврат в главное меню.")
        return None
    else:
        print("Неверный выбор. Попробуйте снова.")
    return current_user
