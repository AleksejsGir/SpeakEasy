from app.utils import load_json, save_json

USERS_FILE = "data/users_data.json"

class User:
    """Класс для работы с пользователями."""

    def __init__(self, username):
        """
        Инициализация пользователя.
        Загружает данные пользователя или создаёт новую запись, если пользователь не существует.
        """
        self.username = username
        self.data = self.load_user_data()

    def load_user_data(self):
        """Загружает данные пользователя из JSON файла."""
        all_users = load_json(USERS_FILE)
        if self.username not in all_users:
            all_users[self.username] = {"quiz_results": []}
            save_json(USERS_FILE, all_users)
        return all_users[self.username]

    def save(self):
        """Сохраняет данные пользователя в файл JSON."""
        all_users = load_json(USERS_FILE)
        all_users[self.username] = self.data
        save_json(USERS_FILE, all_users)

    def add_quiz_result(self, language, correct, total):
        """Добавляет результат викторины в данные пользователя."""
        if "quiz_results" not in self.data:
            self.data["quiz_results"] = []
        self.data["quiz_results"].append({
            "language": language,
            "correct": correct,
            "total": total
        })
        self.save()

    def show_statistics(self):
        """Выводит общую статистику пользователя."""
        stats = self.data.get("quiz_results", [])
        total_games = len(stats)
        total_correct = sum(result["correct"] for result in stats)
        print(f"\nПользователь: {self.username}")
        print(f"Количество игр: {total_games}")
        print(f"Правильных ответов: {total_correct}")

    def show_detailed_results(self):
        """Выводит детализированные результаты игр пользователя."""
        stats = self.data.get("quiz_results", [])
        print(f"\nДетализированные результаты игр пользователя {self.username}:")
        for i, result in enumerate(stats, start=1):
            print(f"{i}. Игра: {result['correct']} правильных ответов из {result['total']} (Язык: {result['language']})")

    def change_username(self, new_name):
        """Изменяет имя пользователя."""
        all_users = load_json(USERS_FILE)
        if new_name in all_users:
            print("Имя уже занято. Попробуйте другое.")
            return
        all_users[new_name] = all_users.pop(self.username)
        save_json(USERS_FILE, all_users)
        self.username = new_name
        self.data = all_users[new_name]
        print(f"Имя пользователя изменено на {new_name}.")

    def delete(self):
        """Удаляет данные пользователя."""
        all_users = load_json(USERS_FILE)
        if self.username in all_users:
            del all_users[self.username]
            save_json(USERS_FILE, all_users)
            print(f"Пользователь {self.username} удалён.")

    def reset_statistics(self):
        """Сбрасывает статистику пользователя."""
        self.data["quiz_results"] = []
        self.save()
        print("Статистика успешно сброшена.")