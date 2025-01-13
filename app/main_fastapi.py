from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.db import SessionLocal, initialize_database, User, Word

# Создание FastAPI-приложения
app = FastAPI()

# Функция для подключения к базе данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Событие старта приложения
@app.on_event("startup")
async def startup():
    initialize_database()

# Главная страница
@app.get("/")
async def read_root():
    return {"message": "Добро пожаловать в SpeakEasy на FastAPI!"}

# --- Маршруты для пользователей ---

# Схема для создания пользователя
class UserCreate(BaseModel):
    username: str

# Получение всех пользователей
@app.get("/users/")
async def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return [{"id": user.id, "username": user.username} for user in users]

# Добавление нового пользователя
@app.post("/users/")
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = User(username=user.username)
    db.add(new_user)
    db.commit()
    return {"id": new_user.id, "username": new_user.username}

# Удаление пользователя
@app.delete("/users/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
        return {"message": f"Пользователь с ID {user_id} удалён"}
    return {"error": "Пользователь не найден"}

# --- Маршруты для работы со словами ---

# Схема для добавления слова
class WordCreate(BaseModel):
    language: str
    word: str
    translation: str

# Добавление нового слова
@app.post("/words/")
async def add_word(word: WordCreate, db: Session = Depends(get_db)):
    new_word = Word(language=word.language, word=word.word, translation=word.translation)
    db.add(new_word)
    db.commit()
    return {"id": new_word.id, "language": new_word.language, "word": new_word.word}

# Получение всех слов
@app.get("/words/")
async def get_words(db: Session = Depends(get_db)):
    words = db.query(Word).all()
    return [{"id": word.id, "language": word.language, "word": word.word, "translation": word.translation} for word in words]

# --- Маршруты для викторин ---

# Запуск викторины для пользователя
@app.post("/quiz/{username}/{language}/")
async def start_quiz(username: str, language: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return {"error": "Пользователь не найден"}

    words = db.query(Word).filter(Word.language == language).all()
    if not words:
        return {"error": "Словарь для языка отсутствует"}

    return {"message": f"Викторина для {username} на языке {language} готова", "words": [word.word for word in words]}
