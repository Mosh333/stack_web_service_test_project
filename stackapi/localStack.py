"""
Initial implementation from:
http://interactivepython.org/runestone/static/pythonds/BasicDS/ImplementingaStackinPython.html

With modification by Rob McLeod (403studiosca@gmail.com)
2015-12-24
    - Add clear method to clear all elements from the stack
"""
from abstractStack import AbstractStack


class LocalStack(AbstractStack):

    """ LocalStack class implementation using a list as a backing datatype."""
    def __init__(self):
        self.items = []

    def __str__(self):
        return str(self.items)

    def isEmpty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[len(self.items)-1]

    def size(self):
        return len(self.items)

    def clear(self):
        self.items = []
