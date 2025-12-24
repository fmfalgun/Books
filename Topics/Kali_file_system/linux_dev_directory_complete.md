# Linux /dev Directory - Complete Device Files Categorization

**Comprehensive categorization of ALL device files, character devices, block devices, and special files in the `/dev` directory with detailed explanations of their functions.**

---

## Table of Contents

1. [Storage & Block Devices](#1-storage--block-devices)
2. [Terminal & Console Devices](#2-terminal--console-devices)
3. [Pseudo-Devices & Memory](#3-pseudo-devices--memory)
4. [Input Devices](#4-input-devices)
5. [Display & Graphics](#5-display--graphics)
6. [Audio Devices](#6-audio-devices)
7. [USB Devices](#7-usb-devices)
8. [Network Devices](#8-network-devices)
9. [Cryptographic & Security Hardware](#9-cryptographic--security-hardware)
10. [Virtualization Devices](#10-virtualization-devices)
11. [Special Hardware Interfaces](#11-special-hardware-interfaces)
12. [Watchdog & System Monitoring](#12-watchdog--system-monitoring)
13. [Device Mapper & LVM](#13-device-mapper--lvm)
14. [Disk Organization & Identification](#14-disk-organization--identification)

---

## 1. Storage & Block Devices

| **Category** | **Device Files & Directories** | **Explanation** |
|---|---|---|
| **NVMe Storage (M.2/PCIe)** | `nvme0`, `nvme0n1`, `nvme0n1p1`, `nvme0n1p2`, `nvme0n1p3`, `nvme0n1p4`, `nvme0n1p5`, `nvme0n1p6` | NVMe (Non-Volatile Memory Express) SSD connected via PCIe. `nvme0` = entire drive, `nvme0n1` = namespace 1, `nvme0n1pX` = partition X. Character device 244:0 for nvme0 |
| **Block Device Index** | `/dev/block/259:0` → `../nvme0n1`, `/dev/block/259:1` → `../nvme0n1p1`, `/dev/block/259:2` → `../nvme0n1p2`, `/dev/block/259:3` → `../nvme0n1p3`, `/dev/block/259:4` → `../nvme0n1p4`, `/dev/block/259:5` → `../nvme0n1p5`, `/dev/block/259:6` → `../nvme0n1p6` | Kernel block device indices using major:minor numbers (259 = NVMe major device number). These are symlinks for device identification. Used by kernel to manage block I/O |
| **Filesystem Control** | `btrfs-control` | Btrfs (B-tree filesystem) control device for managing Btrfs volumes and administration. Required for Btrfs-specific operations |

---

## 2. Terminal & Console Devices

| **Category** | **Device Files & Directories** | **Explanation** |
|---|---|---|
| **Virtual Terminals (VT)** | `tty0`, `tty1`, `tty2`, `tty3`, `tty4`, `tty5`, `tty6`, `tty7`, `tty8`, `tty9`, `tty10`, `tty11`, `tty12`, `tty13`, `tty14`, `tty15`, `tty16`, `tty17`, `tty18`, `tty19`, `tty20`, `tty21`, `tty22`, `tty23`, `tty24`, `tty25`, `tty26`, `tty27`, `tty28`, `tty29`, `tty30`, `tty31`, `tty32`, `tty33`, `tty34`, `tty35`, `tty36`, `tty37`, `tty38`, `tty39`, `tty40`, `tty41`, `tty42`, `tty43`, `tty44`, `tty45`, `tty46`, `tty47`, `tty48`, `tty49`, `tty50`, `tty51`, `tty52`, `tty53`, `tty54`, `tty55`, `tty56`, `tty57`, `tty58`, `tty59`, `tty60`, `tty61`, `tty62`, `tty63` | Linux virtual terminals (64 total). Character device major 4. Accessible via Alt+F1, Alt+F2, etc. for text-based console access. `tty0` = current active terminal |
| **Serial Terminals** | `ttyS0`, `ttyS1`, `ttyS2`, `ttyS3` | Serial ports (COM1-COM4) for legacy serial devices, debugging via serial console, BMC/IPMI access. Character device major 4 (minor 64-67) |
| **Master Console** | `console` | System console device - where kernel messages and boot messages appear. Typically `/dev/tty0` or redirected to serial port |
| **Pseudo-Terminal Master/Slave** | `ptmx` (Character device 5:2), `pts/0`, `pts/1` | Pseudo-terminal multiplexer (`ptmx`) allows creation of virtual terminal pairs. `/dev/pts/X` = slave terminals for SSH, screen, tmux sessions |
| **TTY Control Device** | `tty` (Character device 5:0) | General TTY device - writes go to current terminal |

---

## 3. Pseudo-Devices & Memory

| **Category** | **Device Files & Directories** | **Explanation** |
|---|---|---|
| **Null Device** | `null` (Character device 1:3) | Discards all data written to it, returns EOF on read. Used for redirecting unwanted output (`>/dev/null 2>&1`) |
| **Zero Device** | `zero` (Character device 1:5) | Infinite source of null bytes. Used for creating sparse files, wiping memory, benchmarking |
| **Full Device** | `full` (Character device 1:7) | Simulates a full disk - any write returns ENOSPC error. Used for testing error handling |
| **Random Number Generator** | `random` (Character device 1:8) | Cryptographically secure random number source (entropy-based). Slower but more secure than urandom |
| **Pseudo-Random Generator** | `urandom` (Character device 1:9) | Pseudo-random number generator. Faster than `/dev/random`, suitable for most applications |
| **Memory Access** | `mem` (Character device 1:1) | Direct physical RAM access device. Requires root. Dangerous - used for kernel debugging only |
| **Core Dump** | `core` → `/proc/kcore` | Kernel core dump access via symlink to /proc. Used for post-mortem kernel debugging |
| **Port I/O** | `port` (Character device 1:4) | I/O port access device for x86 systems. Used by tools like `ioctl` for hardware access |
| **Message Queue** | `mqueue` (Directory) | POSIX message queue filesystem mount point. Not a device file, but special filesystem |

---

## 4. Input Devices

| **Category** | **Device Files & Directories** | **Explanation** |
|---|---|---|
| **Keyboard Events** | `input/event0` (Character device 13:64) | Keyboard input events (ps/2 keyboard). Event interface provides raw keyboard events |
| **Keyboard Additional** | `input/event1` (Character device 13:65), `input/event2` (Character device 13:66), `input/event7` (Character device 13:73) | Additional keyboard/input event devices |
| **Mouse Events** | `input/mouse0` (Character device 13:32), `input/mouse1` (Character device 13:33), `input/mice` (Character device 13:63) | Mouse input devices. `mouse0`/`mouse1` = individual mice, `mice` = all mice combined |
| **Generic Input Events** | `input/event3` (13:67), `input/event4` (13:68), `input/event5` (13:69), `input/event6` (13:70), `input/event8` (13:72), `input/event9` (13:73), `input/event10` (13:74), `input/event11` (13:75), `input/event12` (13:76), `input/event13` (13:77), `input/event14` (13:78) | Additional input event devices for touchpads, external keyboards, game controllers, etc. |
| **Input Device Mapping** | `input/by-path/` (Directory) | Symlinks organizing input devices by hardware path for stable identification. Includes: `platform-i8042-serio-0-event-kbd` → `../event0` (PS/2 keyboard), `platform-AMDI0010:00-event-mouse` → `../event6` (Trackpad), `platform-AMDI0010:00-mouse` → `../mouse1`, `platform-pcspkr-event-spkr` → `../event7` (PC Speaker) |

---

## 5. Display & Graphics

| **Category** | **Device Files & Directories** | **Explanation** |
|---|---|---|
| **Framebuffer** | `fb0` (Character device 29:0) | Linux framebuffer interface for direct graphics access. Used by X11, Wayland, and legacy graphics applications |
| **DRM/DRI Devices** | `/dev/dri/card0` (Character device 226:0), `/dev/dri/renderD128` (226:128) | Direct Rendering Management (DRM) devices. `card0` = primary GPU, `renderD128` = render-only GPU node for compute workloads (OpenGL, Vulkan) |
| **DRM Device Mapping** | `/dev/dri/by-path/` (Directory) | Organizes DRM devices by PCI path: `pci-0000:04:00.0-card` → `../card0`, `pci-0000:04:00.0-render` → `../renderD128` |
| **Display Aux Channel** | `drm_dp_aux0`, `drm_dp_aux1`, `drm_dp_aux2`, `drm_dp_aux3`, `drm_dp_aux4`, `drm_dp_aux5`, `drm_dp_aux6`, `drm_dp_aux7` (Character device 239:0-7) | DisplayPort Auxiliary channels for monitor communication, resolution negotiation, and EDID access. Multiple channels for multi-monitor setups |
| **VCS - Video Memory** | `vcs`, `vcs1`, `vcs2`, `vcs3`, `vcs4`, `vcs5`, `vcs6`, `vcs7` (Character device 7:0-7) | Virtual console screen memory - snapshot of text-mode video memory for current VT |
| **VCSA - Video Attributes** | `vcsa`, `vcsa1`, `vcsa2`, `vcsa3`, `vcsa4`, `vcsa5`, `vcsa6`, `vcsa7` (Character device 7:128-135) | Video console with attributes (color, bold, etc.) - enhanced version of VCS |
| **VCSU - Unicode** | `vcsu`, `vcsu1`, `vcsu2`, `vcsu3`, `vcsu4`, `vcsu5`, `vcsu6`, `vcsu7` (Character device 7:64-71) | Unicode console screen memory |

---

## 6. Audio Devices

| **Category** | **Device Files & Directories** | **Explanation** |
|---|---|---|
| **Audio Control** | `snd/controlC0` (Character device 116:7), `snd/controlC1` (116:11) | ALSA mixer control devices for managing audio levels, muting, routing |
| **PCM Playback** | `snd/pcmC0D3p` (116:2), `snd/pcmC0D7p` (116:3), `snd/pcmC0D8p` (116:4), `snd/pcmC0D9p` (116:5), `snd/pcmC1D0p` (116:8) | PCM playback (speaker/output) devices. Cards (C0/C1) with devices (D0-D9). `p` suffix = playback |
| **PCM Capture** | `snd/pcmC1D0c` (116:9) | PCM capture (microphone/input) device. `c` suffix = capture |
| **Hardware Devices** | `snd/hwC0D0` (116:6), `snd/hwC1D0` (116:10) | Hardware-specific audio device control (firmware, DSP) |
| **Sequencer** | `snd/seq` (116:1) | ALSA sequencer for MIDI and real-time synthesis |
| **Timer** | `snd/timer` (116:33) | System audio timer for synchronized playback |
| **Sound Device Mapping** | `snd/by-path/` (Directory) | PCI path identification: `pci-0000:04:00.1` → `../controlC0`, `pci-0000:04:00.6` → `../controlC1` |

---

## 7. USB Devices

| **Category** | **Device Files & Directories** | **Explanation** |
|---|---|---|
| **USB Bus Structure** | `/dev/bus/usb/` (Directory) | USB device hierarchy organized by bus and device number |
| **USB Buses** | `bus/usb/001/`, `bus/usb/002/`, `bus/usb/003/`, `bus/usb/004/`, `bus/usb/005/`, `bus/usb/006/`, `bus/usb/007/`, `bus/usb/008/`, `bus/usb/009/`, `bus/usb/010/` (10 USB buses) | Each directory represents a USB bus controller. Multiple buses for USB 2.0 and 3.0 ports |
| **USB Host Controllers** | `bus/usb/001/001` (Character device 189:0), `bus/usb/002/001` (189:128), `bus/usb/003/001` (189:256), `bus/usb/004/001` (189:384), `bus/usb/005/001` (189:512), `bus/usb/006/001` (189:640), `bus/usb/007/001` (189:768), `bus/usb/008/001` (189:896), `bus/usb/009/001` (189:1024), `bus/usb/010/001` (189:1152) | Root hubs (host controllers) |
| **USB Devices** | `bus/usb/001/002` (189:1), `bus/usb/001/003` (189:2), `bus/usb/005/001` (189:512), `bus/usb/005/002` (189:513) | Connected USB devices. Address space allocated per bus |
| **Video Devices (USB)** | `v4l/by-id/usb-DUJZC0A5AL2XEH_HP_FHD_Camera_0001-video-index0` → `../../video0`, `v4l/by-id/usb-DUJZC0A5AL2XEH_HP_FHD_Camera_0001-video-index1` → `../../video1` | USB camera device identification by serial number |
| **V4L Path Mapping** | `v4l/by-path/pci-0000:05:00.0-usb-0:1:1.0-video-index0` → `../../video0`, `v4l/by-path/pci-0000:05:00.0-usb-0:1:1.0-video-index1` → `../../video1`, `v4l/by-path/pci-0000:05:00.0-usbv2-0:1:1.0-video-index0` → `../../video0`, `v4l/by-path/pci-0000:05:00.0-usbv2-0:1:1.0-video-index1` → `../../video1` | USB camera device identification by PCI/USB path hierarchy |

---

## 8. Network Devices

| **Category** | **Device Files & Directories** | **Explanation** |
|---|---|---|
| **TUN Interface** | `net/tun` (Character device 10:200) | TUN device for user-space network driver. Used by OpenVPN, Wireguard, Docker containers |
| **PPP Interface** | `ppp` (Directory) | Point-to-Point Protocol devices directory. For modem, ISDN, PPPoE connections |

---

## 9. Cryptographic & Security Hardware

| **Category** | **Device Files & Directories** | **Explanation** |
|---|---|---|
| **TPM 2.0** | `tpm0` (Character device 10:224), `tpmrm0` (253:65536) | Trusted Platform Module 2.0 device for cryptographic operations and secure key storage. `tpm0` = standard TPM access, `tpmrm0` = TPM Resource Manager with process isolation |
| **Random Number Generator** | `hwrng` (Character device 10:183) | Hardware random number generator (CPU instruction-based entropy) for cryptographic seed |

---

## 10. Virtualization Devices

| **Category** | **Device Files & Directories** | **Explanation** |
|---|---|---|
| **KVM Hypervisor** | `kvm` (Character device 10:232) | Kernel-based Virtual Machine device for hardware-accelerated virtualization (QEMU, libvirt) |
| **VFIO Container** | `vfio/vfio` (Character device 10:196) | Virtual Function I/O (VFIO) device for userspace device access and GPU passthrough |
| **VHOST Network** | `vhost-net` (Character device 10:238) | Vhost networking backend for KVM accelerated networking |
| **VHOST Vsock** | `vhost-vsock` (Character device 10:241) | VHOST virtual socket for VM-to-host communication |
| **VHOST devices** | `vhost-net`, `vhost-vsock` (Character device range 238-241) | Virtual host devices for optimized hypervisor operations |

---

## 11. Special Hardware Interfaces

| **Category** | **Device Files & Directories** | **Explanation** |
|---|---|---|
| **GPIO** | `gpiochip0` (Character device 254:0) | General-Purpose Input/Output controller. Used for IoT, embedded systems, GPIO control |
| **HPET** | `hpet` (Character device 10:228) | High Precision Event Timer - precise system timer (x86 architecture). Used for timing and profiling |
| **RTC** | `rtc` → `rtc0`, `rtc0` (Character device 249:0) | Real-Time Clock for persistent time storage and BIOS clock sync |
| **Framebuffer** | `fb0` (Character device 29:0) | Legacy framebuffer interface for direct graphics memory access |
| **Media Device** | `media0` (Character device 237:0) | Media controller for video input/output (V4L2) |
| **KFD** | `kfd` (Character device 238:0) | Kernel Fusion Device for AMD GPU compute (ROCm) |
| **DMA Heap** | `dma_heap/system` (Character device 251:0) | DMA-compatible memory allocation for video, graphics, and hardware devices |

---

## 12. Watchdog & System Monitoring

| **Category** | **Device Files & Directories** | **Explanation** |
|---|---|---|
| **Watchdog Timer** | `watchdog`, `watchdog0` (Character device 10:130 for watchdog, 245:0 for watchdog0) | Hardware watchdog timer - reboots system if not "petted" periodically. Used for high-availability systems and crash recovery |
| **CPU DMA Latency** | `cpu_dma_latency` (Character device 10:259) | CPU DMA latency control - prevents CPU from entering deep sleep states. Used for real-time applications |

---

## 13. Device Mapper & LVM

| **Category** | **Device Files & Directories** | **Explanation** |
|---|---|---|
| **Device Mapper Control** | `mapper/control` (Character device 10:236) | Device Mapper control device for LVM (Logical Volume Manager) and dm-crypt operations |
| **Loop Devices** | `loop-control` (Character device 10:237) | Loop device control for mounting files as block devices |

---

## 14. Disk Organization & Identification

| **Category** | **Device Files & Directories** | **Explanation** |
|---|---|---|
| **By-ID Organization** | `/dev/disk/by-id/` (Directory with symlinks) | Persistent disk identification by model and serial number: `nvme-ABSNE27512KP_L52751201835` → `../../nvme0n1`, `nvme-ABSNE27512KP_L52751201835_1` → `../../nvme0n1`, `nvme-ABSNE27512KP_L52751201835_1-part1` → `../../nvme0n1p1`, `nvme-ABSNE27512KP_L52751201835_1-part2` → `../../nvme0n1p2`, etc. (up to part6); `nvme-eui.8c1f64aa40000092` → `../../nvme0n1`, `nvme-eui.8c1f64aa40000092-part1` through `part6` | Model-based persistent identification for udev rules and fstab mounting |
| **By-UUID Organization** | `/dev/disk/by-uuid/` (Directory with symlinks) | Mount-stable identification by filesystem UUID: `21ef7c92-3080-49d0-90a9-f2ccbfef9350` → `../../nvme0n1p5` (UUID), `2a591824-cda8-444c-b79a-22c02d62e7f7` → `../../nvme0n1p3` (UUID), `8DA5-272E` → `../../nvme0n1p4` (FAT UUID), `92D4-EC5C` → `../../nvme0n1p1` (FAT UUID), `bcf76581-d971-464f-bc51-76e0d62ed269` → `../../nvme0n1p2` (UUID), `dc5a2367-dace-4334-ab03-f18518cf23ef` → `../../nvme0n1p6` (UUID) | Filesystem UUID-based identification for reliable mounting |
| **By-DiskSeq** | `/dev/disk/by-diskseq/` (Directory) | Sequential disk enumeration: `1` → `../../nvme0n1`, `1-part1` through `1-part6` → partition references | Kernel-assigned sequential numbers for disk ordering |
| **By-Designator** | `/dev/disk/by-designator/` (Directory) | Partition designations: `esp` → `../../nvme0n1p1` (EFI System Partition), `swap` → `../../nvme0n1p3` (Swap partition) | Semantic partition identification |
| **By-Path** | `/dev/disk/by-path/pci-0000:03:00.0-nvme-1` → `../../nvme0n1`, `pci-0000:03:00.0-nvme-1-part1` through `part6`, `pci-0000:03:00.0-nvme-1-part-by-partnum/`, `pci-0000:03:00.0-nvme-1-part-by-partuuid/`, `pci-0000:03:00.0-nvme-1-part-by-uuid/` | PCI bus path identification for hardware topology-stable naming. Includes sub-directories for partition access methods: by-partnum (partition number 1-6), by-partuuid (partition UUIDs), by-uuid (partition filesystem UUIDs) |

---

## 15. Additional Special Devices

| **Category** | **Device Files & Directories** | **Explanation** |
|---|---|---|
| **Autofs** | `autofs` (Character device 10:235 in char, also listed as regular device) | Automatic filesystem mounting control device for NFS and other network filesystems |
| **HID Raw** | `hidraw0` (Character device 242:0) | Raw HID (Human Interface Device) access for custom USB device control and low-level input handling |
| **NG Netlink** | `ng0n1` (Character device 243:0) | Netlink socket device for kernel-to-userspace communication in network stack |
| **Snapshot** | `snapshot` (Character device 10:231) | Hibernation/suspend support device for state snapshots |
| **CUSE** | `cuse` (Character device 10:229) | Character device in userspace - allows userspace programs to act as character devices |
| **FUSE** | `fuse` (Character device 10:229) | Filesystem in Userspace - allows userspace programs to provide filesystems (SSHFS, Dropbox, etc.) |
| **User Fault FD** | `userfaultfd` (Character device 10:257) | User-space fault handler for page faults, used for live migration and memory management |
| **UDmaBuf** | `udmabuf` (Character device 10:258) | User-space DMA buffer for direct memory access from userspace programs |
| **VGA Arbiter** | `vga_arbiter` (Character device 10:256) | VGA resource arbitration for multiple graphics devices on x86 systems |
| **DBC** | `dbc` (Character device 10:260) | USB Data Bus Config for AMD systems |
| **RF Kill** | `rfkill` (Character device 10:242) | Radio frequency kill switch control (WiFi, Bluetooth, airplane mode) |
| **Shared Memory** | `shm/` (Directory), `shm/sem.haveged_sem` | POSIX shared memory filesystem with semaphore for haveged entropy daemon |
| **NVRAM** | `nvram` | CMOS/BIOS NVRAM access device (x86) |
| **UHID** | `uhid` (Character device 10:239) | User-space HID driver support |
| **UInput** | `uinput` (Character device 10:223) | User-space input device driver for creating synthetic input events |

---

## Summary Table: Device Major Numbers & Device Types

| **Device Class** | **Major Number** | **Count** | **Purpose** |
|---|---|---|---|
| **VT/TTY** | 4 | 64+ | Text terminals and serial ports |
| **TTY Control** | 5 | 3 | Master console and pseudo-terminal |
| **Memory/Null** | 1 | 7 | Pseudo-devices (mem, zero, null, etc.) |
| **Input** | 13 | 15+ | Keyboard, mouse, touchpad events |
| **Video/Framebuffer** | 29 | 1 | Legacy framebuffer |
| **DRI/GPU** | 226 | 2 | DRM graphics devices |
| **Audio (ALSA)** | 116 | 11+ | Sound card and PCM devices |
| **USB** | 189 | 20+ | USB host controllers and devices |
| **Watchdog/Timers** | 10 | 20+ | Watchdog, HPET, RFKill, etc. |
| **RTC** | 249 | 1 | Real-time clock |
| **NVMe** | 244 | 1 | NVMe controller |
| **Watchdog (new)** | 245 | 1 | Watchdog timer |
| **DMA Heap** | 251 | 1 | DMA memory allocation |
| **TPM Resource Mgr** | 253 | 1 | TPM resource manager |
| **GPIO** | 254 | 1 | General-purpose I/O |
| **Display Aux** | 239 | 8 | DisplayPort auxiliary channels |
| **VCS Console** | 7 | 16 | Virtual console memory |
| **VFIO** | 10 | 1 | Virtualization pass-through |
| **Total** | — | **200+** | Complete system hardware access |

---

## /dev Directory Statistics

| **Metric** | **Value** |
|---|---|
| **Total Directories** | 44 |
| **Total Files/Devices** | 486 |
| **Block Devices** | 7 NVMe partitions |
| **Character Devices** | 200+ (various hardware) |
| **Symlinks** | 150+ (identification layers) |
| **TTY Devices** | 64+ virtual terminals |
| **USB Buses** | 10 controllers |
| **Audio Cards** | 2 (controlC0, controlC1) |
| **Input Event Devices** | 15 (keyboards, mice, touchpads) |
| **Storage Partitions** | 6 NVMe partitions |

---

## Key Insights: Why Multiple Organizing Layers?

The `/dev` directory uses **symlink layers** for device identification because:

1. **Stability**: Device names like `/dev/ttyUSB0` can change. UUIDs and model numbers never do.
2. **Uniqueness**: `by-uuid/` guarantees exactly one device per filesystem UUID
3. **Persistence**: `by-id/` uses hardware serial numbers that survive reboots
4. **Flexibility**: `by-path/` preserves topology for BIOS-ordered slots
5. **Fallback**: Multiple layers ensure device discovery even if one fails

**Example Path Resolution:**
```
/dev/disk/by-uuid/bcf76581-d971-464f-bc51-76e0d62ed269
    ↓ symlink
/dev/nvme0n1p2
    ↓ actual block device
Character major:minor = 259:2 (in /dev/block/259:2)
```

---

## Practical Usage Examples

### Mounting by persistent ID:
```bash
mount /dev/disk/by-uuid/bcf76581-d971-464f-bc51-76e0d62ed269 /mnt/data
mount /dev/disk/by-id/nvme-ABSNE27512KP_L52751201835-part2 /mnt/backup
```

### Accessing hardware directly:
```bash
cat /dev/urandom | dd of=/dev/nvme0n1 bs=1M  # Wipe NVMe
dd if=/dev/zero of=/tmp/sparse.img bs=1M    # Create sparse file
fuser /dev/nvme0n1p2                         # Find processes using partition
```

### Audio device access:
```bash
speaker-test -D hw:0,0 -t sine              # Test sound card 0, device 0
amixer -c 0 set Master 50%                  # Set volume via control device
```

### Input device monitoring:
```bash
cat /dev/input/event0                        # Raw keyboard events
hexdump -C /dev/input/mouse0                # Raw mouse events
```

---

**Report Generated**: Complete Linux /dev Device File Analysis
**System Type**: x86_64 with AMD GPU, NVMe storage, USB 3.0, audio, TPM 2.0
**Device Count**: 486 files/directories, 200+ character devices
**Symlink Layers**: 5 (by-id, by-uuid, by-path, by-designator, by-diskseq)
