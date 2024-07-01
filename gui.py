from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QStackedWidget
from report import Report
from ProcessamentoPedidos import ProcessamentoPedidos
from orderScreen import OrderScreen
from orderStatusScreen import OrderStatusScreen
from item import Item
from queue import Queue
from order import Order, OrderStatus
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Menu Principal")
        self.setGeometry(100, 100, 800, 600)

        item1 = Item("Coca Cola", 9.99, "Bebida gaseificada de cola, 500ml")
        item2 = Item("Hamburguer", 35.99, "Pão de hamburguer, hamburguer, maionese, alface, tomate, queijo")
        item3 = Item("Batat frita", 17.99, "Batats fritas no óleo, pequena")
        self.items = [item1, item2, item3]

        self.queue = Queue("Em fila")
        self.production = Queue("Em preparação")
        self.finished = Queue("Entregue")

        layout = QVBoxLayout()

        self.buttons = {
            "Status dos Pedidos": QPushButton("Status dos Pedidos"),
            "Relatório de Vendas": QPushButton("Relatório de Vendas"),
            "Fazer Pedido": QPushButton("Fazer Pedido"),
        }

        for button in self.buttons.values():
            layout.addWidget(button)

        button_widget = QWidget()
        button_widget.setLayout(layout)

        self.stacked_widget = QStackedWidget()
        self.order_status = OrderStatusScreen(self.queue, self.production, self.finished, self.move_order)
        self.stacked_widget.addWidget(self.order_status)
        self.order_screen = OrderScreen(self.items, self.create_order, self.update_report, self.update_queue)
        self.stacked_widget.addWidget(self.order_screen)
        self.reports = Report()
        self.stacked_widget.addWidget(self.reports)

        main_layout = QVBoxLayout()
        main_layout.addWidget(button_widget)
        main_layout.addWidget(self.stacked_widget)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.buttons["Status dos Pedidos"].clicked.connect(self.show_queue)
        self.buttons["Relatório de Vendas"].clicked.connect(self.show_report)
        self.buttons["Fazer Pedido"].clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))


    def update_report(self):
        self.reports.update_table(self.generate_report())

    def show_report(self):
        self.reports.update_table(self.generate_report())
        self.stacked_widget.setCurrentIndex(2)

    def update_queue(self):
        self.order_status.update_layout(self.queue, self.production, self.finished)

    def show_queue(self):
        self.order_status.update_layout(self.queue, self.production, self.finished)
        self.stacked_widget.setCurrentIndex(0)

    def create_order(self, items: list):
        order = Order(OrderStatus.QUEUE, items)
        self.queue.enqueue(order)

    def move_order(self, orderId):
        for order in self.queue.orders:
            if(order.id == orderId):
                order_found = self.queue.dequeue()
                self.production.enqueue(order_found)
                self.update_queue()
                return

        for order in self.production.orders:
            if (order.id == orderId):
                order_found = self.production.dequeue()
                self.finished.enqueue(order_found)
                self.update_queue()
                return


    def generate_report(self):
        report = []
        total_items = []

        for order in self.finished.orders:
            for order_item in order.items:
                total_items.append(order_item)

        for item in self.items:
            quantity = 0
            for total_item in total_items:
                if(item.id == total_item.id):
                    quantity += 1

            report.append(
                {
                    'item': item,
                    'quantity': quantity,
                }
            )

        return report

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
