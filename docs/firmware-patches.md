# 鍥轰欢鏀瑰姩娓呭崟锛圡u-Silicium for vince锛?
宸ヤ綔鐩綍锛歐SL `/root/Mu-Silicium`锛圗DK2 / Mu UEFI锛?
## 1. FD 灏哄淇濇寔涓嶅彉

`Resources/Configs/vince.toml`

```toml
[uefi_fd]
base = 0x9FC00000
size = 0x300000      # 3MB锛屼笉瑕佹斁澶э紙>32MB 浼氬鑷村浐浠惰捣涓嶆潵锛?```

## 2. fdf锛氫笉瑕佸唴宓?unixnu.toml

`Platforms/Xiaomi/vincePkg/vince.fdf` 鐨?`[FV.FvMain]` 閲岀Щ闄わ細

```
FILE RAW = 7D9C9E2A-3B4F-4C8E-9A11-2B3C4D5E6F70 {
  SECTION RAW = vincePkg/unixnu.toml
}
```

鍘熷洜锛欶V 鍐呭祵閰嶇疆杩欐潯璺?`Config->Volume` 鎭掍负 NULL锛孌arwinBoot 浼氭姤 `NULL input`銆?鏀圭敱 `cust` FAT 鍒嗗尯鎻愪緵閰嶇疆銆?
## 3. fdf锛氫繚鐣?DarwinBoot

`[FV.FvMain]` 涓繀椤绘湁锛?
```
INF UniXNUPkg/Application/UniXNU/UniXNU.inf
INF UniXNUPkg/Driver/UniXNUDxe/UniXNUDxe.inf
INF DarwinBootPkg/Driver/DarwinBoot.inf
```

## 4. APRIORI锛氬己鍒舵淳鍙?DarwinBoot锛堝叧閿紒锛?
`Platforms/Xiaomi/vincePkg/Include/APRIORI.inc`锛屽苟鍏?*绗竴涓?* `APRIORI DXE { ... }` 鍧楋細

```
APRIORI DXE {
  INF MdeModulePkg/Core/Dxe/DxeMain.inf
  ...
  INF DarwinBootPkg/Driver/DarwinBoot.inf      # 鈫?鏂板杩欎竴琛?}
```

涓嶅姞杩欒鏃?`LocateProtocol(gUniXNULoaderProtocolGuid)` 杩斿洖 `Not Found`锛?DarwinBoot 鐨?`Boot()` 瀹屽叏涓嶆墽琛屻€?
涓嶈鍗曠嫭鏂板紑涓€涓?`APRIORI DXE {}` 鍧楋紙GenFv 浼氭姤 `ERROR 2000: Invalid parameter`锛夈€?
## 5. 濡傛灉灏嗘潵瑕佸姞鑷缓 DXE 椹卞姩

- 妯″潡鏀?`Silicium-ACPI/Platforms/Xiaomi/vince/Drivers/<Name>/`锛坄vince/` 鏄寘鏍癸級
- dsc `[LibraryClasses]` 闇€瑕佽ˉ锛?  ```
  FileExplorerLib|MdeModulePkg/Library/FileExplorerLib/FileExplorerLib.inf
  UefiDriverEntryPoint|MdePkg/Library/UefiDriverEntryPoint/UefiDriverEntryPoint.inf
  ```
  鍚﹀垯閾炬帴鎶?`undefined symbol: _ModuleEntryPoint`

## 6. 宸茬煡鏃犳晥灏濊瘯锛堝埆鍐嶈瘯锛?
| 鍋氭硶 | 缁撴灉 |
|---|---|
| 鎶婂唴鏍?RAW 濉炶繘 FVMAIN | FVMAIN 62MB锛孭EI 瑙ｅ帇澶辫触 鈫?鍥?fastboot |
| 鍐呮牳 LZMA 鍘嬬缉鍚庡 FVMAIN | FVMAIN 15MB锛屼粛瓒呴绠?鈫?鍥?fastboot |
| blob 鍐欏湪 FD 鍐呫€丗V 澶栵紙FD 60MB锛?| FD 澶ぇ锛孊ootShim 璧蜂笉鏉?|
| 娉ㄥ唽 ramdisk 鍒?`0x11000000` | ABL 瀹為檯涓嶆斁杩欓噷 鈫?data abort |
| 鐢?DarwinBoot 椹卞姩鍏ュ彛鍋?ramdisk 娉ㄥ唽 | 椹卞姩鍏ュ彛涓嶆墽琛岋紙瑙佸潙 6锛?|

