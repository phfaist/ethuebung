# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'compilerwidget.ui'
#
# Created: Sat Oct 25 15:44:01 2014
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

class Ui_CompilerWidget(object):
    def setupUi(self, CompilerWidget):
        CompilerWidget.setObjectName(_fromUtf8("CompilerWidget"))
        CompilerWidget.resize(626, 451)
        self.verticalLayout = QtGui.QVBoxLayout(CompilerWidget)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.frame = QtGui.QFrame(CompilerWidget)
        self.frame.setFrameShape(QtGui.QFrame.WinPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Sunken)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.frame)
        self.horizontalLayout_3.setContentsMargins(3, 5, 3, 5)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.lblFilePath = QtGui.QLabel(self.frame)
        self.lblFilePath.setTextFormat(QtCore.Qt.PlainText)
        self.lblFilePath.setTextInteractionFlags(QtCore.Qt.TextBrowserInteraction)
        self.lblFilePath.setObjectName(_fromUtf8("lblFilePath"))
        self.horizontalLayout_3.addWidget(self.lblFilePath)
        self.verticalLayout.addWidget(self.frame)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.btnCompileEx = QtGui.QPushButton(CompilerWidget)
        self.btnCompileEx.setObjectName(_fromUtf8("btnCompileEx"))
        self.horizontalLayout.addWidget(self.btnCompileEx)
        self.btnCompileSol = QtGui.QPushButton(CompilerWidget)
        self.btnCompileSol.setObjectName(_fromUtf8("btnCompileSol"))
        self.horizontalLayout.addWidget(self.btnCompileSol)
        self.btnCompileTips = QtGui.QPushButton(CompilerWidget)
        self.btnCompileTips.setObjectName(_fromUtf8("btnCompileTips"))
        self.horizontalLayout.addWidget(self.btnCompileTips)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.txtLog = QtGui.QTextEdit(CompilerWidget)
        self.txtLog.setTabChangesFocus(True)
        self.txtLog.setUndoRedoEnabled(False)
        self.txtLog.setReadOnly(True)
        self.txtLog.setObjectName(_fromUtf8("txtLog"))
        self.verticalLayout.addWidget(self.txtLog)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.btnShowEx = QtGui.QPushButton(CompilerWidget)
        self.btnShowEx.setObjectName(_fromUtf8("btnShowEx"))
        self.horizontalLayout_2.addWidget(self.btnShowEx)
        self.btnShowSol = QtGui.QPushButton(CompilerWidget)
        self.btnShowSol.setObjectName(_fromUtf8("btnShowSol"))
        self.horizontalLayout_2.addWidget(self.btnShowSol)
        self.btnShowTips = QtGui.QPushButton(CompilerWidget)
        self.btnShowTips.setObjectName(_fromUtf8("btnShowTips"))
        self.horizontalLayout_2.addWidget(self.btnShowTips)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(CompilerWidget)
        QtCore.QMetaObject.connectSlotsByName(CompilerWidget)

    def retranslateUi(self, CompilerWidget):
        CompilerWidget.setWindowTitle(_translate("CompilerWidget", "Form", None))
        self.lblFilePath.setText(_translate("CompilerWidget", "/home/pfaist/myfile.tex", None))
        self.btnCompileEx.setText(_translate("CompilerWidget", "Compile EXERCISE Sheet", None))
        self.btnCompileSol.setText(_translate("CompilerWidget", "Compile SOLUTIONS Sheet", None))
        self.btnCompileTips.setText(_translate("CompilerWidget", "Compile TIPS Sheet", None))
        self.txtLog.setHtml(_translate("CompilerWidget", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Lucida Grande\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p></body></html>", None))
        self.btnShowEx.setText(_translate("CompilerWidget", "Show EXERCISE Sheet", None))
        self.btnShowSol.setText(_translate("CompilerWidget", "Show SOLUTIONS Sheet", None))
        self.btnShowTips.setText(_translate("CompilerWidget", "Show TIPS Sheet", None))

