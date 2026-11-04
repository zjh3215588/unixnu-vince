#!/usr/bin/env python3
"""Generate the minimal vince hardware Apple-format DT for the first boot.

Derived from scripts/make-nabu-adt.py (UniXNU framework) with Redmi 5 Plus
(MSM8953, Snapdragon 625) hardware facts:

  - 8x Cortex-A53, MPIDR Affinity1 0x000..0x700 (same numbering as SM8150)
  - GIC-400 (GICv2) at 0x0b000000: GICD 0x0b001000, GICC 0x0b002000,
    GICH 0x0b004000, GICV 0x0b006000 -- msm8953.dtsi intc@b000000.
    NOTE: xnu-10063 has no GICv2 interrupt driver; the node keeps the GICv3
    shape (dist + redist registers) with the GIC-400 windows so the first
    boot reaches the video console and reports the genuine missing-driver
    panic. Bring-up will replace this once the interrupt path is ported.
  - CPU timebase 19200000 Hz (Qualcomm architectural counter)
  - DRAM base 0x80000000; 3 GiB physical on the mainstream 3+32 config
  - Storage is eMMC (sdhci@7824900); the nabu UFS HC node is removed.

This is first-boot bring-up data: no Apple device identity beyond the
iPad-class /product that matches the IPSW root volume, and no property is
invented beyond these pinned sources.
"""
from pathlib import Path
import argparse
import os
import struct
import zlib

ROOT = Path(__file__).resolve().parents[1]

DRAM_BASE = 0x80000000
ARMIO_BASE = 0x0b000000          # MSM8953 peripheral block containing the GIC-400
GIC_DIST = 0x0b001000            # msm8953.dtsi intc@b000000: GICD
GIC_DIST_SIZE = 0x1000
GIC_REDIST = 0x0b006000          # GICV window used as the redist stand-in (GICv2 has none)
GIC_REDIST_SIZE = 0x2000
TIMEBASE = 19200000


def node(name, properties=(), children=()):
    properties = [('name', name.encode() + b'\0'), *properties]
    result = struct.pack('<II', len(properties), len(children))
    for key, data in properties:
        result += struct.pack('<32sI', key.encode(), len(data))
        result += data + bytes(-len(data) % 4)
    return result + b''.join(children)


def empty_nvram_proxy():
    """A fresh volatile CHRP bank for upstream IODTNVRAM, with no controller."""
    def header(name, size):
        raw = bytearray(struct.pack('<BBH12s', 0x70, 0, size // 16, name))
        checksum = sum(raw)
        while checksum > 255:
            checksum = (checksum & 255) + (checksum >> 8)
        raw[1] = checksum
        return raw

    image = bytearray(8192)
    image[:16] = header(b'nvram', 32)
    image[32:48] = header(b'common', 16 + 2048)
    free_at = 32 + 16 + 2048
    image[free_at:free_at + 16] = header(b'free', len(image) - free_at)
    struct.pack_into('<I', image, 16, zlib.adler32(image[20:]))
    return [('nvram-bank-size', struct.pack('<I', len(image))),
            ('nvram-bank-count', struct.pack('<I', 1)),
            ('nvram-current-bank', struct.pack('<I', 0)),
            ('nvram-proxy-data', bytes(image))]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path,
                        default=ROOT / 'build/vince/boot/kernel.macho.adt')
    parser.add_argument('--dram-size', type=lambda value: int(value, 0), required=True,
                        help='Actual observed DRAM size, e.g. 0xC0000000 for 3 GiB')
    parser.add_argument('--owned-memory-size', type=lambda value: int(value, 0), default=None,
                        help='Explicit DarwinBoot contiguous window request, 256 MiB..8 GiB in 2 MiB steps')
    parser.add_argument('--root-match-volume-uuid', default=None,
                        help='/chosen/root-matching: select the root by the UUID of an IOMedia')
    parser.add_argument('--unique-chip-id', type=lambda value: int(value, 16), default=None,
                        help='/chosen/unique-chip-id (8 bytes)')
    parser.add_argument('--chip-id', type=lambda value: int(value, 16), default=None)
    parser.add_argument('--ipad-identity', action='store_true',
                        help='/product and /buttons describe an iPad-class device without a Home button')
    parser.add_argument('--cpu-regs', default='0',
                        help='Comma-separated CPU MPIDR affinity values; MSM8953 numbers cores 0x000..0x700 in Affinity1')
    parser.add_argument('--psci-method', choices=['smc', 'hvc'], default='smc')
    parser.add_argument('--packed-data-ramdisk', action='store_true')
    parser.add_argument('--data-ramdisk', action='store_true')
    parser.add_argument('--trust-cache', action='store_true')
    parser.add_argument('--qemu', action='store_true',
                        help='qemu-virt flavour: arm-io window at the PL011 uart (0x09000000) and a uart0 DT node so the VMAPPLE_UART backend registers')
    args = parser.parse_args()
    if (args.unique_chip_id is None) != (args.chip_id is None):
        parser.error('--unique-chip-id and --chip-id must be supplied together')
    if args.unique_chip_id is not None and not (0 < args.unique_chip_id < 1 << 64 and 0 < args.chip_id < 1 << 32):
        parser.error('--unique-chip-id must fit 8 bytes and --chip-id 4 bytes, both nonzero')
    if args.owned_memory_size is not None and (
            not 0x10000000 <= args.owned_memory_size <= 0x200000000
            or args.owned_memory_size % 0x200000):
        parser.error('Owned memory must be 256 MiB to 8 GiB, aligned to 2 MiB')

    try:
        cpu_regs = [int(value, 0) for value in args.cpu_regs.split(',')]
    except ValueError:
        parser.error('--cpu-regs must be integers')
    if (not cpu_regs or cpu_regs[0] != 0 or len(set(cpu_regs)) != len(cpu_regs) or len(cpu_regs) > 8
            or any(reg < 0 or reg > 0xffff or reg & 0xff for reg in cpu_regs)):
        parser.error('--cpu-regs: up to eight distinct Affinity1-numbered cores, boot CPU 0 first')
    cpus = [node('cpu%d' % index, [('state', b'running\0' if index == 0 else b'waiting\0'),
                                   ('reg', struct.pack('<I', reg)),
                                   ('device_type', b'cpu\0'), ('compatible', b'arm,cortex-a53\0'),
                                   ('timebase-frequency', struct.pack('<I', TIMEBASE))])
            for index, reg in enumerate(cpu_regs)]
    # QEMU virt puts its PL011 at 0x09000000; pe_serial.c maps soc_base + reg.
    if args.qemu:
        io_base = 0x09000000
    else:
        io_base = ARMIO_BASE
    tree = node('device-tree', [
        ('model', b'iPad7,1\0' if args.ipad_identity else b'vince-first-boot\0'),
        *([('target-type', b'J120\0')] if args.ipad_identity else []),
        # Root compatible strings: vince board DT is xiaomi,vince / qcom,msm8953.
        ('compatible', b'xiaomi,vince\0qcom,msm8953\0'),
        ('#address-cells', struct.pack('<I', 2)),
        ('#size-cells', struct.pack('<I', 2)),
    ], [
        node('chosen', [('random-seed', os.urandom(64)),
                        *([('unique-chip-id', struct.pack('<Q', args.unique_chip_id)), ('chip-id', struct.pack('<I', args.chip_id))]
                          if args.unique_chip_id is not None else []),
                        # pe_kprintf.c defaults disable_kprintf_output to true and only
                        # clears it when -enable_kprintf_spam is present in boot-args.
                        # Without this property the kernel prints nothing at all and the
                        # boot log is invisible by design.
                        # maxmem caps xmaxmem in arm_init.c; 3072 MiB matches the 3 GiB
                        # mainstream config. amfi/cs flags match the nabu first-boot payload
                        # until the vince trust-cache path is qualified.
                        ('boot-args', b'-enable_kprintf_spam maxmem=3072 '
                            b'amfi_get_out_of_my_way=1 cs_enforcement_disable=1 '
                            b'amfi_allow_any_signature=1\0'),
                        ('osenvironment', b'main\0'),
                        *([('certificate-production-status', struct.pack('<I', 0)), ('effective-production-status-ap', struct.pack('<I', 0)),
                           ('certificate-security-mode', struct.pack('<I', 1)), ('effective-security-mode-sep', struct.pack('<I', 1))]
                          if args.ipad_identity else []),
                        *([('ephemeral-storage', struct.pack('<I', 1))] if (args.data_ramdisk or args.packed_data_ramdisk) else []),
                        *( [('darwinboot-memory-size', struct.pack('<Q', args.owned_memory_size))]
                           if args.owned_memory_size else [] ),
                        ('dram-base', struct.pack('<Q', DRAM_BASE)),
                        ('dram-size', struct.pack('<Q', args.dram_size)),
                        ('crypto-hash-method', b'sha2-384\0'),
                        *( [('root-matching', ('<dict><key>IOProviderClass</key><string>IOMedia</string>'
                                               '<key>IOPropertyMatch</key><dict><key>UUID</key><string>' +
                                               args.root_match_volume_uuid.upper() + '</string></dict></dict>\0').encode())]
                           if args.root_match_volume_uuid else [] ),
                        ('amfi-only-platform-code', struct.pack('<I', 1)),
                        *empty_nvram_proxy()],
             [node('memory-map', ([("PackedRAMDisk" if args.packed_data_ramdisk else "RAMDisk", bytes(16))] if (args.data_ramdisk or args.packed_data_ramdisk) else []) +
                                 ([('TrustCache', bytes(16))] if args.trust_cache else [])),
              node('manifestProperties')]),
        node('cpus', children=cpus),
        *([node('psci', [('compatible', b'arm,psci-1.0\0'), ('method', args.psci_method.encode() + b'\0')])] if len(cpus) > 1 else []),
        node('defaults', [('sleep-disabled', struct.pack('<I', 1))]),
        node('options', []),
        *( [node('buttons', [('compatible', b'buttons\0'), ('device_type', b'buttons\0'),
                             ('button-names', b'hold\0voldown\0volup\0'),
                             ('home-button-type', struct.pack('<I', 2))])] if args.ipad_identity else [] ),
        node('product', [('product-name', b'iPad Pro (12.9-inch) (2nd generation)\0' if args.ipad_identity else b'Redmi 5 Plus\0'),
                         ('model', b'xiaomi,vince\0'),
                         *( [('product-description', b'iPad Pro (12.9-inch) (2nd generation)\0'),
                             ('artwork-device-idiom', b'pad\0'),
                             ('artwork-device-subtype', struct.pack('<I', 2732)),
                             ('artwork-scale-factor', struct.pack('<I', 2)),
                             ('artwork-display-gamut', b'P3\0'),
                             ('compatible-device-fallback', b'iPad6,7\0'),
                             ('thin-bezel', struct.pack('<I', 1))] if args.ipad_identity else [] )]),
        node('arm-io', [('device_type', b'arm-io\0'),
                        ('#address-cells', struct.pack('<I', 2)),
                        ('#size-cells', struct.pack('<I', 2)),
                        ('ranges', struct.pack('<QQQ', 0, io_base, 0x08000000))],
             [node('intc', [('compatible', b'arm,gic-v3\0'),
                            ('interrupt-controller', b'master\0'),
                            ('reg', struct.pack('<4Q',
                                                GIC_DIST - io_base, GIC_DIST_SIZE,
                                                GIC_REDIST - io_base, GIC_REDIST_SIZE)),
                            ('redistributor-stride', struct.pack('<Q', 0x2000))]),
              # vince: pe_arm_map_interrupt_controller looks for device_type="timer".
              node('timer', [('device_type', b'timer\0'),
                             ('compatible', b'arm,armv8-timer\0'),
                             ('reg', struct.pack('<2Q', 0, 0x1000))]),
              # qemu: pe_serial.c VMAPPLE_UART backend looks for name="uart0"
              *([node('uart0', [('device_type', b'serial\0'),
                                ('reg', struct.pack('<2Q', 0, 0x1000))])] if args.qemu else []),
             ]),
    ])
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(tree)
    print(f'vince ADT: {len(tree)} bytes, dram {args.dram_size:#x}, timebase {TIMEBASE}')


if __name__ == '__main__':
    main()

