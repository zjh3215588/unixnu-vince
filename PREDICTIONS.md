# 棰勫垽娓呭崟锛堟洿鏂颁簬 2026-10-22 21:58锛?
鎸?`bsd_init.c` / `bsdinit_task()` 鐨勬墽琛岄『搴忔帓鍒椼€傛挒涓婃椂鐩存帴瀵瑰彿銆?
| # | 鍗＄偣 | 瑙﹀彂鏉′欢 | 鐘舵€?|
|---|---|---|---|
| 1 | `panic("rootvp not authenticated after mounting")` | 闈?macOS 寮哄埗 `require_rootauth = TRUE`锛沵ockfs/ramdisk 鏍规病鏈?sealed 绛惧悕 | 鉁?宸叉彁鍓嶄慨锛坄zzzz-vince-unsealed-root.patch`锛墊
| 2 | `cannot mount root, errno = N` | 娌℃湁鍙敤鏍硅澶囷紙NativeUfs 宸插叧锛屾棤 ramdisk锛墊 **寰呮挒锛岀涓€纭澶?* |
| 3 | `imageboot_setup` | `CONFIG_IMAGEBOOT` 鎵剧郴缁熺鐩橀暅鍍?| 寰呰瀵?|
| 4 | `devfs_kernel_mount("/dev")` | devfs 鏈垵濮嬪寲 | 寰呰瀵?|
| 5 | `load_init_program` 鎵句笉鍒?init | 瑙佷笅 | **绗簩纭澶?* |
| 6 | 8 鏍?loopattach 绔炴€?| 鐪熸満澶氭牳锛決EMU `-smp 1` 瑙勯伩 | 宸茬煡 |

## 鍏冲崱 5 鐨勭粏鑺傦紙宸茬‘璁わ級

`kern_exec.c`锛?
```c
static const char * init_programs[] = ('/usr/appleinternal/sbin/launchd.debug', '/usr/appleinternal/sbin/launchd.development', '/sbin/launchd');
```

鎴戜滑鏄?DEVELOPMENT 鏋勫缓锛屾墍浠ラ『搴忔槸
`launchd.development` 鈫?`/sbin/launchd`銆?`appleinternal` 涓嶄細鏈夛紝**蹇呴』闈犳牴鏂囦欢绯荤粺閲岀殑 `/sbin/launchd`**銆?
**杩欐剰鍛崇潃锛氬唴鏍歌兘鎺ㄥ埌杩欓噷涔嬪悗锛屽啀寰€鍓嶅畬鍏ㄥ彇鍐充簬鏍规枃浠剁郴缁熴€?*
涓嶆槸鍐呮牳閫昏緫闂锛屾槸銆宨OS 鐢ㄦ埛鎬佽娌¤杩涘幓銆嶇殑闂銆?
## 宸茬煡鐨勬纭仛娉曪紙閬垮厤閲嶅韪╋級

- **boot-args 璧?`unixnu.toml` 鐨?`[[entry]] args`**锛屼笉鏄?ADT銆佷笉鏄?`make-vince-adt.py`
- **kprintf 瑕佷袱涓紑鍏冲悓鏃舵竻**锛歚disable_serial_output` 鍜?`disable_kprintf_output`
  锛堥棬鏄?`if (!disable_serial_output && !disable_kprintf_output)`锛?- **`PE_kputc` 瑕佹棤鏉′欢璧嬪€?*锛歚PE_init_kprintf` 璺戝湪 `STARTUP(KPRINTF)`锛屾棭浜?fb 鏄犲皠
- **鏂版彃妗╀竴寰嬬敤 patch 鏂囦欢**锛屾敞鍏ヨ剼鏈凡闈欓粯澶辨晥 5 娆?- **`extern "C"` 淇濇姢**澶存枃浠讹紙C++ 鏂囦欢 include锛?- **鐩稿 include**锛歚osfmk/` 涔嬪涓€寰?`"../../osfmk/arm/vince_early_mark.h"`
- **鎺㈤拡缂栧彿涓婇檺**宸叉墿鍒?128锛堝師鏉?64 浼氶潤榛樹涪寮?65+锛?
## QEMU 渚у凡楠岃瘉鐨勪簨瀹?
- 鍐呮牳 entry 鑳借窇锛堥《閮ㄧ豢鏉★級
- 寮傚父 trace 鍙湁 IRQ锛?*鏃?abort** 鈫?鍐呮牳鍦?QEMU 閲屾槸娲荤殑
- `disable_serial_output=0 / disable_kprintf_output=0 / vince_mark_putc` 閮藉湪浜岃繘鍒堕噷楠岃瘉杩?- 涓插彛浠嶆棤鏂囨湰 鈫?姝ｅ湪鐢ㄣ€屽浐瀹?UART tag銆嶅尯鍒嗐€孶ART 鍐欎笉閫氥€嶅拰銆宬printf 娌¤蛋鍒般€?- **QEMU 澶嶇幇涓嶄簡 IOSurface 鍗℃**锛堥偅鏄?IOKit 鎵撶湡瀹炵‖浠讹級


## 鐪熸満 IOSurface 鍗＄偣鐨勬湰璐紙閲嶈锛?
ios-vince 鐨?`0046-vince-iosurface-iomfb.patch` 鎻ず浜嗗師鍥狅細浠栦滑**娌℃湁鐢?Apple 闂簮鐨?IOSurface kext**锛岃€屾槸鑷繁瀹炵幇浜嗭細

    iokit/Kernel/arm/vinceSurface.cpp       -> IOCoreSurfaceRoot
    iokit/Kernel/arm/vinceFramebuffer.cpp   -> AppleCLCD

骞跺湪 `iokit/KernelConfigTables.cpp` 娉ㄥ唽杩欎袱涓被锛屽彟澶栧湪 `vincePlatformExpert` 閲岀粰
`arm-io` 瀛愯妭鐐瑰缓 nub锛岃鍐呭缓椹卞姩鑳藉尮閰嶃€?
**缁撹锛歚IOsurfaceRoot:installMemoryRegions()` 涔嬪悗鍗′綇锛屼笉鏄柇瑷€銆佷笉鏄唴瀛樹笉瓒筹紝
鑰屾槸闂簮 IOSurface kext 鍦ㄩ潪 Apple 骞冲彴涓婅窇涓嶉€氥€?* 瓒婅繃瀹冮渶瑕侀噸鍐?surface / framebuffer 椹卞姩锛屽睘浜庡懆绾у伐浣滈噺锛屼笉鏄竴涓よ疆 patch 鑳借繃鐨勩€?
杩欎篃瑙ｉ噴浜嗕负浠€涔?ios-vince 鏈?83 涓ˉ涓併€佸仛浜嗗嚑涓湀鎵嶅埌 SpringBoard銆?
