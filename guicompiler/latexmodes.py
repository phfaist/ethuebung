
import re

import pdflatexex


class LatexMode(object):
    def __init__(self, **kwargs):
        super(LatexMode, self).__init__(**kwargs)

    def title(self):
        raise NotImplementedError("Subclasses must reimplement title()!")

    def latexprog(self):
        raise NotImplementedError("Subclasses must reimplement latexprog()!")

    def latexoptions(self):
        raise NotImplementedError("Subclasses must reimplement latexoptions()!")

    def outputext(self):
        raise NotImplementedError("Subclasses must reimplement outputext()!")


class PdflatexMode(LatexMode):
    def title(self):
        return "pdflatex (PDF)"

    def latexprog(self):
        return pdflatexex.resolve_path("pdflatex")

    def latexoptions(self):
        return []
    
    def outputext(self):
        return "pdf"


class LatexDviMode(LatexMode):
    def title(self):
        return "latex (DVI)"

    def latexprog(self):
        return pdflatexex.resolve_path("latex")

    def latexoptions(self):
        return []
    
    def outputext(self):
        return "dvi"



latex_modes = [
    PdflatexMode(),
    LatexDviMode()
    ]

