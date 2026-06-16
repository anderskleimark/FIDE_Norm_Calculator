from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QMainWindow,
    QTableWidget,
    QWidget,
    QVBoxLayout,
    QLabel
)


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("FIDE Norm Calculator")
        self.resize(800, 600)
        self.create_menu_system()
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)
        self.create_main_header()
        self.create_main_table()

    def create_menu_system(self):
        menu_bar = self.menuBar()
        # FileMenu
        file_menu = menu_bar.addMenu("File")
        exit_action = QAction("Quit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

    def create_main_header(self):
        self.header = QLabel("Players")
        self.layout.addWidget(self.header)

        # Centrera texten
        self.header.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Gör texten större och fet
        font = QFont()
        font.setPointSize(20)
        font.setBold(True)
        self.header.setFont(font)
        self.layout.addWidget(self.header)

    def create_main_table(self):
        self.table = QTableWidget(3, 5)
        self.layout.addWidget(self.table)
