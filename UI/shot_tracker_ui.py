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
from PySide6.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QLabel,
    QMainWindow, QSizePolicy, QStackedWidget, QVBoxLayout,
    QWidget)

class Ui_ftrack_Shot_Tracker(object):
    def setupUi(self, ftrack_Shot_Tracker):
        if not ftrack_Shot_Tracker.objectName():
            ftrack_Shot_Tracker.setObjectName(u"ftrack_Shot_Tracker")
        ftrack_Shot_Tracker.resize(800, 600)
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
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.horizontalLayout_4 = QHBoxLayout(self.page)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label = QLabel(self.page)
        self.label.setObjectName(u"label")

        self.horizontalLayout_4.addWidget(self.label)

        self.page_widget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.horizontalLayout_3 = QHBoxLayout(self.page_2)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_2 = QLabel(self.page_2)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_3.addWidget(self.label_2)

        self.page_widget.addWidget(self.page_2)
        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")
        self.horizontalLayout_2 = QHBoxLayout(self.page_3)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_3 = QLabel(self.page_3)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_2.addWidget(self.label_3)

        self.page_widget.addWidget(self.page_3)
        self.page_4 = QWidget()
        self.page_4.setObjectName(u"page_4")
        self.horizontalLayout = QHBoxLayout(self.page_4)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_4 = QLabel(self.page_4)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout.addWidget(self.label_4)

        self.page_widget.addWidget(self.page_4)

        self.verticalLayout.addWidget(self.page_widget)

        ftrack_Shot_Tracker.setCentralWidget(self.centralwidget)

        self.retranslateUi(ftrack_Shot_Tracker)

        QMetaObject.connectSlotsByName(ftrack_Shot_Tracker)
    # setupUi

    def retranslateUi(self, ftrack_Shot_Tracker):
        ftrack_Shot_Tracker.setWindowTitle(QCoreApplication.translate("ftrack_Shot_Tracker", u"ftrack Shot Tracker", None))
        self.label.setText(QCoreApplication.translate("ftrack_Shot_Tracker", u"page1", None))
        self.label_2.setText(QCoreApplication.translate("ftrack_Shot_Tracker", u"page2", None))
        self.label_3.setText(QCoreApplication.translate("ftrack_Shot_Tracker", u"page3", None))
        self.label_4.setText(QCoreApplication.translate("ftrack_Shot_Tracker", u"page4", None))
    # retranslateUi

