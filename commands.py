from project import db
from run import app


@app.cli.command()
def addroles():
    from project.models import Role, Roles
    result = Role.insert_roles()
    is_all_roles_in_bd = False
    for role in result:
        print(f"Role name: {role['name']}, Success: {role['is_success']}")
        is_all_roles_in_bd = role['name'] in Roles

    print(f'Is roles has been added in DB {is_all_roles_in_bd}')


@app.cli.command()
def initroleuser():
    from project.models import User, Role, Roles
    users = User.query.all()

    count_change = 0
    for user in users:
        if user.role_id is None:
            role = Role.query.filter_by(name=Roles.USER.value).first()
            user.role_id = role.id
            print(f"User {user.email} has been change")
            count_change = count_change + 1

    db.session.commit()
    print(f'Count users:  {len(users)} User roles has been change: {count_change}')
