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
        project = session.query(f"Project where name is {project_code}").first()
    
        if not project:
            print("Could not find target project")
            sys.exit(1)
        
        return project
    
    # Query the ftrack assets based on the asset type and return them
    def get_assets(self, asset_type, project):
        assets = session.query(f"{asset_type} where project_id is '{project["id"]}'").all()
    
        return assets
    
    # Gets the information for a given task and returns it as a list
    def get_milestone_asset_build_sequence_information(self, asset):
        asset_info = [asset["name"],
                      asset["type"]["name"],
                      asset["status"]["name"],
                      None,
                      None,
                      None,
                      asset["status"]["state"]["name"],
                      asset["priority"]["name"],  ### THIS CAUSING ISSUES
                      asset["description"]]
        
        return asset_info

    # Gets the information for a given task and returns it as a list
    def get_task_information(self, asset):
        try:
            # Try to get assignees email else set to none
            assignee = asset["assignments"][0]["resource"]["username"]
        except IndexError:
            assignee = None

        try:
            # Try format the start date unless one is not set
            start_date = asset["start_date"].format("YYYY-MM-DD")
        except AttributeError:
            start_date = None

        try:
            # Try format the due date unless one is not set
            end_date = asset["end_date"].format("YYYY-MM-DD")
        except AttributeError:
            end_date = None
        
        asset_info = [asset["name"],
                      asset["type"]["name"],
                      asset["status"]["name"],
                      assignee,
                      start_date,
                      end_date,
                      asset["status"]["state"]["name"],
                      asset["priority"]["name"],
                      asset["description"]]
        
        return asset_info

    # Calls all of the UI creation methods
    def create_ui(self):
        self.create_dropdown_menu()
        # self.fill_tree_information(self.tasks, self.page_1_tree)
        self.fill_tree_milestones_asset_builds_sequences(self.milestones, self.page_1_tree)
        self.fill_tree_milestones_asset_builds_sequences(self.asset_builds, self.page_2_tree)
        self.fill_tree_milestones_asset_builds_sequences(self.sequences, self.page_3_tree)

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

    def fill_tree_milestones_asset_builds_sequences(self, assets, tree_widget):
        for asset in assets[::-1]:
            item = QTreeWidgetItem(tree_widget)
            item.setFlags(item.flags() | Qt.ItemIsEditable)

            info = self.get_milestone_asset_build_sequence_information(asset)
            print(info)
            # for i, inf in enumerate(info):
                # item.setText(i, inf)

    def fill_tree_information(self):
        pass
        # for asset in assets[::-1]:
        #     parent_item = QTreeWidgetItem(tree_widget)
        #     asset_info = self.get_task_information(asset)
        #     for i, info in enumerate(asset_info):
        #         parent_item.setText(i, info)
        #     for i in range(len(asset_info)):
        #         parent_item.setText(i, asset_info[i])
            
        #     children = asset["children"]

        #     for child in children:
        #         child_item = QTreeWidgetItem(parent_item)
        #         child_item.setText(0, child["name"])

        #         more_children = child["children"]

        #         for m_child in more_children:
        #             m_child_item = QTreeWidgetItem(child_item)
        #             m_child_item.setText(0, m_child["name"])

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