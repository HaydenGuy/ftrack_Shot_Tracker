from PySide6.QtWidgets import (QMainWindow, QHBoxLayout, QVBoxLayout)


class ftrack_Shot_Tracker(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ftrack Shot Tracker")
        self.setGeometry(0, 0, 800, 600)