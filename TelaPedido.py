from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QMessageBox
from PySide6.QtCore import Qt
from queue import Queue

class TelaPedido(QWidget):
    def __init__(self, queue: Queue, items: list, create_order, generate_report):
        super().__init__()

        self.create_order = create_order
        self.generate_report = generate_report

        # Layout principal da tela de pedido
        self.main_layout = QVBoxLayout()

        # Título
        titulo = QLabel("Sanduichero - Faça seu pedido")
        titulo.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.main_layout.addWidget(titulo)

        self.items_with_quantity = []

        for item in items:
            self.items_with_quantity.append({'item': item, 'quantity': 0})

        for item_with_quantity in self.items_with_quantity:
            self.criar_item(self.main_layout, item_with_quantity)
        
        # Botão Fazer Pedido
        self.fazer_pedido_button = QPushButton("Fazer Pedido")
        self.fazer_pedido_button.clicked.connect(self.fazer_pedido)
        self.main_layout.addWidget(self.fazer_pedido_button)
        
        # Definir o layout principal
        self.setLayout(self.main_layout)
    
    def criar_item(self, layout, item_with_quantity):
        item_layout = QVBoxLayout()
        
        # Layout horizontal para o nome, preço e controles de quantidade
        h_layout = QHBoxLayout()
        
        # Nome do item
        nome_label = QLabel(f"{item_with_quantity['item'].name}")
        nome_label.setStyleSheet("font-size: 16px;")
        h_layout.addWidget(nome_label)
        
        # Preço
        preco_label = QLabel(f"R$ {item_with_quantity['item'].value:.2f}")
        h_layout.addWidget(preco_label)
        
        # Controle de quantidade
        quantidade_widget = QuantityWidget()
        item_with_quantity['quantity'] = quantidade_widget
        h_layout.addWidget(quantidade_widget)
        
        # Adicionar layout horizontal ao layout do item
        item_layout.addLayout(h_layout)
        
        # Descrição do item
        descricao_label = QLabel(item_with_quantity['item'].description)
        descricao_label.setStyleSheet("font-size: 12px; color: gray;")
        item_layout.addWidget(descricao_label)
        
        # Adicionar item completo ao layout principal
        layout.addLayout(item_layout)
        layout.addSpacing(10)

    def fazer_pedido(self):
        items = []
        for item_quantity in self.items_with_quantity:
            count = 0
            while(count < item_quantity['quantity'].get_quantity()):
                items.append(item_quantity['item'])
                count += 1

            item_quantity['quantity'].reset_quantity()

        if(len(items) == 0):
            self.nenhum_item()
            return

        self.create_order(items)
        self.generate_report()
        self.pedido_confirmado()

    def pedido_confirmado(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Pedido realizado")
        msg.setText("Pedido realizado com sucesso!")
        msg.exec()

    def nenhum_item(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Pedido não realizado")
        msg.setText("Nenhum item adicionado!")
        msg.exec()

class QuantityWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.quantity = 0
        
        # Layout horizontal
        layout = QHBoxLayout()
        
        # Botão de diminuir
        self.decrease_button = QPushButton("-")
        self.decrease_button.clicked.connect(self.decrease_quantity)
        layout.addWidget(self.decrease_button)
        
        # Rótulo da quantidade
        self.quantity_label = QLabel(str(self.quantity))
        self.quantity_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.quantity_label)
        
        # Botão de aumentar
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