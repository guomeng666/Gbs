# _*_ codding:utf-8 _*_
from app import create_app, db
from app.models import *
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from flask import render_template

app = create_app('default')


manager = Manager(app)
migrate = Migrate(app, db)


# User=User, BankType=BankType, Role=Role, Department=Department
def make_shell_context():
    return dict(app=app, db=db, Role=Role, User=User, Department=Department)


manager.add_command("shell", Shell(make_context=make_shell_context))
# 为脚本添加数据库迁移指令
manager.add_command('db', MigrateCommand)


@app.errorhandler(404)
def page_not_found(error):
    """
    404
    """
    return render_template("services/404.html"), 404


if __name__ == '__main__':
    manager.run()
    # app.run('127.0.0.1', 5000)



