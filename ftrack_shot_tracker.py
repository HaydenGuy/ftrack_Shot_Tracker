import sys
import os
import ftrack_api

from dotenv import load_dotenv
from PySide6.QtWidgets import QApplication, QMainWindow, QStyledItemDelegate, QTreeWidgetItem, QDateEdit
from PySide6.QtCore import Qt, QDate
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

class calendar_delegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super(calendar_delegate, self).__init__(parent)

    def create_editor(self, parent):
        # Create a QDateEdit with a calendar popup
        editor = QDateEdit(parent)
        editor.setCalendarPopup(True)
        return editor
    
    def set_editor_data(self, editor, index):
        # Get the data from the item and set it to the editor
        date = index.model().data(index, Qt.EditRole)
        editor.setDate(QDate.fromString(date, "yyyy-MM-dd"))

    def set_model_data(self, editor, model, index):
        # Set the editor data back to the model
        model.setData(index, editor.date().toString("yyyy-MM-dd"), Qt.EditRole)


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

        self.column_headings = ["name", "type", "status", "assignee", "start_date", "end_date", "priority", "description"]

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
        asset_info = {
            "name": self.check_if_none(lambda: asset["name"]),
            "type": self.check_if_none(lambda: asset["type"]["name"]),
            "status": self.check_if_none(lambda: asset["status"]["name"]),
            "assignee": self.check_if_none(
                lambda: asset["assignments"][0]["resource"]["username"]),
            "start_date": self.check_if_none(
                lambda: asset["start_date"].format("YYYY-MM-DD")),
            "end_date": self.check_if_none(lambda: asset["end_date"].format("YYYY-MM-DD")),
            "priority": self.check_if_none(lambda: asset["priority"]["name"]),
            "description" : self.check_if_none(lambda: asset["description"])
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
        # self.create_date_cells(5, self.page_1_tree)
        # self.create_date_cells(6, self.page_1_tree)
        self.page_widget.setCurrentIndex(0) # Sets the page widget to page 1 (fixes issues where page is blank upon loading)

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
            for i, heading in enumerate(self.column_headings): 
                item.setText(i, info[heading])

            self.fill_child_information(asset, item)

    # Retrieves the children for a parent asset/item and sets the information in the table widget
    def fill_child_information(self, parent_asset, parent_item):
        children = parent_asset["children"]

        for child in children:  # Fills info for Shots and Tasks
            child_item = QTreeWidgetItem(parent_item)
            child_item.setFlags(child_item.flags() | Qt.ItemIsEditable)

            # Creates a dictionary with asset information
            child_info = self.get_asset_information(child)

            # Calls the info dictionary and set the tree widget index i to the respective value
            for i, heading in enumerate(self.column_headings):
                child_item.setText(i, child_info[heading])

            # Recursively call self to set any additional children
            self.fill_child_information(child, child_item)

    # Resizes the columns to fit the content in a tree widget
    def resize_columns(self, tree_widget):
        column_count = tree_widget.columnCount()
        tree_widget.expandAll()

        for i in range(column_count):
            tree_widget.resizeColumnToContents(i)

    # Set the date in the given cell based on the provided date 
    # def create_date_cells(self, column, tree_widget):
    #     delegate = calendar_delegate()
    #     tree_widget.setItemDelegateForColumn(column, delegate)

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
