# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'settingsdialog.ui'
#
# Created: Fri Oct 24 12:40:11 2014
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

class Ui_SettingsDialog(object):
    def setupUi(self, SettingsDialog):
        SettingsDialog.setObjectName(_fromUtf8("SettingsDialog"))
        SettingsDialog.resize(575, 295)
        self.verticalLayout = QtGui.QVBoxLayout(SettingsDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gbxLatexMode = QtGui.QGroupBox(SettingsDialog)
        self.gbxLatexMode.setObjectName(_fromUtf8("gbxLatexMode"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.gbxLatexMode)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.cbxLatexMode = QtGui.QComboBox(self.gbxLatexMode)
        self.cbxLatexMode.setObjectName(_fromUtf8("cbxLatexMode"))
        self.cbxLatexMode.addItem(_fromUtf8(""))
        self.cbxLatexMode.addItem(_fromUtf8(""))
        self.verticalLayout_3.addWidget(self.cbxLatexMode)
        self.verticalLayout.addWidget(self.gbxLatexMode)
        self.groupBox = QtGui.QGroupBox(SettingsDialog)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.cbxFileNaming = QtGui.QComboBox(self.groupBox)
        self.cbxFileNaming.setObjectName(_fromUtf8("cbxFileNaming"))
        self.verticalLayout_2.addWidget(self.cbxFileNaming)
        self.lblFileNamingDesc = QtGui.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setItalic(True)
        self.lblFileNamingDesc.setFont(font)
        self.lblFileNamingDesc.setWordWrap(True)
        self.lblFileNamingDesc.setObjectName(_fromUtf8("lblFileNamingDesc"))
        self.verticalLayout_2.addWidget(self.lblFileNamingDesc)
        self.verticalLayout.addWidget(self.groupBox)
        spacerItem = QtGui.QSpacerItem(20, 61, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.btns = QtGui.QDialogButtonBox(SettingsDialog)
        self.btns.setOrientation(QtCore.Qt.Horizontal)
        self.btns.setStandardButtons(QtGui.QDialogButtonBox.Ok)
        self.btns.setObjectName(_fromUtf8("btns"))
        self.verticalLayout.addWidget(self.btns)

        self.retranslateUi(SettingsDialog)
        QtCore.QObject.connect(self.btns, QtCore.SIGNAL(_fromUtf8("accepted()")), SettingsDialog.accept)
        QtCore.QObject.connect(self.btns, QtCore.SIGNAL(_fromUtf8("rejected()")), SettingsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(SettingsDialog)

    def retranslateUi(self, SettingsDialog):
        SettingsDialog.setWindowTitle(_translate("SettingsDialog", "Settings", None))
        self.gbxLatexMode.setTitle(_translate("SettingsDialog", "LaTeX mode", None))
        self.cbxLatexMode.setItemText(0, _translate("SettingsDialog", "pdflatex (PDF)", None))
        self.cbxLatexMode.setItemText(1, _translate("SettingsDialog", "latex (DVI)", None))
        self.groupBox.setTitle(_translate("SettingsDialog", "Output file naming scheme", None))
        self.lblFileNamingDesc.setText(_translate("SettingsDialog", "Description of the naming scheme here.", None))

