from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QGridLayout
from PySide6.QtWidgets import QHeaderView
from PySide6.QtWidgets import QMainWindow
from PySide6.QtWidgets import QTableWidget
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QTableWidgetItem
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QFormLayout
from PySide6.QtWidgets import QLineEdit
from PySide6.QtWidgets import QCheckBox
from PySide6.QtWidgets import QSpinBox
from PySide6.QtWidgets import QMessageBox
from logic import Logic

# Klass för att hantera objekt av schackspelare.


class Chessplayer:
    def __init__(self):
        self.firstname = ""
        self.lastname = ""
        self.federation = ""
        self.rating = ""
        self.title = None

# Klass för GUI


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.chessplayer = Chessplayer()
        self.opponents = []
        self.central_widget = None  # Centerwidget
        self.button_widget = None  # Widget under tabellen för att göra beräkningar

        self.setWindowTitle("FIDE Norm Calculator")
        self.resize(800, 600)
        self.create_menu_system()

        # QLabel
        self.im_norm_score_label = None
        self.gm_norm_score_label = None

        # Knappar
        self.compute_button = None
        self.erase_button = None

        # Centerwidget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.central_widget.setLayout(self.layout)

        self.create_player_form()
        self.create_main_table()
        self.create_score_labels()
        self.create_button_widget()

    # Funktion för att skapa menysystemet.
    def create_menu_system(self):
        menu_bar = self.menuBar()
        # FileMenu
        file_menu = menu_bar.addMenu("Arkiv")
        exit_action = QAction("Quit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

    # Funktion för att skapa ett formulär för den spelare, som normberäkningarna gäller.
    def create_player_form(self):
        self.player_widget = QWidget()
        layout = QGridLayout()

        self.player_firstname = QLineEdit()
        self.player_lastname = QLineEdit()
        self.player_country = QLineEdit()

        self.number_of_opponents = QSpinBox()
        self.number_of_opponents.setRange(9, 14)
        self.number_of_opponents.setValue(9)
        self.number_of_opponents.valueChanged.connect(
            self.update_number_of_opponents
        )

        self.federation_requirement = QCheckBox(
            "Kontrollera federationskravet"
        )
        self.federation_requirement.setChecked(True)

        # Rad 0
        layout.addWidget(QLabel("Förnamn"), 0, 0)
        layout.addWidget(self.player_firstname, 0, 1)

        layout.addWidget(QLabel("Efternamn"), 0, 2)
        layout.addWidget(self.player_lastname, 0, 3)

        layout.addWidget(QLabel("Land"), 0, 4)
        layout.addWidget(self.player_country, 0, 5)

        # Rad 1
        layout.addWidget(QLabel("Antal motståndare"), 1, 0)
        layout.addWidget(self.number_of_opponents, 1, 1)

        layout.addWidget(self.federation_requirement, 1, 2, 1, 4)

        self.player_widget.setLayout(layout)
        self.layout.addWidget(self.player_widget)

    # Funktion för att skapa tabellen med motståndarna.
    def create_main_table(self):
        self.table = QTableWidget(9, 5)
        self.layout.addWidget(self.table)

        self.table.setHorizontalHeaderLabels([
            "Titel",
            "Förnamn",
            "Efternamn",
            "Land",
            "Elo-tal",
        ])

        # Kolumnerna fyller hela bredden
        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        # Visa alltid plats för 9 rader
        visible_rows = 10
        row_height = self.table.verticalHeader().defaultSectionSize()
        header_height = self.table.horizontalHeader().height()

        self.table.setFixedHeight(
            header_height + visible_rows * row_height + 2
        )

        self.table.itemChanged.connect(self.update_table)

    # Funktion för att skapa etiketter för hur många poäng som krävs för normerna.
    def create_score_labels(self):
        widget = QWidget()
        widget_layout = QHBoxLayout()
        widget.setLayout(widget_layout)
        self.im_norm_score_label = QLabel("IM-norm: ")
        self.gm_norm_score_label = QLabel("GM-norm: ")
        widget_layout.addWidget(self.im_norm_score_label)
        widget_layout.addWidget(self.gm_norm_score_label)
        self.layout.addWidget(widget)

    # Funktion för att skapa knappar för beräkning med mera.
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

    # Funktion som uppdaterar tabellen.
    def update_table(self):
        self.opponents.clear()

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
            federation = get(3).upper()

            # Exempel: endast 3 bokstäver (SWE, NOR, DEN ...)
            if federation and (len(federation) != 3 or not federation.isalpha()):
                federation = ""
                item = self.table.item(row, 3)
                if item:
                    self.table.blockSignals(True)
                    item.setText("")
                    self.table.blockSignals(False)

            player.federation = federation

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
                player.federation,
                player.rating
            ]):
                self.opponents.append(player)

    # Funktion för att beräkna normkraven.
    def compute(self):
        if len(self.opponents) < 9:
            QMessageBox.warning(self,
                                "Fel",
                                "Inte tillräckligt med motståndare."
                                )
            print("Not enough players")
        else:
            logic = Logic(self.opponents, self.player_country)
            # Uppdatering av normetiketterna.
            scores = logic.compute_norm_scores()
            if scores[0] is None:
                self.im_norm_score_label.setText("IM-norm: -")
            else:
                self.im_norm_score_label.setText(f"IM-norm: {scores[0]}")
            if scores[1] is None:
                self.gm_norm_score_label.setText("GM-norm: -")
            else:
                self.gm_norm_score_label.setText(f"GM-norm: {scores[1]}")

    # Funktion för att rensa formuläret.
    def erase(self):
        self.opponents.clear()
        self.table.clearContents()

    # Funktion för att uppdatera tabellen, så att den motsvarar antal motståndare.
    def update_number_of_opponents(self, value):
        self.table.setRowCount(value)
