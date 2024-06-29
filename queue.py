from collections import deque
from order import Order

class Queue:
    def __init__(self, name: str):
        self._name = name
        self._orders = deque()

    @property
    def name(self):
        return self._name

    @property
    def orders(self):
        return self._orders

    def enqueue(self, order: Order):
        self.orders.append(order)

    def dequeue(self):
        if not self.empty():
            return self.orders.popleft()

    def empty(self):
        return len(self._orders) == 0

    def size(self):
        return len(self._orders)