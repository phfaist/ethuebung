# -*- mode: python -*-

import sys
import os
import os.path

ethuebung_path = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))

print "PATH IS: ", ethuebung_path

##
## set up our import paths well first of all for this same script.
##
#sys.path += [ethuebung_path + '/bin'];


a = Analysis(['guicompiler.py'],
             pathex=[
                 ethuebung_path + '/guicompiler',
                 ethuebung_path + '/bin',
                 ],
             hiddenimports=[
                 'pdflatexex',
                 # it seems pdflatexex modules are not detected...
                 'sys',
                 're',
                 'os',
                 'os.path',
                 'subprocess',
                 'tempfile',
                 'argparse',
                 'shutil',
                 'signal',
                 'traceback',
                 ],
             hookspath=None,
             runtime_hooks=None)

if (sys.platform.startswith('win')):
    # have this problem of 'File already installed but should not: pyconfig.h'
    # hack from http://stackoverflow.com/questions/19055089/
    for d in a.datas:
        if 'pyconfig' in d[0]:
            a.datas.remove(d)
            break


pyz = PYZ(a.pure)

if (sys.platform.startswith('darwin')):
    exe = EXE(pyz,
              a.scripts,
              exclude_binaries=True,
              name=os.path.join('dist', 'ethuebung_compiler'),
              debug=True,
              strip=None,
              upx=True,
              console=False,
              )
    coll = COLLECT(exe,
                   a.binaries,
                   a.zipfiles,
                   a.datas,
                   strip=None,
                   upx=True,
                   name=os.path.join('dist', 'ethuebung_compiler'),
                   )
    app = BUNDLE(coll,
                 name=os.path.join('dist', 'EthuebungCompiler.app'),
                 #icon='bibolamazi_icon.icns',
                 )
else:
    kwargs = {}
    if (sys.platform.startswith('win')):
        exename = os.path.join('dist', 'ethuebung_compiler.exe')
        #kwargs['icon'] = 'bibolamazi_icon.ico'
    else:
        exename = os.path.join('dist', 'ethuebung_compiler')
        
    exe = EXE(pyz,
              a.scripts,
              a.binaries,
              a.zipfiles,
              a.datas,
              name=exename,
              debug=False,
              strip=None,
              upx=True,
              console=False,
              **kwargs
              )
