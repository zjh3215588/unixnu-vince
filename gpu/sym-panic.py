import struct, sys, bisect
path = sys.argv[1]
targets = [int(x, 16) for x in sys.argv[2:]]
d = open(path, 'rb').read()
magic = struct.unpack_from('<I', d, 0)[0]
if magic != 0xfeedfacf:
    print('not macho64', hex(magic)); sys.exit(1)
ncmds = struct.unpack_from('<I', d, 16)[0]
off = 32
syms = []
for _ in range(ncmds):
    cmd, cmdsize = struct.unpack_from('<II', d, off)
    if cmd == 0x2:
        symoff, nsyms, stroff, strsize = struct.unpack_from('<IIII', d, off + 8)
        for i in range(nsyms):
            so = symoff + i * 16
            n_strx, n_type, n_sect, n_desc, n_value = struct.unpack_from('<IBBHQ', d, so)
            if n_value and (n_type & 0x0e) == 0x0e:
                end = d.index(b'\0', stroff + n_strx)
                name = d[stroff + n_strx:end].decode(errors='replace')
                syms.append((n_value, name))
    off += cmdsize
syms.sort()
vals = [s[0] for s in syms]
print('nsyms', len(syms))
for t in targets:
    i = bisect.bisect_right(vals, t) - 1
    if i >= 0:
        v, n = syms[i]
        print(hex(t), '->', n, '+', hex(t - v))
    else:
        print(hex(t), 'no symbol')
