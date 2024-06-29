from enum import Enum


class OrderStatus(Enum):
    QUEUE = "Em fila"
    PRODUCTION = "Em produção"
    FINISHED = "Entregue"


class Order:
    last_id = 1

    def __init__(self, status: OrderStatus, items: list):
        self._status = status
        self._items = items
        self._id = Order.last_id
        Order.last_id += 1

    @property
    def id(self):
        return self._id

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status: OrderStatus):
        self._status = status

    @property
    def items(self):
        return self._items

    @items.setter
    def items(self, items: list):
        self._items = items
