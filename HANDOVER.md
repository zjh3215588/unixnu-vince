# vince XNU 绉绘锛氫氦鎺ユ枃妗?
**浜ゆ帴鏃堕棿**锛?026-10-23
**浜ゆ帴鍘熷洜**锛氭柊绐楀彛鎺ユ墜锛屽崟绾挎帹杩?**褰撳墠鐘舵€?*锛氬彲澶嶇幇鍩虹嚎锛宑heckpoint 123

> 鏃╂湡璺緞锛堟帰閽堟敞鍏ユ柟妗堛€乣boot_args.Video` 鐨勫彂鐜般€丮ARK 鏂规鐨勬潵鍘嗭級璁板綍鍦?> **`HANDOVER-legacy.md`**銆傛湰鏂囨槸鍏ュ彛銆?
---

## 涓€銆佷笁鍗佺浜嗚В鐜扮姸

**鑳藉仛浠€涔?*锛欳I 鏋勫缓鍐呮牳锛?3 鍒嗛挓锛夆啋 鎵撳寘 payload 鈫?鍒锋満 鈫?鐪熸満璺戝埌
`IOsurfaceRoot::installMemoryRegions()` 鍋滀綇锛屽睆骞曟樉绀?checkpoint `123` 鍜?16 涓僵鑹叉柟鍧椼€?
**涓嶈兘鍋氫粈涔?*锛氭牴鏂囦欢绯荤粺娌℃寕涓婏紝`launchd` 璧蜂笉鏉ワ紝娌℃湁鐢婚潰銆?
**涓嬩竴姝?*锛氬厛纭閭ｄ釜銆屽仠浣忋€嶆槸鐪熸璺繕鏄彧鏄棩蹇椾腑鏂紙绗簲鑺傦級銆?
---

## 浜屻€佸繀椤荤煡閬撶殑鍏潯纭簨瀹?
### 1. 鍐呮牳鏃ュ織鐨勪袱涓紑鍏抽兘瑕佸叧

```c
// pe_kprintf.c
SECURITY_READ_ONLY_LATE(bool) disable_serial_output  = false;  // 蹇呮敼
SECURITY_READ_ONLY_LATE(bool) disable_kprintf_output = false;  // 蹇呮敼
...
if (!disable_serial_output && !disable_kprintf_output) { ... }
```

**涓や釜榛樿閮芥槸 `true`**锛屽彧鏀逛竴涓笉浼氭湁浠讳綍杈撳嚭銆?
### 2. `PE_kputc` 蹇呴』鏃犳潯浠惰祴鍊?
`PE_init_kprintf` 璺戝湪 `STARTUP(KPRINTF)`锛?*鏃╀簬** framebuffer 鏄犲皠銆傛墍浠ヤ笉鑳藉啓
`if (vince_console_fb_ready()) PE_kputc = vince_mark_putc;` 鈥斺€?鏉′欢姘歌繙涓哄亣锛宧ook 姘镐笉瀹夎銆?
### 3. `0x9000000` 鐨?UART 鏄犲皠鍙兘鍦?QEMU

杩欐槸 **checkpoint 50 鐨勭湡鍑?*銆俙0x9000000` 鍦?QEMU virt 鏄?PL011锛屽湪 SM8150 涓婃槸鍒殑瀵勫瓨鍣ㄣ€?`ml_io_map_unmappable` 鍦ㄤ袱杈?*閮借繑鍥炴垚鍔?*锛岀涓€涓瓧绗﹀啓杩涚湡瀹炵‖浠跺氨宕┿€?
鐜版柟妗堬細鎸夐潰鏉垮昂瀵稿垽鏂紙QEMU 800x600 / vince 1600x2560锛夛紝鍙湪 `w <= 1024` 鏃舵槧灏勩€?
### 4. ADT 閲屽繀椤绘湁 `RAMDisk` 鑺傜偣

鍚﹀垯 DarwinBoot 鎶?`boot refused: Compromised Data`锛?
```
/chosen/memory-map/RAMDisk   16 bytes锛屼袱鍗婂叏 0
```

`make-vince-adt.py --data-ramdisk` 浼氱敓鎴愩€俙board.toml` 鐨?`[payload.adt]` **鍙湁
`packed_data_ramdisk`锛屾病鏈夋櫘閫?`data_ramdisk`** 鈥斺€?璧板畼鏂规祦绋嬫椂杩欐槸涓己鍙ｃ€?
### 5. Xcode 26.0.1 鐨勬柊璀﹀憡瑕佸湪涓夊鎶戝埗

`-Wunnecessary-virtual-specifier` 鍦?`-Weverything -Werror` 涓嬪彉閿欒锛宍OSSymbol.h` 瑙﹀彂銆?涓変釜鐙珛浣嶇疆鍚勬湁鑷繁鐨?flag 鍒楄〃锛?
| 浣嶇疆 | 澶勭悊 |
|---|---|
| `makedefs/MakeInc.def` 鐨?`WARNFLAGS_STD` | `build-xnu-4k-baseline.sh` 鐩存帴娉ㄥ叆 |
| `installhdrs` 鐨?make 璋冪敤 | 浼?`CFLAGS_EXTRA` |
| `build-arm-driver.py` / `audit-storage-interface.py` | 鍚勮嚜琛?`-Wno-*` |

### 6. `kernel.py` 鍐锋瀯寤鸿窇涓ら亶

绗竴閬嶅彧鐢熸垚 compile record锛?*鏁呮剰娓呯┖** 5 涓彉閲忋€備换浣曘€屽悎鏍煎熀绾裤€峠ate 閮戒細鍦ㄧ涓€閬嶆嫤鎴€?鐜版柟妗堬細`build-xnu-4k-baseline.sh` 寮€澶存娴?`startup.o.json` 涓嶅瓨鍦ㄥ氨鏁翠綋闄嶇骇銆?
---

## 涓夈€佸彲澶嶇幇鍩虹嚎

| 椤?| 鍊?|
|---|---|
| 鏋勫缓 | `39905065571` / 13 鍒嗛挓 / success |
| 鍐呮牳 | `kernel.macho` 49.2 MB |
| runner | `macos-26` + Xcode 26.6 |
| defconfig | **9 涓紑鍏?* |
| `[kernel] archives` | **8 涓?* |
| prelink roots | 20 涓?|
| 鍒嗘敮 | `main`锛堟案杩滀繚鎸佸彲鏋勫缓鍙埛鏈猴級|

**鎭㈠鍛戒护**锛?```bash
gh run list --repo Lux12138/unixnu-vince --limit 1 --workflow build-kernel.yml
gh run download <id> --repo Lux12138/unixnu-vince -n kernel-vince -D C:\Temp\vince-base
# gh run download 甯稿け璐ワ紝鐢?API 鐩磋繛锛?#   curl.exe -sL -H "Authorization: token $(gh auth token)" -o out.zip \
#     https://api.github.com/repos/Lux12138/unixnu-vince/actions/artifacts/<AID>/zip
wsl -e bash -c 'KM=/mnt/c/Temp/vince-base/kernel/kernel.macho bash /mnt/c/Temp/payload2.sh'
cd C:\platform-tools
.\fastboot.exe flash cust C:\Users\Administrator\Desktop\unixnu-vince-kernel-ufs\cust-payload.img
.\fastboot.exe boot C:\Users\Administrator\Desktop\unixnu-vince-kernel-ufs\vince-xnu64-Z.img
```

---

## 鍥涖€佷粖澶╂渶澶х殑鏁欒

> **鎶娿€屽惎鐢ㄥ畼鏂瑰叏閮ㄧ壒鎬с€嶅綋鎴愯繕鍊猴紝浠ｄ环鏄崄鍑犺疆鏋勫缓銆?*

`CONFIG_XNU_BOOT_PROGRESS` / `NATIVE_UFS` / `NATIVE_AES` / `VIRTIO_BLOCK` / `OWNER_ROOT_AUDIT`
**涓嶆槸寮€鍏?*锛屾槸涓€鏁村浜掔浉渚濊禆鐨勫悎鏍煎熀绾匡細

- `boot-progress` 瀹炵幇鍦?`UniXNU-sheng/kits/sheng/BootProgress.c`锛?2 KB锛? 3 涓帰閽?鈮?**136 KB**
- 瀹冪殑 builder锛坄build-boot-progress.py`锛夊湪 **fork 鍜?upstream 涓や釜 UniXNU 浠撳簱閲岄兘涓嶅瓨鍦?*
- 鍚敤鍚庤Е鍙?gate 閾撅細AES closure 鈫?CPU/pthread 鈫?owner crypto 鈫?virtio archive锛?*淇竴涓啋涓€涓?*
- `kernel.py` 鐨?bootstrap pass 鏁呮剰娓呯┖杩欎簺鍙橀噺 鈫?gate 鍦ㄥ喎鏋勫缓鏃?*蹇呯劧**鍐茬獊

**绔嬬殑瑙勭煩**锛?1. **bring-up 涓€斾笉鏀?defconfig**
2. **鏋勫缓閾炬帓闅滆秴杩?2 杞氨鍥為€€**
3. **`main` 姘歌繙鍙瀯寤?*

---

## 浜斻€佷笅涓€姝ワ紙鎸夐『搴忥紝鍒烦锛?
### 绗竴姝ワ細鎺掗櫎銆屾棩蹇椾腑鏂€嶇殑鍙兘锛堝崐澶╋級

**鐜板湪鐨勫亣璁惧彲鑳芥槸閿欑殑銆?* 鎴戜滑涓€鐩磋涓?IOSurface 鏄璺紝浣?*浠庢病楠岃瘉鍐呮牳鏄惁杩樺湪璺?*銆?
```c
bsd_autoconf();                              // 褰撳墠鍋滃湪杩欓噷闈?kprintf("vince: bsd_autoconf returned\n");    // 鍔犺繖涓€琛?```

- **鏈夎緭鍑?* 鈫?鍐呮牳杩樻椿鐫€锛孖OSurface 鍙槸鏃ュ織鏂偣 鈫?**鐩存帴杩涚浜屾**
- **鏃犺緭鍑?* 鈫?纭鏄璺?鈫?璧扮涓夋

### 绗簩姝ワ細鏍规枃浠剁郴缁燂紙1鈥? 鍛級

渚濇嵁 `/guide/userdata` + `/concepts/userdata`锛?
```
1. board.toml 鐨?[ipsw] fetch 鍔?"OS" 鍜?"Cryptex1,SystemOS"   鈫?宸插姞锛屾湭楠岃瘉
2. ./unixnu ipsw fetch          # 鎷変袱涓粍浠讹紝鍑?GB
3. ./unixnu build userdata      # SHNGROOT manifest + 涓や釜绐楀彛
4. [payload.adt] 璁?root_match_volume_uuid = <OS 鍗风殑 UUID>
5. fastboot flash userdata out/vince/userdata/userdata-root.img
6. 瑙傚療鏄惁鎸備笂銆乴aunchd 鏄惁璧锋潵
```

**宸茬煡**锛歚[userdata]` 鐨?LBA 鏃╁疄娴嬪ソ锛坄first_lba = 0x288C40` /
`last_lba = 0x77BF3FA` / `lba_bytes = 4096`锛夈€?
### 绗笁姝ワ細鏄剧ず锛?鈥? 鍛紝鍙湪绗簩姝ヤ箣鍚庯級

鐓?`UniXNU-sheng`锛氳嚜鐮?`IOCoreSurfaceRoot` + `AppleCLCD`锛屾敞鍐岃繘
`iokit/KernelConfigTables.cpp`锛屽苟鍦?platform expert 閲岀粰 `arm-io` 瀛愯妭鐐瑰缓 nub銆?
**涓嶈鍏堝仛杩欎竴姝?* 鈥斺€?瀹冭В鍐炽€岀湅涓嶇湅寰楄銆嶏紝涓嶆槸銆岃捣涓嶈捣寰楁潵銆嶃€?
---

## 鍏€佸弬鑰冪墿

| 鍙傜収 | 鐢ㄩ€?|
|---|---|
| **`UniXNU-sheng`** | **鍞竴姝ｇ‘鐨勫弬鐓?*锛歳oots / archives / defconfig 瀹屾暣渚嬪瓙 |
| `UniXNU/UniXNU` | 妗嗘灦鏈綋锛涙垜浠殑 fork 钀藉悗 163 commit锛屼笖涓嶈兘鐩存帴鎹紙`-mach_msg2`锛墊
| `glebenekt/ios-vince` | 鍚岃澶囥€乮PadOS 16.6.1銆?3 琛ヤ竵鍒?SpringBoard |
| `unixnu.com` | 瀹樻柟鏂囨。 |

**鏂囨。鐨勪袱涓瀵肩偣**锛堣俯杩囷級锛?1. `/guide/debugging` 鎶?`boot-progress` 鍐欐垚閫氱敤鍔熻兘锛屽疄涓?sheng 涓撳睘 136 KB
2. `macos-26` 闀滃儚涓?*娌℃湁** Xcode 26.6锛屽彧鏈?26.0 / 26.0.1

---

## 涓冦€佸伐鍏锋竻鍗?
| 宸ュ叿 | 鐢ㄩ€?|
|---|---|
| `C:\Temp\auto\watch.ps1` | 涓€鍒嗛挓杞鏋勫缓 |
| `C:\Temp\payload2.sh` | 鎵撳寘 payload锛?*娉ㄦ剰**锛氭墜鍔ㄨ皟 `make-vince-adt.py`锛岀粫杩囧畼鏂?`build payload`锛墊
| `C:\Temp\auto\shot.ps1` | QEMU 鍚姩 + 鎴浘 |
| `C:\Temp\findsym.py` | 鍐呮牳绗﹀彿鍙嶆煡 |

**QEMU 鍙傛暟锛堢己涓€涓兘涓嶈锛?*锛?```
-M virt -cpu max -m 8192 -smp 1
-drive if=pflash,...,file=edk2-aarch64-code.fd
-drive if=none,id=esp,...,file=fat:<ESP鐩綍>
-device virtio-blk-pci,drive=esp -device ramfb
-display none -serial file:<log>
```
`-cpu max`锛坈ortex-a72 涓嶈 `MSR S3_0_C4_C1_4`锛夛紱`-m 8192`锛?096 鏃?DarwinBoot 鎶?`Out of Resources`锛夈€?
---

## 鍏€佹枃浠跺湴鍥?
| 鏂囦欢 | 浣滅敤 |
|---|---|
| `board.toml` | 鏉跨骇閰嶇疆锛歱relink roots / archives / userdata / payload |
| `configs/vince_defconfig` | 9 涓紑鍏筹紙**鍒贡鍔?*锛墊
| `patches/xnu/*.patch` | 鍐呮牳琛ヤ竵锛屾寜鍚嶅瓧鎺掑簭搴旂敤 |
| `.github/workflows/build-kernel.yml` | CI锛?7 姝ワ紝鍚?`build payload`锛墊
| `STATUS.md` | 褰撳墠鐘舵€佸揩鐓?|
| `FLOW.md` | 娴佺▼鍥撅紙涓冮樁娈?+ 涓ゆ潯璺嚎锛墊
| `HANDOVER-legacy.md` | 鏃╂湡璺緞锛堟帰閽堟柟妗堟潵鍘嗭級|

**澶栭儴渚濊禆**锛?- `C:\Users\Administrator\Documents\UniXNU` 鈥?`UniXNU` 浠撳簱鏈湴 clone锛?*CI 瀹為檯鐢ㄧ殑鏄畠 push 鍒?fork 鐨勭増鏈?*锛堣繖鐐瑰緢閲嶈锛氭敼鏈湴涓?push锛孋I 鐪嬩笉鍒帮級
- `C:\Users\Administrator\Desktop\unixnu-vince-kernel-ufs` 鈥?payload 涓?boot image 宸ヤ綔鐩綍

---

## 涔濄€佹柊绐楀彛鐨勭涓€鏉″懡浠?
```powershell
cd C:\Users\Administrator\Documents\unixnu-vince-gh
git log --oneline -10
Get-Content STATUS.md | Select-Object -First 60
gh run list --repo Lux12138/unixnu-vince --limit 3 --workflow build-kernel.yml
```

**鐒跺悗浠庣浜旇妭绗竴姝ュ紑濮嬨€?*

