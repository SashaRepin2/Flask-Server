from flask_login import login_required

from project.admin import admin, controller
from project.decorators import permission_required
from project.models import Roles


@admin.route('/panel/', methods=['POST', 'GET'])
@admin.route('/panel/<int:page>', methods=['POST', 'GET'])
@login_required
@permission_required(Roles.ADMIN.value)
def admin_panel(page=1):
    return controller.admin_panel(page)


@admin.route('/accepted-blog/<int:id>', methods=['POST'])
@login_required
@permission_required(Roles.ADMIN.value)
def accepted_blog(id):
    return controller.accepted_blog(id)


@admin.route('/get-admin-role', methods=['POST', 'GET'])
@login_required
def get_admin_role():
    return controller.get_admin_role()
