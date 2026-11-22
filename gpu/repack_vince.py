#!/usr/bin/env python3
"""Repack a vince boot image with the original ADT, a new kernel and a new cmdline.
Usage: python3 repack_vince.py SRC.img KERNEL OUT.img --cmdline "..."
"""
import argparse, hashlib, os, struct, sys, tempfile

REPO = '/root/ref/ios-rebivincek'
sys.path.insert(0, os.path.join(REPO, 'tools'))
import mkpayload  # noqa: E402

PAGE = 2048


def pad(b):
    return b + b'\0' * (-len(b) % PAGE)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('src')
    ap.add_argument('kernel')
    ap.add_argument('out')
    ap.add_argument('--cmdline', required=True)
    ap.add_argument('--adt-out')
    a = ap.parse_args()

    img = open(a.src, 'rb').read()
    assert img[:8] == b'ANDROID!'
    (kernel_size, kernel_addr, ramdisk_size, ramdisk_addr, second_size, second_addr,
     tags_addr, page_size, header_version, os_version) = struct.unpack_from('<10I', img, 8)
    assert page_size == PAGE and header_version == 0
    kz = img[PAGE:PAGE + kernel_size]
    payload_off = PAGE + ((kernel_size + PAGE - 1) // PAGE) * PAGE
    payload = img[payload_off:payload_off + ramdisk_size]
    assert payload[:8] == b'SWEETXNU', payload[:8]

    adt_off, adt_size = struct.unpack_from('<QQ', payload, 0x20)
    adt = payload[adt_off:adt_off + adt_size]
    if a.adt_out:
        open(a.adt_out, 'wb').write(adt)
    old_cmdline = payload[0x48:0x48 + 608].split(b'\0', 1)[0].decode()
    print('src payload', len(payload), 'ADT', adt_off, adt_size, 'old cmdline', old_cmdline)

    new_payload, info = mkpayload.build(a.kernel, a.adt_out or _write_temp(adt), a.cmdline)
    print('new payload', len(new_payload), 'virt_base', info['virt_base'], 'entry', info['entry'])

    hdr = bytearray(1632)
    hdr[:8] = b'ANDROID!'
    struct.pack_into('<10I', hdr, 8, kernel_size, kernel_addr, len(new_payload), ramdisk_addr,
                     second_size, second_addr, tags_addr, PAGE, 0, os_version)
    hdr[48:64] = b'vince-m3b'.ljust(16, b'\0')
    cl = a.cmdline.encode()[:511]
    hdr[64:64 + len(cl)] = cl
    sha = hashlib.sha1()
    for blob in (kz, new_payload, b''):
        sha.update(blob)
        sha.update(struct.pack('<I', len(blob)))
    hdr[576:608] = sha.digest().ljust(32, b'\0')

    out = bytearray()
    out += hdr + b'\0' * (PAGE - len(hdr))
    out += pad(kz)
    out += pad(new_payload)
    open(a.out, 'wb').write(out)
    print('wrote', a.out, len(out), 'sha256', hashlib.sha256(out).hexdigest())


def _write_temp(adt):
    fd, path = tempfile.mkstemp(suffix='.adt')
    os.write(fd, adt)
    os.close(fd)
    return path


if __name__ == '__main__':
    main()
