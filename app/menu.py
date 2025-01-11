import logging
from app.models import User
from app.utils import load_json, save_json, log_error


def main_menu():
    current_user = None  # Текущий пользователь

    # Приветствие
    logging.info("Запуск главного меню.")
    print("\nДобро пожаловать в программу \"SpeakEasy\"!")

    while True:
        try:
            if current_user:
                print(f"\n--- Меню пользователя {current_user.username} ---")
                print("1. Пройти викторину")
                print("2. Просмотреть статистику")
                print("3. Изменить имя пользователя")
                print("4. Посмотреть детализированные результаты игр")
                print("5. Удалить пользователя")
                print("6. Сбросить статистику")
                print("7. Вернуться в главное меню")
                choice = input("Ваш выбор: ")

                if choice == "1":
                    language = select_language()
                    start_quiz(current_user, language)
                elif choice == "2":
                    current_user.show_statistics()
                elif choice == "3":
                    new_name = input("Введите новое имя пользователя: ")
                    current_user.change_username(new_name)
                elif choice == "4":
                    current_user.show_detailed_results()
                elif choice == "5":
                    confirm = input(f"Вы уверены, что хотите удалить пользователя {current_user.username}? (да/нет): ")
                    if confirm.lower() == "да":
                        current_user.delete()
                        logging.info(f"Пользователь {current_user.username} удалён.")
                        current_user = None
                elif choice == "6":
                    current_user.reset_statistics()
                    logging.info(f"Статистика пользователя {current_user.username} сброшена.")
                elif choice == "7":
                    current_user = None
                    logging.info("Возврат в главное меню.")
                else:
                    print("Неверный выбор. Попробуйте снова.")
            else:
                print("\n--- Главное меню ---")
                print("1. Выбрать или добавить пользователя")
                print("2. Просмотреть всех пользователей и их статистику")
                print("3. Выйти")
                choice = input("Ваш выбор: ")

                if choice == "1":
                    username = input("Введите имя пользователя (или добавьте нового): ")
                    current_user = User(username)
                    logging.info(f"Пользователь {username} выбран.")
                    print(f"Добро пожаловать {username}")
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
    """Выводит всех пользователей и их статистику."""
    try:
        data = load_json("data/users_data.json")
        if not data:
            print("Нет зарегистрированных пользователей.")
            logging.info("Запрос всех пользователей: данных нет.")
            return

        print("\n--- Все пользователи и их статистика ---")
        for index, (username, user_data) in enumerate(data.items(), start=1):
            quiz_results = user_data.get("quiz_results", [])
            total_games = len(quiz_results)
            total_correct_answers = sum(result.get("correct", 0) for result in quiz_results)

            print(f"{index}. Пользователь: {username}")
            print(f"  - Количество игр: {total_games}")
            print(f"  - Правильных ответов: {total_correct_answers}")
            print("-" * 30)
        logging.info("Запрос всех пользователей: данные выведены успешно.")
    except Exception as e:
        log_error(f"Ошибка в show_all_users: {e}")
        print(f"Произошла ошибка: {e}.")


def select_language():
    while True:
        try:
            print("\n--- Выберите язык для викторины ---")
            print("1. Английский → Русский")
            print("2. Испанский → Русский")
            print("3. Немецкий → Русский")
            print("4. Французский → Русский")
            choice = input("Ваш выбор: ")

            if choice == "1":
                return "en-ru"
            elif choice == "2":
                return "es-ru"
            elif choice == "3":
                return "de-ru"
            elif choice == "4":
                return "fr-ru"
            else:
                print("Неверный выбор. Попробуйте снова.")
        except Exception as e:
            log_error(f"Ошибка в select_language: {e}")
            print(f"Произошла ошибка: {e}.")


def start_quiz(user, language):
    try:
        words = load_json(f"data/{language}.json")
        if not words:
            print(f"Словарь для языка {language} пуст или не найден.")
            logging.warning(f"Словарь для языка {language} отсутствует.")
            return

        correct_answers = 0
        total_questions = len(words)

        print(f"\nНачинаем викторину для пользователя {user.username}.")
        print("Введите перевод для каждого слова. Напишите 'exit', чтобы остановить викторину в любой момент.\n")
        logging.info(f"Викторина для пользователя {user.username} начата (язык: {language}).")

        for word, translation in words.items():
            answer = input(f"Что означает слово '{word}'? ").strip()
            if answer.lower() == "exit":
                print("Викторина остановлена.")
                logging.info(f"Викторина для пользователя {user.username} остановлена.")
                break
            if answer.lower() == translation.lower():
                print("Правильно!")
                correct_answers += 1
            else:
                print(f"Неправильно. Правильный ответ: {translation}")

        print("\nВикторина завершена.")
        print(f"Вы ответили правильно на {correct_answers} из {total_questions} вопросов.")
        logging.info(f"Викторина завершена для пользователя {user.username}: {correct_answers}/{total_questions}.")

        # Сохраняем результаты
        user.add_quiz_result(language, correct_answers, total_questions)
    except Exception as e:
        log_error(f"Ошибка в start_quiz: {e}")
        print(f"Произошла ошибка: {e}. Викторина не была завершена.")
