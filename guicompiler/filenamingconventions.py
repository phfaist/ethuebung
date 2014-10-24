
import re
import os.path

import pdflatexex_mod as pdflatexex


class FileNamingConvention(object):
    def __init__(self, **kwargs):
        super(FileNamingConvention, self).__init__(**kwargs)

    def title(self, **kwargs):
        raise NotImplementedError("Subclasses should reimplement title()")

    def description(self, **kwargs):
        raise NotImplementedError("Subclasses should reimplement description()")

    def pdfname(self, texfilename, mode, ext='pdf', option_for_pdflatexex=False, **kwargs):
        """
        Returns the name of the PDF file that is generated when generating the sheet in
        the given mode. `mode` should be one of `pdflatexex.MODE_EX`,
        `pdflatexex.MODE_SOL` or `pdflatexex.MODE_TIPS`.

        If `option_for_pdflatexex` is `False`, then the complete file name of the
        corresponding PDF file is returned. If `option_for_pdflatexex` is `True`, then the
        return value should be suitable to pass as the `pdfbasename` argument to
        `pdflatexex.run()`.

        This function should account for possibly different output extensions, not only
        'pdf'. The relevant extension is provided as the `ext` parameter.

        The default implementation raises `NotImplementedError`. Don't forget to override
        this method.
        """
        raise NotImplementedError("Subclasses should reimplement pdfname()")





class DefaultNamingConvention(FileNamingConvention):
    """
    Simple `FileNamingConvention` object that describes `pdflatexex` default naming
    convention.
    """
    def __init__(self):
        super(DefaultNamingConvention, self).__init__()

    def title(self, **kwargs):
        return "Default"

    def description(self, ext='pdf', **kwargs):
        return (
            "Add suffix ***_ex.%(ext)s, ***_sol.%(ext)s and ***_tips.%(ext)s" %{'ext': ext}
            )

    def pdfname(self, texfilename, mode, ext='pdf', option_for_pdflatexex=False, **kwargs):
        if option_for_pdflatexex:
            return None

        suffix = pdflatexex.defaultsuffix(mode)
        return pdflatexex.rx_latex.sub('_'+suffix+'.'+ext, texfilename)



class ConvenientNamingConvention(FileNamingConvention):
    """
    Returns the name of the PDF file that is generated when generating sheet in mode
    `mode`. If the tex file is named 'exNN.tex', then this is 'exNN.pdf', 'solNN.pdf'
    or 'tipsNN.pdf'. Otherwise, a suffix '_ex.pdf', '_sol.pdf' or '_tips.pdf' is
    added.

    If `option_for_pdflatexex` is `True`, then `None` is returned if the sheet is not
    named 'exNN.tex', and only the basename is returned in the other cases. (This is
    only useful for passing to the `pdflatexex` module.)
    """
    def __init__(self):
        super(ConvenientNamingConvention, self).__init__()
        # DefaultNamingConvention object to fall back to for non-"exNN.tex" files
        self._default_namingconvention = DefaultNamingConvention()

    def title(self, ext='pdf', **kwargs):
        return (
            "Convenient (exNN.%(ext)s, solNN.%(ext)s, tipsNN.%(ext)s)"
            %{ 'ext': ext }
            )
    def description(self, ext='pdf', **kwargs):
        return (
            u"For files `exNN.tex' \u2192 exNN.%(ext)s, solNN.%(ext)s, tipsNN.%(ext)s; otherwise as"
            u" for `Default' naming convention"
            ) % { 'ext': ext }

    def pdfname(self, texfilename, mode, ext='pdf', option_for_pdflatexex=False):
        m = re.match(r'ex(?P<num>\d+)\.tex', os.path.basename(texfilename))
        if m:
            basename = {
                pdflatexex.MODE_EX:   'ex'+m.group('num'),
                pdflatexex.MODE_SOL:  'sol'+m.group('num'),
                pdflatexex.MODE_TIPS: 'tips'+m.group('num'),
                }[mode]
            if option_for_pdflatexex:
                return basename
            return os.path.dirname(texfilename) + '/' + basename + '.' + ext

        return self._default_namingconvention.pdfname(texfilename=texfilename,
                                                      mode=mode,
                                                      ext=ext,
                                                      option_for_pdflatexex=option_for_pdflatexex)




naming_conventions = [
    DefaultNamingConvention(),
    ConvenientNamingConvention(),
    ]



def get_naming_convention(clsname):
    global naming_conventions

    if not isinstance(clsname, basestring):
        clsname = clsname.__name__

    return next(iter( (naming for naming in naming_conventions
                       if naming.__class__.__name__ == clsname) ))
