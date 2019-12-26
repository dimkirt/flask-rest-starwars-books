from . import abstract_dao


class UsersMemoryDAO(abstract_dao.AbstractUsersDAO):
    """"""
    def __init__(self, db):
        """
        Set the db reference
        """
        self._db = db

    def find_user_by_credentials(self, username, password):
        """
        Given a username and password find the User in db
        """
        for user in self._db['users']:
            if user['username'] == username and user['password'] == password:
                return user
        return None
