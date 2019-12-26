from abc import ABCMeta, abstractmethod


class AbstractUsersDAO(metaclass=ABCMeta):
    """
    Defines the interface for the User data access objects
    """
    @abstractmethod
    def find_user_by_credentials(self, username, password):
        raise NotImplementedError

    @abstractmethod
    def find_user_by_id(self, userid):
        raise NotImplementedError
