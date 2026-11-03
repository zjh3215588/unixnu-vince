# PMGR 绉绘璁″垝锛坣abu / SM8150锛?
鍐呮牳宸茬粡鍦?vince 涓婅繘鍏ユ墽琛岋紙`DARWINBOOT: hand-off to the kernel`锛夈€?鎺ヤ笅鏉ユ渶鏃╀細 panic 鐨勫湴鏂癸紝鍩烘湰鍙互纭畾鏄?**骞冲彴鐢垫簮绠＄悊锛圥MGR锛?*锛?XNU 鍦?`bsd_init` 涔嬪墠灏变細閫氳繃 `ApplePMGR` 瀹舵棌璁块棶 AON / PMGR 瀵勫瓨鍣ㄣ€?
## 0. 鍏堣鐨勪笢瑗匡細涓€浠?panic 鏃ュ織

娌℃湁鏃ュ織灏辨棤浠庝笅鎵嬶紝涓ょ鍙栨硶锛堜紭鍏堢涓€绉嶏級锛?
1. **灞忓箷**锛氱幇鍦ㄥ唴鏍稿凡鎺ョ鏄剧ず锛宲anic 浼氬柗鍦ㄥ睆骞曚笂 鈫?鎵嬫満褰曞儚/杩炴媿鎶撲笅鏉?2. **UART**锛氫覆鍙?115200锛圫M8150 涓€鑸?`ttyMSM0`锛夛紝閰嶇疆閲屾湁 `serial=3`锛?   鎺?USB-TTL 鍒颁富鏉挎祴璇曠偣鍙嬁瀹屾暣 log

鏃ュ織閲岄噸鐐规壘锛?- `panic(...)` 鐨勭涓€琛屼笌璋冪敤鏍?- 浠讳綍 `ApplePMGR` / `AppleARMIODevice` / `platform-power` 瀛楁牱鐨?kext 鍚?- 鏈€鍚庢垚鍔熷姞杞界殑 kext锛堢敤瀹冨垽鏂槸绗嚑涓┍鍔ㄦ寕鐨勶級

## 1. SM8150 渚х殑鐪熷疄褰㈡€侊紙鍜岃嫻鏋滃畬鍏ㄤ笉鍚岋級

> 璇﹁ `docs/vince-dts-extract.md`锛氳琛ㄦ潵鑷叕鍏?vince DTS锛屽湴鍧€宸叉牳瀵广€?

| 灞?| 鑻规灉 | SM8150 |
|---|---|---|
| 瀵勫瓨鍣ㄨ闂?| MMIO + AON mailbox | **IPC(CmdDb) 娑堟伅**銆丷PMh 鍛戒护 TCS銆丼PMI |
| 鐢垫簮鍩?| PMGR 涓€澶у潹 | RPMh锛圧SC + TCS锛夈€丯PA銆丳DC |
| 鏃堕挓 | PMGR clock gates | GCC锛坄0x100000`锛?|

宸茬‘璁ゅ熀鍧€锛?
```
RPMh RSC  0x18200000  (0x10000) 脳3 banks   <-- 鐪熸鐨?RPMh 鍏ュ彛
IPCC/apss_shared 0x17c00000  (0x1000)  <-- 鍙槸 mailbox锛屼笉鏄?RPMh
cmd-db    0x85f20000  (0x20000)
SPMI      0x0c440000
watchdog  0x17c10000
timer     0x17c20000
SMEM      0x86000000
GCC       0x100000    (瑙?scripts/GccUfs-vince.h 鐨勫亸绉昏〃)
```

RPMh DRV 鍏抽敭瀵勫瓨鍣紙SM8150锛夛細

```
RSC_DRV_CTL_TCS_DATA_HI   0x38
RSC_DRV_CTL_TCS_DATA_LO   0x40
TCS_AMC_MODE_ENABLE       BIT(16)
```

## 2. ApplePMGR 鐨勬帴鍙ｉ潰锛堥€嗗悜缁撴灉锛?
```
ApplePMGR sizeof = 0x4b8a8
vtable slot 177..340   锛堝叡 164 涓?slot 闇€瑕佸疄鐜帮級
slot 320  readAon()
slot 321  writeAon(uint64_t)
```

绛栫暐锛?*涓嶈涓€娆″啓 164 涓?*銆傚厛璁?`readAon/writeAon` 鍜屽垵濮嬪寲璺緞宸ヤ綔锛?鍏朵綑 slot 鍏堢粰瀹夊叏鐨勭┖瀹炵幇锛堣繑鍥?0 / 涓嶅仛鍔ㄤ綔锛夛紝闈?panic 鏃ュ織閫愪釜琛ャ€?杩欏拰 sheng 鐨勫仛娉曚竴鑷达細`sheng-platform-power.patch` 鍙槸鍦?`bsd_init.c` 閲?鍔犱簡涓€鍙?`sheng_pmgr_run()`銆?
## 2.5 RPMh 鏈€灏忚閫氳矾锛堜笅涓€娈典唬鐮佺殑鐩爣锛?
```
cmd-db(0x85f20000) 閲屾寜 "active"/"wake"/"sleep" 鏌ュ埌 TCS 鍩哄潃
        鈫?缁?AMC 鍛戒护 16 瀛楄妭锛歿 msg_id, addr, data, wait | cmd<<28 }
        鈫?鍐?bank + RSC_DRV_CTL_TCS_DATA_HI(0x38) / LO(0x40)锛岀疆 TCS_AMC_MODE_ENABLE(BIT16)
        鈫?绛?DRV completion锛堟垨 SMEM 閲岀殑 ack 閫氶亾锛?        鈫?鍥炶 data 鈫?杩欏氨鏄?XNU 鎯宠鐨?鐢垫簮鍩熺姸鎬?鐢靛帇/鏃堕挓"
```

鍒ゅ畾鎴愬姛涓嶆槸"涓嶅穿"锛岃€屾槸**鑳芥墦鍗板嚭闈?0 鐨勭湡瀹炵數鍘?鏃堕挓鍊?*銆?
## 3. 瀹炴柦椤哄簭

1. `kits/vince/vincePlatformPower.cpp` 楠ㄦ灦锛堟湰娆″凡鏀撅級
2. `build-vince-platform-power.py`锛氭妸楠ㄦ灦缂栬瘧鎴?kit锛屾敞鍏?UniXNU 椹卞姩鍒楄〃
3. `vince-platform-power.patch`锛氶暅鍍?`sheng-platform-power.patch`锛?   鍦?`bsd_init.c` 閲屽姞 `vince_pmgr_run()`
4. 棣栨鍙疄鐜帮細
   - `init()`锛氭帰娴?IPCC / cmd-db / SMEM锛屾墦鍗板熀鍧€涓庣増鏈?   - `readAon/writeAon`锛氬厛鍋?**cmd-db 鏌ヨ + RPMh TCS 鍐?*鐨勬渶灏忛棴鐜紝
     澶辫触鍒欒繑鍥?0 鑰屼笉鏄穿
5. 鎶?panic 鈫?琛ヤ笅涓€涓?slot 鈫?寰幆

## 4. 鍒ゆ柇"鏄惁鐪熺殑閫氫簡"

鏍囧噯涓嶆槸"涓?panic"锛岃€屾槸锛?- 鑳芥墦鍗板嚭浠?RPMh 璇诲埌鐨勭湡瀹炵數鍘?鏃堕挓鍊硷紙鑰屼笉鏄?0锛?- UFS 椹卞姩鑳藉湪 XNU 閲屾灇涓惧埌鍒嗗尯锛坄NativeUfs` 宸插湪鏍稿績閲岋級
- 鑳借蛋鍒?`bsd_init` 骞跺紑濮嬪姞杞?kext

## 5. 椋庨櫓

- RPMh TCS 鏄?*鍏变韩璧勬簮**锛屽啓閿欎細璁╂暣鏈烘帀鐢?鎸傛锛堝彲闀挎寜鐢垫簮鎭㈠锛?- 寤鸿姣忔瀹為獙鍓嶇‘淇?`cust` payload 瀹屽ソ锛岄殢鏃跺彲閲嶅埛
- 涓嶈鍔?`abl`/`xbl`/`bootloader`

