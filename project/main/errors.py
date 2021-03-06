from flask import render_template

from project import login_manager
from project.main import main


@main.app_errorhandler(404)
def error_404(e):
    return render_template('errors/404.html', error=404, error_text="Страница не найдена"), 404


@login_manager.unauthorized_handler
def error_401():
    return render_template('errors/404.html', error=401, error_text="Не авторизован"), 401


@main.app_errorhandler(403)
def error_403(e):
    return render_template('errors/404.html', error=403, error_text="Нет прав"), 403

@main.app_errorhandler(405)
def error_404(e):
    return render_template('errors/404.html', error=405, error_text="Метод не поддерживается"), 405