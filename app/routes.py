from flask import Blueprint

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    return "Добро пожаловать в Learn & Speak Pro!"
