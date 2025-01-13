import logging
from app.models import UserManager
from app.db import get_all_users, get_all_words, SessionLocal, QuizResult, User
from app.utils import log_error

def main_menu():
    """
    Главное меню программы.
    """
    current_user = None  # Текущий пользователь

    # Приветствие
    logging.info("Запуск главного меню.")
    print("\nДобро пожаловать в программу \"SpeakEasy\"!")

    while True:
        try:
            if current_user:
                # Меню действий для текущего пользователя
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
                    new_name = input("Введите новое имя пользователя: ").strip()
                    if new_name:
                        current_user.change_username(new_name)
                elif choice == "4":
                    confirm = input(f"Вы уверены, что хотите удалить пользователя {current_user.username}? (да/нет): ")
                    if confirm.lower() == "да":
                        current_user.delete()
                        current_user = None
                        print("Пользователь успешно удалён.")
                elif choice == "5":
                    current_user.close_session()
                    current_user = None
                    logging.info("Возврат в главное меню.")
                else:
                    print("Неверный выбор. Попробуйте снова.")
            else:
                # Главное меню
                print("\n--- Главное меню ---")
                print("1. Выбрать или добавить пользователя")
                print("2. Просмотреть всех пользователей")
                print("3. Выйти")
                choice = input("Ваш выбор: ")

                if choice == "1":
                    username = input("Введите имя пользователя: ").strip()
                    if username:
                        current_user = UserManager(username)
                        print(f"Добро пожаловать, {current_user.username}!")
                        logging.info(f"Пользователь {current_user.username} выбран.")
                elif choice == "2":
                    show_all_users()
                elif choice == "3":
                    print("Выход из программы...")
                    logging.info("Программа завершена.")
                    break
                else:
                    print("Неверный выбор. Попробуйте снова.")
        except Exception as e:
            log_error(f"Ошибка в main_menu: {e}")
            print(f"Произошла ошибка: {e}. Попробуйте снова.")

def show_all_users():
    """
    Выводит всех пользователей из базы данных.
    """
    try:
        users = get_all_users()  # Получаем всех пользователей из базы данных
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

def select_language():
    """
    Выбор языка для викторины.
    """
    while True:
        try:
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
        except Exception as e:
            log_error(f"Ошибка в select_language: {e}")
            print(f"Произошла ошибка: {e}.")

def start_quiz(username, language):
    """
    Начало викторины для пользователя.
    """
    try:
        words = get_all_words()  # Получаем все слова из базы данных
        language_words = [word for word in words if word.language == language]

        if not language_words:
            print(f"Словарь для языка {language} пуст или не найден.")
            logging.warning(f"Словарь для языка {language} отсутствует.")
            return

        correct_answers = 0
        total_questions = len(language_words)

        print(f"\nНачинаем викторину для пользователя {username}.")
        print("Введите перевод для каждого слова. Напишите 'exit', чтобы остановить викторину в любой момент.\n")
        logging.info(f"Викторина начата (пользователь: {username}, язык: {language}).")

        for word in language_words:
            answer = input(f"Что означает слово '{word.word}'? ").strip()
            if answer.lower() == "exit":
                print("Викторина остановлена.")
                logging.info(f"Викторина для пользователя {username} остановлена.")
                break
            if answer.lower() == word.translation.lower():
                print("Правильно!")
                correct_answers += 1
            else:
                print(f"Неправильно. Правильный ответ: {word.translation}")

        print("\nВикторина завершена.")
        print(f"Вы ответили правильно на {correct_answers} из {total_questions} вопросов.")
        logging.info(f"Викторина завершена (пользователь: {username}): {correct_answers}/{total_questions}.")

        # Сохранение результатов
        session = SessionLocal()
        user = session.query(User).filter_by(username=username).first()
        new_result = QuizResult(
            user_id=user.id,
            language=language,
            correct_answers=correct_answers,
            total_questions=total_questions
        )
        session.add(new_result)
        session.commit()
        session.close()
        print("Результаты сохранены.")
    except Exception as e:
        log_error(f"Ошибка в start_quiz: {e}")
        print(f"Произошла ошибка: {e}. Викторина не завершена.")

def show_detailed_results(username):
    """
    Показывает детализированные результаты игр пользователя.
    """
    try:
        session = SessionLocal()
        user = session.query(User).filter_by(username=username).first()
        if not user or not user.quiz_results:
            print(f"У пользователя {username} пока нет результатов викторин.")
            session.close()
            return

        print(f"\n--- Детализированные результаты игр пользователя {username} ---")
        for result in user.quiz_results:
            print(f"Язык: {result.language}")
            print(f"Правильные ответы: {result.correct_answers}/{result.total_questions}")
            print("-" * 30)
        session.close()
    except Exception as e:
        log_error(f"Ошибка в show_detailed_results: {e}")
        print(f"Произошла ошибка: {e}.")
