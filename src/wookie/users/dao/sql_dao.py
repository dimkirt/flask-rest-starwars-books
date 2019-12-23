from . import abstract_dao
from ...db import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    author_pseudonym = db.Column(db.String(80), unique=True, nullable=False)
    books = db.relationship('Book',
                            lazy='select',
                            backref=db.backref('user', lazy='joined'))

    def __repr__(self):
        return '<User %r>' % self.username

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class UsersSQLDAO(abstract_dao.AbstractUsersDAO):
    """
    Implements the in sql data access object for the Books
    """
    def find_user_in_db(self, username, password):
        user = User.query.filter_by(username=username,
                                    password=password).first()
        return user.as_dict()
