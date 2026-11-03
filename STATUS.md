# 鐘舵€佸揩鐓?
> 鏈満鏄?**鎵╁鐗?vince**锛氱墿鐞?DRAM **12 GiB**锛屽疄娴嬭嚜 TWRP 鐨?`/proc/meminfo`
> 锛坄MemTotal = 11766512 kB`锛屽嵆 12 GiB 鍑忓幓绾?816 MB 缁?modem/hyp/rmtfs锛夈€?> 鍥犳 `dram_size = 0x300000000`銆乣owned_memory_size = 0x130000000` 鏄?*涓鸿繖鍙版満鍣ㄦ祴鍑烘潵鐨勫€?*锛?> 涓嶆槸鏍囧噯 6/8 GB 鏈哄瀷涓婄殑鏁板瓧銆傜収鎶勫叾浠栭」鐩殑 `0x180000000`锛? GiB锛変細璁?6 GiB 浠ヤ笂鐨?> 鐗╃悊鍐呭瓨瀵?Darwin 涓嶅彲瑙併€?
## 鐜扮姸锛?026-10-28锛屼互姝や负鍑嗭級

**鐢ㄦ埛鎬佸凡缁忚窇璧锋潵锛屼笉鍐嶅仠鍦?`errno 2`銆?*

| 椤?| 瀹炴祴 |
|---|---|
| 鏍瑰嵎 + launchd | 閫氳繃锛涘畬鏁村惎鍔ㄦ棩蹇?**146,042 B / 2,032 琛?*锛堜笌鑷姩澶嶄綅鍚屼竴杞彇寰楋級 |
| 瀹堟姢杩涚▼ | `[hb] tag=chk n=68 sb=1 bb=1 rb=1 cfg=1`锛況unningboardd / backboardd / SpringBoard 閮藉湪鍚勮嚜 mqueue 涓婄瓑娑堟伅 |
| keybagd | `DEVICE HAS EPHEMERAL DATA VOLUME, SKIP INIT` + `[ex] pid=11 comm=keybagd rv=0x0` |
| 鏄剧ず | `[nm] mask=7 size=1336 init=1 rel=0`锛涜繍琛屾湡鍞竴鏄剧ず鐩稿叧澶辫触 `[ex] pid=26 comm=IOMFB_FDR_Loader rv=0x100 sig=0 code=1` |
| 褰撳墠闃诲 | 缂轰竴涓?`IOMobileFramebuffer` 鐨?provider 瀹炰緥 |
| 姣忚疆鎴愭湰 | 86~129 s锛岄浂鎸夐敭锛圕DC 鎺у埗閫氶亾 + WDT 瀹氭椂鍋滆溅锛岃 `vince-usb-cdc` 鐨?`docs/07`锛?|

涓嬮潰浠庛€岄噷绋嬬锛氬唴鏍歌蛋鍒颁簡 launchd銆嶅紑濮嬬殑鍐呭鏄?**2026-10-23 ~ 10-25 鐨勫巻鍙叉祦姘?*锛?淇濈暀鐢ㄤ簬杩芥函锛涚粨璁猴紙鈥滅己涓€涓浜嗙郴缁熸枃浠剁殑鏍规枃浠剁郴缁熲€濓級**宸茶鍙栦唬**銆?
## 閲岀▼纰戯細鍐呮牳璧板埌浜?launchd

**灞忓箷璇佹嵁锛?026-10-23 鏅氾級**

```
Process 1 exec of /sbin/launchd failed, errno 2
/sbin/launchd
kern_exec.c

FAR=18446744042837921792
PC=18446744005117767160
LR=18446744005111703156
```

**鍐呮牳瀹屾暣璧板畬浜嗚繖鏉￠摼锛?*

```
bsd_autoconf()        鉁?  kminit()            鉁?    IOsurfaceRoot::installMemoryRegions()   鉁?  鈫?涔嬪墠浠ヤ负鍗″湪杩欓噷锛屽叾瀹炴病鏈?bsd_init 鍚庡崐娈?      鉁?  vfs_mountroot()     鉁?  load_init_program() 鉁?  鈫?瑙ｆ瀽鍑?/sbin/launchd
    execve("/sbin/launchd")   鉂? errno 2 (ENOENT)
```

**`errno 2` 鏄枃浠朵笉瀛樺湪 鈥斺€?涓嶆槸鍐呮牳闂锛屾槸鏍规枃浠剁郴缁熼噷娌℃湁閭ｄ釜鏂囦欢銆?*

### 杩欐帹缈讳簡涓夊ぉ鏉ョ殑鍒ゆ柇

`IOsurfaceRoot::installMemoryRegions()` 閭ｄ竴琛?*浠庢潵涓嶆槸缁堢偣**锛屽畠鍙槸鏈€鍚庝竴鏉?kprintf銆?瀹冧箣鍚庣揣鎺ョ殑 `dtrace_postinit()`銆乣inittodr()` 鍜屾潯浠剁紪璇戠殑缃戠粶鍒濆鍖栭兘涓嶆墦鏃ュ織锛屾墍浠?銆屾棩蹇楀仠姝€嶈褰撴垚浜嗐€屽唴鏍稿仠姝€嶃€?
鐪熸涓€鐩寸己鐨勬槸**涓€涓湡姝ｇ殑鏍?*锛屼笉鏄嚜鐮?surface銆?
## 鏈湴 Linux 鏋勫缓鎵撻€氾紙鎻愰€?12 鍊嶏級

| 椤?| GitHub macOS runner | 鏈湴 WSL Ubuntu |
|---|---|---|
| 鍗曡疆鏋勫缓 | 15鈥?7 鍒嗛挓 | **72 绉?* |
| 浜х墿 | 49.2 MB | **49 MB** |
| 鍙鐜?| 鍙兘闈?CI | 鏈満闅忔椂璺?|

楠岃瘉锛?
```
file            Mach-O 64-bit arm64 executable, flags:<NOUNDEFS|PIE>
__TEXT vmaddr   0xfffffff007004000      鈫?涓庡師鐗?kernelcache 涓€鑷?symbols         22708
vince 鎺㈤拡       vince_mark / vince_mark_map / vince_mark_num / vince_mark_putc
UFS 鎺㈡祴        vince_ufs_register_probe.cpp
sha256          c756ecdb88a9dd50156dc27d2cdf48a08ddf93fcf204040fa57804f814fc3c15
```

**宸ュ叿閾?*锛歚Allenwdk/xnu-linux-toolchain`锛圲buntu 24.04 / clang 18 / 12 鏍革級

## 涓€璺笂瑙ｅ喅鐨?18 涓棶棰?
```
 1  libdispatch 鏃?Ubuntu 鍖?         鈫?婧愮爜缂栬瘧 + 鎵嬪啓 .pc
 2  toolchain/csh 鏄鍙烽摼鎺?         鈫?cp -L
 3  xcrun 纭紪鐮?/usr/bin/xcrun       鈫?杞摼
 4  sysctl 纭紪鐮?/usr/sbin/sysctl    鈫?Darwin shim 鏇挎崲
 5  /bin/sh 鏄?dash                   鈫?鎸囧悜 bash
 6  bison/flex/m4 鍦?/usr/sbin        鈫?杞摼
 7  hostcompat.h 涓嶅瓨鍦?              鈫?鑷啓
 8  libc.h 涓嶅瓨鍦?                    鈫?鑷啓锛圤SAtomic / 椤靛榻愶級
 9  copyfile.h / fcopyfile            鈫?鑷啓
10  setmode/getmode                   鈫?鑷啓锛坵ho 浣嶇Щ + mask 淇锛?11  TargetConditionals.h              鈫?鑷啓锛屼笖鍙斁涓ゅ
12  sys/_types/_os_inline.h           鈫?鑷啓骞堕暅鍍忓埌 compat 鏍?13  mach/mach_init.h                  鈫?鑷啓
14  -Wno-* 涓嶈璇?                    鈫?-Wno-unknown-warning-option
15  macOS clang 26 璇婃柇鍚?            鈫?CCC_OVERRIDE_OPTIONS 閫愭潯闄嶇骇
16  sed -i '' 鏄?BSD 璇硶             鈫?鍒嗘敮澶勭悊锛屼笖鍙湪 Darwin 璺?17  awk \( 鍦?GNU 淇濈暀鍙嶆枩鏉?         鈫?鍋氭垚 patch锛坺zzz-vince-awk-parens锛?18  mockfs 鍙岄噸閾炬帴锛?3 涓噸澶嶇鍙凤級  鈫?鍘绘帀 force_load
```


## 缁?`.cache/xnu-work` 閲岀殑鏂囦欢鎵撹ˉ涓侊細鍏釜蹇呰俯鐨勫潙

`unixnu tree` 姣忔閮芥妸 `.cache/xnu-work` reset 鍒?`d8b8029` 鍐嶆寜鏂囦欢鍚嶉『搴忓簲鐢?`patches/xnu/*.patch`锛屾墍浠?*鎵嬪伐鏀瑰伐浣滄爲涓€瀹氫細琚鐩?*锛屽繀椤诲仛鎴?patch銆傝€?patch 鏈韩鏈夊叚涓潙锛?杩欐鍏ㄨ俯浜嗕竴閬嶏細

| 鍧?| 鐥囩姸 | 姝ｈВ |
|---|---|---|
| 姣忎釜 hunk 閮藉甫涓€瀵?`--- / +++` | `git apply` 褰撴垚澶氫釜鏂囦欢锛岃緭鍑哄娆?`Checking patch` | **涓€涓枃浠跺ご锛宧unk 鍫嗗彔** |
| 绌鸿涓婁笅鏂囧啓鎴愮湡绌鸿 | `patch` 鎶?`fuzz`锛宍git apply` 鐩存帴鎷掔粷 | **` ` + 鎹㈣**锛堜竴涓┖鏍硷級|
| hunk 鍙湁 2 琛屼笂涓嬫枃 | `git apply` 榛樿涓?fuzz | **鑷冲皯 3 琛?*锛屽疄璺典腑缁?6鈥?2 琛?|
| 琛屽彿鎸夊共鍑€妫€鍑虹殑鏂囦欢绠?| `failed at 801` / `924` | **閲忋€屽墠闈㈡墍鏈?patch 搴旂敤鍚庛€嶇殑浣嶇疆** |
| 璧风偣鍋囪鏈夋敞閲婂潡 | `bsd_autoconf(void)` 涓婇潰骞舵病鏈?`/**` | 浠?`kern_return_t` 寮€濮?|
| 璺宠繃涓棿鏌愪釜 `#if` 鍧?| `#endif` 鍚庡叾瀹炶繕鏈?4 琛?`XNU_NATIVE_OFFLINE_GPU` | 涓婁笅鏂囨埅鍒?`#endif` 灏卞仠 |

### 鎬庝箞閲忕湡瀹炶鍙?
`unixnu tree` 澶辫触鏃讹紝`.cache` 姝ｅソ鍋滃湪銆屾墍鏈夊墠闈㈢殑 patch 宸插簲鐢ㄣ€佸綋鍓嶈繖涓湭搴旂敤銆嶇殑鐘舵€?鈥斺€?杩欏氨鏄閲忕殑鐩爣锛?
```python
import io
src = io.open('.cache/xnu-work/bsd/kern/bsd_init.c', encoding='utf-8').read().split('\n')
for needle in ('calling bsd_autoconf', 'bsd_autoconf(void)', 'kminit();'):
    print(needle, [i + 1 for i, l in enumerate(src) if needle in l][:5])
```

鏈瀹炴祴鍊硷紙鍓嶉潰 patch 鍏ㄩ儴搴旂敤鍚庯級锛?
```
' * Version 2.0.'         80
'#include <sys/param.h>'  83
calling sysctl_mib_init  912
calling bsd_autoconf     924
bsd_autoconf(void)      1291     鈫?323 鏄墠缃０鏄庯紝涓嶆槸瀹氫箟
kminit();               1294
```

### 楠岃瘉琛ヤ竵鑳藉簲鐢紝鍒潬鏋勫缓

```bash
cd .cache/xnu-work
git apply --check /path/to.patch && git apply /path/to.patch
grep -n 'vince:' bsd/kern/bsd_init.c
```

**娉ㄦ剰涓嶈鍏?`git checkout --` 閭ｄ釜鏂囦欢** 鈥斺€?閭ｄ細鎶婂畠杩樺師鎴?pristine锛岃鍙峰張鍙樺洖鍙︿竴濂椼€?

## `bsd_autoconf` 涔嬪悗涓轰粈涔堜竴鐗囬潤榛?
鍐呮牳鍦?`bsd_autoconf()` 杩斿洖鍚庣湅璧锋潵銆屽仠浣忋€嶏紝浣嗚繖涓棿姣忎竴绔欓兘鐢?`bsd_init_kprintf` 鎵撳嵃锛?鑰屽畠鍦ㄥ綋鍓嶉厤缃笅鏄?**no-op**銆傛墍浠ュ崱鍦?`dtrace_postinit`銆乣loopattach`銆乣ether_family_init`銆?`net_init_run`銆乣inittodr`銆乣vfs_mountroot` 涓殑浠讳綍涓€澶勶紝灞忓箷涓婄湅鍒扮殑閮藉拰鍗″湪涓婁竴琛屼竴妯′竴鏍枫€?
鐜板湪姣忎竴绔欓兘鐢ㄧ湡 `kprintf` + `vince_MARK` 鎷捣鏉ヤ簡锛?
```
vince: before kminit          61
vince: after kminit           62
vince: bsd_autoconf returned  65
vince: dtrace_postinit
vince: dtrace done            66
vince: loopattach             67
vince: loopattach done
vince: ether_family_init      68
vince: ether done
vince: net_init_run           69
vince: net done
vince: inittodr               70
vince: inittodr done
```

**鏈€鍚庝竴鏉″嚭鐜板湪灞忓箷涓婏紝灏辨槸鐪熸鐨勫崱鐐广€?* 缂栧嚭鏉ョ殑 `kernel.macho` 閲?13 鏉″瓧绗︿覆鍏ㄩ儴鍙煡锛?
```bash
strings out/vince/kernel/kernel.macho | grep '^vince: ' | sort -u
```

### 涓や釜鏇剧粡璇鍒ゆ柇鐨勫亣绾跨储

**`IOsurfaceRoot::installMemoryRegions()` 涓嶆槸鍗＄偣銆?* 瀹冩潵鑷閾炬帴杩?`kernelcache.decompressed` 鐨?Apple kext锛坄IOSurfaceRoot.cpp`锛夛紝婧愮爜涓嶅湪杩欐５鏍戜笂銆?`nm kernel.macho | grep -i iosurfaceroot` 鏄┖鐨?鈥斺€?閭ｈ鏃ュ織鍙槸 kext 鐨?`start()` 椤哄甫鎵撳嵃銆?
**`native_offline_gpu_publish()` 涔熸病鏈夎璋冪敤銆?* `XNU_NATIVE_OFFLINE_GPU` 榛樿 0锛?`#if` 鏁翠綋涓哄亣锛宍nm kernel.macho | grep native_offline_gpu` 鏄?0 娆°€傚畠鐨勬簮鐮佸湪
`drivers/NativeMetal/NativeOfflineGPU.cpp`锛屼絾杩欎唤鍐呮牳閲屾病鏈夊畠銆?

## 杩欎竴杞垜鍙嶅鐘殑閿欙紙鍐欑粰涓嬫鐨勮嚜宸憋級

杩欎竴鏅氬湪 `bsd_init.c` 鐨勬帰閽堜笂鑰椾簡鍗佸嚑杞瀯寤猴紝**娌℃湁涓€娆℃槸鍐呮牳鐨勯棶棰橈紝鍏ㄩ儴鏄祦绋嬮棶棰?*銆?閫愭潯璁颁笅鏉ワ紝涓嬫涓嶅啀鐘€?
### 1. 鍚屼竴涓姩浣滈噸澶嶅崄鍑犳鑰屼笉鎹㈡柟娉?
姣忔閮芥槸銆岀寽琛屽彿 鈫?鍐?diff 鈫?鏋勫缓 70 绉?鈫?澶辫触銆嶏紝鎸佺画浜嗗崄鍑犺疆銆?
**`git apply` 瀵瑰亸绉昏繃澶х殑 hunk 鏄潤榛樹涪寮冪殑**锛屼笉鎶ラ敊涔熶笉澶辫触銆傛墍浠ャ€屾瀯寤烘垚鍔熴€嶄笉绛変簬
銆宲atch 搴旂敤浜嗐€嶃€傛垜鐩村埌鐢?`strings kernel.macho | grep vince` 鏁板嚭鏉ヤ竴鐩存槸 **13 涓?*鑰?涓嶆槸 14 涓紝鎵嶅彂鐜?`vfs_mountroot` 閭ｄ釜 hunk 浠庢潵娌¤繘鍘昏繃銆?
**瑙勫垯锛氬悓涓€涓伐鍏峰け璐ヤ笁娆″氨鎹㈡柟娉曪紝涓嶈缁х画璋冨弬銆?* 鏈€鍚庢敼鎴愭寜鍞竴閿氱偣鎻掑叆鏂囨湰
锛坄scripts/vince-bsd-init-probes.py`锛夛紝涓€娆℃垚鍔燂紝鑰屼笖骞傜瓑銆?
### 2. 涓嶅厛楠岃瘉灏辨瀯寤?
鏀瑰畬 patch 搴旇鍏?`git apply --check`锛屾垜鍗寸洿鎺ユ瀯寤猴紝鐢?70 绉掓崲涓€涓€岃繕鏄笉琛屻€嶃€?
**瑙勫垯锛氳兘鍦ㄤ竴绉掑唴楠岃瘉鐨勪簨锛屼笉瑕佺敤涓€鍒嗛挓鐨勬瀯寤哄幓楠岃瘉銆?*

### 3. 琛屽彿閲忛敊浜嗗璞?
鎴戦噺鐨勬槸銆屾垜鐨?patch 宸茬粡搴旂敤涔嬪悗銆嶇殑浣嶇疆锛屽嵈褰撴垚銆屽簲鐢ㄤ箣鍓嶃€嶇殑鍩虹嚎鍐欒繘 diff銆?鏇寸碂鐨勬槸涓€旀崲浜嗕笁娆″弬鑰冪姸鎬侊紙pristine / `unixnu tree` 涔嬪悗 / build 澶辫触涔嬪悗锛夛紝
姣忔寰楀埌鐨勬暟瀛楅兘涓嶄竴鏍凤細

```
pristine                      calling bsd_autoconf = 816
unixnu tree 涔嬪悗锛堟病鎵?patch锛? = 816
build 澶辫触涔嬪悗锛堟湁鍓嶉潰 64 涓級  = 924
鎴戠殑 patch 搴旂敤涔嬪悗            = 925
```

**瑙勫垯锛氬啓 diff 鍓嶅厛鏄庣‘銆屾垜瑕佺殑鏄摢涓€涓姸鎬佺殑鍧愭爣銆嶏紝骞跺湪鍚屼竴娆℃祴閲忛噷鍙栧叏閮ㄩ敋鐐广€?*

### 4. WSL 閲岀敤 Windows 璺緞

`generate_patch.py` 閲屽啓 `r'C:\Users\...'`锛屽湪 WSL 閲岄偅鏄?*瀛楅潰鏂囦欢鍚?*锛屼簬鏄柊 patch
鍐欒繘浜嗕竴涓彨 `C:\Users\...` 鐨勬€枃浠讹紝鐪熸鐨?patch 涓€涓瓧閮芥病鍙橈紝鏋勫缓鑷劧杩樻槸鏃х殑銆?
**瑙勫垯锛歐SL 閲屼竴寰?`/mnt/c/...`銆?*

### 5. 鏀逛簡鏂囦欢娌℃彁浜わ紝WSL 鐨?`reset --hard` 灏辨妸瀹冨悆鎺変簡

鍑虹幇杩囪嚦灏戜笁娆°€俙build` 鑴氭湰绗竴姝ュ氨鏄?`git reset --hard FETCH_HEAD`銆?
**瑙勫垯锛氭敼瀹岀珛鍒?commit + push锛屽啀璁?WSL 鎷夈€?*

### 6. 鎶娿€屾帰閽堜笉瀛樺湪銆嶅綋鎴愩€屾帰閽堟病杈撳嚭銆?
鎴戣杩囥€宍vince: loopattach` 娌″嚭鏉ワ紝鎵€浠ュ崱鍦?loopattach銆嶁€斺€?**閭ｆ潯鎺㈤拡褰撴椂鏍规湰涓嶅瓨鍦?*銆傚垽鏂€屾煇鏉℃棩蹇楁病鍑虹幇銆嶄箣鍓嶏紝蹇呴』鍏堢‘璁ゅ畠鍦ㄤ簩杩涘埗閲屻€?
**瑙勫垯锛歚strings kernel.macho | grep '^vince: '` 鏁颁竴閬嶏紝鍐嶈В璇诲睆骞曘€?*

### 7. 杩?`IOsurfaceRoot` 鐨勬簮鐮?
鑺辨椂闂村湪鏍戦噷鎼?`installMemoryRegions`锛屽彧鎼滃埌浜岃繘鍒躲€?`nm kernel.macho` 閲屽叾瀹?*涓€涓?`iosurfaceroot` 绗﹀彿閮芥病鏈?* 鈥斺€?瀹冩潵鑷閾炬帴杩?`kernelcache.decompressed` 鐨?Apple kext锛屾敼涓嶄簡銆傜敤鎴风洿鎺ュ彨鍋滀簡杩欐潯姝昏矾銆?
**瑙勫垯锛氬厛 `nm`/`strings` 纭绗﹀彿褰掑睘锛屽啀鍐冲畾瑕佷笉瑕佹壘婧愮爜銆?*

### 8. 涓轰簡銆屽榻愬埆浜恒€嶆妸宸查獙璇佺殑鍊兼敼鍧?
鎶?`darwinboot-memory-size` 浠?4.75 GiB 鏀规垚 1PJL 鐨?512 MiB锛岀洿鎺ヤ粠銆岃蛋鍒?launchd銆?閫€鍥炲埌銆屽崱鍦?`kminit`銆嶃€傞偅鏄?6 GiB 鏈哄瀷鐨勫€硷紝鑰岃繖鍙版槸 **12 GiB 鎵╁鏈?*銆?
**瑙勫垯锛氳兘璺戦€氱殑閰嶇疆鍒姩銆傚埆浜虹殑鍙傛暟瑕佹寜鑷繁鏈哄櫒鐨勭墿鐞嗗唴瀛樻崲绠椼€?*

### 9. 蹇界暐浜嗘瀯寤虹紦瀛?
鏀逛簡 patch锛屼絾 `bsd_init.o` 鍥犱负 `OWNER_ROOT_STAMP` 娌″彉鑰屾病閲嶇紪锛屾帰閽堣嚜鐒惰繘涓嶅幓銆?
**瑙勫垯锛氬姩 `bsd_init.c` 灏卞繀椤?`find build -name 'bsd_init.o' -delete`銆?*

### 10. 姣忔 `unixnu tree` 閮戒細娓呮帀 `.cache/xnu-work` 閲岀殑鎵嬪伐鏀瑰姩

鍖呮嫭 DriverKit 澶达紙`IORPC.h`锛夛紝浜庢槸 `archive-03` 鎶?`IORPC.h file not found`銆?鐜板湪缁熶竴鍏ュ彛 `build_one.sh` 閲屼細鑷姩琛ワ紝浣嗚繖鏉¤璁颁綇銆?
### 鏈€缁堝舰鎬?
```bash
bash scripts/vince-bsd-init-probes.py .cache/xnu-work/bsd/kern/bsd_init.c
```

鎸夐敋鐐规彃鍏ワ紝杈撳嚭姣忎竴澶?`insert` / `skip`锛岄噸澶嶈繍琛屽畨鍏ㄣ€?`build-xnu-4k-baseline.sh` 鍦?patch 寰幆涔嬪悗璋冪敤瀹冦€?

## 鏍瑰嵎鎸傝浇璺緞锛氬崱鐐瑰凡缁忔敹鏁涘埌涓€琛岃皟鐢?
涓夊ぉ鍓嶅彧鑳界湅鍒般€屽睆骞曞仠浣忋€嶃€傜幇鍦?`bsd_init.c` 鍜?`IOKitBSDInit.cpp` 閲屼竴鍏?39 涓帰閽堬紝
鎶?`inittodr` 涔嬪悗鐨勬瘡涓€绔欓兘鐓т寒浜嗐€傚疄闄呰蛋鍒扮殑璺緞鏄細

```
inittodr done
mount loop iteration
setconf enter
setconf calling IOFindBSDRoot
IOFindBSDRoot enter
IOBSD wait start
IOBSD waitForMatchingService
  IOsurfaceRoot::installMemoryRegions()        <- 绛夊緟鏈熼棿鏋氫妇鏈嶅姟锛屼笉鏄崱鐐?  IOSurface disallowing global lookups
IOBSD matched                                   <- apfs + IOStorageFamily 閮芥敞鍐屾垚鍔熶簡
IOBSD read /chosen
root-matching Present                           <- 鎴戝姞鐨?UUID 璇诲埌浜?didRam=0
mdevadd ramdisk base=c40d5000 size=400000       <- 4 MiB RAMDisk锛屽氨鏄?ramdisk.img
past ramdisk, matching=set rd=none              <- matching 鏈夊€硷紝rd 宸叉竻绌?waitForService enter                            <- 鈽?鍗″湪杩欓噷
```

### 缁撹

`IOFindBSDRoot` 鎷跨潃 `root-matching` 鐨勫尮閰嶆潯浠跺幓绛変竴涓?IOMedia锛?
```xml
<dict>
  <key>IOProviderClass</key><string>IOMedia</string>
  <key>IOPropertyMatch</key>
  <dict><key>UUID</key><string>04769D26-2CA0-4825-B443-E2E5F88300F2</string></dict>
</dict>
```

**杩欎釜 UUID 鏄?APFS 鍗风殑 UUID锛屼笉鏄?GPT 鍒嗗尯 UUID銆?* 瀹冨彧鏈夊湪 apfs 瑙ｆ瀽瀹屽鍣ㄣ€佹妸鍗蜂綔涓?IOMedia 鍙戝竷涔嬪悗鎵嶄細鍑虹幇鍦ㄥ睘鎬ч噷銆?
`IOKitBSDInit.cpp` 鐨勭瓑寰呮槸锛?
```c
968  do {
969      t.tv_sec = ROOTDEVICETIMEOUT;      // 120 鎴?60 绉?973      service = IOService::waitForService( matching, &t );
974      if ((!service) || (mountAttempts == 10)) { ... }
```

**瓒呮椂涓嶆槸鑷村懡鐨?* 鈥斺€?杩斿洖 NULL 鍚庢墦鍗?`still waiting for root device`銆佺潯 5 绉掑啀閲嶈瘯銆?鎵€浠ユ妸 `ROOTDEVICETIMEOUT` 涓存椂鏀规垚 5 绉掞紝姣忔鍒锋満 30 绉掑氨鑳芥嬁鍒扮瓟妗堛€?
### 鎺掗櫎鎺夌殑涓夋潯姝昏矾

| 鏇剧粡鎬€鐤?| 瀹為檯 |
|---|---|
| `IOsurfaceRoot::installMemoryRegions()` 鍗℃ | 瀹冩潵鑷閾炬帴鐨?Apple kext锛坄IOSurfaceRoot.cpp`锛夛紝鍙槸 `IOBSD wait` 鏈熼棿鏋氫妇鏈嶅姟鐨勫壇浜у搧 |
| `native_offline_gpu_publish()` 鍗℃ | `XNU_NATIVE_OFFLINE_GPU` 榛樿 0锛宍strings` 閲岄偅鏉¤皟鐢ㄦ牴鏈笉瀛樺湪 |
| `darwinboot-memory-size` 澶皬 | 4.75 GiB 瓒冲鎶?4 MiB RAMDisk 鏄犲皠鍑烘潵锛坄mdevadd base=c40d5000`锛夈€?12 MiB 閭ｆ鐨勫洖閫€鏄畠瀵艰嚧鐨勶紝宸叉仮澶?|
| apfs 娌″湪 roots 閲?| `IOBSD matched` 璇佹槑 apfs 鍜?IOStorageFamily 閮芥敞鍐屼簡 |

#
## 灞忓箷杈撳嚭锛氬凡缁忎慨濂戒簡

### 涓や釜鏍瑰洜锛堥兘鍦ㄧ敾瀛椾唬鐮侀噷锛屼笉鍦ㄨ鍙凤級

| 闂 | 浠ｇ爜 | 鍚庢灉 |
|---|---|---|
| 姣忕敾涓€琛屾竻鎺?**450px** | `vince_mark_text`: `fill(0, y-12, g_w, 10*lh, BLACK)`锛宍lh = 45` | 琛岃窛灏忎簬 450px 鐨勮浜掔浉鎿﹂櫎锛屾€庝箞鎺掍綅閮芥病鐢?|
| console 婊氬埌**灞忓箷鏈€搴?* | `vince_mark_putc`: `g_ty > g_h - 40` 鎵嶅洖鍗?| console 浼氱洊鎺変换浣曚綅缃殑鐘舵€佽 |

### 淇硶

```c
/* vince_early_mark.c 鈥斺€?姣忚鍙竻鑷繁 */
fill(0, y > 20 ? y - 12 : 0, g_w, lh + 16, 0xFF000000);

/* vince_early_mark.c 鈥斺€?console 鍋滃湪鐘舵€佸尯涔嬩笂 */
if (g_ty > (g_h > 200 ? g_h - 780 : 600)) { g_ty = 16; }
```

### 鏈€缁堝竷灞€锛坧anel 1600x2560锛?
```
 16 鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?      console        鈹? 婊氬埌 1780 涓烘
1780 鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?                    鈫?780px 淇濈暀鍖?1850  guard 0/1/2
1920  walk N
1990  <绫诲悕>
2060  <瀹炰緥鍚?
2130  IOFindBSDRoot entered
2200  A call wfs  鈫? B returned 0/1
```

**鍏绛夎窛 70px銆佷簰涓嶅共鎵般€乧onsole 杩涗笉鏉ャ€?* 杩欎竴鍧楀凡缁忕ǔ瀹氾紝瀹炴満楠岃瘉閫氳繃銆?
### 杩樺墿涓嬬殑灞忓箷闂

console 鏃ュ織浠嶇劧鏄剧ず銆傚師鍥犳煡娓呬簡锛歚PE_kputc` 鏈?*涓夊**璧嬪€硷紝鍓嶄袱澶勬垜宸茬粡鍏虫帀锛?
1. `osfmk/arm/vince_early_mark.c` 鈥斺€?`if (0)` 鍖呬綇锛屽凡澶辨晥
2. `pexpert/arm/pe_kprintf.c` 鐨?regex patch 鈥斺€?鍥犱负 `PE_kputc` 鏄嚱鏁版寚閽堣€岄潪鍑芥暟瀹氫箟锛宺egex 鍖归厤涓嶅埌锛岃蛋浜?WARN 鍒嗘敮
3. **`patches/xnu/zzzz-vince-kprintf-default-on.patch:29`** 鈥斺€?鏃犳潯浠舵墽琛岋紝**杩欐墠鏄棩蹇楄繕鍦ㄧ殑鐪熸鏉ユ簮**锛屼笅涓€杞鐞嗗畠

鍙﹀ `IOsurfaceRoot` 鍜岃摑搴?`UnI XNU` 妯箙宸茬粡閫氳繃銆屾槧灏勫悗鏁村睆濉粦銆嶆竻鎺変簡銆?

## 鏍瑰洜鎵惧埌浜嗭細ADT 缂轰竴涓?`interrupt-controller` 灞炴€?
**杩欐槸鏁存潯閾剧殑鐪熸婧愬ご锛屾瘮涔嬪墠杩界殑 IODTNVRAM 杩囨护瑕佹牴鏈緱澶氥€?*

灞忓箷涓婃湁杩欎箞涓€琛岀櫧瀛楋細

```
pe_arm_map_interrupt_controller: failed to find the interrupt-controller.
```

`pexpert/arm/pe_identify_machine.c:206` 鏄繖鏍锋壘涓柇鎺у埗鍣ㄧ殑锛?
```c
if (SecureDTFindEntry("interrupt-controller", "master", &entryP) == kSuccess) {
    SecureDTGetProperty(entryP, "reg", (void const **)&reg_prop, &prop_size);
    gPicBase = ml_io_map(soc_phys + *reg_prop, *(reg_prop + 1));
}
if (gPicBase == 0) {
    kprintf("...failed to find the interrupt-controller.\n");
}
```

`SecureDTFindEntry` 鐨勭鍚嶆槸 **(propName, propValue, entryP)**锛屽悓鏂囦欢閲屽叾瀹冭皟鐢ㄥ彲浠ュ嵃璇侊細

```c
SecureDTFindEntry("name", "arm-io", ...)          // 鎵?name = "arm-io"
SecureDTFindEntry("device_type", "timer", ...)    // 鎵?device_type = "timer"
SecureDTFindEntry("name", "uart0", ...)           // 鎵?name = "uart0"
```

鎵€浠ュ畠鎵剧殑鏄細**甯?`interrupt-controller` 灞炴€с€佷笖璇ュ睘鎬у€间负 `master` 鐨勮妭鐐?*銆?
鑰?`make-vince-adt.py` 鐢熸垚鐨?`intc` 鑺傜偣鍙湁涓変釜灞炴€э細

```python
node('intc', [('compatible', b'arm,gic-v3\0'),
              ('reg', ...),
              ('redistributor-stride', ...)])
```

**娌℃湁 `interrupt-controller` 鏍囪锛屾墍浠ユ案杩滄壘涓嶅埌銆?*

### 涓轰粈涔堣繖涓€涓睘鎬у氨鑳藉崱姝绘暣涓?boot

```
ADT 缂?interrupt-controller
  鈫?gPicBase = 0锛屼腑鏂瓙绯荤粺瀹屽叏涓嶅彲鐢?    鈫?IODTNVRAM 璇诲睘鎬ц璧?SPI/I2C锛岀瓑涓嶅埌涓柇锛屾棤闄愰樆濉?      鈫?instanceMatch 鍗″湪 matchInternal 閲?        鈫?waitForService(IOMedia+UUID) 鐨?5 绉掕秴鏃朵篃杞笉鍒帮紙瀹冩寔鐫€ IOCatalogue 閿侊級
          鈫?boot 鍋滀綇
```

**UFS 璇荤洏瑕佽蛋涓柇锛屼篃鏄悓涓€涓梾鏍广€?* 涔嬪墠鎶婂崱鐐瑰綊鍒?IODTNVRAM銆乁FS銆乤pfs銆丟PU 閮戒笉瀵癸紝
瀹冧滑閮藉彧鏄€岀瓑涓柇銆嶇殑涓嶅悓鍙楀鑰呫€?
### 淇

```python
node('intc', [('compatible', b'arm,gic-v3\0'),
              ('interrupt-controller', b'master\0'),    # 鈫?鏂板锛孲afeDTFindEntry 鎵剧殑灏辨槸瀹?              ('name', b'interrupt-controller\0'),
              ('reg', struct.pack('<4Q',
                                  GIC_DIST - ARMIO_BASE, GIC_DIST_SIZE,
                                  GIC_REDIST - ARMIO_BASE, GIC_REDIST_SIZE)),
              ('redistributor-stride', struct.pack('<Q', 0x40000))])
```

鍩哄潃鏈潵灏卞寰椾笂锛?
```
ARMIO_BASE = 0x17000000        (arm-io 鐨?ranges锛屽嵆 gSocPhys)
GIC_DIST   = 0x17a00000        (SM8150 sm8150.dtsi intc@17a00000)
reg 鍋忕Щ   = GIC_DIST - ARMIO_BASE = 0xA00000
gPicBase   = soc_phys + 鍋忕Щ = 0x17a00000   鉁?```

## 涓嬩竴姝ヨ鐪嬬殑涓や欢浜?
1. **`waitForService` 鏄秴鏃惰繑鍥?NULL锛岃繕鏄牴鏈崱姝伙紵** 5 绉掕秴鏃跺悗濡傛灉鍙嶅鎵撳嵃
   `waitForService=(nil)` + `still waiting for root device`锛屽氨鏄€孶FS 娌″彂甯冨甫璇?UUID
   鐨?IOMedia銆嶏紱濡傛灉 `=%p` 涓€鐩翠笉鎵撳嵃锛屾墠鏄?IOCatalogue 鐨勯攣闂銆?2. **UFS 椹卞姩鍙戝竷 IOMedia 鏃跺甫涓嶅甫 UUID銆?* `NativeUfs.cpp:1532` 鍜?   `NativeRamBlock.cpp:293` 閲岀殑 `selectVolumeSeed()` 閮芥槸**鏌ヨ**鏂癸紙`getMatchingServices`锛夛紝
   涓嶆槸鍙戝竷鏂广€傜湡姝ｈ `UUID` 灞炴€х殑鏄?`IOStorageFamily` 浠庝粙璐ㄩ噷璇诲嚭鏉ョ殑锛?   鎵€浠?UFS 涓€渚у繀椤昏 apfs 鑳借鍑哄鍣ㄥご銆?
## 涓嬩竴姝?
**鍞竴缂虹殑鏄竴浠界湡姝ｇ殑鏍规枃浠剁郴缁熴€?*

```
./unixnu ipsw fetch                          # OS + Cryptex1,SystemOS
./unixnu build userdata                      # SHNGROOT manifest + 涓や釜绐楀彛
fastboot flash userdata out/vince/userdata/userdata-root.img
```

宸茬煡锛歚[userdata]` 鐨?LBA 鏃╁疄娴嬪ソ锛坄first_lba = 0x288C40` / `last_lba = 0x77BF3FA` /
`lba_bytes = 4096`锛夈€?
**涓嶅啀鏄紪璇戦棶棰橈紝涓嶅啀鏄┍鍔ㄩ棶棰?鈥斺€?鏄暟鎹棶棰樸€?*

> ### 涓€涓細闈欓粯姣佹帀鎵€鏈夋瀯寤虹殑鍧戯紙宸蹭慨锛?>
> WSL 鐨勫叏灞€ gitconfig 閲屾浘缁忔湁锛?>
> ```
> url.https://gh.llkk.cc/https://github.com/.insteadof  https://github.com/
> ```
>
> 閭ｄ釜鍔犻€熼暅鍍忓凡缁忔寕浜嗭紝浜庢槸**姣忔 `git fetch` 閮介潤榛樺け璐?*锛坄gnutls_handshake() failed`锛夛紝
> 鑰屾瀯寤鸿剼鏈収鏃х敤銆屽凡缁忔鍑虹殑鏃т唬鐮併€嶇户缁窇銆傝〃鐜版槸锛氭槑鏄庢敼浜嗕粨搴擄紝鏋勫缓缁撴灉鍗存案杩滀笉鍙樸€?> 宸插垹闄よ瑙勫垯锛宍github.com` 鐩磋繛姝ｅ父銆?>
> **鍑℃槸銆屾敼浜嗘病鍙嶅簲銆嶏紝绗竴姝ュ厛鏌?`git log -1` 鍜?`git fetch` 鏄惁鐪熺殑鎴愬姛銆?*


> ### 閲岀▼纰戯細鍧楅┍鍔ㄧ涓€娆＄湡姝ｆ敞鍐岋紙walk 浠?1 鍙樻垚 2锛?>
> 涔嬪墠鎵€鏈夌増鏈殑灞忓箷閮芥槸 `walk 1` 鈥斺€?閬嶅巻鍙鍒伴偅涓?IODTNVRAM 鑺傜偣锛屽洜涓?UFS 鏄彧璇绘帰閽堬紝
> 浠庝笉鍙戝竷鍧楄澶囥€傛仮澶嶃€岀湡鍧楅┍鍔?+ `build-ufs-original-bindings.py`銆嶄箣鍚庯細
>
> ```
> keys1
> walk2      鈫?鈽?instanceMatch 璧颁簡 2 涓湇鍔★紝鍧楄澶囪嚜宸辨敞鍐岃繘鏉ヤ簡
> guard2
> IOFindBSDRoot entered
> ```
>
> **杩欏悓鏃惰瘉鏄庣粷瀵瑰湴鍧€缁戝畾锛坄.globl` + `.set symbol, <addr>`锛夊湪鐪熸満涓婃垚绔?* 鈥斺€?鑻ュ湴鍧€涓嶅锛?> 鍐呮牳浼氬湪鏇存棭闃舵宕╂帀锛屼笉浼氳蛋鍒?`IOFindBSDRoot`銆?>
> ### 涓轰粈涔堣В鍐充簡銆寀ndefined 涓?duplicate銆嶇殑涓ら毦
>
> `IOBlockStorageDevice` 灞炰簬 IOStorageFamily kext锛屼笉鍦ㄥ唴鏍搁噷锛?>
> | 鍋氭硶 | 缁撴灉 |
> |---|---|
> | 涓嶉摼鎺?| 鍑犵櫨涓?`__ZN20IOBlockStorageDevice...` undefined |
> | 閾炬帴 `IOBlockStorageDevice-reference.o` | 娉ㄥ唽绗簩涓?metaclass 鈫?`postModLoad` panic |
> | `-Wl,-undefined,dynamic_lookup` | Linux 鐨?ld64 鏂█宕╂簝锛坢acOS 鎵嶅彲鐢級 |
> | **`build-ufs-original-bindings.py`** | **绗﹀彿 `.set` 鍒?prelinked kext 鐨勭湡瀹炲湴鍧€** |
>
> binder 璇荤殑鏄?`build/native-prelink/*-candidate.macho` + `.json`銆傞偅涓?candidate 浠庝笉鐢熸垚锛?> 浣?`out/vince/kernel/kernel.macho` + `kernel.json` 婊¤冻瀹冪殑鍏ㄩ儴鏍￠獙
> 锛坄candidate_sha256` 鐩哥銆乣original_sha256` 绛変簬閿佸畾鐨?kernelcache銆乸lan 閲屽惈 IOStorageFamily锛夛紝
> 鎵€浠ユ瀯寤哄墠鎶婅繖涓や釜鏂囦欢鏆傚瓨鎴?candidate 鍗冲彲銆備骇鍑?11 涓鍙凤紝鍏ㄩ儴鏍囪 `A`锛坅bsolute锛夈€?>
> **鏃堕棿绾匡紙浠庝粨搴撳巻鍙叉仮澶嶏級**锛?0:40 鍐呮牳鍒?launchd 鏃讹紝鍧楅┍鍔ㄤ笌 bindings 閮藉湪浣嶏紱21:37 鏀圭敤
> 瀵勫瓨鍣ㄦ帰閽堬紝21:41 椤烘墜鍘绘帀 bindings锛屾鍚?`IOMedia` 鎭掍负 0锛屾枃妗ｅ嵈璁版垚銆屼笉鏄┍鍔ㄩ棶棰樸€嶃€?>
> ### 寰呬慨锛歚IOMedia` 璁℃暟琛屼細琚?console 瑕嗙洊
>
> `vince_mark_num("IOMedia", nmedia, 1850)` 鍦ㄦ帰閽堥噷浠嶅湪鎵ц銆佸唴鏍搁噷涔熸湁璇ュ瓧绗︿覆锛屼絾灞忓箷涓婁笉鏄剧ず锛?> 璇ヨ浣嶄簬 console 娈嬬暀鐧藉瓧鐨勮鐩栬寖鍥村唴銆備笅涓€杞妸瀹冩尓鍒?1900 浠ヤ笅鎴栨敼涓轰笌 `keys` 鍚屾帓鏄剧ず銆?
> ### 涓嬩竴闃舵鐩爣锛堝綋鍓嶏級
>
> 鏋勫缓鏄豢鐨勶紝鍧楅┍鍔ㄦ寜璁捐鏄彧璇绘帰閽堬紝閮戒笉鏄棶棰樸€傜洰鏍囨敹鏁涙垚涓夋潯锛?>
> 1. **鐢ㄤ粨搴撻噷杩欎竴鐗堝唴鏍稿惎鍔紝纭瀹冨仴搴峰湴瓒婅繃 `vfs_mountroot`** 鈥斺€?鍒ゆ嵁鏄睆骞曚笂涓嶅啀鍑虹幇
>    `Metaclass ... duplicate class`銆乣gPICBase` 鏄湁鏁堝湴鍧€銆佸叚琛岀姸鎬佽骞插噣銆?> 2. **鏌ユ竻宸茬粡鍒峰叆鐨?userdata 涓轰粈涔堟病琚噰鐢ㄤ负鏍?* 鈥斺€?瀵圭収 `userdata-root.json` 閲?>    `manifest_sha256 = 6684c652鈥 涓?OS 绐楀彛 `offset=1048576 / size=6077546496`锛?>    纭 `[payload.adt]` 鐨?`root_match_volume_uuid` 涓?manifest 閲岀殑鍗疯韩浠戒竴鑷淬€?> 3. **鍙湁涓婇潰涓ゆ潯閮芥垚绔?*锛屾墠閲嶆柊鑰冭檻鐪熷潡椹卞姩锛坄XNU_vince_UFS_REGISTER_PROBE=0`锛夛紝
>    鑰岄偅鏉¤矾闇€瑕?verified-root bundle锛宐undle 闇€瑕?target image 鐨?volume policy銆?








> ### 馃幆 浜屽垎缁撴灉锛歚vm_page_free_count` 鐨勫紓甯告槸鐥囩姸锛屼笉鏄梾鍥?>
> 浜斾釜鏃剁偣鍏ㄩ儴瀹炴祴锛堝墠鍥涗釜鐢?`vince_mark_num` 鐢诲浐瀹氳锛屾渶鍚庝竴涓粠 panic 閲岃锛夛細
>
> | 鏃剁偣 | `vm_page_free_count` | 浣嶇疆 |
> |---|---|---|
> | `initialize_ram_ranges` | **0** | `pmap.c` |
> | `pmap_startup` 杩斿洖鍚?| **1,207,626** 鉁?| `vm_resident.c` |
> | `vm_page_bootstrap` 缁撴潫 | **1,207,621** 鉁擄紙wire 37,563锛?| `vm_resident.c` |
> | `IOFindBSDRoot` 鍏ュ彛 | **1,207,627** 鉁?| `IOKitBSDInit.cpp` |
> | execve 鏃?| **91,199,441** 鉁?| `kern_exec.c` 璺緞 |
>
> **`max_mem` = 4864 MiB锛堟纭級锛宍max_mem/4096` = 1,245,184锛屼笌瀹炴祴椤垫暟鍚诲悎銆?*
>
> 缁撹锛氫粠鍐呮牳鍚姩鍒版牴鍗峰尮閰嶃€乁FS 椹卞姩鍏ㄧ▼锛坄host:driver-alloc` / `ufs:entered` /
> `root:1-bringup` 閮藉湪灞忓箷涓婏級锛屽唴瀛樿鏁?*涓€鐩存纭?*銆傛崯鍧忓彧鍙戠敓鍦ㄦ渶鍚庝竴娆?鈥斺€?`execve` 閲岄偅娆?> `copyout` 缂洪〉銆?>
> **鎵€浠?9100 涓囬〉鏄己椤靛け璐ョ殑鍓骇鍝侊紝涓嶆槸缂洪〉澶辫触鐨勫師鍥犮€?* 涔嬪墠鍥寸粫銆屽唴瀛樹笉瓒冲鑷村缓椤靛け璐ャ€嶇殑
> 鏁存潯鎺ㄦ柇绾夸綔搴燂紝`dram_size` / `owned_memory_size` 瀹屽叏涓嶇敤鍔ㄣ€?>
> ### 杞悜锛氭煡 pmap 鐨?fault 璺緞
>
> 宸茬煡锛?>
> - `cpo0` / `cp20` 鎴愬姛 鈥斺€?鏍堥《鍑犻〉鍙啓
> - 寰€ `ap` 鐩存帴 `copyout` 涓€瀛楄妭 鈫?**panic锛屼笉杩斿洖閿欒**
> - 缂洪〉鐩爣鏄悎娉曠敤鎴峰湴鍧€锛岃惤鍦ㄥ垎閰嶅尯闂村唴
> - 缂洪〉鍙戠敓鍚?`vm_page_free_count` 鍙樻垚 9100 涓?>
> 涓嬩竴姝ヨ鐪嬬殑锛歚vm_fault` 鍦?`MACHINE_CONFIGS=BCM2837` 涓嬬殑琛屼负锛岀壒鍒槸
> `pmap_enter` 瀵?`VM_MEMORY_STACK` 鐨勫垎鏀紝浠ュ強 `copyout` 鐨?`user_access` 寮傚父琛ㄩ」鏄惁娉ㄥ唽 鈥斺€?> 鍚庤€呭喅瀹氱己椤垫槸銆屼慨濂藉苟閲嶈瘯鎸囦护銆嶈繕鏄€岀洿鎺?data abort銆嶃€?>
> ### 宸ュ叿鏀硅繘锛氫竴娆″惎鍔ㄦ嬁鍏ㄩ儴鏃剁偣
>
> 涔嬪墠姣忎釜鏃剁偣閮借 `panic` + 鍒锋満 + 鎷嶇収涓€杞€傛敼鎴?`vince_mark_num(label, value, row)` 鐢诲湪鍥哄畾琛屽悗锛?> 鍥涗釜鏃剁偣鍙互鍦?*鍚屼竴娆″惎鍔?*閲屽叏閮ㄨ鍒?鈥斺€?琛岃窛 80px锛堟瘡琛屾竻 61px锛夛紝鍏ㄩ儴钀藉湪 console 甯?> 锛坄g_h-780 = 1780`锛変互涓嬶細1780 / 1860 / 1940 / 2020銆?
> ### 馃幆 鍐冲畾鎬ф暟鎹細ADT 鍐呭瓨鍙傛暟鏄鐨勶紝寮傚父鍦?`vm_page_free_count`
>
> ```
> maxmem4864        = 4864 MiB = 4.75 GiB   鈫?绛変簬 owned_memory_size = 0x130000000 鉁?> pages1207620      = 1,207,620 椤?> freepg91199444    = 91,199,444 椤?       鈫?搴旂害涓?1,207,620锛岃櫄楂?76 鍊?> ```
>
> 楠岀畻椤靛ぇ灏忥細
>
> ```
> 1,207,620 脳 4096  = 4.95 GB 鈮?4.6 GiB   鉁?涓?4.75 GiB 鍚诲悎 鈫?椤靛ぇ灏?4 KB
> 1,207,620 脳 16384 = 19.8 GB             鉁?涓嶇
> ```
>
> **`max_mem` 涓?`vm_page_pages` 閮芥纭紝`dram_size` / `owned_memory_size` 涓嶉渶瑕佹敼銆?*
> 浠讳綍銆屾妸 dram_size 鏀规垚 6/8 GB銆嶇殑寤鸿閮藉缓绔嬪湪杩欎釜鍊煎緱閲嶆柊纭涔嬪墠 鈥斺€?鑰屾湰鏈烘槸 12 GiB 鎵╁鐗堬紝
> `owned_memory_size` 4.75 GiB 鏄疄娴嬭蛋閫氬埌 launchd 鐨勫€笺€?>
> **鍞竴寮傚父锛歚vm_page_free_count` 铏氶珮 76 鍊嶃€?* 杩欐鏄己椤靛け璐ョ殑鏍瑰洜锛氬垎閰嶅櫒浠ヤ负鏈?9100 涓囩┖闂查〉锛?> 浠?free list 鍙栭〉鏃舵嬁鍒拌秺鐣屾潯鐩紝`pmap_enter` 澶辫触锛岀己椤典簬鏄彉鎴?kernel data abort銆?>
> 涔熻В閲婁簡鏈疆鐨勪袱涓娴嬪樊寮傦細`cpo0` / `cp20` 钀藉湪宸插缓濂芥槧灏勭殑椤典笂锛屾棤闇€鍒嗛厤锛屾墍浠ユ垚鍔燂紱鑰屽湪 `ap`
> 涓婂啓涓€瀛楄妭闇€瑕佹柊椤碉紝璧颁簡閿欒鐨?free list锛岀洿鎺?panic銆?>
> ### 涓嬩竴杞殑鐩爣鏀舵暃涓轰竴涓?>
> **`vm_page_free_count` 涓轰粈涔堟槸 91,199,441銆?*
>
> 宸茬煡瀹冧笉绛変簬 `vm_page_pages`锛?,207,620锛夛紝涔熶笉鏄换浣曞悎鐞嗙殑鐗╃悊閲忋€傝鏌ワ細
>
> 1. `vm_page_bootstrap` 閲屽 `vm_page_free_count` 鐨勮祴鍊艰矾寰勶紱
> 2. 鏄惁鏈夊埆澶勫湪鍚姩鏃╂湡绱姞浜嗚繖涓鏁板櫒锛坄vm_page_grab`/`vm_page_insert` 鐨勫垵鍊硷級锛?> 3. `MACHINE_CONFIGS=BCM2837` 鏄惁璁╅〉姹犲垵濮嬪寲璧颁簡鏍戣帗娲剧殑鍒嗘敮銆?
> ### 鏈疆鐨勭粓鐐癸細鐢ㄦ埛绌洪棿缂洪〉鏃犳硶淇锛圴M/PMAP 灞傦級
>
> 浠?`B returned1` 涔嬪悗锛屽唴鏍歌繘鍒?`launchd` 鐨?`execve`锛岀劧鍚庡湪杩欐潯璺緞涓?panic锛?>
> ```
> ESR = 0x96000045     Data Abort, WnR=1(鍐?, DFSC=0x5(translation fault L1)
> PC  = __bcopyout + 0x1c
> LR  = _copyout + 0x70
> FAR = ustk - 328     钀藉湪鐢ㄦ埛鏍堝垎閰嶅尯闂村唴
> ```
>
> 閫愬眰鎺掗櫎鐨勭粨鏋滐細
>
> | 宸查獙璇?| 缁撹 |
> |---|---|
> | `cpo0`锛坋xec_copyout_strings锛?| 鎴愬姛 鈥斺€?鏍堥《鍑犻〉鍙敤 |
> | `cp20`锛坉ynlinker copyoutptr锛?| 鎴愬姛 |
> | `prt16384` | 涓嶆槸 `size - rlimit` 涓嬫孩锛宲rotect 姝ｅ父 |
> | `freepg 91199444` / `wirepg 945550` | **閮借秴杩囩墿鐞嗛〉鏁帮紙12 GiB 鈮?78 涓囬〉锛?*锛岄〉缁熻涓嶅彲淇?|
> | 鎻愬墠璋冪敤 `exec_prefault_data` | 鏃犳晥 鈥斺€?瀹冨彧 prefault 鏁版嵁娈碉紝涓嶅惈鏍?|
> | 鍦?`ap` 涓婄洿鎺?`copyout` 涓€瀛楄妭 | **鏈韩 panic锛屾病鏈夎繑鍥為敊璇?* |
>
> **缁撹锛氫笉鏄湴鍧€绠楅敊銆佷笉鏄爤澶皬銆佷笉鏄唴瀛樿€楀敖锛岃€屾槸銆岀敤鎴风┖闂寸己椤垫椂鍐呮牳涓嶄慨椤碉紝鐩存帴 data abort銆嶃€?*
> 姝ｅ父鍐呮牳閲?`copyout` 瑙﹀彂缂洪〉浼氱敱 `vm_fault` 鐜板満寤洪〉鍚庨噸璇曟寚浠わ紱杩欓噷瀹冨彉鎴?panic銆?>
> ### 涓嬩竴杞殑涓夋潯绾跨储锛堝悓涓€涓牴锛?>
> 1. **`MACHINE_CONFIGS=BCM2837`** 鈥斺€?鏍戣帗娲鹃厤缃敤浜?SM8150锛孉RM64 pmap 鐨勭粏鑺傦紙椤佃〃灞炴€с€?>    `pmap_enter` 鐨?`VM_MEMORY_STACK` 鍒嗘敮锛夊彲鑳戒笌鐪熸満瑕佹眰涓嶅悓锛?> 2. **`copyout` 鐨?fault 鎭㈠璺緞** 鈥斺€?`user_access` 寮傚父琛ㄩ」鏄惁娉ㄥ唽姝ｇ‘锛坄fault_addr`锛?
> 3. **`vm_page_bootstrap` 鎷垮埌鐨勫唴瀛樺昂瀵镐笉瀵?* 鈥斺€?椤电粺璁¤秴鍑虹墿鐞嗗唴瀛橈紝浼氳繛甯﹀奖鍝?pmap 鍒嗛厤椤佃〃椤点€?>
> 涓夎€呮寚鍚戝悓涓€浠朵簨锛?*VM/PMAP 鍦ㄣ€岄潪鏍囧噯 ARM64 骞冲彴閰嶇疆銆嶄笅鐨勫垵濮嬪寲涓嶅畬鏁淬€?* 鏈疆鐨勪环鍊兼槸鎶婂畠浠?> 銆屽畬鍏ㄧ湅涓嶈銆嶅彉鎴愩€岀簿纭埌灞傘€嶃€?>
> ### 楠岃瘉宸ュ叿鐨勪笁涓潙锛堝悇韪╄繃锛?>
> | 鍧?| 鍚庢灉 | 姝ｈВ |
> |---|---|---|
> | `strings` 榛樿 鈮? 瀛楃 | 2 瀛楃鎺㈤拡鏍囩鐪嬩技涓嶅瓨鍦?| `strings -n 2` |
> | `vince_mark_text` 姣忚娓?61px | 琛岃窛 <61px 鐨勬爣璁颁簰鐩告摝闄?| 琛岃窛 鈮?0px |
> | xnu 鐩爣鏂囦欢鏄?`.cpo` | 鏀规簮鐮佷笉閲嶇紪 | 鍒?`.cpo` 涓嶆槸 `.o` |

> ### 馃幆 绐佺牬锛氭牴鍗锋壘鍒帮紝launchd 鍑虹幇锛圔 returned 1锛?>
> ```
> IOFindBSDRoot entered
> B returned1              鈫?waitForService 杩斿洖浜嗘湇鍔★細甯?UUID 鐨?IOMedia 鎵惧埌浜?> launchd                  鈫?鍐呮牳杩涘埌 load_init_program / execve
> unexpected STATUS!! ...
> ESR=0x96000045  FAR=0x16eff7eb8
> PC=0xfffffff00740eb60  LR=0xfffffff0073fb070
> ```
>
> **杩欐槸鏈Щ妞嶇涓€娆¤ `waitForService(IOMedia+UUID)` 鐪熺殑杩斿洖銆?* 涔嬪墠鎵€鏈夌増鏈兘鏄瓑涓嶅埌銆?> 鎴栫洿鎺ョ┖杞紱杩欎竴娆℃牴鍗峰尮閰嶆垚鍔燂紝`mountroot` 璧伴€氾紝鍐呮牳缁х画鍒?`launchd`銆?>
> 瑙﹀彂鏉′欢锛氶€€浼?`keys`/`walk`/`guard` 涓変釜鎺㈤拡涔嬪悗鍖归厤鎵嶆垚鍔熴€傚畠浠瘡娆￠兘鍦?> `getMatchingServices` 閲岄亶鍘嗘暣涓敞鍐岃〃锛屽緢鍙兘鎵颁贡浜嗗尮閰嶆椂搴忋€?>
> ### 鏂扮殑鍗＄偣锛歟xecve 鍐欑敤鎴锋爤鏃?fault
>
> ```
> PC  = __bcopyout + 0x1c      鍐呮牳鍦?copyout锛堝線鐢ㄦ埛绌洪棿鍐欙級
> LR  = _copyout + 0x70        璋冪敤鑰?> FAR = 0x16eff7eb8            鐩爣鍦板潃锛堝悎娉曠殑 ARM64 鐢ㄦ埛鍦板潃锛屼絾鏈槧灏勶級
> ESR = 0x96000045             EC=0x25 Data Abort, WnR=1 鍐? DFSC=0x5 translation fault L1
> ```
>
> 涔熷氨鏄細`/sbin/launchd` 宸茶鍔犺浇锛屽唴鏍告鍦ㄦ妸 argv/envp 澶嶅埗鍒版柊杩涚▼鐢ㄦ埛鏍堬紝鑰岀洰鏍囬〉娌℃湁寤虹珛
> 鏄犲皠銆?*杩欏睘浜?VM / execve 灞傦紝涓庡瓨鍌ㄨ矾寰勬棤鍏炽€?*
>
> 寰呮煡鏂瑰悜锛?>
> 1. `execve` 閲岀敤鎴锋爤鐨勫垎閰嶈矾寰勶紙`exec_mach_imgact` 鈫?`allocate_user_stack`锛夋槸鍚﹀洜涓?>    `userdata` 涓婄殑鏌愪簺鏉′欢琚烦杩囷紱
> 2. 鐢ㄦ埛鍦板潃绌洪棿鐨勪笂闄愪笌璇ュ湴鍧€锛?.1 GiB锛夌殑鍏崇郴 鈥斺€?鎴戜滑鐨?`dram_size = 0x300000000`锛?2 GiB锛夛紝
>    鐢ㄦ埛 VA 甯冨眬鍙兘涓庤繖涓妯℃湁鍏筹紱
> 3. 鏄惁瀛樺湪銆岄〉琛ㄩ」寤哄ソ浣?pmap 鏈悓姝ャ€嶇殑鏃跺簭闂銆?>
> ### 浠婃櫄瀹屾暣閾炬潯
>
> ```
> boot-arg 淇        -> ufs:entered
> IODelay 鎹㈣嚜鏃?      -> host:lun
> validate() 鎵撳紑      -> prep:attach-done
> start() 鎻掓々         -> start:ok
> 鍧楄澶囧彂甯?          -> walk 3->5
> 鏃跺熀纭             -> clock:advances
> waitForService 鎹㈠繖绛?-> B returned 1     鈽?鏍瑰嵎鎵惧埌
> 閫€浼戝共鎵版帰閽?        -> launchd            鈽?execve 寮€濮?> ```

> ### 浠婃櫄鐨勫畬鏁撮摼璺紙浠庨潤榛樺埌绮剧‘澶辫触锛?>
> 璧风偣锛氬睆骞曚竴鐗囩櫧瀛椼€佸叚琛屾帰閽堜笉鍔ㄣ€佸畬鍏ㄤ笉鐭ラ亾鍐呮牳鍋滃湪鍝€?> 缁堢偣锛歚mountroot` 鏁存潯璺緞璺戝畬骞剁粰鍑?panic 鈥斺€?銆屾槑纭殑澶辫触銆嶆瘮浠讳綍闈欓粯閮芥湁浠峰€笺€?>
> ```
> Failed to mount "root" device 2f5a?d      鈫?panic 杈撳嚭锛圛OKitBSDInit.cpp锛?>
> clock:advances      鏃跺熀姝ｅ父
> host:lun            UFS 鍛戒护閾惧叏閫氾紙NOP / 鐢垫簮鏌ヨ / START STOP UNIT / LUN ready锛?> ufs:entered         NativeUfs::start 閫氳繃涓夐亾妫€鏌?> prep:attach-done    configure + attach 鎴愬姛
> keys2               鍖归厤琛?= IOMedia + UUID锛堟纭舰鐘讹級
> media:no-uuid       鏃犵鍚嶈韩浠斤紝璺宠繃 UUID 绛夊緟
> walk402             200 娆¤疆璇?脳 2 涓湇鍔★紝姝ｅ父閫€鍑?> guard1              绫诲悕鍖归厤锛堥潪 exact锛?> IOFindBSDRoot entered
> B returned0         200 娆￠亶鍘嗭紝鏃?IOMedia 甯︾洰鏍?UUID
> ```
>
> ### 閫愰」淇锛堟寜鍙戠幇椤哄簭锛?>
> | 鐜拌薄 | 鐪熷洜 | 澶勭悊 |
> |---|---|---|
> | 灞忓箷鍙湁鐧藉瓧锛屼竴涓帰閽堥兘涓嶅姩 | `NativeUfs::start()` 缂?`native-ufs-root=1`锛岀涓€琛屽氨 return false | ADT `boot-args` 琛ヤ笂锛屽苟鍔?`native-ufs-diagnostics=1` |
> | 鎵€鏈夋帰閽堥兘鐢诲湪 console 鍖鸿鐧藉瓧鍘嬩綇 | 琛屽彿 1240鈥?640 鍏ㄥ湪 `g_h-780` 浠ュ唴 | 鍏ㄩ儴鎼埌 1780 浠ヤ笅锛岄棿璺?鈮?80px锛堟瘡琛屾竻 61px锛?|
> | 鍗″湪 `host:nop` 涓€鍒嗛挓 | `IODelay()` 鍐呴儴绛?`mach_absolute_time()`锛岃€屽懡浠ょ‘瀹炴病瀹屾垚 | 鎹?timer-free `yield` 鑷棆 + 杞璁℃暟 |
> | 鏈夎秴鏃朵唬鐮佸嵈浠庝笉瑙﹀彂 | 鍚屼笂锛宍expired()` 渚濊禆鍚屼竴鎶婇挓 | `pollUfsTransfer` 鍔?100 涓囨涓婇檺 |
> | 鍧楄澶囦笉鍙戝竷 | `validate()` 鍦ㄩ潪 verified 鏋勫缓閲屾棤鏉′欢 `return false` | bring-up 鏈熼棿鎵撳紑锛堝師鏂囨敞閲婏細Root publication requires owner verification in every build锛墊
> | `B returned` 姘镐笉鍑虹幇 | `waitForService` 鐫＄嚎绋嬬瓑涓柇鍞ら啋锛岃€岀潯鐪犲湪姝ら樁娈典笉宸ヤ綔 | 鎹㈡垚蹇欑瓑杞 `getMatchingServices` |
> | 杞涓嶉€€鍑猴紙walk 娑ㄥ埌 4 涓囷級 | `mach_absolute_time()` 鍗曚綅涓嶆槸绾崇锛宍+5e9` 绛変簬鍑犲崈绉?| 鏀规垚 200 娆″皾璇曞皝椤?|
>
> ### 鍓╀笅鐨勫敮涓€闂
>
> **`IOStorageFamily` 娌℃湁鎶婂潡璁惧鍙樻垚鍙寕杞界殑鍗枫€?* 璇锋眰姝ｇ‘锛坄keys2`锛夈€侀亶鍘嗚窇婊★紙`walk402`锛夈€?> 缁撴灉涓虹┖锛坄B returned 0`锛夛紝浜庢槸 `mountAttempts` 绱姞鍒?10 鍚?panic銆?>
> 鏈€鍙兘鐨勫師鍥狅細缂哄皯閰嶅鐨?**`IOBlockStorageDriver`**銆俙NativeUfsBlock` 鍙疄鐜颁簡
> `IOBlockStorageDevice` 鎺ュ彛锛岃€屾病鏈夐┍鍔ㄥ幓鏋氫妇瀹冧笂闈㈢殑浠嬭川骞惰В鏋?APFS 瀹瑰櫒澶?鈥斺€?鎵€浠ユ案杩滀笉浼氬嚭鐜?> 甯?UUID 鐨?`IOMedia`銆?>
> 涓嬩竴姝ョ殑鍒ゆ嵁锛堜竴娆″惎鍔ㄥ嵆鍙尯鍒嗭級锛氭灇涓炬墍鏈?`IOMedia` 骞舵墦鍗板叾 `UUID` 灞炴€?>
> | 缁撴灉 | 缁撹 |
> |---|---|
> | 涓€涓?IOMedia 閮芥病鏈?| 缂?`IOBlockStorageDriver`锛堟渶鍙兘锛墊
> | 鏈?IOMedia 浣?UUID 涓嶅悓 | 鎶婂疄闄?UUID 鍐欒繘 `[payload.adt]` 鐨?`root_match_volume_uuid` |
> | 鏈?IOMedia 涓?UUID 姝ｅソ鍖归厤 | 鍖归厤閫昏緫鏈韩鏈?bug |
>
> ### 涓や釜楠岃瘉宸ュ叿鐨勫潙锛堝悇韪╀袱娆★級
>
> 1. `strings` 榛樿鍙緭鍑?鈮? 瀛楃锛? 瀛楃鐨勬帰閽堟爣绛撅紙`tA`/`tD`锛夌湅璧锋潵銆屼笉鍦ㄥ唴鏍搁噷銆嶃€?*蹇呴』 `strings -n 2`銆?*
> 2. xnu 鐨?C++ 鐩爣鏄?`.cpo` 涓嶆槸 `.o`锛涘彧鍒?`.o` 浼氬鑷存敼浜嗘簮鐮佷笉閲嶇紪銆?
> ### 閲岀▼纰戯細UFS 鍛戒护閾惧叏閫氾紙host:lun锛?>
> ```
> host:lun            鈫?NOP OUT 鈫?鐢垫簮鏌ヨ 鈫?START STOP UNIT 鍞ら啋 鈫?LUN ready 杞
> ufs:entered
> prep:attach-done
> start:ok
> media:no-uuid
> walk5
> guard2
> IOFindBSDRoot entered
> A call wfs
> ```
>
> 涔嬪墠涓€鐩村仠鍦?`host:nop`锛岀湅璧锋潵鍍忋€岃澶囦笉鍝嶅簲 NOP銆嶃€傛崲鎴?timer-free 鑷棆鍚庢暣鏉″懡浠ら摼涓€娆¤蛋閫氾紝
> 璇存槑璁惧涓€鐩村搷搴旇壇濂?鈥斺€?鍗′綇鐨勬槸 `IODelay` 鏈韩銆?>
> 鑷虫 UFS 渚у畬鏁村彲鐢細鎺у埗鍣ㄦ帴绠?鈫?鍛戒护閫氳矾 鈫?绐楀彛鍙戝竷锛坵alk5锛夆啋 `start:ok`銆?>
> ### 浠嶅湪纭鐨勪竴浠朵簨锛氭椂鍩烘槸鍚﹀墠杩?>
> `tA = 3967735401` 璇佹槑 `mach_absolute_time()` 杩斿洖闈為浂锛屼絾宸€奸偅琛屽缁堢┖鐧?鈥斺€?鏀规垚瀛楅潰瀛楃涓?> 锛坄clock:advances` / `clock:STUCK`锛変互鎺掗櫎鏁板瓧娓叉煋璺緞鐨勫奖鍝嶃€?>
> 杩欎釜绛旀鍐冲畾涓嬩竴姝ユ柟鍚戯細
>
> | 缁撴灉 | 鍚箟 | 涓嬩竴姝?|
> |---|---|---|
> | `clock:advances` | 鏃跺熀姝ｅ父 | `waitForService` 鍗″湪涓柇/璋冨害鍣ㄦ病鏈夋帹杩涳紝鍘绘煡璁℃椂鍣ㄤ腑鏂笌 `gPicBase` 鎺ョ嚎 |
> | `clock:STUCK` | 鏃跺熀鍐荤粨 | `CNTPCT`/`CNTFRQ` 鏈紪绋嬶紱淇ソ瀹冨彲涓€娆℃€цВ鍐?`IOSleep`/`IODelay`/`inittodr`/鎵€鏈?IOKit 瓒呮椂 |
>
> ### 楠岃瘉宸ュ叿鐨勫潙锛堜粖鏅氳俯浜嗕袱娆★級
>
> `strings` 榛樿鍙緭鍑?鈮? 瀛楃鐨勫瓧绗︿覆銆傛帰閽堟爣绛?`tA` / `tD` 鍙湁 2 涓瓧绗︼紝浜庢槸銆屽唴鏍搁噷娌℃湁鎺㈤拡銆?> 鐨勯敊璇粨璁哄嚭鐜颁袱娆★紝鐧借窇浜嗕袱杞瀯寤恒€?*鏌?2 瀛楃鎺㈤拡蹇呴』鐢?`strings -n 2`銆?*
>
> 鍙﹀ `vince_mark_text` 姣忚娓?61px锛屾爣璁拌璺濆繀椤?鈮?61px锛堢幇鐢?80px锛夛紝鍚﹀垯鐩搁偦鏍囪浜掔浉鎿﹂櫎 鈥斺€?> 杩欎篃鏄?`tD` 涓€寮€濮嬬湅涓嶈鐨勫師鍥犱箣涓€銆?
> ### 閲岀▼纰戯細鍧楄澶囧畬鏁村彂甯冿紙walk 3 鈫?5锛?>
> ```
> ufs:entered
> prep:attach-done     鈫?configure + attach 鍏ㄩ儴閫氳繃
> start:ok             鈫?registerService() 琚皟鐢?> media:no-uuid        鈫?鏃犵鍚嶈韩浠芥椂璺宠繃 UUID 绛夊緟
> keys1
> walk5                鈫?1 涓?IODTNVRAM + 2 涓?provider + 2 涓?IOMedia
> guard2
> IOFindBSDRoot entered
> A call wfs
> ```
>
> `NativeUfsBlock` 鐨勫畬鏁寸敓鍛藉懆鏈熺涓€娆¤蛋閫氾細鍒嗛厤 鈫?init 鈫?configure锛堢獥鍙ｅ嚑浣曟牎楠岋級鈫?attach 鈫?> `start()` 鈫?`registerService()`銆備袱涓獥鍙ｏ紙OS / SystemOS锛夐兘娉ㄥ唽鎴愬姛銆?>
> ### 鍐冲畾鎬х殑淇锛歚IODelay` 姝荤瓑
>
> 鍦ㄦ涔嬪墠锛屾墍鏈夈€屽崱浣忋€嶅叾瀹炲崱鍦ㄧ瓑寰呭嚱鏁版湰韬紝鑰屼笉鏄瓑寰呯殑鏉′欢锛?>
> ```c
> void delay ()   { IODelay (2); }                            // 鍐呴儴 spin 绛?mach_absolute_time 鍓嶈繘
> bool expired () { return mach_absolute_time () >= deadline; } // 鍚屼竴鎶婇挓
> ```
>
> 鍦ㄨ繖涓惎鍔ㄩ樁娈?`mach_absolute_time()` 涓嶅墠杩涳紝浜庢槸 `IODelay` 绗竴娆¤皟鐢ㄥ氨姘镐笉杩斿洖銆傝繖瑙ｉ噴浜嗕笁涓?> 鐜拌薄鍚屾椂鍑虹幇锛氭湁瓒呮椂浠ｇ爜鍗村崱婊′竴鍒嗛挓銆乣rootDiagnosticFailure("NOP OUT")` 浠庝笉琚皟鐢紙1810 绌虹櫧锛夈€?> 杩?`native-ufs-diagnostics=1` 鐨?panic 閮藉彂涓嶅嚭鏉ャ€傚悗鏉ュ姞鐨?100 涓囨杞涓婇檺涔熸病鐢ㄢ€斺€斿惊鐜綋绗竴姝?> 灏辨病杩斿洖銆?>
> 鐜板湪鍛戒护璺緞涓婃病鏈変换浣曡鏃跺櫒渚濊禆锛?>
> | 浣嶇疆 | 鍘熷疄鐜?| 鐜板湪 |
> |---|---|---|
> | `HardwareTransferPort::delay` | `IODelay(2)` | 200 娆?`yield` 鑷棆 |
> | `hostWaitRegister` 鑺傛媿 | `IODelay(10)` | 400 娆?`yield` 鑷棆 |
> | `hostWaitRegister` 寰幆 | `while (mach_absolute_time() < deadline)` | `for (round < 20000)` |
> | `pollUfsTransfer` 寰幆 | 浠?`expired()` | `+ polls >= 1000000` |
>
> 娉ㄦ剰 `-Werror,-Wdeprecated-volatile`锛氳嚜鏃嬭鏁板櫒涓嶈兘甯?`volatile` 闄愬畾绗︼紙`++` 瀵?volatile 宸插純鐢級锛?> 寰幆浣撻噷鐨?`asm volatile` 瓒充互闃绘浼樺寲銆?>
> ### 鐜板湪鍙墿涓€涓棶棰橈細UUID 涓嶅尮閰?>
> `A call wfs` 涔嬪悗浠嶆棤 `B returned`锛屽嵆 `waitForService(IOMedia + UUID=04769D26-鈥?` 鏈繑鍥炪€?> 鍧楄澶囧凡缁忓瓨鍦紙walk5锛夛紝鎵€浠ラ棶棰樻敹绐勪负锛?*鍙戝竷鐨?IOMedia 甯︿笉甯﹂偅涓?UUID**銆?>
> UUID 鐢?IOStorageFamily 浠?APFS 瀹瑰櫒澶磋鍑猴紝涓嶆槸绐楀彛鑷甫鐨勫睘鎬с€備笅涓€姝ヨ纭鐨勬槸绐楀彛鍑犱綍涓?> `userdata-root.img` 鐨勫疄闄呭竷灞€鏄惁涓€鑷达紙`offset=1048576` / `size=6077546496`锛夈€?
> ### 閲岀▼纰戯細鏍圭獥鍙ｇ粓浜庡彂甯冧簡锛坵alk 1 鈫?3锛?>
> ```
> keys1
> walk3        鈫?instanceMatch 鐜板湪閬嶅巻 3 涓湇鍔★細IODTNVRAM 鑺傜偣 + OS 绐楀彛 + SystemOS 绐楀彛
> guard2
> IOFindBSDRoot entered
> A call wfs
> ```
>
> 涔嬪墠鎵€鏈夌増鏈兘鏄?`walk1`銆俙walk3` 璇存槑涓や釜 `NativeUfsBlock` 宸茬粡閫氳繃 `registerService()` 鍙戝竷锛?> 涔熷氨鏄?`IOStorageFamily` 鏈変簡鍙灇涓剧殑鍧楄澶囥€?>
> 涓夐亾闂ㄤ緷娆℃墦寮€鎵嶈蛋鍒拌繖閲岋紝鍏ㄩ儴璁板綍鍦ㄦ锛?>
> | 闂?| 浣嶇疆 | 澶勭悊 |
> |---|---|---|
> | SMMU 鍐欏悗鍥炶涓嶇 | `SmmuTakeover.h` `configureUfsSmmu()` | bring-up 鏈熼棿 bypass锛堝啓浠嶇劧鍙戠敓锛屽彧鏄笉浠ュ洖璇诲畾鎴愯触锛墊
> | `start()` 鐨勪笁涓墠鎻?| `NativeUfs.cpp` `NativeUfsBlock::start()` | 姣忛亾闂ㄨ嚜鎶ュ悕瀛楋紙`start:no-bounce` / `no-lock` / `base-false` / `ok`锛墊
> | **鏍圭獥鍙ｅ彂甯冮棬绂?* | `NativeUfs.cpp` `validate()` 鐨?`#else` 鍒嗘敮 | **`return false` 鈫?鎵撳紑銆傚師鏂囨敞閲婏細Root publication requires owner verification in every build.** |
>
> **`validate()` 閭ｉ亾鏄璁′笂鐨勭‖闂ㄧ**锛氭湭鍚敤 `NATIVE_VERIFIED_BLOCK` 鐨勬瀯寤洪噷瀹冩棤鏉′欢鎷掔粷鍙戝竷锛?> 杩欐鏄?defconfig 娉ㄩ噴閲岄偅鏉°€屽喎鏋勫缓婊¤冻涓嶄簡鐨勯棬閾俱€嶃€俠ring-up 鏈熼棿浠ユ湭璁よ瘉绐楀彛鍙戝竷锛岃鐩樺皻鏈彲淇°€?>
> ### 鐜板湪鐨勭姸鎬佷笌涓嬩竴姝?>
> 鍧楄澶囨湁浜嗭紝浣?`B returned` 浠嶆湭鍑虹幇锛宍A call wfs` 涔嬪悗娌℃湁涓嬫枃 鈥斺€?`waitForService(IOMedia+UUID)`
> 杩樻病杩斿洖銆傝涔堟槸 5 绉掕秴鏃跺皻鏈蛋鍒帮紝瑕佷箞鏄亶鍘嗘寔鏈夐攣銆?>
> 涓嬩竴姝ュ彧闇€鍥炵瓟涓€涓棶棰橈細**鍙戝竷鐨勮繖涓や釜 IOMedia 甯︿笉甯?root volume 鐨?UUID**銆?>
> ```
> 鏈熸湜锛歎UID = 04769D26-2CA0-4825-B443-E2E5F88300F2锛圼payload.adt] root_match_volume_uuid锛?> 瀹為檯锛氱獥鍙ｅ彧鏄?UFS 涓婄殑瀛楄妭鍖洪棿锛孶UID 瑕佺敱 IOStorageFamily 浠?APFS 瀹瑰櫒澶撮噷璇诲嚭鏉?> ```
>
> 鑻?UUID 涓嶅尮閰嶏紝灏辫纭 `userdata-root.img` 鐨?OS 绐楀彛鍋忕Щ锛坄offset=1048576`銆?> `size=6077546496`锛岃 `userdata-root.json`锛変笌椹卞姩 `configure()` 鏀跺埌鐨勭獥鍙ｅ嚑浣曟槸鍚︿竴鑷淬€?

