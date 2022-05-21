from flask_login import login_required
from project.auth import auth, controller
from project.decorators import login_not_required


@auth.route('/register', methods=['POST', 'GET'])
@login_not_required
def register():
    return controller.register()


@auth.route('/login', methods=['GET', 'POST'])
@login_not_required
def login():
    return controller.login()


@auth.route('/logout', endpoint='logout')
@login_required
def logout():
    return controller.logout()


@auth.route('/confirm/<link>')
def confirm(link):
    return controller.confirm(link)
