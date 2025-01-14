import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db import Base, User, Word


@pytest.fixture
def test_session():
    """
    Фикстура для создания тестовой базы данных SQLite в памяти.
    """
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    TestingSessionLocal = sessionmaker(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()
    engine.dispose()


def test_add_user(test_session):
    """
    Тест добавления пользователей в базу данных.
    """
    user = User(username="Aleksej")
    test_session.add(user)
    test_session.commit()

    users = test_session.query(User).all()
    assert len(users) == 1
    assert users[0].username == "Aleksej"


def test_add_word(test_session):
    """
    Тест добавления слов в базу данных.
    """
    word = Word(language="en", word="cat", translation="кот")
    test_session.add(word)
    test_session.commit()

    words = test_session.query(Word).all()
    assert len(words) == 1
    assert words[0].word == "cat"
    assert words[0].translation == "кот"


def test_get_all_users(test_session):
    """
    Тест получения всех пользователей.
    """
    test_session.add(User(username="Aleksej"))
    test_session.add(User(username="Linda"))
    test_session.commit()

    users = test_session.query(User).all()
    assert len(users) == 2
    assert users[0].username == "Aleksej"
    assert users[1].username == "Linda"


def test_get_all_words(test_session):
    """
    Тест получения всех слов.
    """
    test_session.add(Word(language="en", word="cat", translation="кот"))
    test_session.add(Word(language="en", word="dog", translation="собака"))
    test_session.commit()

    words = test_session.query(Word).all()
    assert len(words) == 2
    assert words[0].word == "cat"
    assert words[1].word == "dog"
