from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QMessageBox
from PySide6.QtCore import Qt
from queue import Queue

class OrderScreen(QWidget):
    def __init__(self, items: list, create_order, generate_report, update_queue):
        super().__init__()

        self.create_order = create_order
        self.generate_report = generate_report
        self.update_queue = update_queue

        self.main_layout = QVBoxLayout()

        title = QLabel("Sanduichero - Faça seu pedido")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.main_layout.addWidget(title)

        self.items_with_quantity = []

        for item in items:
            self.items_with_quantity.append({'item': item, 'quantity': 0})

        for item_with_quantity in self.items_with_quantity:
            self.create_item(self.main_layout, item_with_quantity)
        
        self.do_order_button = QPushButton("Fazer Pedido")
        self.do_order_button.clicked.connect(self.do_order)
        self.main_layout.addWidget(self.do_order_button)

        self.setLayout(self.main_layout)
    
    def create_item(self, layout, item_with_quantity):
        item_layout = QVBoxLayout()
        
        h_layout = QHBoxLayout()
        
        name_label = QLabel(f"{item_with_quantity['item'].name}")
        name_label.setStyleSheet("font-size: 16px;")
        h_layout.addWidget(name_label)
        
        price_label = QLabel(f"R$ {item_with_quantity['item'].value:.2f}")
        h_layout.addWidget(price_label)
        
        quantity_widget = QuantityWidget()
        item_with_quantity['quantity'] = quantity_widget
        h_layout.addWidget(quantity_widget)
        
        item_layout.addLayout(h_layout)
        
        description_label = QLabel(item_with_quantity['item'].description)
        description_label.setStyleSheet("font-size: 12px; color: gray;")
        item_layout.addWidget(description_label)
        
        layout.addLayout(item_layout)
        layout.addSpacing(10)

    def do_order(self):
        items = []
        for item_quantity in self.items_with_quantity:
            count = 0
            while(count < item_quantity['quantity'].get_quantity()):
                items.append(item_quantity['item'])
                count += 1

            item_quantity['quantity'].reset_quantity()

        if(len(items) == 0):
            self.not_confirmed_order()
            return

        self.create_order(items)
        self.generate_report()
        self.update_queue()
        self.confirmed_order()

    def confirmed_order(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Pedido realizado")
        msg.setText("Pedido realizado com sucesso!")
        msg.exec()

    def not_confirmed_order(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Pedido não realizado")
        msg.setText("Nenhum item adicionado!")
        msg.exec()

class QuantityWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.quantity = 0
        
        layout = QHBoxLayout()
        
        self.decrease_button = QPushButton("-")
        self.decrease_button.clicked.connect(self.decrease_quantity)
        layout.addWidget(self.decrease_button)
        
        self.quantity_label = QLabel(str(self.quantity))
        self.quantity_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.quantity_label)
        
        self.increase_button = QPushButton("+")
        self.increase_button.clicked.connect(self.increase_quantity)
        layout.addWidget(self.increase_button)
        
        self.setLayout(layout)
    
    def decrease_quantity(self):
        if self.quantity > 0:
            self.quantity -= 1
        self.quantity_label.setText(str(self.quantity))
    
    def increase_quantity(self):
        self.quantity += 1
        self.quantity_label.setText(str(self.quantity))
    
    def get_quantity(self):
        return self.quantity

    def reset_quantity(self):
        self.quantity = 0
        self.quantity_label.setText(str(self.quantity))