import sys
import os
import ftrack_api

from dotenv import load_dotenv
from PySide6.QtWidgets import QApplication, QMainWindow, QTreeWidgetItem
from PySide6.QtCore import Qt
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

        # Call function on the target project code (argument 2) and assign as variable
        self.project = self.get_target_project(sys.argv[1])

        self.milestones = self.get_assets("Milestone", self.project)
        self.asset_builds = self.get_assets("AssetBuild", self.project)
        self.sequences = self.get_assets("Sequence", self.project)
        self.tasks = self.get_assets("Task", self.project)

        self.create_ui()

    # Check if an ftrack project exists by calling its code and return the project if it does
    def get_target_project(self, project_code):
        project = session.query(f"Project where name is {
                                project_code}").first()

        if not project:
            print("Could not find target project")
            sys.exit(1)

        return project

    # Query the ftrack assets based on the asset type and return them
    def get_assets(self, asset_type, project):
        assets = session.query(f"{asset_type} where project_id is '{
                               project["id"]}'").all()

        return assets

    # Check if the asset information returns as None and if it does set it to None
    def check_if_none(self, getter):
        try:
            return getter()
        except (TypeError, AttributeError, KeyError, IndexError):
            return None

    # Gets the assets information for a given asset and returns it as a list
    def get_asset_information(self, asset):
        asset_info = [
            self.check_if_none(lambda: asset["name"]),
            self.check_if_none(lambda: asset["type"]["name"]),
            self.check_if_none(lambda: asset["status"]["name"]),
            self.check_if_none(
                lambda: asset["assignments"][0]["resource"]["username"]),
            self.check_if_none(
                lambda: asset["start_date"].format("YYYY-MM-DD")),
            self.check_if_none(lambda: asset["end_date"].format("YYYY-MM-DD")),
            self.check_if_none(lambda: asset["priority"]["name"]),
            self.check_if_none(lambda: asset["description"])
        ]

        return asset_info

    # Calls all of the UI creation methods
    def create_ui(self):
        self.create_dropdown_menu()
        self.fill_tree_information(self.milestones, self.page_1_tree)
        self.fill_tree_information(self.asset_builds, self.page_2_tree)
        self.fill_tree_information(self.sequences, self.page_3_tree)
        self.page_widget.setCurrentIndex(0) # Sets the page widget to page 1 (fixes issues where page is upon loading)

    # Set the dropdown menu up with its items and funtionality
    def create_dropdown_menu(self):
        # Set the items in the dropdown menu list
        self.asset_type_combo.addItems(
            ["Milestones", "Asset Builds", "Sequences"])

        # If a different item from the dropdown menu is selected call the change page slot
        self.asset_type_combo.currentIndexChanged.connect(self.change_page)

    # Change the page when the dropdown menu item is changed
    def change_page(self):
        page_index = self.asset_type_combo.currentIndex()  # Get index of combo item
        # Change page to index of item
        self.page_widget.setCurrentIndex(page_index)

    # Fills in the tree information for the passed tree widget
    def fill_tree_information(self, assets, tree_widget):
        for asset in assets[::-1]:  # Fills info for the Milestones, Sequences, AssetBuilds
            item = QTreeWidgetItem(tree_widget)
            item.setFlags(item.flags() | Qt.ItemIsEditable)

            # Retrieves the table information
            info = self.get_asset_information(asset)
            for i, inf in enumerate(info):
                item.setText(i, inf)  # Set the table info in postion i

            # Retrieves and sets the child information for the Milestones, Sequences, AssetBuilds
            self.fill_child_information(asset, item)

    # Retrieves the children for a parent asset/item and sets the information in the table widget
    def fill_child_information(self, parent_asset, parent_item):
        children = parent_asset["children"]

        for child in children:  # Fills info for Shots and Tasks
            child_item = QTreeWidgetItem(parent_item)
            child_item.setFlags(child_item.flags() | Qt.ItemIsEditable)

            # Retrieves the table information
            info = self.get_asset_information(child)
            for i, inf in enumerate(info):
                child_item.setText(i, inf)  # Set the table info in postion i

            # Recursively call self to set any additional children
            self.fill_child_information(child, child_item)


if __name__ == "__main__":
    # Print usage statement and exit if there are not two arguments
    if len(sys.argv) != 2:
        print("Usage: python script.py <target_project_code>")
        sys.exit(1)

    # Initalize app, create and show the window
    app = QApplication()
    window = ftrack_Shot_Tracker()
    window.show()

    # Start application and close it when finished
    sys.exit(app.exec())
