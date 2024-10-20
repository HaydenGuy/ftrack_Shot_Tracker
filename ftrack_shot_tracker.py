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

STATUSES = ["Not started", "Ready to start", "In progress",
          "Pending Review", "On Hold", "Client Approved"]

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

        # Get a set of the team_members and a set of the project_groups
        self.team_members, self.project_groups = self.get_project_team_members_and_groups(self.project)
        
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
    
    # Returns two sets; 1.team_members ("John Smith", "Mary Anne") and 2.project_groups ("Modeling Team", "Lighting Team")
    def get_project_team_members_and_groups(self, project):
        team_members = set()
        project_groups = set()

        # Add all allocated groups and users
        for allocation in project["allocations"]:

            # Resources are either groups or a user
            resource = allocation["resource"]

            # If the resource is a group, add its members to team_members and add the group name to project_groups
            if isinstance(resource, session.types["Group"]):
                project_groups.add(resource["name"]) # Add the group name to the set

                # Get the users from the groups and add them to team_members
                for membership in resource["memberships"]:
                    user = membership["user"]
                    team_members.add(user["first_name"] + " " + user["last_name"])

            # The resource is a user, add it
            else:
                user = resource
                team_members.add(user["first_name"] + " " + user["last_name"])

        return team_members, project_groups
    
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
        
    # Gets the number of assignees that a specific object has and returns it as a list
    def set_assignee_info(self, asset):
        # Checks if there are assignees otherwise sets as None
        assignees = self.check_if_none(lambda: asset["assignments"])

        names = []
        groups = []
        for assignee in assignees:
            resource = assignee["resource"]
            
            # Get assigned groups or users depending on assignee type and append to appropriate list
            try:
                if isinstance(resource, session.types["Group"]):
                    groups.append(resource["name"])
                else:
                    first_name = resource["first_name"]
                    last_name = resource["last_name"]
                    names.append(f"{first_name} {last_name}")
            except KeyError:
                pass

        if asset.entity_type in ["AssetBuild", "Sequence", "Shot"]:
            return groups
        else:
            return names

    # Gets the assets information for a given asset and returns it as a list
    def get_asset_information(self, asset):
        asset_info = {
            "name": asset["name"],
            "type": self.set_type_info(asset), # Task (Editing), Asset Buiild (Character)
            "status": self.check_if_none(lambda: asset["status"]["name"]),
            "assignee": self.set_assignee_info(asset),
            "start_date": self.check_if_none(
                lambda: asset["start_date"].format("YYYY-MM-DD")),
            "end_date": self.check_if_none(lambda: asset["end_date"].format("YYYY-MM-DD")),
            "priority": self.check_if_none(lambda: asset["priority"]["name"]),
            "description": self.check_if_none(lambda: asset["description"]),
            "type_name": self.check_if_none(lambda: asset["type"]["name"]), # Conform, Editing, Previz
            "entity_type": self.check_if_none(lambda: asset.entity_type) # Task, Milestone, Asset Build
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
                # Sets the assignee combobox to team members if its a Task or Milestone 
                if i == 3 and info["entity_type"] in ["Task", "Milestone"]:
                    combo = self.create_multi_combo_box(self.team_members, item, i, tree_widget)
                    self.set_combo_box_assignees(info["assignee"], combo)

                elif i == 3: # Sets assignee combobox to project groups if its not a Task or Milestone
                    combo = self.create_multi_combo_box(self.project_groups, item, i, tree_widget)
                    self.set_combo_box_assignees(info["assignee"], combo)

                # If the item is a Milestone set the end_date calendar cells
                if info["entity_type"] == "Milestone" and i == 5:
                    self.create_calendar_cells(
                        info[heading], item, i, tree_widget)
                else:
                    try:
                        item.setText(i, info[heading])
                    except TypeError:
                        pass

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

                # Sets the assignee combobox to team members if its a Task or Milestone 
                if i == 3 and child_info["entity_type"] in ["Task", "Milestone"]:
                    combo = self.create_multi_combo_box(self.team_members, child_item, i, tree_widget)
                    self.set_combo_box_assignees(child_info["assignee"], combo)

                # Sets assignee combobox to project groups if its not a Task or Milestone
                elif i == 3: 
                    combo = self.create_multi_combo_box(self.project_groups, child_item, i, tree_widget)
                    self.set_combo_box_assignees(child_info["assignee"], combo)

                # If the type is an accepted task type create calendar cells
                if child_info["type_name"] in TASK_NAMES_ID and i in {4, 5}:
                    self.create_calendar_cells(
                        child_info[heading], child_item, i, tree_widget)
                else:
                    try:
                        child_item.setText(i, child_info[heading])
                    except TypeError:
                        pass

            # Recursively call self to set any additional children
            self.fill_child_information(child, child_item, tree_widget)

    # Resizes the columns to fit the content in a tree widget
    def resize_columns(self, tree_widget):
        column_count = tree_widget.columnCount()
        tree_widget.expandAll()

        # Resize all columns to size of content except assignees which has set starting value
        for i in range(column_count):
            if i != 3:
                tree_widget.resizeColumnToContents(i)
            else:
                tree_widget.setColumnWidth(3, 200)

    # Creates a QDateEdit with a calendar popup tool in YYYY-MM-DD format and set it to the treewidget cell
    def create_calendar_cells(self, date, item, column, tree_widget):
        try:
            year, month, day = date.split("-")
            date_edit = QDateEdit()
            date_edit.setCalendarPopup(True)
            date_edit.setDisplayFormat("yyyy-MM-dd")
            date_edit.setDate(QDate(int(year), int(month), int(day)))
            tree_widget.setItemWidget(item, column, date_edit)
        except AttributeError:
            pass

        date_edit.dateChanged.connect(self.date_changed)

    def date_changed(self, date): # Date change is currently setting it 1 day less on ftrack (probably a date_time thing)
        print(date.toString("yyyy-MM-dd"))
        # new_date = datetime(date.year(), date.month(), date.day())
        # new_end_date_utc = new_date.replace(tzinfo=timezone.utc)
        # milestone = session.query(f"Milestone where id is 'cac38610-ac10-4299-9e6d-bcb166b2d8ce'").one()
        # milestone["end_date"] = new_end_date_utc
        # session.commit()

    # Creates a MultiSelectComboBox which allows multiple options to be selected and displayed in a cell
    def create_multi_combo_box(self, combo_items, item, column, tree_widget):
        combo = MultiSelectComboBox()
        combo.addItems(combo_items)
        tree_widget.setItemWidget(item, column, combo)

        return combo

    # Takes an *item*["assignee"] and checks those on in the passed combobox 
    def set_combo_box_assignees(self, info_assignees, combo):
        combo_indexes = []

        for name in info_assignees:
            i = combo.findText(name)
            combo_indexes.append(i)    

        combo.setCurrentIndexes(combo_indexes)

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
