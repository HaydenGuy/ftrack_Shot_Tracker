import sys
import os
import ftrack_api

from dotenv import load_dotenv
from PySide6.QtWidgets import QApplication, QMainWindow, QTreeWidgetItem, QDateEdit
from PySide6.QtCore import Qt, QDate
from UI.shot_tracker_ui import Ui_ftrack_Shot_Tracker
from pyqt6_multiselect_combobox import MultiSelectComboBox

# Load the .env file and assign the information to variables
load_dotenv()
server_url = os.getenv("SERVER_URL")
api_user = os.getenv("API_USER")
api_key = os.getenv("API_KEY")

# Information used to connect to the ftrack session
session = ftrack_api.Session(server_url=f"{server_url}",
                             api_user=f"{api_user}",
                             api_key=f"{api_key}")

COLUMN_HEADINGS = ["name", "type", "status", "assignee",
                   "start_date", "end_date", "priority", "description"]

TASK_NAMES_ID = {
    "Animation": "44dc3636-4164-11df-9218-0019bb4983d8",
    "Audio Mix": "a557384c-a5b5-4aec-b192-2049db0975d1",
    "Brand Assets": "bec6a235-717f-4225-8d9f-bde3a7fd2667",
    "Character": "66d145f0-13c6-11e3-abf2-f23c91dfaa16",
    "Color": "d410af88-73e9-4a2f-be54-dabb3fd09f50",
    "Compositing": "44dd23b6-4164-11df-9218-0019bb4983d8",
    "Concept Art": "56807358-a0f4-11e9-9843-d27cf242b68b",
    "Conform": "a3ead45c-ae42-11e9-9454-d27cf242b68b",
    "Deliverable": "ae1e2480-f24e-11e2-bd1f-f23c91dfaa16",
    "Editing": "cc46c4c6-13d2-11e3-8915-f23c91dfaa16",
    "Environment": "66d1daba-13c6-11e3-abf2-f23c91dfaa16",
    "Furniture": "0e996e82-6662-11ed-a73a-92ba0fc0dc3d",
    "FX": "44dcea86-4164-11df-9218-0019bb4983d8",
    "Layout": "ffaebf7a-9dca-11e9-8346-d27cf242b68b",
    "Lighting": "44dd08fe-4164-11df-9218-0019bb4983d8",
    "Long Form": "20b1c08e-dea7-468c-a72d-0817ee2ed6ec",
    "Lookdev": "44dc8cd0-4164-11df-9218-0019bb4983d8",
    "Matte Painting": "66d2038c-13c6-11e3-abf2-f23c91dfaa16",
    "Modeling": "44dc53c8-4164-11df-9218-0019bb4983d8",
    "Music": "8233270a-14ac-4802-9e47-2e7a774563c0",
    "News": "387efc10-d040-4cb4-bfdd-47e8995f0cef",
    "Previz": "44dc6ffc-4164-11df-9218-0019bb4983d8",
    "Production": "b628a004-ad7d-11e1-896c-f23c91df1211",
    "Prop": "66d1aedc-13c6-11e3-abf2-f23c91dfaa16",
    "Rendering": "262225e8-9dcb-11e9-82b8-d27cf242b68b",
    "Rigging": "44dd5868-4164-11df-9218-0019bb4983d8",
    "Rotoscoping": "c3bcfdb4-ad7d-11e1-a444-f23c91df1211",
    "Short Form": "d1aa3488-299e-45d1-8469-51fa1b10cebe",
    "Social": "a566a954-ee06-487f-a1db-3103cfb62ec2",
    "Sports": "32617c36-dc40-4bd2-8ae0-375194ae8616",
    "Texture": "a750a84f-b253-11eb-ad41-1e003a0c2434",
    "Tracking": "44dd3ed2-4164-11df-9218-0019bb4983d8",
    "Vehicle": "8c39f908-8b4c-11eb-9cdb-c2ffbce28b68",
    "Video Shoot": "b7df1bd9-9268-42ea-8be2-6b99abc1730f",
    "Voice Over": "2ea3363d-8617-4e45-ad23-ae678ec50b43"
}

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
        except (TypeError, AttributeError, IndexError):
            return None
    
    # Sets the type info which is used in get_asset_information
    def set_type_info(self, asset):
        type = self.check_if_none(lambda: asset["type"]["name"]) # Check if None
        entity_type = asset.entity_type # AssetBuild/Sequence/Shot etc. 

        # Return Sequence or Shot - else return eg. Task (Concept Art)
        if entity_type == "Sequence" or entity_type == "Shot":
            return entity_type
        else:
            return f"{entity_type} ({type})"
    
    # Sets the assignee info which is used in get_asset_information
    def set_assignee_info(self, asset):
        # Checks if there are assignees otherwise sets as None
        assignees = self.check_if_none(lambda: asset["assignments"]) 
        names = []

        if assignees != None:
            for i in range(len(assignees)): # Add first+last names to the names list
                first_name = self.check_if_none(lambda: asset["assignments"][i]["resource"]["first_name"])
                last_name = self.check_if_none(lambda: asset["assignments"][i]["resource"]["last_name"])

                names.append(f"{first_name} {last_name}")

        # If names list empty assignees is empty cell else cell is all names separated by comma eg. John Smith, Mary Kelly
        if not names:        
            return ""
        else:
            return ", ".join(names)

    # Gets the assets information for a given asset and returns it as a list
    def get_asset_information(self, asset):
        asset_info = {
            "name": asset["name"],
            "type": self.set_type_info(asset),
            "status": self.check_if_none(lambda: asset["status"]["name"]),
            "assignee": self.set_assignee_info(asset),
            "start_date": self.check_if_none(
                lambda: asset["start_date"].format("YYYY-MM-DD")),
            "end_date": self.check_if_none(lambda: asset["end_date"].format("YYYY-MM-DD")),
            "priority": self.check_if_none(lambda: asset["priority"]["name"]),
            "description": self.check_if_none(lambda: asset["description"]),
        }

        return asset_info

    # Calls all of the UI creation methods
    def create_ui(self):
        self.create_dropdown_menu()
        self.fill_tree_information(self.milestones, self.page_1_tree)
        self.fill_tree_information(self.asset_builds, self.page_2_tree)
        self.fill_tree_information(self.sequences, self.page_3_tree)
        self.resize_columns(self.page_1_tree)
        self.resize_columns(self.page_2_tree)
        self.resize_columns(self.page_3_tree)
        # Sets the page widget to page 1 (fixes issues where page is blank upon loading)
        self.page_widget.setCurrentIndex(0)

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
        for asset in reversed(assets):
            item = QTreeWidgetItem(tree_widget)
            item.setFlags(item.flags() | Qt.ItemIsEditable)

            # Creates a dictionary with asset information
            info = self.get_asset_information(asset)

            # Calls the info dictionary and set the tree widget index i to the respective value
            for i, heading in enumerate(COLUMN_HEADINGS):
                item.setText(i, info[heading])

            self.fill_child_information(asset, item, tree_widget)

    # Retrieves the children for a parent asset/item and sets the information in the table widget
    def fill_child_information(self, parent_asset, parent_item, tree_widget):
        children = parent_asset["children"]

        for child in children:  # Fills info for Shots and Tasks
            child_item = QTreeWidgetItem(parent_item)
            child_item.setFlags(child_item.flags() | Qt.ItemIsEditable)

            # Creates a dictionary with asset information
            child_info = self.get_asset_information(child)

            # Calls the child_info dictionary and set the tree widget index i to the respective value
            for i, heading in enumerate(COLUMN_HEADINGS):
                # If the type is an accepted task type create calendar cells
                if child_info["type"] in TASK_NAMES_ID and i in {4, 5}:
                    self.create_calendar_cells(
                        child_info[heading], child_item, i, tree_widget)
                else:
                    child_item.setText(i, child_info[heading])

            # Recursively call self to set any additional children
            self.fill_child_information(child, child_item, tree_widget)

    # Resizes the columns to fit the content in a tree widget
    def resize_columns(self, tree_widget):
        column_count = tree_widget.columnCount()
        tree_widget.expandAll()

        for i in range(column_count):
            if i != 3: # Makes it so the assignee column doesn't resize
                tree_widget.resizeColumnToContents(i)

    # Creates a QDateEdit with a calendar popup tool in YYYY-MM-DD format and set it to the treewidget cell
    def create_calendar_cells(self, date, item, column, tree_widget):
        year, month, day = date.split("-")
        date_edit = QDateEdit()
        date_edit.setCalendarPopup(True)
        date_edit.setDisplayFormat("yyyy-MM-dd")
        date_edit.setDate(QDate(int(year), int(month), int(day)))
        tree_widget.setItemWidget(item, column, date_edit)

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
