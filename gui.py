from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QStackedWidget
from RelatorioVendas import RelatorioVendas
from ProcessamentoPedidos import ProcessamentoPedidos
from TelaPedido import TelaPedido
from StatusPedido import StatusPedidos
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

        # Criando o layout principal
        layout = QVBoxLayout()

        # Criando os botões do menu
        self.buttons = {
            "Status dos Pedidos": QPushButton("Status dos Pedidos"),
            "Relatório de Vendas": QPushButton("Relatório de Vendas"),
            "Fazer Pedido": QPushButton("Fazer Pedido"),
            # "Processamento de Pedidos": QPushButton("Processamento de Pedidos")
        }

        # Adicionando botões ao layout
        for button in self.buttons.values():
            layout.addWidget(button)

        # Criando um widget para segurar os botões
        button_widget = QWidget()
        button_widget.setLayout(layout)

        # Criando o StackedWidget para segurar as telas
        self.stacked_widget = QStackedWidget()
        self.status_pedidos = StatusPedidos(self.queue, self.production, self.finished, self.mover_pedido)
        self.stacked_widget.addWidget(self.status_pedidos)
        self.tela_pedido = TelaPedido(self.queue, self.items, self.create_order, self.atualizar_relatorio, self.atualizar_filas)
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
        self.buttons["Status dos Pedidos"].clicked.connect(self.mostrar_filas)
        self.buttons["Relatório de Vendas"].clicked.connect(self.mostrar_relatorio)
        self.buttons["Fazer Pedido"].clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        # self.buttons["Processamento de Pedidos"].clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))


    def atualizar_relatorio(self):
        self.relatorio_vendas.update_table(self.generate_report())

    def mostrar_relatorio(self):
        self.relatorio_vendas.update_table(self.generate_report())
        self.stacked_widget.setCurrentIndex(3)

    def atualizar_filas(self):
        self.status_pedidos.update_layout(self.queue, self.production, self.finished)

    def mostrar_filas(self):
        self.status_pedidos.update_layout(self.queue, self.production, self.finished)
        self.stacked_widget.setCurrentIndex(0)

    def create_order(self, items: list):
        order = Order(OrderStatus.QUEUE, items)
        self.queue.enqueue(order)

    def mover_pedido(self, orderId):
        for order in self.queue.orders:
            if(order.id == orderId):
                order_found = self.queue.dequeue()
                self.production.enqueue(order_found)
                self.atualizar_filas()
                return

        for order in self.production.orders:
            if (order.id == orderId):
                order_found = self.production.dequeue()
                self.finished.enqueue(order_found)
                self.atualizar_filas()
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
