import os
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

# Настройки базы данных
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, '../data/data.db')
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# Подключение к базе данных
engine = create_engine(DATABASE_URL, echo=False)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)

# Определение моделей
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    quiz_results = relationship("QuizResult", back_populates="user", cascade="all, delete-orphan")


class Word(Base):
    __tablename__ = "words"

    id = Column(Integer, primary_key=True, index=True)
    language = Column(String, nullable=False)
    word = Column(String, nullable=False)
    translation = Column(String, nullable=False)


class QuizResult(Base):
    __tablename__ = "quiz_results"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    language = Column(String, nullable=False)
    correct_answers = Column(Integer, nullable=False)
    total_questions = Column(Integer, nullable=False)

    user = relationship("User", back_populates="quiz_results")

# Инициализация базы данных
def initialize_database():
    """
    Создаёт таблицы в базе данных, если их ещё нет.
    """
    Base.metadata.create_all(bind=engine)

# Функции для работы с базой данных
def add_user(username: str):
    """
    Добавляет нового пользователя в базу данных.
    """
    session = SessionLocal()
    try:
        new_user = User(username=username)
        session.add(new_user)
        session.commit()
        print(f"Пользователь '{username}' успешно добавлен!")
    except Exception as e:
        print(f"Ошибка добавления пользователя: {e}")
        session.rollback()
    finally:
        session.close()

def get_all_users():
    """
    Возвращает список всех пользователей из базы данных.
    """
    session = SessionLocal()
    try:
        return session.query(User).all()
    finally:
        session.close()

def add_word(language: str, word: str, translation: str):
    """
    Добавляет новое слово в базу данных.
    """
    session = SessionLocal()
    try:
        new_word = Word(language=language, word=word, translation=translation)
        session.add(new_word)
        session.commit()
        print(f"Слово '{word}' ({language}) успешно добавлено!")
    except Exception as e:
        print(f"Ошибка добавления слова: {e}")
        session.rollback()
    finally:
        session.close()

def get_all_words():
    """
    Возвращает список всех слов из базы данных.
    """
    session = SessionLocal()
    try:
        return session.query(Word).all()
    finally:
        session.close()

def save_quiz_result(user_id: int, language: str, correct_answers: int, total_questions: int):
    """
    Сохраняет результат викторины в базу данных.
    """
    session = SessionLocal()
    try:
        new_result = QuizResult(
            user_id=user_id,
            language=language,
            correct_answers=correct_answers,
            total_questions=total_questions,
        )
        session.add(new_result)
        session.commit()
        print("Результат викторины успешно сохранён!")
    except Exception as e:
        print(f"Ошибка сохранения результата викторины: {e}")
        session.rollback()
    finally:
        session.close()
