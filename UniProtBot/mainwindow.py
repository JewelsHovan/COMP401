import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QCheckBox, QLineEdit
from PyQt6.QtGui import QPixmap, QPalette, QColor


class MainWindow(QMainWindow):

    def __init__(self):
        self.app = QApplication(sys.argv)
        super().__init__()
        self.setWindowTitle("UniProt Scraper")
        self.initialize_values()
        self.initUI() # setup UI elements
        self.show()
        sys.exit(self.app.exec()) # application loop 


    def initialize_values(self):
        self.species = None
        self.min_prot = None
        self.max_prot = None

    def initUI(self):
        # styles
        label_style = "font-size: 18px; font-weight: bold; border: 1px solid black; background-color: white"
        # labels

        title_label = QLabel("UnitProt Scraper")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        search_label = QLabel("Species: ")
        min_prot_label = QLabel("Minimal Protein threshold")
        max_prot_label = QLabel("Maximal Protein threshold")
        description_label = QLabel("Description...")

        self.labels = [title_label, search_label, min_prot_label, max_prot_label]
        for l in self.labels:
            self.setLabelStyle(l, label_style)

        # edit lines
        search_edit = QLineEdit()
        min_prot_edit = QLineEdit()
        max_prot_edit = QLineEdit()
        self.edits = [search_edit, min_prot_edit, max_prot_edit]

        # buttons
        save_bt = QPushButton("Save Values")
        run_bt = QPushButton("Run")
        headless_checkbox = QCheckBox("Headless Mode")

        # connect buttons
        save_bt.clicked.connect(self.saveValues)
        run_bt.clicked.connect(self.run_bot)


        # layout
        window_layout = QVBoxLayout()
        config_layout = QHBoxLayout() # for labels and edit
        bottom_layout = QHBoxLayout() # for buttons and checks

        label_layout = QVBoxLayout()
        label_layout.addWidget(search_label)
        label_layout.addWidget(min_prot_label)
        label_layout.addWidget(max_prot_label)

        edit_layout = QVBoxLayout()
        edit_layout.addWidget(search_edit)
        edit_layout.addWidget(min_prot_edit)
        edit_layout.addWidget(max_prot_edit)

        config_layout.addLayout(label_layout)
        config_layout.addLayout(edit_layout)

        bottom_layout.addWidget(save_bt)
        bottom_layout.addWidget(run_bt)
        bottom_layout.addWidget(headless_checkbox)

        window_layout.addWidget(title_label)
        window_layout.addLayout(config_layout)
        window_layout.addLayout(bottom_layout)

        window = QWidget()
        window.setLayout(window_layout)
        self.setCentralWidget(window)

        #set up the palette
        palette = QPalette()
        red_color = QColor(205, 32, 32)
        palette.setColor(QPalette.ColorRole.Window, red_color)
        self.setPalette(palette)

        # set up menu bar
        self.createMenuBar()
        # status bar
        self.createStatusBar()

    def createMenuBar(self):
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu("File")
        fileMenu.addAction("Exit", self.close)
        AboutMenu = menuBar.addMenu("About")
        AboutMenu.addAction("Description")
        menuBar.setStyleSheet("background-color: gainsboro")
    
    def createStatusBar(self):
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("Status: OK")
        self.status_bar.setStyleSheet("background-color: gainsboro")

    def setLabelStyle(self, label: QLabel, stylestring: str) -> None:
        label.setStyleSheet(stylestring)

    def saveValues(self):
        self.scrap_values = []
        for value in self.edits:
            self.scrap_values.append(value)
        
        self.species = self.scrap_values[0].text()
        self.min_prot = (self.scrap_values[1].text())
        self.max_prot = (self.scrap_values[2].text())

        self.status_bar.showMessage("Status: Values saved")
    
    def run_bot(self):
        if self.species in [None, ""] or self.min_prot in [None, ""] or self.max_prot in [None, ""]:
            self.status_bar.showMessage("Status: Cannot Run (values are null or invalid)")
        else:
            self.status_bar.showMessage("Status: Running...")


if __name__ ==  '__main__':
    window = MainWindow()

