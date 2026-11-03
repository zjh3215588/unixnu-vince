# UniXNU on Xiaomi Pad 5 (vince / SM8150)

鍦?**灏忕背骞虫澘 5锛坣abu锛岄獊榫?860 / SM8150锛?* 涓婇€氳繃 UEFI 鍚姩 **鑻规灉 XNU 鍐呮牳** 鐨勫畬鏁寸Щ妞嶈褰曘€?
> **鏈粨搴撹褰曠殑鏄€屾帹鍊掗噸鏉ャ€嶄箣鍓嶇殑閭ｆ潯绾裤€?* 褰撳墠瀹為檯鐘舵€併€佷互鍙婃棫鏂囨。閲屽凡缁忓け鏁堢殑璇存硶锛?> 瑙?[`CURRENT-STATE.md`](CURRENT-STATE.md)锛涗笌鏃ф枃妗ｅ啿绐佹椂**浠ュ畠涓哄噯**銆?
> **鏈満鏄墿瀹圭増**锛氱墿鐞?DRAM **12 GiB**锛圱WRP 瀹炴祴 `MemTotal = 11766512 kB`锛?> 鍗?12 GiB 鍑忓幓绾?816 MB 缁?modem/hyp/rmtfs锛夛紝userdata **绾?468 GiB**
> 锛坄fastboot partition-size:userdata = 0x74167BB000`锛夈€?> 鎵€浠?`dram_size = 0x300000000` 鏄?*涓鸿繖鍙版満鍣ㄦ祴鍑烘潵鐨?*锛屼笉鏄爣鍑?6/8 GB 鏈哄瀷鐨勬暟瀛椼€?
> **鐘舵€侊紙2026-10-28锛屼互姝や负鍑嗭級**锛?*鐢ㄦ埛鎬佸凡缁忚窇璧锋潵浜嗐€?*
>
> - 鏍瑰嵎 + launchd 宸查€氳繃锛氬畬鏁村惎鍔ㄦ棩蹇?**146 KB / 2,032 琛?*锛堜笌鑷姩澶嶄綅鍚屼竴杞彇寰楋級锛?> - runningboardd / backboardd / SpringBoard 閮藉湪杩愯锛屽悇鑷湪鑷繁鐨?mqueue 涓婄瓑娑堟伅
>   锛坄[hb] tag=chk n=68 sb=1 bb=1 rb=1 cfg=1`锛夛紝keybagd 璧?>   `DEVICE HAS EPHEMERAL DATA VOLUME, SKIP INIT`锛?> - 鏄剧ず锛歚[nm] mask=7 size=1336 init=1`锛堜笁涓娊璞″熀绫?*鍚嶅瓧**涓嶅彲瀹炰緥鍖栵紝
>   `IOMobileFramebufferUserClient` 鍙垎閰嶄笖 init 鎴愬姛锛夛紱杩愯鏈熷敮涓€鏄剧ず鐩稿叧澶辫触鏄?>   `[ex] pid=26 comm=IOMFB_FDR_Loader rv=0x100 sig=0 code=1`銆?*缂虹殑鏄竴涓?provider 瀹炰緥**锛?> - 姣忚疆宸叉棤浜哄€煎畧锛?6~129 s 璺戝畬涓€杞€侀浂鎸夐敭锛圕DC 鎺у埗閫氶亾 + WDT 瀹氭椂鍋滆溅鐨勭粏鑺傝
>   鍏紑浠撳簱 [`vince-usb-cdc`](https://github.com/Lux12138/vince-usb-cdc) 鐨?`docs/07`锛夈€?>
> **鍘嗗彶鐘舵€侊紙2026-10-25锛屽凡琚笂闈㈠彇浠ｏ級**锛氬唴鏍告墽琛屽埌 `execve("/sbin/launchd")`锛?> `Process 1 exec of /sbin/launchd failed, errno 2`锛涘綋鏃剁己鐨勬槸瑁呬簡绯荤粺鏂囦欢鐨勬牴鏂囦欢绯荤粺銆?
---

## 涓€銆侀噷绋嬬锛氬唴鏍歌蛋鍒颁簡 launchd

**灞忓箷璇佹嵁**

```
Process 1 exec of /sbin/launchd failed, errno 2
/sbin/launchd
kern_exec.c

FAR=18446744042837921792
PC=18446744005117767160
LR=18446744005111703156
```

**瀹屾暣閾捐矾**

```
bsd_autoconf()                            OK
  kminit()                                OK
    IOsurfaceRoot::installMemoryRegions() OK   <- 鏇捐璇涓哄崱鍦ㄨ繖閲?bsd_init 鍚庡崐娈?                          OK
  vfs_mountroot()                         OK
  load_init_program()                     OK   <- 瑙ｆ瀽鍑?/sbin/launchd
    execve("/sbin/launchd")               errno 2 (ENOENT)
```

**`errno 2` 鏄枃浠朵笉瀛樺湪锛屼笉鏄唴鏍告晠闅溿€?*

### 鏇剧粡璇垽浜嗕笁澶?
`IOsurfaceRoot::installMemoryRegions()` 閭ｄ竴琛?*浠庢潵涓嶆槸缁堢偣锛屽彧鏄渶鍚庝竴鏉?kprintf**銆?瀹冧箣鍚庣殑 `dtrace_postinit()`銆乣inittodr()`銆佹潯浠剁紪璇戠殑缃戠粶鍒濆鍖?*鍏ㄩ兘涓嶆墦鏃ュ織**锛?浜庢槸銆屾棩蹇楀仠姝€嶈璇绘垚浜嗐€屽唴鏍稿仠姝€嶃€?
鐪熸缂虹殑涓€鐩存槸涓€涓牴鏂囦欢绯荤粺銆?
---

## 浜屻€佸惎鍔ㄩ摼锛堢湡鏈洪獙璇侊級

```
fastboot boot -> Mu UEFI -> UniXNU 鑿滃崟 -> cust 鍒嗗尯 payload
-> DarwinBoot -> 璇?51MB 鍐呮牳 -> 瑙ｆ瀽 Mach-O -> ADT 鏍￠獙
-> 鍒嗛厤绐楀彛 -> 鏄犲皠娈?-> ExitBootServices -> 璺宠浆 XNU -> 鍐呮牳鎵ц
```

鍏抽敭鏃ュ織锛?
```
UNIXNU: runxnu entry vol=A2142798 path=\EFI\UniXNU\Payloads\kernel.macho cfgerr=[]
DB1 kernel read  Success size=53760000
DB2 kernel parse Success
DB3 adt read     Success size=13188
DB4 adt ok  win=120000000 keep=0 rd=ffffffffffffffff
DB arm64 va=0xfffffff007ac2000 pa=0x80070000 owned=0x120000000 window=0x30000000
video base=0x... width=2560 depth=32 bpp
DARWINBOOT: EL1 installed
DARWINBOOT: inputs validated; exiting boot services
still-there kernel entry code ran
DARWINBOOT: hand-off to the kernel
```

---

## 涓夈€佹湰鍦?Linux 鏋勫缓锛?2 绉掍竴杞級

鍐呮牳鐜板湪鑳藉湪鏈湴 WSL Ubuntu 24.04 涓婄紪璇戯紝**72 绉?*涓€杞紝瀵圭収 GitHub macOS runner 鐨?15鈥?7 鍒嗛挓銆?
| 椤?| GitHub macOS runner | 鏈湴 WSL Ubuntu |
|---|---|---|
| 鍗曡疆鏋勫缓 | 15鈥?7 鍒嗛挓 | **72 绉?* |
| 浜х墿 | 49.2 MB | **49 MB** |
| 鍙鐜?| 鍙兘闈?CI | 鏈満闅忔椂璺?|

**浜х墿楠岃瘉**

```
file            Mach-O 64-bit arm64 executable, flags:<NOUNDEFS|PIE>
__TEXT vmaddr   0xfffffff007004000      涓庡師鐗?kernelcache 涓€鑷?symbols         22708
vince 鎺㈤拡       vince_mark / vince_mark_map / vince_mark_num / vince_mark_putc
UFS 鎺㈡祴        vince_ufs_register_probe.cpp
sha256          c756ecdb88a9dd50156dc27d2cdf48a08ddf93fcf204040fa57804f814fc3c15
```

宸ュ叿閾炬潵鑷?[`Allenwdk/xnu-linux-toolchain`](https://github.com/Allenwdk/xnu-linux-toolchain)銆?
### 鎵撻€?Linux 鏃惰俯鐨?18 涓潙

| 绫诲埆 | 鏁伴噺 | 渚嬪瓙 |
|---|---|---|
| 宸ュ叿閾剧己澶?| 8 | `libdispatch` 鏃?Ubuntu 鍖咃紱`hostcompat.h` / `libc.h` / `copyfile.h` / `setmode` 鍏ㄩ渶鑷啓 |
| 璺緞纭紪鐮?| 5 | `/usr/bin/xcrun`銆乣/usr/sbin/sysctl`銆乣compression_tool`銆乣dsymutil`銆乣lzfse` |
| BSD vs GNU | 3 | `sed -i ''`銆乣awk \(`銆佹湭鐭?`-Wno-*` |
| 閫昏緫鍐茬獊 | 2 | mockfs 鍙岄噸閾炬帴锛?3 涓噸澶嶇鍙凤級銆乣TargetConditionals.h` 閲嶅 |

**鏈€鏈変环鍊肩殑涓€涓?*锛歚makesyscalls.sh` 閲?`printf("\t{ \(sy_call_t *\)...")` 鈥斺€?**BSD awk 鎶?`\(` 褰撹浆涔夛紝gawk 淇濈暀鍙嶆枩鏉?*锛孡inux 涓婄敓鎴愮殑 `init_sysent.c` 鍏ㄦ槸
`\(sy_call_t *\)`锛岀紪璇戝櫒鎶ヤ竴鐗?`expected expression`銆傚仛鎴?patch锛坄zzzz-vince-awk-parens.patch`锛夛紝
鍥犱负 `unixnu tree` 姣忔閮介噸寤?`.cache`锛屾墜宸ユ敼浼氳瑕嗙洊銆?
---

## 鍥涖€佹牴鏂囦欢绯荤粺锛?-Zip 鐩存帴瑙ｏ紝涓嶇敤 hdiutil

`build userdata` 鍦?Linux 涓婂崱鍦?`hdiutil`銆備笉鐢ㄨ嚜宸卞啓 UDIF 瑙ｆ瀽鍣?鈥斺€?**7-Zip 23.01 鍘熺敓鏀寔 DMG + LZFSE**锛岀洿鎺ヨВ鍑哄畬鏁?iOS 鏂囦欢绯荤粺锛?
```bash
sudo apt-get install -y p7zip-full
7z x -y -o/tmp/dmgout 044-76040-038.dmg
```

瀹炴祴缁撴灉锛?
```
/sbin/launchd   561,856 bytes   Mach-O 64-bit arm64 executable
                               flags:<NOUNDEFS|DYLDLINK|TWOLEVEL|PIE>

9.7 GB / 210,828 涓枃浠?  8.1G  System
  713M  usr
  483M  private
  313M  Applications
  139M  Library
  960K  sbin
```

**娉ㄦ剰**锛歚dmg2img 1.6.7` **涓嶆敮鎸?LZFSE**锛屼細鎶?`Unsupported or corrupted block found: -2147483641` 骞惰緭鍑烘畫鍍忋€傜敤 7-Zip銆?
`7z l -slt` 鑳界洿鎺ョ湅鍑哄帇缂╂柟寮忥細

```
Method = Copy Zero2 LZFSE CRC
Path   = 3.apfs
Size   = 6077546496         5.66 GiB
Type   = APFS
Name   = DawnUpdate21H461.J120J121J207J208OS.apfs
num_files: 165509
```

---

## 浜斻€佸叚閬撶‖鍧戜笌瑙ｆ硶锛堢収杩欎釜椤哄簭韪╋紝鑳界渷鍑犲ぉ锛?
### 鍧?1锛歚fastboot boot` 鎶?`Failed to load/authenticate boot image: Load Error`

**涓嶆槸** 瀹樻敼 ABL 绂佺敤 boot锛?*鏄?USB 绾?*銆?
- 鍔ｈ川鍏呯數绾夸細璁?96MB 绾ч暅鍍忎紶杈撲涪鏁版嵁 -> ABL 鏍￠獙澶辫触
- 鎹㈠師瑁呮暟鎹嚎 + 鎻掍富鏉垮悗闈㈡澘 USB 鍙ｅ悗锛屽悓涓€闀滃儚绔嬪埢 `Booting OKAY`

### 鍧?2锛歳amdisk 澶у皬鏈変笂涓嬮檺

| ramdisk | ABL | UEFI |
|---|---|---|
| 16 MB | Load Error | 鈥?|
| 32 MB | OK | 鑿滃崟姝ｅ父 |
| 64 MB | OK | 鑿滃崟姝ｅ父 |
| 96 MB | OK | 榛戝睆 |

鍙敤鍖洪棿 **32鈥?4MB**锛沗header_version = 1`锛宍page_size 2048`銆?
### 鍧?3锛歚fastboot boot` 鍓嶅厛閲嶅惎璁惧

璁惧姣忔閲嶅惎鍚?*绗竴娆?boot 鎴愬姛鐜囨渶楂?*锛涜繛缁?boot 浼氬嚭鐜?Load Error锛坉ownload buffer 鐘舵€佹畫鐣欙級銆?
### 鍧?4锛氭妸鍐呮牳濉炶繘鍥轰欢鍗疯蛋涓嶉€氾紙PEI 瑙ｅ帇棰勭畻锛?
| FVMAIN 澶у皬 | 缁撴灉 |
|---|---|
| 8 MB锛堝師濮嬶級 | 鍥轰欢姝ｅ父 |
| 62 MB锛堟湭鍘嬬缉鍐呮牳锛?| 鍥?fastboot |
| 15 MB锛圠ZMA 鍘嬬缉鍐呮牳锛?| 鍥?fastboot |

FVMAIN 涓婇檺绾?8鈥?0MB锛汧D 鏈韩涔熸湁涓婇檺銆?*鍐呮牳涓嶈兘璧?boot.img 鍐呮牳娈碉紝鍙兘璧板瓨鍌ㄣ€?*

### 鍧?5锛氭病鏈変换浣?FAT 鐩橈紙鏈€鏍规湰鐨勪竴涓級

鍥轰欢鍏跺疄鑷甫瀹屾暣瀛樺偍鏍堬紙`UFSDxe` / `PartitionDxe` / `DiskIoDxe` / `Fat`锛夛紝
浣嗗畨鍗撳垎鍖哄叏鏄?ext4/f2fs锛孶niXNU 鏋氫妇涓嶅埌浠讳綍甯?`unixnu.toml` 鐨勫嵎銆?
### 鍧?6锛欰DT 閲岀殑 DRAM 蹇呴』鏄疄娴嬪€?
```
dram-size               = 0x300000000   12 GiB锛堟湰鏈烘墿瀹癸級
darwinboot-memory-size  = 0x20000000    512 MiB 杩炵画绐楀彛
```

`darwinboot-memory-size` 鏄?DarwinBoot 鍚戝浐浠惰鐨勪竴鍧?*杩炵画**鐗╃悊鍐呭瓨銆?512 MiB 瓒冲锛涙洿澶х殑鍊兼洿闅句粠 `EfiConventionalMemory` 閲屾壘鍒拌繛缁尯闂淬€?
---

## 鍏€佷笅涓€姝ワ紙2026-10-28 鏇存柊锛?
**鍞竴纭樆濉烇細缁?`IOMobileFramebuffer` 鎻愪緵涓€涓?provider 瀹炰緥銆?*

鍏朵綑宸插叏閮ㄥ湪鏉夸笂璺戦€氾紙瑙佹枃棣栫姸鎬侊級銆傚綋鍓嶄笁鏉″緟鍔烇紝鎸夊垽鍒姏鎺掑簭锛?
1. ~~鎶?`mask=7` 鐨勬涔夊畾姝粇~ 鈥斺€?**宸插畾妗?*锛歚[nm] reg=0x7` 璇存槑涓変釜鍩虹被閮藉凡娉ㄥ唽锛?   `mask=7` 鍙槸鈥滃畠浠槸鎶借薄绫烩€濈殑琛ㄧ幇銆?2. **缁?`AppleDPDisplay` 閰嶄竴涓兘鍖归厤鐨勮澶囪妭鐐?*锛歚AppleCLCD` 涓嶅湪 iPadOS 鐨?   kernelcache 閲岋紝鏄剧ず渚х湡韬槸 `com.apple.driver.AppleDPDisplay`锛堝尮閰?`lcd,edp`锛夛紝
   瀹冨凡琚疄娴嬭兘鍔犺浇骞舵敞鍐岋紙`[nm] late load=0 reg2=f`锛夛紱杩樺樊璁惧鏍戦噷鍖归厤鐨勮妭鐐?   锛堢ぞ鍖烘槸鑷€?`/arm-io/disp0`锛夛紝鎵嶄細 attach 鍑?provider 瀹炰緥銆?   鑷啓 `IOMobileFramebuffer` 瀛愮被閭ｆ潯璺凡鍦ㄩ摼鎺ユ湡琚惁璇侊紙缂?`gMetaClass` / ctor / dtor锛夈€?3. **鎶娾€滃挰鍚?= 姝﹁鍚庣害 32 s鈥濅粠鎺ㄦ柇鍙樻垚瀹炴祴**锛氭妸 `--capture` 鏀鹃暱鍒拌鐩栧浣嶇偣锛?   鐢ㄧ湡瀹炵殑 `USB LOST at` 鏃堕棿鎴冲畾銆?
> **鍘嗗彶锛?026-10-25 鐨勪笅涓€姝ワ紝宸插彇浠ｏ級**锛氭妸瑙ｅ嚭鏉ョ殑鏍瑰仛鎴愪竴涓兘鎸傜殑鍗?> 锛坄./unixnu build userdata` + `fastboot flash userdata`锛夈€傜幇鍦ㄦ牴鍗疯蛋 APFS +
> **vincevar**锛堝唴瀛樺嵎鎸?`/private/var`锛夛紝涓嶅啀闇€瑕佸埛 userdata銆?
---

## 涓冦€佸弬鑰?
- [`Allenwdk/xnu-linux-toolchain`](https://github.com/Allenwdk/xnu-linux-toolchain) 鈥斺€?Linux 浜ゅ弶宸ュ叿閾?- [`1PJL/unixnu-vince`](https://github.com/1PJL/unixnu-vince) 鈥斺€?UFS 鍗疯瘖鏂郴鍒楋紙`Recover GPT` / `Build Volume` / `Repack` 涓夋锛岃窇鍦?`ubuntu-24.04` 涓婏級
- `UniXNU` 涓婃父 鈥斺€?鍐呮牳绉绘涓?UEFI 鍚姩閾?
