import logging
from sqlalchemy.orm import Session
from app.db import User, SessionLocal, QuizResult


class UserManager:
    """
    Класс для работы с пользователями через базу данных.
    """

    def __init__(self, username):
        """
        Инициализация объекта пользователя.
        """
        self.username = username
        self.session: Session = SessionLocal()

    def create_user(self):
        """
        Создаёт нового пользователя, если он не существует.
        """
        try:
            existing_user = self.session.query(User).filter(User.username == self.username).first()
            if not existing_user:
                new_user = User(username=self.username)
                self.session.add(new_user)
                self.session.commit()
                logging.info(f"Создана новая запись для пользователя {self.username}.")
            else:
                logging.info(f"Пользователь {self.username} уже существует.")
        except Exception as e:
            logging.error(f"Ошибка при создании пользователя {self.username}: {e}")
            self.session.rollback()
            raise

    def delete(self):
        """
        Удаляет пользователя из базы данных.
        """
        try:
            user = self.session.query(User).filter(User.username == self.username).first()
            if user:
                self.session.delete(user)
                self.session.commit()
                logging.info(f"Пользователь {self.username} удалён.")
            else:
                logging.warning(f"Пользователь {self.username} не найден.")
        except Exception as e:
            logging.error(f"Ошибка при удалении пользователя {self.username}: {e}")
            self.session.rollback()
            raise
        finally:
            self.close_session()

    def change_username(self, new_name):
        """
        Изменяет имя пользователя.
        """
        try:
            user = self.session.query(User).filter(User.username == self.username).first()
            if not user:
                logging.warning(f"Пользователь {self.username} не найден.")
                return

            # Проверяем, не занято ли новое имя
            existing_user = self.session.query(User).filter(User.username == new_name).first()
            if existing_user:
                logging.warning(f"Имя пользователя {new_name} уже занято.")
                return

            user.username = new_name
            self.session.commit()
            logging.info(f"Имя пользователя {self.username} изменено на {new_name}.")
            self.username = new_name
        except Exception as e:
            logging.error(f"Ошибка при изменении имени пользователя {self.username}: {e}")
            self.session.rollback()
            raise
        finally:
            self.close_session()

    def get_quiz_results(self):
        """
        Получает все результаты викторин для пользователя.
        """
        try:
            user = self.session.query(User).filter(User.username == self.username).first()
            if not user:
                logging.warning(f"Пользователь {self.username} не найден.")
                return []

            results = self.session.query(QuizResult).filter(QuizResult.user_id == user.id).all()
            return results
        except Exception as e:
            logging.error(f"Ошибка при получении результатов викторины пользователя {self.username}: {e}")
            raise
        finally:
            self.close_session()

    def close_session(self):
        """
        Закрывает сессию базы данных.
        """
        if self.session:
            self.session.close()
            logging.info(f"Сессия для пользователя {self.username} закрыта.")
