# 浜ゆ帴锛歟xecve 缂洪〉涓轰綍鍙樻垚 panic锛?026-10-24 涓嬪崍锛?
> 鎵挎帴 `HANDOVER-2026-10-24.md`銆備笂鍗堥偅浠借褰曚簡銆屾牴鍗锋壘鍒?+ launchd 鍔犺浇銆嶏紝
> 杩欎唤璁板綍**閭ｄ釜 panic 鐨勫畬鏁存満鐞?*銆?
---

## 涓€銆佸凡缁忕‘瀹氱殑鍥犳灉閾?
```
execve("/sbin/launchd")
  鈹斺攢 vm_map_switch(get_task_map(task))        L1821  鉁?鍒囧埌鐢ㄦ埛 map
     鈹斺攢 exec_copyout_strings()                L1839  鉁?cpo0  杩斿洖 0
        鈹斺攢 dynlinker copyoutptr()             鉁?cp20  杩斿洖 0
           鈹斺攢 copyoutptr(dynlinker_fd, ap, 8) L1925  鉁?FAULT
              鈹斺攢 _bcopyout 鍐呯己椤?                 鈹斺攢 handle_kernel_abort
                    鈹斺攢 find_copyio_recovery_entry(state)
                       鈹溾攢 鍖归厤 鈫?handle_kernel_abort_recover 鈫?鎭㈠锛岀户缁?                       鈹斺攢 涓嶅尮閰嶏紙recover == 0锛夆啋 panic  鈫?鎴戜滑鍦ㄨ繖閲?```

**`vm_page_free_count` 鐨?9100 涓囨槸杩欐 panic 鐨?*鍚庢灉**锛屼笉鏄師鍥犮€傚洓涓椂鐐瑰疄娴嬭瘉鏄庡畠涓€鐩存甯革細**

| 鏃剁偣 | 鍊?| 鍒ゅ畾 |
|---|---|---|
| `initialize_ram_ranges` | 0 | 椤垫暟缁勮繕涓嶅瓨鍦?|
| `pmap_startup` 杩斿洖 | 1,207,626 | 鉁?涓?`max_mem/4096 = 1,245,184` 鍚诲悎 |
| `vm_page_bootstrap` 缁撴潫 | 1,207,621锛坵ire 37,563锛?| 鉁?|
| `IOFindBSDRoot` 鍏ュ彛 | 1,207,627 | 鉁?UFS 椹卞姩鍏ㄧ▼鏃犻棶棰?|
| execve 鏃?| 91,199,441 | 鉁?鍦ㄨ繖涓?panic 閲岃鍐欏潖 |

**鎵€浠ワ細`dram_size` / `owned_memory_size` 瀹屽叏涓嶇敤鍔ㄣ€?*

---

## 浜屻€佸凡缁忔帓闄ょ殑鍋囪锛堟瘡鏉￠兘鏈夊疄娴嬶級

| 鍋囪 | 鎺掗櫎鏂瑰紡 | 缁撹 |
|---|---|---|
| ADT 鍐呭瓨鍙傛暟閿?| `maxmem4864`銆乣pages1207622` | 4.75 GiB 姝ｇ‘锛岄〉澶у皬 4 KB |
| `size - rlimit` 涓嬫孩 | `prt16384` = PAGE_SIZE | 鏈笅婧?|
| 鏍堝お灏?| `usz 4.24 MB`銆乣rlimit 1 MB` | 鍒嗛厤鍏呰冻 |
| `exec_prefault_data` 澶櫄 | 鎻愬墠璋冪敤鍚?fault 浣嶇疆涓嶅彉 | 瀹冨彧 prefault 鏁版嵁娈碉紝涓嶅惈鏍?|
| kernel-to-kernel copy 璺緞 | **`Q40`** = 绾跨▼涓嶅湪 kernel_map | 璧扮殑鏄湁淇濇姢鐨?`_bcopyout` |
| `__copyio_vectors` 琛ㄤ涪澶?| 娈靛瓨鍦紝`0x120` 瀛楄妭 = 12 鏉?| 琛ㄥ畬鏁达紝`cre_recovery` 鎸囧悜 `copyio_error` |
| `expected_fault_handler` | 鍙湪 `#ifdef CONFIG_XNUPOST` 閲岃璁剧疆 | 姝ｅ父鍐呮牳閲屾亽涓?NULL锛屼笉鏄繖鏉¤矾寰?|

---

## 涓夈€佸叧閿簮鐮佷綅缃紙閮藉湪 `.cache/xnu-work/`锛?
| 鏂囦欢 | 琛?| 鍐呭 |
|---|---|---|
| `bsd/kern/kern_exec.c` | 1821 | `vm_map_switch(get_task_map(task))` |
| | 1839 | `exec_copyout_strings()` |
| | 1925 | `copyoutptr(dynlinker_fd, ap, 8)` 鈫?fault 鐐?|
| `osfmk/arm64/machine_routines_asm.s` | 672 | `_bcopyout`锛屽惈 `COPYIO_RECOVER_RANGE 3f` |
| | 68 | `COPYIO_RECOVER_RANGE` 瀹忥紝鍐?`__copyio_vectors` |
| `osfmk/arm64/sleh.c` | 1765 | `recover = find_copyio_recovery_entry(state)` |
| | 1878/1885 | `if (recover) handle_kernel_abort_recover(...)` |
| | 1890 | `panic_fault_address = fault_addr` |
| `osfmk/arm64/sleh.c` | 299 | `find_copyio_recovery_entry`锛氭寜 PC offset 鏌ヨ〃 |
| `osfmk/arm64/copyio.c` | 132 | `copy_validate`锛宍EXDEV` 鏃惰蛋鏃犱繚鎶ょ殑 `copyout_kern` |

**鍐呮牳閲岃〃鐨勪綅缃紙12:54 鏋勫缓锛夛細**
```
__copyio_vectors      size 0x120  addr 0xfffffff007157b2e
_copyio_recover_table         0xfffffff007157b2e
_copyio_recover_table_end     0xfffffff007157c4e
copyio_error                  0xfffffff00740e9e4   (offset 0x2b6eb6 from base)
_bcopyout                     0xfffffff00740eb44
```

**12 鏉¤〃椤癸紝绗?9 鏉¤寖鍥?`0x2b7022..0x2b7056`銆俙_bcopyout + 0x1c` 鐨?offset 鏄?`0x2b7032`锛岀悊璁鸿惤鍦ㄥ叾涓€?*

---

## 鍥涖€佷笅涓€涓帰閽堝凡缁忓竷濂?
鍦?`handle_kernel_abort` 鍏ュ彛鐢讳笁涓€硷紙`sleh.c` 鐨?`vince-sleh-probes.py`锛夛細

| 琛?| 鏍囩 | 鍚箟 |
|---|---|---|
| 1900 | `RV` | `recover` 鎸囬拡锛?*0 琛ㄧず鏌ヨ〃澶辫触** |
| 1980 | `PCOF` | `copyio_recovery_offset(PC)` |
| 2060 | `TB` | `copyio_recover_table` 鍩哄潃 |

**鍒よ锛?*
- `RV` 闈?0 鈫?鏌ヨ〃鎴愬姛锛宲anic 鍙︽湁鍘熷洜锛堝線 `vm_fault` 杩斿洖鍊肩湅锛?- `RV` = 0 涓?`PCOF` 钀藉湪鏌愭潯 `[cre_start, cre_end)` 鍐?鈫?鏌ヨ〃閫昏緫鏈韩鏈夐棶棰?- `RV` = 0 涓?`PCOF` 钀藉湪鎵€鏈夎寖鍥翠箣澶?鈫?PC 涓嶅湪 `COPYIO_RECOVER_RANGE` 瑕嗙洊鍖洪棿锛岄渶瑕佹墿澶ц寖鍥?
鍚屽睆杩樻湁 P0鈥揚3 / Q4锛?100鈥?420锛変笌 ESR/FAR/PC/LR锛?560鈥?820锛夈€?
---

## 浜斻€佽繖杞俯鐨勫伐鍏峰潙锛堥兘璁颁笅鏉ワ紝鍒啀韪╋級

| 鍧?| 琛ㄧ幇 | 瑙ｆ硶 |
|---|---|---|
| 鏀?`scripts/*.py` 涓?commit | `unixnu tree` 閲嶇疆锛屾敼浜嗗崄鍑犺疆鍏ㄦ棤鏁?| 姣忔鏀瑰畬绔嬪埢 commit + push |
| `strings` 榛樿 4 瀛楃 | `"P0"`銆乣"RV"` 杩欎簺 2 瀛楃鏍囩鏌ヤ笉鍒?| 涓€寰?`strings -n 2` |
| 鎺㈤拡鐢诲湪 1780 浠ヤ笂 | console 鐧藉瓧鐩栦綇 | console cap = `g_h-780`锛屽叏鏀?2100+ |
| `vince_mark_text` 姣忚娓?61px | 琛岃窛 <61px 浜掔浉鎿﹂櫎 | 琛岃窛 80px |
| 鍒?`.cpo` 閲嶅缓 | `link.filelist` 缂洪」 鈫?`_page_size` 娑堝け 鈫?archive 10 澶辫触 | 鐢?`touch` 婧愭枃浠讹紝鍒垹浜х墿 |
| `panic` 浼犳暣鏁?| hook 鎶?vararg 褰?`char*`锛屾暟瀛椾笉鏄剧ず | 鍏?`snprintf` 鍐?`panic("%s", buf)` |
| 涓€涓?panic 涓€杞埛鏈?| 姣忕偣涓€娆″叏娴佺▼ | 鏀圭敤 `vince_mark_num` 鐢诲浐瀹氳锛屼竴娆″惎鍔ㄦ嬁鍏ㄩ儴 |
| inserter 閿氱偣甯︾┖鏍?| `vince_mark_text (` vs `vince_mark_text(` | 鎸夊疄闄呮簮鐮佸啓閿氱偣 |
| C++/C 璇█閾炬帴 | `extern void` 涓?header 鍐茬獊 | `DECL` 鎸夋枃浠跺悕鏉′欢鍖?|

---

---

## 涓冦€佸凡鎺掗櫎锛氬唴鏍?slide 涓嶄細璁?offset 绠楅敊

`find_copyio_recovery_entry` 鐨勭畻娉曟槸锛?
```c
static inline ptrdiff_t
copyio_recovery_offset(uintptr_t addr)
{
    return (ptrdiff_t)(addr - (uintptr_t)copyio_recover_table);
}
```

**瀹冪敤銆岃繍琛屾椂 PC銆嶅噺鍘汇€宍copyio_recover_table` 绗﹀彿鍊笺€嶃€?*

### 涓轰粈涔堝畠涓嶆垚绔?
涓ょ澶勫湪鍚屼竴 slide 绌洪棿锛屽樊鍊艰嚜鍔ㄦ姷娑堬細

| 绔?| 鏉ユ簮 | 鏄惁鍚?slide |
|---|---|---|
| `get_saved_state_pc(state)` | 杩愯鏃?PC | 鏄紙宸?slide锛?|
| `(uintptr_t)copyio_recover_table` | C 鍙栫鍙峰湴鍧€锛岀紪璇戜负 `adrp/add` | 鏄紙杩愯鏃惰嚜鍔?slide锛?|
| `cre_start` / `cre_end` | 姹囩紪 `.quad Lcre_start - _copyio_recover_table` | 鍚︼紙閾炬帴鏈熷父閲忥級 |

鍓嶄袱鑰呯浉鍑忥紝slide 鎶垫秷锛涚粨鏋滀笌绗笁绫诲悓閲忕翰銆?*鏈満铏界劧 `slide = "-0x1000000"`锛屼絾杩欎笉褰卞搷璇ョ畻娉曘€?*

### 鍥犳 `recover == 0` 鍙墿涓夌鍙兘

| 鍙兘 | 鍒ゆ嵁锛坄PCOF` 鎺㈤拡宸插竷鍦?1980 琛岋級 |
|---|---|
| PC 鐪熺殑钀藉湪鎵€鏈夎寖鍥翠箣澶?| `PCOF` 鏄彲璇荤殑灏忓€硷紝浣嗕笉鍦ㄤ换浣?`[cre_start, cre_end)` 鍐?|
| `find_copyio_recovery_entry` 鐨勫惊鐜病鎵ц | `TB`锛?060 琛岋級涓?0 鎴栫瓑浜?`_end` |
| fault 涓嶆槸浠庤繖涓?PC 鎶ョ殑 | `PCOF` 涓?`_bcopyout+0x1c` 鐨勯鏈?offset锛坄0x2b7032`锛夊樊寰堣繙 |

**棰勬湡鍊煎彲浠ユ墜绠楋細`_bcopyout = 0xfffffff00740eb44`锛屽姞 `0x1c` 寰?`0xfffffff00740eb60`锛涘噺鍘昏〃鍩哄潃 `0xfffffff007157b2e` 寰?`0x2b7032`銆傜 9 鏉¤〃椤硅寖鍥?`0x2b7022..0x2b7056` 姝ｅソ鍖呭惈瀹冦€?* 鎵€浠ヨ嫢 `PCOF == 0x2b7032` 鑰?`RV == 0`锛岄棶棰樺氨鍦ㄦ煡琛ㄥ惊鐜湰韬€?
---

## 鍏€侌煄?宸插畾浣嶅苟淇锛歅AC 浣嶆贩杩涗簡 copyio 琛ㄧ殑 offset 璁＄畻

### 鍐冲畾鎬у疄娴嬶紙`RV` / `PCOF` / `TB` 鎺㈤拡锛?
```
RV   = 0                        recover = NULL锛屾煡琛ㄥけ璐?PCOF = 0x230397                 绠楀嚭鐨?offset
TB   = 0xfffffff006f6f663       琛ㄥ熀鍧€锛堟甯稿唴鏍稿湴鍧€锛?PC   = 0x1999999800c2bd60       鈫?涓嶆槸鍐呮牳鍦板潃鏍煎紡锛?LR   = 0x1999999800c18270
```

**`PC` 鏄?PAC 绛惧悕鍊笺€?* ARM64 涓?`get_saved_state_pc()` 杩斿洖鐨?PC 甯︽寚閽堣璇佷綅銆?
### 鏍瑰洜

```c
/* sleh.c:299 */
static inline struct copyio_recovery_entry *
find_copyio_recovery_entry(arm_saved_state_t *state)
{
    ptrdiff_t offset = copyio_recovery_offset(get_saved_state_pc(state));   // 鈫?灏戜簡 strip
    for (e = copyio_recover_table; e < copyio_recover_table_end; e++) {
        if (offset >= e->cre_start && offset < e->cre_end) return e;
    }
    return NULL;
}
```

**`sleh.c` 閲屽叾浠栨瘡涓€澶勬秷璐?saved PC 閮藉仛浜嗗寘瑁咃細**

| 琛?| 鍐欐硶 |
|---|---|
| 700 | `VM_KERNEL_ADDRHIDE(far), VM_KERNEL_UNSLIDE(get_saved_state_pc(state))` |
| 959 | 鍚屼笂 |
| 2350 | `VM_KERNEL_UNSLIDE(get_saved_state_pc(state))` |

**鍙湁 `find_copyio_recovery_entry` 鐩存帴鐢ㄤ簡瑁?PC銆?* 鐢ㄥ畠鍑忓幓閾炬帴鏈熷父閲忚〃鍩哄潃锛屽緱鍒扮殑 offset
钀戒笉杩涗换浣?`[cre_start, cre_end)`锛宍recover` 鎭掍负 NULL锛屼簬鏄瘡娆?copyio 缂洪〉閮借蛋 panic 鑰屼笉鏄?recovery銆?
### 淇硶

```c
- ptrdiff_t offset = copyio_recovery_offset(get_saved_state_pc(state));
+ ptrdiff_t offset = copyio_recovery_offset(VM_KERNEL_STRIP_PTR(get_saved_state_pc(state)));
```

**涓轰粈涔堟槸 `STRIP_PTR` 鑰屼笉鏄?`UNSLIDE`锛?*

```
copyio_recovery_offset(addr) = addr - (uintptr_t)copyio_recover_table
```

| 绔?| 杩愯鏃舵槸鍚?slide |
|---|---|
| `addr`锛堜繚瀛樼殑 PC锛?| 鏄?|
| `copyio_recover_table`锛圕 鍙栫鍙凤紝`adrp/add`锛?| 鏄?|

**涓ょ閮?slide 鈫?鐩稿噺鎶垫秷銆傛墍浠ュ彧闇€瑕佸幓鎺?PAC 浣嶏紝涓嶈兘鍔?slide銆?*
`UNSLIDE` 浼氶澶栧噺鍘?slide锛屽弽鑰屾妸瀵归綈鐮村潖鎺夛紙绗竴鐗堝氨鏄繖涔堝啓鐨勶紝宸叉敼姝ｏ級銆?
### 杩欎竴鏉¤В閲婂姏

**瀹冨悓鏃惰В閲婁簡姝ゅ墠鎵€鏈夊紓甯歌娴嬶細**

| 瑙傛祴 | 瑙ｉ噴 |
|---|---|
| 缂洪〉鍦板潃鍚堟硶銆佸湪鍒嗛厤鍖洪棿鍐?| 鍦板潃鏈韩娌￠棶棰?|
| 鏃╁厛鍑犳 copyout 鎴愬姛 | 閭ｄ簺椤靛凡鏄犲皠锛屼笉瑙﹀彂缂洪〉 |
| 涓€娆?`copyout` 涓€瀛楄妭灏?panic | 缂洪〉蹇呯劧缁忚繃 `find_copyio_recovery_entry`锛屽繀鐒惰繑鍥?NULL |
| `exec_prefault_data` 鎻愬墠鏃犳晥 | 瀹冨彧 prefault 鏁版嵁娈碉紝鏍堜粛缂洪〉 |
| `vm_page_free_count` 鍙樻垚 9100 涓?| panic 璺緞鐨勫壇浣滅敤 |
| 琛ㄥ畬鏁达紙0x120 瀛楄妭銆?2 鏉★級 | 琛ㄦ病闂锛屾槸鏌ヨ鍙傛暟閿欎簡 |

### 楠岃瘉鏂瑰紡

`RV`锛?900 琛岋級鍙樻垚闈?0 鍗充慨澶嶇敓鏁?鈥斺€?缂洪〉浼氳 `handle_kernel_abort_recover` 鎺ヤ綇骞惰烦鍒?`copyio_error`锛宍copyoutptr` 杩斿洖 `EFAULT` 鑰屼笉鏄鍐呮牳宕╂帀銆?
---

## 涔濄€丼TRIP_PTR 淇宸茬敓鏁?鈥斺€?鏁呴殰鐐瑰悗绉?
### 淇鍓嶅悗鐨?`PCOF` 瀵规瘮

| 鍚姩 | `PCOF` | `RV` | 鍒ゅ畾 |
|---|---|---|---|
| 淇鍓?| `0x230397` | **0** | 瀵?PAC 绛惧悕鍊肩畻 offset锛岃惤涓嶈繘浠讳綍琛ㄩ」 |
| **淇鍚?* | **`0x2b7027`** | **`0xfffffff006f6f779`** | **offset 姝ｇ‘锛屾煡琛ㄦ垚鍔?* |

**楠岀畻锛?*

```
RV - TB      = 192 = 8 脳 24          鈫?绗?9 鏉¤〃椤癸紙0-based #8锛?琛ㄩ」 9 鑼冨洿   = 0x2b7022 .. 0x2b7056
瀹炴祴 PCOF    = 0x2b7027              鈫?钀藉湪鑼冨洿鍐?鉁?```

**鎵€浠?`find_copyio_recovery_entry` 鐜板湪鑳借繑鍥炴湁鏁堟寚閽堜簡銆傝繖鏄湰杞敮涓€鐨勫疄璐ㄦ€т慨澶嶏紝鎴愬姛浜嗐€?*

### 浣?panic 渚濇棫 鈥斺€?鏁呴殰鐐圭Щ鍒颁簡 `handle_kernel_abort_recover`

`handle_kernel_abort_recover` 鐨?asm 閫昏緫锛坄sleh.c:1716`锛夛細

```asm
ldr  x1, [recover, CRE_RECOVERY]   // x1 = cre_recovery锛岀浉瀵瑰亸绉?add  x1, x1, x6                    // x1 += copyio_recover_table 鈫?缁濆鍦板潃
str  x1, [x0, SS64_PC]             // 鍐欏洖 saved PC锛岃烦杩囧幓
```

**璁＄畻鏈韩鏄鐨勶紙`TB + 0x2b6eb6` 鍗?`copyio_error`锛夈€?* 鏂板鎺㈤拡鏌ュ疄闄呭€硷細

| 琛?| 鏍囩 | 鍚箟 |
|---|---|---|
| 2140 | `JT` | `recover->cre_recovery` 鈥斺€?鍗冲皢璺宠浆鍒扮殑鍦板潃 |
| 2220 | `RJ` | `recover` 鎸囬拡锛岀敤浜庝笌 `RV` 瀵圭収 |

### 涓嬩竴姝ョ殑涓夌鍒よ

| `JT` 鍊?| 缁撹 | 鍔ㄤ綔 |
|---|---|---|
| `TB + 0x2b6eb6`锛堟甯革級 | 璺宠浆鐩爣姝ｇ‘锛宲anic 鍙戠敓鍦?`copyio_error` 杩斿洖涔嬪悗 | 鏌?`copyoutptr` 鐨勮繑鍥炲€艰矾寰勪笌 exec 鐨?`badtoolate` |
| 寮傚父灏忓€兼垨 0 | 琛ㄩ」鍐呭琚閿?| 鏌?`CRE_RECOVERY` 鐨?`offsetof` 涓庣粨鏋勫竷灞€ |
| 涓?`TB` 鏃犲叧鐨勫€?| `recover` 鎸囬拡铏界劧闈?0 浣嗕笉鍦ㄨ〃鍐?| 閲嶆柊妫€鏌?`find_copyio_recovery_entry` 鐨勮竟鐣屾瘮杈?|

### 鏈疆鎬荤粨

**浠庛€屾瘡娆?copyio 缂洪〉蹇呭穿銆嶅埌銆屾煡琛ㄨ兘鎴愬姛銆嶏紝鏈哄埗涓婅法浜嗕竴姝ャ€?* 鍓╀笅鐨勬槸鎭㈠涔嬪悗鐨勮矾寰勯棶棰橈紝
涓嶅啀鏄€岃〃鏌ヤ笉鍒般€嶈繖涓€绫汇€?
---

## 鍗併€侌煄?execve 鐨勭己椤靛凡缁忚法杩囧幓浜?鈥斺€?鐜板湪鏄?launchd 琚?SIGKILL

### 璇佹嵁閾?
```
R2 (panic 鐐圭殑 recover)  娌＄敾  鈫? handle_kernel_abort 娌¤蛋鍒伴偅閲?JT (recovery 璺宠浆鐩爣)   娌＄敾  鈫? 浣?RV 闈?0锛宺ecover 纭疄鎵惧埌浜?                              鈫? handle_kernel_abort_recover 鎵ц锛岃烦鍥?copyio_error
                              鈫? copyoutptr 杩斿洖 EFAULT锛宔xecve 缁х画
                              鈫? launchd 璧锋潵浜?                              鈫? 鐒跺悗琚?SIGKILL
```

**鐩樿笧涓€鏁村ぉ鐨?`_bcopyout` 缂洪〉 panic 宸茬粡娑堝け銆?* PAC 淇锛坄VM_KERNEL_STRIP_PTR`锛夋槸鏈夋晥鐨勯偅涓€鍒€銆?
### 鏂扮殑 panic 鍙婂叾鍑哄

涔呰繚鐨勯偅鍙ュ睆骞曟枃鏈紝鎴戜竴寮€濮嬭鎴愪簡 `unexpected STATUS!! nf %x %x with mask`锛?瀹為檯鏄唴鏍镐簩杩涘埗閲岀殑锛?
```
unexpected SIGKILL of %s %s with reason -- namespace %d code 0x%llx description %.800s
```

鍑哄 `bsd/kern/kern_sig.c:2077`锛屽湪 `psignal()` 閲岋細

```c
/* catch unexpected initproc kills early for easier debuggging */
if (signum == SIGKILL && p == initproc) {
    panic_plain("unexpected SIGKILL of %s %s with reason -- ...",
        (p->p_name[0] ? p->p_name : "initproc"),
        ((proc_getcsflags(p) & CS_KILLED) ? "(CS_KILLED)" : ""),   // 鈫?杩欎竴鍒楀喅瀹氭€ц川
        signal_reason->osr_namespace, signal_reason->osr_code, ...);
}
```

**PID 1 涓嶅厑璁歌 kill锛屾墍浠ュ唴鏍?panic 鎶ュ嚭鏉ャ€?*

### 馃幆 鏍瑰洜锛氫袱濂?boot-args锛岀敓鏁堢殑閭ｅ娌℃湁 AMFI

| 鏉ユ簮 | 鍐呭 | AMFI |
|---|---|---|
| `make-vince-adt.py:135`锛?*瀹為檯鐢熸晥**锛?| `-enable_kprintf_spam native-ufs-root=1 native-ufs-diagnostics=1 maxmem=4864` | 鉂?|
| `unixnu.toml` 鐨?`args`锛?*涓嶇敓鏁?*锛?| `... amfi_get_out_of_my_way=1 ...` | 鉁?|

**DarwinBoot 璇?ADT**锛堝惎鍔ㄦ棩蹇?`DB3 adt read Success`锛夛紝`unixnu.toml` 鐨?`args` 鏍规湰鍒颁笉浜嗗唴鏍搞€?
**`launchd` 鏈鍚?鈫?`CS_KILLED` 鈫?SIGKILL 鈫?panic銆?* 涓庤瀵熷畬鍏ㄤ竴鑷淬€?
### 淇

`make-vince-adt.py` 鐨?boot-args 鍔犱笂涓変釜瀹樻柟鏍囧織锛?
```
amfi_get_out_of_my_way=1
cs_enforcement_disable=1
amfi_allow_any_signature=1
```

宸查獙璇佽繘鍏?ADT锛?
```
amfi_get_out_of_my_way       1
cs_enforcement_disable       1
amfi_allow_any_signature     1
maxmem                       1
native-ufs-root              1
```

### 涓嬩竴姝ュ垽璇?
| 鐜拌薄 | 鍚箟 |
|---|---|
| 涓嶅啀鍑虹幇 `unexpected SIGKILL` | AMFI 鐢熸晥锛宭aunchd 娲荤潃 鈫?**杩涘叆 Stage 6 鍚庡崐娈?*锛坙aunchd 涔嬪悗鏄?userspace 鏈嶅姟锛?|
| 浠嶅嚭鐜颁笖甯?`(CS_KILLED)` | AMFI 鏍囧織娌¤璇嗗埆锛岄渶瑕佹崲娉ㄥ叆璺緞锛圓DT 鐨?`chosen` 鑺傜偣灞炴€э級 |
| 浠嶅嚭鐜颁絾涓嶅甫 `(CS_KILLED)` | 涓嶆槸绛惧悕闂锛屾槸鍒殑 exit reason 鈥斺€?鐪?`namespace` / `code` 涓や釜鏁板瓧 |

---

## 鍗佷竴銆丄MFI 纭鐢熸晥锛屼笖**涓嶆槸**浠ｇ爜绛惧悕闂

### 瀹炴祴

```
AMx = 10
```

瑙ｅ寘锛歚AMx = AMFI鍊?脳 10 + CS_KILLED`

| 椤?| 鍊?| 鍚箟 |
|---|---|---|
| `AMFI 鍊糮 | **1** | `amfi_get_out_of_my_way` **纭疄琚唴鏍歌В鏋愬埌浜?* |
| `CS_KILLED` | **0** | **`launchd` 涓嶆槸鍥犱唬鐮佺鍚嶈鏉€鐨?* |

**鎵€浠ヤ袱鏉℃帹鏂兘琚惁瀹氾細**

- 鉂?銆孉DT 鐨?boot-args 娌″埌鍐呮牳銆?鈥斺€?鍒颁簡锛宍AMFI = 1`
- 鉂?銆宍launchd` 鏈鍚嶈 `CS_KILLED`銆?鈥斺€?涓嶆槸锛宍CS_KILLED = 0`

### 杩欐剰鍛崇潃浠€涔?
`psignal()` 閲岄偅涓?`if (signum == SIGKILL && p == initproc)` 鍒嗘敮**纭疄琚蛋鍒颁簡**锛堟墍浠ユ湁閭ｅ彞
`unexpected SIGKILL` 鐨?panic锛夛紝浣嗘潃瀹冪殑鍘熷洜涓嶆槸绛惧悕锛岃€屾槸鍒殑 exit reason銆?
### 鍞竴杩樼己鐨勪俊鎭?
`signal_reason->osr_namespace` 鍜?`osr_code` 鈥斺€?瀹冧滑鏈潵鐢诲湪 2580 琛岋紝**瓒呭嚭 2560 鐨勫睆骞曢珮搴?*锛?鎵€浠ヤ竴鐩寸湅涓嶅埌銆?
宸叉敼鍒?2500 琛岋紙`AMx` 鐨勭粨璁哄凡鎷垮埌锛岃浣嶏級锛岀紪鐮佷负锛?
```
SIG = namespace 脳 100000 + (osr_code % 100000)
SIG = 7777777  鈫? signal_reason == NULL
```

### 鍒よ琛?
| `SIG` | `osr_namespace` | 鍚箟 |
|---|---|---|
| `400000 + code` | 4 | **Jetsam** 鈥斺€?鍐呭瓨鍘嬪姏锛屼笌 boot-arg 鏃犲叧 |
| `300000 + code` | 3 | **EXEC** 鈥斺€?鎵ц闃舵澶辫触锛坄EXEC_EXIT_REASON_*`锛?|
| `600000 + code` | 6 | **CODESIGNING** 鈥斺€?涓?`CS_KILLED=0` 鐭涚浘锛岄渶閲嶆柊鏌?|
| `7777777` | 鈥?| `signal_reason` 涓?NULL锛岃蛋鐨勬槸銆宯o reason provided銆嶉偅鏉?panic |
| 鍏朵粬 | 鈥?| 鎸?`osr_namespace` 鍊兼煡 `osfmk/kern/exit_reason.h` |

**鑻ヤ负 EXEC锛?锛?*锛歚osr_code` 浼氭寚鍑哄叿浣撴槸鍝竴姝?鈥斺€?渚嬪 `EXEC_EXIT_REASON_COPYOUT_STRINGS`
瀵瑰簲鎴戜滑鏃╁厛鐪嬪埌鐨?`cpo0`锛宍EXEC_EXIT_REASON_COPYOUT_DYNLINKER` 瀵瑰簲 `cp2`銆傝繖涔熸濂借兘楠岃瘉
PAC 淇涔嬪悗閭ｆ recovery 绌剁珶鎶?`copyoutptr` 鍙樻垚浜嗕粈涔堣繑鍥炵爜銆?
---

## 鍗佷簩銆侌煄?`SIG900008` 瀹屽叏瑙ｇ爜锛歚OS_REASON_EXEC` + `SECURITY_POLICY`

### 瑙ｇ爜

```
SIG = 900008
    = namespace 脳 100000 + (code % 100000)
      namespace = 9   = OS_REASON_EXEC           锛坆sd/sys/reason.h:96锛?      code      = 8   = EXEC_EXIT_REASON_SECURITY_POLICY  锛堝悓鏂囦欢:255锛?```

**`launchd` 涓嶆槸琚?jetsam銆佷笉鏄绛惧悕銆佷篃涓嶆槸琚埆鐨勫瓙绯荤粺鏉€鐨?鈥斺€?鏄?exec 鐨勫畨鍏ㄧ瓥鐣ユ嫆缁濄€?*

### 瀹屾暣鍥犳灉閾撅紙鍏ㄩ儴瀹炴祴锛?
```
kern_exec.c:8018   if (imgp->ip_mac_return != 0)
                     鈫?os_reason_create(OS_REASON_EXEC, EXEC_EXIT_REASON_SECURITY_POLICY)
kern_exec.c:6773     imgp->ip_mac_return = label_update_return
kern_credential.c    kauth_proc_label_update_execve(... &label_update_return)
mac_vfs.c:876        *labelupdateerror = error
mac_vfs.c:~840       error = mac_error_select(hook(...), error)   閬嶅巻鎵€鏈?policy
psignal()            SIGKILL on initproc 鈫?panic
```

**鑰?`machine_task_process_signature`锛堝彟涓€鏉′細浜х敓鍚屼竴 reason 鐨勮矾寰勶級鍙互鎺掗櫎锛?*
瀹冪殑閿欒瀛楃涓?`custom x18 ABI usage` 鍦ㄥ唴鏍镐簩杩涘埗閲屽嚭鐜?**0 娆?*锛岃鏄?`#if !__ARM_KERNEL_PROTECT__` 鍒嗘敮鐢熸晥锛屽嚱鏁拌繑鍥?`KERN_SUCCESS`銆?
### 鏍戦噷娉ㄥ唽鐨勪袱涓?policy 閮?*娌℃湁**閭ｄ釜閽╁瓙

| policy | 鏂囦欢 | `mpo_cred_label_update_execve` |
|---|---|---|
| `CHECK`锛圕heck Assumptions锛?| `bsd/kern/policy_check.c:527` | 鉂?|
| `Guarded vnode policy` | `bsd/kern/kern_guarded.c:1582` | 鉂?|

`libkern/amfi/amfi.c` 鍙湁 293 瀛楄妭锛屽唴瀹逛粎 `amfi_interface_register()` 鈥斺€?鏄?*鎺ュ彛娉ㄥ唽**锛?鐪熸鐨勫疄鐜板湪澶栭儴 kext銆?
**鎵€浠?MAC 寰幆鐞嗚涓婂簲璁?`error` 淇濇寔 0銆傝繖涓庛€孲ECURITY_POLICY 琚垱寤恒€嶇煕鐩俱€?*

### 姝ｅ湪閲忕殑涓滆タ

鏂板 `LU` 鎺㈤拡锛?500 琛岋級鐢?`*labelupdateerror`锛?
| `LU` | 鍚箟 | 涓嬩竴姝?|
|---|---|---|
| **0** | MAC 鏈嫆缁?鈥斺€?`SECURITY_POLICY` 鏉ヨ嚜鍒 | 鍥炲埌 `kern_exec.c:8018` 涔嬪墠鐨勫叾瀹?`goto done` 璺緞 |
| **闈?0** | 鏌愪釜 policy hook 杩斿洖浜嗚鍊?| 鐢?errno 鍙嶆煡鏄摢涓?hook锛圗PERM/EACCES/EAUTH鈥︼級 |

### 涓轰粈涔堣繖涓€杞€煎緱

**浠庛€宍launchd` 琚?SIGKILL銆嶅埌銆宔xec 鐨勫畨鍏ㄧ瓥鐣ユ嫆缁濓紝涓斾笉鏄鍚嶃€佷笉鏄?jetsam銆嶁€斺€?鑼冨洿宸茬粡鏀剁獎鍒?涓€涓嚱鏁拌繑鍥炲€笺€?* 鍓嶅洓涓?namespace 鍊欓€夊叏閮ㄦ帓闄わ紝鍓╀笅杩欎竴鏉°€?
---

## 鍗佷笁銆佹帹鏂笌浠ｇ爜鐭涚浘 鈫?鏀逛负鍦?SIGKILL 浜や粯鐐瑰疄娴?
### 鐭涚浘

**瀹炴祴浜嬪疄锛?*

```
SIG = 900008  鈫? namespace 9 (OS_REASON_EXEC) + code 8 (EXEC_EXIT_REASON_SECURITY_POLICY)
```

**鍏ㄦ爲鍙湁涓ゅ浜х敓杩欎釜 reason锛?*

| 浣嶇疆 | 瑙﹀彂鏉′欢 | 鏄惁鎺掗櫎 |
|---|---|---|
| `kern_exec.c:7950` | `machine_task_process_signature` 杩斿洖闈?`KERN_SUCCESS` | 鉁?鍐呮牳閲?`custom x18 ABI usage` 瀛楃涓?**0 娆?*锛岃鏄庤窇鐨勬槸 `#if !__ARM_KERNEL_PROTECT__` 鍒嗘敮锛岃繑鍥?SUCCESS |
| `kern_exec.c:8019` | `imgp->ip_mac_return != 0` | 鈿狅笍 闇€瑕?`exec_handle_sugid` 璧板埌 L6773 |

**鑰?`ip_mac_return` 鐨勬潵婧愰摼锛?*

```
kern_exec.c:6640   int label_update_return = 0;      鈫?宸插垵濮嬪寲
kern_exec.c:6757   kauth_proc_label_update_execve(..., &label_update_return)
kern_exec.c:6773   imgp->ip_mac_return = label_update_return;
mac_vfs.c:876      *labelupdateerror = error;
```

**`LU` 鎺㈤拡锛堝湪 `*labelupdateerror = error` 澶勶級浠庢湭鐢诲嚭** 鈫?`mac_cred_label_update_execve` 娌¤璋冪敤
鈫?`label_update_return` 淇濇寔 0 鈫?`ip_mac_return` 搴斾负 0 鈫?L8019 涓嶈瑙﹀彂銆?
**浠ｇ爜璇翠笉璇ュ彂鐢燂紝瀹炴祴璇村彂鐢熶簡銆?*

### 瀵圭瓥锛氬湪浜や粯鐐归噺锛屼笉鍐嶅悜鍚庡弽鎺?
鏂板 `PN` / `PC2` 鎺㈤拡锛岀洿鎺ョ敾 `psignal_with_reason` 鏀跺埌鐨勯偅浠?reason锛?
```c
nb u_mark_num("PN",  exec_failure_reason ? ->osr_namespace : 7777, 2100);
nb u_mark_num("PC2", exec_failure_reason ? ->osr_code      : 7777, 2180);
psignal_with_reason(current_proc(), SIGKILL, exec_failure_reason);
```

| `PN` | `PC2` | 鍚箟 |
|---|---|---|
| 7777 | 7777 | reason 鏄?NULL 鈫?璧扮殑鏄?`kern_sig.c` 鐨勩€宯o reason provided銆嶉偅鏉★紝涓?`SIG900008` 鐭涚浘锛岃鏄庢垜瑙ｇ爜閿欎簡 |
| **9** | **8** | 纭 `SECURITY_POLICY`锛屼笖瀹冪‘瀹炰粠杩欓噷鍙戝嚭 鈥斺€?閭?`ip_mac_return` 涓€瀹氶潪 0锛岄渶瑕佸啀鎵剧涓変釜璧嬪€肩偣 |
| 鍏朵粬 | 鍏朵粬 | 鐪熸鐨勫師鍥犵涓€娆＄幇褰?|

### 杩欎竴澶╃殑鏁欒锛堝啓涓嬫潵鍏嶅緱閲嶅锛?
**浠庢棭涓婂埌鐜板湪锛屽嚒鏄€屾寜浠ｇ爜鎺ㄦ柇銆嶅緱鍑虹殑缁撹锛屾湁涓€鍗婅瀹炴祴鎺ㄧ炕锛?*

| 鎺ㄦ柇 | 瀹炴祴缁撴灉 |
|---|---|
| ADT 鐨?dram_size 闇€瑕佹敼 | `maxmem4864` 姝ｇ‘ |
| `size - rlimit` 涓嬫孩 | `prt16384` 姝ｅ父 |
| 鏍堝お灏?| `usz` 4.24 MB 鍏呰冻 |
| `freepg` 铏氶珮瀵艰嚧缂洪〉澶辫触 | `freepg` 鏄?panic 鐨?*鍚庢灉** |
| slide 璁?offset 绠楅敊 | 涓ょ鍚?slide锛屾姷娑?|
| boot-args 娌″埌鍐呮牳 | `AMFI = 1`锛屽埌浜?|
| 绛惧悕澶辫触锛圕S_KILLED锛?| `CS_KILLED = 0` |

**鍞竴琚疄娴嬭瘉瀹炵殑鎺ㄦ柇鏄?PAC 閭ｆ潯** 鈥斺€?鑰屽畠涔熸槸鍞竴琚敼鎴愬疄闄呬慨澶嶇殑涓€鏉★紙`PCOF` 浠?`0x230397` 鍙樻垚 `0x2b7027`锛宍RV` 浠?0 鍙樻垚鏈夋晥鎸囬拡锛宍_bcopyout` 鐨?panic 娑堝け锛夈€?
**鎵€浠ワ細鍏堥噺锛屽啀鏀广€傚睆骞曚笂鐨勬瘡涓€涓暟瀛楅兘瑕佺湡鐨勮鍑烘潵銆?*

---

## 鍗佸洓銆乣bsd/kern` 閲屽叡鏈?*鍏釜** `SIGKILL` 鎶曢€掔偣锛屾帰閽堜箣鍓嶆彃閿欎簡

### 鍏釜绔欑偣

| 鏂囦欢:琛?| reason 鍙橀噺 | 鑳藉惁鏄?`SECURITY_POLICY` |
|---|---|---|
| `kern_exec.c:2158` | `exec_failure_reason` | 鉂?璇ュ彉閲忎粠鏈璧嬫垚 SECURITY_POLICY锛堝叏鏄?BAD_MACHO / COPYOUT_STRINGS / SET_DYLD_INFO 绛夛級 |
| `kern_exec.c:4845` | `exec_failure_reason` | 鉂?鍚屼笂 |
| **`kern_exec.c:8227`** | **`signature_failure_reason`** | 鉁?**鍙湁瀹?*锛圠8019 璧嬪€硷級 |
| `kern_proc.c:4354` / `4573` | `kill_reason` | 鉂?灞炲埆鐨勫瓙绯荤粺 |
| `kern_sig.c:1608` | `signal_reason` | 杞彂璺緞 |
| `mach_loader.c:1400` | `load_failure_reason` | 鉂?鏄?`FAIRPLAY_DECRYPT`(10) / `DECRYPT`(11) |

### 鎴戜箣鍓嶆彃閿欎簡浣嶇疆

`PN`/`PC2` 鎺㈤拡鎻掑湪 **L2158**锛坄badtoolate` 閭ｆ潯锛夛紝鑰岄偅鏉?*浠庝笉瑙﹀彂** 鈥斺€?鎵€浠ュ睆骞曚笂
`PN`銆乣PC2` 閮芥槸绌虹櫧锛屽彧鍓?`SIG900008`銆?*鐪嬭捣鏉ュ儚銆屾帰閽堟病鐢熸晥銆嶏紝瀹為檯鏄€岃繖鏉¤矾寰勬病璧般€嶃€?*

### 宸叉敼鍒版纭綅缃?
```c
kern_exec.c:8225   n a b u_mark_num("SN",  signature_failure_reason ? ->osr_namespace : 7777, 2100);
kern_exec.c:8226   n a b u_mark_num("SC",  signature_failure_reason ? ->osr_code      : 7777, 2180);
kern_exec.c:8227   n a b u_mark_num("SU",  (unsigned long)require_success, 2260);
kern_exec.c:8227   psignal_with_reason(p, SIGKILL, signature_failure_reason);
```

### 鍒よ

| `SN` | `SC` | `SU` | 鍚箟 |
|---|---|---|---|
| **9** | **8** | 0 鎴?1 | 涓?`SIG900008` 涓€鑷达紝纭 reason 浠庤繖閲屽彂鍑?鈫?`signature_failure_reason` 纭疄鏉ヨ嚜 L8019 鈫?**`ip_mac_return` 闈?0锛屽瓨鍦ㄦ垜娌℃壘鍒扮殑璧嬪€艰矾寰?* |
| 7777 | 7777 | 鈥?| reason 鏄?NULL 鈫?閭?`SIG900008` 涓嶆槸浠庤繖涓璞℃潵鐨勶紝鎴戠殑瑙ｇ爜閾炬潯瑕侀噸鏉?|
| 鍏朵粬 | 鍏朵粬 | 鈥?| 鐪熸鐨勫師鍥犵涓€娆＄幇褰?|

### 涓€鏉￠€氱敤鏁欒

**銆屾帰閽堟病鏄剧ず銆嶆湁涓夌瀹屽叏涓嶅悓鐨勫師鍥狅紝蹇呴』鍏堝尯鍒嗗啀鏀癸細**

1. **娌＄紪璇戣繘鍘?* 鈥斺€?`strings -n 2` 鏌ヤ笉鍒版爣绛撅紙`strings` 榛樿 4 瀛楃锛? 瀛楃鏍囩姘歌繙鏌ヤ笉鍒帮級
2. **缂栬瘧杩涘幓浜嗕絾閭ｆ浠ｇ爜娌℃墽琛?* 鈥斺€?鏍囩鍦ㄦ牳蹇冮噷銆佸睆骞曚笂鍗存病鏈?3. **鎵ц浜嗕絾琚鐩?* 鈥斺€?琛屽彿鍦?console 甯︼紙< 1780锛夊唴锛屾垨琚浉閭绘帰閽堢殑 61px 娓呴櫎鍖烘摝鎺?
**杩欎竴鏁村ぉ鑷冲皯浜旀鎶?(2) 璇垽鎴?(1)锛岀櫧鐧介噸鏋勫缓銆?* 姝ｇ‘鍋氭硶鏄瘡娆￠兘鍏?`strings -n 2 kernel.macho | grep -cx LABEL` 纭鏍囩瀛樺湪锛屽啀涓婃満鐪嬨€?
---

## 鍗佸叚銆乣LU` 涓嶆槸娌℃墽琛?鈥斺€?鏄 `SIG` 瑕嗙洊

### 鐪熺浉

鎴戠粰 `LU`锛坄*labelupdateerror`锛夊拰 `SIG`锛坄psignal` 閲岀殑 reason锛?*閮藉垎閰嶄簡 2500 琛?*銆?`SIG` 鍦ㄥ惎鍔ㄤ腑鏅氬緱澶氭墠鐢伙紝鎵€浠ュ畠鎶?`LU` 瑕嗙洊鎺変簡銆?
**浜庢槸鏁存暣鍗佸嚑杞噷锛屾垜鎶娿€岃瑕嗙洊銆嶈璇绘垚銆岃繖娈典唬鐮佹病璺戙€嶏紝骞朵互姝ゆ帓闄や簡
`mac_cred_label_update_execve` 鈥斺€?鑰屽悗鑰呮墠鏄湡姝ｄ骇鐢?`SECURITY_POLICY` 鐨勫湴鏂广€?*

### 淇

| 鎺㈤拡 | 鍘熻 | 鏂拌 | 鐘舵€?|
|---|---|---|---|
| `LU`锛坄*labelupdateerror`锛?| 2500锛堣瑕嗙洊锛?| **2100** | 鍙 |
| `KR`锛坄machine_task_process_signature`锛?| 2340 | 2180 | 鍙 |
| `EM`锛坄error_msg != NULL`锛?| 2420 | 2260 | 鍙 |
| `SN`/`SC`/`SU` | 2100/2180/2260 | 閫€浼?| 宸插洖绛旓細9 / 8 / 0 |

### 褰撳墠鐨勫畬鏁撮摼鏉★紙閮藉凡瀹炴祴锛?
```
mac_cred_label_update_execve   閬嶅巻 policy锛宔rror = mac_error_select(hook(...))
   鈹斺攢 *labelupdateerror = error          鈫?LU锛岀幇鍦ㄥ彲瑙?kern_exec.c:6773  imgp->ip_mac_return = label_update_return
kern_exec.c:8019  if (ip_mac_return != 0) 鈫?OS_REASON_EXEC + SECURITY_POLICY
kern_exec.c:8227  psignal_with_reason(SIGKILL, signature_failure_reason)   鈫?SN9 SC8 SU0 瀹炴祴
psignal()         initproc 琚?SIGKILL 鈫?panic
```

### 鍒よ

| `LU` | 鍚箟 |
|---|---|
| **闈?0** | 鏌愪釜 MACF policy 鐨?`mpo_cred_label_update_execve` 鎷掔粷浜?exec 鈥斺€?鐢?errno 鍙嶆煡鏄摢涓?hook |
| **0** | MACF 娌℃嫆缁濓紱閭?`SECURITY_POLICY` 鍙墿 `proc_process_signature` 涓€鏉℃潵婧愶紙鐢?`KR`/`EM` 楠岃瘉锛?|

### 涓€鏉¤鍒诲湪澧欎笂鐨勬暀璁?
**鎺㈤拡鐨?娌℃樉绀?蹇呴』鍏堝尯鍒嗕笁绉嶆儏鍐靛啀涓嬬粨璁猴細**

1. 娌＄紪璇戣繘鍘?鈫?`strings -n 2` 鏌ユ爣绛撅紙娉ㄦ剰 2 瀛楃鏍囩蹇呴』 `-n 2`锛?2. 缂栬瘧浜嗕絾閭ｆ浠ｇ爜娌℃墽琛?鈫?鏍囩鍦ㄦ牳蹇冦€佸睆骞曟棤
3. **鎵ц浜嗕絾琚埆鐨勬帰閽堣鐩?* 鈫?鍚屼竴琛屾垨 61px 娓呴櫎鍖洪噸鍙?
**浠婂ぉ鑷冲皯鍏鎶?(3) 褰撴垚 (2)锛岀櫧鐧界儳鎺夋暣杞瀯寤恒€?* 姣忔涓婃満鍓嶉兘璇ユ牳瀵逛竴閬嶈鍙疯〃銆?
---

## 鍗佷竷銆佹湰杞敹灏撅細宸茶瘉瀹炵殑銆佺煕鐩剧殑銆佷互鍙婁笅涓€姝?
### 宸茶瘉瀹烇紙瀹炴祴锛屼笉鍐嶆帹鏂級

| 浜嬪疄 | 璇佹嵁 |
|---|---|
| reason 纭疄鏄?`OS_REASON_EXEC`(9) + `SECURITY_POLICY`(8) | `SN9`/`SC8` 鍦ㄤ氦浠樼偣璇诲嚭锛沗SIG900008` 缂栫爜鍚诲悎 |
| reason 浠?`psignal_with_reason(p, SIGKILL, signature_failure_reason)` 鍙戝嚭 | 鎺㈤拡鎻掑湪 L8225 绱ч偦澶勶紝璇荤殑灏辨槸杩欎釜瀵硅薄 |
| `struct os_reason` 瀛楁甯冨眬姝ｅ父 | `osr_namespace`/`osr_code` 鐪熷疄瀛樺湪 |
| `machine_task_process_signature` 杩斿洖 SUCCESS | `custom x18 ABI` 瀛楃涓插湪鍐呮牳閲?0 娆★紝PROTECT 鍒嗘敮娌＄紪璇?|
| MACF 鐨?`cred_label_update_execve` hook 鏈繍琛?| `LU` 鍦ㄥ共鍑€琛屽彿锛?500锛変笂浠庢湭鍑虹幇 |
| `ip_cs_error` 鍦?kern_exec.c 鍐呭彧琚竻绌?| 鍏ㄩ儴璧嬪€兼槸 `= OS_REASON_NULL` |
| `ip_cs_error` 鐨勫閮ㄧ敓浜ц€呭彧浜?`CODESIGNING`(3) | `mac_vfs.c:1394`銆乣mach_loader.c:3387` 閮芥槸 namespace 3 |

### 鐭涚浘

**涓冧釜 `signature_failure_reason` 鐨勮祴鍊肩偣鍏ㄩ儴琚帓闄わ紝浣嗗畠闈?NULL 涓斿瓧娈垫纭€?*

浠ｇ爜璺緞涓庡疄娴嬫暟鎹煕鐩撅紝璇存槑杩樼己涓€鍧楁嫾鍥撅細瑕佷箞瀛樺湪涓€鏉℃垜娌℃壘鍒扮殑璧嬪€艰矾寰勶紝瑕佷箞 `SN9/SC8` 璇诲埌鐨勫璞?骞朵笉鏄垜浠ヤ负鐨勯偅娆?exec 鍒涘缓鐨勶紙渚嬪 reason 瀵硅薄鍦ㄥ娆?exec 闂村鐢ㄣ€佹垨 `psignal` 鍦ㄥ埆鐨勭嚎绋嬩笂鏀跺埌瀹冿級銆?
### 涓嬩竴姝ワ紙鎸変紭鍏堢骇锛?
1. **鍦?`proc_process_signature` 鐨勮皟鐢ㄥ锛圠8180锛夌敾 `error` 鍜?`signature_failure_reason` 鎸囬拡** 鈥斺€?   纭瀹冩槸鍚﹁璋冪敤銆佽繑鍥炰粈涔堛€乺eason 鎸囬拡瀵逛笉瀵癸紙涔嬪墠鐨?`KR` 鎾炰簡 `PC3` 鐨勮锛屾暟鎹笉鍙俊锛夈€?2. **鍦?`os_reason_create` 閲岀敾 `(namespace, code, 杩斿洖鎸囬拡)`**锛屽鐓?L8227 澶勭殑鎸囬拡锛岀洿鎺ユ壘鍑?   鏄摢涓€娆?create 浜у嚭浜嗚繖涓璞?鈥斺€?杩欐槸涓嶄緷璧栦换浣曟帹鏂殑鏈€寮烘墜娈点€?3. 鑻ョ‘璁?`reason` 鏉ヨ嚜 L8019锛屽垯鍥炲ご閲?`ip_mac_return` 鐨勭湡瀹炶祴鍊兼椂鍒伙紙`exec_handle_sugid` 鏄惁
   鐪熺殑琚皟鐢ㄤ簡锛岀敤鎺㈤拡鍦?L1635 鏃佽竟纭锛夈€?
### 浠婂ぉ鐨勫伐鍏锋暀璁紙閮藉凡鍐欏叆STATUS/浜ゆ帴锛?
- 鎺㈤拡琛屽彿鍐茬獊鏄?*浠婂ぉ鏈€澶х殑涓€绫诲亣淇″彿**锛歀U/SIG 鍚岃銆並R/PC3 鍚岃銆丒M/PC3 鍚岃锛屽叏閮ㄦ妸
  銆屾墽琛屼簡浣嗚瑕嗙洊銆嶈璇绘垚銆屾病鎵ц銆嶃€?- `strings` 榛樿 4 瀛楃锛宍PN2`/`PC3`/`SIG` 杩欑被鐭爣绛惧繀椤?`strings -n 2`銆?- 璇诲睆瀹规槗鎶?`PN2`+鍊?9 璇绘垚 `PN29`銆?*鏍囩鍜屾暟鍊间箣闂存病鏈夊垎闅旂**锛岃灏炬暟瀛楄鍏堟寜鏍囩琛ㄥ垏鍒嗐€?- 鏀?`scripts/*.py` 涓?commit锛宍unixnu tree` 浼氳繕鍘?鈥斺€?鎵€鏈?inserter 鏀瑰姩蹇呴』绔嬪埢鎻愪氦銆?- trust cache 宸叉帴鍏?payload锛?6 瀛楄妭锛宭aunchd cdhash `1d52c6鈥锛夛紝骞堕€氳繃 DarwinBoot
  `ValidTrustCaches` 鍏ㄩ儴瑙勫垯锛涜繖閮ㄥ垎鏄?*鍙鐢ㄨ祫浜?*锛屾棤璁?reason 浠庡摢鏉ラ兘涓嶇櫧鍋氥€?
## 鍏€佺姸鎬侀€熸煡

**鑳藉仛浠€涔?*锛欳I + 鏈湴 WSL 鏋勫缓锛?2 绉掞級锛屾墦鍖?cust锛屽埛鏈猴紝鐪熸満璺戝埌 `execve` 鐨?`copyoutptr`銆?
**涓嶈兘鍋氫粈涔?*锛氳法杩囬偅娆＄己椤点€俙launchd` 宸茶В鏋愩€佸凡鍔犺浇锛屼絾鐢ㄦ埛鏍堜笂鏈変竴椤靛啓涓嶈繘鍘汇€?
**`STATUS.md` 908 琛?*璁板綍浜嗗畬鏁村巻鍙诧紱鏈枃浠舵槸褰撳墠鏂潰銆?
