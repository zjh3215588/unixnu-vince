# vince (Redmi 5 Plus) — Adreno 506 GPU 渲染 bring-up

本目录记录在 **Redmi 5 Plus (vince / MSM8953 / SD625 / 8×A53 / Adreno 506 / 3GB+32GB)** 上让
XNU + iOS16 的 CoreAnimation 真正跑在 **Adreno 506** 上的完整过程与可复现工具。
上游内核移植自 sweet；上游只保证 4GB/64GB，本目录解决 3GB + vince 显示通路差异。

## 结论（硬证据）

- 内核 GPU bring-up 11 步全 SUCCESS（CP 首命令 `0xc0ffee01`、zap 认证出 secure、CP up `0xc0ffee02`、`VinceGPU service registered`）。
- 用户态 Mesa/freedreno 认到 GPU：`gputest: vendor freedreno / renderer FD506 / version OpenGL ES 3.1 Mesa 25.0.7`。
- CoreAnimation 接管：`redwood-gl: 7 of 7 methods of EAGLContext are ours`，
  `an OpenGL ES 3 context for CoreAnimation, by Mesa … FD506`，IOSurface→texture + shader 编译真实发生。
- 显示零拷贝：`VINCE FB: vincezero on: the window server's surface is scanned out by VIG0`。
- 完整日志见 `evidence/gpu-render-log.txt`。

## 关键根因与修复

`gpu=1` 早期 panic：`pc=AppleCLCD::showDirect+0x140, far=0x18`。
反汇编定位 showDirect 的 MDP-latch 等待循环读 `fCtl0`(偏移0x570)，其映射的是 sweet 的 MDP `0x05e02000`，
在 vince 上为 NULL。**vince 正确通路是 1018 补丁零拷贝**：必须 `vincezero=1`
（映射 `fZCtl=0x01a02000`、置 `fZero=true`）。漏掉 `vincezero=1` 是 v35/v36/v38 panic 的共同原因。

## 启动 cmdline（v44，已验证可进系统）

```
cpus=8 gpu=1 adreno=11 vincecache=1 vinceplace=1 vincezero=1 vincelog=1 vincelogsecs=1 sweetfb_noconsole=1
```

（v43 同上去掉 `sweetfb_noconsole=1`，用于带控制台调试。）

## 复现步骤

1. 重打包 boot：`python3 repack_vince.py --src <v31 img> --kernel <kernel.gpu.sweet> --cmdline "<上面 cmdline>"`。
2. 安装 GPU 用户态到根镜像（HFSX，用 libguestfs，WSL 无 hfsplus 模块）：
   `guestfish --rw -a ios16-root-v2.img -f topaz-install.gf`（mount-options rw,force），
   或 `vince-topaz-install.py` / `vince-gputest-install.py`。产物来自 topaz-ios / mesa-ios（arm64 iOS Mach-O）。
3. 重刷 userdata：先 `cp` 到 ext4 再 `img2simg`（drvfs 不支持 SEEK_HOLE，直接读 /mnt/d 会挂），
   得 sparse 后经 UNC `\\wsl.localhost\Ubuntu2204\root\gpu.simg` 以 `fastboot -S 256M flash userdata` 刷入（raw 直刷不可靠）。
4. `fastboot boot v44.img`；首启停 logo 数分钟属正常（keybag/数据迁移），随后进系统。
5. 拉持久日志：TWRP 下 dd userdata 尾块，`python3 sweet-log.py` 解码，grep `gputest|topaz|redwood|vincezero`。
6. 固定开机直入：`fastboot flash boot v44.img && fastboot reboot`。

## 已知问题（3GB 限制）

- jetsam 会杀超限 daemon（driverkitd 等）；SpringBoard 扩展在 3GB 上可能 SIGKILL，可用 `vincenolimit=1` 缓解。
- `vince-gputest` 自检偶发 SIGBUS（GPU 缓存映射 unaligned-store，README 已知 open 问题），不阻塞 backboardd 主渲染。
- `vinceplace` 池几分钟填满（上游已知 open 问题）。

## 文件清单

- `repack_vince.py` boot 重打包；`sym-panic.py` panic 符号化/反汇编。
- `mk-launchd-gpu.py` / `topaz-install.gf` GPU 用户态注入安装。
- `vince-topaz-install.py` / `vince-gputest-install.py` / `vince-gpu-fw.py` / `mkadt_vince.py` 上游 vince 工具。
- `sweet-log.py` 持久日志解码。
- `evidence/gpu-render-log.txt` GPU bring-up + 渲染硬证据。