from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QStackedWidget, QTableWidget, QTableWidgetItem, QMessageBox
from PySide6.QtCore import Qt
import sys

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

class TelaPedido(QWidget):
    def __init__(self, fazer_pedido_callback):
        super().__init__()
        
        self.fazer_pedido_callback = fazer_pedido_callback

        # Layout principal da tela de pedido
        self.main_layout = QVBoxLayout()

        # Título
        titulo = QLabel("Sanduíches")
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

class ProcessamentoPedidos(QWidget):
    def __init__(self):
        super().__init__()

        # Layout principal da tela de processamento de pedidos
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
        if current_index == 0:
            next_layout = self.preparacao_layout
        elif current_index == 1:
            next_layout = self.entregue_layout
        else:
            return

        current_layout.removeWidget(button)
        next_layout.addWidget(button, alignment=Qt.AlignCenter)
        button.setParent(next_layout.parentWidget())

class RelatorioVendas(QWidget):
    def __init__(self):
        super().__init__()

        # Layout principal da tela de relatório de vendas
        main_layout = QVBoxLayout()

        # Título
        titulo = QLabel("Relatório")
        titulo.setStyleSheet("font-size: 18px; font-weight: bold;")
        main_layout.addWidget(titulo)

        # Tabela de relatório de vendas
        self.table = QTableWidget()
        self.table.setRowCount(3)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Item", "Quantidade", "Valor unitário", "Total por item"])
        self.table.horizontalHeader().setStretchLastSection(True)

        main_layout.addWidget(self.table)

        # Total geral
        self.total_label = QLabel()
        main_layout.addWidget(self.total_label)

        self.setLayout(main_layout)

        # Dicionário para acumular quantidades
        self.acumulado = {
            "Coca cola": 0,
            "Hamburguer": 0,
            "Batata frita": 0
        }
    
    def update_table(self, items):
        total_geral = 0

        for item in items:
            quantidade = item["quantidade_widget"].get_quantity()
            self.acumulado[item["nome"]] += quantidade

        for i, item in enumerate(items):
            quantidade = self.acumulado[item["nome"]]
            valor_unitario = item["preco"]
            total_item = quantidade * valor_unitario

            self.table.setItem(i, 0, QTableWidgetItem(item["nome"]))
            self.table.setItem(i, 1, QTableWidgetItem(f"{quantidade}x"))
            self.table.setItem(i, 2, QTableWidgetItem(f"R$ {valor_unitario:.2f}"))
            self.table.setItem(i, 3, QTableWidgetItem(f"R$ {total_item:.2f}"))

            total_geral += total_item
        
        self.total_label.setText(f"Total R$ {total_geral:.2f}")

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
        if current_index == 0:
            next_layout = self.preparacao_layout
        elif current_index == 1:
            next_layout = self.entregue_layout
        else:
            return

        current_layout.removeWidget(button)
        next_layout.addWidget(button, alignment=Qt.AlignCenter)
        button.setParent(next_layout.parentWidget())

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Menu Principal")
        self.setGeometry(100, 100, 800, 600)

        # Criando o layout principal
        layout = QVBoxLayout()

        # Criando os botões do menu
        self.buttons = {
            "Status dos Pedidos": QPushButton("Status dos Pedidos"),
            "Relatório de Vendas": QPushButton("Relatório de Vendas"),
            "Fazer Pedido": QPushButton("Fazer Pedido"),
            "Processamento de Pedidos": QPushButton("Processamento de Pedidos")
        }

        # Adicionando botões ao layout
        for button in self.buttons.values():
            layout.addWidget(button)

        # Criando um widget para segurar os botões
        button_widget = QWidget()
        button_widget.setLayout(layout)

        # Criando o StackedWidget para segurar as telas
        self.stacked_widget = QStackedWidget()
        self.status_pedidos = StatusPedidos()
        self.stacked_widget.addWidget(self.status_pedidos)
        self.tela_pedido = TelaPedido(self.atualizar_relatorio)
        self.stacked_widget.addWidget(self.tela_pedido)
        self.processamento_pedidos = ProcessamentoPedidos()
        self.stacked_widget.addWidget(self.processamento_pedidos)
        self.relatorio_vendas = RelatorioVendas()
        self.stacked_widget.addWidget(self.relatorio_vendas)

        # Criando o layout principal da janela
        main_layout = QVBoxLayout()
        main_layout.addWidget(button_widget)
        main_layout.addWidget(self.stacked_widget)

        # Criando um container principal
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Conectando botões às funções de troca de tela
        self.buttons["Status dos Pedidos"].clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        self.buttons["Relatório de Vendas"].clicked.connect(self.mostrar_relatorio)
        self.buttons["Fazer Pedido"].clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        self.buttons["Processamento de Pedidos"].clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))

    def atualizar_relatorio(self):
        self.relatorio_vendas.update_table(self.tela_pedido.get_items())

    def mostrar_relatorio(self):
        self.relatorio_vendas.update_table(self.tela_pedido.get_items())
        self.stacked_widget.setCurrentIndex(3)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
