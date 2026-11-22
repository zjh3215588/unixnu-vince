#!/usr/bin/env python3
"""Put the GPU test (gputest + libOSMesa) into the iOS root and start it at boot.

  sudo python3 vince-gputest-install.py ROOT OUTDIR     # ROOT = the mounted iOS root (has System/Library/xpc)
  sudo python3 vince-gputest-install.py ROOT --undo     # take it out again

OUTDIR is the unpacked artifact "mesa-ios" of the GitHub workflow (libOSMesa.8.dylib and gputest in it).
What it does:
  ROOT/topaz/lib/libOSMesa.8.dylib      Mesa with freedreno (the library gputest links to)
  ROOT/usr/local/bin/vince-gputest      the test
  ROOT/System/Library/xpc/launchd.plist one job added, com.vince.gputest, RunAtLoad, output to /dev/console
                                        (a copy of the plist is kept as launchd.plist.vince-orig)
The test runs at every boot, but only does anything useful with adreno=11 in the boot-args (without the GPU
Mesa falls back to software, and the test says so). Its lines start with "gputest:" in the boot log.
"""
import os, plistlib, shutil, sys

LABEL = 'com.vince.gputest'
LIB = 'topaz/lib/libOSMesa.8.dylib'
BIN = 'usr/local/bin/vince-gputest'
PLIST = 'System/Library/xpc/launchd.plist'


def chown_root(path):
    try:
        os.chown(path, 0, 0)
    except PermissionError:
        print('warning: not root, owner of %s not set' % path)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    undo = '--undo' in sys.argv
    if not args or not os.path.isdir(os.path.join(args[0], 'System/Library/xpc')) or (not undo and len(args) != 2):
        sys.exit(__doc__)
    root = args[0]
    plist_path = os.path.join(root, PLIST)
    st = os.stat(plist_path)
    with open(plist_path, 'rb') as f:
        plist = plistlib.load(f)
    jobs = plist['LaunchDaemons']
    for key in [k for k, j in jobs.items() if j.get('Label') == LABEL]:
        del jobs[key]

    if undo:
        for rel in (BIN, LIB):
            if os.path.exists(os.path.join(root, rel)):
                os.remove(os.path.join(root, rel))
        print('removed the job and the files')
    else:
        out = args[1]
        for name, rel in (('libOSMesa.8.dylib', LIB), ('gputest', BIN)):
            src = os.path.join(out, name)
            if not os.path.isfile(src):
                sys.exit('missing %s' % src)
            dst = os.path.join(root, rel)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copyfile(src, dst)
            os.chmod(dst, 0o755)
            chown_root(dst)
        jobs['/System/Library/LaunchDaemons/%s.plist' % LABEL] = {
            'Label': LABEL,
            'ProgramArguments': ['/' + BIN],
            'RunAtLoad': True,
            'KeepAlive': False,
            'StandardOutPath': '/dev/console',
            'StandardErrorPath': '/dev/console',
            # the first run was killed by jetsam (per-process memory limit) while Mesa compiled the shader
            'JetsamProperties': {'JetsamMemoryLimit': 1024},
            'EnablePressuredExit': False,
            'EnableTransactions': False,
        }
        print('installed %s and %s, job %s' % (LIB, BIN, LABEL))

    backup = plist_path + '.vince-orig'
    if not os.path.exists(backup):
        shutil.copyfile(plist_path, backup)
    with open(plist_path, 'wb') as f:
        plistlib.dump(plist, f, fmt=plistlib.FMT_BINARY)
    os.chmod(plist_path, st.st_mode & 0o7777)
    os.chown(plist_path, st.st_uid, st.st_gid) if os.geteuid() == 0 else None


main()
