# vince 鍏叡璁惧鏍戣捀棣忥紙PMGR / 瀛樺偍 / 鏃堕挓 / PMIC锛?
鏉ユ簮锛坧inned锛夛細
```
https://github.com/SeimoDev/linux-xiaomi-vince
commit 4e6d08bb1b467c721e19cd693e4ec7388d982d73
file   arch/arm64/boot/dts/qcom/sm8150-xiaomi-vince.dts
```
> 鏉跨骇 dts 鏄?overlay 椋庢牸锛宍gcc` / `ufs*` / `cpus` / `pmic` / RPMh 鑺傜偣鍦?> 鍚?commit 鐨?`sm8150.dtsi`銆乣pm8150{,b,l}.dtsi` 閲屻€?
鏉跨骇鏍囪瘑锛歚compatible = "xiaomi,vince", "qcom,sm8150"`锛宍model = "Xiaomi Pad 5"`锛?`chassis-type = "tablet"`銆?
---

## 1. RPMh / 鐢垫簮绠＄悊锛?*鏈€閲嶈**锛?
| 鑺傜偣 | compatible | 鍦板潃 | 璇存槑 |
|---|---|---|---|
| `apps_rsc: rsc@18200000` | `qcom,rpmh-rsc` | **`0x18200000 +0x10000`**<br>**`0x18210000 +0x10000`**<br>**`0x18220000 +0x10000`** | **RPMh RSC 瀹炰綋锛屼笁涓?bank** |
| `rpmhpd: power-controller` | `qcom,sm8150-rpmhpd` | 鏃?reg锛坄apps_rsc` 瀛愯妭鐐癸級 | 鐢垫簮鍩?|
| `rpmhcc: clock-controller` | `qcom,sm8150-rpmh-clk` | 鏃?reg锛坄apps_rsc` 瀛愯妭鐐癸級 | RPMh 鏃堕挓 |
| `aop_cmd_db: memory@85f20000` | `qcom,cmd-db` | `0x85f20000 +0x20000` | cmd-db |
| `smem` | `qcom,smem` | `memory-region = <&smem_mem>` 鈫?`0x86000000 +0x200000` | SMEM |
| `apss_shared: mailbox@17c00000` | `qcom,sm8150-apss-shared` | `0x17c00000 +0x1000` | **apss_shared mailbox锛堜笉鏄?RPMh锛?* |
| `spmi_bus: spmi@c440000` | `qcom,spmi-pmic-arb` | `0xc440000 +0x1100`銆乣0xc600000 +0x2000000`銆乣0xe600000 +0x100000`銆乣0xe700000 +0xa0000`銆乣0xc40a000 +0x26000` | SPMI arbiter |
| `pdc: interrupt-controller@b220000` | `qcom,sm8150-pdc` | `0xb220000 +0x30000` | PDC |
| `osm_l3: interconnect@18321000` | `qcom,sm8150-osm-l3` | `0x18321000 +0x1400` | OSM L3 |

> 鈿狅笍 **淇**锛歋M8150 娌℃湁 `qcom,ipcc` 鑺傜偣锛屼篃娌℃湁 legacy `qcom,rpm`銆?> 涔嬪墠鎶?`0x17c00000` 褰?RPMh 鏄敊鐨勨€斺€斿畠鏄?apss_shared mailbox銆?> **RPMh 蹇呴』璁块棶 `0x18200000` 閭ｄ竴鐗囥€?*

浜掕繛锛坕nterconnect锛夎妭鐐逛竴瑙堬紙鍋氬甫瀹?鏃堕挓鏃跺彲鑳界敤鍒帮級锛?
| 鑺傜偣 | compatible | 鍦板潃 |
|---|---|---|
| config_noc | `qcom,sm8150-config-noc` | `0x1500000 +0x7400` |
| system_noc | `qcom,sm8150-system-noc` | `0x1620000 +0x19400` |
| mc_virt | `qcom,sm8150-mc-virt` | `0x163a000 +0x1000` |
| aggre1_noc | `qcom,sm8150-aggre1-noc` | `0x16e0000 +0xd080` |
| aggre2_noc | `qcom,sm8150-aggre2-noc` | `0x1700000 +0x20000` |
| compute_noc | `qcom,sm8150-compute-noc` | `0x1720000 +0x7000` |
| mmss_noc | `qcom,sm8150-mmss-noc` | `0x1740000 +0x1c100` |
| dc_noc | `qcom,sm8150-dc-noc` | `0x9160000 +0x3200` |
| gem_noc | `qcom,sm8150-gem-noc` | `0x9680000 +0x3e200` |
| camnoc_virt | `qcom,sm8150-camnoc-virt` | `0xac00000 +0x1000` |

## 2. GCC锛堟椂閽?/ 澶嶄綅 / GDSC锛?
| 鑺傜偣 | compatible | reg | cells |
|---|---|---|---|
| `gcc: clock-controller@100000` | `qcom,gcc-sm8150` | `0x100000 +0x1f0000` | `#clock-cells = <1>`, `#reset-cells = <1>`, `#power-domain-cells = <1>` |

## 3. UFS锛堜笌 `NativeUfs` 瀵瑰簲锛?
| 鑺傜偣 | compatible | reg |
|---|---|---|
| `ufs_mem_hc: ufshc@1d84000` | `qcom,sm8150-ufshc`, `qcom,ufshc`, `jedec,ufs-2.0` | `0x1d84000 +0x2500`锛坰td锛夈€乣0x1d90000 +0x8000`锛坕ce锛?|
| `ufs_mem_phy: phy@1d87000` | `qcom,sm8150-qmp-ufs-phy` | `0x1d87000 +0x1000` |

`status = "okay"`锛沗lanes-per-direction = <2>`锛沚oot device `soc@0/1d84000.ufshc`銆?
## 4. UFS 渚涚數锛堝啓鐢垫簮椹卞姩瑕佺収杩欎釜锛?
| supply | 绋冲帇鍣?| PMIC 杞?| 鐢靛帇 | 鐢垫祦涓婇檺 |
|---|---|---|---|---|
| `vcc-supply` | `vreg_l10a_2p5` | pm8150 ldo10 | 2504鈥?950 mV | 750 mA |
| `vccq-supply` | `vreg_l9a_1p2` | pm8150 ldo9 | 1200 mV | 700 mA |
| `vccq2-supply` | `vreg_s4a_1p8` | pm8150 S4锛堝浐瀹氾級 | 1800 mV | 750 mA |
| `vdda-phy-supply` | `vreg_l5a_0p8` | pm8150 ldo5 | 880 mV | 90.2 mA |
| `vdda-pll-supply` | `vreg_l3c_1p2` | pm8150l ldo3 | 1200 mV | 19 mA |

PMIC 鑺傜偣锛圫PMI USID锛夛細

| PMIC | 鑺傜偣 | compatible | reg |
|---|---|---|---|
| pm8150 | `pmic@0` | `qcom,pm8150`, `qcom,spmi-pmic` | `0x0` |
| pm8150b | `pmic@2` | `qcom,pm8150b`, `qcom,spmi-pmic` | `0x2` |
| pm8150l | `pmic@4` | `qcom,pm8150l`, `qcom,spmi-pmic` | `0x4` |
| pm8009 | **涓嶅瓨鍦?*锛堟澘绾ф敞閲婃敞鏄?not present锛?| 鈥?| 鈥?|

RPMh 绋冲帇鍣ㄧ粍锛坄apps_rsc` 涓嬶級锛歚pm8150-rpmh-regulators`锛坄pmic-id = "a"`锛夈€?`pm8150l-rpmh-regulators`锛坄pmic-id = "c"`锛夈€?
## 5. CPU锛堜笌 ADT 鐨?`cpu-regs` 涓€鑷?鉁擄級

`cpu@0/100/200/300/400/500/600/700`锛宍reg = <0x0 0xN00>`锛?`compatible = "qcom,kryo485"`锛宍enable-method = "psci"`锛?idle 璧?`domain-idle-states`锛坄/cpus/idle-states`锛宍entry-method = "psci"`锛夈€?鏉跨骇棰濆鍔?`cpu7_opp21 = 2956800000 Hz`銆?
> 涓庢垜浠?ADT 閲岀殑 `--cpu-regs "0,0x100,...,0x700"` **瀹屽叏瀵逛笂**锛屾棤闇€鏀瑰姩銆?
---

## 瀵?PMGR 鐨勭洿鎺ョ粨璁?
1. **RPMh 璁块棶鐩爣鏀逛负 `0x18200000`**锛? 涓?bank锛夛紝涓嶆槸 `0x17c00000`
2. cmd-db `0x85f20000`銆丼MEM `0x86000000` 缁存寔鍘熷垽鏂?3. 鐢靛帇/鏃堕挓涓嶈鑷繁鐚滐細UFS 浜旇矾渚涚數涓?PMIC USID 鐩存帴浠庢湰琛ㄥ彇
4. `rpmhpd` / `rpmhcc` 鏄?`apps_rsc` 鐨?*瀛愯妭鐐?*锛屾剰鍛崇潃鐢垫簮鍩熶笌鏃堕挓閮借
   閫氳繃 RPMh 鍛戒护閫氶亾涓嬪彂锛堝拰鑻规灉鐨?MMIO PMGR 瀹屽叏涓嶅悓锛?
