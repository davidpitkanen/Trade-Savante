
class queue:

    def __init__(self):
        self.first = self.Node()
        self.last = self.Node()
        self.N = 0

	class Node:
        def __init__(self, item=None, next=None):
            self.item = item
            self.next = next

    def isEmpty(self):
        return self.first == None

    def size(self):
        return self.N

    def enqueue(self, x):
        oldlast = self.last
        self.last = self.Node()
        self.last.item = x
        self.last.next = None
        if self.isEmpty():
            self.first = self.last
        else:
            oldlast.next = self.last
        self.N = self.N + 1

    def dequeue(self):
        item = self.first.item
        self.first = self.first.next
        self.N = self.N -1
        if self.isEmpty():
            self.last = None
        return item