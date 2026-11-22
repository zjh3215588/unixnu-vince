#!/usr/bin/env python3
"""Put the GPU window server (topaz) into the iOS root.

  sudo python3 vince-topaz-install.py ROOT OUTDIR     # ROOT = mounted iOS root; OUTDIR = unpacked artifact "topaz-ios"
  sudo python3 vince-topaz-install.py ROOT --undo     # back to the stock backboardd

(libOSMesa.8.dylib of the "mesa-ios" artifact must already be in ROOT/topaz/lib: vince-gputest-install.py puts it there.)
What it does:
  ROOT/topaz/lib/libtopaz-gl.dylib, libtopaz-inject.dylib
  ROOT/usr/libexec/real/backboardd      the stock backboardd, moved here (kept untouched)
  ROOT/usr/libexec/backboardd           the wrapper: sets DYLD_INSERT_LIBRARIES and execs the real one
Without the GPU service (no adreno=11) or with gl=0 in the boot-args the loader does nothing: the window server
draws as before. The kernel boot log shows "topaz-gl:" / "redwood-gl:" lines.
"""
import os, shutil, sys

BB = 'usr/libexec/backboardd'
REAL = 'usr/libexec/real/backboardd'
LIBS = ('libtopaz-gl.dylib', 'libtopaz-inject.dylib')


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    undo = '--undo' in sys.argv
    if not args or not os.path.isfile(os.path.join(args[0], BB)) or (not undo and len(args) != 2):
        sys.exit(__doc__)
    root = args[0]
    bb, real = os.path.join(root, BB), os.path.join(root, REAL)
    if undo:
        if os.path.isfile(real):
            shutil.move(real, bb)
            print('stock backboardd back')
        for n in LIBS:
            p = os.path.join(root, 'topaz/lib', n)
            if os.path.exists(p):
                os.remove(p)
        return
    out = args[1]
    for n in LIBS + ('backboardd-wrap',):
        if not os.path.isfile(os.path.join(out, n)):
            sys.exit('missing %s' % os.path.join(out, n))
    if not os.path.isfile(os.path.join(root, 'topaz/lib/libOSMesa.8.dylib')):
        sys.exit('no ROOT/topaz/lib/libOSMesa.8.dylib: run vince-gputest-install.py first')
    if not os.path.isfile(real):
        os.makedirs(os.path.dirname(real), exist_ok=True)
        shutil.move(bb, real)      # the stock one, only the first time
    for n in LIBS:
        dst = os.path.join(root, 'topaz/lib', n)
        shutil.copyfile(os.path.join(out, n), dst)
        os.chmod(dst, 0o755)
        os.chown(dst, 0, 0)
    shutil.copyfile(os.path.join(out, 'backboardd-wrap'), bb)
    os.chmod(bb, 0o755)
    os.chown(bb, 0, 0)
    print('done: wrapper in %s, stock backboardd in %s' % (BB, REAL))


main()
