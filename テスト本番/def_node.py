# Nodeクラスの定義
class Node:
    def __init__(self, data, next=None):
        self.data = data
        self.next = next


def print_linked_list(top):
    names = []

    while top is not None:
        names.append(top.data.name)
        top = top.next

    print(" -> ".join(names))

