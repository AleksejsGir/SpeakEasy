import logging
from app.db import get_all_words, SessionLocal, QuizResult, User
from app.utils import log_error


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
    Начало викторины для пользователя.
    """
    try:
        words = get_all_words()
        language_words = [word for word in words if word.language == language]

        if not language_words:
            print(f"Словарь для языка {language} пуст или не найден.")
            logging.warning(f"Словарь для языка {language} отсутствует.")
            return

        correct_answers = 0
        total_questions = len(language_words)

        print(f"\nНачинаем викторину для пользователя {username}.")
        print("Введите перевод для каждого слова. Напишите 'exit', чтобы остановить викторину.\n")
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

        save_quiz_result(username, language, correct_answers, total_questions)
    except Exception as e:
        log_error(f"Ошибка в start_quiz: {e}")
        print(f"Произошла ошибка: {e}. Викторина не завершена.")


def save_quiz_result(username, language, correct_answers, total_questions):
    """
    Сохраняет результаты викторины в базу данных.
    """
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
