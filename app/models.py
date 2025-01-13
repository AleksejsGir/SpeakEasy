import logging
from sqlalchemy.orm import Session
from app.db import User, SessionLocal

class UserManager:
    """
    Класс для работы с пользователями через базу данных.
    """

    def __init__(self, username):
        """
        Инициализация пользователя.
        Если пользователь не существует, создаём новую запись.
        """
        self.username = username
        self.session: Session = SessionLocal()

        # Проверяем, существует ли пользователь
        existing_user = self.session.query(User).filter(User.username == self.username).first()
        if not existing_user:
            new_user = User(username=self.username)
            self.session.add(new_user)
            self.session.commit()
            logging.info(f"Создана новая запись для пользователя {self.username}.")
        else:
            logging.info(f"Пользователь {self.username} инициализирован.")

    def delete(self):
        """
        Удаляет пользователя из базы данных.
        """
        try:
            user = self.session.query(User).filter(User.username == self.username).first()
            if user:
                self.session.delete(user)
                self.session.commit()
                print(f"Пользователь {self.username} удалён.")
                logging.info(f"Пользователь {self.username} удалён.")
            else:
                print(f"Пользователь {self.username} не найден.")
        except Exception as e:
            logging.error(f"Ошибка при удалении пользователя {self.username}: {e}")
            self.session.rollback()

    def change_username(self, new_name):
        """
        Изменяет имя пользователя.
        """
        try:
            user = self.session.query(User).filter(User.username == self.username).first()
            if not user:
                print(f"Пользователь {self.username} не найден.")
                return

            # Проверяем, не занято ли новое имя
            existing_user = self.session.query(User).filter(User.username == new_name).first()
            if existing_user:
                print("Имя уже занято. Попробуйте другое.")
                return

            user.username = new_name
            self.session.commit()
            self.username = new_name
            print(f"Имя пользователя изменено на {new_name}.")
            logging.info(f"Имя пользователя {self.username} изменено на {new_name}.")
        except Exception as e:
            logging.error(f"Ошибка при изменении имени пользователя {self.username}: {e}")
            self.session.rollback()

    def close_session(self):
        """
        Закрывает сессию базы данных.
        """
        self.session.close()
