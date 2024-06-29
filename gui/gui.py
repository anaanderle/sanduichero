from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QStackedWidget
from RelatorioVendas import RelatorioVendas
from ProcessamentoPedidos import ProcessamentoPedidos
from TelaPedido import TelaPedido
from StatusPedido import StatusPedidos 
import sys

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
