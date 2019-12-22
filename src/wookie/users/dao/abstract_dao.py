from abc import ABCMeta, abstractmethod


class AbstractUsersDAO(metaclass=ABCMeta):
    """
    Defines the interface for the User data access objects
    """
    @abstractmethod
    def find_user_in_db(self, username, password):
        raise NotImplementedError
