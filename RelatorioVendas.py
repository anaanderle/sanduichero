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

    def update_table(self, report):
        data = report

        total_geral = 0
        for row, item in enumerate(data):
            internal_item = item["item"].name
            quantidade = item['quantity']
            valor_unitario = item['item'].value
            total_por_item = quantidade * valor_unitario
            total_geral += total_por_item

            self.table.setItem(row, 0, QTableWidgetItem(internal_item))
            self.table.setItem(row, 1, QTableWidgetItem(str(quantidade)))
            self.table.setItem(row, 2, QTableWidgetItem(f"{valor_unitario:.2f}"))
            self.table.setItem(row, 3, QTableWidgetItem(f"{total_por_item:.2f}"))


