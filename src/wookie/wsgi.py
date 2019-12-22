from . import app

# Use in-memory storage for now
db = {
    'books': [{
        'id': 0,
        'title': 'This is the title',
        'author': 'This is the author',
        'description': 'This is the description',
        'price': 100,
        'cover':
        'https://upload.wikimedia.org/wikipedia/en/thumb/7/7d/Lenna_%28test_image%29.png/220px-Lenna_%28test_image%29.png',  # noqa
        'publisher': 666,  # id of the publisher
    }],
    'users': [{
        'id': 0,
        'username': 'jedi-master',
        'password': 'Test1234',
        'author_pseudonym': 'Luke'
    }]
}

prod_app = app.create_app(db)

if __name__ == '__main__':
    prod_app.run()
