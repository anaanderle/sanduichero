from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QStackedWidget, QTableWidget, QTableWidgetItem, QMessageBox
from PySide6.QtCore import Qt
import sys

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
