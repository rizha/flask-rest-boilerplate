import os
from flask.ext.script import Manager, Shell

from app import mongo, create_app


app = create_app(os.getenv('FLASK_CONFIG') or 'local')

manager = Manager(app)

@manager.command
def tests():
    os.system('nosetests tests app')

def _make_shell_context():
    return dict(app=app, db=mongo)

manager.add_command('shell', Shell(make_context=_make_shell_context))

if __name__ == '__main__':
    manager.run()
