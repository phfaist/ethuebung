#!/usr/bin/env python

import sys
import re
import os
import os.path
import subprocess
import tempfile
import argparse
import shutil




# see  http://stackoverflow.com/a/10555130/1694896

def resolve_path(executable):
    if os.name == 'nt':
        # windows: use custom resolver
        return windows_resolve_path(executable)
    return subprocess.Popen(
        "which '%s'"%(re.sub(r"'", r"'\''", executable)),
        shell=True, stderr=subprocess.STDOUT, stdout=subprocess.PIPE
        ).communicate()[0].strip();
    

def windows_resolve_path(executable):
    if os.path.sep in executable:
        raise ValueError("Invalid executable name: %s" % executable)

    path = os.environ.get("PATH", "").split(os.pathsep)
    # PATHEXTS tells us which extensions an executable may have
    path_exts = os.environ.get("PATHEXTS", ".exe;.bat;.cmd").split(";")
    has_ext = os.path.splitext(executable)[1] in path_exts
    if not has_ext:
        exts = path_exts
    else:
        # Don't try to append any extensions
        exts = [""]

    for d in path:
        try:
            for ext in exts:
                exepath = os.path.join(d, executable + ext)
                if os.access(exepath, os.X_OK):
                    return exepath
        except OSError:
            pass

    return None



class PdfLatexError(Exception):
    def __init__(self, errmsg):
        super(PdfLatexError, self).__init__(errmsg)

class PrepError(Exception):
    def __init__(self, errmsg):
        super(PrepError, self).__init__(errmsg)



MODE_EX = 0
MODE_SOL = 1
MODE_TIPS = 2

rx_latex = re.compile(r'\.((la)?tex)$')


def run(texfile, pdflatexopts=[], mode=MODE_EX):

    # THIS IS IMPORTANT, as we build the name of the PDF based on this (via the name of the temp latex file)
    if (not rx_latex.search(texfile)):
        sys.stderr.write("Error: Expected a latex file (*.tex, *.latex): `%s'\n" % (texfile))
        raise PrepError("Expected a latex file (*.tex, *.latex): `%s'" %(texfile))

    # find pdflatex
    pdflatex = subprocess.Popen("which pdflatex", shell=True, stderr=subprocess.STDOUT,
                                stdout=subprocess.PIPE).communicate()[0].strip();

    if (not pdflatex):
        print >>sys.stderr, "Can't find pdflatex!";
        exit(255);

    runtexfile = None;

    workdir = tempfile.mkdtemp();

    if mode == MODE_EX:
        fnsuffix = 'ex'
        wantlatex = r'exercisesheet'
    elif mode == MODE_SOL:
        fnsuffix = 'sol'
        wantlatex = r'solutions'
    elif mode == MODE_TIPS:
        fnsuffix = 'tips'
        wantlatex = r'tipssheet'
    else:
        raise ValueError("Invalid mode: %r" %(mode))

    runtexfile = os.path.join(workdir, rx_latex.sub(r'_' + fnsuffix + r'.\1', texfile))
    try:
        f = open(runtexfile, 'w');
        f.write(r'\def\ethuebungwant' + wantlatex + r'{}\input{'+texfile+'}' +'\n');
        f.close();
    except:
        print >>sys.stderr, "Can't open file %s." % (runtexfile)
        raise PrepError("Can't write to file %s" %(runtexfile))
    
    (runtexfile_dir, runtexfile_bn) = os.path.split(runtexfile)

    cmd = [pdflatex];
    cmd += pdflatexopts;
    cmd += [runtexfile_bn];

    orig_dirs = runtexfile_dir + ":" + os.path.dirname(os.path.realpath(texfile))

    e = dict(os.environ)
    e['TEXINPUTS'] = orig_dirs+":"+(e['TEXINPUTS'] if 'TEXINPUTS' in e else '')
    e['BIBINPUTS'] = orig_dirs+":"+(e['BIBINPUTS'] if 'BIBINPUTS' in e else '')

    #print "runtexfile=%r (runtexfile_dir=%s, runtexfile_bn=%s);\ne=%r\n" %(
    #    runtexfile, runtexfile_dir, runtexfile_bn, e
    #    )
    #print "cmd=%r" %(cmd)


    def finished(code, noraise=False):
        if (not finished._cleaned_up):
            #for f in os.listdir(workdir):
            #    os.remove(os.path.join(workdir, f))
            #os.rmdir(workdir)
            if workdir and os.path.isdir(workdir):
                shutil.rmtree(workdir)
            finished._cleaned_up = True

        if not noraise:
            if (code < 0):
                sys.stderr.write("Child terminated by signal %d" %(-code));
                raise PdfLatexError("pdflatex terminated by signal %d" %(-code));
            elif code > 0:
                raise PdfLatexError("pdflatex exited with error code %d" %(code));

    #
    # "Static" variable for our function finished()
    finished._cleaned_up = False


    #
    # Run pdflatex up to three times
    #
    try:
        code = 0;
        for n in xrange(3):
            # run pdflatex
            code = subprocess.call(cmd, env=e);
            if (code != 0):
                finished(code);

        finished(0)
    except PdfLatexError:
        raise
    except KeyboardInterrupt:
        raise
    except:
        import traceback;
        sys.stderr.write("EXCEPTION:\n%s" %(traceback.format_exc()));
        finished(255, noraise=True)



if __name__ == "__main__":


    parser = argparse.ArgumentParser(description='Utility to run pdflatex on ethuebung sheets')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--exercisesheet', dest='mode', action='store_const', const=MODE_EX, default=MODE_EX,
                        help='Generate regular exercise sheet (the default)')
    group.add_argument('--solutionssheet', dest='mode', action='store_const', const=MODE_SOL,
                        help='Generate solutions sheet')
    group.add_argument('--tipssheet', dest='mode', action='store_const', const=MODE_TIPS,
                        help='Generate tips sheet')

    parser.add_argument('texfile', nargs=1,
                        help='The LaTeX file name')
    parser.add_argument('pdflatexopts', nargs=argparse.REMAINDER,
                        help='Additional options for pdflatex')

    args = parser.parse_args()
    texfile = args.texfile[0]

    print repr(args)

    run(texfile=texfile, pdflatexopts=args.pdflatexopts, mode=args.mode)

    
