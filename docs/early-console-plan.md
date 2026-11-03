# 鍐呮牳鏃╂湡 console 璧板抚缂撳啿锛堜笉鎷嗘満鎷垮埌 panic锛?
## 闂

鍐呮牳宸茶繘鍏ユ墽琛岋紙`DARWINBOOT: hand-off to the kernel` / `still-there kernel entry code ran`锛夛紝
浣?*灞忓箷涓婃病鏈変换浣?panic 鏂囧瓧**锛屾帶鍒舵潈闅忓悗鍥炲埌 UniXNU锛堣彍鍗曡閲嶇粯锛夈€?
鍘熷洜锛歑NU 鏃╂湡 `kprintf` 榛樿杈撳嚭鍒?*涓插彛**锛涗笉鎺?UART 灏辨槸榛戠銆?鑰?UART 闇€瑕佹媶鏈洪绾匡紝`fastboot`/ADB 鍦ㄦ鏃堕兘涓嶅瓨鍦ㄣ€?
## 宸叉湁鐨勬湁鍒╂潯浠?
DarwinBoot 宸茬粡鎶婃樉瀛樹俊鎭氦缁欏唴鏍革紙boot args `Video[6]`锛夛細

```
video base=0x50000000   1600x2560   row 6400 bytes   32 bpp
```

鍗?`PE_state.video` 閲屽凡鏈?`v_baseAddr / v_rowBytes / v_width / v_height / v_depth`銆?甯х紦鍐叉槸鏅€氬唴瀛樻槧灏勶紝EL1 涓嬪彲鍐?鈥斺€?**瀹屽叏涓嶉渶瑕侀澶栫‖浠?*銆?
## 鏂规锛氳嚜甯︿竴涓瀬灏忓抚缂撳啿 console

涓嶄緷璧栬嫻鏋滅殑 `video_console`锛堣瀛愮郴缁熶富瑕佷负 x86 鍚姩灞?鐧藉睆鏈嶅姟锛孉RM 渚ф湭鍚敤锛夛紝
鑷繁鍐欎竴涓嚜鍖呭惈鐨?putc 鍚庣锛岄闄╂渶浣庛€?
```
scripts/vince-early-fb-console/
鈹溾攢鈹€ vince_fb_console.c    ~150 琛?鈹?    - 8x16 鐐归樀瀛楀簱锛圓SCII 32..126锛屽彲鍏堝彧鍋?0x20..0x7E 瀛愰泦锛?鈹?    - vince_fb_putc(c)锛氬鐞?\n / \r / 婊氬睆
鈹?    - 鍍忕礌鍐欏叆锛歜ase + rowBytes*y + 4*x 锛?2bpp 鐩存帴鍐?0x00FFFFFF
鈹?    - 鍏ㄩ儴鍩轰簬 PE_state.video锛屼笉鍋氫换浣?MMIO / 瀵勫瓨鍣ㄦ搷浣?鈹斺攢鈹€ inject.py            鏋勫缓鏈熸敞鍏?```

### 娉ㄥ叆鐐?
1. `PE_init_kprintf()`锛坄pexpert/gen/pe_gen.c` 鎴?arm 鐨勫疄鐜帮級
   鈫?鍦ㄥ垵濮嬪寲涔嬪悗鍔狅細
   ```c
   if (PE_state.video.v_baseAddr != 0) { vince_fb_init(); }
   ```
2. `vputchar()`锛坄osfmk/console/printf.c` 鎴?pexpert 瀵瑰簲澶勶級
   鈫?涓插彛杈撳嚭涔嬪悗杩藉姞 `vince_fb_putc(c);`

### 瀹夊叏绾︽潫

- `v_baseAddr == 0` 鎴?`v_depth != 32` 鎴栧楂樺紓甯?鈫?**瀹屽叏涓嶅惎鐢?*锛堢洿鎺?return锛?- 鍙仛鏅€氬唴瀛樺啓锛涗笉璇汇€佷笉鍐欎换浣?SoC 瀵勫瓨鍣?- 涓嶅仛鍐呭瓨鍒嗛厤锛堟棭鏈熸棤 malloc锛夛紝闈欐€佹暟缁勪繚瀛樺厜鏍?棰滆壊
- 澶辫触缁濅笉 panic锛屾渶鍧忔儏鍐靛氨鏄?灞忓箷涓婁粈涔堥兘涓嶅"

## 瀹炴柦椤哄簭

1. 鎷変竴浠?xnu 婧愮爜锛圕I 鎴栨湰鍦?clone 鍒?`~/xnu`锛夛紝纭锛?   - `PE_init_kprintf` 鐨勭湡瀹炶矾寰勪笌鍑芥暟浣?   - `vputchar` 鐨勭湡瀹炶矾寰勪笌绛惧悕
   - `PE_state.video` 瀛楁鍚嶄笌绫诲瀷锛坄video_info_t`锛?2. 鍐?`vince_fb_console.c`锛岀敤鐪熷疄瀛楁鍚嶏紱鍏堝湪鏈湴 `clang -fsyntax-only` 杩囦竴閬?3. `inject.py`锛氬熀浜庨敋鐐瑰瓧绗︿覆鎻掑叆锛屾彃鍏ュ悗**鏍￠獙閿氱偣鍞竴涓旀彃鍏ユ垚鍔?*锛屽け璐ョ洿鎺ヨ鏋勫缓 fail
4. 鎺?CI 缂栧唴鏍?鈫?閲嶆墦 boot.img锛坄vince-xnu64-*.img` 鍚屾祦绋嬶級鈫?鐪熸満 boot
5. 鍒ゅ畾锛?   - 灞忓箷鍑虹幇鍐呮牳鏃╂湡鏂囧瓧 / `panic(...)` 鈫?console 閫氫簡 鉁?   - 浠嶆槸鍙湁 UniXNU 鑿滃崟 鈫?鍐呮牳鎸傚緱姣?`PE_init_kprintf` 鏇存棭
     鈫?鎶?fb 鍒濆鍖栧啀鍓嶇Щ锛坄arm_init` / `machine_startup` 涔嬪墠锛夛紝鎴栫洿鎺ユ斁鍒?       `Entry.S` 涔嬪悗鐨?C 鍏ュ彛绗竴琛?
## 涓?PMGR 鐨勫叧绯?
杩欐槸**鍓嶇疆椤?*锛氭病鏈夋棭鏈熻緭鍑猴紝PMGR 姣忎竴姝ラ兘鏄洸鏀广€?console 鎵撻€氬悗锛孭MGR 鐨勮皟璇曞惊鐜彉鎴愶細
鏀?`vincePlatformPower.cpp` 鈫?缂?鈫?boot 鈫?灞忓箷涓婄洿鎺ョ湅鍒拌鍒扮殑鐢靛帇/鏃堕挓鍊笺€?
---

## 瀹炴祴杩涘睍锛?026-10-21 19:49锛?
### 宸蹭慨澶嶏細瑙嗛鏁扮粍閿欎綅锛堢湡鍑朵箣涓€锛?
`DarwinBootPkg/Driver/BootVideo.h` 鍘熸潵鎶?`boot_args.Video[6]` 鍐欐垚浜?
```
[0]=base  [1]=1  [2]=rowBytes  [3]=width  [4]=height  [5]=32
```

鑰?XNU锛坄pexpert/arm/pe_init.c:425`锛夋湡鏈?
```
[0]=base  [1]=rowBytes  [2]=width  [3]=height  [4]=depth  [5]=display
```

鈫?鍐呮牳璇诲埌 `rowBytes=1 / width=6400 / height=1600 / depth=2560`锛?`initialize_screen()` 鍒ゅ畾澶辫触 鈫?**闈欓粯鍒囧洖涓插彛** 鈫?灞忓箷姘歌繙娌℃湁鍐呮牳杈撳嚭銆?
宸蹭慨姝ｄ负姝ｇ‘甯冨眬锛堝苟鍚屾淇 DarwinBoot 鑷繁缁樺埗鏂囧瓧鏃剁殑涓嬫爣锛夈€?淇鍚庡疄娴嬶細`base=0x50000000 row=6400 width=1600 height=2560 depth=32 display=0` 鉁?
### 浣嗕粛鏃犲唴鏍歌緭鍑?鈫?鍐呮牳姝诲湪 `PE_create_console` 涔嬪墠

`osfmk/arm/arm_init.c:616` 鐨?`PE_create_console()` 鏄涓€涓彲鑳藉嚭瀛楃殑鐐广€?瑙嗛鍙傛暟宸插畬鍏ㄦ纭嵈浠嶆棤杈撳嚭锛岃鏄?*娌¤蛋鍒伴偅閲?*銆?
## 褰撳墠绗竴瀚岀枒锛氳捣濮嬪紓甯哥骇鍒紙EL锛変笉鍖归厤

| 浜嬪疄 | 璇存槑 |
|---|---|
| DarwinBoot 鎺㈤拡瀹炴祴 `EL=4`锛? EL1锛?| 鎴戜滑鐜板湪**鍦?EL1** 浜や粯鍐呮牳 |
| DarwinBoot 婧愮爜瑕佹眰 `DarwinCurrentEl() == 4` | 瀹冨己鍒?EL1 |
| 鑻规灉鐪熷疄閾捐矾 | **iBoot 鍦?EL2 浜や粯锛孹NU 鑷繁闄嶅埌 EL1** |

XNU 鐨?`arm_init` / `arm_start` 鏃╂湡浼氳闂?EL2 鐩稿叧绯荤粺瀵勫瓨鍣?锛坄HCR_EL2`銆乣VTCR_EL2`銆乣VHE` 绛夛級銆?*鑻ュ唴鏍镐互涓鸿嚜宸卞湪 EL2 鑰屽疄闄呭湪 EL1锛?绗竴鏉＄浉鍏虫寚浠ゅ氨瑙﹀彂寮傚父锛屼笖姝ゆ椂浠讳綍 console 閮借繕娌″垵濮嬪寲 鈫?闈欓粯姝讳骸銆?*
杩欎笌瑙傚療瀹屽叏涓€鑷达細瑙嗛鍙傛暟姝ｇ‘銆佸唴鏍稿叆鍙ｄ唬鐮佹墽琛屼簡銆佸嵈涓€涓瓧閮芥病鏈夈€?
### 楠岃瘉鏂规硶锛堜笅涓€姝ワ紝浜岄€変竴锛?
**A. 璁╁唴鏍歌嚜宸辫**锛堟渶鐩存帴锛?鍦?`osfmk/arm/arm_init.c` 鐨?`arm_init()` 绗竴琛屾敞鍏ヤ竴涓嚜鍖呭惈鐨?甯х紦鍐?putc锛堝彧鍐?`boot_args_ptr->Video` 鎸囧悜鐨勬樉瀛橈紝涓嶄緷璧栦换浣?console锛夛細

```c
vince_fb_early_init(boot_args_ptr->Video);
vince_fb_early_puts("arm_init enter\n");
```
鍐嶅湪 `machine_startup`銆乣PE_init_platform`銆乣PE_create_console` 鍓嶅悗鍚勬墦涓€涓爣璁帮紝
灏辫兘绮剧‘鐪嬪埌鍐呮牳璧板埌绗嚑琛屻€?
**B. 鏀?DarwinBoot 鍦?EL2 浜や粯**
鎶?`DarwinCurrentEl() != 4` 鐨勫垽鏂敼鎴愬厑璁?EL2锛堟垨鐩存帴鍘绘帀锛夛紝
璁╁唴鏍告寜鑻规灉鐪熷疄閾捐矾浠?EL2 璧锋銆傞闄╋細DarwinBoot 鏈韩褰撳墠璺戝湪 EL1锛?瑕佽瀹冩妸鎺у埗鏉冧氦缁?EL2 闇€瑕侀澶栧仛 EL 鍒囨崲锛坄eret` 鍒?EL2锛夛紝鏀瑰姩鏇村ぇ銆?
> 寤鸿鍏堝仛 A锛堜俊鎭噺鏈€澶с€侀闄╂渶浣庯級锛岀‘璁ゆ鐐瑰悗鍐嶅喅瀹氭槸鍚﹂渶瑕?B銆?
---

## 鏂规璋冩暣锛氬厛鐢ㄣ€屾柟鍧楁鏌ョ偣銆嶏紝涓嶅仛瀛楀簱

鍐?8脳16 瀛楀簱瑕?~1500 瀛楄妭鐐归樀鏁版嵁锛屽鏄撶敾鑺变笖涓嶆槗鏍￠獙锛?鑰?*瀹氫綅姝荤偣鏍规湰涓嶉渶瑕佹枃瀛?*鈥斺€斿彧瑕佺煡閬?璧板埌绗嚑涓鏌ョ偣"鍗冲彲銆?
### 鏈哄埗

`kits/vince/vince_early_mark.c`锛氬線 `boot_args.Video` 鎸囧悜鐨勬樉瀛橀噷鐢?**48脳48 鑹插潡**锛?涓嶄緷璧?console銆佷笉鍋氬垎閰嶃€佷笉纰板瘎瀛樺櫒锛屽弬鏁伴潪娉曞氨闈欓粯鏀惧純锛坄depth!=32` / `base==0`锛夈€?
### 璇绘硶锛堝睆骞曞乏涓婅涓€琛屾柟鍧楋級

| 鐪嬪埌鐨勬柟鍧楁暟 | 鍚箟 |
|---|---|
| **0 涓?* | 杩?`arm_init` 閮芥病杩涘幓 鈥斺€?姝诲湪姹囩紪鍏ュ彛 / MMU 寤虹珛 |
| **1 涓紙鐧斤級** | 杩涗簡 `arm_init` |
| **2 涓紙榛勶級** | 杩囦簡 `PE_init_platform` |
| **3 涓紙闈掞級** | 杩囦簡 `PE_create_console` |
| **4 涓紙缁匡級** | 杩囦簡 `machine_startup` |
| **N 涓孩** | 鍙傛暟闈炴硶锛堝凡瀹夊叏鏀惧純锛屾病鍐欏潖鍐呭瓨锛?|

### 娉ㄥ叆鐐癸紙涓嬩竴杞紝鏀?XNU 婧愮爜锛?
```c
// osfmk/arm/arm_init.c : arm_init() 绗竴琛?vince_mark_init(boot_args_ptr->Video);
vince_MARK(1);

// 涔嬪悗鍦ㄦ瘡鍏抽敭姝ヤ箣鍚庡悇鎻掍竴涓?PE_init_platform(...);   vince_MARK(2);
PE_create_console();     vince_MARK(3);
// machine_startup 鍐?```

### 涓轰粈涔堣繖涓柟娉曟洿浼?
- 浠ｇ爜閲?~110 琛岋紝鏃犵偣闃垫暟鎹紝鍑犱箮涓嶅彲鑳?鐢婚敊"
- 鍒よ鍙渶鏁版柟鍧楋紝鐓х墖/褰曞儚閮借兘鐪嬫竻
- 澶辫触缁濆瀹夊叏锛堝彧鍋氳竟鐣屾鏌ュ悗鐨勬樉瀛樺啓锛?- 瀹氫綅鍒板叿浣撻樁娈靛悗锛屽啀鍐冲畾鏄惁闇€瑕佷笂瀛楀簱锛堥偅鏃跺彲鑳藉凡缁忎笉闇€瑕佷簡锛?
