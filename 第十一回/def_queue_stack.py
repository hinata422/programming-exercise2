class Queue:
    def __init__(self):
        self.list = []

    def enqueue(self, data):
        self.list.append(data)

    def dequeue(self):
        if len(self.list) == 0:
            return None
        return self.list.pop(0)

    def is_empty(self):
        return len(self.list) == 0


class Stack:
    def __init__(self):
        self.list = []

    def push(self, data):
        self.list.append(data)

    def pop(self):
        if len(self.list) == 0:
            return None
        return self.list.pop()

    def is_empty(self):
        return len(self.list) == 0
