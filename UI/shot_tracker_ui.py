# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'shot_tracker.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QHeaderView,
    QMainWindow, QSizePolicy, QStackedWidget, QTreeWidget,
    QTreeWidgetItem, QVBoxLayout, QWidget)

class Ui_ftrack_Shot_Tracker(object):
    def setupUi(self, ftrack_Shot_Tracker):
        if not ftrack_Shot_Tracker.objectName():
            ftrack_Shot_Tracker.setObjectName(u"ftrack_Shot_Tracker")
        ftrack_Shot_Tracker.resize(1000, 600)
        self.centralwidget = QWidget(ftrack_Shot_Tracker)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.combo_box_layout = QVBoxLayout()
        self.combo_box_layout.setObjectName(u"combo_box_layout")
        self.combo_box_layout.setContentsMargins(-1, -1, -1, 0)
        self.project_names_combo = QComboBox(self.centralwidget)
        self.project_names_combo.setObjectName(u"project_names_combo")

        self.combo_box_layout.addWidget(self.project_names_combo)


        self.verticalLayout.addLayout(self.combo_box_layout)

        self.page_widget = QStackedWidget(self.centralwidget)
        self.page_widget.setObjectName(u"page_widget")
        self.page_1 = QWidget()
        self.page_1.setObjectName(u"page_1")
        self.horizontalLayout_4 = QHBoxLayout(self.page_1)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.page_1_layout = QVBoxLayout()
        self.page_1_layout.setObjectName(u"page_1_layout")
        self.page_1_tree = QTreeWidget(self.page_1)
        self.page_1_tree.setObjectName(u"page_1_tree")

        self.page_1_layout.addWidget(self.page_1_tree)


        self.horizontalLayout_4.addLayout(self.page_1_layout)

        self.page_widget.addWidget(self.page_1)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.verticalLayout_4 = QVBoxLayout(self.page_2)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.page_2_layout = QVBoxLayout()
        self.page_2_layout.setObjectName(u"page_2_layout")
        self.page_2_tree = QTreeWidget(self.page_2)
        self.page_2_tree.setObjectName(u"page_2_tree")

        self.page_2_layout.addWidget(self.page_2_tree)


        self.verticalLayout_4.addLayout(self.page_2_layout)

        self.page_widget.addWidget(self.page_2)
        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")
        self.verticalLayout_5 = QVBoxLayout(self.page_3)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.page_3_layout = QVBoxLayout()
        self.page_3_layout.setObjectName(u"page_3_layout")
        self.page_3_tree = QTreeWidget(self.page_3)
        self.page_3_tree.setObjectName(u"page_3_tree")

        self.page_3_layout.addWidget(self.page_3_tree)


        self.verticalLayout_5.addLayout(self.page_3_layout)

        self.page_widget.addWidget(self.page_3)
        self.page_4 = QWidget()
        self.page_4.setObjectName(u"page_4")
        self.verticalLayout_3 = QVBoxLayout(self.page_4)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.page_4_layout = QVBoxLayout()
        self.page_4_layout.setObjectName(u"page_4_layout")
        self.page_4_tree = QTreeWidget(self.page_4)
        self.page_4_tree.setObjectName(u"page_4_tree")

        self.page_4_layout.addWidget(self.page_4_tree)


        self.verticalLayout_3.addLayout(self.page_4_layout)

        self.page_widget.addWidget(self.page_4)

        self.verticalLayout.addWidget(self.page_widget)

        ftrack_Shot_Tracker.setCentralWidget(self.centralwidget)

        self.retranslateUi(ftrack_Shot_Tracker)

        self.page_widget.setCurrentIndex(3)


        QMetaObject.connectSlotsByName(ftrack_Shot_Tracker)
    # setupUi

    def retranslateUi(self, ftrack_Shot_Tracker):
        ftrack_Shot_Tracker.setWindowTitle(QCoreApplication.translate("ftrack_Shot_Tracker", u"ftrack Shot Tracker", None))
        ___qtreewidgetitem = self.page_1_tree.headerItem()
        ___qtreewidgetitem.setText(8, QCoreApplication.translate("ftrack_Shot_Tracker", u"Description", None));
        ___qtreewidgetitem.setText(7, QCoreApplication.translate("ftrack_Shot_Tracker", u"Priority", None));
        ___qtreewidgetitem.setText(6, QCoreApplication.translate("ftrack_Shot_Tracker", u"State", None));
        ___qtreewidgetitem.setText(5, QCoreApplication.translate("ftrack_Shot_Tracker", u"Due date", None));
        ___qtreewidgetitem.setText(4, QCoreApplication.translate("ftrack_Shot_Tracker", u"Start date", None));
        ___qtreewidgetitem.setText(3, QCoreApplication.translate("ftrack_Shot_Tracker", u"Assignee", None));
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("ftrack_Shot_Tracker", u"Status", None));
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("ftrack_Shot_Tracker", u"Type", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("ftrack_Shot_Tracker", u"Tasks", None));
        ___qtreewidgetitem1 = self.page_2_tree.headerItem()
        ___qtreewidgetitem1.setText(8, QCoreApplication.translate("ftrack_Shot_Tracker", u"Description", None));
        ___qtreewidgetitem1.setText(7, QCoreApplication.translate("ftrack_Shot_Tracker", u"Priority", None));
        ___qtreewidgetitem1.setText(6, QCoreApplication.translate("ftrack_Shot_Tracker", u"State", None));
        ___qtreewidgetitem1.setText(5, QCoreApplication.translate("ftrack_Shot_Tracker", u"Due date", None));
        ___qtreewidgetitem1.setText(4, QCoreApplication.translate("ftrack_Shot_Tracker", u"Start date", None));
        ___qtreewidgetitem1.setText(3, QCoreApplication.translate("ftrack_Shot_Tracker", u"Assignee", None));
        ___qtreewidgetitem1.setText(2, QCoreApplication.translate("ftrack_Shot_Tracker", u"Status", None));
        ___qtreewidgetitem1.setText(1, QCoreApplication.translate("ftrack_Shot_Tracker", u"Type", None));
        ___qtreewidgetitem1.setText(0, QCoreApplication.translate("ftrack_Shot_Tracker", u"Tasks", None));
        ___qtreewidgetitem2 = self.page_3_tree.headerItem()
        ___qtreewidgetitem2.setText(8, QCoreApplication.translate("ftrack_Shot_Tracker", u"Description", None));
        ___qtreewidgetitem2.setText(7, QCoreApplication.translate("ftrack_Shot_Tracker", u"Priority", None));
        ___qtreewidgetitem2.setText(6, QCoreApplication.translate("ftrack_Shot_Tracker", u"State", None));
        ___qtreewidgetitem2.setText(5, QCoreApplication.translate("ftrack_Shot_Tracker", u"Due date", None));
        ___qtreewidgetitem2.setText(4, QCoreApplication.translate("ftrack_Shot_Tracker", u"Start date", None));
        ___qtreewidgetitem2.setText(3, QCoreApplication.translate("ftrack_Shot_Tracker", u"Assignee", None));
        ___qtreewidgetitem2.setText(2, QCoreApplication.translate("ftrack_Shot_Tracker", u"Status", None));
        ___qtreewidgetitem2.setText(1, QCoreApplication.translate("ftrack_Shot_Tracker", u"Type", None));
        ___qtreewidgetitem2.setText(0, QCoreApplication.translate("ftrack_Shot_Tracker", u"Tasks", None));
        ___qtreewidgetitem3 = self.page_4_tree.headerItem()
        ___qtreewidgetitem3.setText(8, QCoreApplication.translate("ftrack_Shot_Tracker", u"Description", None));
        ___qtreewidgetitem3.setText(7, QCoreApplication.translate("ftrack_Shot_Tracker", u"Priority", None));
        ___qtreewidgetitem3.setText(6, QCoreApplication.translate("ftrack_Shot_Tracker", u"State", None));
        ___qtreewidgetitem3.setText(5, QCoreApplication.translate("ftrack_Shot_Tracker", u"Due date", None));
        ___qtreewidgetitem3.setText(4, QCoreApplication.translate("ftrack_Shot_Tracker", u"Start date", None));
        ___qtreewidgetitem3.setText(3, QCoreApplication.translate("ftrack_Shot_Tracker", u"Assignee", None));
        ___qtreewidgetitem3.setText(2, QCoreApplication.translate("ftrack_Shot_Tracker", u"Status", None));
        ___qtreewidgetitem3.setText(1, QCoreApplication.translate("ftrack_Shot_Tracker", u"Type", None));
        ___qtreewidgetitem3.setText(0, QCoreApplication.translate("ftrack_Shot_Tracker", u"Tasks", None));
    # retranslateUi

