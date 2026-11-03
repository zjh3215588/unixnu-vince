# START HERE 鈥?vince (灏忕背骞虫澘5 / SM8150) XNU 绉绘

> **鍏堣 [`CURRENT-STATE.md`](CURRENT-STATE.md)銆?*
> 鏈粨搴撳叾浣欐枃妗ｆ槸**鎺ㄥ€掗噸鏉ヤ箣鍓?*鐨勮褰曪細閲岄潰鐨勨€滃綋鍓嶅熀绾库€濃€滀笅涓€姝モ€濃€滃崱鐐光€?> 閮藉凡琚彇浠ｏ紝鍙敤浜庤拷婧€滃綋鍒濅负浠€涔堥偅涔堝仛鈥濄€備笌 `CURRENT-STATE.md` 鍐茬獊鏃朵互瀹冧负鍑嗐€?
> 浠讳綍鏂颁細璇?鏂扮獥鍙ｆ帴鎵嬶紝**鍏堣杩欎釜鏂囦欢**锛屽啀璇讳笅闈㈡寚瀹氱殑鏂囨。锛岀劧鍚庢墠鍔ㄦ墜銆?> 涓嶆寜椤哄簭璇诲氨鍔ㄦ墜锛屼細閲嶅浠婂ぉ韪╄繃鐨勫崄涓潙銆?
## 涓€銆佸繀璇绘竻鍗曪紙杩欐槸纭€ц姹傦紝涓嶈璺筹級

**鍏堣 `DOCS-INDEX.md`**锛屽畠鍒楀嚭浜嗕簯绔粨搴撻噷**鍏ㄩ儴 18 浠芥枃妗?*鍚勮嚜璁蹭粈涔堛€佽浠€涔堟椂鍊欒銆?
鐒跺悗**閫愪唤鐮旇**锛堜笉鏄壂涓€鐪硷級锛?
| 椤哄簭 | 鏂囦欢 | 鍐呭 |
|---|---|---|
| 1 | **鏈枃浠?* | 閾佸緥 + 褰撳墠鍩虹嚎 + 涓や釜浠撳簱鐨?HEAD |
| 2 | `HANDOVER-2026-10-24-ROLLBACK.md` | 鏈€鏂颁氦鎺ワ細浠婂ぉ鎵€鏈夊疄娴嬬粨璁?+ 鍗佷釜鍧?+ 涓嬩竴姝ユ帓搴?|
| 3 | `HANDOVER-exec-fault.md` | 涓荤嚎 689 琛屽畬鏁磋褰曪紙execve/SIGKILL 鍏ㄩ摼鏉★級 |
| 4 | `HANDOVER.md` | 鏉冨▉鍒濆浜ゆ帴锛堜袱涓?kprintf 寮€鍏炽€丳E_kputc銆丷AMDisk銆丗VMAIN 涓婇檺锛?|
| 5 | `HANDOVER-legacy.md` | 40K 鏃╂湡鍘嗗彶锛岃拷婧?褰撳垵涓轰粈涔堣繖涔堝仛" |
| 6 | `STATUS.md` | 40K 閫愯疆娴佹按锛屾煡鏌愯疆鍒板簳鍙戠敓浜嗕粈涔?|
| 7 | `README.md` | 纭欢涓庢瀯寤虹幆澧冧簨瀹?|

**杩樿璇诲叏閮ㄦ彁浜よ褰曠殑 message**锛堜袱杈逛粨搴撻兘瑕侊級锛?
```bash
cd ~/src/unixnu-vince && git log --oneline -60
cd ~/src/UniXNU      && git log --oneline -60
```

**姣忔潯閮借鐪嬨€?* 瀹冧滑涓嶆槸濂楄瘽锛岃€屾槸褰撹疆鐨勫疄娴嬬粨璁恒€備緥濡?`5488c9e`锛圥AC 淇鏈哄埗锛夈€乣bcedff4`锛坴m_page_free_count 鏄悗鏋滀笉鏄師鍥狅級銆?`6373972`锛堟帰閽堝集璺殑鍗佷釜娴佺▼閿欒锛夈€乣ded3190`锛圓DT 缂鸿妭鐐瑰鑷村姛鑳介潤榛樺け鏁堚€斺€?鍚庢潵 TrustCache 鏄悓涓€涓ā寮忥級銆乣5b095ac`锛圖WC3 涓轰粈涔堝穿锛屽凡鍥炴粴锛岃瀹冮伩鍏嶉噸韫堬級銆?
**璇诲畬鍚庡繀椤昏兘鍥炵瓟杩欎簲涓棶棰?*锛堢瓟涓嶅嚭灏辩户缁锛夛細
1. 鐜板湪鐨?panic 鏄粈涔堬紵reason 鐨?namespace/code 鏄灏戯紝瀹炴祴鍊间粠鍝潵锛?2. execve 缂洪〉鏄€庝箞淇ソ鐨勶紵鏀瑰姩鍦ㄥ摢涓€琛岋紵
3. 涓轰粈涔?AMFI boot-args 瑕佹敼鍦?`make-vince-adt.py` 鑰屼笉鏄?`unixnu.toml`锛?4. 鎺㈤拡"娌℃樉绀?鏈夊摢涓夌鍙兘锛熶粖澶╁悇韪╄繃鍑犳锛?5. 鑷姩璇绘棩蹇楃殑鍥涙潯璺噷锛屽摢鏉″彲琛屻€佸摢涓夋潯瀹炴祴涓嶉€氾紵

`PUSH-GOTCHA.md` 鏄?git push 鍋囨垚鍔熼偅涓潙锛屾帹閫佸墠鎵竴鐪笺€?
## 浜屻€佷簲鏉￠搧寰嬶紙杩濆弽浠讳綍涓€鏉￠兘浼氱櫧鐑т竴杞級

1. **缁撹蹇呴』閲忓嚭鏉ワ紝涓嶈闈犱唬鐮佹帹鏂€?*
   浠婂ぉ鎵€鏈夐噸澶ч敊璇兘婧愪簬姝わ細`PN2`+`9` 璇绘垚 `PN29`銆乣vince RESTART: 0` 褰撴垚"鎾ら櫎鎴愬姛"銆?2. **楠岃瘉鍒ゆ嵁瑕侀€?搴斿綋瀛樺湪"鐨勪笢瑗裤€?*
   `count = 0` 鏄亽鐪熺殑锛屼笉鑳藉綋鎴愬姛璇佹嵁銆傜敤 **md5 鍙樺寲** + **搴斿瓨鍦ㄧ殑瀛楃涓?count > 0**銆?3. **鏀?`scripts/*.py` 蹇呴』鎻愪氦锛屽苟鐢?`git show origin/main:<file>` 楠岃瘉杩滅鐪熺殑鏇存柊銆?*
   `git push` 浼氳繑鍥?`exit=0` 浣?*涓嶇敓鏁?*銆傛瀯寤烘瘡杞?`git reset --hard FETCH_HEAD`锛屾湰鍦版湭鎻愪氦鐨勬敼鍔ㄤ細琚啿鎺夈€?4. **鍥炴粴瑕佸悓鏃跺洖婊?`UniXNU` 鍜?`unixnu-vince` 涓や釜浠撳簱銆?*
   鍙洖婊氫竴涓?鈫?board.toml 浠嶅垪鐫€宸插垹闄ょ殑椹卞姩 鈫?`KERNEL NOT REGENERATED` 鈫?鍒风殑鏄棫鍐呮牳娈嬬暀銆?5. **鏋勫缓娌′骇鍑烘柊鍐呮牳鏃讹紝鍏?`rm -rf out/vince/tree/build/xnu/ios-obj` 鍏ㄩ噺閲嶅缓銆?*
   鐥囩姸锛氬唴鏍?mtime 涓嶅彉銆乣strings` 鏌ヤ笉鍒版柊鏍囩銆傝繖鏄敮涓€鎭㈠鎵嬫銆?
## 涓夈€佸綋鍓嶅熀绾匡紙2026-10-24 鏅氾紝宸蹭笂鏈洪獙璇侊級

- **灞忓箷鍋滃湪**锛歚unexpected SIGKILL of %s %s with reason -- launchd`锛宍ESR=2516582469`
- **鍐呮牳**锛歮d5 `e9ebb7e6377d4e1dfd6fe2f5fa733159`锛?7:41 鏋勫缓锛屽凡鍒锋満楠岃瘉
- **浠撳簱 HEAD**锛?  - `Lux12138/UniXNU` 鈫?**`aae83c4`**锛堢函鎺㈤拡锛屾棤 DWC3銆佹棤閲嶅惎璋冪敤锛?  - `Lux12138/unixnu-vince` 鈫?**`105e1bb`**锛堝惈 trust_cache銆佸叏閮ㄦ枃妗ｏ級
- **宸蹭慨澶?*锛歟xecve 缂洪〉锛圥AC `VM_KERNEL_STRIP_PTR`锛夈€丄MFI boot-args銆乼rust cache 鎺ュ叆
- **鏈В**锛歭aunchd 琚?`OS_REASON_EXEC + SECURITY_POLICY` 鏉€鎺夛紝涓冧釜鐢熶骇鑰呭叏閮ㄦ帓闄?
## 鍥涖€佸鐜板熀绾匡紙3 鏉″懡浠わ級

```bash
# WSL 鍐?cd ~/src/UniXNU && git checkout aae83c4 2>/dev/null
cd ~/src/unixnu-vince && git checkout 105e1bb 2>/dev/null
bash /mnt/c/Temp/auto/build_pack_short.sh
```
```powershell
# Windows 渚?cd C:\platform-tools
.\fastboot.exe flash cust C:\Temp\cust-final2.img
.\fastboot.exe boot C:\Users\Administrator\Desktop\unixnu-vince-kernel-ufs\vince-xnu64-Z.img
```

**鏋勫缓鎴愬姛鐨勫垽鎹?*锛堝埆鍐嶈楠楋級锛?- `/tmp/bv2.log` 鍑虹幇 `built kernel at`锛?*涓嶅嚭鐜?* `KERNEL NOT REGENERATED`
- `out/vince/kernel/kernel.macho` 鐨?**md5 涓庝笂涓€娆′笉鍚?*

## 浜斻€佷笅涓€姝ワ紙鎸変环鍊兼帓搴忥紝璇﹁浜ゆ帴鏂囨。 搂6锛?
1. **鍐呭瓨 ring buffer + UFS 鏃ュ織钀界洏** 鈥斺€?绾鐩娿€佷笉纰伴噸鍚€昏緫锛屼换浣?panic 閮借兘鐣欎笅瀹屾暣 log
   锛坄native_ufs_log_open/write/sync` API 宸茬幇鎴愶紝鍦?NativeUfs.cpp:1119-1180锛屾棤璋冪敤鑰咃級
2. **GccUsb.h** 鈥斺€?DWC3 鐨勬椂閽熼棬鎺э紝USB 鐨勫墠鎻?3. **閲嶅惎鏃舵満** 鈥斺€?鍦?`panic_trap_to_debugger` 灏鹃儴锛堝钩鍙板凡灏辩华锛夊姞寤舵椂閲嶅惎锛宐oot-arg 闂ㄦ帶
4. 涓荤嚎 SIGKILL 鈥斺€?鏈変簡瀹屾暣 log 鍚庯紝涓€娆?panic 灏辫兘瀹氫綅 `SECURITY_POLICY` 鐨勭湡姝ｆ潵婧?
## 鍏€佹渶瀹规槗韪╃殑鍧戦€熸煡

| 鐥囩姸 | 鐪熷嚩 |
|---|---|
| 鍐呮牳 mtime 涓嶅彉銆佹柊鎺㈤拡鏌ヤ笉鍒?| `ios-obj` 缂撳瓨鎹熷潖 鈫?娓呭畠鍏ㄩ噺閲嶅缓 |
| 灞忓箷涓婃帰閽?娌℃樉绀? | 鍏堟煡琛屽彿琛紙琛屽啿绐?琚鐩栵級锛屼笉鏄?娌℃墽琛? |
| `Kernel data abort` + `FAR=0` + 鍋滃湪 `Initializing serial KDP` 鍚?| **DWC3 椹卞姩鏃犳椂閽熷啓瀵勫瓨鍣?*锛圗SR `...2405`锛?|
| `git push` exit=0 浣嗘敼鍔ㄦ病鐢熸晥 | 鐢?`git show origin/main:<file>` 楠岃瘉锛涙垨鏀圭敤 GitHub API PUT |
| 鏀逛簡 board.toml 浣嗘病鏁堟灉 | defconfig 鐨?`CONFIG_XNU_*` 鏈繀浼犺繘鏋勫缓鑴氭湰锛屽厛鎵撳嵃鍙橀噺鍊?|

