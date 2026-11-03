# UniXNU on Xiaomi Pad 5 (vince / SM8150) 鈥?瀹屾暣浜ゆ帴鏂囨。

> 鐘舵€侊細**XNU 鍐呮牳宸插湪鐪熸満涓婅繘鍏ユ墽琛?*锛圖arwinBoot `exiting boot services` 鈫?`hand-off to the kernel`锛?> 褰撳墠宸ヤ綔锛氱粰鍐呮牳瑁?鍙鎬ф帰閽?锛堟妸榛戠鍙樼櫧绠憋級銆?> 鉁?娉ㄥ叆閾捐矾宸蹭慨濂藉苟 **CI 璺戦€?*锛圲niXNU `0c4e9a1` / unixnu-vince `b7642cf`锛宺un `39612555624` success锛?> 鏂瑰潡鏍囪 MARK1鈥? 宸查摼杩?`kernel.macho`锛夈€?> 鉁?鍚屾椂鏌ュ疄"鍐呮牳鏃犺緭鍑?鐨?*鐪熷洜**锛欴arwinBoot 鐨?`boot_args.Video` 琚敼鎴愪簡鏃ф暟缁勯『搴忥紝
> 涓庡唴鏍?`struct Boot_Video` 瀛楁閿欎綅锛堣瑙?**鍧?8 鏇存**锛夈€?> 猬?涓嬩竴姝ワ細**閲嶇紪鍥轰欢 + 鍒锋満鏁版柟鍧?*锛堢 7 鑺傜 5 姝ワ紝闇€瑕佹帴璁惧锛夈€?
---

## 0. 浠撳簱涓庝骇鐗╀綅缃?
| 椤?| 璺緞 |
|---|---|
| 鏈粨搴擄紙鏂囨。/鑴氭湰/kit锛?| `C:\Users\Administrator\Documents\unixnu-vince-gh` 鈫?https://github.com/Lux12138/unixnu-vince |
| UniXNU fork锛堝唴鏍告瀯寤鸿剼鏈級 | `C:\Users\Administrator\Documents\UniXNU` 鈫?https://github.com/Lux12138/UniXNU |
| 鍐呮牳/payload/闀滃儚浜х墿 | `C:\Users\Administrator\Desktop\unixnu-vince-kernel-ufs`锛?*鎵€鏈?vince-xnu64-*.img 閮藉湪杩欓噷**锛墊
| WSL锛堝浐浠舵瀯寤猴級 | `/root/Mu-Silicium`锛圗DK2/Mu UEFI锛夈€乣/root/UniXNU`锛堜笂娓革級銆乣/root/xnu`锛堢█鐤?clone 鐨?xnu 鍙傝€冿級|
| fastboot/adb | `C:\platform-tools` |
| git | `C:\Users\Administrator\.dsh-tools\PortableGit\cmd\git.exe` |
| gh | `C:\Program Files\GitHub CLI\gh.exe` |

> 鈿狅笍 鏄撻敊鐐癸細`Documents\unixnu-vince-kernel-ufs` 鍜?`Desktop\unixnu-vince-kernel-ufs` 閮藉瓨鍦紝
> **boot 闀滃儚鍦?Desktop 閭ｄ釜**锛屼箣鍓嶅娆″洜璺緞鍐欓敊瀵艰嚧 `No such file`銆?
---

## 1. 宸叉墦閫氱殑閾捐矾锛堢湡鏈洪€愰」楠岃瘉锛?
```
fastboot boot 鈫?BootShim 鈫?Mu UEFI 鈫?UniXNU 鑿滃崟 鈫?cust 鍒嗗尯 FAT payload
鈫?DarwinBoot 鈫?璇?51MB 鍐呮牳 鈫?瑙ｆ瀽 Mach-O 鈫?璇?ADT 鈫?ADT 鏍￠獙
鈫?鍒嗛厤绐楀彛 鈫?鏄犲皠娈?鈫?ExitBootServices 鈫?璺宠浆 XNU 鍐呮牳 鉁?```

鐪熸満鏃ュ織锛堝疄鎷嶏級锛?```
UNIXNU: runxnu entry vol=A2142798 path=\EFI\UniXNU\Payloads\kernel.macho cfgerr=
DB1 kernel read  Success size=0x3345000      (鈮?1.2MB锛屾敞鎰忔槸鍗佸叚杩涘埗鎵撳嵃)
DB2 kernel parse Success
DB3 adt read     Success size=0x330C
DB4 adt ok  win=0x130000000 keep=0 rd=ffffffffffffffff
DB6 va=0xFFFFFFF00427C000 pa=0x8007C000 args=0xC4364000
DARWINBOOT: inputs validated; exiting boot services
still-there kernel entry code ran
```

---

## 2. 纭潙涓庤В娉曪紙鎸夎俯鍧戦『搴忥級

### 鍧?1锛歀oad Error
- 璇垽杩?瀹樻敼 ABL 绂佺敤 boot"锛?*鐪熸鍘熷洜鏄?USB 绾?*
- 鍔ｈ川绾垮鑷村ぇ闀滃儚浼犺緭涓㈡暟鎹?鈫?ABL 鏍￠獙澶辫触
- 鉁?鎹㈠師瑁呮暟鎹嚎 + 涓绘澘鍚庨潰鏉?USB 鍙?
### 鍧?2锛歳amdisk 澶у皬鍖洪棿
| ramdisk | ABL | UEFI |
|---|---|---|
| 16 MB | 鉂?Load Error | 鈥?|
| 32 MB | 鉁?| 鉁?|
| 64 MB | 鉁?| 鉁?|
| 96 MB | 鉁?| 鉂?榛戝睆 |

鈫?**鍙敤鍖洪棿 32鈥?4MB**锛沗header_version=1`銆乣page_size=2048`

### 鍧?3锛氭瘡娆?boot 鍓嶅繀椤婚噸鍚澶?閲嶅惎鍚?*绗竴娆?boot 鎴愬姛鐜囨渶楂?*锛涜繛缁?boot 浼?Load Error锛坉ownload buffer 娈嬬暀锛夈€?
### 鍧?4锛氬唴鏍镐笉鑳藉杩涘浐浠跺嵎锛圥EI 瑙ｅ帇棰勭畻锛?| FVMAIN | 缁撴灉 |
|---|---|
| 8 MB锛堝師濮嬶級 | 鉁?|
| 62 MB锛堟湭鍘嬬缉鍐呮牳锛?| 鉂?|
| 15 MB锛圠ZMA 鍐呮牳锛?| 鉂?|

FD 鏈綋涓婇檺锛?*3MB 鍙敤锛?2MB/60MB 鍏ㄩ儴璧蜂笉鏉?*锛坄[uefi_fd] size` 淇濇寔 `0x300000`锛夈€?
### 鍧?5锛氭病鏈変换浣?FAT 鍗凤紙鏈€鏍规湰锛?鍥轰欢鑷甫瀛樺偍鏍堬紙`UFSDxe`/`PartitionDxe`/`DiskIoDxe`/`Fat`锛夛紝浣嗗畨鍗撳垎鍖哄叏鏄?ext4/f2fs 鈫?`Config->Volume=NULL` 鈫?DarwinBoot 鎶?`NULL input`銆?
鉁?**payload 鍒疯繘 `cust` 鍒嗗尯**锛?GB锛屽嚭鍘傝祫婧愬垎鍖猴紝涓嶅奖鍝嶇郴缁熷惎鍔級锛?```
\EFI\UniXNU\unixnu.toml
\EFI\UniXNU\Payloads\kernel.macho        (51MB)
\EFI\UniXNU\Payloads\kernel.macho.adt    (13KB)
```
鈿狅笍 鍒峰墠纭瀹屾暣锛歚Sending 'cust' (65536 KB)`锛涙浘琚埅鏂垚 1.2MB锛岃〃鐜颁负 `config error: unixnu.toml line 1: expected '='`

### 鍧?6锛欴arwinBoot 涓嶈 dispatch
鉁?骞惰繘 `Include/APRIORI.inc` 鐨?*绗竴涓?* `APRIORI DXE { }` 鍧楋紙鏂板紑鍧椾細 `GenFv ERROR 2000`锛?
### 鍧?7锛欰DT 鐨?RAMDisk 鍗犱綅绗﹀繀椤讳笌瀹為檯涓€鑷?```c
else if (RamdiskOffset != MAX_UINTN) { Status = EFI_UNSUPPORTED; goto Fail; }
```
鉁?鐢熸垚 ADT 鏃?*涓嶈** `--data-ramdisk` / `--packed-data-ramdisk`锛屼娇 `rd=ffffffffffffffff keep=0`

### 鍧?8锛歚boot_args.Video` 甯冨眬锛堚殸锔?涔嬪墠鐨勭粨璁烘湁閿欙紝瑙佷笅锛?`BootVideo.h` 鍘熷啓 `[base, 1, rowBytes, width, height, 32]`锛屽綋鏃惰涓?XNU 鏈熸湜
`[base, rowBytes, width, height, depth, display]`
鈫?鍐呮牳璇诲埌 `rowBytes=1 / depth=2560` 鈫?`initialize_screen()` 澶辫触 鈫?**闈欓粯鍒囧洖涓插彛**
鉁?鏀瑰啓杩囦竴娆★紙骞跺悓姝ユ敼 DarwinBoot 缁樺埗涓嬫爣锛夛紱DarwinBoot 渚ц嚜鎶?`base=0x50000000 row=6400 1600x2560 depth=32`

> **鈿狅笍 鏇存锛堟湰娆′細璇濇牳瀹烇級**锛歺nu-10063.141.1 鐨?`boot_args.Video` **涓嶆槸鏁扮粍**锛屾槸
> `struct Boot_Video`锛屽畾涔夊湪 `pexpert/pexpert/arm64/boot.h:31-38`锛?> ```c
> struct Boot_Video {
>     unsigned long v_baseAddr;  // [0]
>     unsigned long v_display;   // [1]  鈫?绗?2 涓紒涓嶆槸鏈€鍚庝竴涓?>     unsigned long v_rowBytes;  // [2]
>     unsigned long v_width;     // [3]
>     unsigned long v_height;    // [4]
>     unsigned long v_depth;     // [5]
> };
> ```
> 鑰?`pexpert/arm/pe_init.c:419-429` 鏄寜**瀛楁鍚?*閫愪釜鍙栫殑锛?> ```c
> PE_state.video.v_baseAddr = boot_args_ptr->Video.v_baseAddr;
> PE_state.video.v_display  = boot_args_ptr->Video.v_display;
> PE_state.video.v_rowBytes = boot_args_ptr->Video.v_rowBytes;
> PE_state.video.v_width    = ...->Video.v_width;
> PE_state.video.v_height   = ...->Video.v_height;
> PE_state.video.v_depth    = (...->Video.v_depth >> 0) & 0xFF;   // 浣?8 浣嶆墠鏄繁搴?> PE_state.video.v_rotate   = (v_depth>>8 & 0xFF) + (v_depth>>24 & 0xFF);
> PE_state.video.v_scale    = ((v_depth>>16) & 0xFF) + 1;
> ```
> 涔熷氨鏄锛?*濡傛灉 DarwinBoot 鐪熸寜 `[base, rowBytes, width, height, depth, display]` 鍐?*锛?> 鍐呮牳浼氳鍒?`v_display=rowBytes(闈?0锛屼簬鏄蛋 graphics)銆乿_rowBytes=width銆?> v_width=height銆乿_height=depth銆乿_depth=display浣嶆鍏?0` 鈥斺€?> **鏁存潯 video 鍙傛暟鍏ㄩ敊浣?*锛宍vcattach` 鎷垮埌鐨勮瀹?瀹介珮閮芥槸閿欑殑锛岃〃鐜板氨鏄?娌℃湁杈撳嚭"銆?>
> 鈬?杩?*灏辨槸**"鍐呮牳鍦?`PE_create_console` 涔嬪墠闈欓粯姝讳骸"鐨勭湡鍥狅紙宸叉牳瀹烇紝闈炴帹娴嬶級锛?> `vcattach` 鎷垮埌鐨?`v_rowBytes=1600`锛堢湡瀹?6400锛夈€乣v_width=2560`锛堢湡瀹?1600锛夈€?> `v_height=32`锛堢湡瀹?2560锛夈€乣v_depth=0` 鈥斺€?灞忓箷鍙傛暟鍏ㄩ敊锛屽浘褰?console 璧蜂笉鏉ャ€?>
> **鏍稿疄璇佹嵁閾?*锛?> 1. `pexpert/arm/pe_init.c:419-429` 鎸?*瀛楁鍚?*璇伙紙涓嶆槸鎸変笅鏍囨暟缁勮锛?> 2. `pexpert/pexpert/arm64/boot.h:31-38` 缁撴瀯浣撻『搴?= base, display, rowBytes, width, height, depth
> 3. `drivers/DarwinBoot/DarwinBootPkg/Driver/BootVideo.h` 鐨?`git diff` 鏄剧ず锛?>    **涓婃父鍘熺増鏈潵灏辨槸姝ｇ‘鐨勭粨鏋勪綋椤哄簭**
>    ```c
>    Video[0] = FrameBufferBase;              Video[1] = 1;      // v_display
>    Video[2] = RowBytes;                     Video[3] = HorizontalResolution;
>    Video[4] = VerticalResolution;           Video[5] = 32;
>    ```
>    鑰?鍧?8 淇"鎶婂畠鏀规垚浜?`Video[1]=RowBytes 鈥?Video[5]=0` 鈥斺€?**鏂瑰悜鏀瑰弽浜?*銆?> 4. `DarwinBoot.c` 鐨?`DiagDraw` 琚悓姝ユ敼鎴愮敤 `Video[1]` 褰?rowBytes锛堜篃鏄弽鐨勶級锛?>    鑰?`Video[2]*Video[4]`锛團B size锛夈€乣Video[3]/Video[4]`锛堝楂橈級绛夊叾瀹冭皟鐢ㄧ偣
>    **涓€鐩存槸缁撴瀯浣撹涔夈€佹病琚敼** 鈥斺€?鑷瘉鍘熷浠ｇ爜鏄鐨勩€?>
> 鉁?**宸插洖婊氾紙WSL `/root/UniXNU/drivers/DarwinBoot`锛?*锛?> - `git checkout -- DarwinBootPkg/Driver/BootVideo.h` 鈫?鎭㈠涓婃父缁撴瀯浣撻『搴?> - `DiagDraw` 鐨?5 澶勪笅鏍囨敼鍥?`Video[2]`=rowBytes / `Video[3]`=width / `Video[4]`=height
> - 鍏跺畠璋冪敤鐐癸紙`Video[2]*Video[4]`=FB size銆乣Video[3]`/`Video[4]`=瀹介珮銆?>   鏃ュ織閲岀殑 base/width/height/row/depth锛?*鏈潵灏辨槸缁撴瀯浣撹涔夛紝鏃犻渶鏀?*
>
> 鈬?**缁撹锛氫笂娓?HEAD 鐨?DarwinBoot 灏辨槸瀵圭殑銆備笉闇€瑕?patch銆佷笉闇€瑕?fork銆?*
> 瑕佸仛鐨勫彧鏄?鍒啀鎸夋暟缁勯『搴忔敼瀹?銆傞噸缂栧浐浠跺悗 `Video` 甯冨眬鍗充笌鍐呮牳涓€鑷淬€?
### 鍧?11锛氬唴鏍告棭鏈?*涓嶈兘**鍐欏抚缂撳啿锛堟帰閽堟浘缁忚嚜宸辨妸鍐呮牳鎵撴锛?`ExitBootServices` 涔嬪悗甯х紦鍐?*浠嶇劧鏄彲鍐欏彲瑙佺殑**锛堝凡鐢?DarwinBoot 鍙岃壊鎺㈤拡璇佹槑锛岃涓嬶級锛?浣嗛偅鏄?*鍦?UEFI 鐨勯〉琛ㄤ笅**銆傚唴鏍?`start.s` 涔嬪悗鐢ㄧ殑鏄唴鏍歌嚜宸辩殑椤佃〃锛宍0x50000000`
杩欎釜**鐗╃悊鍦板潃**鍦ㄥ唴鏍搁〉琛ㄩ噷娌℃湁鏄犲皠 鈥斺€?浜庢槸 `arm_init` 閲岄偅娆″啓**鐩存帴 fault**锛?鍐呮牳灏卞湴姝讳骸锛屽睆骞曚繚鎸佸師鏍凤紝鐪嬭捣鏉ュ拰"鍐呮牳娌¤窇"涓€妯′竴鏍枫€?
**鐥囩姸鐗瑰緛**锛氭湁鏃ュ織銆佹湁灞忓箷銆佹棤鏂瑰潡锛屼笖鍔犳爣璁板墠鍚庤涓轰笉鍙橈紙鍥犱负鏍囪鏈韩灏辨槸姝诲洜锛夈€?
鉁?**淇硶锛圲niXNU `9ad570c`锛?*锛?- `vince_mark_init()` 鍙竻鐘舵€侊紝**涓嶇 fb**
- `vince_MARK(n)` 鍙妸鍛戒腑璁拌繘 RAM 浣嶅浘 `g_hits`锛圧AM 蹇呯劧鍙啓锛?- `vince_mark_rebind()` 鎸傚湪 **`vcattach()` 鐨勬湯灏?*锛屼竴娆℃€ф妸鍛戒腑鍥炴斁鍒板睆骞?
> 鈿狅笍 **鏄犲皠鐐逛笉鏄?`PE_create_console()`锛?*锛堢涓€鐗堝氨閿欏湪杩欓噷锛岀櫧鍒蜂簡涓よ疆锛?> - `vcattach()` 鐢?**`PE_init_printf(TRUE)`** 璋冭捣锛坄pexpert/gen/pe_gen.c:135-140`锛?> - 鑰?`arm_init` 閲屽彧鏈?`PE_init_printf(FALSE)` 鈫?**`arm_init` 鏈熼棿 fb 浠庢湭琚槧灏?*
> - 鐪熸鐨勬槧灏勫湪 `vcattach` 鈫?`initialize_screen(NULL, kPEAcquireScreen)`
>   鈫?`ml_io_map_unmappable(...)`锛坄osfmk/console/video_console.c:2880`锛?>
> 鎵€浠ユ敞鍏ョ偣鍦?`vcattach` 鏀跺熬鐨?`}` 涔嬪墠锛屽苟涓斿姞浜嗕竴閬?*鍐呮牳 VA 瀹堝崼**锛?> ```c
> if ((unsigned long)PE_state.video.v_baseAddr >= 0xFFFFFFF000000000UL) {
>     vince_mark_rebind((const unsigned long *)&PE_state.video);
> }
> ```
> 鍦板潃杩樹笉鍍忓唴鏍?VA 灏?*璺宠繃**锛岀寽閿欎篃涓嶄細 fault銆?>
> **鍓骇鍝佺粨璁?*锛氭棦鐒?rebind锛堝湪 console 涔嬪悗锛夋浘鎶婂唴鏍告墦姝伙紝璇存槑**鍐呮牳纭疄鑳借窇鍒?> `PE_create_console` 涔嬪悗**鈥斺€旀瘮姝ゅ墠 HANDOVER 璁板綍鐨?姝诲湪 `PE_create_console` 涔嬪墠"杩滃緱澶氥€?
### 鍧?12锛氬睆骞曢《閮ㄧ豢鏉?*涓嶆槸** "kernel entry code ran"
`DarwinBoot.c` 閲岄偅鍙ユ彁绀烘槸閿欑殑銆傝瘉鎹細
1. `BootShim.S` 鍏ㄦ枃娌℃湁鐢荤豢鏉＄殑浠ｇ爜锛汳u-Silicium / UniXNU 涔熸悳涓嶅埌
2. 鍥涘紶瀹炴媿閲岀豢鏉￠珮搴︿笌瀛楀彿**姣斾緥鎭掑畾**锛屽彧鏄媿鎽勮窛绂讳笉鍚?3. A/B 鎺㈤拡瀹為獙璇佸疄锛氱豢鏉?*涓嬫柟**鐢荤殑绾㈠潡/缁垮潡閮借兘姝ｅ父鏄剧ず

鈬?缁挎潯鍙槸 UEFI 渚х殑鍥哄畾妯箙锛?*涓嶈兘**褰撳唴鏍歌繘搴︾敤銆傚垽璇诲彧鐪嬫柟鍧椼€?
#### A/B 鎺㈤拡瀹為獙锛堝喅瀹氭€э級
鍦?DarwinBoot 閲屽悓涓€娆″惎鍔ㄧ敾涓ゅ潡锛堥兘鍦ㄧ豢鏉′笅鏂?y=800锛夛細
| 鎺㈤拡 | 鏃舵満 | 缁撴灉 |
|---|---|---|
| 缁垮潡 (700,800) | `ExitBootServices` **涔嬪墠** | 鉁?鍑虹幇 |
| 绾㈠潡 (32,800) | `ExitBootServices` **涔嬪悗** | 鉁?鍑虹幇 |

鈬?浜ゆ鍚?fb 鍙啓鍙锛?*鎺掗櫎**"甯х紦鍐插け鏁?杩欐潯璺嚎銆?
### 鍧?10锛歚vince_mark_init(args->Video)` 缂栬瘧涓嶈繃锛堝凡淇級
```
error: passing 'Boot_Video' (aka 'struct Boot_Video') to parameter of
       incompatible type 'const unsigned long long *'
```
鉁?鏀逛负鎸夈€宍unsigned long` 瀛楁祦銆嶄紶锛歚vince_mark_init((const unsigned long *)&args->Video);`
鏍囪瀹炵幇鍚屾椂鏀寔涓ょ瑙ｉ噴锛堢粨鏋勪綋椤哄簭浼樺厛锛岃嚜鍔ㄥ洖閫€鏃ф暟缁勯『搴忥級锛?骞跺湪 `depth&0xFF != 32` 鎴栬蛋浜嗗洖閫€鏃?*鐢荤孩鍧?*锛屾妸甯冨眬闂鐩存帴鏆撮湶鍦ㄥ睆骞曚笂銆?
### 鍧?9锛欵L 涓嶆槸闂锛屽埆鍐嶆煡
- `ModuleEntryPoint.S` 鐨?`EL1_OR_EL2` 鍒嗘敮锛氳捣濮?EL2 鍒欑暀 EL2锛岃捣濮?EL1 鍒欑暀 EL1
- 瀹炴祴 `EL=4`锛圗L1锛夆啋 **ABL 鐢?EL1 浜や粯**锛?*寰€涓婅烦 EL 涓嶅彲鑳?*
- DarwinBoot 婧愮爜鏈韩瑕佹眰 EL1锛屼笌 UniXNU 璁捐涓€鑷?鉁?
---

## 3. 褰撳墠鍞竴鍗＄偣锛堟鍦ㄥ仛锛?
鍐呮牳宸茶烦杞墽琛岋紝浣?*鍦?`PE_create_console()`锛坅rm_init.c:616锛変箣鍓嶉潤榛樻浜?*锛屽睆骞曟棤浠讳綍鍐呮牳杈撳嚭銆?
### 瑙ｆ硶锛氬唴鏍告渶鏃╁叆鍙ｇ敾"鏂瑰潡妫€鏌ョ偣"
鍘熺悊锛歚boot_args.Video` 宸茬粰鍑哄抚缂撳啿锛屽唴鏍稿湪 `arm_init()` 鏈€寮€澶寸洿鎺ョ敾 48脳48 鑹插潡锛?*涓嶉渶瑕?console銆佷笉闇€瑕佸瓧搴?*銆?
| 鏂瑰潡鏁?| 棰滆壊 | 鍚箟 |
|---|---|---|
| 0 | 鈥?| 姝诲湪姹囩紪鍏ュ彛/MMU锛屾垨甯х紦鍐叉湭鏄犲皠 |
| 1 | 鐧?| 杩涗簡 `arm_init` |
| 2 | 榛?| 杩囦簡 `PE_init_platform` |
| 3 | 闈?| 杩囦簡 `PE_create_console` 鈫?**console 閫氫簡** |
| 4 | 缁?| 杩囦簡绗簩娆?`PE_init_platform` |

鏂瑰潡浠?`(32,32)` 璧枫€侀棿闅?64px銆佷笂闈㈡湁榛戣壊妯潯鑳屾櫙銆?
### 宸插疄鐜?- `kits/vince/vince_early_mark.{c,h}`锛堢函 C锛宍gcc -fsyntax-only` 閫氳繃锛?- `scripts/inject-early-marks.sh`锛?*鍙傝€冪敤**锛氭敞鍏ヤ换鎰忕粰瀹?xnu 婧愭爲锛汣I 涓嶅啀璋冪敤瀹冿級
- 鉁?**鏉冨▉瀹炵幇鍦?* `UniXNU/scripts/build-xnu-4k-baseline.sh`锛坈ommit `18ca785`锛夛細
  琛ヤ竵寰幆涔嬪悗娉ㄥ叆 `.cache/xnu-work`锛屽甫 pre-clean 鍙噸鍏ワ紝閿氱偣缂╄繘鏃犲叧锛孧ARK1鈥揗ARK4 榻愬叏

> `.github/workflows/build-kernel.yml` 閲屽師鏉ラ偅姝ャ€屾敞鍏?`refer/xnu`銆嶅凡鍒犻櫎鈥斺€旈偅妫垫爲涓嶅弬涓庣紪璇戯紝
> 鐣欑潃鍙細璇锛涙敼涓烘瀯寤哄悗鏂板 `Verify early checkpoint marks` 姝ラ锛岃嚜鍔ㄦ墦鍗?> `marks inserted` / `WARN: mark? anchor` / `llvm-nm` 绗﹀彿妫€鏌ヤ笁浠借瘉鎹€?
### 娉ㄥ叆韪╁潙鍙诧紙閲嶈锛侊級
1. CI 鐙珛姝ラ 鈫?`refer/xnu` 涓嶅瓨鍦紙**refer 婧愬欢杩熸媺鍙?*锛宍tree.py` 娉ㄩ噴 `fetched when a step needs it`锛?2. 鏀捐繘 Build kernel 姝ラ 鈫?`ls refer/` 鏄剧ず `total 0`
3. 鏀捐繘鏋勫缓鑴氭湰銆佷絾**鍦?`if [ ! -d refer/xnu/.git ]; then` 鍧楀唴** 鈫?CI 宸?fetch 杩囷紝鍧楄璺宠繃
4. 绉诲嚭 if 鍧?鈫?PowerShell `Set-Content -Encoding UTF8` 鍐欏叆 **BOM+CRLF** 鈫?bash 瑙ｆ瀽澶辫触锛堝凡鐢?Python 褰掍竴鎴?LF锛?5. 娉ㄥ叆鍒?`refer/xnu` 鈫?涓嶇敓鏁堬紝**鐪熸鏋勫缓鐩綍鏄?`.cache/xnu-work`** 鉁?宸叉敼
6. 鏀瑰埌 `.cache/xnu-work` 鈫?CI **failure**锛氭敞鍏ユ敼浜?`arm_init.c`锛屼笌鍚庣画 `git apply` 瀹樻柟琛ヤ竵**鍐茬獊**
   鈫?鉁?**宸蹭慨**锛氭敞鍏ュ潡绉诲埌琛ヤ竵寰幆 `done`锛堢113琛岋級**涔嬪悗**锛屽苟鍔犱簡 pre-clean 鍙嶅悜娓呯悊
   锛坄native-4k-user-abi.patch`銆乣zzz-boot-progress.patch` 鏀?`osfmk/arm/arm_init.c`锛?   `source-machine-layer.patch` 鏀?`osfmk/conf/files.arm64`锛?7. 閿氱偣鍘熸潵鏄?`assert`锛屽疄娴嬪彂鐜?*缂╄繘鏁忔劅**锛坄\t` vs 绌烘牸锛変細璇垽
   鈫?鉁?鏀逛负**缂╄繘鏃犲叧姝ｅ垯** + 鏃犲尮閰嶅彧 `print WARN` 涓嶄腑鏂紱`#include` 閿氱偣缂哄け鏃跺洖钀藉埌鏈€鍚庝竴涓?`#include` 琛?8. 鍐呮牳鏋勫缓浼氳窇**涓ら亶**鑴氭湰锛坆ootstrap pass 鍑虹紪璇戣褰?鈫?鐪熸鐨?pass锛夛紝鍚屼竴 `.cache/xnu-work`
   鈫?鉁?pre-clean 璁╂敞鍏ュ彲閲嶅叆锛坄MKU` 鍏堟挙銆乣MKP` 鍐嶆敞锛夛紝CI 澶嶇敤宸ヤ綔鏍戜篃涓嶄細姹℃煋琛ヤ竵涓婁笅鏂?
### 楠岃瘉娉ㄥ叆鏄惁鐢熸晥
- 鉂?鍒彧鐪?CI 鎺у埗鍙帮紙鑴氭湰 stdout 琚噸瀹氬悜杩涗骇鐗╋級
- 鉁?鏌ヤ骇鐗?`kernel.log`锛歚marks inserted` / `vince_early_mark`
- 鉁?鏌?`kernel.macho` 浜岃繘鍒跺惈 `vince_mark`

---

## 4. 鍏抽敭婧愮爜閿氱偣锛坸nu-10063.141.1 / commit d8b80295锛屽凡楠岃瘉锛?
| 鏂囦欢 | 琛?| 鍐呭 |
|---|---|---|
| `osfmk/arm/arm_init.c` | 199 | `void arm_init(boot_args * args);` |
| | 370 | `PE_init_platform(FALSE, args);` 鈫?MARK1 閿氱偣 |
| | 616 | `PE_create_console();` 鈫?MARK2/3 閿氱偣 |
| | 619 | `PE_init_printf(FALSE);` |
| `pexpert/arm/pe_init.c` | 425-436 | 浠?`boot_args.Video` 濉?`PE_state.video`锛堥€氱敤 arm64锛墊
| `pexpert/gen/pe_gen.c` | 135 | `PE_init_printf(boolean)`锛坄TRUE`鈫抳cattach锛墊
| `osfmk/conf/files.arm64` | 51 | `osfmk/arm/arm_init.c	optional config_pmap_ppl`锛堟柊鏂囦欢鐓ф鏍煎紡杩藉姞锛墊

鏋勫缓鑴氭湰 `UniXNU/scripts/build-xnu-4k-baseline.sh`锛堣鍙锋寜 commit `18ca785`锛夛細

| 琛?| 鍐呭 |
|---|---|
| 13 | `if [ ! -d refer/xnu/.git ]; then git clone ...; fi`锛坮efer 婧愶紝**涓嶅弬涓庣紪璇?*锛墊
| 21 | `if [ ! -d .cache/xnu-work/.git ]; then git clone --shared refer/xnu .cache/xnu-work; fi` |
| 40-66 | **vince pre-clean锛圡KU锛?*锛氭挙鎺変笂涓€娆℃敞鍏ワ紝淇濊瘉琛ヤ竵 `apply --check` 涓婁笅鏂囧共鍑€ |
| 76-81 | **琛ヤ竵搴旂敤寰幆**锛坄done` 鍦ㄧ 81 琛岋級|
| 82-169 | **vince 娉ㄥ叆鍧楋紙MKP锛?*锛氬啓 `vince_early_mark.{c,h}` + `files.arm64` + `arm_init.c` 鍥涗釜 MARK |
| 992 | `make -C .cache/xnu-work "${XNU_BUILD_TARGET:-build}" ...`锛堢湡姝ｇ紪璇戯級|

> 鈿狅笍 娉ㄥ叆**蹇呴』**鍦ㄨˉ涓佸惊鐜箣鍚庯細`native-4k-user-abi.patch` 涓?`zzz-boot-progress.patch` 閮芥敼
> `osfmk/arm/arm_init.c`锛宍source-machine-layer.patch` 鏀?`osfmk/conf/files.arm64`銆?> 鍙﹀鍐呮牳鏋勫缓浼氳窇**涓ら亶**鑴氭湰锛坆ootstrap pass + 姝ｅ紡 pass锛夛紝鎵€浠?pre-clean 鏄繀闇€鐨勶紝涓嶆槸鍙€夈€?
---

## 5. 纭欢瀹炴祴鏁版嵁

| 椤?| 鍊?|
|---|---|
| DRAM | 12 GiB |
| **RPMh RSC** | **`0x18200000` 脳3 bank** |
| IPCC/apss_shared | `0x17c00000`锛?*鍙槸 mailbox锛屼笉鏄?RPMh**锛墊
| cmd-db / SMEM | `0x85f20000` / `0x86000000` |
| SPMI / PDC | `0xc440000` / `0xb220000` |
| GCC | `0x100000 +0x1f0000`锛坄#clock-cells=1`锛墊
| UFS HC / PHY | `0x1d84000`锛坕ce `0x1d90000`锛? `0x1d87000` |
| 鏃堕棿鍩哄噯 | 19200000 Hz |
| cust 鍒嗗尯 | `0x40000000`锛?GB锛墊
| CPU | `reg 0x0..0x700`锛宲sci锛宬ryo485锛堜笌 ADT `--cpu-regs` 涓€鑷达級|
| UFS 渚涚數 | vcc 2.504鈥?.95V(L10A)銆乿ccq 1.2V(L9A)銆乿ccq2 1.8V(S4A)銆乿dda-phy 0.88V(L5A)銆乿dda-pll 1.2V(L3C) |
| PMIC | pm8150=0銆乸m8150b=2銆乸m8150l=4锛?*鏃?pm8009**锛墊

---

## 6. 鍛戒护閫熸煡

```bash
# ADT锛堝姟蹇呬笉甯?RAMDisk 鍗犱綅绗︼級
python3 UniXNU/scripts/make-vince-adt.py --dram-size 0x300000000 \
  --owned-memory-size 0x130000000 --cpu-regs "0,0x100,0x200,0x300,0x400,0x500,0x600,0x700" \
  --ipad-identity --chip-id 0x207 --unique-chip-id 0x0000000000000001 --output kernel.macho.adt

# cust payload
bash unixnu-vince-gh/scripts/make-cust-payload.sh kernel.macho kernel.macho.adt cust-payload.img

# 鍒?+ 鍚紙闇€ fastboot锛?fastboot flash cust cust-payload.img
fastboot boot C:\Users\Administrator\Desktop\unixnu-vince-kernel-ufs\vince-xnu64-T.img

# 鍥轰欢锛圵SL锛?cd /root/Mu-Silicium && python3 build_uefi.py -d vince -r DEBUG
```

**鎭㈠**锛氶暱鎸夌數婧愰敭 10 绉掞紱鍏ㄧ▼**鍙啓杩?`cust`**锛宍abl`/`xbl`/`bootloader` 浠庢湭鍒疯繃銆?
---

## 7. 涓嬩釜浼氳瘽绗竴浠朵簨锛堟寜椤哄簭锛?
> 鉁?1鈥? 宸插畬鎴愶紙commit `18ca785` @ UniXNU main锛夈€?*浠庣 4 姝ユ帴鐫€鍋氥€?*

| # | 浜嬮」 | 鐘舵€?|
|---|---|---|
| 1 | 娉ㄥ叆鍧楃Щ鍒拌ˉ涓佸惊鐜?`done` 涔嬪悗 | 鉁?瀹屾垚 |
| 2 | `assert` 鏀瑰閿欙紙骞跺崌绾т负缂╄繘鏃犲叧姝ｅ垯锛?| 鉁?瀹屾垚 |
| 3 | `bash -n` 鏍￠獙 鈫?commit/push UniXNU 鈫?瑙﹀彂 CI | 鉁?瀹屾垚锛坄18ca785`锛墊
| 3.5 | 棣栬疆 CI 淇敞鍏ュ啿绐?鈫?鏆撮湶缂栬瘧閿欒 鈫?鍐嶄慨 | 鉁?瀹屾垚锛堣涓嬶級|
| 4 | 涓嬭浇浜х墿 鈫?鏌ユ棩蹇?绗﹀彿 | 鉁?瀹屾垚锛坮un `39612555624` success锛墊
| 4.5 | 鏌ョ湡鍥狅細`boot_args.Video` 甯冨眬閿欎綅 | 鉁?纭锛堣鍧?8 鏇存锛墊
| 5 | 閲嶇紪鍥轰欢锛堜慨 Video锛夆啋 閲嶆墦 cust payload 鈫?鍒?+ 鍚?鈫?鏁版柟鍧?| 馃攧 绗?1 杞凡鍒凤細鏂瑰潡 **0**锛堣涓嬶級锛屽凡涓嬫矇 MARK1 绛夌 3 杞唴鏍?|
| 6 | 鑻ユ柟鍧?0锛氭敼"鍐欏彲鍐?RAM + DarwinBoot 鍥炶" | 猬?鏉′欢瑙﹀彂 |

### 绗?5 姝ュ疄娴嬶紙鐪熸満閫愯疆锛?
| 杞 | 鍐呮牳渚ф敼鍔?| 灞忓箷缁撴灉 | 缁撹 |
|---|---|---|---|
| 1 | MARK1鈥?锛岀洿鎺ュ啓鐗╃悊 fb | **0 鍧?* | 鎺㈤拡鑷繁 fault锛坒b 鏈槧灏勶級|
| 2 | MARK1 涓嬫矇鍒?`arm_init` 鍏ュ彛 | 0 鍧?| 鍚屼笂 |
| 3 | 鏃╂湡鍙 RAM锛宍PE_create_console` 鍚?rebind | 0 鍧?| 杩欐椂 fb 浠嶆湭鏄犲皠 |
| 4 | rebind 鎸傚埌 `vcattach` 鏈熬 | 0 鍧?| 鍐呮牳娌¤蛋鍒?`vcattach` |
| 5 | **`vince_mark_map()` 鐢?`ml_io_map_unmappable` 鑷缓鏄犲皠** | **5 鍧?* 鉁?| `arm_init` 涓诲共璺戦€?|
| 6 | 瀹炴椂閲嶇敾 + MARK7锛坄machine_startup` 鍓嶏級+ MARK8/9锛坄kernel_bootstrap`锛墊 **8 鍧?* 鉁呪渽 | **瓒婅繃 `machine_startup`锛岃繘浜?`kernel_bootstrap()`** |

**绗?6 杞殑鍏抽敭鍒よ**锛? 鍧?= MARK1鈥? 鍏ㄩ儴鍛戒腑锛屽嵆
`arm_init` 瀹屾暣璺戝畬 鈫?`machine_startup(args)` 鈫?杩涘叆 `kernel_bootstrap()`銆?浣嗙 9 鍧楋紙`PE_init_iokit()` 涔嬪悗锛夋病鏈夊嚭鐜帮紝涓?*灞忎笂娌℃湁鍐呮牳鏂囧瓧** 鈥斺€?鈬?姝讳骸鐐归攣瀹氬湪 **`PE_init_iokit()` 鍐呴儴**锛屼篃灏辨槸 `PE_init_printf(TRUE)` 鈫?`vcattach`
鈫?`initialize_screen(NULL, kPEAcquireScreen)` 杩欐潯 console 鍒濆鍖栭摼璺笂銆?
> 鈿狅笍 **杩欏交搴曟帹缈讳簡"鍐呮牳鍦?`PE_create_console` 涔嬪墠灏遍潤榛樻浜?鐨勬棫缁撹銆?*
> 鍐呮牳瀹為檯鑳借窇鍒?`kernel_bootstrap`锛屼箣鍓嶇湅涓嶅埌浠讳綍杈撳嚭锛岀函绮规槸
> **娌′汉缁欏唴鏍告棭鏈熸槧灏勬樉瀛?*锛堣鍧?11锛夈€?
**宸查噰鍙?*锛氭柊澧?4 涓帰閽堟妸 `PE_init_iokit` 鍐呴儴鍒囧紑锛圲niXNU `cb2a921`锛夛細
```
10 = PE_init_iokit 鍏ュ彛
11 = vcattach 鍏ュ彛
12 = initialize_screen(NULL, kPEAcquireScreen) 涔嬪悗
13 = PE_init_printf(TRUE) 涔嬪悗
```

鏂瑰潡璇箟锛坴4锛氬疄鏃堕噸鐢伙紝13 涓Ы浣嶏級锛?
> 鈿狅笍 缁挎潯涓嶆槸杩涘害淇″彿锛堣鍧?12锛夈€傚彧鏁版柟鍧椼€?> 鏂瑰潡浼氬湪姣忔鍛戒腑鏃?*绔嬪埢鍒锋柊**锛屾墍浠ュ睆骞曟樉绀虹殑灏辨槸鍐呮牳鐨勫綋鍓嶆渶鏂颁綅缃€?
| 鏂瑰潡鏁?| 鏈€杩滃埌杈?|
|---|---|
| 0 | `arm_init` 鏃╂湡锛堟垨 `vince_mark_map` 涔嬪墠锛墊
| 5 | 绗簩娆?`PE_init_platform` 涔嬪悗 |
| 6 | `arm_vm_init` + 鑷槧灏勬垚鍔?|
| 7 | `machine_startup(args)` 涔嬪墠 鈫?**`arm_init` 璺戝畬** |
| 8 | 杩涘叆 `kernel_bootstrap()` |
| 9 | 杩囦簡 `PE_init_iokit()` |
| 10 | 杩涘叆 `PE_init_iokit()` |
| 11 | 杩涘叆 `vcattach()` |
| 12 | `initialize_screen(kPEAcquireScreen)` 涔嬪悗 |
| 13 | `PE_init_printf(TRUE)` 涔嬪悗 鈫?**console 瀹屽叏灏辩华** |
| 闄勫姞绾㈠潡 | 鍙充笂瑙掔嫭绔嬬孩鍧?= Video 甯冨眬/娣卞害鍙枒锛堝浐浠舵病鐢熸晥锛墊

### 绗?4 姝ラ獙璇佺粨鏋滐紙run `39612555624`锛宻uccess锛?```
鈶?琛ヤ竵鍐茬獊锛氭棤 patch failed / does not apply
鈶?娉ㄥ叆璁板綍锛?   kernel-bootstrap.log : marks inserted: MARK1=True MARK2=True MARK3=True MARK4=True
   kernel.log           : vince pre-clean: reverted .cache/xnu-work/osfmk/arm/arm_init.c
                          vince pre-clean: reverted .cache/xnu-work/osfmk/conf/files.arm64
                          marks inserted: MARK1=True MARK2=True MARK3=True MARK4=True
   鈫?涓ら亶鑴氭湰銆乸re-clean 鐢熸晥銆佺浜岄亶閲嶆柊娉ㄥ叆姝ｇ‘锛氳璁￠獙璇侀€氳繃
鈶?绗﹀彿锛坘ernel.macho 53,760,000 B锛夛細_vince_mark 脳6銆乢vince_mark_init 脳2
```

### 绗?3.5 姝ワ細棣栬疆 CI 缁撴灉锛堣褰曞湪妗堬級
- run `39611266428` **failure**锛屼絾**涓嶅啀鏄ˉ涓佸啿绐?*鈥斺€斿啿绐佸凡淇ソ銆?  璇佹嵁锛歚zzz-boot-progress.patch` 鐨?`apply --check` 鍏ㄨ繃绋嬫棤 `patch failed`銆?- 鏂伴敊璇槸缂栬瘧鏈燂細
  `arm_init.c:373: passing 'Boot_Video' to parameter of incompatible type 'const unsigned long long *'`
  鈫?瑙?*鍧?10**锛歚args->Video` 鏄?`struct Boot_Video`锛屼笉鏄暟缁勩€?- 鍚屾椂鐢?`pexpert/arm/pe_init.c:419-429` 鍙嶆煡鍑?*鍧?8 鐨勭粨璁烘湁璇?*锛坉isplay 鍦ㄧ 2 浣嶏級锛?  宸插湪璇ヨ妭鍐欐洿姝ｄ笌寰呮牳瀹為」銆?- 淇硶锛氫紶 `(const unsigned long *)&args->Video`锛屽疄鐜板涓ょ甯冨眬鑷€傚簲锛屽竷灞€鍙枒鏃剁敾绾㈠潡銆?
### 绗?4 姝ワ細纭娉ㄥ叆鐪熺殑杩涗簡浜岃繘鍒?
瑙﹀彂鏂瑰紡锛坵orkflow_dispatch锛宍build-kernel.yml`锛夛細
```bash
gh workflow run build-kernel.yml --repo Lux12138/unixnu-vince
gh run watch --repo Lux12138/unixnu-vince
gh run download --repo Lux12138/unixnu-vince -n kernel-vince -D /tmp/vince-kernel
```

涓夊璇佹嵁锛?*鏂板鐨?`Verify early checkpoint marks` 姝ラ宸茬粡鎶婅繖涓夋潯鎵撳ソ浜?*锛夛細

```bash
# 鈶?澧為噺琛ヤ竵骞插噣搴旂敤锛堟病鏈?apply 澶辫触 = 娉ㄥ叆娌″拰琛ヤ竵鎵撴灦锛?grep -a 'error: patch failed' /tmp/vince-kernel/logs/kernel.log || echo clean
# 鈶?娉ㄥ叆璁板綍锛氬繀椤荤湅鍒?MARK1..MARK4 鍏?True
grep -a 'marks inserted' /tmp/vince-kernel/logs/kernel.log
# 鏈熸湜: marks inserted: MARK1=True MARK2=True MARK3=True MARK4=True
# 鑻ュ嚭鐜?WARN: mark? anchor missing 鈫?涓婃父婧愮爜閿氱偣婕傜Щ锛屾寜绗?4 鑺傝鍙烽噸鏂版牳瀵?# 鈶?绗﹀彿鐪熺殑閾捐繘鍐呮牳
xcrun llvm-nm --defined-only /tmp/vince-kernel/kernel/kernel.macho | grep vince_mark
# 鏈熸湜: 涓よ _vince_mark / _vince_mark_init锛圱锛?```
鈿狅笍 **鍒彧鐪?CI 鎺у埗鍙?*锛堣剼鏈?stdout 琚噸瀹氬悜杩?`out/vince/logs/kernel.log`锛夛紱
`kernel-bootstrap.log` 鏄?bootstrap pass 鐨勬棩蹇楋紝涓ら亶閮戒細璺戞敞鍏ワ紝涓ら亶閮借鍑虹幇 `marks inserted`銆?
### 绗?5 姝ワ細鍒锋満 + 鏁版柟鍧?
**5a. 閲嶇紪鍥轰欢锛堝繀椤诲厛鍋氾紒鍚﹀垯 Video 浠嶆槸閿欑殑锛?*
DarwinBoot 宸插洖婊氬埌涓婃父姝ｇ‘鐗堟湰锛岄噸缂栧嵆鐢熸晥锛?```bash
wsl -e bash
cd /root/Mu-Silicium && python3 build_uefi.py -d vince -r DEBUG
cd /root/UniXNU && ./unixnu bootimg        # 鎵撳寘鎴?Android boot 闀滃儚锛圲EFI FD + dtb + ramdisk锛?```
浜х墿鎸夋棦鏈夊懡鍚嶉€掑锛堝綋鍓嶆渶鏂?`vince-xnu64-T.img`锛屼笅涓€涓缓璁?`-U`锛夛紝鏀惧埌
`C:\Users\Administrator\Desktop\unixnu-vince-kernel-ufs\`銆?
**5b. 閲嶆墦 cust payload锛堝唴鏍镐晶锛?*
```bash
# ADT锛堝姟蹇呬笉甯?RAMDisk 鍗犱綅绗︼級
python3 UniXNU/scripts/make-vince-adt.py --dram-size 0x300000000 \
  --owned-memory-size 0x130000000 --cpu-regs "0,0x100,0x200,0x300,0x400,0x500,0x600,0x700" \
  --ipad-identity --chip-id 0x207 --unique-chip-id 0x0000000000000001 --output kernel.macho.adt
bash unixnu-vince-gh/scripts/make-cust-payload.sh kernel.macho kernel.macho.adt cust-payload.img
```
`kernel.macho` 鐢?CI 浜х墿 `C:\Temp\vince-ok\kernel\kernel.macho`锛坮un `39612555624`锛夈€?
**5c. 鍒?+ 鍚?*锛堝埛鍓嶇‘璁?`Sending 'cust' (65536 KB)`锛屽埆琚埅鏂級
```bash
fastboot flash cust cust-payload.img
fastboot boot C:\Users\Administrator\Desktop\unixnu-vince-kernel-ufs\vince-xnu64-U.img
```
**姣忔 boot 鍓嶅厛闀挎寜鐢垫簮 10 绉掗噸鍚?*锛堝潙 3锛夈€?
**鍒よ鏂板鐨?绾㈠潡"淇″彿**锛氳嫢鍙充笂瑙掞紙绗?8 妲斤級鍑虹幇绾㈠潡锛岃鏄庡唴鏍镐晶璁や负
`Video` 甯冨眬浠嶇劧瀵逛笉涓?鈥斺€?閭ｆ剰鍛崇潃鍥轰欢娌￠噸缂栨垚鍔燂紝鑰屼笉鏄抚缂撳啿闂銆?
鏂瑰潡璇箟锛坴3锛氭棭鏈熷彧璁?RAM锛宍PE_create_console` 涔嬪悗涓€娆℃€у洖鏀撅紱浠?`(32,32)` 璧枫€侀棿闅?64px锛夛細

> 鈿狅笍 **缁挎潯涓嶆槸杩涘害淇″彿**锛堣鍧?12锛夈€傚彧鏁版柟鍧椼€?> 鍥犱负 `PE_create_console` 涔嬪墠鏃犳硶鍐欏睆锛?*"0 鍧?鍙兘璇存槑"姝诲湪 console 涔嬪墠"锛?> 鏃犳硶鍐嶇粏鍒?*鈥斺€旇繖鏄綋鍓嶈娴嬫墜娈电殑纭檺鍒躲€?
| 鏂瑰潡鏁?| 棰滆壊 | 鍚箟 |
|---|---|---|
| **0** | 鈥?| 姝诲湪 `PE_create_console()` 涔嬪墠锛坄arm_init` 鏃╂湡 / JOP 绛惧悕 / `arm_vm_init`锛墊
| 4 | 鐧介粍闈掔豢 | 鍒颁簡 `PE_create_console()`锛屼笖 1/2/3 鍏ㄩ儴缁忚繃锛堟甯告儏鍐碉級|
| 5 | +鍝佺孩 | 鍏ㄨ繃锛屽寘鎷浜屾 `PE_init_platform` |
| 闄勫姞绾㈠潡 | 绾?| 鍙充笂瑙掔嫭绔嬬孩鍧?= Video 甯冨眬/娣卞害鍙枒锛堝浐浠舵病鐢熸晥锛屾垨 fallback 鐢熸晥锛墊
| 鍙湁 1~3 鍧?| 鈥?| 涓嶄細鍑虹幇锛氬洖鏀句竴瀹氫細鎶婂凡鍛戒腑鐨勫叏閮ㄧ敾鍑猴紝缂哄彿璇存槑浣嶅浘/鍑犱綍鏈夐棶棰?|

### 绗?6 姝ワ紙浠呮柟鍧?0 鏃讹級
`Video` 鍩哄潃鍦ㄥ唴鏍告棭鏈熼〉琛ㄩ噷娌℃湁鏄犲皠锛堝唴鏍?start.s 娌跨敤 UEFI 椤佃〃锛屼絾鍙繚璇?RAM 鍖哄煙锛夛紝
鎵€浠?`vince_mark_init` 鐨勫啓浼?fault銆備袱涓柟鍚戯細
1. **鍏堢‘璁?fb 鏄惁鐪熺殑涓嶅彲鍐?*锛氳 DarwinBoot 鍦?`ExitBootServices` 涔嬪悗銆乣DarwinEnter` 涔嬪墠
   鐢ㄨ嚜宸卞凡楠岃瘉杩囩殑 fb 鐢讳竴涓?浜ゆ鍧?銆傚睆骞曚笂鍑虹幇浜ゆ鍧椾絾**娌℃湁** MARK1 鈬?鍐呮牳渚?fb 涓嶅彲鍐欙紙纭瘖锛夈€?2. **鏀圭敤 RAM 浼犻€?*锛歚arm_init` 鏃╂湡鍙啓闈欐€佸彉閲忥紙bss 蹇呯劧鍙啓锛夛紝
   鍦?`arm_vm_init` 涔嬪悗鐢?pmap 鏄犲皠 fb锛屽啀涓€娆℃€?flush 鍏ㄩ儴妫€鏌ョ偣鍒板睆骞曘€?
### 澶囬€夛紙鑻ユ爣璁拌矾绾垮彈闃伙級
- B锛欴arwinBoot 鍦?EL2 浜や粯锛堥渶 EL 鍒囨崲锛屾敼鍔ㄥぇ锛?- C锛歎ART 115200锛堥渶鎷嗘満锛?*鐢ㄦ埛涓嶆帴鍙?*锛?- D锛氬唴鏍告棭鏈?console 璧?GOP锛坄vcattach` 鍦?`PE_create_console` 涔嬪悗鎵嶇敓鏁堬紝鏁戜笉浜嗘洿鏃╂浜★級

---

## 8. 鏂囨。绱㈠紩

| 鏂囦欢 | 鍐呭 |
|---|---|
| `README.md` | 鎴樻姤锛氶摼璺?+ 鍧?+ 澶嶇幇 |
| `HANDOVER.md` | 鏈枃妗?|
| `docs/firmware-patches.md` | 鍥轰欢鏀瑰姩娓呭崟 + 宸茬煡鏃犳晥灏濊瘯 |
| `docs/vince-dts-extract.md` | DTS 钂搁锛圧PMh 鍦板潃绾犻敊 + UFS/PMIC/鏃堕挓锛墊
| `docs/pmgr-plan.md` | PMGR 璁″垝 + RPMh 鏈€灏忚閫氳矾 |
| `docs/early-console-plan.md` | 鏃╂湡 console + 鏂瑰潡妫€鏌ョ偣鏈哄埗 |
| `docs/prior-art-0xDive-ios-vince.md` | 鍚岀被椤圭洰瀵规瘮 |
| `kits/vince/vincePlatformPower.cpp` | PMGR 楠ㄦ灦 |
| `kits/vince/vince_early_mark.{c,h}` | 鏂瑰潡妫€鏌ョ偣锛堢函 C锛墊
| `scripts/make-cust-payload.sh` | cust payload 鐢熸垚 |
| `scripts/inject-early-marks.sh` | 鏍囪娉ㄥ叆鍣?|

---

## 13. xnu-10063 鍚姩鍋滃湪 mig_init锛堟湰杞畾浣嶇粨璁猴級

### 浜嬪疄閾撅紙鍏ㄩ儴鏈夌‖浠惰瘉鎹級

| 妫€鏌ョ偣 | 璇绘暟 | 鍚箟 |
|---|---|---|
| `vince_MARK(8)` | 8 | 杩涘叆 `kernel_bootstrap` |
| 鑷姩缂栧彿 18..44 | 26 | 璧板埌 `mac_policy_init` |
| 45 / 46 | **45** | `mac_policy_init()` 杩斿洖锛沗kernel_startup_initialize_upto(STARTUP_SUB_MACH_IPC)` 鍐呭穿 |
| 瀛愮郴缁?+ 鏉＄洰 | 13 / 27 | MACH_IPC 杞 28 涓潯鐩?|
| `cur->func` 鏁ｅ垪 | 56 鈫?50 | 涓ょ増宸ュ叿閾句笅閮藉敮涓€鏄犲皠鍒?**`_mig_init`** |
| `mig_e[i]` 绱㈠紩 | **0** | `_mach_vm_subsystem` |
| 渚嬬▼绱㈠紩 j | **0** | `mach_vm_allocate`锛坢sgid 4800锛?|
| stub 鎸囬拡鏁ｅ垪 | 19 | `0x...153c >> 4 & 0x3F`锛屼笌闈欐€?dump 涓€鑷?鈫?kstub **闈為浂** |

`mig_init()` 鐨勪簲涓?panic 鍒嗘敮涓紝瑙﹀彂鐨勬槸锛?
```c
panic("kroutine must have precise size %d %d", mig_e[i]->start, j);
```

鍗?`mach_vm_allocate` 鐨?`max_reply_msg == 0`銆備絾 `mach_vm.defs` 閲屽畠鏈?`out` 鍙傛暟锛?鎻忚堪绗?*鐞嗗簲**甯﹀洖澶嶅昂瀵?鈥斺€?鎵€浠ユ槸**鏋勫缓鏈?mig 鐢熸垚鐜妭涓簡璇ュ瓧娈?*锛屼笉鏄畾涔夐棶棰樸€?
### 宸叉帓闄?
- 閲嶅娉ㄥ唽锛?1 涓?ops銆?1 涓敮涓€ `iko_op_type`
- 鏁扮粍瓒婄晫锛歚__init_entry_set` 95856 B = 3994脳24锛沗ipc_kobject_ops_array` 1728 B = 54脳32
- 宸ュ叿閾剧増鏈細`picked: /Applications/Xcode_15.0.app` 鍚庝粛鍋滃湪鍚屼竴涓?panic
- 鎴戜滑鐨勮ˉ涓侊細patch 闆嗛噷娌℃湁浠讳綍 `IKOT` / `mig` 鏀瑰姩
- 璺?boot RAM 浼犻€掞細`keep probe` 绗簩娆″惎鍔ㄤ粛鏄?`fresh RAM`锛孌RAM 涓嶄繚鐣?
### 閲囩敤鐨勫缃?
鎶?panic 鏀逛负鍥為€€锛?
```c
} else {
    mig_buckets[pos].kreply_size = mig_e[i]->maxsize;   /* 淇濆畧鍊?*/
    mig_buckets[pos].kreply_desc_cnt =
        mig_e[i]->kroutine[j].reply_descr_count;
}
```

灞炰簬**鍔″疄缁曡繃**锛堝昂瀵稿亸澶у彧娴垂鍐呭瓨锛宲anic 鍒欎涪鏁翠釜鍚姩锛夈€傚壇浣滅敤涓庨殣鎮ｏ細
鍥炲缂撳啿鍖烘寜瀛愮郴缁熸渶澶у€硷紙mach_vm 涓?4140 B锛夊垎閰嶏紝鑻ュ悗缁嚭鐜?kalloc 鍘嬪姏鎴?reply 瑙ｆ瀽寮傚父锛屽簲浼樺厛鎬€鐤戞澶勩€?
### 鎺㈤拡缁忛獙锛堥伩鍏嶅啀韪╋級

- framebuffer 鍦?`arm_init` 鍏ㄧ▼**鏈槧灏?*锛沗ml_io_map_unmappable` 鑷缓鏄犲皠鍚庢墠鍙啓
- 鏂瑰潡鏉℃渶澶?24 鏍间笖鎸夌紪鍙?*浠庡皬鍒板ぇ**鐢伙紝鏅氭湡鐨?45/46/50/60 浼氳鎸ゆ帀锛堝凡鏀逛负鐢绘渶鏂?24 涓級
- `draw_number` 蹇呴』鐢诲墠鎿︽牸锛屽惁鍒欏崄浣嶆畫鐣欙紙50 浼氳璇绘垚 54/58锛?- 鍗曚竴鏁板瓧鏀句笉涓嬩俊鎭細mach 鍚姩琛ㄦ湁 1736 鏉★紙`subsystem <= 14`锛夛紝ZALLOC 鐙崰 767 鏉★紝
  宸叉敼涓恒€屽瓙绯荤粺 + 鏉＄洰搴忓彿銆嶅弻鏍硷紝鍐嶅崌绾т负 `vince_mark_quad` 鍥涙牸
---

## 14. 瓒婅繃 mach IPC锛氬唴鏍歌繘鍏?IOKit kext 鍔犺浇

### 閲岀▼纰?
浠婂ぉ绗竴娆￠€氳繃 `kernel_startup_initialize_upto(STARTUP_SUB_MACH_IPC)`銆?涔嬪墠鐨勭粨璁猴紙"鍋滃湪 mig_init 鐨?kroutine panic"锛夋槸瀵圭殑锛屼絾**鍙槸绗竴灞?*銆?
### 瀹屾暣姝诲洜閾撅紙姣忎竴灞傞兘鏈夊睆骞曡鏁版敮鎾戯級

| 灞?| 鐜拌薄 | 璇佹嵁 | 澶勭疆 |
|---|---|---|---|
| 1 | `panic("kroutine must have precise size")` | i=0/j=0 鈫?`mach_vm_allocate`锛宍max_reply_msg=0` | 鍥為€€鍒板瓙绯荤粺 `maxsize` |
| 2 | 鏀跺熬 `printf` 瑙﹀彂 kprintf | 绉婚櫎鍚庝粛鍋?| 鍒犳帀璇ヨ瘖鏂?printf |
| 3 | `assert3u(grp,<,TASK_GRP_COUNT)` 璇垽 | 闈㈡澘 `line=283 x=120675180 y=32` | 瀹炰负涓嬩竴灞?|
| 4 | **`reply_descr_count <= IPC_KOBJECT_RDESC_MAX`** | 鏂█鍘熸枃 + `x=120675180`锛堟寚閽堜綆浣嶏級銆乣y=32` | **鍏虫帀涓や釜鎻忚堪绗﹁鏁版柇瑷€** |
| 5 | **`OSMetaClass: Kext %s class %s is a duplicate`** | 缁垮瓧鍘熸枃 | 褰撳墠闂锛坧relink 灞傦級|

绗?4 灞傛槸鐪熷嚩锛歚kern_routine_descriptor` 鐨勫瓧娈靛亸绉讳笌鏈瀯寤轰笉绗︼紝
`reply_descr_count` 璇诲埌浜嗘寚閽堜綆浣嶏紙0x731_4xxx锛夛紝鏂█蹇呯劧澶辫触銆?杩欎篃瑙ｉ噴浜嗘鍓嶆墍鏈夐潤鎬?dump銆屽竷灞€鎬庝箞绠楅兘瀵逛笉涓娿€嶃€?
### 瑙傛祴鎵嬫鐨勬紨杩涳紙鍏抽敭宸ョ▼鏀惰幏锛?
1. **鐗╃悊 framebuffer 鑷槧灏?*锛歚vince_mark_map()`锛屽湪 `arm_vm_init` 涔嬪悗鍙敤
2. **鏂瑰潡 / 鏁板瓧鎺㈤拡**锛氭棭鏈熼潬杩欎釜瀹氫綅鍒?`mig_init`
3. **5x7 瀛楀簱 + `vince_mark_text()`**锛氱洿鎺ユ妸 panic 鏍煎紡涓茬敾鍒板睆骞?4. **panic 閽╁瓙瑙ｆ瀽 varargs**锛氱敾鍑烘柇瑷€琛ㄨ揪寮忋€佽鍙枫€亁/y 瀹為檯鍊?5. 鎺㈤拡鍏ㄩ儴涓嬬Щ鍒板睆骞曚笅鍗婇儴锛坄y鈮?000+`锛夛紝鎶婁笂鍗婇儴鐣欑粰 console/鏂囨湰

> 缁忛獙锛?*鍒啀鐢ㄤ袱浣嶆暟鏍煎瓙鐚滄暟鍊?*銆俙x=5180/y=32` 鏄璇伙紝
> 瀹為檯 `x=120675180/y=32`锛岀粨璁哄畬鍏ㄤ笉鍚屻€傜敤 `vince_mark_num()` 鎵撳嵃鍗佽繘鍒舵枃鏈€?
### 璇曡繃浣嗘棤鏁堢殑璺?
- **early console**锛坄arm_init` 閲岃皟 `PE_init_printf(TRUE)`锛夛細
  `vcattach` 鍗婂垵濮嬪寲锛岄殢鍚?`gc_update_color` 鎾?`assert(gc_ops.update_color)`
  锛坄video_console.c:1226`锛夆€斺€旇嚜浼わ紝宸茬Щ闄?- **璺?boot RAM 浼犻€?*锛欴RAM 閲嶅惎涓嶄繚鐣欙紝`keep probe` 绗簩娆′粛鏄?`fresh RAM`
- **UART 涓插彛**锛歺nu 鏈?`serial_console` 妗嗘灦锛屼絾缂哄钩鍙?UART 鍩哄潃 + 闇€瑕佺‖浠舵帴绾?- **USB 鏃ュ織**锛圥agani/giulia 鐨勫仛娉曪級锛氳繘鍏ョ敤鎴锋€佸悗鎵嶆湁锛屾棭鏈熸棤鐢?
### 鏋勫缓绠＄嚎鐨勫潙锛堟氮璐逛簡鍗佸嚑杞級

- `unixnu tree` 宸插簲鐢?patch锛屾瀯寤鸿剼鏈張搴旂敤涓€閬?鈫?`patch does not apply`锛?  涓旈敊璇 `|| true` 鍚炴帀銆?*淇硶锛歱atch 鍓?`git reset --hard` + `clean -fdq`**
- `source-machine-layer.patch` 寰€ `files.arm64` 鍔犱簡 4 涓?`amcc_rorgn_*.c`锛?  杩欎簺鏂囦欢鍦?10063 閲屼笉瀛樺湪 鈫?鏂囦欢鍒楄〃闃舵 `Error 2` 鏃犺瘖鏂?- `pexpert/arm/` 娌℃湁 osfmk include root锛宍<arm/vince_early_mark.h>` 瑙ｆ瀽澶辫触锛?  蹇呴』鐢?`"../../osfmk/arm/vince_early_mark.h"`
- 鍐呮牳閲?*娌℃湁 `strstr`**锛岄摼鎺ヤ細澶辫触锛涚敤瀛楅潰鍓嶇紑姣旇緝鏇夸唬
- 娉ㄥ叆浠ｇ爜寮曠敤 `vince_early_mark.c` 鐨?`static` 鍙橀噺锛堝 `g_h`锛変細缂栬瘧澶辫触锛?  鍙兘鐢ㄥ浐瀹氬潗鏍?
### 褰撳墠闂

`OSMetaClass: Kext %s class %s is a duplicate; kext %s already has a class with this name`

IOKit 鍒濆鍖栨椂鎶?kext 绫诲悕閲嶅銆傚睘浜?**prelink 鎵撳寘**锛坄kits/NativePrelink` 瀛愭ā鍧楋級
灞傞潰鐨勯棶棰橈紝涓嶆槸鍐呮牳閫昏緫銆備笅涓€姝ワ細璇诲嚭閲嶅鐨?kext 鍚嶏紝鏍稿 prelink 娓呭崟銆?
---

## 15. QEMU 蹇€熻凯浠ｇ幆澧冿紙浠婂ぉ寤烘垚锛?
### 涓轰粈涔?
CI 涓€娆″唴鏍告瀯寤?**8.1 鍒嗛挓**锛堟€?9.3 鍒嗛挓閲?87% 鏄紪璇戯級锛?姣忚疆鍒锋満鍐嶅姞蹇?2 鍒嗛挓 + 浜哄伐鎷嶇収鍒よ銆傛病鏈?macOS 涓绘満灏辨病娉曟湰鍦扮紪锛?鎵€浠ュ彧鑳芥妸**楠岃瘉**杩欎竴鍗婃惉鍒版湰鍦帮細**QEMU 45 绉掍竴杞紝涓插彛鏃ュ織鐩存帴鍙**銆?
### 缁勬垚閮ㄥ垎锛堝叏閮ㄥ凡灏变綅锛?
| 浠?| 浣嶇疆 | 璇存槑 |
|---|---|---|
| QEMU | `C:\Program Files\qemu` | 11.1.0锛屽惈 `edk2-aarch64-code.fd` |
| Mu_Basecore | `UniXNU/package/Mu_Basecore` | EDK2 鍒嗘敮 `release/202608`锛?.3k 鏂囦欢 |
| UniXNU.efi | `package/Build/Out/AARCH64-DEBUG/UniXNU.efi` | 94 KB锛宍./build.sh -b DEBUG -t GCC` |
| DarwinBoot.efi | `package/Build/UniXNU/DEBUG_GCC/AARCH64/DarwinBoot.efi` | 36 KB锛屾彁渚?XNU loader protocol |
| ESP | `C:\Temp\qemu-test\esp` | `EFI/BOOT/BOOTAA64.EFI` + `EFI/UniXNU/{Drivers,Payloads,unixnu.toml}` |

### 鍏抽敭鍧?
- `build.sh` 閲?`PACKAGES_PATH` 鍘熸湰鍙湁 `package` + `edk2`锛?  `DarwinBootPkg` 鍦?`drivers/DarwinBoot/` 涓嬶紝闇€瑕?  `$ROOT/../drivers/DarwinBoot:$ROOT/../drivers:$ROOT:$EDK2`
- `DarwinBoot.dsc` 閲岀殑 `Test/Validation.inf` 璺緞鏄浉瀵?`DarwinBootPkg/` 鍐欑殑锛?  瀹為檯鏂囦欢鍦?`drivers/DarwinBoot/Test/`锛屼細瑙ｆ瀽澶辫触锛屽凡绉婚櫎
- EDK2 鐨?`build` 澶辫触鏃跺彧鎵撳嵃 `- Failed -`锛岃 `-d 9` 鎵嶈兘鐪嬪埌鍘熷洜
- **WSL 璋?Windows QEMU 鏃讹紝QEMU 鍛戒护琛岄噷鐨勮矾寰勫繀椤绘槸 Windows 褰㈠紡**
  锛坄C:/...`锛夛紝鍙湁鏃ュ織鏂囦欢鐣欏湪 WSL 渚?- `-m 4096` 鏃?DarwinBoot 鎶?`boot refused: Out of Resources`锛?*8 GB 鎵嶅**

### QEMU 閲屽凡楠岃瘉鐨勪簨瀹?
```
UNIXNU: UniXNU 0.1.0 starting as application, firmware EDK II
UNIXNU: driver \EFI\UniXNU\Drivers\DarwinBoot.efi (config): started
DARWINBOOT: loader v2 installed EL1
DARWINBOOT: ARM64 va=0xFFFFFFF00427C000 pa=0x4807C000 entry=0x4B1EB488
DARWINBOOT: hand-off to the kernel
```

**鍐呮牳 entry code 璺戜簡锛堥《閮ㄧ豢鏉★級锛屽紓甯?trace 鏄剧ず鍐呮牳鍦ㄦ甯告墽琛岋細**
852 涓紓甯革紝灏鹃儴鍏ㄦ槸 `Taking exception 5 [IRQ]`锛宍SPSR 0x205`锛圗L1h锛夛紝
**娌℃湁浠讳綍 abort**銆傛墍浠ュ唴鏍稿湪 QEMU 閲屾槸娲荤殑锛屽彧鏄病寰€涓插彛杈撳嚭銆?
### 寰呭姙

- `vince_mark_putc` 鍔?**PL011 tee**锛坄0x9000000`锛夊悗锛孮EMU 鎵嶈兘鎶撳埌鍐呮牳鏂囨湰锛?  鐪熸満涓婅鍦板潃鏈槧灏勶紝鍐欏叆琚己椤靛鐞嗗悶鎺夛紝涓嶅奖鍝?fb 璺緞
- 涓插彛閫氫簡涔嬪悗锛宍-d int` 鐨?trace 灏变笉闇€瑕佷簡

### 鍏ㄨ嚜鍔?
- `C:\Temp\auto\run.ps1` 鈥斺€?涓€娆★細绛夋渶鏂版瀯寤?鈫?涓嬭浇 鈫?鍒?ESP 鈫?QEMU 鈫?鎽樿
- `C:\Temp\auto\loop.ps1` 鈥斺€?寰幆锛氳Е鍙戞瀯寤?鈫?绛?鈫?涓嬭浇 鈫?QEMU 鈫?鍒嗘瀽 鈫?涓嬩竴杞紝
  姣忚疆鏃ュ織瀛?`C:\Temp\auto\rounds\<n>\`
- CI 渚у凡鍔?`actions/cache`锛坄xnu-work/build`锛夛紝涓嬩竴娆¤捣缂栬瘧搴斿彉鎴愬閲?

---

## 16. QEMU 閲岀殑鍐呮牳鏃ュ織鎵撻€氾紙浠婃櫄鎴愭灉锛?
### 缁撴灉

鏈湴 QEMU 鐜板湪鑳芥墦鍗?*鐪熷疄鐨勫唴鏍告棩蹇?*锛?
```
vince                                                          <- UART 鏄犲皠鎴愬姛鐨勬爣璁?kprintf initialized
Serial mode specified: 00000003
initialize_screen: b=23C7A0000, w=320, h=258, r=0xC80
pe_arm_init_interrupts: args: 0xfffffff007a62860
corecrypto_kext_start (tracing disabled)
FIPSPOST_KEXT ... all tests PASSED (1690 ms)
corecrypto_kext_start completed successfully
ulock_initialize>thread_max=1536, ull_hash_buckets=512        <- 鍋滃湪杩?```

涓€杞獙璇?**40 绉?*锛圕I 8.5 鍒嗛挓 + 鍒锋満 2 鍒嗛挓 + 鎷嶇収锛夈€?
### 鍥涢亾鍏筹紙姣忛亾涓€涓槑纭牴鍥狅級

| # | 鐥囩姸 | 鏍瑰洜 |
|---|---|---|
| 1 | 瀹屽叏鏃犳棩蹇?| `kprintf` 鐨勯棬鏄?`if (!disable_serial_output && !disable_kprintf_output)`锛?*涓や釜榛樿閮芥槸 true**锛屽彧娓呬竴涓病鐢?|
| 2 | 娓呬簡杩樻槸鏃犳棩蹇?| `PE_init_kprintf` 鍦?`STARTUP(KPRINTF)` 璺戯紝**鏃╀簬 fb 鏄犲皠**锛屾寜銆宖b 灏辩华銆嶅垽鏂鑷?hook 姘镐笉瀹夎 |
| 3 | UART tag 涔熶笉鍑虹幇 | `0x9000000` 鏄?*鐗╃悊鍦板潃**锛屽唴鏍?VM 鏈槧灏勶紝鍐欏叆 fault 琚悶锛涘繀椤?`ml_io_map_unmappable` 鍏堟槧灏?|
| 4 | Undefined Instruction | QEMU `-cpu cortex-a72` 涓嶈璇?`MSR S3_0_C4_C1_4`锛?xd500419f锛夛紱**`-cpu max` 鎵嶈** |

### QEMU 鐨勮竟鐣?
鍗″湪 `ulock_initialize()`锛坄STARTUP(EARLY_BOOT, STARTUP_RANK_FIRST)`锛夌殑
`zalloc_permanent`銆?*鐪熸満鑳借繃杩欎竴姝?*锛堢湡鏈哄凡鍒?IOKit锛夛紝鎵€浠ヨ繖鏄?QEMU 缂虹‖浠?
鍐呭瓨甯冨眬宸紓閫犳垚鐨勶紝涓嶆槸鍐呮牳缂洪櫡銆?*QEMU 鐨勯獙璇佹繁搴﹀埌姝や负姝?*銆?
### 鍙鐢ㄧ殑涓滆タ

| 浠?| 浣嶇疆 |
|---|---|
| Mu_Basecore | `UniXNU/package/Mu_Basecore`锛坄release/202608`锛墊
| UniXNU.efi | `package/Build/Out/AARCH64-DEBUG/UniXNU.efi` |
| DarwinBoot.efi | `package/Build/UniXNU/DEBUG_GCC/AARCH64/DarwinBoot.efi` |
| ESP | `C:\Temp\auto\esp` |
| QEMU 璁惧鏍?| `C:\Temp\auto\qemu.adt` |
| 鎴浘 | `C:\Temp\auto\shot.ps1` |
| 鍏ㄨ嚜鍔?| `C:\Temp\auto\loop.ps1` |

**QEMU 鍛戒护琛岋紙缂轰竴涓兘涓嶈锛?*

```
-M virt -cpu max -m 8192 -smp 1
-drive if=pflash,format=raw,readonly=on,file=edk2-aarch64-code.fd
-drive if=none,id=esp,format=raw,readonly=on,file=fat:<ESP鐩綍>
-device virtio-blk-pci,drive=esp -device ramfb
-display none -serial file:<log>
```

- `-cpu max`锛歝ortex-a72 浼氭挒鏈畾涔夋寚浠?- `-m 8192`锛?096 鏃?DarwinBoot 鎶?`boot refused: Out of Resources`
- ESP 鐢?*鐩綍**锛坄fat:`锛夛紝涓嶉渶瑕?dd/mkfs.vfat 閫犻暅鍍?- WSL 閲岃皟 Windows QEMU 鏃讹紝**鍛戒护琛岃矾寰勫繀椤绘槸 `C:/...` 褰㈠紡**

### 璁惧鏍戣鐢?QEMU 鐨勶紝涓嶆槸 vince 鐨?
`make-dt.py --armvirt --armcpu --smp 1` 鐢熸垚銆傜敤 vince 鐨?`.adt` 浼氭姤锛?
```
*** CPU id 256 from CPU ordinal 1 'reg' property is out of range [0..7]
*** Missing 'interrupts' property for CPU 0
*** Missing 'function-ipi_dispatch' property for CPU 0
```

### 鐪熸満 IOSurface 鐨勬湰璐紙宸叉煡娓咃級

`IOsurfaceRoot:installMemoryRegions()` 涔嬪悗鍗′綇锛?*涓嶆槸鏂█銆佷笉鏄唴瀛樹笉瓒?*锛屾槸
**Apple 闂簮 IOSurface kext 鍦ㄩ潪 Apple 骞冲彴涓婅窇涓嶉€?*銆?
ios-vince 鐨勫仛娉曟槸**閲嶅啓**锛歚vinceSurface.cpp`锛圛OCoreSurfaceRoot锛?
`vinceFramebuffer.cpp`锛圓ppleCLCD锛夛紝娉ㄥ唽杩?`iokit/KernelConfigTables.cpp`锛?骞跺湪 `vincePlatformExpert` 閲岀粰 `arm-io` 瀛愯妭鐐瑰缓 nub銆?*鍛ㄧ骇宸ヤ綔閲?*銆?
