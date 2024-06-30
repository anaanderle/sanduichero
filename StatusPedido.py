from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt

class StatusPedidos(QWidget):
    def __init__(self, queue, production, finished, mover_pedido):
        super().__init__()

        self.mover_pedido = mover_pedido

        # Layout principal da tela de status de pedidos
        main_layout = QVBoxLayout()

        # Título
        titulo = QLabel("Pedidos")
        titulo.setStyleSheet("font-size: 18px; font-weight: bold;")
        main_layout.addWidget(titulo)

        # Layout para as colunas
        self.columns_layout = QHBoxLayout()
        main_layout.addLayout(self.columns_layout)

        # Definir o layout principal
        self.setLayout(main_layout)

        # Inicializar o dicionário para armazenar os layouts das colunas
        self.colunas = {}

        # Chamar update_layout para configurar as colunas iniciais
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

        # Atualizar ou adicionar colunas conforme necessário
        self.adicionar_ou_atualizar_coluna("Na fila", queue_orders)
        self.adicionar_ou_atualizar_coluna("Em preparação", production_orders)
        self.adicionar_ou_atualizar_coluna("Entregue", finished_orders)

    def adicionar_ou_atualizar_coluna(self, titulo, pedidos):
        if titulo in self.colunas:
            coluna_layout, _ = self.colunas[titulo]  # Obter o layout da coluna
            self.atualizar_valores_coluna(coluna_layout, pedidos)
        else:
            coluna_layout, nome_coluna = self.adicionar_coluna(titulo, pedidos)
            self.colunas[nome_coluna] = (coluna_layout, nome_coluna)

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
            pedido_button.clicked.connect(lambda: self.mover_pedido(pedido))
            coluna_layout.addWidget(pedido_button, alignment=Qt.AlignCenter)

        # Adicionar coluna ao layout principal
        self.columns_layout.addLayout(coluna_layout)

        # Retornar layout da coluna e título
        return coluna_layout, titulo

    def atualizar_valores_coluna(self, coluna_layout, novos_pedidos):
        # Limpar widgets existentes da coluna
        while coluna_layout.count() > 1:
            child = coluna_layout.takeAt(1)
            if child.widget():
                child.widget().deleteLater()

        # Adicionar novos botões de pedidos
        for pedido in novos_pedidos:
            pedido_button = QPushButton(str(pedido))
            pedido_button.setFixedSize(50, 50)
            pedido_button.clicked.connect(lambda: self.mover_pedido(pedido))
            coluna_layout.addWidget(pedido_button, alignment=Qt.AlignCenter)
