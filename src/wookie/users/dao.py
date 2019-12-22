class UsersDAO(object):
    """"""
    def __init__(self, db):
        """
        Set the db reference
        """
        self._db = db

    def find_user_in_db(self, username, password):
        """
        Given a username and password find the User in db
        """
        for user in self._db['users']:
            if user['username'] == username and user['password'] == password:
                return user
        return None
