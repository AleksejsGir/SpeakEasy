import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db import Base, User, QuizResult

@pytest.fixture
def test_db():
    """
    Фикстура для настройки тестовой базы данных SQLite.
    """
    # Создаём тестовый движок SQLite (в памяти)
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    TestingSessionLocal = sessionmaker(bind=engine)
    return TestingSessionLocal()

def test_add_user(test_db):
    """
    Тест добавления пользователя.
    """
    session = test_db
    new_user = User(username="Ivan")
    session.add(new_user)
    session.commit()
    user = session.query(User).filter_by(username="Ivan").first()
    assert user is not None
    assert user.username == "Ivan"

def test_add_quiz_result(test_db):
    """
    Тест добавления результата викторины.
    """
    session = test_db
    # Добавляем пользователя
    new_user = User(username="Ivan")
    session.add(new_user)
    session.commit()

    # Добавляем результат викторины
    quiz_result = QuizResult(user_id=new_user.id, language="en", correct_answers=4, total_questions=5)
    session.add(quiz_result)
    session.commit()

    results = session.query(QuizResult).filter_by(user_id=new_user.id).all()
    assert len(results) == 1
    assert results[0].language == "en"
    assert results[0].correct_answers == 4
    assert results[0].total_questions == 5

def test_change_username(test_db):
    """
    Тест изменения имени пользователя.
    """
    session = test_db
    new_user = User(username="Ivan")
    session.add(new_user)
    session.commit()

    # Изменяем имя пользователя
    user = session.query(User).filter_by(username="Ivan").first()
    user.username = "Maria"
    session.commit()

    updated_user = session.query(User).filter_by(username="Maria").first()
    assert updated_user is not None
    assert updated_user.username == "Maria"

def test_delete_user(test_db):
    """
    Тест удаления пользователя.
    """
    session = test_db
    new_user = User(username="Ivan")
    session.add(new_user)
    session.commit()

    # Удаляем пользователя
    user = session.query(User).filter_by(username="Ivan").first()
    session.delete(user)
    session.commit()

    deleted_user = session.query(User).filter_by(username="Ivan").first()
    assert deleted_user is None
