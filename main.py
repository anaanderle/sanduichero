from item import Item
from queue import Queue
from order import Order, OrderStatus

item1 = Item("Coca Cola", 9.99, "Bebida gaseificada de cola, 500ml")
item2 = Item("Hamburguer", 35.99, "Pão de hamburguer, hamburguer, maionese, alface, tomate, queijo")
item3 = Item("Batat frita", 17.99, "Batats fritas no óleo, pequena")
items = [item1, item2, item3]

queue = Queue("Em fila")
production = Queue("Em preparação")
finished = Queue("Entregue")

def createOrder(items: list):
    order = Order(OrderStatus.QUEUE, items)
    queue.enqueue(order)

def verify_item_in_list(list: list, item: Item):
    for list_item in list:
        if(list_item['item_id'] == item.id):
            return list_item
    return None

def generate_report():
    report = []

    for order in finished.orders:
        for order_item in order.items:
            current = verify_item_in_list(report, order_item)

            if(current != None):
                current['quantity'] += 1
                current['total'] += order_item.value
            else:
                report.append(
                    {
                        'item_id': order_item.id,
                        'quantity': 1,
                        'value': order_item.value,
                        'total': order_item.value,
                    }
                )
    return report

