# 褰撳墠鐘舵€?鈥斺€?閲嶅啓鍚庣殑鏂扮嚎锛?026-10-28锛?
> **鏈粨搴撳叾浣欐枃妗ｆ槸銆屾帹鍊掗噸鏉ャ€嶄箣鍓嶇殑璁板綍**锛屽彧浣滆拷婧敤锛涗笌鏈枃鍐茬獊鏃?*浠ユ湰鏂囦负鍑?*銆?> 鏂扮嚎鐨勪唬鐮佷笌鍒跺搧涓嶅湪鏈粨搴擄細涓插彛/鎺у埗閫氶亾涓庢棤浜哄€煎畧娴佹按绾胯
> [`vince-usb-cdc`](https://github.com/Lux12138/vince-usb-cdc)锛坄docs/07` 鏄帶鍒堕€氶亾涓?WDT 瀹氭椂鍋滆溅锛夈€?
## 0. 涓€鍙ヨ瘽

7 涓樁娈甸噷鍓?6 涓叏閫氾紝鍐呮牳宸茶繘鍏ョ敤鎴锋€侊紱闃舵 7 鍐呴儴**鍙樊涓€涓?`IOMobileFramebuffer` 鐨?provider 瀹炰緥**銆?
## 1. 鏉夸笂瀹炴祴锛坉1b 杞紝2026-10-28锛?
```bash
python E:/vince/tools/pipeline.py --full --capture 60 \
    --payload-dir <鍒跺搧鐩綍> --expect-payload-sha <payload sha256>
```

| 椤?| 鍊?| 璇佹嵁 |
|---|---|---|
| 瀹屾暣鍚姩鏃ュ織 | **146,042 B / 2,032 琛?* | `d1b-run-com.bin` |
| 瀹堟姢杩涚▼ | `[hb] tag=chk n=68 sb=1 bb=1 rb=1 cfg=1` | 鍚屼笂 |
| keybagd | `DEVICE HAS EPHEMERAL DATA VOLUME, SKIP INIT` + `[ex] pid=11 comm=keybagd rv=0x0` | 鍚屼笂 |
| 鏄剧ず鏃?| `[nm] mask=7 size=1336 init=1 rel=0`锛堢 87 琛岋級 | 鍚屼笂 |
| 鏄剧ず娉ㄥ唽琛?| `[nm] reg=0x7 (imo,imos,imol,dpd)` | d2~d5 杞?|
| 鏅氬姞杞?| `[nm] late reg=7 load=0 reg2=f` | d4 / d5 杞?|
| 鏄剧ず澶辫触鐐?| `[ex] pid=26 comm=IOMFB_FDR_Loader rv=0x100 sig=0 code=1` | wdt-final 杞悓鍨?|

### `mask=7` 鎬庝箞璇伙紙宸插畾妗堬級

`mask` 鏄?`OSMetaClass::allocClassWithName()` 瀵逛笁涓悕瀛楃殑澶辫触浣嶅浘锛?`IOMobileFramebuffer` / `IOMobileFramebufferService` / `IOMobileFramebufferLegacy`銆?
**鎶借薄绫荤殑 `alloc()` 鎭掕繑鍥?NULL**锛坄OSDefineAbstractStructors` 鐢熸垚鐨勫氨鏄?`return NULL;`锛夛紝
鎵€浠?`mask=7` **涓嶈兘**璇绘垚鈥滆繖涓変釜绫讳笉瀛樺湪鈥濄€傚悓涓€琛岀殑 `size=1336 init=1` 鏉ヨ嚜
`IOMobileFramebufferUserClient`锛堝叿浣撶被锛屽彲鍒嗛厤涓?init 鎴愬姛锛夈€?
鐢?`getMetaClassWithName()` 澶嶆牳杩囷紙`[nm] reg=0x7`锛夛細**涓変釜鍩虹被閮藉凡娉ㄥ唽**锛?`mask=7` 鍙槸鈥滃畠浠槸鎶借薄绫烩€濈殑琛ㄧ幇銆傜鍥涗綅 `dpd`锛坄AppleDPDisplay`锛夊湪鏃╂湡涓?0锛?鎵ц `OSKextLoadKextWithIdentifier("com.apple.driver.AppleDPDisplay")` 鍚庡彉鎴?`reg2=f`锛坄load=0` 琛ㄧず鍔犺浇鎴愬姛锛夆€斺€斿嵆 **`AppleDPDisplay` 鍙互鍔犺浇骞舵敞鍐岃繘鏉?*銆?
**缂虹殑浠嶇劧鏄竴涓凡 attach 鐨?provider 瀹炰緥**锛堟湁绫?鈮?鏈夋寕鍒拌澶囨爲涓婄殑瀵硅薄锛夈€?
## 2. 鍚姩閾句笌澶嶄綅

```
XBL 鈫?ABL 鈫?fastboot boot Mu UEFI 鈫?cust 閲岀殑 UniXNU payload 鈫?XNU

澶嶄綅锛歬ernel `vince-park-after=N`
        鈫?`[park] arm`锛堝彧璁?deadline锛?        鈫?deadline 鍒扮偣鎵嶈皟 vince_wdt_arm_now()锛屾墦 `[park] wdt`
        鈫?APSS WDT(0x17C10000) EN=1銆丅ARK=BITE=2097152 ticks
        鈫?绾?32 s 鍚庡挰鍚?鈫?SoC 澶嶄綅 鈫?ABL 璇?misc 鈫?recovery
```

- `WDT.CFG` 鍙 `mode=N`锛涚幇琛?`mode=0`锛堜笉璁?Mu 棰勬瑁咃級銆?- **鍜悎 = 姝﹁鍚庣害 32 s**锛屼笉鏄?64 s锛坄2097152 ticks / 32768` 鍙槸鎹㈢畻锛屼笉鏄疄娴嬶級銆?  鐩存帴瑙傛祴鍒扮殑鍙湁涓€杞細r10z3v锛宒eadline 82.7 s 鈫?USB LOST boot+114.8锛?1.3 s锛夈€?  鍏朵綑杞鐨勫挰鍚堟椂鍒婚兘鏄€渄eadline + 32鈥濈殑鎺ㄦ柇銆?- 鎯宠澶嶄綅鏇存櫄锛?*鍙兘鍔犲ぇ `park-after`**锛?:1锛夈€備唬浠锋槸鈥滄瑁呮椂鍒讳箣鍓嶇殑 panic 娌℃湁纭欢鐙楀厹搴曗€濄€?
## 3. 鏍瑰嵎涓庣敤鎴锋€?
- 鏍癸細鍙 APFS锛沗/private/var` 鐢?**vincevar**锛堝唴瀛樺嵎锛夋寕杞斤紱preboot 鏍戜笌 dyld shared cache锛?36锛夊凡閫氥€?- 娌欑洅鐩墠 skip锛坄vince-mac-skip-sandbox=1`锛夈€?
## 4. 鏃犱汉鍊煎畧涓庡垽鎹邯寰?
- 鍗曡疆 **86~129 s**锛岄浂鎸夐敭锛屽け璐ヨ疆锛坧anic / keybag 鑷村懡锛変篃浼氭寜鏃跺洖 TWRP銆?- **鍙綋浜嬩欢鏃跺埢鐨勫彧鏈変笁绫?*锛歱ort-session 鑷墦鐨?`HH:MM:SS TX/RX`銆佺湡瀹炵殑 USB LOST銆?  `adb devices` 鐪嬪埌 recovery 鐨勬椂鍒汇€?  pipeline 鐨?`[HH:MM:SS]` 鍓嶇紑銆乣closed`銆乣close <鏃跺埢>`銆乣auto-reset TWRP after X s`
  閮芥槸瀛愯繘绋嬭繑鍥炲悗琛ョ殑锛?*涓嶈兘褰撲簨浠舵椂鍒?*銆?- 姣忚疆鐨?`[park] arm` 鏃跺埢閮戒笉鍚岋紙瀹炴祴 48.6 / 50.5 / 52.4 / 56.3 s锛夛紝
  鎵€浠ュ垽璇讳竴寰嬬敤褰撹疆 `dl 鈭?ticks` 鍙嶇畻锛屼笉璁稿涓婁竴杞殑甯告暟銆?
## 5. 鏈粨搴撳巻鍙查儴鍒嗛噷宸茬粡澶辨晥鐨勮娉?
| 鏃ц娉曪紙10-23 ~ 10-25锛?| 鐜扮姸 |
|---|---|
| 鍐呮牳鍋滃湪 `execve("/sbin/launchd")`锛宍errno 2`锛岀己鏍规枃浠剁郴缁?| 宸茶繃锛氭牴鍗?+ launchd 閫氳繃锛岀敤鎴锋€佽捣鏉ヤ簡 |
| 涓嬩竴姝?`./unixnu build userdata` + `fastboot flash userdata` | 宸插彇浠ｏ細鍙 APFS 鏍?+ vincevar 鎸?`/private/var` |
| 鏃ュ織闈?UFS 绐楀彛锛坄vinceLOG1`锛寀serdata 鏈熬 32 MiB锛夊畾鏈熷啓鐩樺啀璇诲洖 | 涓荤嚎鏀逛负 DWC3 CDC 瀹炴椂涓插彛锛沀FS 绐楀彛鍙繚鐣欎负 panic 鍦烘櫙鏃佽矾 |
| 澶嶄綅闈?panic 璺緞閲岀殑 PSCI `SYSTEM_RESET` | 鐜板湪涓诲浣嶆簮鏄?APSS 纭欢鐙楋紙park-after 瀹氭椂姝﹁锛夛紱PSCI 浠嶇敤浜?`REBOOT` 鎺у埗甯?|
| 鏄剧ず璧扳€滆嚜鐮?`IOCoreSurfaceRoot` + `AppleCLCD`锛屾敞鍐岃繘 `iokit/KernelConfigTables.cpp`鈥濓紙`HANDOVER.md` / `FLOW.md` / `PREDICTIONS.md` / `PLAN.md`锛?| **`AppleCLCD` 涓嶅湪 iPadOS 鐨?kernelcache 閲?*锛涙樉绀轰晶鐪熻韩鏄?`com.apple.driver.AppleDPDisplay`锛堝尮閰?`lcd,edp`锛夛紝宸插湪鏉夸笂瀹炴祴鍙姞杞藉苟娉ㄥ唽锛坄late load=0 reg2=f`锛夈€傝嚜鍐?`IOMobileFramebuffer` 瀛愮被閭ｆ潯闈欐€侀摼鎺ヨ矾宸茶鍚﹁瘉 |

## 6. 涓嬩竴姝ワ紙鎸夊垽鍒姏鎺掑簭锛?
1. ~~`getMetaClassWithName()` 瀹氭 `mask=7`~~ 鈥斺€?**宸插仛**锛歚reg=0x7`锛屼笁涓熀绫诲潎宸叉敞鍐岋紝
   `mask=7` 鍙鏄庡畠浠娊璞°€?2. **缁?`AppleDPDisplay` 涓€涓兘鍖归厤鐨勮澶囪妭鐐?*锛歚OSKextLoadKextWithIdentifier` 宸茶兘鎶婂畠
   鍔犺浇骞舵敞鍐岋紙`reg2=f`锛夛紝浣嗗畠杩橀渶瑕佽澶囨爲閲屽尮閰?`lcd,edp` 鐨勮妭鐐癸紙绀惧尯鏄嚜閫?   `/arm-io/disp0`锛夋墠浼?attach锛屼骇鐢?provider 瀹炰緥銆?3. **閲囬泦绐楀彛**锛歚--capture` 鏀鹃暱鍒拌鐩栧浣嶇偣锛岀敤鐪熷疄 `USB LOST at` 鏃堕棿鎴?   鎶娾€滄瑁呭悗绾?32 s鈥濅粠鎺ㄦ柇鍙樻垚瀹炴祴銆?
