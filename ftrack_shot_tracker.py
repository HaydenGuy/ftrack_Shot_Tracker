import sys
import os
import ftrack_api

from PySide6.QtWidgets import QApplication
from UI import ftrack_Shot_Tracker

# Information about the session
# session = ftrack_api.Session(server_url="",
#                              api_user="",
#                              api_key="")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = ftrack_Shot_Tracker()
    window.show()

    sys.exit(app.exec_())