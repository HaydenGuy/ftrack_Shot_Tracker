import sys
import os
import ftrack_api

from dotenv import load_dotenv
from PySide6.QtWidgets import QApplication, QMainWindow, QComboBox, QLabel
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
        print("Could not find target project")
        sys.exit(1)
    
    return project

# Query the ftrack assets based on the asset type and return them
def get_assets(asset_type, project):
    assets = session.query(f"{asset_type} where project_id is '{project["id"]}'").all()

    return assets

class ftrack_Shot_Tracker(QMainWindow, Ui_ftrack_Shot_Tracker):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Call function on the target project code (argument 2) and assign as variable
        self.project_code = get_target_project(sys.argv[1])

        self.create_dropdown_menu()
        self.create_asset_labels()

    # Set the dropdown menu up with its items and funtionality
    def create_dropdown_menu(self):
        # Set the items in the dropdown menu list
        self.project_names_combo.addItems(["Milestones", "Asset Builds", "Sequences"])

        # If a different item from the dropdown menu is selected call the change page slot
        self.project_names_combo.currentIndexChanged.connect(self.change_page)

    # Change the page when the dropdown menu item is changed
    def change_page(self):
        page_index = self.project_names_combo.currentIndex() # Get index of combo item
        self.page_widget.setCurrentIndex(page_index) # Change page to index of item

    # Add labels based on asset names to the page1 layout - to be updated
    def create_asset_labels(self):
        asset_builds = get_assets("AssetBuild", self.project_code)

        for asset in asset_builds[::-1]:
            label = QLabel(asset["name"])
            self.page_2_layout.addWidget(label)


if __name__ == "__main__":
    # Print usage statement and exit if there are not two arguments
    if len(sys.argv) != 2:
        print("Usage: python script.py <target_project_code>")
        sys.exit(1)

    # Call function on the target project code (argument 2) and assign as variable
    project = get_target_project(sys.argv[1])

    # Assign each of the asset types to variables
    milestones = get_assets("Milestone", project)
    asset_builds = get_assets("AssetBuild", project)
    sequences = get_assets("Sequence", project)
    shots = get_assets("Shot", project)
    tasks = get_assets("Task", project)
    
    # Initalize app, create and show the window
    app = QApplication()
    window = ftrack_Shot_Tracker()
    window.show()

    # Start application and close it when finished
    sys.exit(app.exec())