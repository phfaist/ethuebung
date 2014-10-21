
import re
import os
import os.path

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from util import ContextAttributeSetter

import pdflatexex
from pdflatexex import PdfLatexError

from qtauto.ui_compilerwidget import Ui_CompilerWidget







class CompilerWidget(QWidget):
    def __init__(self, parent):
        super(CompilerWidget, self).__init__(parent=parent)

        self.ui = Ui_CompilerWidget()
        self.ui.setupUi(self)

        self.mainwin = None

        self.fn = None

    def setMainWin(self, mainwin):
        self.mainwin = mainwin

    def setOpenFile(self, fn):
        self.fn = fn
        self.ui.lblFilePath.setText(fn)


    @pyqtSlot()
    def on_btnCompileEx_clicked(self):
        self.run_latex(mode=pdflatexex.MODE_EX)

    @pyqtSlot()
    def on_btnCompileSol_clicked(self):
        self.run_latex(mode=pdflatexex.MODE_SOL)

    @pyqtSlot()
    def on_btnCompileTips_clicked(self):
        self.run_latex(mode=pdflatexex.MODE_TIPS)


    def run_latex(self, mode):

        def dynamic_log(msg):
            self.log(msg)
            dynamic_log.numlines_since_last_procevents += 1

            # and maybe process the display events
            if (dynamic_log.numlines_since_last_procevents > 10):
                QApplication.instance().processEvents(QEventLoop.ExcludeUserInputEvents)
                dynamic_log.numlines_since_last_procevents = 0
        dynamic_log.numlines_since_last_procevents = 0;

        with ContextAttributeSetter(
            (self.ui.btnCompileEx.isEnabled, self.ui.btnCompileEx.setEnabled, False),
            (self.ui.btnCompileSol.isEnabled, self.ui.btnCompileSol.setEnabled, False),
            (self.ui.btnCompileTips.isEnabled, self.ui.btnCompileTips.setEnabled, False),
            ):
            try:
                self.ui.txtLog.clear()
                QApplication.instance().processEvents() #QEventLoop.ExcludeUserInputEvents)
                
                pdflatexex.run(
                    texfile=self.fn,
                    pdflatex=self.mainwin.latexmode.latexprog(),
                    pdflatexopts=self.mainwin.latexmode.latexoptions(),
                    pdfbasename=self.mainwin.filenamingconvention.pdfname(
                        texfilename=self.fn,
                        mode=mode,
                        ext=self.mainwin.latexmode.outputext(),
                        option_for_pdflatexex=True),
                    mode=mode,
                    close_stdin=True,
                    capture_output=dynamic_log
                    )
            except PdfLatexError as e:
                self.log(u"Error generating %s: %s" %(self.sheetname(mode), unicode(e)))
            else:
                self.log(u"Successfully generated file %s" %(self.fnpdfname(mode=mode)))

    def log(self, msg):
        if msg[-1:] == '\n':
            # remove final newline
            msg = msg[:-1]
        self.ui.txtLog.append(msg)


    def sheetname(self, mode):
        return {
            pdflatexex.MODE_EX: 'exercise sheet',
            pdflatexex.MODE_SOL: 'solutions sheet',
            pdflatexex.MODE_TIPS: 'tips sheet',
            }[mode]

    def fnpdfname(self, mode):
        """
        Shortcut for getting the output file name. This calls
        `self.mainwin.filenamingconvention.pdfname()`.
        """
        return self.mainwin.filenamingconvention.pdfname(
            texfilename=self.fn,
            mode=mode,
            ext=self.mainwin.latexmode.outputext(),
            )

    @pyqtSlot()
    def on_btnShowEx_clicked(self):
        self.show_pdf(mode=pdflatexex.MODE_EX)

    @pyqtSlot()
    def on_btnShowSol_clicked(self):
        self.show_pdf(mode=pdflatexex.MODE_SOL)

    @pyqtSlot()
    def on_btnShowTips_clicked(self):
        self.show_pdf(mode=pdflatexex.MODE_TIPS)


    def show_pdf(self, mode):
        fnpdf = self.fnpdfname(mode=mode)
        fnpdfabs = os.path.realpath(os.path.abspath(fnpdf))
        
        if fnpdfabs[0] != '/': # e.g. because of drive name on windows
            fnpdfabs = '/'+fnpdfabs;

        if not os.path.exists(fnpdfabs):
            QMessageBox.critical(self, "Error", u"The file %s does not exist yet. compile it first!"%(fnpdf))
            return

        QDesktopServices.openUrl(QUrl("file://"+fnpdfabs))
