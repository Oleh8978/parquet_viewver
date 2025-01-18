import sys
import pandas as pd
import pyarrow.parquet as pq
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QTableView, QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QMessageBox, QMenu
)
from PyQt5.QtCore import QAbstractTableModel, Qt
from PyQt5.QtGui import QClipboard


class DataFrameModel(QAbstractTableModel):
    def __init__(self, df):
        super().__init__()
        self._df = df

    def rowCount(self, parent=None):
        return self._df.shape[0]

    def columnCount(self, parent=None):
        return self._df.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return str(self._df.iloc[index.row(), index.column()])
        return None

    def setData(self, index, value, role=Qt.EditRole):
        if role == Qt.EditRole:
            self._df.iloc[index.row(), index.column()] = value
            return True
        return False

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self._df.columns[section]
            if orientation == Qt.Vertical:
                return str(self._df.index[section])
        return None

    def flags(self, index):
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Parquet Viewer & Editor")
        self.resize(900, 600)

        self.current_file_path = None
        self.df = None

        # Main layout
        layout = QVBoxLayout()

        # Buttons
        button_layout = QHBoxLayout()
        self.open_button = QPushButton("Open File")
        self.save_button = QPushButton("Save File")
        self.save_as_button = QPushButton("Save As")
        self.open_button.clicked.connect(self.open_file)
        self.save_button.clicked.connect(self.save_file)
        self.save_as_button.clicked.connect(self.save_file_as)
        button_layout.addWidget(self.open_button)
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.save_as_button)

        # Table view
        self.table = QTableView()
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.show_context_menu)

        layout.addLayout(button_layout)
        layout.addWidget(self.table)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def open_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open Parquet File", "", "Parquet Files (*.parquet)")
        if path:
            try:
                self.df = pd.read_parquet(path)
                self.current_file_path = path
                self.model = DataFrameModel(self.df)
                self.table.setModel(self.model)
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to open file:\n{e}")
                try:
                    table = pq.read_table(path, use_threads=True)
                    self.df = table.to_pandas()
                    self.current_file_path = path
                    self.model = DataFrameModel(self.df)
                    self.table.setModel(self.model)
                    QMessageBox.information(self, "Repair Successful", "The file was repaired and loaded.")
                except Exception as repair_error:
                    QMessageBox.critical(self, "Repair Failed", f"Could not repair file:\n{repair_error}")

    def save_file(self):
        if self.current_file_path:
            try:
                self.df.to_parquet(self.current_file_path)
                QMessageBox.information(self, "Success", "File saved successfully.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save file:\n{e}")
        else:
            self.save_file_as()

    def save_file_as(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save File As", "", "Parquet Files (*.parquet)")
        if path:
            try:
                self.df.to_parquet(path)
                self.current_file_path = path
                QMessageBox.information(self, "Success", "File saved successfully.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save file:\n{e}")

    def show_context_menu(self, position):
        menu = QMenu()
        copy_cell_action = menu.addAction("Copy Cell")
        copy_column_action = menu.addAction("Copy Column")

        action = menu.exec_(self.table.viewport().mapToGlobal(position))

        if action == copy_cell_action:
            self.copy_cell()
        elif action == copy_column_action:
            self.copy_column()

    def copy_cell(self):
        index = self.table.currentIndex()
        if index.isValid():
            value = str(self.model.data(index, Qt.DisplayRole))
            QApplication.clipboard().setText(value)

    def copy_column(self):
        index = self.table.currentIndex()
        if index.isValid():
            column_data = self.df.iloc[:, index.column()].to_string(index=False)
            QApplication.clipboard().setText(column_data)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet("""
        QMainWindow {
            background-color: #f5f5f5;
        }
        QPushButton {
            background-color: #0078d7;
            color: white;
            border-radius: 5px;
            padding: 5px 10px;
            font-size: 14px;
        }
        QPushButton:hover {
            background-color: #005a9e;
        }
        QTableView {
            gridline-color: #dcdcdc;
            font-size: 13px;
        }
        QHeaderView::section {
            background-color: #0078d7;
            color: white;
            font-weight: bold;
            border: 1px solid #dcdcdc;
        }
    """)
    window = MainWindow()
    window.show()
    app.exec_()
