from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QStackedWidget, QTableWidget, QTableWidgetItem, QMessageBox
from PySide6.QtCore import Qt
import sys

class Report(QWidget):
    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout()

        title = QLabel("Relatório")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        main_layout.addWidget(title)

        self.table = QTableWidget()
        self.table.setRowCount(3)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Item", "Quantidade", "Valor unitário", "Total por item"])
        self.table.horizontalHeader().setStretchLastSection(True)

        main_layout.addWidget(self.table)

        self.total_label = QLabel()
        main_layout.addWidget(self.total_label)

        self.setLayout(main_layout)

    def update_table(self, report):
        for row, item in enumerate(report):
            internal_item = item["item"].name
            quantity = item['quantity']
            value = item['item'].value
            total = quantity * value

            self.table.setItem(row, 0, QTableWidgetItem(internal_item))
            self.table.setItem(row, 1, QTableWidgetItem(str(quantity)))
            self.table.setItem(row, 2, QTableWidgetItem(f"{value:.2f}"))
            self.table.setItem(row, 3, QTableWidgetItem(f"{total:.2f}"))
