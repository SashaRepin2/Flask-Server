from flask import render_template

from project import login_manager
from project.main import main


@main.app_errorhandler(404)
def error_404(e):
    return render_template('errors/404.html', error=404, error_text="Страница не найдена"), 404


@login_manager.unauthorized_handler
def error_401():
    return render_template('errors/404.html', error=401, error_text="Нет доступа"), 401
