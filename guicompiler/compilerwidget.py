
import re
import os
import os.path

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import pdflatexex

from qtauto.ui_compilerwidget import Ui_CompilerWidget


class CompilerWidget(QWidget):
    def __init__(self, parent):
        super(CompilerWidget, self).__init__(parent)

        self.ui = Ui_CompilerWidget()
        self.ui.setupUi(self)

        self.fn = None

        self.log_initialized = False
        

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
        try:
            pdflatexex.run(self.fn, pdflatexopts=[], mode=mode)
        except PdfLatexError as e:
            self.log(u"Error generating %s: %s" %(self.sheetname(mode), unicode(e)))
        else:
            self.log(u"Successfully generated file %s" %(self.fnpdfname(mode=mode)))

    def log(self, msg):
        if not self.log_initialized:
            self.ui.txtLog.setPlainText(u"")
            self.log_initialized = True
            
        self.ui.txtLog.append(msg)

    def sheetname(self, mode):
        return {
            pdflatex.MODE_EX: 'exercise sheet',
            pdflatex.MODE_SOL: 'solutions sheet',
            pdflatex.MODE_TIPS: 'tips sheet',
            }[mode]

    def fnpdfname(self, mode):
        suffix = {pdflatexex.MODE_EX: 'ex', pdflatexex.MODE_SOL: 'sol', pdflatexex.MODE_TIPS: 'tips'}[mode]
        return pdflatexex.rx_latex.sub('_'+suffix+'.pdf', self.fn)
        

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

        QDesktopServices.openUrl(QUrl("file://"+fnpdfabs))
