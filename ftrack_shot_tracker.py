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

# Check if an ftrack project exists by calling its code and return the project if it does
def get_target_project(project_code):
    project = session.query(f"Project where name is {project_code}").first()

    if not project:
        print("Could not find target_project")
        sys.exit(1)
    
    return project

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
    # Print usage statement and exit if there are not two arguments
    if len(sys.argv) != 2:
        print("Usage: python script.py <target_project_code>")
        sys.exit(1)

    # Call function on the target project code (argument 2)
    get_target_project(sys.argv[1])

    # Initalize app, create and show the window
    app = QApplication()
    window = ftrack_Shot_Tracker()
    window.show()

    # Start application and close it when finished
    sys.exit(app.exec())