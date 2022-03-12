from localStack import LocalStack
from localCollection import LocalCollection


class AbstractStackFactory(object):
    """
    AbstractStackFactory is effectively a generic interface to concrete
    factories of various implementations of the stack datastype.
    """
    @staticmethod
    def getStackFactory(factory):
        """ Returns a new instance of the Stack Factory. """
        if factory == 'LocalStack':
            return LocalStackFactory()
        elif factory == 'LocalCollection':
            return LocalCollectionFactory()
        raise NotImplementedError('Unknown Factory.')


class LocalStackFactory(object):
    """
    Concrete factory implmenetation for the Local Stack class.
    """
    def getStackFactory(self):
        """ Returns a new instance of the Local Stack class. """
        return LocalStack()


class LocalCollectionFactory(object):
    """
    Concrete factory implementation for the Local Collection class.
    """
    def getStackFactory(self):
        """ Returns a new instance of the Local Collection class."""
        return LocalCollection()
