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

import filenamingconventions
import latexmodes
from util import ContextAttributeSetter

import compilerwidget

from qtauto.ui_mainwidget import Ui_MainWidget
from qtauto.ui_settingsdialog import Ui_SettingsDialog


class MainWidget(QMainWindow):
    def __init__(self):
        super(MainWidget, self).__init__()

        #self.setAttribute(Qt.WA_MacBrushedMetal) # doesn't show well

        self.ui = Ui_MainWidget()
        self.ui.setupUi(self)

        # dict of canonical file names to 
        self.opendocuments = []
        self.documentwidgets = {}

        # current latex mode
        self.latexmode = None
        # current file naming convention
        self.filenamingconvention = None
        # load the settings
        self.loadsettings()

        # the settings dialog will be instanciated only upon need
        self.settingsdialog = None


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
        self.close()

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
        w.setMainWin(self)
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



    def loadsettings(self):
        settings = QSettings()

        settings.beginGroup('latexstuff')
        latexmodecls = str(settings.value("latexmode").toString())
        self.latexmode = next(iter( (mode for mode in latexmodes.latex_modes
                                     if mode.__class__.__name__ == latexmodecls) ),
                              None)
        if not self.latexmode:
            if latexmodecls:
                sys.stderr.write("Can't find latex mode: %s\n"%(latexmodecls))
            self.latexmode = latexmodes.latex_modes[0]

        filenamingconventioncls = str(settings.value("filenamingconvention").toString())
        self.filenamingconvention = next(
            iter( (filenaming for filenaming in filenamingconventions.naming_conventions
                   if filenaming.__class__.__name__ == filenamingconventioncls)
                  ),
            None)
        if not self.filenamingconvention:
            if filenamingconventioncls:
                sys.stderr.write("Can't find file naming convention: %s\n"%(filenamingconventioncls))
            self.filenamingconvention = filenamingconventions.get_naming_convention('ConvenientNamingConvention')
        settings.endGroup()

        settings.beginGroup('openfiles')
        arraylen = settings.beginReadArray('file_list')
        for ind in range(arraylen):
            settings.setArrayIndex(ind)
            fn = str(settings.value('filename').toString())
            self.openFile(fn)
        settings.endArray()
        settings.endGroup()

    def savesettings(self):
        settings = QSettings()

        settings.beginGroup('latexstuff')
        settings.setValue('latexmode', QString(self.latexmode.__class__.__name__))
        settings.setValue('filenamingconvention', QString(self.filenamingconvention.__class__.__name__))
        settings.endGroup()

        settings.beginGroup('openfiles')
        settings.beginWriteArray('file_list', len(self.opendocuments))
        for ind in range(len(self.opendocuments)):
            settings.setArrayIndex(ind)
            settings.setValue('filename', QString(self.opendocuments[ind]))
        settings.endArray()
        settings.endGroup()

    @pyqtSlot()
    def on_aSettingsDialog_triggered(self):
        if self.settingsdialog is None:
            self.settingsdialog = SettingsDialog(mainwin=self)

        self.settingsdialog.showSettings()

    def closeEvent(self, closeevent):
        print "Closing!"
        self.savesettings()
        super(MainWidget, self).closeEvent(closeevent)


class SettingsDialog(QDialog):
    def __init__(self, mainwin, **kwargs):
        super(SettingsDialog, self).__init__(parent=mainwin)
        self.ui = Ui_SettingsDialog()
        self.ui.setupUi(self)

        self.mainwin = None
        
        #with ContextAttributeSetter(
        #    (self.ui.cbxLatexMode.blockSignals, self.ui.cbxLatexMode.signalsBlocked, True),
        #    (self.ui.cbxFileNaming.blockSignals, self.ui.cbxFileNaming.signalsBlocked, True),
        #    ):
        #    # set up the initial values, without re-updating the main windows' settings at this point
        self.setupLatexModes()
        self.setupFileNamingConventions()

        self.mainwin = mainwin



    def showSettings(self):
        self.show()
        try:
            blk1 = self.ui.cbxLatexMode.blockSignals(True)
            blk2 = self.ui.cbxFileNaming.blockSignals(True)
            # set up the initial values, without re-updating the main windows' settings at this point
            idx = latexmodes.latex_modes.index(self.mainwin.latexmode)
            self.ui.cbxLatexMode.setCurrentIndex(idx)
            idx = filenamingconventions.naming_conventions.index(self.mainwin.filenamingconvention)
            self.ui.cbxFileNaming.setCurrentIndex(idx)
            self.updateFileNamingConventionDescription()
        finally:
            self.ui.cbxLatexMode.blockSignals(blk1)
            self.ui.cbxFileNaming.blockSignals(blk2)
            
    
    def setupLatexModes(self):
        self.ui.cbxLatexMode.clear()
        for mode in latexmodes.latex_modes:
            self.ui.cbxLatexMode.addItem(mode.title(), QVariant(QString(str(mode.__class__.__name__))))

    @pyqtSlot(int)
    def on_cbxLatexMode_activated(self, index):
        if not self.mainwin:
            return
        cls = str(self.ui.cbxLatexMode.itemData(index).toString())
        try:
            latexmode = next(iter( (mode for mode in latexmodes.latex_modes if mode.__class__.__name__ == cls) ))
        except StopIteration:
            logger.warning("Couldn't find mode: %s", cls)
            return

        self.mainwin.latexmode = latexmode
        self.updateFileNamingConventions()

    def setupFileNamingConventions(self):
        self.ui.cbxFileNaming.clear()
            
        titlekwargs = {}
        if self.mainwin:
            titlekwargs['ext'] = self.mainwin.latexmode.outputext()

        for filenaming in filenamingconventions.naming_conventions:
            self.ui.cbxFileNaming.addItem(filenaming.title(**titlekwargs),
                                          QVariant(QString(str(filenaming.__class__.__name__))))

    def updateFileNamingConventions(self):
        titlekwargs = {}
        if self.mainwin:
            titlekwargs['ext'] = self.mainwin.latexmode.outputext()

        for k in range(self.ui.cbxFileNaming.count()):
            self.ui.cbxFileNaming.setItemText(
                k,
                filenamingconventions.naming_conventions[k].title(**titlekwargs)
                )
        self.updateFileNamingConventionDescription()

    def updateFileNamingConventionDescription(self, index=None):
        titlekwargs = {}
        if self.mainwin:
            titlekwargs['ext'] = self.mainwin.latexmode.outputext()

        if index is None:
            index = self.ui.cbxFileNaming.currentIndex()
            
        if index >= 0 and index < self.ui.cbxFileNaming.count():
            text = filenamingconventions.naming_conventions[index].description(**titlekwargs)
        else:
            text = ""
            
        self.ui.lblFileNamingDesc.setText(text)

    @pyqtSlot(int)
    def on_cbxFileNaming_activated(self, index):
        self.updateFileNamingConventionDescription(index)

        cls = str(self.ui.cbxFileNaming.itemData(index).toString())
        try:
            filenaming = next(iter(
                (mode for mode in filenamingconventions.naming_conventions if mode.__class__.__name__ == cls)
                ))
        except StopIteration:
            logger.warning("Couldn't find file naming scheme: %s", cls)
            return

        self.mainwin.filenamingconvention = filenaming
        



class GuiCompilerApplication(QApplication):
    def __init__(self):
        self.main_widget = None
        
        super(GuiCompilerApplication, self).__init__(sys.argv)
        
        self.setWindowIcon(QIcon(':/pic/ueb.png'))
        self.setApplicationName('ethuebung GuiCompiler')
        self.setApplicationVersion("1.0")
        self.setOrganizationDomain('org.ethuebung')
        self.setOrganizationName('ethuebung')


    def setup(self):

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

    app.setup()

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
