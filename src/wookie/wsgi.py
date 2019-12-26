from . import app
from .config import config

prod_app = app.create_app(config=config['production'])

if __name__ == '__main__':
    prod_app.run()
