# 浜ゆ帴鏂囨。 鈥?2026-10-24 鏅氾紙鍥炴粴涔嬪锛?
> 鍐欑粰涓嬩竴涓帴鎵嬬殑浜猴紙鎴栨垜鑷繁锛夈€?*鍏堣杩欒妭鍐嶅姩鎵嬶紝鍚﹀垯浼氶噸韫堟垜浠婂ぉ鐨勮杈欍€?*

## 0. 褰撳墠鐘舵€佷竴鍙ヨ瘽

璁惧鍋滃湪 `unexpected SIGKILL of launchd` panic 鈥斺€?涓庢槰澶╁畬鍏ㄧ浉鍚岀殑鍩虹嚎銆?涓や釜浠撳簱宸插洖婊氬埌宸茬煡鑹ソ鐗堟湰锛屽唴鏍?md5 `e9ebb7e6鈥锛?7:41 鏋勫缓锛夛紝宸插埛鏈洪獙璇併€?
---

## 1. 纭欢涓庡惎鍔ㄩ摼锛堜笉鍙橈級

- **灏忕背 Pad 5 (vince / SM8150-AC / 楠侀緳860)**锛宻erial `f91fa664`锛?2 GiB 鎵╁鐗?- 鍚姩閾撅細`fastboot boot vince-xnu64-Z.img` 鈫?BootShim 鈫?Mu UEFI 鈫?UniXNU 鑿滃崟
  鈫?**cust 鍒嗗尯 payload** 鈫?DarwinBoot 鈫?XNU
- 鍐呮牳锛歺nu-10063.141.1锛宍KERNEL_CONFIGS=DEVELOPMENT`锛宍MACHINE_CONFIGS=BCM2837`
- ADT boot-args锛堝敮涓€鐢熸晥鐨勪竴濂楋紝`make-vince-adt.py:135`锛夛細
  `-enable_kprintf_spam native-ufs-root=1 native-ufs-diagnostics=1 maxmem=4864 amfi_get_out_of_my_way=1 cs_enforcement_disable=1 amfi_allow_any_signature=1`
- 灞忓箷 1600脳2560锛宑onsole 涓婇檺 1780锛涙帰閽堝繀椤?鈮?0px 琛岃窛銆侀伩寮€ <1780 琛?
## 2. 浠撳簱鐘舵€侊紙鍏ㄩ儴宸叉帹閫侊紝杩滅宸插己鍒舵寚鍥烇級

| 浠撳簱 | HEAD | 鍐呭 |
|---|---|---|
| `Lux12138/UniXNU` | **`aae83c4`** | 绾帰閽堢増锛歳eason creator 鎺㈤拡锛圧N=/RA=锛屾爣绛惧甫 `=` 鍒嗛殧锛夈€佸叏閮ㄨ瘖鏂帰閽堛€?*鏃?DWC3銆佹棤閲嶅惎璋冪敤** |
| `Lux12138/unixnu-vince` | **`24b73bc`** | board.toml锛堝惈 trust_cache=true锛夈€乨efconfig銆佸叏閮ㄤ氦鎺ユ枃妗ｏ紙HANDOVER-exec-fault.md 689 琛岋級 |
| `Lux12138/NativeDwc3` | `e2501a8` | **鐙珛鐨?USB 椹卞姩浠撳簱**锛堜粖澶╂柊寤猴級銆傚凡楠岃瘉鑳界紪璇戦摼鎺ワ紝浣嗗洜缂?GCC 鏃堕挓闂ㄦ帶浼氬穿婧?鈥斺€?**涓嶈鎺ュ洖 board.toml**锛岄櫎闈炲厛鍋?GccUsb |
| `Lux12138/xnu-linux-toolchain` | `1270e1b` | 涓婃父 `Allenwdk/xnu-linux-toolchain` 鐨?fork锛岃ˉ浜?`zzzz-vince-awk-parens.patch` + `docs/vince-18-PITFALLS.md` |

**鍥炴粴鏃剁殑鍏抽敭鏁欒锛歎niXNU 鍜?unixnu-vince 蹇呴』涓€璧峰洖婊氥€?* 鍙洖婊氫竴涓紝board.toml 閲岀殑
`build-arm-driver.py NativeDwc3` 浼氳 archive 8 姣忚疆澶辫触 鈫?`KERNEL NOT REGENERATED` 鈫?鍒风殑鏄棫鍐呮牳娈嬬暀锛岃€屼綘浠ヤ负鏀瑰姩浜嗐€?
## 3. 浠婂ぉ鎼炴竻妤氱殑浜嬪疄锛堝叏閮ㄥ疄娴嬶紝鍙洿鎺ュ紩鐢級

### 3.1 涓荤嚎闂鐨勮繘灞?
| 闂 | 缁撹 |
|---|---|
| execve 缂洪〉 panic | 鉁?**宸蹭慨澶?*锛圥AC锛歚find_copyio_recovery_entry` 灏戜簡 `VM_KERNEL_STRIP_PTR`锛夈€俙PCOF` 浠?`0x230397`鈫抈0x2b7027`锛岃惤鍦ㄨ〃椤?9 |
| `vm_page_free_count` 91M | 鐥囩姸闈炲師鍥狅紝`dram_size`/`owned_memory_size` 涓嶈鍔?|
| AMFI boot-args | `AMx=10` 鈫?AMFI=1 瑙ｆ瀽鎴愬姛锛宍CS_KILLED=0`锛?*涓嶆槸绛惧悕闂** |
| SIGKILL 鐨?reason | **`SIG900008` = `OS_REASON_EXEC`(9) + `EXEC_EXIT_REASON_SECURITY_POLICY`(8)**锛屼氦浠樼偣瀹炴祴 `SN9 SC8 SU0` |
| 涓冧釜 reason 鐢熶骇鑰?| 鍏ㄩ儴鎺掗櫎锛歀8019 闇€ `ip_mac_return鈮?`锛圠U 浠庢湭鐢诲嚭锛夛紱L7950 鐨?`custom x18 ABI` 瀛楃涓?0 娆★紱L8059/69 鏄?WRONG_PLATFORM(14)锛汱8097/121/128 鏄?CODESIGNING(3) 鎴?TASKGATED_OTHER(9)锛沗ip_cs_error` 涓や釜澶栭儴婧愰兘鏄?CODESIGNING(3) |
| trust cache | 鉁?宸叉帴鍏ワ細56 瀛楄妭鏂囦欢锛坙aunchd cdhash `1d52c69747dffc4b1937d241bdbc9cee3b22df18`锛夊唴宓?base64 鍦?`make-cust-payload.sh`锛孉DT 鏈?`TrustCache` 鑺傜偣銆傞€氳繃 DarwinBoot `ValidTrustCaches` 鍏ㄩ儴瑙勫垯銆?*浣嗘病瑙ｅ喅 SIGKILL** 鈥斺€?鍥犱负 `load_static_trust_cache()` 闇€瑕?AMFI 鎺ュ彛锛岃€?`_amfi == NULL`锛堟病鏈?AppleMobileFileIntegrity kext锛?|

### 3.2 浠婂ぉ鐨勬柊鍧戯紙姣忎釜閮界儳浜嗘垜鑷冲皯涓€杞級

1. **鎺㈤拡琛屽彿鍐茬獊**锛歚LU`(2500) 琚?`SIG`(2500) 瑕嗙洊銆乣KR`(2340) 琚?`PN2` 瑕嗙洊銆乣EM`(2420) 琚?`IOFindBSDRoot` 瑕嗙洊銆?*"娌℃樉绀? 鈮?"娌℃墽琛?**锛屽厛鏍稿琛屽彿琛ㄣ€?2. **璇诲睆閿欒**锛歚PN2`+`9` 杩炴帓璇绘垚 `PN29`锛宍PC3`+`8` 璇绘垚 `PC38`銆?*宸茬粰鎵€鏈夋爣绛惧姞 `=` 鍒嗛殧绗?*锛坄RN=`/`RA=`锛夛紝浠ュ悗璇诲浘鍏堟寜鏍囩琛ㄥ垏鍒嗐€?3. **`__builtin_return_address(0)` 鍦?`-O2` 涓嬩笉鍙潬**锛歚RA=124812296` 鍥哄畾鍨冨溇锛圠R 琚紪璇戝櫒澶嶇敤锛夈€?*杩欐潯瀹氫綅璋冪敤鑰呯殑璺綔搴?*銆?4. **`ios-obj` 缂撳瓨鎹熷潖 鈫?鏋勫缓闈欓粯涓嶄骇鍑烘柊鍐呮牳**銆傜棁鐘讹細鍐呮牳 mtime 涓嶅彉銆乣strings` 鏌ヤ笉鍒版柊鏍囩銆?*鍞竴鎭㈠鎵嬫锛歚rm -rf out/vince/tree/build/xnu/ios-obj` 鍏ㄩ噺閲嶅缓**銆?5. **xnu C++ 浜х墿鏄?`.cpo/.cpd` 涓嶆槸 `.o`**锛涘垹 `.cpo` 浼氱牬鍧?link.filelist锛屽垹 `.o` 浼氫涪澶卞璞°€?*姝ｇ‘鍋氭硶鏄妸婧愭枃浠跺姞杩?build_verify.sh 鐨?缂撳瓨鍒犻櫎娓呭崟"**锛堢害 L54 鐨?find 鍧楋級銆?6. **鏀?`scripts/*.py` 蹇呴』 push**锛歚build_verify.sh` 姣忚疆 `git fetch + reset --hard FETCH_HEAD`锛屾湰鍦版湭鎻愪氦鐨勬敼鍔ㄤ細琚啿鎺夈€?*浣?`git push` 浼氬亣鎴愬姛**锛堣涓嬫潯锛夈€?7. **git push `exit=0` 浣嗚繙绔病鏇存柊**锛堣瑙?`PUSH-GOTCHA.md`锛夈€?*鍞竴鍙潬鐨勯獙璇?*锛?   ```bash
   git fetch -q origin main
   git show origin/main:<file> | grep -c '<鍏抽敭鏀瑰姩>'
   ```
   鎴栬€呭共鑴嗙敤 **GitHub API PUT contents**锛堢鍥烇紝浠庢湭澶辫触锛夈€?8. **楠岃瘉蹇呴』閫?搴斿綋瀛樺湪"鐨勫垽鎹?*銆傛垜鏇炬嬁 `vince RESTART: 0` 褰?鎾ら櫎鎴愬姛"鈥斺€斾絾閭ｄ釜瀛楃涓?*浠庢病杩涜繃鍐呮牳**锛? 鏄亽鐪熺殑銆傛纭垽鎹簲鏄?md5 鍙樺寲 + 搴斿瓨鍦ㄧ殑瀛楃涓?count>0銆?9. **`PEHaltRestart` 涓嶈兘鍦?early-boot 闃舵瑁歌皟**锛歚os_reason_create` 閲岃皟鐢?鈫?`Kernel data abort`锛孎AR=0锛屽穿鍦?`Initializing serial KDP` 涔嬪悗銆俙PE_halt_restart` 鍑芥暟鎸囬拡瑕佺瓑骞冲彴涓撳鍒濆鍖栧悗鎵嶅氨缁€傦紙涓嶈繃褰撴椂鐪熸宕╂簝婧愭槸 DWC3锛岃涓嬫潯鈥斺€旇繖涓粨璁哄緟閲嶆柊楠岃瘉锛?10. **DWC3 椹卞姩鏈厤鏃堕挓灏辨槧灏勫苟鍐?`0x0A600000` 鈫?鏃╂湡 data abort**銆傚睆骞曠壒寰侊細`Kernel data abort.`锛宍ESR=2516582405`锛宍FAR=0`锛孭C 鍦?`0xfffffff01167xxxx`锛屽仠鍦?`Initializing serial KDP` 涔嬪悗銆丼kywalk 鑷祴涔嬪墠銆?*杩欏氨鏄粖澶╅偅涓ゆ"鑾悕鍏跺"宕╂簝鐨勭湡鍑躲€?*

### 3.3 DWC3 椹卞姩鐨勭幇鐘讹紙`Lux12138/NativeDwc3`锛?
宸插畬鎴愮殑锛氬瘎瀛樺櫒澶达紙涓ユ牸鐓?Android `dwc3/core.h` 杞綍锛夈€乻tage-1 `start()`锛坢ap 鈫?GSNPSID 鈫?杞浣?鈫?device mode 鈫?娓?SUSPHY 鈫?RUN_STOP 鈫?璇?DSTS锛夈€両nfo.plist銆丄DT 鐨?`usb0` 鑺傜偣銆佹瀯寤洪摼鍏ㄦ墦閫氾紙鐧藉悕鍗?+ 鐩綍鏄犲皠 + force_load + config name锛夈€?
**鍗′綇鐨勫湴鏂癸紙涓嬩竴姝ヤ粠杩欓噷寮€濮嬶級**锛?1. `CONFIG_XNU_NATIVE_DWC3=y` 浼犱笉杩?`build-xnu-4k-baseline.sh`锛堝疄娴?`XNU_NATIVE_DWC3=UNSET`锛夈€俷abu 鐨勬瀯寤哄叆鍙ｄ笉璧?`build-cpu-desktop-kernel.py` 鐨?names 琛ㄣ€?*闇€瑕佹壘鍒?vince 鐪熸鐨?env 娉ㄥ叆鐐?*锛堝彲鑳藉湪 `unixnu` 鐨?kernel.py 鎴?board.toml 鐨?env 娈碉級銆?2. **缂?GCC 鏃堕挓闂ㄦ帶**锛氬嵆浣块摼鎺ユ垚鍔燂紝鍐欏瘎瀛樺櫒涔熷穿銆傞渶瑕佺収鎶?`NativeUfs/GccUfs.h` 鍐?`GccUsb.h`锛屽厛寮€ `GCC_USB30_PRIM_*` 鍏釜鏃堕挓 + GDSC锛屽啀纰?DWC3 瀵勫瓨鍣ㄣ€係M8150 鐨?GCC 鍩哄潃鍜?UFS 鐩稿悓锛堝悓涓€ GCC 鍧楋級锛宐it 浣嶄粠 `gcc-sm8150.h` 鏌ャ€?3. `IOProviderClass=IOPlatformDevice` 闇€瑕佸尮閰?ADT 鑺傜偣 鈥斺€?`usb0` 鑺傜偣宸插姞锛坄make-vince-adt.py:190`锛夛紝浣?*娌￠獙璇佽繃 IOKit 鏄惁鐪熺殑鍖归厤骞惰皟鐢ㄤ簡 start()**锛堝綋鏃跺穿婧冩帺鐩栦簡杩欎竴鐐癸級銆?
### 3.4 鑷姩璇绘棩蹇楁柟妗堢殑瀹氳

| 鏂规 | 缁撹 |
|---|---|
| fastboot fetch 鍒嗗尯 | 鉂?瀹炴祴 `Device does not support fetch command` |
| xnu 鑷甫 UART | 鉂?鍏ㄦ槸 Apple 涓撴湁瀹忥紙APPLE_UART/DOCKCHANNEL/VMAPPLE锛夛紝涓旈渶 ADT 鑺傜偣锛泂heng 涔熸病鍋?|
| 鐗╃悊 UART 寮曞嚭 | 鉂?纭欢娌℃湁 |
| **panic 鍚庤嚜鍔ㄩ噸鍚?+ adb 璇?* | 鉁?**鍞竴鍙**锛屽垎涓ゅ崐锛氶噸鍚?+ 璇?|
| adb 璇绘棩蹇楃殑鏁版嵁婧?| 鉁?**鐜版垚 API**锛歚native_ufs_log_open/write/sync`锛圢ativeUfs.cpp:1119-1180锛岄鐣欐棩蹇?LBA 鍖猴紝4K 鍧楀啓锛屾棤璋冪敤鑰呪€斺€斿氨鏄负杩欎釜鍦烘櫙棰勫煁鐨勶級 |

**鎺ㄨ崘瀹炴柦椤哄簭**锛堟瘡姝ョ嫭绔嬪彲楠岃瘉锛夛細
1. `vince_mark_putc` 鍔犲唴瀛?ring buffer锛?MB锛夛紝瀛樻墍鏈?kprintf 杈撳嚭 鈥斺€?绾唴瀛橈紝鏃犻闄?2. 鎵惧埌 panic 璺緞**姝ｇ‘鏃舵満**鐨勯噸鍚偣锛坄kdp_machine_reboot()` 宸插瓨鍦紝鎴栧湪 `panic_trap_to_debugger` 杩斿洖鍓嶏紱**涓嶅湪 `os_reason_create`**锛夆€斺€?鍏堝彧鍔犱竴涓?鐢绘爣璁板悗 5 绉掑啀閲嶅惎"鐨勫欢鏃讹紝楠岃瘉鏃舵満瀹夊叏
3. panic 鍓嶆妸 ring buffer 鍐欒繘 `native_ufs_log_write`锛堥鐣欏尯鍦ㄧ洏灏撅紝涓嶇鏍瑰嵎锛?4. 閲嶅惎鍚庯紙杩?Android锛夛紝`adb shell dd if=/dev/block/by-name/<鏃ュ織鍒嗗尯> of=/sdcard/log.bin` + `adb pull`锛宧ost 渚ц剼鏈В鏋?5. 鍏ㄦ祦绋嬫墦鍖呮垚涓€涓剼鏈細`build 鈫?flash 鈫?boot 鈫?绛?panic 鈫?绛夐噸鍚?鈫?adb pull log 鈫?瑙ｆ瀽鍏抽敭鍊糮

## 4. 澶嶇幇褰撳墠鍩虹嚎锛? 鏉″懡浠わ級

```bash
# WSL 鍐?cd ~/src/UniXNU && git checkout aae83c4 2>/dev/null
cd ~/src/unixnu-vince && git checkout 24b73bc 2>/dev/null
bash /mnt/c/Temp/auto/build_pack_short.sh   # 浜у嚭 /mnt/c/Temp/cust-final2.img
```
```powershell
# Windows 渚?cd C:\platform-tools
.\fastboot.exe flash cust C:\Temp\cust-final2.img
.\fastboot.exe boot C:\Users\Administrator\Desktop\unixnu-vince-kernel-ufs\vince-xnu64-Z.img
```
棰勬湡锛?0 绉掑悗鍋滃湪 `unexpected SIGKILL of ... launchd`锛屽睆骞曟湁 `RN8`/`RA124812296`銆乣ufs:entered`銆乣IOFindBSDRoot entered`銆?
**鏋勫缓鎴愬姛鐨勫垽鎹?*锛堝埆鍐嶇敤瀛楃涓?count 楠楄嚜宸憋級锛?- `/tmp/bv2.log` 鍑虹幇 `built kernel at`锛?*娌℃湁** `KERNEL NOT REGENERATED`
- `out/vince/kernel/kernel.macho` 鐨?**md5 鍙樺寲**

## 5. 鏂囦欢鍦板浘锛堥兘鍦ㄥ摢锛?
| 鏂囦欢 | 浣滅敤 |
|---|---|
| `C:\Temp\auto\build_verify.sh` | 鐪熸鐨勫唴鏍告瀯寤猴紙鍚紦瀛樺垹闄ゆ竻鍗?L54銆佹瘡杞?git reset锛?|
| `C:\Temp\auto\build_pack_short.sh` | 鏋勫缓+鎵撳寘+楠岃瘉涓€鏉￠緳 |
| `C:\Temp\auto\pack_from_board.sh` | ADT 鐢熸垚锛堜粠 board.toml 璇诲弬鏁帮級+ make-cust-payload |
| `C:\Temp\auto\make-trustcache.py` | cdhash 鎻愬彇 + trustcache 鐢熸垚锛坆ig-endian CS blob 宸蹭慨锛?|
| `~/src/UniXNU/scripts/vince-reason-probes.py` | **姣忚疆蹇呰窇鐨?inserter**锛堟敼 sys_reason.c锛岃 2100/2180锛夆€斺€?鍔犳柊鎺㈤拡浼樺厛鎸傝繖閲?|
| `~/src/UniXNU/scripts/build-xnu-4k-baseline.sh` | 椹卞姩閾炬帴锛坒orce_load 鍧?~L1735锛夈€佹帰閽?hook 鐐?|
| `PUSH-GOTCHA.md` | git push 鍋囨垚鍔熺殑鍧戜笌姝ｇ‘涓夋娉?|
| `HANDOVER-exec-fault.md` | 涓荤嚎 689 琛屽畬鏁磋褰曪紙鍗佸叚鑺傦級 |

## 6. 涓嬩竴姝ュ缓璁紙鎸変环鍊兼帓搴忥級

1. **鍐呭瓨 ring buffer + UFS 鏃ュ織钀界洏**锛埪?.4 鐨?1/3 姝ワ級鈥斺€?涓嶇閲嶅惎閫昏緫锛岀函澧炵泭锛屼换浣?panic 閮借兘鐣欎笅瀹屾暣 log
2. **GccUsb.h**锛圖WC3 鐨勬椂閽熼棬鎺э級鈥斺€?鎵撻€?USB 鐨勫墠鎻?3. **閲嶅惎鏃舵満**锛氬湪 `panic_trap_to_debugger` 灏鹃儴锛堟鏃跺钩鍙板凡灏辩华锛夊姞寤舵椂閲嶅惎锛宐oot-arg 闂ㄦ帶
4. 涓荤嚎 SIGKILL锛氳嫢 搂3.4 鐨?log 鑳借惤鐩橈紝涓€娆?panic 灏辫兘鐪嬪埌瀹屾暣鐨?exec 璺緞锛宍SECURITY_POLICY` 鐨勭湡姝ｆ潵婧愬ぇ姒傜巼涓€鐩簡鐒?
