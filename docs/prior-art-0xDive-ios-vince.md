# 鍓嶄綔瀵规瘮锛?xDive/ios-vince

璋冩煡鏃堕棿 2026-10-21銆備粨搴?<https://github.com/0xDive/ios-vince>
锛?026-10-19 鍒涘缓锛孭ython锛?2 涓?open PR/issue锛屾渶鏂?#34锛夈€?
## 浠栦滑璧扮殑鏄畬鍏ㄤ笉鍚岀殑璺?
| 缁村害 | 0xDive/ios-vince | 鏈」鐩紙unixnu-vince锛?|
|---|---|---|
| 寮曞灞?| **U-Boot v2026.07**锛圦ualcomm phone U-Boot锛宲in `ece349ad...`锛?| **Mu-Silicium EDK2** + UniXNU |
| 褰撳墠鐩爣 | 鍏堣В鍐?*鏃ュ織閫氶亾**锛圲SB gadget ACM console / `fastboot oem console`锛?| 鐩存帴鍚姩 XNU |
| 瀹炴祴杩涘害 | 鍗″湪鍥轰欢 / USB 鏍?bring-up锛?*娌℃湁 XNU 鍚姩鎴愭灉** | **XNU 鍐呮牳宸茶繘鍏ユ墽琛?*锛坄DARWINBOOT: hand-off to the kernel`锛?|

## 浠栦滑鐨勫叿浣撳崱鐐癸紙PR #30鈥?34锛?
鐩爣鏄 Qualcomm USB 鏍堝湪 EDK2 閲屾椿杩囨潵锛屼互渚跨敤 USB 褰撲覆鍙ｏ細

- 鎷垮埌 `PciHostBridge` 鐨?PE32 鑳?`LoadImage` 鎴愬姛锛屼絾
  `EFI_PCI_ROOT_BRIDGE_IO` / `EFI_PCI_IO` / `EFI_USB2_HC` / `EFI_USB_IO` **鍏ㄩ儴缂哄け**
- 渚濇嵁鏃у紑婧?`XhciPciEmulation.c`锛岃涓哄簲缁戝畾 `QCOM_USB_CONFIG_PROTOCOL`
  锛圙UID `E722B03F-B250-42CE-8EBD-5BD51812D037`锛屽凡鍦ㄥ叾 pinned SM8150 浜岃繘鍒堕噷楠岃瘉瀛樺湪锛夛紝
  `EFI_USB_INIT` GUID `2DA15AC7-4909-4C4C-B8C3-A742195EA46E`
- 璋冩暣 DXE 椤哄簭锛坄pci-first` / `usb-stack-first`锛変細鍦?**EFI Shell 涔嬪墠鍚屾寮傚父**锛?  `ELR 0x13FE0C440`銆乣ESR 0x02000000`锛圗C=0锛夈€乣FAR=0`
  鈫?绂荤嚎绗﹀彿鍖栧埌 `ArmCpuDxe::UpdateRegionMappingRecursive()`锛?  鏍堥噷鏈?`DxeCore::SetUefiImageMemoryAttributes()` / `ProtectUefiImage()`
- 璇曡繃 `PcdImageProtectionPolicy = 0` 鍏虫帀闀滃儚淇濇姢鏉ュ畾浣嶏紝浠嶆湭璺戦€?- Stage 8鈥?1 澶ч噺 "host-only 瀹¤"锛圲-Boot 缂栬瘧銆乶abu DTS銆丳M8150B Type-C/PHY锛夛紝
  鎵€鏈変骇鐗╀竴寰嬫爣 `safe_to_boot = false`锛?*浠庢湭鍙戝竷鍙惎鍔ㄩ暅鍍?*

## 瀵规垜浠湁鐢ㄧ殑涓夋潯鎯呮姤

### 1. EDK2 闀滃儚淇濇姢鐨勫潙锛堣涓嬫潵锛?
`ArmCpuDxe::UpdateRegionMappingRecursive` + `PcdImageProtectionPolicy` 缁勫悎锛?鍦ㄦ垜浠敼 fdf / APRIORI / FD 灏哄鏃?*娌℃湁韪╁埌**锛屼絾涓€鏃︽敼鍔ㄩ暅鍍忓竷灞€鎴栨潈闄愶紝
鍙兘瑙﹀彂鍚岀被鏃╂湡 MMU 宕╂簝銆傛帓鏌ユ墜娈碉細`PcdImageProtectionPolicy = 0` 鍋氬崟鍙橀噺瀵圭収銆?
### 2. vince 鍏叡 DTS锛圥MGR 闃舵鐨勭幇鎴愯祫鏂欙級

```
repo:   https://github.com/SeimoDev/linux-xiaomi-vince
commit: 4e6d08bb1b467c721e19cd693e4ec7388d982d73
file:   arch/arm64/boot/dts/qcom/sm8150-xiaomi-vince.dts
鍏煎:   "xiaomi,vince", "qcom,sm8150"
```

PMGR / UFS / 鏃堕挓 / 绋冲帇鍣ㄨ妭鐐?*鐩存帴鎶勮繖涓簮**锛屾瘮閫嗗悜 ApplePMGR 蹇緱澶氥€?娉ㄦ剰锛氶渶瑕侀厤濂楃殑 `sm8150-wcd9340.dtsi`锛孶-Boot 鑷甫鏍戦噷娌℃湁銆?
### 3. USB / PHY 纭欢鍙傛暟锛堜互鍚庡啓 USB銆佸厖鐢甸┍鍔ㄨ鐢級

| 椤?| 鍊?|
|---|---|
| USB1 wrapper | `0x0A6F8800`锛圤TG锛孒igh-Speed锛?|
| USB1 HS PHY | `0x088E2000` |
| USB2 controller | `0x0A800000`锛坔ost锛?*SuperSpeed Plus**锛?|
| PHY 渚涚數 | 0.880V(PLL) / 1.800V(digital) / 3.072V(analog) |
| Type-C | `qcom,pm8150b-typec` + `qcom,pm8150b-vbus-reg` |
| Android 瀹炴祴 | `/sys/class/udc/a600000.dwc3`锛歚state=configured`锛宍maximum_speed=high-speed`锛宍is_otg=1` |

## 缁撹

**涓嶈窡闅忎粬浠殑璺嚎銆?* 浠栦滑涓轰簡鎷挎棩蹇楃粫鍘?U-Boot锛岀粨鏋滃崱鍦ㄥ浐浠跺眰锛?鏈」鐩凡缁忔湁鍙敤鐨勬棩蹇楁墜娈碉紙灞忓箷 `Print` + 蹇呰鏃?UART 115200锛夛紝
骞朵笖宸茬粡瓒婅繃浠栦滑娌″埌杩囩殑浣嶇疆锛堝唴鏍告墽琛岋級銆?
鍙€熼壌鐨勫彧鏈変笂闈笁鏉?*璧勬枡鎬?*鎯呮姤锛屽挨鍏舵槸 vince 鍏叡 DTS 鈥斺€?鐩存帴鏈嶅姟浜?PMGR銆?
