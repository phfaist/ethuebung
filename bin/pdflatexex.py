#!/usr/bin/env python

import sys
import re
import os
import os.path
import subprocess
import tempfile
import argparse
import shutil
import signal




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

# regex to capture the `.latex` or `.tex` ending in file names
rx_latex = re.compile(r'\.((la)?tex)$')

def defaultsuffix(mode):
    return {
        MODE_EX: 'ex',
        MODE_SOL: 'sol',
        MODE_TIPS: 'tips',
        }[mode]
    


def run(texfile, pdflatexopts=[], mode=MODE_EX, pdfbasename=None, pdflatex=None,
        close_stdin=False, capture_output=None):

    # THIS IS IMPORTANT, as we build the name of the PDF based on this (via the name of the temp latex file)
    if (not rx_latex.search(texfile)):
        sys.stderr.write("Error: Expected a latex file (*.tex, *.latex): `%s'\n" % (texfile))
        raise PrepError("Expected a latex file (*.tex, *.latex): `%s'" %(texfile))

    # find pdflatex
    if not pdflatex:
        pdflatex = resolve_path('pdflatex')

    (pdflatex_dir, pdflatex_bn) = os.path.split(pdflatex)

    if (not pdflatex):
        sys.stderr.write("Can't find pdflatex!\n");
        raise PrepError("Can't find pdflatex!")

    runtexfile = None;

    (texfile_dir,texfile_bn) = os.path.split(texfile)
    if not texfile_dir:
        texfile_dir = None # None, by default (meaning CWD)

    workdir = tempfile.mkdtemp();

    fnsuffix = defaultsuffix(mode)
    if mode == MODE_EX:
        wantlatex = r'exercisesheet'
    elif mode == MODE_SOL:
        wantlatex = r'solutions'
    elif mode == MODE_TIPS:
        wantlatex = r'tipssheet'
    else:
        raise ValueError("Invalid mode: %r" %(mode))

    if pdfbasename:
        runtexfile = os.path.join(workdir, pdfbasename + '.tex')
    else:
        runtexfile = os.path.join(workdir, rx_latex.sub(r'_' + fnsuffix + r'.\1', texfile_bn))

    try:
        f = open(runtexfile, 'w');
        f.write(r'\def\ethuebungwant' + wantlatex + r'{}\input{'+texfile_bn+'}' +'\n');
        f.close();
    except:
        print >>sys.stderr, "Can't open file %s." % (runtexfile)
        raise PrepError("Can't write to file %s" %(runtexfile))
    
    (runtexfile_dir, runtexfile_bn) = os.path.split(runtexfile)

    cmd = [pdflatex];
    cmd += pdflatexopts;
    cmd += [runtexfile];

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
                sys.stderr.write("Child %s terminated by signal %d" %(pdflatex_bn, -code));
                raise PdfLatexError("%s terminated by signal %d" %(pdflatex_bn, -code));
            elif code > 0:
                raise PdfLatexError("%s exited with error code %d" %(pdflatex_bn, code));

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
            this_stdin = (subprocess.PIPE if close_stdin else None)
            this_stdout = (subprocess.PIPE if capture_output else None)
            this_stderr = (subprocess.STDOUT if capture_output else None)
            
            p = subprocess.Popen(cmd, env=e, cwd=texfile_dir,
                                 # see http://bugs.python.org/issue1652 :
                                 preexec_fn=preexec_fn_setup_pipe_sig,
                                 # pipes:
                                 stdin=this_stdin, stdout=this_stdout, stderr=this_stderr);
            if close_stdin:
                # no stdin
                p.stdin.close()
            
            if capture_output is not None:

                capture_output('\n========== %s run #%d ==========\n\n'%(pdflatex_bn, 1+n))
                
                # capture output
                while p.poll() is None:
                    line = p.stdout.readline()
                    capture_output(line)

                # capture the rest of stdout, if something is left
                rest = p.stdout.read()
                if rest:
                    for line in rest.split('\n'):
                        capture_output(line)

            else:
                p.wait()
            
            code = p.returncode
            
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
        finished(999999, noraise=True)


def preexec_fn_setup_pipe_sig():
    try:
        # see http://bugs.python.org/issue1652
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    except ValueError:
        # on Windows, there is no SIGPIPE
        pass
    


if __name__ == "__main__":


    parser = argparse.ArgumentParser(description='Utility to run pdflatex on ethuebung sheets')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--exercisesheet', dest='mode', action='store_const', const=MODE_EX, default=MODE_EX,
                        help='Generate regular exercise sheet (the default)')
    group.add_argument('--solutionssheet', dest='mode', action='store_const', const=MODE_SOL,
                        help='Generate solutions sheet')
    group.add_argument('--tipssheet', dest='mode', action='store_const', const=MODE_TIPS,
                        help='Generate tips sheet')

    parser.add_argument('--pdfbasename', dest='pdfbasename', action='store', default=None,
                        help='The base name of the generated PDF file. This overrides the default '
                        'behavior of adding the suffix "ex", "sol" or "tips".')

    parser.add_argument('--pdflatex', dest='pdflatex', action='store', default=None,
                        help='The pdflatex executable to call. By default, it is search for in '
                        '$PATH. You may set this to the `latex\' executable if you prefer to '
                        'generate DVI output.')

    parser.add_argument('texfile', nargs=1,
                        help='The LaTeX file name')
    parser.add_argument('pdflatexopts', nargs=argparse.REMAINDER,
                        help='Additional options for pdflatex')

    args = parser.parse_args()
    texfile = args.texfile[0]

    print repr(args)

    run(texfile=texfile, pdflatexopts=args.pdflatexopts, mode=args.mode, pdfbasename=args.pdfbasename,
        pdflatex=args.pdflatex)

    
