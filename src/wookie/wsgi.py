from . import app

prod_app = app.create_app('production')

if __name__ == '__main__':
    prod_app.run()
