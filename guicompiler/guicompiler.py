
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from ui import Ui_MainWidget


class WelcomeWidget(QWidget):
    def __init__(self):
        super(WelcomeWidget, self).__init__()

        self.ui = Ui_WelcomeWidget()
        self.ui.setupUi(self)

    @pyqtslot()
    def on_btnOpenFile_clicked(self):
        pass

    @pyqtslot()
    def on_btnQuit_clicked(self):
        

    
