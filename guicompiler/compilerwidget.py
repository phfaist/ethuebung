
import re
import os
import os.path

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import pdflatexex
from pdflatexex import PdfLatexError

from qtauto.ui_compilerwidget import Ui_CompilerWidget




class ContextAttributeSetter:
    """Give a list of pairs of method and value to set.

    For example:

    >>> with ContextAttributeSetter( (object.isEnabled, object.setEnabled, False), ):
            ...

    will retreive the current state of if the object is enabled with `object.isEnabled()`, then
    will disable the object with `object.setEnabled(False)`. Upon exiting the with block, the
    state is restored to its original state with `object.setEnabled(..)`.

    """

    def __init__(self, *args):
        """Constructor. Does initializations. The \"enter\" statement is done with __enter__().

        Note: the argument are a list of 3-tuples `(get_method, set_method, set_to_value)`.
        """
        self.attribpairs = args
        self.initvals = None

    def __enter__(self):
        self.initvals = []
        for (getm, setm, v) in self.attribpairs:
            self.initvals.append(getm())
            setm(v)
            
        return self

    def __exit__(self, type, value, traceback):
        # clean-up
        for i in xrange(len(self.attribpairs)):
            (getm, setm, v) = self.attribpairs[i]
            setm(self.initvals[i])











class CompilerWidget(QWidget):
    def __init__(self, parent):
        super(CompilerWidget, self).__init__(parent)

        self.ui = Ui_CompilerWidget()
        self.ui.setupUi(self)

        self.fn = None
        

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
                QApplication.instance().processEvents(QEventLoop.ExcludeUserInputEvents)
                
                pdflatexex.run(self.fn, #pdflatexopts=['-interaction=batchmode'],
                               pdfbasename=self.fnpdfname(mode=mode, option_for_pdflatexex=True),
                               mode=mode, close_stdin=True,
                               capture_output=dynamic_log)
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

    def fnpdfname(self, mode, option_for_pdflatexex=False):
        """
        Returns the name of the PDF file that is generated when generating sheet in mode
        `mode`. If the tex file is named 'exNN.tex', then this is 'exNN.pdf', 'solNN.pdf'
        or 'tipsNN.pdf'. Otherwise, a suffix '_ex.pdf', '_sol.pdf' or '_tips.pdf' is
        added.

        If `option_for_pdflatexex` is `True`, then `None` is returned if the sheet is not
        named 'exNN.tex', and only the basename is returned in the other cases. (This is
        only useful for passing to the `pdflatexex` module.)
        """
        m = re.match(r'ex(?P<num>\d+)\.tex', os.path.basename(self.fn))
        if m:
            basename = {
                pdflatexex.MODE_EX:   'ex'+m.group('num'),
                pdflatexex.MODE_SOL:  'sol'+m.group('num'),
                pdflatexex.MODE_TIPS: 'tips'+m.group('num'),
                }[mode]
            if option_for_pdflatexex:
                return basename
            return os.path.dirname(self.fn) + '/' + basename + '.pdf'

        if option_for_pdflatexex:
            return None
        
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
            return

        QDesktopServices.openUrl(QUrl("file://"+fnpdfabs))
