from abstractStack import AbstractStack
from collections import deque


class LocalCollection(AbstractStack):
    """
    LocalCollection class implementation using a collection as a backing
    datatype.
    """
    def __init__(self):
        self.items = deque()

    def __str__(self):
        return str(self.items)

    def isEmpty(self):
        return False if self.items else True

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
