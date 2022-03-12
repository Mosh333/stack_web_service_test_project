from abc import ABCMeta, abstractmethod


class AbstractStack(object):
    """
    AbstractStack base class. All derived classes must provide a concrete
    implementation to these methods.
    """
    __metaclass__ = ABCMeta

    """ Check if the stack is empty. """
    @abstractmethod
    def isEmpty(self):
        return

    """ Add item to the stack. """
    @abstractmethod
    def push(self, item):
        return

    """ Retrieve the topmost item and remove it from the stack. """
    @abstractmethod
    def pop(self):
        return

    """ Retrieve the topmost item from the stack. """
    @abstractmethod
    def peek(self):
        return

    """ Retrieve the number of elements in the stack. """
    @abstractmethod
    def size(self):
        return

    """ Clear the stack. Remove all elements. """
    @abstractmethod
    def clear(self):
        return
