from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt

class OrderStatusScreen(QWidget):
    def __init__(self, queue, production, finished, move_order):
        super().__init__()

        self.move_order = move_order

        main_layout = QVBoxLayout()

        title = QLabel("Pedidos")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        main_layout.addWidget(title)

        self.columns_layout = QHBoxLayout()
        main_layout.addLayout(self.columns_layout)

        self.setLayout(main_layout)

        self.columns = {}

        self.update_layout(queue, production, finished)

    def update_layout(self, queue, production, finished):
        queue_orders = []
        production_orders = []
        finished_orders = []

        for order in queue.orders:
            queue_orders.append(order.id)

        for order in production.orders:
            production_orders.append(order.id)

        for order in finished.orders:
            finished_orders.append(order.id)

        self.add_or_update_column("Na fila", queue_orders)
        self.add_or_update_column("Em preparação", production_orders)
        self.add_or_update_column("Entregue", finished_orders)

    def add_or_update_column(self, title, orders):
        if title in self.columns:
            column_layout, _ = self.columns[title]
            self.update_column(column_layout, orders)
        else:
            column_layout, name_column = self.add_column(title, orders)
            self.columns[name_column] = (column_layout, name_column)

    def add_column(self, title, orders):
        column_layout = QVBoxLayout()

        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 16px;")
        column_layout.addWidget(title_label)

        for order in orders:
            order_button = QPushButton(str(order))
            order_button.setFixedSize(50, 50)
            order_button.clicked.connect(lambda: self.move_order(order))
            column_layout.addWidget(order_button, alignment=Qt.AlignCenter)

        self.columns_layout.addLayout(column_layout)

        return column_layout, title

    def update_column(self, column_layout, new_orders):
        while column_layout.count() > 1:
            child = column_layout.takeAt(1)
            if child.widget():
                child.widget().deleteLater()

        for order in new_orders:
            order_button = QPushButton(str(order))
            order_button.setFixedSize(50, 50)
            order_button.clicked.connect(lambda: self.move_order(order))
            column_layout.addWidget(order_button, alignment=Qt.AlignCenter)
