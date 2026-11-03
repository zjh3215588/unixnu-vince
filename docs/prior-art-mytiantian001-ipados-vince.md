# 鍙傝€冨伐绋嬶細mytiantian001/iPadOS-vince

> 鏉ユ簮锛歨ttps://github.com/mytiantian001/iPadOS-vince
> 璁板綍鏃堕棿锛?026-10-22锛堟湰浠撳簱绗?6鈥? 杞?bring-up 鏈熼棿锛?> 鐢ㄩ€旓細**鍚岀被椤圭洰瀵圭収**銆備笉鏄湰浠撳簱鐨勪緷璧栵紝鏄樊璺濇竻鍗曘€?
## 1. 瀹冨仛鍒颁簡浠€涔堬紙瀵规柟 README 鑷堪锛?
鍦ㄥ悓涓€鍙?**Xiaomi Pad 5 / vince / SM8150-AC** 涓婏細

| 閮ㄥ垎 | 鐘舵€?|
|---|---|
| 鍚姩 | 瑙ｉ攣 stock ABL 鈫?`fastboot boot` 鑷 shim 鈫?XNU |
| CPU | 1 鏍哥ǔ瀹氾紱8 鏍歌兘鍒?userspace |
| 瀛樺偍 | 鑷 UFS host driver锛沬PadOS root 鍦?`userdata` 鐨?HFS+锛屽彲璇诲啓 |
| **鐢ㄦ埛鎬?* | **鐪熷疄 iPad7,3 / iPadOS 16.6.1 (20G81) root 涓?shared cache锛沴aunchd 涓庣郴缁?daemon 鑳借窇** |
| **SpringBoard** | **SpringBoard銆乥ackboardd銆丄KS 閮借兘璧?* |
| 鏄剧ず鏈嶅姟 | `AppleCLCD`銆乣IOMobileFramebuffer`銆乣IOSurface` 宸叉敞鍐岋紱1600脳2560 闈㈡澘宸蹭寒 |
| 鎸夐敭 / AKS | PMIC PON / GPIO 姝ｅ父锛汚KS selector 姝ｅ父锛宬eybag 琛ラ綈 |
| 鏃ュ織 | `userdata` 鏈熬 4 MiB **鎸佷箙 ring**锛屽彲鐢?TWRP 璇诲彇 |

鏈畬鎴愶細iPad UI 鐪熸鏄剧ず锛坆ackboardd 鍙彁浜よ繃涓€娆?`SwapEnd` 灏?`RequestPowerChange(0)` 鍏冲睆锛夈€?GPU accelerator銆佽Е鎽革紙Novatek NT36523 SPI锛夈€?
## 2. 鍏抽敭浜嬪疄锛?*瀹冧篃鏄嚜缂?XNU**

- 鍐呮牳鍩虹嚎锛?*xnu-8796锛坕OS 16 涓栦唬锛?*锛屾潵鑷?Apple 寮€婧愬彂琛岀増
- 涓嶆槸"鍘熺増 iPadOS kernel"锛涚敤鎴锋€佹槸鐪熷疄鐨?iPadOS 16.6.1 浜岃繘鍒?- patch 鏁伴噺锛?*83 涓?*锛坄xnu/patches/0001鈥?083`锛?
> 鈿狅笍 鏈粨搴撴鍓嶇殑鍒ゆ柇"瀵规柟鐢ㄧ殑鏄師鐗?kernel"鏄?*閿欑殑**锛屼互鏈妭涓哄噯銆?
## 3. 涓庢湰浠撳簱锛圲niXNU / xnu-10063.141.1锛夌殑宸紓

| 椤?| 鏈粨搴?| 瀵规柟 |
|---|---|---|
| 鍐呮牳鍩虹嚎 | **xnu-10063.141.1**锛坕OS 17 / macOS 14 涓栦唬锛?| **xnu-8796**锛坕OS 16 涓栦唬锛?|
| 鍖归厤鐨勭敤鎴锋€?| 鏃狅紙10063 涓?iPadOS 16.6.1 鐨?ABI 涓嶅尮閰嶏級 | iPadOS 16.6.1 (20G81) |
| 褰撳墠杩涘害 | 鍐呮牳璺戝埌 `kernel_bootstrap()` 鍐呴儴 | SpringBoard / backboardd / AKS |
| 鍙鎬ф墜娈?| 鑷爺鏂瑰潡+鏁板瓧鎺㈤拡锛坄vince_mark`锛?| `vince_early` 鏂囨湰 console + 鎸佷箙 log ring |

**缁撹**锛氭棤璁烘効鎰忎笌鍚︼紝**瑕佽窇鐪熷疄 iPadOS 鐢ㄦ埛鎬侊紝鍐呮牳鍩虹嚎蹇呴』鏄?8796 涓栦唬**銆?10063 鍗充娇鍐呮牳瀹屽叏璺戦€氾紝涔熸棤娉曞姞杞?iPadOS 16.6.1 鐨勭敤鎴锋€併€?
## 4. 鍙洿鎺ュ€熼壌鐨勪笁涓?patch

### 4.1 `0010-vince-early-framebuffer-debug.patch` 鈥斺€?鏃╂湡 fb 鏂囨湰 console

鏍稿績鏈哄埗锛堝師鏂囨敞閲婏級锛?```c
/* start.s maps the splash framebuffer VA=PA as Normal Non-Cacheable memory.
 * Stop using that mapping before arm_vm_init tears down bootstrap TTBR0. */
```

- 鍦?**`start.s`** 灏辨妸 splash framebuffer 寤烘垚 **VA=PA銆丯ormal Non-Cacheable**
  鈫?鍐欏叆绔嬪嵆鐢熸晥锛?*涓嶉渶瑕?cache flush**
- `vince_early_putc()` 鐢?`iso_font[256*16]`锛?脳16 浣嶅浘锛?*鐩存帴鎵撳嵃鏂囨湰**锛?  琛屾粴鍔ㄣ€乣\r`/`\n` 澶勭悊锛屽叏闈欐€佺姸鎬侊紝鍙湪 `panic()` 閲岀敤
- 鍦?`arm_vm_init()` 閲屻€乣set_mmu_ttb(invalid_ttep & TTBR_BADDR_MASK)` **涔嬪墠**
  璋?`vince_early_disable()`
- 鎵撶偣浣嶇疆锛歚arm_init` 鍏ュ彛 / `PE_init_platform` 鍚?/ `ml_parse_cpu_topology` 鍚?/
  `cpu_bootstrap` 鍚?/ `kernel_startup_bootstrap` 鍚?/ `cpu_init` 鍚?/ 杩?`arm_vm_init` 鍓?
**瀵规湰浠撳簱鐨勬剰涔?*锛氭垜浠幇鍦ㄧ殑鏂瑰潡鎺㈤拡鍙兘浼?绗嚑鍙?锛?鎹㈡垚鏂囨湰鑳界洿鎺ユ墦鍗?鍗″湪鍝釜鍑芥暟"锛屼俊鎭噺澶т竴涓暟閲忕骇銆?
### 4.2 `0012-vince-keep-debug-console-after-ttbr0.patch` 鈥斺€?TTBR0 涔嬪悗淇濅綇 console

璇存槑"鎹㈤〉琛ㄤ箣鍚?console 灏辨病浜?鏄繖鏉¤矾绾跨殑**鍏辨€у潙**锛屼笉鏄垜浠嫭鏈夌殑闂銆?
### 4.3 `0047-vince-persistent-console-log.patch` 鈥斺€?鎸佷箙 ring log

鎶?console 杈撳嚭鍐欒繘 `userdata` 鏈熬 4 MiB 鐨?ring锛?**閲嶅惎鍚庣敤 TWRP 璇诲嚭鏉?*鈥斺€斿交搴曠粫寮€"灞忓箷涓婁粈涔堥兘鐪嬩笉鍒?鐨勫洶澧冦€?
**杩欐槸鏈粨搴撴渶璇ュ厛鎶勭殑涓€浠朵笢瑗?*锛氭瘮浠讳綍灞忓箷鎺㈤拡閮藉彲闈犮€?
## 5. 鍏跺畠鍊煎緱瀵圭収鐨?patch锛堟寜鏈粨搴撶己澶卞彲鑳芥€ф帓搴忥級

| patch | 浣滅敤 | 涓轰綍鐩稿叧 |
|---|---|---|
| `0004-vince-machine-config` | 鏈哄櫒閰嶇疆 | 骞冲彴甯搁噺 |
| `0006-vince-master-config-open-source-asm-pmap` | 寮€婧?asm/pmap 閫傞厤 | 鎴戜滑涔熸湁 4K pmap 绯诲垪锛岄渶瀵圭収 |
| `0011-vince-physmap-alignment-padding` | physmap 瀵归綈琛ラ綈 | VM 鍒濆鍖栫浉鍏?|
| `0016-vince-device-tree-platform-expert` | DT 鈫?platform expert | `PE_init_platform` 涔嬪悗鐨勮涓?|
| `0017-vince-device-tree-virtual-timer-irq` | DT 铏氭嫙瀹氭椂鍣?IRQ | **`kernel_bootstrap` 鍐呮椂閽熷垵濮嬪寲** |
| `0018-vince-boot-cpu-driver` | 鍚姩 CPU 椹卞姩 | **鍚屼笂** |
| `0013/0014` kmem rng / hmac prng | 鍘绘帀 corecrypto 渚濊禆 | 鏃╂湡闅忔満鏁?|
| `0025/0035/0038` AMFI / entitlements / AKS | 鐢ㄦ埛鎬佺鍚嶉摼 | 鍒?SpringBoard 蹇呴渶 |
| `0028/0030/0034/0069/0082` UFS 绯诲垪 | 鑷 UFS 椹卞姩 | root 鎸傝浇 |
| `0046-vince-iosurface-iomfb` | IOSurface + IOMobileFramebuffer | 鏄剧ず鏈嶅姟 |
| `0058/0060/0062/0083` HID / keys / touch / NT36523 | 杈撳叆 | 瑙︽懜 bring-up |

## 6. 琛屽姩寤鸿锛堟寜鎬т环姣旓級

1. **鍏堟妱 `0047` 鎸佷箙 ring log**锛氫竴娆℃姇鍏ワ紝涔嬪悗鎵€鏈?鐪嬩笉鍒?鐨勯棶棰橀兘鍙樻垚"璇绘棩蹇?銆?2. **鍐嶆妱 `0010` 鐨勬枃鏈?console**锛歚start.s` 寤?VA=PA Non-Cacheable + `iso_font`銆?3. **璁ょ湡璇勪及鎹㈠熀绾?*锛氭妸鍐呮牳浠?10063 鎹㈠埌 **8796**锛岀洿鎺ュ榻愬鏂?83 涓?patch 鐨?   涓婁笅鏂囷紝鏄埌鐢ㄦ埛鎬佺殑鍞竴鐜板疄璺緞銆傜户缁湪 10063 涓婅ˉ锛屾案杩滄嬁涓嶅埌 iPadOS 16.6.1 鐢ㄦ埛鎬併€?
