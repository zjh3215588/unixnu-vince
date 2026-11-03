# vince XNU 绉绘锛氬弬鑰冮」鐩殑璺緞涓庢垜浠殑鍙鎬ф柟妗?
鐢熸垚鏃堕棿锛?026-10-22

---

## 涓€銆佸弬鑰冮」鐩殑鐪熷疄瑙勬ā

| 椤圭洰 | 鍐呮牳鐗堟湰 | 琛ヤ竵瑙勬ā | 鍒拌揪鐘舵€?|
|---|---|---|---|
| **glebenekt/ios-vince** | xnu-8796 | **83 涓?patch / 1.58 MB** | XNU 涓婄湡鏈恒€乁FS 鏍瑰彲璇诲啓銆?*launchd / SpringBoard / backboardd 鍚姩**銆佹樉绀烘湇鍔℃敞鍐?|
| **oosexgang/hackios** | xnu-8796 | **鍗曟枃浠?119 KB** | 閿佸睆/妗岄潰/璁剧疆/Safari 鍙敤锛圓dreno GPU锛墊
| **IssacL04/Pagani** | BCM2837 閰嶇疆澶嶇敤 | 鑻ュ共 | 瓒婅繃鍒嗛厤鍣ㄦ柇瑷€锛屽埌 BSD setconf |
| **鎴戜滑锛圠ux12138锛?* | **xnu-10063** | 绾?20 涓嚜鐮?patch | **鍐呮牳鍒?bsd_autoconf 涔嬪悗锛屽崱 IOSurface** |

**鍏抽敭宸紓**锛氫袱涓垚鐔熼」鐩兘鐢?**xnu-8796**锛屾垜浠潥鎸?**10063**銆?琛ヤ竵**涓嶈兘鐩存帴绉绘**锛屼絾**闃舵鍒掑垎鍜屾柟娉曡鍙互鐓ф惉**銆?
---

## 浜屻€乮os-vince 鐨?83 涓ˉ涓侊紝瀹為檯鏄竴鏉′簲闃舵璺緞

### 闃舵 1锝滆鍐呮牳鑳藉惎鍔紙0001鈥?020锛?0 涓級

| 琛ヤ竵 | 浣滅敤 |
|---|---|
| 0001/0002/0005 | 鏂?clang 鐨勭紪璇戜慨澶?|
| **0003/0010/0012** | **framebuffer serial console銆佹棭鏈?fb 璋冭瘯銆乼tbr0 涔嬪悗淇濈暀 console** |
| 0004/0006鈥?009 | machine config銆佸紑婧?asm pmap銆乻tub Apple 鍐呴儴澶存枃浠躲€佽ˉ closed lib 绌烘礊 |
| 0011 | physmap 瀵归綈琛ラ綈 |
| **0013/0014** | **RNG 涓嶄緷璧?corecrypto**锛坄vm_kern.c`锛?7 琛岋級|
| **0015** | **trust cache 杩愯鏃朵笉鍙敤** |
| **0016/0017/0018** | **device tree platform expert銆佽櫄鎷?timer IRQ銆乥oot CPU 椹卞姩** |
| **0019** | **builtin pthread**锛堜笉鏄?prelink锛侊級|
| 0020 | portable AES-CBC |

**鎴戜滑宸插仛鍒扮殑**锛?003/0010/0012 鐨勭瓑浠风墿锛坒b + UART + kprintf锛屼粖鏅氭墦閫氾級銆?**鎴戜滑杩樼己鐨?*锛?013/0014锛圧NG锛夈€?015锛坱rust cache锛夈€?016鈥?018锛圖T platform expert锛夈€?*0019锛坧thread 鍐呯疆锛屾垜浠敊鐢ㄤ簡 prelink锛?*銆?
### 闃舵 2锝滄牴鏂囦欢绯荤粺锛?021鈥?037锛?7 涓級

| 琛ヤ竵 | 浣滅敤 |
|---|---|
| **0021** | **mockfs + RAM disk 浣滄牴**锛?4 琛岋級|
| 0022/0024 | 鏃?IOMedia 鐨?ramdisk 鏍广€乵ockfs 铏氭嫙 ramdisk IO |
| 0023/0026/0027/0032/0033 | 鍐呯疆 sha256 / HFS / BearSSL锛坢d5/sha1/sha384/sha512锛墊
| **0025** | **鑷缓 AMFI锛屼笉鍋?entitlements 妫€鏌?*锛坄bsd/kern/vince_amfi.c`锛?92 琛岋級|
| **0028/0030/0031/0034** | UFS 鏍硅澶囥€佸啓鏀寔銆佽鍐欐牴銆丏MA above 4G |
| **0029** | **unsealed root**锛?4 琛岋紝鎶?panic 鏀规垚 printf锛墊
| 0035/0036 | AMFI entitlements銆乸latform binaries 绛惧悕 |
| 0037 | bindfs |

**鍏抽敭**锛氫粬浠?*鍏堢敤 mockfs + RAM disk 璧锋**锛?021锛夛紝**UFS 鏄悗鏉ユ墠鍔犵殑**锛?028锛夈€?鎴戜滑鍏虫帀 NativeUfs 鍚庢濂介渶瑕?0021 杩欐潯璺€?
### 闃舵 3锝滆繍琛屾椂绋冲畾锛?038鈥?045锛? 涓級

AppleKeyStore銆乧oredump 鍏抽棴銆?*iowatchdog锛?040/0045锛?*銆丠FS link notes銆?exec 鐭棩蹇椼€?*console crash log锛?043/0044锛?*銆?
**iowatchdog 寰堝叧閿?*锛氭病鏈夊畠锛岀郴缁熻捣涓嶆潵浼氳鐪嬮棬鐙楀浣嶏紝鐪嬭捣鏉ュ儚"闅忔満閲嶅惎"銆?
### 闃舵 4锝滄樉绀猴紙0046鈥?049锛? 涓級

| 琛ヤ竵 | 浣滅敤 |
|---|---|
| **0046** | **鑷爺 IOSurface + IOMobileFramebuffer**锛坄vinceSurface.cpp` / `vinceFramebuffer.cpp`锛墊
| **0047** | **鎸佷箙 console 鏃ュ織**锛? MiB 鐜舰锛屽啓鍦?userdata 鏈熬锛孴WRP 鍙锛墊
| 0048/0049 | devnull tee銆両OKit trace |

**0046 灏辨槸鎴戜滑鍗′綇鐨勯偅涓€娈?*锛屼粬浠殑绛旀鏄?*涓嶇敤 Apple 闂簮 kext锛岃嚜宸卞啓**銆?
### 闃舵 5锝滅敤鎴锋€佸璁撅紙0050鈥?083锛?4 涓級

sandbox 绛栫暐銆乧rash 閲囨牱銆丠FS rename銆乸rocess sampler銆丄KS銆乫b 鑺傛祦銆?**HID event services锛?058锛?*銆乮Phone identity锛?059锛夈€?**瑙︽懜/鎸夐敭椹卞姩锛?060/0062/0063/0071/0083锛?*銆乮Phone X 鏄剧ず灏哄锛?061锛夈€?**SMP PSCI锛?065/0078锛?*銆乧onsole mute銆乻urface 鏌ユ壘缂撳瓨銆乁FS 鍔犻€熴€?**USB锛?072鈥?077/0081锛?*銆乨isplay power銆乶et trace銆乁FS AES銆?
---

## 涓夈€佹垜浠殑瀹為檯宸窛锛堝凡鎸夊疄闄?patch 鐩樼偣淇锛?
鍒濈増鎶婂樊璺濅及寰楄繃閲嶃€傛竻鐐?`patches/xnu/` 鍚庯紝鎯呭喌鏄細

| 鑳藉姏 | 鎴戜滑宸叉湁鐨?patch | ios-vince 瀵瑰簲 | 鐘舵€?|
|---|---|---|---|
| mockfs 缂栬瘧淇 | `mockfs-typed-allocation` / `mockfs-statfs` / `mockfs-intermediate-lookup` / `mockfs-memory-device-width` / `mockfs-test-file` | 0021/0024 | 鉁?**宸插仛** |
| 鏃?block storage 瀹瑰繊 | `null-root-media` | 0021 | 鉁?**宸插仛** |
| trust cache 杩愯鏃?| `native-trust-cache-runtime` | 0015 | 鉁?**宸插仛** |
| **pthread** | `source-pthread-bootstrap`锛堟柊澧?`bsd/kern/source_pthread_bootstrap.c`锛墊 0019 | 鉁?**宸叉湁鏂规** |
| SMP | `native-smp-secondary` | 0065/0078 | 鉁?宸叉湁 |
| panic 鍖?| `native-dt-panic-region` | 0066 | 鉁?宸叉湁 |
| work interval | `native-priv-work-interval` / `native-work-interval-soft-fail` | 0064 | 鉁?宸叉湁 |
| 骞冲彴涓撳 / DT | `armvirt-platform-personality` / `source-machine-layer` / `sheng-platform-power` | 0016鈥?018 | 馃煛 閮ㄥ垎 |
| **mockfs 缂栧叆鍐呮牳** | `zzzz-vince-mockfs-root`锛堟湰杞柊澧烇級| 0021 | 馃煛 **鏈疆楠岃瘉涓?* |
| **RNG 涓嶄緷璧?corecrypto** | 鈥?| 0013/0014 | 鉂?缂?|
| **iowatchdog** | 鈥?| 0040/0045 | 鉂?缂?|
| **AMFI 鏃?entitlements** | 鈥?| 0025 | 鉂?缂猴紙鎴栧凡鐢?`public-entitlements-header` 閮ㄥ垎瑕嗙洊锛墊
| **鑷爺 surface / framebuffer** | 鈥?| 0046 | 鉂?缂猴紝**浠嶆槸鏈€澶у樊璺?* |
| 瑙︽懜 / USB / 鏄剧ず鐢垫簮 | 鈥?| 0058鈥?083 | 鉂?缂猴紝杩滄湡 |

**缁撹锛氶樁娈?1 鍜岄樁娈?2 鐨勭粷澶ч儴鍒嗘垜浠凡缁忔湁浜?*锛岀湡姝ｇ殑绌虹櫧闆嗕腑鍦?**RNG锛?013锛夈€乮owatchdog锛?040锛夈€丄MFI锛?025锛夊拰 surface/framebuffer锛?046锛?*銆?
---

## 鍥涖€佸彲琛屾€ф柟妗?
### 鏂规 A锝滅户缁?10063锛屾寜 ios-vince 鐨勯樁娈佃蛋锛堟帹鑽愮粰"瑕佽嚜涓?鐨勭洰鏍囷級

**鍓嶆彁**锛氭帴鍙?10063 鏄?iOS 17 鍐呮牳锛岀敤鎴锋€?ABI 椋庨櫓鑷媴銆?
**绗?1 姝ワ細琛ラ綈闃舵 1 鍓╀笅鐨勶紙1鈥? 澶╋級**

| 鍔ㄤ綔 | 瀵瑰簲鍙傝€?| 璇存槑 |
|---|---|---|
| **鎶?pthread 浠?prelink 鏀瑰洖鍐呯疆** | 0019 | 鎴戜滑鐩墠鎶?`com.apple.kec.pthread` 鍔犺繘 prelink roots锛屾柟寮忎笉瀵?|
| RNG 涓嶄緷璧?corecrypto | 0013 | 鏀?`osfmk/vm/vm_kern.c` |
| trust cache 杩愯鏃跺蹇?| 0015 | 娌℃湁 Image4 鏃朵笉瑕?panic |
| DT platform expert | 0016鈥?018 | 杩欐槸璁?`arm-io` 瀛愯妭鐐硅兘鍖归厤椹卞姩鐨勫墠鎻?|

**绗?2 姝ワ細鎷挎牴鏂囦欢绯荤粺锛?鈥? 澶╋級**

| 鍔ㄤ綔 | 瀵瑰簲鍙傝€?| 鎴戜滑鐨勫叿浣撴敼娉?|
|---|---|---|
| **`FILESYS_BASE` 鍔?`mockfs`** | 0021 | 鎴戜滑鐨?`config/MASTER.arm64.bcm2837` 褰撳墠鏄?`[devfs fifo fs_compression config_protect config_mnt_rootsnap config_fse routefs namedstreams bindfs]`锛?*娌℃湁 mockfs** |
| **瀹瑰繊鏃?`IOBlockStorageDriver`** | 0021 | `iokit/Kernel/IOService.cpp:5261` 鐨?`assert(ioblockstoragedriverClass)` 瑕佸幓鎺夛紙鎴戜滑鍏充簡 NativeUfs锛岃繖涓被涓嶅瓨鍦級|
| **unsealed root** | 0029 | 鉁?**宸插畬鎴?*锛坄zzzz-vince-unsealed-root.patch`锛墊
| RAM disk 浣滄牴 | 0021/0022 | `rd=md0` 涔嬬被锛屾垨鐢?mockfs 鐩存帴褰撴牴 |

**绗?3 姝ワ細鏄剧ず锛?鈥? 鍛紝杩欐槸鐪熸鐨勫潕锛?*

| 閫夐」 | 宸ヤ綔閲?| 缁撴灉 |
|---|---|---|
| **鑷爺 `IOCoreSurfaceRoot` + `AppleCLCD`** | 2鈥? 鍛?| 鑳界敾鍥撅紝涓?SpringBoard 閾鸿矾 |
| 鏀惧純鍥惧舰 | 0 | 鍐呮牳鑳藉埌 launchd锛屼絾鐪嬩笉瑙佺敾闈?|

**绗?4 姝ワ細杩愯鏃?+ 澶栬**锛堥樁娈?3/5锛屾暟鍛級

### 鏂规 B锝滃垏鍒?8796锛屽熀浜?ios-vince锛堟帹鑽愮粰"瑕佺湅鍒扮敾闈?鐨勭洰鏍囷級

| 椤?| 璇存槑 |
|---|---|
| 鏀剁泭 | **83 涓ˉ涓佺洿鎺ュ彲鐢?*銆佸悓璁惧銆佸悓 iPadOS 16.6.1銆佸凡鍒?SpringBoard |
| 鎴愭湰 | 閲嶆惌鏋勫缓绠＄嚎锛堜絾鎴戜滑鏈?`build-kernel-8796.yml` 鍜?87 涓?patch 鐨勫簳瀛愶級|
| 椋庨櫓 | 闇€瑕佺悊瑙ｅ苟缁存姢鍒汉鐨?1.58 MB 琛ヤ竵 |
| 鏃堕棿 | **1 鍛ㄥ唴鑳界湅鍒板埌浠栦滑鐨勪綅缃?*锛岃€屼笉鏄嚑涓湀 |

### 鏂规 C锝滃弻绾垮苟琛岋紙鏈€绋筹級

- **涓荤嚎 10063**锛氱户缁獙璇佹垜浠嚜宸辩殑鍐呮牳锛圦EMU 宸插埌杈圭晫锛岀湡鏈哄埌 IOSurface锛?- **鍓嚎 8796**锛氱敤 ios-vince 鐨勮ˉ涓佸揩閫熸嬁鍒颁竴涓?*鑳界湅瑙佺敾闈?*鐨勭郴缁?- 涓ゆ潯绾垮叡浜細QEMU 鐜銆丆I 绠＄嚎銆佹帰閽堝伐鍏?
---

## 浜斻€佹垜鐨勫缓璁?
**鍏堝仛鏂规 A 鐨勭 1銆? 姝ワ紙3鈥? 澶╋級锛屽洜涓鸿繖涓ゆ鏃犺璧板摢鏉¤矾閮借鍋氾紝鑰屼笖鎴愭湰鍙帶锛?*

1. **pthread 鏀瑰唴缃?*锛堢幇鍦ㄦ槸閿欑殑锛?2. **`FILESYS_BASE` 鍔?mockfs**
3. **鍘绘帀 `assert(ioblockstoragedriverClass)`**
4. **RAM disk 褰撴牴**

鍋氬畬杩欏洓浠朵簨锛屾垜浠湁寰堝ぇ姒傜巼鎶婂唴鏍告帹杩涘埌 **`load_init_program`**锛堟壘 `/sbin/launchd`锛夈€?鍒伴偅涓€姝ュ啀鍐崇瓥 **鏂规 A 绗?3 姝ワ紙鑷爺 surface锛屽嚑鍛級vs 鏂规 B锛堝垏 8796锛屼竴鍛級**銆?
**鐞嗙敱**锛氬墠鍥涗欢浜嬫槸**涓ゆ潯璺殑鍏叡閮ㄥ垎**锛屽仛浜嗕笉娴垂锛涜€?IOSurface 閭ｄ竴娈垫槸**鍒嗗矓鐐?*锛?搴旇绛夋嬁鍒?`load_init_program` 鐨勫疄闄呯粨鏋滀箣鍚庡啀鍐冲畾銆?
---

## 鍏€佺珛鍗冲彲鎵ц娓呭崟锛堟寜鎬т环姣旀帓搴忥級

| # | 鍔ㄤ綔 | 鍙傝€?| 棰勮 |
|---|---|---|---|
| 1 | `config/MASTER.arm64.bcm2837` 鐨?`FILESYS_BASE` 鍔?`mockfs` | 0021 | 10 鍒嗛挓 |
| 2 | `IOService.cpp` 鐨?block storage assert 鏀规垚瀹瑰繊 NULL | 0021 | 10 鍒嗛挓 |
| 3 | pthread 浠?prelink roots 绉婚櫎锛屾敼鐢ㄥ唴缃疄鐜?| 0019 | 鍗婂ぉ |
| 4 | `vm_kern.c` 鐨?RNG 涓嶄緷璧?corecrypto | 0013 | 鍗婂ぉ |
| 5 | trust cache 杩愯鏃朵笉鍙敤涓?panic | 0015 | 2 灏忔椂 |
| 6 | RAM disk 浣滄牴锛岄獙璇佽兘鍒?`load_init_program` | 0021/0022 | 1 澶?|
| 7 | 鍐崇瓥锛氳嚜鐮?surface 杩樻槸鍒?8796 | 鈥?| 鈥?|

---

## 涓冦€佽瘹瀹炵殑鍒ゆ柇

- **1鈥? 鍋氬畬锛屽唴鏍稿ぇ姒傜巼鑳藉埌 launchd**锛屼絾**鐪嬩笉瑙佺敾闈?*
- **鐪嬭鐢婚潰**闇€瑕?IOSurface 娈碉紝閭ｄ竴娈?*娌℃硶缁?*
- **ios-vince 鐢?83 涓ˉ涓併€佸嚑涓湀**鍋氬埌锛屾垜浠嚜宸卞仛鍚屾牱鐨勬椿**涓嶄細鏇村揩**
- 鍞竴鑳芥樉钁楀姞閫熺殑鏄?*鏂规 B锛堝垏 8796 + 鍊熻ˉ涓侊級**

**鎵€浠ユ渶缁堝缓璁?*锛氬厛鍋?1鈥?锛堝叕鍏遍儴鍒嗭紝3鈥? 澶╋級锛屾嬁鍒?`load_init_program` 鐨勫疄娴嬬粨鏋滐紝
鍐嶅喅瀹?IOSurface 娈垫槸鑷繁鍐欒繕鏄垏鐗堟湰銆?
