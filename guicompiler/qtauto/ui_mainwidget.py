# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwidget.ui'
#
# Created: Fri Sep 26 00:28:33 2014
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

class Ui_MainWidget(object):
    def setupUi(self, MainWidget):
        MainWidget.setObjectName(_fromUtf8("MainWidget"))
        MainWidget.resize(667, 325)
        MainWidget.setUnifiedTitleAndToolBarOnMac(True)
        self.centralwidget = QtGui.QWidget(MainWidget)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setMargin(0)
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
        spacerItem = QtGui.QSpacerItem(20, 35, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.btnOpenFile = QtGui.QPushButton(self.tabHome)
        self.btnOpenFile.setObjectName(_fromUtf8("btnOpenFile"))
        self.verticalLayout_2.addWidget(self.btnOpenFile)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        spacerItem2 = QtGui.QSpacerItem(20, 35, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem2)
        self.tabs.addTab(self.tabHome, _fromUtf8(""))
        self.verticalLayout.addWidget(self.tabs)
        MainWidget.setCentralWidget(self.centralwidget)
        self.toolBar = QtGui.QToolBar(MainWidget)
        self.toolBar.setMovable(False)
        self.toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.toolBar.setFloatable(False)
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        MainWidget.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        MainWidget.insertToolBarBreak(self.toolBar)
        self.aOpenFile = QtGui.QAction(MainWidget)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/pic/file.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.aOpenFile.setIcon(icon)
        self.aOpenFile.setObjectName(_fromUtf8("aOpenFile"))
        self.aQuit = QtGui.QAction(MainWidget)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/pic/closehide.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.aQuit.setIcon(icon1)
        self.aQuit.setObjectName(_fromUtf8("aQuit"))
        self.aCloseFile = QtGui.QAction(MainWidget)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/pic/closefile.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.aCloseFile.setIcon(icon2)
        self.aCloseFile.setObjectName(_fromUtf8("aCloseFile"))
        self.toolBar.addAction(self.aOpenFile)
        self.toolBar.addAction(self.aCloseFile)
        self.toolBar.addAction(self.aQuit)

        self.retranslateUi(MainWidget)
        self.tabs.setCurrentIndex(0)
        QtCore.QObject.connect(self.btnOpenFile, QtCore.SIGNAL(_fromUtf8("clicked()")), self.aOpenFile.trigger)
        QtCore.QMetaObject.connectSlotsByName(MainWidget)

    def retranslateUi(self, MainWidget):
        MainWidget.setWindowTitle(_translate("MainWidget", "MainWindow", None))
        self.btnOpenFile.setText(_translate("MainWidget", "Open LaTeX File ...", None))
        self.tabs.setTabText(self.tabs.indexOf(self.tabHome), _translate("MainWidget", "Home", None))
        self.toolBar.setWindowTitle(_translate("MainWidget", "toolBar", None))
        self.aOpenFile.setText(_translate("MainWidget", "Open File", None))
        self.aOpenFile.setToolTip(_translate("MainWidget", "Choose LaTeX file to open", None))
        self.aOpenFile.setShortcut(_translate("MainWidget", "Ctrl+O", None))
        self.aQuit.setText(_translate("MainWidget", "Quit", None))
        self.aQuit.setToolTip(_translate("MainWidget", "Close Application", None))
        self.aCloseFile.setText(_translate("MainWidget", "Close File", None))
        self.aCloseFile.setToolTip(_translate("MainWidget", "Close the currently open file", None))
        self.aCloseFile.setShortcut(_translate("MainWidget", "Ctrl+W", None))

import guicompiler_rc
