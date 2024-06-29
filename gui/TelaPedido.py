from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QMessageBox
from PySide6.QtCore import Qt

class TelaPedido(QWidget):
    def __init__(self, fazer_pedido_callback):
        super().__init__()
        
        self.fazer_pedido_callback = fazer_pedido_callback

        # Layout principal da tela de pedido
        self.main_layout = QVBoxLayout()

        # Título
        titulo = QLabel("Sanduichero - Faça seu pedido")
        titulo.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.main_layout.addWidget(titulo)

        # Criar os itens do menu
        self.items = [
            {"nome": "Coca cola", "descricao": "Bebida gaseificada de cola 500ml", "preco": 9.99, "quantidade_widget": None},
            {"nome": "Hamburguer", "descricao": "Pão de hamburguer, hamburguer, maionese, alface, tomate, queijo", "preco": 35.99, "quantidade_widget": None},
            {"nome": "Batata frita", "descricao": "Batatas fritas no óleo pequena", "preco": 17.99, "quantidade_widget": None}
        ]

        for item in self.items:
            self.criar_item(self.main_layout, item)
        
        # Botão Fazer Pedido
        self.fazer_pedido_button = QPushButton("Fazer Pedido")
        self.fazer_pedido_button.clicked.connect(self.fazer_pedido)
        self.main_layout.addWidget(self.fazer_pedido_button)
        
        # Definir o layout principal
        self.setLayout(self.main_layout)
    
    def criar_item(self, layout, item):
        item_layout = QVBoxLayout()
        
        # Layout horizontal para o nome, preço e controles de quantidade
        h_layout = QHBoxLayout()
        
        # Nome do item
        nome_label = QLabel(f"{item['nome']}")
        nome_label.setStyleSheet("font-size: 16px;")
        h_layout.addWidget(nome_label)
        
        # Preço
        preco_label = QLabel(f"R$ {item['preco']:.2f}")
        h_layout.addWidget(preco_label)
        
        # Controle de quantidade
        quantidade_widget = QuantityWidget()
        item["quantidade_widget"] = quantidade_widget
        h_layout.addWidget(quantidade_widget)
        
        # Adicionar layout horizontal ao layout do item
        item_layout.addLayout(h_layout)
        
        # Descrição do item
        descricao_label = QLabel(item["descricao"])
        descricao_label.setStyleSheet("font-size: 12px; color: gray;")
        item_layout.addWidget(descricao_label)
        
        # Adicionar item completo ao layout principal
        layout.addLayout(item_layout)
        layout.addSpacing(10)
    
    def get_items(self):
        return self.items

    def fazer_pedido(self):
        self.fazer_pedido_callback()
        for item in self.items:
            item["quantidade_widget"].reset_quantity()
        self.mostrar_notificacao()

    def mostrar_notificacao(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Pedido realizado")
        msg.setText("Pedido realizado com sucesso!")
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