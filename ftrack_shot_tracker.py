import sys
import os
import ftrack_api
import tzlocal
from datetime import datetime

from dotenv import load_dotenv
from PySide6.QtWidgets import QApplication, QMainWindow, QTreeWidgetItem, QDateTimeEdit, QComboBox
from PySide6.QtCore import Qt, QDate, QTime, QDateTime
from PySide6.QtGui import QBrush, QColor
from UI.shot_tracker import Ui_ftrack_Shot_Tracker
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
    "Animation": {
        "ID": "44dc3636-4164-11df-9218-0019bb4983d8",
        "Animation": {
            "AssetBuild": "N",
            "Milestone": "Y",
            "Task": "Y",
        },
        "Model Production": {
            "AssetBuild": "N",
            "Milestone": "N",
            "Task": "N",
        },
        "VFX": {
            "AssetBuild": "N",
            "Milestone": "Y",
            "Task": "Y",
        }        
    },
    "Audio Mix": {
        "ID": "a557384c-a5b5-4aec-b192-2049db0975d1",
        "Animation": {
            "AssetBuild": "N",
            "Milestone": "N",
            "Task": "N",
        },
        "Model Production": {
            "AssetBuild": "N",
            "Milestone": "N",
            "Task": "N",
        },
        "VFX": {
            "AssetBuild": "N",
            "Milestone": "N",
            "Task": "N",
        }    
    },
    "Brand Assets": {
        "ID": "bec6a235-717f-4225-8d9f-bde3a7fd2667",
        "Animation": {
            "AssetBuild": "N",
            "Milestone": "N",
            "Task": "N",
        },
        "Model Production": {
            "AssetBuild": "N",
            "Milestone": "N",
            "Task": "N",
        },
        "VFX": {
            "AssetBuild": "N",
            "Milestone": "N",
            "Task": "N",
        }    
    },
    "Character": {
        "ID": "66d145f0-13c6-11e3-abf2-f23c91dfaa16",
        "Animation": {
            "AssetBuild": "Y",
            "Milestone": "N",
            "Task": "N",
        },
        "Model Production": {
            "AssetBuild": "N",
            "Milestone": "N",
            "Task": "N",
        },
        "VFX": {
            "AssetBuild": "Y",
            "Milestone": "N",
            "Task": "N",
        }    
    },
    "Color": {
        "ID": "d410af88-73e9-4a2f-be54-dabb3fd09f50",
        "Animation": {
            "AssetBuild": "N",
            "Milestone": "N",
            "Task": "N",
        },
        "Model Production": {
            "AssetBuild": "N",
            "Milestone": "N",
            "Task": "N",
        },
        "VFX": {
            "AssetBuild": "N",
            "Milestone": "N",
            "Task": "N",
        }    
    },
    "Compositing": {
        "ID": "44dd23b6-4164-11df-9218-0019bb4983d8",
        "Animation": {
            "AssetBuild": "N",
            "Milestone": "Y",
            "Task": "Y",
        },
        "Model Production": {
            "AssetBuild": "N",
            "Milestone": "N",
            "Task": "N",
        },
        "VFX": {
            "AssetBuild": "N",
            "Milestone": "Y",
            "Task": "Y",
        }    
    },
    "Concept Art": {
        "ID": "56807358-a0f4-11e9-9843-d27cf242b68b",
        "Animation": {
            "AssetBuild": "N",
            "Milestone": "Y",
            "Task": "Y",
        },
        "Model Production": {
            "AssetBuild": "Y",
            "Milestone": "N",
            "Task": "N",
        },
        "VFX": {
            "AssetBuild": "N",
            "Milestone": "Y",
            "Task": "Y",
        }    
    },
    "Conform": {
        "ID": "a3ead45c-ae42-11e9-9454-d27cf242b68b",
        "Animation": {
            "AssetBuild": "N",
            "Milestone": "N",
            "Task": "N",
        },
        "Model Production": {
            "AssetBuild": "N",
            "Milestone": "N",
            "Task": "N",
        },
        "VFX": {
            "AssetBuild": "N",
            "Milestone": "Y",
            "Task": "Y",
        }    
    },
    "Deliverable": {
        "ID": "ae1e2480-f24e-11e2-bd1f-f23c91dfaa16",
        "Animation": {
            "AssetBuild": "N",
            "Milestone": "Y",
            "Task": "N",
        },
        "Model Production": {
            "AssetBuild": "N",
            "Milestone": "Y",
            "Task": "N",
        },
        "VFX": {
            "AssetBuild": "N",
            "Milestone": "Y",
            "Task": "N",
        }    
    },
    "Editing": {
        "ID": "cc46c4c6-13d2-11e3-8915-f23c91dfaa16",
        "Animation": {
            "AssetBuild": "N",
            "Milestone": "Y",
            "Task": "Y",
        },
        "Model Production": {
            "AssetBuild": "N",
            "Milestone": "N",
            "Task": "N",
        },
        "VFX": {
            "AssetBuild": "N",
            "Milestone": "Y",
            "Task": "Y",
        }    
    },
    "Environment": {
        "ID": "66d1daba-13c6-11e3-abf2-f23c91dfaa16",
        "Animation": {
            "AssetBuild": "Y",
            "Milestone": "N",
            "Task": "N",
        },
        "Model Production": {
            "AssetBuild": "N",
            "Milestone": "N",
            "Task": "N",
        },
        "VFX": {
            "AssetBuild": "Y",
            "Milestone": "N",
            "Task": "N",
        }    
    },
    "Furniture": {
        "ID": "0e996e82-6662-11ed-a73a-92ba0fc0dc3d",
        "Animation": {
            "AssetBuild": "N",
            "Milestone": "N",
            "Task": "N",
        },
        "Model Production": {
            "AssetBuild": "Y",
            "Milestone": "N",
            "Task": "N",
        },
        "VFX": {
            "AssetBuild": "N",
            "Milestone": "N",
            "Task": "N",
        }    
    },
    "FX": {
        "ID": "44dcea86-4164-11df-9218-0019bb4983d8",
        "Animation": {
            "AssetBuild": "N",
            "Milestone": "N",
            "Task": "Y",
        },
        "Model Production": {
            "AssetBuild": "N",
            "Milestone": "N",
            "Task": "N",
        },
        "VFX": {
            "AssetBuild": "N",
            "Milestone": "Y",
            "Task": "Y",
        }    
    },
    "Layout": {
        "ID": "ffaebf7a-9dca-11e9-8346-d27cf242b68b",
        "Animation": {
            "AssetBuild": "N",
            "Milestone": "Y",
            "Task": "Y",
        },
        "Model Production": {
            "AssetBuild": "N",
            "Milestone": "N",
            "Task": "N",
        },
        "VFX": {
            "AssetBuild": "N",
            "Milestone": "Y",
            "Task": "Y",
        }    
    },
    "Lighting": {
        "ID": "44dd08fe-4164-11df-9218-0019bb4983d8",
        "Animation": {
            "AssetBuild": "N",
            "Milestone": "Y",
            "Task": "Y",
        },
        "Model Production": {
            "AssetBuild": "N",
            "Milestone": "N",
            "Task": "N",
        },
        "VFX": {
            "AssetBuild": "N",
            "Milestone": "Y",
            "Task": "Y",
        }    
    },
    "Long Form": {
        "ID": "20b1c08e-dea7-468c-a72d-0817ee2ed6ec",
        "Animation": {
            "AssetBuild": "N",
            "Milestone": "N",
            "Task": "N",
        },
        "Model Production": {
            "AssetBuild": "N",
            "Milestone": "N",
            "Task": "N",
        },
        "VFX": {
            "AssetBuild": "N",
            "Milestone": "N",
            "Task": "N",
        }    
    },
    "Lookdev": {
        "ID": "44dc8cd0-4164-11df-9218-0019bb4983d8",
        "Animation": {
            "AssetBuild": "N",
            "Milestone": "Y",
            "Task": "Y",
        },
        "Model Production": {
            "AssetBuild": "N",
            "Milestone": "N",
            "Task": "N",
        },
        "VFX": {
            "AssetBuild": "N",
            "Milestone": "Y",
            "Task": "Y",
        }    
    },
    "Matte Painting": {
        "ID": "66d2038c-13c6-11e3-abf2-f23c91dfaa16",
        "Animation": {
            "AssetBuild": "N",
            "Milestone": "N",
            "Task": "N",
        },
        "Model Production": {
            "AssetBuild": "N",
            "Milestone": "N",
            "Task": "N",
        },
        "VFX": {
            "AssetBuild": "Y",
            "Milestone": "N",
            "Task": "N",
        }    
    },
    "Modeling": {
        "ID": "44dc53c8-4164-11df-9218-0019bb4983d8",
        "Animation": {
            "AssetBuild": "N",
            "Milestone": "Y",
            "Task": "Y",
        },
        "Model Production": {
            "AssetBuild": "N",
            "Milestone": "N",
            "Task": "Y",
        },
        "VFX": {
            "AssetBuild": "N",
            "Milestone": "Y",
            "Task": "Y",
        }    
    },
    "Music": {
        "ID": "8233270a-14ac-4802-9e47-2e7a774563c0",
        "Animation": {
            "AssetBuild": "N",
            "Milestone": "N",
            "Task": "N",
        },
        "Model Production": {
            "AssetBuild": "N",
            "Milestone": "N",
            "Task": "N",
        },
        "VFX": {
            "AssetBuild": "N",
            "Milestone": "N",
            "Task": "N",
        }    
    },
    "News": {
        "ID": "387efc10-d040-4cb4-bfdd-47e8995f0cef",
        "Animation": {
            "AssetBuild": "N",
            "Milestone": "N",
            "Task": "N",
        },
        "Model Production": {
            "AssetBuild": "N",
            "Milestone": "N",
            "Task": "N",
        },
        "VFX": {
            "AssetBuild": "N",
            "Milestone": "N",
            "Task": "N",
        }    
    },
    "Previz": {
        "ID": "44dc6ffc-4164-11df-9218-0019bb4983d8",
        "Animation": {
            "AssetBuild": "N",
            "Milestone": "N",
            "Task": "Y",
        },
        "Model Production": {
            "AssetBuild": "N",
            "Milestone": "N",
            "Task": "N",
        },
        "VFX": {
            "AssetBuild": "N",
            "Milestone": "Y",
            "Task": "Y",
        }    
    },
    "Production": {
        "ID": "b628a004-ad7d-11e1-896c-f23c91df1211",
        "Animation": {
            "AssetBuild": "N",
            "Milestone": "Y",
            "Task": "Y",
        },
        "Model Production": {
            "AssetBuild": "N",
            "Milestone": "N",
            "Task": "N",
        },
        "VFX": {
            "AssetBuild": "N",
            "Milestone": "Y",
            "Task": "Y",
        }    
    },
    "Prop": {
        "ID": "66d1aedc-13c6-11e3-abf2-f23c91dfaa16",
        "Animation": {
            "AssetBuild": "Y",
            "Milestone": "N",
            "Task": "N",
        },
        "Model Production": {
            "AssetBuild": "N",
            "Milestone": "N",
            "Task": "N",
        },
        "VFX": {
            "AssetBuild": "Y",
            "Milestone": "N",
            "Task": "N",
        }    
    },
    "Rendering": {
        "ID": "262225e8-9dcb-11e9-82b8-d27cf242b68b",
        "Animation": {
            "AssetBuild": "N",
            "Milestone": "Y",
            "Task": "Y",
        },
        "Model Production": {
            "AssetBuild": "N",
            "Milestone": "N",
            "Task": "N",
        },
        "VFX": {
            "AssetBuild": "N",
            "Milestone": "Y",
            "Task": "Y",
        }    
    },
    "Rigging": {
        "ID": "44dd5868-4164-11df-9218-0019bb4983d8",
        "Animation": {
            "AssetBuild": "N",
            "Milestone": "Y",
            "Task": "Y",
        },
        "Model Production": {
            "AssetBuild": "N",
            "Milestone": "N",
            "Task": "N",
        },
        "VFX": {
            "AssetBuild": "N",
            "Milestone": "Y",
            "Task": "Y",
        }    
    },
    "Rotoscoping": {
        "ID": "c3bcfdb4-ad7d-11e1-a444-f23c91df1211",
        "Animation": {
            "AssetBuild": "N",
            "Milestone": "N",
            "Task": "N",
        },
        "Model Production": {
            "AssetBuild": "N",
            "Milestone": "N",
            "Task": "N",
        },
        "VFX": {
            "AssetBuild": "N",
            "Milestone": "Y",
            "Task": "Y",
        }    
    },
    "Short Form": {
        "ID": "d1aa3488-299e-45d1-8469-51fa1b10cebe",
        "Animation": {
            "AssetBuild": "N",
            "Milestone": "N",
            "Task": "N",
        },
        "Model Production": {
            "AssetBuild": "N",
            "Milestone": "N",
            "Task": "N",
        },
        "VFX": {
            "AssetBuild": "N",
            "Milestone": "N",
            "Task": "N",
        }    
    },
    "Social": {
        "ID": "a566a954-ee06-487f-a1db-3103cfb62ec2",
        "Animation": {
            "AssetBuild": "N",
            "Milestone": "N",
            "Task": "N",
        },
        "Model Production": {
            "AssetBuild": "N",
            "Milestone": "N",
            "Task": "N",
        },
        "VFX": {
            "AssetBuild": "N",
            "Milestone": "N",
            "Task": "N",
        }    
    },
    "Sports": {
        "ID": "32617c36-dc40-4bd2-8ae0-375194ae8616",
        "Animation": {
            "AssetBuild": "N",
            "Milestone": "N",
            "Task": "N",
        },
        "Model Production": {
            "AssetBuild": "N",
            "Milestone": "N",
            "Task": "N",
        },
        "VFX": {
            "AssetBuild": "N",
            "Milestone": "N",
            "Task": "N",
        }    
    },
    "Texture": {
        "ID": "a750a84f-b253-11eb-ad41-1e003a0c2434",
        "Animation": {
            "AssetBuild": "N",
            "Milestone": "Y",
            "Task": "Y",
        },
        "Model Production": {
            "AssetBuild": "N",
            "Milestone": "N",
            "Task": "Y",
        },
        "VFX": {
            "AssetBuild": "N",
            "Milestone": "Y",
            "Task": "Y",
        }    
    },
    "Tracking": {
        "ID": "44dd3ed2-4164-11df-9218-0019bb4983d8",
        "Animation": {
            "AssetBuild": "N",
            "Milestone": "N",
            "Task": "N",
        },
        "Model Production": {
            "AssetBuild": "N",
            "Milestone": "N",
            "Task": "N",
        },
        "VFX": {
            "AssetBuild": "N",
            "Milestone": "Y",
            "Task": "Y",
        }    
    },
    "Vehicle": {
        "ID": "8c39f908-8b4c-11eb-9cdb-c2ffbce28b68",
        "Animation": {
            "AssetBuild": "N",
            "Milestone": "N",
            "Task": "N",
        },
        "Model Production": {
            "AssetBuild": "N",
            "Milestone": "N",
            "Task": "N",
        },
        "VFX": {
            "AssetBuild": "Y",
            "Milestone": "N",
            "Task": "N",
        }    
    },
    "Video Shoot": {
        "ID": "b7df1bd9-9268-42ea-8be2-6b99abc1730f",
        "Animation": {
            "AssetBuild": "N",
            "Milestone": "N",
            "Task": "N",
        },
        "Model Production": {
            "AssetBuild": "N",
            "Milestone": "N",
            "Task": "N",
        },
        "VFX": {
            "AssetBuild": "N",
            "Milestone": "N",
            "Task": "N",
        }    
    },
    "Voice Over": {
        "ID": "2ea3363d-8617-4e45-ad23-ae678ec50b43",
        "Animation": {
            "AssetBuild": "N",
            "Milestone": "N",
            "Task": "N",
        },
        "Model Production": {
            "AssetBuild": "N",
            "Milestone": "N",
            "Task": "N",
        },
        "VFX": {
            "AssetBuild": "N",
            "Milestone": "N",
            "Task": "N",
        }    
    }
}

MILESTONE_STATUSES = {
    "Not started": (255, 255, 255),
    "In progress": (52, 152, 219),
    "Completed": (28, 188, 144)
}

ASSET_BUILD_TASK_STATUSES = {
    "Not started": (255, 255, 255),
    "Ready to start": (0, 255, 255),
    "In progress": (52, 152, 219),
    "Pending Review": (241, 196, 15),
    "On Hold": (231, 76, 60),
    "Approved": (28, 188, 144)
}

PRIORITY_LABELS = ["Urgent", "High", "Medium", "Low", "None"]

LOCAL_TZ = tzlocal.get_localzone()

class ftrack_Shot_Tracker(QMainWindow, Ui_ftrack_Shot_Tracker):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Call function on the target project code (argument 2) and assign as variable
        self.project = self.get_target_project(sys.argv[1])

        # Gets the project type (Animation, VFX, Model Production)
        self.project_type = self.project["project_schema"]["name"]

        # Initialize type lists that will be used in the Type combobox based on the project type
        self.asset_build_type_list = self.get_type_lists(self.project_type, "AssetBuild", TASK_NAMES_ID)
        self.milestone_type_list = self.get_type_lists(self.project_type, "Milestone", TASK_NAMES_ID)
        self.task_type_list = self.get_type_lists(self.project_type, "Task", TASK_NAMES_ID)

        self.milestones = self.get_assets("Milestone", self.project)
        self.asset_builds = self.get_assets("AssetBuild", self.project)
        self.sequences = self.get_assets("Sequence", self.project)
        self.tasks = self.get_assets("Task", self.project)

        # Stores QTreeWidgetItem as a key and the info dictionary from get_asset_info as values
        self.tree_item_and_info = {}

        # Get a set of the team_members and a set of the project_groups
        self.team_members, self.project_groups = self.get_project_team_members_and_groups(self.project)
        
        self.create_ui()

        # Call item_changed when an item updated on any of tree widgets
        self.page_1_tree.itemChanged.connect(self.item_changed)
        self.page_2_tree.itemChanged.connect(self.item_changed)
        self.page_3_tree.itemChanged.connect(self.item_changed)

        # Clicking items in column 1 or 2 on a tree widget calls a method to set the type or status
        self.page_1_tree.itemClicked.connect(lambda item, column: self.set_type_or_status_list(item, column, self.page_1_tree))
        self.page_2_tree.itemClicked.connect(lambda item, column: self.set_type_or_status_list(item, column, self.page_2_tree))
        self.page_3_tree.itemClicked.connect(lambda item, column: self.set_type_or_status_list(item, column, self.page_3_tree))
        
        self.save_btn.clicked.connect(self.save_session)

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
    
    # Return a list of the Types for the passed asset_type using items from the TASK_NAME_ID dictionary
    def get_type_lists(self, project_type, asset_type, dictionary):
        types = []

        for type_name, info in dictionary.items():
            if info[project_type][asset_type] == "Y":
                types.append(type_name)

        return types

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
            "start_date": self.check_if_none(lambda: asset["start_date"]),
            "end_date": self.check_if_none(lambda: asset["end_date"]),
            "priority": self.check_if_none(lambda: asset["priority"]["name"]),
            "description": self.check_if_none(lambda: asset["description"]),
            "type_name": self.check_if_none(lambda: asset["type"]["name"]), # Conform, Editing, Previz
            "entity_type": self.check_if_none(lambda: asset.entity_type), # Task, Milestone, Asset Build
            "id": self.check_if_none(lambda: asset["id"])
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
        self.page_1_tree.sortItems(0, Qt.SortOrder.AscendingOrder)
        self.page_2_tree.sortItems(0, Qt.SortOrder.AscendingOrder)
        self.page_3_tree.sortItems(0, Qt.SortOrder.AscendingOrder)
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

            # Adds the tree item and its info to dictionary for easy use in other methods
            self.tree_item_and_info[item] = info

            # Calls the info dictionary and set the tree widget index i to the respective value
            for i, heading in enumerate(COLUMN_HEADINGS):
                
                # Set background color of status cells
                if i == 2 and info["entity_type"] == "Milestone":
                    text = info["status"]
                    r, g, b = MILESTONE_STATUSES[text][0], MILESTONE_STATUSES[text][1], MILESTONE_STATUSES[text][2]
                    brush = QBrush(QColor(r, g, b)) # Create brush and brush color
                    item.setBackground(2, brush) # Set background to brush color
                
                # Set background color of status cells
                elif i == 2 and info["entity_type"] in ["Task", "AssetBuild"]:
                    text = info["status"]
                    r, g, b = ASSET_BUILD_TASK_STATUSES[text][0], ASSET_BUILD_TASK_STATUSES[text][1], ASSET_BUILD_TASK_STATUSES[text][2]
                    brush = QBrush(QColor(r, g, b))
                    item.setBackground(2, brush)

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
                        info[heading], item, info["id"], info["entity_type"], i, tree_widget)
                
                # Sets up the priority column cells if not a milestone
                elif info["entity_type"] != "Milestone" and i == 6:
                    self.set_priority_labels(item, info, tree_widget)

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

            # Adds the tree item and its info to dictionary for easy use in other methods
            self.tree_item_and_info[child_item] = child_info

            # Calls the child_info dictionary and set the tree widget index i to the respective value
            for i, heading in enumerate(COLUMN_HEADINGS):
                
                # Set background color of status cells
                if i == 2 and child_info["entity_type"] == "Milestone":
                    text = child_info["status"]
                    r, g, b = MILESTONE_STATUSES[text][0], MILESTONE_STATUSES[text][1], MILESTONE_STATUSES[text][2]
                    brush = QBrush(QColor(r, g, b)) # Create brush and brush color
                    child_item.setBackground(2, brush) # Set background to brush color
                
                # Set background color of status cells
                elif i == 2 and child_info["entity_type"] in ["Task", "AssetBuild"]:
                    text = child_info["status"]
                    r, g, b = ASSET_BUILD_TASK_STATUSES[text][0], ASSET_BUILD_TASK_STATUSES[text][1], ASSET_BUILD_TASK_STATUSES[text][2]
                    brush = QBrush(QColor(r, g, b))
                    child_item.setBackground(2, brush)

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
                        child_info[heading], child_item, child_info["id"], child_info["entity_type"], i, tree_widget)
                
                # Sets up the priority column cells if not a milestone
                elif child_info["entity_type"] != "Milestone" and i == 6:
                    self.set_priority_labels(child_item, child_info, tree_widget)

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

    # Creates a combobox to be used when selecting an item from the type or status column
    def set_type_or_status_list(self, item, column, tree_widget):
        combo = QComboBox()
        current_text = item.text(column)  # Get the current text in column 1
        entity_type = self.tree_item_and_info[item]["entity_type"] # Get entity type of item that was clicked
        
        # Logic to create a type list combo
        if column == 1 and entity_type in ["AssetBuild", "Milestone", "Task"]:
            match entity_type: # Populate combo with respective type list
                case "AssetBuild":
                    combo.addItems(self.asset_build_type_list)
                case "Milestone":
                    combo.addItems(self.milestone_type_list)
                case "Task":
                    combo.addItems(self.task_type_list)

            
            type_name = current_text.split("(")[1].split(")")[0]  # Extract type name in parentheses
            active = combo.findText(type_name)  # Find index of the extracted text
            combo.setCurrentIndex(active)  # Set active combo item to extracted text name

            tree_widget.setItemWidget(item, column, combo)  # Replace column 1 with the combo box
            combo.activated.connect(lambda _: self.set_item_text_from_combo(tree_widget, item, combo, column))
            combo.showPopup()
        
        # Logic to create a status combo 
        elif column == 2 and entity_type in ["AssetBuild", "Milestone", "Task"]:
            
            if entity_type == "Milestone":
                combo.addItems(list(MILESTONE_STATUSES.keys()))
            else:
                combo.addItems(list(ASSET_BUILD_TASK_STATUSES.keys()))

            active = combo.findText(current_text) # Find currently set text in the combo
            combo.setCurrentIndex(active) # Set the active text to the combo current index

            tree_widget.setItemWidget(item, column, combo) # Replace column 2 with the combo box
            combo.activated.connect(lambda _: self.set_item_text_from_combo(tree_widget, item, combo, column))
            combo.showPopup()
        
        else:
            pass
            
    # Takes the passed combo item and sets its value as text in the column
    def set_item_text_from_combo(self, tree_widget, item, combo, column):
        entity_type = self.tree_item_and_info[item]["entity_type"]
        if column == 1: # For types
            # Task (Layout), Asset Build (Modeling) etc.
            text = f"{entity_type} ({combo.currentText()})"
        else:
            text = combo.currentText()
            
            # Return the rgb values of the key text in specified dictionary 
            if entity_type == "Milestone":
                r, g, b = MILESTONE_STATUSES[text][0], MILESTONE_STATUSES[text][1], MILESTONE_STATUSES[text][2]
            else:
                r, g, b = ASSET_BUILD_TASK_STATUSES[text][0], ASSET_BUILD_TASK_STATUSES[text][1], ASSET_BUILD_TASK_STATUSES[text][2]
            
            brush = QBrush(QColor(r, g, b)) # Create brush and brush color
            item.setBackground(column, brush) # Set background to brush color

        item.setText(column, text)
        tree_widget.removeItemWidget(item, column)  # Remove the combo box

    # Creates a QDateEdit with a calendar popup tool in YYYY-MM-DD format and set it to the treewidget cell
    def create_calendar_cells(self, date, item, id, entity_type, column, tree_widget):
        try:
            # Split local time into individual variables
            local_datetime_obj = date.astimezone(LOCAL_TZ)
            year = local_datetime_obj.year
            month = local_datetime_obj.month
            day = local_datetime_obj.day
            hours = local_datetime_obj.hour
            minutes = local_datetime_obj.minute
            seconds = local_datetime_obj.second

            # Create QDateTimeEdit and set it to the tree widget cell
            datetime_edit = QDateTimeEdit()
            datetime_edit.setCalendarPopup(True)
            datetime_edit.setDisplayFormat("yyyy-MM-dd")
            datetime_edit.setDateTime(QDateTime(QDate(int(year), int(month), int(day)), QTime(int(hours), int(minutes), int(seconds))))
            tree_widget.setItemWidget(item, column, datetime_edit)
            
            # When the date is changed call the date_changed method and pass it additional variables using lambda
            datetime_edit.dateTimeChanged.connect(lambda date_time: self.date_changed(date_time, id, entity_type, column))
        except AttributeError:
            pass

    # Sets the start/end date of the changed date cell to the correct utc date
    def date_changed(self, date_time, id, entity_type, column):
        utc = date_time.toUTC()
        utc_datetime = datetime(utc.date().year(), utc.date().month(), utc.date().day())
        asset = session.query(f"{entity_type} where id is '{id}'").one()

        if column == 4:
            asset["start_date"] = utc_datetime
        elif column == 5:
            asset["end_date"] = utc_datetime
        else:
            pass
        
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

    # Sets the priority column combo box
    def set_priority_labels(self, item, info, tree_widget):
        combo = QComboBox()
        combo.addItems(PRIORITY_LABELS)
        current_label = info["priority"] # Get the current priority for the item
        active = combo.findText(current_label)
        combo.setCurrentIndex(active) # Set the active combo item to the item priority
        tree_widget.setItemWidget(item, 6, combo) # Set the cell to the combo

    # Calls a specific method when an item in a particular column is updated
    def item_changed(self, item, column):
        entity_type = self.tree_item_and_info[item]["entity_type"] # Get entity type (Task, Milestone, etc.)
        id = self.tree_item_and_info[item]["id"] # Get the id of the item from the dict

        # Get the updated text on the tree widget and update item name on ftrack 
        if column == 0:
            new_name = item.text(column) # Get the text in the column
            self.update_item("name", new_name, entity_type, id) # Update the items name on ftrack
            self.tree_item_and_info[item]["name"] = new_name # Update the items name in the dict
        if column == 1:
            current_text = item.text(column)
            type_name = current_text.split("(")[1].split(")")[0]  # Extract type name in parentheses
            type_id = TASK_NAMES_ID[type_name]["ID"] # Get the type ID from the global dict
            new_type = session.query(f"Type where id is {type_id}").one() # Query the type from ftrack
            self.update_item("type", new_type, entity_type, id) # Update the items type on ftrack
            self.tree_item_and_info[item]["type"] = new_type["name"] # Update the items name in the dict

    # Update the name of the passed item on ftrack (ready for commit/save)
    def update_item(self, to_change, change_to, entity_type, id):
        asset = session.query(f"{entity_type} where id is '{id}'").one()

        asset[to_change] = change_to

    def save_session(self):
        session.commit()

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
