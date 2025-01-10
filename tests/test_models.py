import pytest
from app.models import User
from app.utils import load_json, save_json

USERS_FILE = "data/users_data.json"

@pytest.fixture
def setup_user_data(tmp_path):
    """Фикстура для создания временного JSON-файла."""
    test_file = tmp_path / "test_users.json"
    test_data = {
        "Ivan": {
            "quiz_results": [
                {"language": "en-ru", "correct": 3, "total": 5}
            ]
        }
    }
    save_json(test_file, test_data)
    return test_file

def test_load_user_data(setup_user_data, monkeypatch):
    """Тест загрузки данных пользователя."""
    monkeypatch.setattr("app.models.USERS_FILE", str(setup_user_data))
    user = User("Ivan")
    assert user.username == "Ivan"
    assert len(user.data["quiz_results"]) == 1

def test_add_quiz_result(setup_user_data, monkeypatch):
    """Тест добавления результата викторины."""
    monkeypatch.setattr("app.models.USERS_FILE", str(setup_user_data))
    user = User("Ivan")
    user.add_quiz_result("fr-ru", 4, 5)
    assert len(user.data["quiz_results"]) == 2
    assert user.data["quiz_results"][1] == {
        "language": "fr-ru",
        "correct": 4,
        "total": 5
    }

def test_change_username(setup_user_data, monkeypatch):
    """Тест изменения имени пользователя."""
    monkeypatch.setattr("app.models.USERS_FILE", str(setup_user_data))
    user = User("Ivan")
    user.change_username("Maria")
    all_users = load_json(setup_user_data)
    assert "Maria" in all_users
    assert "Ivan" not in all_users

def test_delete_user(setup_user_data, monkeypatch):
    """Тест удаления пользователя."""
    monkeypatch.setattr("app.models.USERS_FILE", str(setup_user_data))
    user = User("Ivan")
    user.delete()
    all_users = load_json(setup_user_data)
    assert "Ivan" not in all_users
