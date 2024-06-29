from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt

class StatusPedidos(QWidget):
    def __init__(self):
        super().__init__()

        # Layout principal da tela de status de pedidos
        main_layout = QVBoxLayout()

        # Título
        titulo = QLabel("Pedidos")
        titulo.setStyleSheet("font-size: 18px; font-weight: bold;")
        main_layout.addWidget(titulo)

        # Layout para as colunas
        self.columns_layout = QHBoxLayout()

        # Colunas
        self.fila_layout = self.adicionar_coluna("Na fila", [2, 7])
        self.preparacao_layout = self.adicionar_coluna("Em preparação", [1, 6])
        self.entregue_layout = self.adicionar_coluna("Entregue", [6, 4])

        # Adicionar o layout de colunas ao layout principal
        main_layout.addLayout(self.columns_layout)

        # Definir o layout principal
        self.setLayout(main_layout)
    
    def adicionar_coluna(self, titulo, pedidos):
        coluna_layout = QVBoxLayout()
        
        # Título da coluna
        titulo_label = QLabel(titulo)
        titulo_label.setAlignment(Qt.AlignCenter)
        titulo_label.setStyleSheet("font-size: 16px;")
        coluna_layout.addWidget(titulo_label)

        # Adicionar botões de pedidos
        for pedido in pedidos:
            pedido_button = QPushButton(str(pedido))
            pedido_button.setFixedSize(50, 50)
            pedido_button.clicked.connect(self.mover_pedido)
            coluna_layout.addWidget(pedido_button, alignment=Qt.AlignCenter)
        
        # Adicionar coluna ao layout
        self.columns_layout.addLayout(coluna_layout)
        return coluna_layout

    def mover_pedido(self):
        button = self.sender()
        current_layout = button.parent().layout()

        # Encontrar o índice do layout atual nas colunas principais
        current_index = self.columns_layout.indexOf(current_layout)

        # Mover para o próximo layout, se existir
        if current_index < self.columns_layout.count() - 1:
            next_layout = self.columns_layout.itemAt(current_index + 1).layout()
            current_layout.removeWidget(button)
            next_layout.addWidget(button, alignment=Qt.AlignCenter)