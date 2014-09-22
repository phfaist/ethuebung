
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from qtauto.ui_compilerwidget import Ui_CompilerWidget


class CompilerWidget(QWidget):
    def __init__(self, parent):
        super(CompilerWidget, self).__init__(parent)

        self.ui = Ui_CompilerWidget()
        self.ui.setupUi(self)

        self.fn = None

    def setOpenFile(self, fn):
        self.fn = fn
        self.lblFileName.setText(fn)

        
