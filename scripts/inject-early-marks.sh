#!/bin/bash
# 鎶婃棭鏈熸鏌ョ偣鏍囪娉ㄥ叆 XNU 婧愮爜鏍戯紙浠呯敤浜庤瘖鏂瀯寤猴級
# 鐢ㄦ硶: bash inject-early-marks.sh <xnu-source-root>
set -e
X="${1:?xnu source root}"

echo "[1/4] copy marker sources"
cp "$(dirname "$0")/../kits/vince/vince_early_mark.c" "$X/osfmk/arm/vince_early_mark.c"
cp "$(dirname "$0")/../kits/vince/vince_early_mark.h" "$X/osfmk/arm/vince_early_mark.h"

echo "[2/4] register in conf/files.arm64"
python3 - "$X" <<'PY'
import io,sys
x=sys.argv[1]
p=x+'/osfmk/conf/files.arm64'
s=io.open(p,encoding='utf-8').read()
if 'vince_early_mark' not in s:
    a='osfmk/arm/arm_init.c\toptional config_pmap_ppl'
    assert a in s, 'anchor missing in files.arm64'
    s=s.replace(a, a+'\nosfmk/arm/vince_early_mark.c\tstandard', 1)
    io.open(p,'w',encoding='utf-8',newline='').write(s)
    print('  registered')
else:
    print('  already')
PY

echo "[3/4] insert marks into arm_init.c"
python3 - "$X" <<'PY'
import io,sys
x=sys.argv[1]
p=x+'/osfmk/arm/arm_init.c'
s=io.open(p,encoding='utf-8').read()

if '#include <arm/vince_early_mark.h>' not in s:
    a='#include <pexpert/arm/consistent_debug.h>'
    assert a in s, 'include anchor missing'
    s=s.replace(a, a+'\n#include <arm/vince_early_mark.h>', 1)

if 'vince_MARK(1)' not in s:
    a1='\tPE_init_platform(FALSE, args); /* Get platform expert set up */'
    assert a1 in s, 'mark1 anchor missing'
    s=s.replace(a1,
        '\tvince_mark_init((const unsigned long *)&args->Video);\n'
        '\tvince_MARK(1);\n'+a1, 1)

if 'vince_MARK(2)' not in s:
    a2='\tPE_create_console();'
    assert a2 in s, 'mark2 anchor missing'
    s=s.replace(a2, '\tvince_MARK(2);\n'+a2+'\n\tvince_MARK(3);', 1)

if 'vince_MARK(4)' not in s:
    a3='\t\tPE_init_platform(TRUE, &BootCpuData);'
    assert a3 in s, 'mark4 anchor missing'
    s=s.replace(a3, a3+'\n\t\tvince_MARK(4);', 1)

io.open(p,'w',encoding='utf-8',newline='').write(s)
print('  marks inserted')
PY

echo "[4/4] verify"
grep -n "vince_MARK" "$X/osfmk/arm/arm_init.c" | head -4
echo "inject done"

