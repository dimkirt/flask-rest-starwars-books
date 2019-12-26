import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from wookie.app import create_app
from wookie.db import db
from wookie.config import config

production_config = config['production']
production_config.DATABASE_URI = os.environ.get(
    'DATABASE_URI', 'sqlite:///wookie.sqlite.prod')

app = create_app(production_config)
from wookie.books.dao.sql_dao import Book  # noqa
from wookie.users.dao.sql_dao import User  # noqa

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
