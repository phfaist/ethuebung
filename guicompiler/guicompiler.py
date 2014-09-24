#!/usr/bin/env python
# -*- coding: utf-8 -*-



import sys
import os
import os.path
import re


from PyQt4.QtCore import *
from PyQt4.QtGui import *

# load pdflatexex
sys.path += [os.path.dirname(os.path.realpath(__file__))+'/../bin'];
import pdflatexex

import compilerwidget

from qtauto.ui_mainwidget import Ui_MainWidget


class MainWidget(QMainWindow):
    def __init__(self):
        super(MainWidget, self).__init__()

        #self.setAttribute(Qt.WA_MacBrushedMetal) # doesn't show well

        self.ui = Ui_MainWidget()
        self.ui.setupUi(self)

        # dict of canonical file names to 
        self.opendocuments = []
        self.documentwidgets = {}

    @pyqtSlot()
    def on_aOpenFile_triggered(self):
        fname = str(QFileDialog.getOpenFileName(self, 'Open LaTeX/ethuebung File', QString(),
                                                'LaTeX Files (*.tex *.latex);;All Files (*)'))
        if not fname:
            return

        self.openFile(fname)

    @pyqtSlot()
    def on_aCloseFile_triggered(self):
        self.closeCurrentFile()

    @pyqtSlot()
    def on_aQuit_triggered(self):
        QApplication.instance().quit()

    @pyqtSlot(QString)
    def openFile(self, fn):
        fn = os.path.realpath(str(fn))
        fnbase = os.path.basename(fn)

        if not pdflatexex.rx_latex.search(fn):
            QMessageBox.critical(self, "Not a LaTeX file",
                                 "The file `%s' does not look like a latex file. Please select a file "
                                 "with extension `.tex' or `.latex'.")
            return

        if fn in self.documentwidgets:
            self.ui.tabs.setCurrentWidget(self.documentwidgets[fn])
            return

        w = compilerwidget.CompilerWidget(self.ui.tabs)
        w.setOpenFile(fn)
        self.ui.tabs.addTab(w, fnbase)
        self.ui.tabs.setCurrentWidget(w)
        self.opendocuments.append(fn)
        self.documentwidgets[fn] = w

    @pyqtSlot()
    def closeCurrentFile(self):
        self.closeTab(self.ui.tabs.currentIndex())

    @pyqtSlot(int)
    def closeTab(self, index):
        if (index == 0):
            # can't close `Home' tab
            return
        
        fn = self.opendocuments[index-1]
        del self.documentwidgets[fn]
        del self.opendocuments[index-1]
        self.ui.tabs.removeTab(index)

    @pyqtSlot(int)
    def on_tabs_tabCloseRequested(self, index):
        self.closeTab(index)




class GuiCompilerApplication(QApplication):
    def __init__(self):
        self.main_widget = None
        
        super(GuiCompilerApplication, self).__init__(sys.argv)
        
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
        return super(GuiCompilerApplication, self).event(event)




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
