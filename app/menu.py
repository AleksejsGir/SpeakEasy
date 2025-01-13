import logging
from app.models import UserManager
from app.db import get_all_users, get_all_words, add_word, save_quiz_result
from app.utils import log_error
from app.db import SessionLocal, QuizResult, User

def main_menu():
    """
    Главное меню программы.
    """
    logging.info("Запуск консольного меню.")
    print("\nДобро пожаловать в программу \"SpeakEasy\"!")

    while True:
        print("\n--- Главное меню ---")
        print("1. Управление пользователями")
        print("2. Работа со словарём")
        print("3. Выйти")
        choice = input("Ваш выбор: ")

        if choice == "1":
            user_menu()
        elif choice == "2":
            dictionary_menu()
        elif choice == "3":
            print("Выход из программы...")
            logging.info("Программа завершена.")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

def user_menu():
    """
    Меню для управления пользователями.
    """
    print("\n--- Управление пользователями ---")
    print("1. Показать всех пользователей")
    print("2. Добавить пользователя")
    print("3. Выбрать пользователя")
    print("4. Назад")
    choice = input("Ваш выбор: ")

    if choice == "1":
        show_all_users()
    elif choice == "2":
        username = input("Введите имя пользователя: ").strip()
        if username:
            UserManager(username).create_user()
            print(f"Пользователь {username} добавлен!")
    elif choice == "3":
        username = input("Введите имя пользователя: ").strip()
        if username:
            user_submenu(username)
    elif choice == "4":
        return
    else:
        print("Неверный выбор. Попробуйте снова.")

def user_submenu(username):
    """
    Подменю для выбранного пользователя.
    """
    user_manager = UserManager(username)

    while True:
        print(f"\n--- Меню пользователя {username} ---")
        print("1. Пройти викторину")
        print("2. Посмотреть детализированные результаты игр")
        print("3. Изменить имя пользователя")
        print("4. Удалить пользователя")
        print("5. Вернуться в главное меню")
        choice = input("Ваш выбор: ")

        if choice == "1":
            language = select_language()
            start_quiz(username, language)
        elif choice == "2":
            show_detailed_results(username)
        elif choice == "3":
            new_name = input("Введите новое имя пользователя: ").strip()
            if new_name:
                user_manager.change_username(new_name)
        elif choice == "4":
            confirm = input(f"Вы уверены, что хотите удалить пользователя {username}? (да/нет): ")
            if confirm.lower() == "да":
                user_manager.delete()
                print(f"Пользователь {username} удалён.")
                return
        elif choice == "5":
            return
        else:
            print("Неверный выбор. Попробуйте снова.")

def dictionary_menu():
    """
    Меню для работы со словарём.
    """
    print("\n--- Работа со словарём ---")
    print("1. Показать все слова")
    print("2. Добавить новое слово")
    print("3. Назад")
    choice = input("Ваш выбор: ")

    if choice == "1":
        show_all_words()
    elif choice == "2":
        language = input("Введите язык слова (например, 'en'): ").strip()
        word = input("Введите слово: ").strip()
        translation = input("Введите перевод: ").strip()
        if language and word and translation:
            add_word(language, word, translation)
            print(f"Слово {word} ({language}) добавлено!")
    elif choice == "3":
        return
    else:
        print("Неверный выбор. Попробуйте снова.")

def show_all_users():
    """
    Вывод всех пользователей.
    """
    try:
        users = get_all_users()
    except Exception as e:
        log_error(f"Ошибка при получении пользователей: {e}")
        users = []

    if not users:
        print("Пользователи не найдены.")
    else:
        print("\n--- Список пользователей ---")
        for user in users:
            print(f"- {user.username}")

def show_all_words():
    """
    Вывод всех слов.
    """
    try:
        words = get_all_words()
    except Exception as e:
        log_error(f"Ошибка при получении слов: {e}")
        words = []

    if not words:
        print("Словарные слова не найдены.")
    else:
        print("\n--- Список слов ---")
        for word in words:
            print(f"{word.language}: {word.word} -> {word.translation}")

def select_language():
    """
    Выбор языка для викторины.
    """
    while True:
        print("\n--- Выберите язык для викторины ---")
        print("1. Английский → Русский")
        print("2. Испанский → Русский")
        print("3. Немецкий → Русский")
        print("4. Французский → Русский")
        choice = input("Ваш выбор: ")

        if choice == "1":
            return "en"
        elif choice == "2":
            return "es"
        elif choice == "3":
            return "de"
        elif choice == "4":
            return "fr"
        else:
            print("Неверный выбор. Попробуйте снова.")

def start_quiz(username, language):
    """
    Запуск викторины.
    """
    try:
        words = get_all_words()
        language_words = [word for word in words if word.language == language]
    except Exception as e:
        log_error(f"Ошибка при получении слов для викторины: {e}")
        language_words = []

    if not language_words:
        print(f"Словарь для языка {language} пуст или не найден.")
        return

    print(f"\nНачинаем викторину для пользователя {username}.")
    correct_answers = 0

    for word in language_words:
        answer = input(f"Переведите слово '{word.word}': ").strip()
        if answer.lower() == word.translation.lower():
            print("Правильно!")
            correct_answers += 1
        else:
            print(f"Неправильно. Правильный ответ: {word.translation}")

    print(f"\nВикторина завершена. Правильных ответов: {correct_answers}/{len(language_words)}")

    user = next((u for u in get_all_users() if u.username == username), None)
    if user:
        save_quiz_result(user.id, language, correct_answers, len(language_words))

def show_detailed_results(username):
    """
    Показать детализированные результаты игр пользователя.
    :param username: Имя пользователя, для которого нужно показать результаты.
    """
    logging.info(f"Запрос детализированных результатов для пользователя: {username}")
    session = SessionLocal()
    try:
        # Находим пользователя по имени
        user = session.query(User).filter(User.username == username).first()
        if not user:
            print(f"Пользователь {username} не найден.")
            logging.warning(f"Пользователь {username} не найден в базе данных.")
            return

        # Получаем результаты викторин для пользователя
        results = session.query(QuizResult).filter(QuizResult.user_id == user.id).all()
        if not results:
            print(f"У пользователя {username} пока нет результатов викторин.")
            logging.info(f"У пользователя {username} отсутствуют записи в таблице QuizResult.")
            return

        # Выводим результаты
        print(f"\n--- Детализированные результаты игр пользователя {username} ---")
        for result in results:
            print(f"Язык: {result.language}")
            print(f"Правильные ответы: {result.correct_answers}/{result.total_questions}")
            print("-" * 30)
        logging.info(f"Пользователь {username} успешно просмотрел {len(results)} результатов.")
    except Exception as e:
        logging.error(f"Ошибка при получении результатов для пользователя {username}: {e}")
        print(f"Произошла ошибка при получении результатов. Попробуйте снова.")
    finally:
        session.close()

if __name__ == "__main__":
    main_menu()
