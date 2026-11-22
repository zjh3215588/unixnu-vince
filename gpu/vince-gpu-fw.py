#!/usr/bin/env python3
"""
vince-gpu-fw.py - put the Adreno 506 firmware from YOUR phone into a built kernel.

The firmware is Qualcomm's and is not in the repository. The kernel (patch 0982)
carries an empty slot; this script fills it. Run it on the kernel file from the
build, BEFORE vince_pack.py:

    python3 vince-gpu-fw.py KERNEL FWDIR [-o OUT]

FWDIR is a folder with the files copied from the Android /vendor/firmware
(any subfolders are searched):
    a530_pm4.fw  a530_pfp.fw  a506_zap.mdt  a506_zap.b02

By default KERNEL is overwritten (a KERNEL.bak copy is made first).
Never commit the result, the firmware or the log of this script into the repo.
"""
import argparse, os, shutil, struct, sys

MARKER = b"VINCE-GPU-FW-v1\0"
FILLED = 0x46574742
LIMITS = {"mdt": 8192, "b02": 8192, "pm4": 24576, "pfp": 24576}
NAMES = {"pm4": "a530_pm4.fw", "pfp": "a530_pfp.fw",
         "mdt": "a506_zap.mdt", "b02": "a506_zap.b02"}
# struct layout, see bsd/dev/vince_gpu_firmware.h
HDR = 16 + 4 + 4 * 4 + 3 * 4          # marker, filled, 4 sizes, pad[3]
OFF = {"mdt": HDR}
OFF["b02"] = OFF["mdt"] + LIMITS["mdt"]
OFF["pm4"] = OFF["b02"] + LIMITS["b02"]
OFF["pfp"] = OFF["pm4"] + LIMITS["pm4"]
TOTAL = OFF["pfp"] + LIMITS["pfp"]


def find(root, name):
    for d, _, fs in os.walk(root):
        if name in fs:
            return os.path.join(d, name)
    sys.exit("missing %s in %s" % (name, root))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("kernel")
    ap.add_argument("fwdir")
    ap.add_argument("-o", "--out")
    a = ap.parse_args()

    data = bytearray(open(a.kernel, "rb").read())
    pos = data.find(MARKER)
    if pos < 0:
        sys.exit("slot marker not found: kernel is built without patch 0982, or it is compressed/wrapped")
    if data.find(MARKER, pos + 1) >= 0:
        sys.exit("slot marker found twice, refusing")
    if pos + TOTAL > len(data):
        sys.exit("slot runs past the end of the file")

    blobs = {}
    for k, n in NAMES.items():
        b = open(find(a.fwdir, n), "rb").read()
        if not 4 < len(b) <= LIMITS[k]:
            sys.exit("%s: %d bytes, allowed 5..%d" % (n, len(b), LIMITS[k]))
        blobs[k] = b
    if blobs["mdt"][:4] != b"\x7fELF":
        sys.exit("a506_zap.mdt is not an ELF file")

    struct.pack_into("<I4I", data, pos + 16, FILLED, len(blobs["mdt"]),
                     len(blobs["b02"]), len(blobs["pm4"]), len(blobs["pfp"]))
    for k, b in blobs.items():
        o = pos + OFF[k]
        data[o:o + LIMITS[k]] = b + bytes(LIMITS[k] - len(b))

    out = a.out or a.kernel
    if out == a.kernel:
        shutil.copyfile(a.kernel, a.kernel + ".bak")
    open(out, "wb").write(data)
    print("slot at file offset %#x filled: mdt %d, b02 %d, pm4 %d, pfp %d bytes -> %s"
          % (pos, len(blobs["mdt"]), len(blobs["b02"]), len(blobs["pm4"]), len(blobs["pfp"]), out))


main()
