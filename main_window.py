from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QGridLayout
from PySide6.QtWidgets import QHeaderView
from PySide6.QtWidgets import QMainWindow
from PySide6.QtWidgets import QTableWidget
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QPushButton
from chessplayer import Chessplayer
from PySide6.QtWidgets import QTableWidgetItem


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.chessplayers = []
        self.central_widget = None  # Centerwidget
        self.button_widget = None  # Widget under tabellen för att göra beräkningar

        self.setWindowTitle("FIDE Norm Calculator")
        self.resize(800, 600)
        self.create_menu_system()

        # Knappar
        self.compute_button = None
        self.erase_button = None

        # Centerwidget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.central_widget.setLayout(self.layout)

        self.create_main_header()
        self.create_main_table()
        self.create_button_widget()

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

    def create_main_table(self):
        self.table = QTableWidget(11, 7)
        self.layout.addWidget(self.table)

        self.table.setHorizontalHeaderLabels([
            "Titel",
            "Förnamn",
            "Efternamn",
            "Land",
            "Elo-tal",
            "IM-norm",
            "GM-norm"
        ])

        # Vi gör de två sista kolumnerna ej redigeringsbara.
        for row in range(self.table.rowCount()):
            for col in [5, 6]:
                item = self.table.item(row, col)

                if item is None:
                    item = QTableWidgetItem()
                    self.table.setItem(row, col, item)

                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)

        # Kolumnerna fyller hela bredden
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.itemChanged.connect(self.update_table)

    def create_button_widget(self):
        self.button_widget = QWidget()
        layout = QGridLayout()
        self.button_widget.setLayout(layout)
        self.compute_button = QPushButton("Beräkna")
        self.compute_button.clicked.connect(self.compute)
        layout.addWidget(self.compute_button, 0, 0)
        self.erase_button = QPushButton("Rensa")
        self.erase_button.clicked.connect(self.erase)
        layout.addWidget(self.erase_button, 0, 1)

        self.layout.addWidget(self.button_widget)

    def update_table(self):
        self.chessplayers.clear()

        valid_titles = {"GM", "IM", "FM", "WGM", "WIM", "WFM"}

        for row in range(self.table.rowCount()):
            player = Chessplayer()

            def get(col):
                item = self.table.item(row, col)
                return item.text().strip() if item else ""

            # ----- Titel -----
            title = get(0).upper()
            if title not in valid_titles:
                title = ""
                item = self.table.item(row, 0)
                if item:
                    self.table.blockSignals(True)
                    item.setText("")
                    self.table.blockSignals(False)

            player.title = title

            # ----- Förnamn -----
            firstname = get(1)

            if any(ch.isdigit() for ch in firstname):
                firstname = ""
                item = self.table.item(row, 1)
                if item:
                    self.table.blockSignals(True)
                    item.setText("")
                    self.table.blockSignals(False)

            player.firstname = firstname

            # ----- Efternamn -----
            lastname = get(2)

            if any(ch.isdigit() for ch in lastname):
                lastname = ""
                item = self.table.item(row, 2)
                if item:
                    self.table.blockSignals(True)
                    item.setText("")
                    self.table.blockSignals(False)

            player.lastname = lastname

            # ----- Land -----
            country = get(3).upper()

            # Exempel: endast 3 bokstäver (SWE, NOR, DEN ...)
            if country and (len(country) != 3 or not country.isalpha()):
                country = ""
                item = self.table.item(row, 3)
                if item:
                    self.table.blockSignals(True)
                    item.setText("")
                    self.table.blockSignals(False)

            player.club = country

            # ----- Elo -----
            rating_text = get(4)

            try:
                rating = int(rating_text)
            except ValueError:
                rating = 0

            if not (1400 <= rating <= 3000):
                rating = 0
                item = self.table.item(row, 4)
                if item:
                    self.table.blockSignals(True)
                    item.setText("")
                    self.table.blockSignals(False)

            player.rating = rating

            # Lägg bara till spelare om raden inte är helt tom
            if any([
                player.title,
                player.firstname,
                player.lastname,
                player.club,
                player.rating
            ]):
                self.chessplayers.append(player)

    def compute(self):
        if len(self.chessplayers) < 10:
            print("Not enough players")
        else:
            print("Enough players")

    def erase(self):
        self.chessplayers.clear()
        self.table.clearContents()
