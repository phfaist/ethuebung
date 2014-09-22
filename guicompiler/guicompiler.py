#!/usr/bin/env python
# -*- coding: utf-8 -*-



import sys
import os
import os.path


from PyQt4.QtCore import *
from PyQt4.QtGui import *

import compilerwidget

from qtauto.ui_mainwidget import Ui_MainWidget


class MainWidget(QMainWindow):
    def __init__(self):
        super(MainWidget, self).__init__()

        self.ui = Ui_MainWidget()
        self.ui.setupUi(self)

        # dict of canonical file names to 
        self.opendocuments = {}

    @pyqtSlot()
    def on_aOpenFile_triggered(self):
        fname = str(QFileDialog.getOpenFileName(self, 'Open LaTeX/ethuebung File', QString(),
                                                'LaTeX Files (*.tex *.latex);;All Files (*)'))
        if not fname:
            return

        self.openFile(fname)

    @pyqtSlot()
    def on_aQuit_triggered(self):
        QApplication.instance.quit()

    @pyqtSlot(QString)
    def openFile(self, fn):
        fn = os.path.realpath(str(fn))
        fnbase = os.path.basename(fn)

        if fn in self.opendocuments:
            self.ui.tabs.setCurrentWidget(opendocuments[fn])
            return

        w = compilerwidget.CompilerWidget(self.ui.tabs)
        w.setOpenFile(fn)
        w.fileClosed.connect(self.bibFileClosed)
        self.ui.tabs.addTab(w, fnbase)
        self.opendocuments[fn] = w

    @pyqtSlot(int)
    def on_tabs_tabCloseRequested(self, index):
        if (index == 0):
            # can't close `Home' tab
            return
        
        del self.opendocuments[index-1]
        self.ui.tabs.removeTab(index)




class GuiCompilerApplication(QApplication):
    def __init__(self):
        self.main_widget = None
        
        super(BibolamaziApplication, self).__init__(sys.argv)
        
        self.setWindowIcon(QIcon(':/pic/ueb.png'))
        self.setApplicationName('ethuebung GuiCompiler')
        self.setApplicationVersion("1.0")
        self.setOrganizationDomain('org.ethuebung')
        self.setOrganizationName('ethuebung')

        # create & setup main widget
        self.main_widget = MainWidget()

        self.main_widget.show()
        self.main_widget.raise_()


    def event(self, event):
        if (event.type() == QEvent.FileOpen):
            print "Opening file %s" %(event.file())
            # request to open file
            if (self.main_widget is None):
                print "ERROR: CAN'T OPEN FILE: MAIN WIDGET IS NONE!"
            else:
                self.main_widget.openFile(event.file())
            return True
        return super(BibolamaziApplication, self).event(event)




def run_main():

    app = GuiCompilerApplication();

    args = app.arguments();
    _rxscript = re.compile('\.(py[co]?|exe)$', flags=re.IGNORECASE);
    for k in xrange(1,len(args)): # skip program name == argv[0]
        fn = str(args[k])
        if (_rxscript.search(fn)):
            # our own script, bug on windows?
            print "skipping own arg: %s" %(fn)
            continue
        
        print "opening arg: %s" % (fn)
        app.main_widget.openFile(fn);

    sys.exit(app.exec_())
    

if __name__ == '__main__':
    run_main()
