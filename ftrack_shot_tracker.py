import sys
import os
import ftrack_api

from dotenv import load_dotenv
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton
from UI.shot_tracker_ui import Ui_ftrack_Shot_Tracker

# Load the .env file and assign the information to variables
load_dotenv()
server_url = os.getenv("SERVER_URL")
api_user = os.getenv("API_USER")
api_key = os.getenv("API_KEY")

# Information used to connect to the ftrack session
session = ftrack_api.Session(server_url=f"{server_url}",
                             api_user=f"{api_user}",
                             api_key=f"{api_key}")

class ftrack_Shot_Tracker(QMainWindow, Ui_ftrack_Shot_Tracker):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        button_names = ["testing", "button", "names"]

        self.button_create(button_names)

    def button_create(self, button_names):
        for button in button_names:
            self.button_box.addWidget(QPushButton(f"{button}"))

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = ftrack_Shot_Tracker()
    window.show()

    sys.exit(app.exec_())