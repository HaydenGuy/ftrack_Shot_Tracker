import sys
import os
import ftrack_api

from dotenv import load_dotenv
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QTreeWidget, QTreeWidgetItem
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

        self.milestones = get_assets("Milestone", self.project_code )
        self.asset_builds = get_assets("AssetBuild", self.project_code )
        self.sequences = get_assets("Sequence", self.project_code )

        self.create_ui()
        
    # Calls all of the UI creation methods
    def create_ui(self):
        self.create_dropdown_menu()
        self.fill_tree_information(self.milestones, self.page_1_tree)
        self.fill_tree_information(self.asset_builds, self.page_2_tree)
        self.fill_tree_information(self.sequences, self.page_3_tree)

    # Set the dropdown menu up with its items and funtionality
    def create_dropdown_menu(self):
        # Set the items in the dropdown menu list
        self.asset_type_combo.addItems(["Milestones", "Asset Builds", "Sequences"])

        # If a different item from the dropdown menu is selected call the change page slot
        self.asset_type_combo.currentIndexChanged.connect(self.change_page)

    # Change the page when the dropdown menu item is changed
    def change_page(self):
        page_index = self.asset_type_combo.currentIndex() # Get index of combo item
        self.page_widget.setCurrentIndex(page_index) # Change page to index of item

    def fill_tree_information(self, assets, tree_widget):
        for asset in assets:
            item = QTreeWidgetItem(tree_widget)
            item.setText(0, asset["name"])

        # child_item = QTreeWidgetItem(parent_item)
        # child_item.setText(0, "Child")
        # child_item.setText(1, "Child testing")


if __name__ == "__main__":
    # Print usage statement and exit if there are not two arguments
    if len(sys.argv) != 2:
        print("Usage: python script.py <target_project_code>")
        sys.exit(1)

    # # Call function on the target project code (argument 2) and assign as variable
    # project = get_target_project(sys.argv[1])

    # # Assign each of the asset types to variables
    # shots = get_assets("Shot", project)
    # tasks = get_assets("Task", project)
    
    # Initalize app, create and show the window
    app = QApplication()
    window = ftrack_Shot_Tracker()
    window.show()

    # Start application and close it when finished
    sys.exit(app.exec())