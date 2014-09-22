# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwidget.ui'
#
# Created: Mon Sep 22 19:19:46 2014
#      by: PyQt4 UI code generator 4.10.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(759, 537)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tabs = QtGui.QTabWidget(self.centralwidget)
        self.tabs.setTabPosition(QtGui.QTabWidget.South)
        self.tabs.setUsesScrollButtons(True)
        self.tabs.setDocumentMode(True)
        self.tabs.setTabsClosable(True)
        self.tabs.setMovable(True)
        self.tabs.setObjectName(_fromUtf8("tabs"))
        self.tabHome = QtGui.QWidget()
        self.tabHome.setObjectName(_fromUtf8("tabHome"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.tabHome)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.lblWelcome = QtGui.QLabel(self.tabHome)
        self.lblWelcome.setMinimumSize(QtCore.QSize(0, 50))
        self.lblWelcome.setPixmap(QtGui.QPixmap(_fromUtf8(":/pic/ethuebungcompiler.png")))
        self.lblWelcome.setAlignment(QtCore.Qt.AlignCenter)
        self.lblWelcome.setObjectName(_fromUtf8("lblWelcome"))
        self.verticalLayout_2.addWidget(self.lblWelcome)
        spacerItem = QtGui.QSpacerItem(20, 96, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.btnOpenFile = QtGui.QPushButton(self.tabHome)
        self.btnOpenFile.setObjectName(_fromUtf8("btnOpenFile"))
        self.verticalLayout_2.addWidget(self.btnOpenFile)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        spacerItem2 = QtGui.QSpacerItem(20, 96, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem2)
        self.tabs.addTab(self.tabHome, _fromUtf8(""))
        self.verticalLayout.addWidget(self.tabs)
        MainWindow.setCentralWidget(self.centralwidget)
        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        MainWindow.insertToolBarBreak(self.toolBar)
        self.aOpenFile = QtGui.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/pic/file.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.aOpenFile.setIcon(icon)
        self.aOpenFile.setObjectName(_fromUtf8("aOpenFile"))
        self.aQuit = QtGui.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/pic/closehide.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.aQuit.setIcon(icon1)
        self.aQuit.setObjectName(_fromUtf8("aQuit"))
        self.toolBar.addAction(self.aOpenFile)
        self.toolBar.addAction(self.aQuit)

        self.retranslateUi(MainWindow)
        self.tabs.setCurrentIndex(0)
        QtCore.QObject.connect(self.btnOpenFile, QtCore.SIGNAL(_fromUtf8("clicked()")), self.aOpenFile.trigger)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.btnOpenFile.setText(_translate("MainWindow", "Open LaTeX File ...", None))
        self.tabs.setTabText(self.tabs.indexOf(self.tabHome), _translate("MainWindow", "Home", None))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar", None))
        self.aOpenFile.setText(_translate("MainWindow", "Open File ...", None))
        self.aOpenFile.setIconText(_translate("MainWindow", "Open File ...", None))
        self.aOpenFile.setToolTip(_translate("MainWindow", "Choose LaTeX file to open", None))
        self.aOpenFile.setShortcut(_translate("MainWindow", "Ctrl+O", None))
        self.aQuit.setText(_translate("MainWindow", "Quit", None))
        self.aQuit.setToolTip(_translate("MainWindow", "Close Application", None))

import guicompiler_rc
