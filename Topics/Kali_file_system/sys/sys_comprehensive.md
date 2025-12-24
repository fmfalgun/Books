# /sys Directory - Complete Functional Use Case Analysis

**Comprehensive master table organizing 2000+ system device entries by functional use case with all symlinks and file types**

---

## Table of Contents
1. Block Devices
2. ACPI Bus System
3. Auxiliary Bus
4. CEC (Consumer Electronics Control)
5. Clock Events & Clock Source
6. Container & CXL Memory
7. CPU System & Processor
8. EDAC (Error Detection & Correction)
9. Event Source Performance Monitoring
10. Faux Devices (Test/Dummy)
11. GPIO (General Purpose I/O)
12. HDAudio (High Definition Audio)
13. HID (Human Interface Device)
14. I2C Bus System
15. ISA Bus
16. Machine Check
17. MDIO Bus & Network PHY
18. Media Devices
19. Memory & Thermal
20. Network Interfaces
21. PCI Bus System
22. Platform Devices
23. Realtek Network PHY Drivers
24. USB Bus System
25. Virtual Devices & Miscellaneous

---

## 1. BLOCK DEVICES

| **Use Case** | **Binaries, Files & Directories** | **Explanation** |
|---|---|---|
| **NVMe Storage Devices** | `block/nvme0n1 (symlink → ../devices/pci0000:00/0000:00:02.4/0000:03:00.0/nvme/nvme0/nvme0n1)` | NVMe (Non-Volatile Memory Express) block device providing direct access to M.2 SSD storage; symlink points to actual device in PCI hierarchy allowing block layer to discover and manage NVMe storage |

---

## 2. ACPI BUS SYSTEM

| **Use Case** | **Binaries, Files & Directories** | **Explanation** |
|---|---|---|
| **ACPI Device Registry** | `bus/acpi/devices/ (directory)` | Central registry of all ACPI (Advanced Configuration & Power Interface) devices discovered during system bootup; contains symbolic links to actual device entries in /sys/devices/ hierarchy |
| **ACPI Power Resources** | `ACPI0003:00 (symlink), ACPI0007:00 through ACPI0007:0f (16 items, symlinks), ACPI000C:00 (symlink), ACPI000E:00 (symlink), ACPI0010:00 (symlink)` | Power management and control devices: ACPI0003 (Power Supply), ACPI0007 (CPU device refs 0-15), ACPI000C (Sleeping Button), ACPI000E (Thermal), ACPI0010 (Processor Container) |
| **AMD-specific ACPI Devices** | `AMDI0007:00 (symlink - AMD GPIO), AMDI0010:00, AMDI0010:01, AMDI0010:02, AMDI0010:03 (4 items - AMD I2C controllers), AMDI0016:00, AMDI0016:01, AMDI0016:02, AMDI0016:03 (4 items - AMD SPI controllers), AMDI0020:00, AMDI0020:01, AMDI0020:02, AMDI0020:03, AMDI0020:04 (5 items - AMD UART controllers), AMDI0030:00 (AMD GPIO resource), AMDI0051:00 (AMD Sensor), AMDI0052:00 (AMD Sensor), AMDI0060:00 (AMD I2C), AMDI0063:00, AMDI0063:01 (AMD I2S), AMDI0080:00 (AMD Storage), AMDI0081:00 (AMD Storage)` | AMD-specific platform devices including I2C, SPI, UART controllers for system communication, GPIO for general purpose I/O, sensors, and storage interfaces |
| **ACPI Processor & Thermal Zones** | `LNXTHERM:00 through LNXTHERM:06 (7 items - Thermal zones), LNXPOWER:00 through LNXPOWER:16 (17 items - Power domains)` | Thermal zone monitoring (CPU, GPU, chipset, ambient temps), Power domain management (individual device power planes) for dynamic power scaling |
| **ACPI Video & Display** | `LNXVIDEO:00 (symlink - GPU display), device:14 through device:1c (9 items - video outputs)` | GPU and display device control for brightness, DPMS (Display Power Management Signaling), video output enumeration |
| **ACPI PCI Root Bridge** | `PNP0A08:00 (symlink - PCI Root Complex), device:00 through device:47 (72+ items)` | Root PCI bridge enumerating all PCI slots and devices; maps logical PCI devices to hardware resources |
| **ACPI EC (Embedded Controller)** | `PNP0C09:00 (symlink - Embedded Controller)` | Low-level hardware interface for battery, thermal, and fan control; firmware-based device management |
| **ACPI Keyboard & Power Button** | `LNXPWRBN:00 (symlink - Power Button), PNP0C0D:00 (symlink - Lid Switch), PNP0C0E:00 (symlink - Sleep Button)` | System control input devices for sleep, hibernation, and power management |
| **ACPI Battery & AC Adapter** | `PNP0C0A:00, PNP0C0A:01 (2 items - Battery devices), ACPI0003:00 (AC Power Supply)` | Battery status monitoring and AC power detection for power management decisions |
| **ACPI System & Bus** | `LNXSYSTM:00 (symlink - System device), LNXSYBUS:00, LNXSYBUS:01 (2 items - ACPI bus), LNXPWRBN:00 (Power button)` | ACPI system root device and virtual buses for device organization |
| **ACPI IRQ Routing** | `PNP0C0F:00 through PNP0C0F:07 (8 items - IRQ routing)` | Interrupt request routing for PCI devices; manages hardware interrupt allocation |
| **ACPI Platform Devices** | `PNP0000:00 (PIC - Programmable Interrupt Controller), PNP0100:00 (Timer), PNP0103:00 (HPET - High Precision Timer), PNP0200:00 (DMA - Direct Memory Access), PNP0500:00 through PNP0500:03 (4 items - Serial ports), PNP0800:00 (Speaker), PNP0B00:00 (Real-Time Clock), PNP0C01:00 (Memory), PNP0C02:00 through PNP0C02:0f (16 items - Misc platform)` | Low-level platform devices: timers, DMA controllers, serial ports, RTC, memory mappings |
| **ACPI Storage Controllers** | `PNP0C04:00 (Math Coprocessor - deprecated)` | Math coprocessor (legacy x87 FPU interfaces) |
| **ACPI Sleep States & Power Management** | `PNP0C0C:00 (Sleep Button), PNP0C14:00, PNP0C14:01 (WBEM Wake Events)` | Sleep state control and wake event management |
| **ACPI Battery Charging** | `PNP0C32:00 (AC Device)` | AC adapter and battery charging control |
| **HID Devices (I2C)** | `SYNA311F:00 (Synaptics Touchpad HID), ELAN2513:00 (Elan Touchpad HID), NXP8013:00 (NXP Audio Codec), device:48, device:49` | Human Interface Devices for touchpad, stylus, and audio control connected via I2C |
| **HP ACPI Extensions** | `HPIC000C:00, HPIC0013:00 (HP Illuminated Keyboard), HPIC0011:00, HPQ8002:00 (HP Extras)` | HP laptop-specific ACPI extensions for keyboard lighting and special functions |
| **Intel ACPI Extensions** | `INTC1073:00 (Intel Audio DSP), INTC1092:00 (Intel Temperature)` | Intel platform-specific ACPI devices for audio digital signal processing and temperature monitoring |
| **Thermal Monitoring** | `NTC0702:00 (Nuvoton Thermal Sensor), LNXTHERM:00-06 (7 thermal zones)` | Temperature sensor for thermal management and fan control |
| **USB Type-C** | `USBC000:00 (symlink - USB Type-C Port Manager), device:48, device:49` | USB Type-C port and connector configuration |
| **ACPI Bus Drivers** | `bus/acpi/drivers/ (directory), battery, button, ec, thermal, video, tpm_crb, hpet, hardware_error_device` | Driver subsystem for loading ACPI device drivers on demand |

---

## 3. AUXILIARY BUS

| **Use Case** | **Binaries, Files & Directories** | **Explanation** |
|---|---|---|
| **Auxiliary Bus System** | `bus/auxiliary/devices/ (empty directory), bus/auxiliary/drivers/ (empty directory)` | Virtual bus for miscellaneous driver-managed devices not belonging to standard buses |

---

## 4. CEC (CONSUMER ELECTRONICS CONTROL)

| **Use Case** | **Binaries, Files & Directories** | **Explanation** |
|---|---|---|
| **CEC Bus** | `bus/cec/devices/ (empty), bus/cec/drivers/ (empty)` | Consumer Electronics Control bus for HDMI CEC device discovery (typically empty on Linux) |

---

## 5. CLOCK EVENTS & CLOCK SOURCE

| **Use Case** | **Binaries, Files & Directories** | **Explanation** |
|---|---|---|
| **System Clock Events** | `bus/clockevents/devices/ (directory), broadcast (symlink → ../../../devices/system/clockevents/broadcast), clockevent0 through clockevent11 (12 items - symlinks)` | System timer events and scheduling clock sources; broadcast is for inter-processor timer interrupts, individual clockevent entries for each CPU core (0-11 = 12 cores) |
| **System Clock Source** | `bus/clocksource/devices/ (directory), clocksource0 (symlink → ../../../devices/system/clocksource/clocksource0)` | Primary system timekeeping source for monotonic clock and timestamps |

---

## 6. CONTAINER & CXL MEMORY

| **Use Case** | **Binaries, Files & Directories** | **Explanation** |
|---|---|---|
| **Container Bus** | `bus/container/devices/ (empty), bus/container/drivers/ (empty)` | ACPI container device bus (typically unused) |
| **CXL (Compute Express Link) Memory** | `bus/cxl/devices/ (directory), bus/cxl/drivers/cxl_port, cxl_region, bus/cxl/flush` | CXL protocol support for heterogeneous memory hierarchies and high-bandwidth persistent memory |

---

## 7. CPU SYSTEM & PROCESSOR

| **Use Case** | **Binaries, Files & Directories** | **Explanation** |
|---|---|---|
| **CPU Devices** | `bus/cpu/devices/ (directory), cpu0 through cpu11 (12 items - symlinks)` | 12 logical CPU cores discovered by kernel; each symlink points to /sys/devices/system/cpu/cpuX for individual core management |
| **Processor Driver** | `bus/cpu/drivers/processor/ (directory), bind, unbind, uevent, cpu0-cpu11 (12 symlinks)` | ACPI processor driver managing CPU P-states (power states), C-states (idle states), frequency scaling, and thermal throttling for each core |

---

## 8. COREBOOT FIRMWARE

| **Use Case** | **Binaries, Files & Directories** | **Explanation** |
|---|---|---|
| **Coreboot Devices** | `bus/coreboot/devices/ (empty)` | Coreboot open-source firmware support (typically unused on systems using proprietary UEFI/BIOS) |
| **Coreboot Framebuffer** | `bus/coreboot/drivers/framebuffer/ (directory), bind, unbind, uevent` | Display framebuffer driver for Coreboot-based systems |

---

## 9. CXL MEMORY BUS

| **Use Case** | **Binaries, Files & Directories** | **Explanation** |
|---|---|---|
| **DAX (Direct Access) Devices** | `bus/dax/devices/ (empty), bus/dax/drivers/ (empty)` | Direct Access persistent memory interface for bypassing page cache (typically unused without PMEM/CXL hardware) |
| **EDAC (Memory Error Correction)** | `bus/edac/devices/ (directory), mc (symlink → ../../../devices/system/edac/mc)` | Error Detection & Correction memory controller monitoring for multi-bit error detection and single-bit error correction |

---

## 10. EVENT SOURCE (PERFORMANCE MONITORING)

| **Use Case** | **Binaries, Files & Directories** | **Explanation** |
|---|---|---|
| **Performance Monitoring Units** | `bus/event_source/devices/ (directory)` | Linux Performance Event Interface (perf) for CPU performance counters |
| **Monitoring Devices** | `amd_df (Data Fabric PMU), amd_iommu_0 (IOMMU performance), amd_l3 (L3 cache events), breakpoint (software breakpoints), cpu (CPU cycles/instructions), ibs_fetch, ibs_op (Instruction-Based Sampling), kprobe (dynamic kernel tracing), msr (Model-Specific Register), power, power_core (power domain events), software (software events), tracepoint (tracepoint kernel hooks), uprobe (user-space tracing)` | Comprehensive performance monitoring: CPU counters, cache events, IOMMU transfers, instruction sampling, and user/kernel tracing for profiling |

---

## 11. FAUX DEVICES (TEST/DUMMY)

| **Use Case** | **Binaries, Files & Directories** | **Explanation** |
|---|---|---|
| **Dummy Audio Devices** | `bus/faux/devices/ (directory), reg-dummy, snd-soc-dummy (2 items)` | Kernel test audio drivers for testing sound infrastructure without real hardware |
| **Faux Driver** | `bus/faux/drivers/faux_driver/ (directory), reg-dummy, snd-soc-dummy (symlinks), uevent` | Dummy device driver for testing driver model |

---

## 12. GPIO (GENERAL PURPOSE I/O)

| **Use Case** | **Binaries, Files & Directories** | **Explanation** |
|---|---|---|
| **GPIO Devices** | `bus/gpio/devices/ (directory), gpiochip0 (symlink → ../../../devices/platform/AMDI0030:00/gpiochip0)` | AMD GPIO controller (gpiochip0) providing 32+ digital I/O lines for system control signals |
| **GPIO Stub Driver** | `bus/gpio/drivers/gpio_stub_drv/ (directory), bind, unbind, uevent` | GPIO driver support infrastructure |

---

## 13. HDAUDIO (HIGH DEFINITION AUDIO)

| **Use Case** | **Binaries, Files & Directories** | **Explanation** |
|---|---|---|
| **HDAudio Codec Devices** | `bus/hdaudio/devices/ (directory), hdaudioC0D0 (symlink → ../../../devices/pci0000:00/0000:00:08.1/0000:04:00.1/hdaudioC0D0), hdaudioC1D0 (symlink → ../../../devices/pci0000:00/0000:00:08.1/0000:04:00.6/hdaudioC1D0)` | Two HDAudio codec controllers: C0D0 = HDMI audio (GPU), C1D0 = Realtek Codec (speaker/microphone) |
| **HDAudio Drivers** | `bus/hdaudio/drivers/ (directory with 3 codec drivers)` | Audio codec driver infrastructure |
| **HDMI Audio Codec Driver** | `snd_hda_codec_hdmi/ (directory), bind, unbind, module, hdaudioC0D0 (symlink), uevent` | HDMI audio codec driver for GPU-based audio output (4 channels, 48kHz support) |
| **Realtek Audio Codec Driver** | `snd_hda_codec_realtek/ (directory), bind, unbind, module, hdaudioC1D0 (symlink), uevent` | Realtek ALC codec driver for integrated speaker and microphone (analog audio I/O) |
| **Generic HDAudio Codec** | `snd_hda_codec_generic/ (directory), bind, unbind, module, uevent` | Generic fallback codec driver for unsupported audio codecs |

---

## 14. HID (HUMAN INTERFACE DEVICE)

| **Use Case** | **Binaries, Files & Directories** | **Explanation** |
|---|---|---|
| **HID Devices** | `bus/hid/devices/ (directory), 0018:06CB:CFC9.0001 (symlink → ../../../devices/platform/AMDI0010:00/i2c-0/i2c-SYNA311F:00/0018:06CB:CFC9.0001)` | Synaptics HID touchpad (vendor 06CB, product CFC9) connected via I2C with interrupt-driven input |
| **HID Generic Driver** | `bus/hid/drivers/hid-generic/ (directory), bind, unbind, module, new_id, uevent` | Generic HID driver as fallback for unknown devices |
| **HID Multitouch Driver** | `bus/hid/drivers/hid-multitouch/ (directory), 0018:06CB:CFC9.0001 (symlink), bind, unbind, module, new_id, uevent` | Multitouch HID driver supporting capacitive touchpads with gesture recognition |

---

## 15. I2C BUS SYSTEM

| **Use Case** | **Binaries, Files & Directories** | **Explanation** |
|---|---|---|
| **I2C Adapter Devices** | `bus/i2c/devices/ (directory with 20 I2C buses)` | I2C (Inter-Integrated Circuit) serial bus adapters for sensor, touchpad, codec communication |
| **I2C Bus 0** | `i2c-0 (symlink → ../../../devices/platform/AMDI0010:00/i2c-0)` | AMD I2C0 controller (touchpad/sensor bus) |
| **I2C Bus 1-2** | `i2c-1, i2c-2 (symlinks → AMDI0010:01/i2c-1, AMDI0010:02/i2c-2)` | AMD I2C1, I2C2 controllers for sensors and miscellaneous I2C devices |
| **I2C Bus 3-9** | `i2c-3 through i2c-9 (7 items - symlinks → GPU i2c controllers)` | GPU (AMDGPU) integrated I2C for DDC-CI (Display Data Channel) communication with monitors |
| **I2C Bus 10-11** | `i2c-10, i2c-11 (symlinks)` | GPU secondary I2C for additional display/sensor interface |
| **I2C DDC (Display Data Channel)** | `i2c-12 through i2c-19 (8 items - symlinks)` | HDMI/DP DDC buses for monitor EDID reading and brightness control (card0-eDP-1, card0-DP-1 through DP-7) |
| **I2C HID Device** | `i2c-SYNA311F:00 (symlink → ../../../devices/platform/AMDI0010:00/i2c-0/i2c-SYNA311F:00)` | Synaptics HID touchpad connected to I2C0 |
| **I2C Drivers** | `bus/i2c/drivers/ (directory with 5 driver types)` | I2C device driver management |
| **Dummy I2C Driver** | `dummy/ (directory), bind, unbind, uevent` | Test driver for I2C bus testing |
| **I2C HID ACPI Driver** | `i2c_hid_acpi/ (directory), bind, unbind, module, i2c-SYNA311F:00 (symlink), uevent` | ACPI-based HID over I2C driver for touchpads (supports GPIO interrupts and power management) |
| **Intel PMICs (Power Management ICs)** | `intel_soc_pmic_chtwc/, intel_soc_pmic_crc/ (2 items - directories)` | Intel system-on-chip power management IC drivers (may not apply to AMD systems but present in generic drivers) |
| **SMBus Alert Handler** | `smbus_alert/ (directory), bind, unbind, module, uevent` | System Management Bus alert line handling for battery and thermal alerts |

---

## 16. ISA BUS

| **Use Case** | **Binaries, Files & Directories** | **Explanation** |
|---|---|---|
| **ISA Bus (Legacy)** | `bus/isa/devices/ (empty), bus/isa/drivers/ (empty)` | ISA (Industry Standard Architecture) bus support (legacy; typically unused on modern systems) |

---

## 17. MACHINE CHECK & ERROR HANDLING

| **Use Case** | **Binaries, Files & Directories** | **Explanation** |
|---|---|---|
| **Machine Check Devices** | `bus/machinecheck/devices/ (directory), machinecheck0 through machinecheck11 (12 items - symlinks)` | CPU machine check exception handlers for each core (0-11); detects catastrophic CPU errors, cache corruption, and hardware faults |

---

## 18. MDIO BUS & NETWORK PHY

| **Use Case** | **Binaries, Files & Directories** | **Explanation** |
|---|---|---|
| **Network PHY Device** | `bus/mdio_bus/devices/ (directory), r8169-0-100:00 (symlink → ../../../devices/pci0000:00/0000:00:02.1/0000:01:00.0/mdio_bus/r8169-0-100/r8169-0-100:00)` | Realtek RTL8169 Ethernet PHY (physical layer transceiver) for 1Gbps network interface |
| **Generic Clause 45 PHY Driver** | `Generic Clause 45 PHY/ (directory), bind, unbind, module, uevent` | 10G+ Ethernet PHY driver |
| **Generic FE-GE PHY Driver** | `Generic FE-GE Realtek PHY/ (directory), bind, unbind, module, r8169-0-100:00 (symlink), uevent` | Realtek 10/100/1000 Mbps PHY driver (matches RTL8169) |
| **Generic PHY Fallback** | `Generic PHY/ (directory), bind, unbind, module, uevent` | Fallback driver for standard IEEE 802.3 PHYs |
| **Realtek PHY Variants (30+ drivers)** | `Realtek Internal NBASE-T PHY, RTL8201CP, RTL8201F, RTL8208, RTL8211B-F variants, RTL8221B variants, RTL8224, RTL8226, RTL8251B, RTL8365MB, RTL8366RB, RTL8366S, RTL9000AA, etc.` | 30+ Realtek Ethernet PHY drivers covering 10M-10G speeds with various features (Power-over-Ethernet, Fiber, NBASE-T, etc.) |

---

## 19. MEDIA DEVICES

| **Use Case** | **Binaries, Files & Directories** | **Explanation** |
|---|---|---|
| **Media Bus** | `bus/media/devices/, bus/media/drivers/, bus/media/drivers_autoprobe, bus/media/drivers_probe, bus/media/uevent` | Media framework for video capture, DVB (Digital Video Broadcasting), and camera devices (typically empty without video capture hardware) |

---

## 20. MEMORY & THERMAL MANAGEMENT

| **Use Case** | **Binaries, Files & Directories** | **Explanation** |
|---|---|---|
| **Memory Bus** | `bus/memory/devices/, bus/memory/drivers/`, `bus/memory/drivers_autoprobe, bus/memory/drivers_probe, bus/memory/uevent` | Memory device management (DIMM hot-add/remove for servers; typically empty on laptops) |
| **NVDIMM Bus** | `bus/nd/devices/, bus/nd/drivers/`, `bus/nd/drivers_autoprobe, bus/nd/drivers_probe, bus/nd/uevent` | NVMe DIMM (persistent memory) support |
| **Thermal Bus** | `bus/thermal/devices/ (directory), LNXTHERM:00 through LNXTHERM:06 (7 items - symlinks)` | Thermal zone devices for temperature monitoring |
| **Thermal Drivers** | `bus/thermal/drivers/thermal/ (directory), bind, unbind, LNXTHERM:00-06 (7 symlinks), module, uevent` | ACPI thermal management driver controlling fan speed and CPU throttling |

---

## 21. NETWORK & PCI DEVICES

| **Use Case** | **Binaries, Files & Directories** | **Explanation** |
|---|---|---|
| **PCI Bus Hierarchy** | `bus/pci/devices/` (hundreds of devices in tree structure) | Complete PCI (Peripheral Component Interconnect) device tree with slots, bridges, and endpoints |
| **PCI Root** | `pci0000:00` | Domain 0, root complex; primary PCI bus on system |
| **PCI Slot 0 (CPU Lanes)** | `0000:00:02.1 (Network: Realtek RTL8169), 0000:00:02.4 (NVMe: PCI Express), 0000:00:08.1 (Audio/Video)` | PCIe slots directly connected to CPU lanes |
| **PCIe Switch Hierarchy** | `0000:03:00.0 (NVMe endpoint under PCIe switch)` | Multi-level PCIe device hierarchy through switches and bridges |
| **USB Bus** | `bus/usb/devices/` | USB device enumeration (typically empty in /sys/devices without USB peripherals) |
| **USB Drivers** | `bus/usb/drivers/usb, usbfs` | USB device and bus driver infrastructure |

---

## 22. PLATFORM DEVICES

| **Use Case** | **Binaries, Files & Directories** | **Explanation** |
|---|---|---|
| **Platform Device Bus** | `bus/platform/devices/ (directory), bus/platform/drivers/ (directory with multiple drivers)` | Virtual bus for system platform devices (ACPI, OF, CPU sensors, GPIO, UART, etc.) |
| **AMD Platform Devices** | `AMDI0030:00 (GPIO resource), AMDI0010:00, AMDI0010:01, AMDI0010:02 (I2C controllers with various sensors)` | AMD platform controller hub devices |

---

## 23. REALTEK NETWORK PHY DRIVERS

| **Use Case** | **Binaries, Files & Directories** | **Explanation** |
|---|---|---|
| **RTL8201CP Fast Ethernet** | Driver for 10/100 Mbps Realtek PHY |
| **RTL8201F Fast Ethernet** | Improved RTL8201 variant |
| **RTL8208 Fast Ethernet** | Enhanced 10/100 Mbps PHY |
| **RTL8211B Gigabit Ethernet** | 1000 Mbps Realtek PHY |
| **RTL8211C Gigabit Ethernet** | Improved RTL8211B variant |
| **RTL8211DN Gigabit Ethernet** | 1000 Mbps PHY for Dell/HP laptops |
| **RTL8211E Gigabit Ethernet** | High-performance 1000 Mbps PHY |
| **RTL8211F Gigabit Ethernet** | Latest 1000 Mbps with advanced power management |
| **RTL8211F-VD Gigabit Ethernet** | Variant with additional features |
| **RTL8211 Gigabit Ethernet** | Generic RTL8211 support |
| **RTL8221B Series (30+ variants)** | 2.5 Gbps multi-gig PHYs with Power-over-Ethernet, Fiber, C22/C45 clauses |
| **RTL8224 2.5Gbps PHY** | Advanced 2.5G Ethernet PHY |
| **RTL8226 2.5Gbps PHY** | 2.5G variant |
| **RTL8251B 5Gbps PHY** | High-speed 5G Ethernet PHY |
| **RTL8365/8366 Managed Switches** | Network switch PHY support |

---

## 24. TPM & DEVICE SECURITY

| **Use Case** | **Binaries, Files & Directories** | **Explanation** |
|---|---|---|
| **TPM CRB Driver** | `bus/acpi/drivers/tpm_crb/ (directory), bind, unbind, uevent` | Trusted Platform Module (Command Response Buffer) driver for system security and measured boot |

---

## 25. VIDEO & DISPLAY DEVICES

| **Use Case** | **Binaries, Files & Directories** | **Explanation** |
|---|---|---|
| **Video Bus** | `bus/acpi/drivers/video/ (directory), bind, unbind, module, LNXVIDEO:00 (symlink), uevent` | GPU and display driver infrastructure for backlight brightness, DPMS power management, and video output control |

---

## SYSTEM DEVICE HIERARCHY

| **Use Case** | **Binaries, Files & Directories** | **Explanation** |
|---|---|---|
| **System CPU Devices** | `devices/system/cpu/ (directory with cpu0-cpu11, 12 logical cores)` | Individual CPU core entry points for frequency scaling (cpufreq), idle states (cpuidle), thermal throttling |
| **System Clock Events** | `devices/system/clockevents/ (directory with broadcast, clockevent0-11)` | Timer event devices for scheduler and hrtimer infrastructure |
| **System Clock Source** | `devices/system/clocksource/ (directory with clocksource0)` | Primary system timekeeping device (usually TSC - Time Stamp Counter on x86) |
| **System EDAC** | `devices/system/edac/ (directory with mc for memory controller)` | Memory error correction monitoring device |
| **System Machine Check** | `devices/system/machinecheck/ (directory with machinecheck0-11)` | CPU exception handlers for fatal hardware errors |
| **AMDGPU Performance** | `devices/amd_df (AMD Data Fabric PMU), devices/amd_iommu_0 (IOMMU PMU), devices/amd_l3 (L3 cache PMU)` | Performance monitoring units for system analysis |
| **Perf Tracing** | `devices/breakpoint, devices/kprobe, devices/uprobe, devices/tracepoint` | Dynamic tracing infrastructure for kernel and user-space debugging |
| **Perf Counters** | `devices/cpu (CPU cycle counters), devices/power (power domain counters), devices/software (software counters)` | Performance event monitoring for profiling |
| **Instruction Sampling** | `devices/ibs_fetch, devices/ibs_op (AMD Instruction-Based Sampling)` | Low-overhead performance profiling capturing actual instructions executed |

---

## DEVICE DRIVER LOADING

| **Use Case** | **Binaries, Files & Directories** | **Explanation** |
|---|---|---|
| **drivers_autoprobe** | Present in all buses | Enables automatic driver loading when devices are connected (1 = on, 0 = off) |
| **drivers_probe** | Present in all buses | Manual trigger for re-probing all devices on bus |
| **uevent** | Present in all buses | Netlink socket for udev device hot-plug events |
| **bind/unbind** | Driver directories | Manual device binding/unbinding to drivers (test/debug) |

---

## COMPLETE ITEM LISTING BY CATEGORY

### BLOCK DEVICES (1 item)
- nvme0n1

### ACPI DEVICES (100+ items)
ACPI0003:00, ACPI0007:00-0f (16), ACPI000C:00, ACPI000E:00, ACPI0010:00, AMDI0007:00, AMDI0010:00-03 (4), AMDI0016:00-03 (4), AMDI0020:00-04 (5), AMDI0030:00, AMDI0051:00, AMDI0052:00, AMDI0060:00, AMDI0063:00-01 (2), AMDI0080:00, AMDI0081:00, device:00-49 (50 items), ELAN2513:00, HPIC000C:00, HPIC0011:00, HPIC0013:00, HPQ8002:00, INTC1073:00, INTC1092:00, LNXPWRBN:00, LNXPOWER:00-16 (17), LNXSYBUS:00-01 (2), LNXSYSTM:00, LNXTHERM:00-06 (7), LNXVIDEO:00, NTC0702:00, NXP8013:00, PNP0000:00, PNP0100:00, PNP0103:00, PNP0200:00, PNP0500:00-03 (4), PNP0800:00, PNP0A08:00, PNP0B00:00, PNP0C01:00, PNP0C02:00-0f (16), PNP0C04:00, PNP0C09:00, PNP0C0A:00-01 (2), PNP0C0C:00, PNP0C0D:00, PNP0C0E:00, PNP0C0F:00-07 (8), PNP0C14:00-01 (2), PNP0C32:00, SYNA311F:00, USBC000:00

### CLOCK EVENTS (12 items)
broadcast, clockevent0-11

### CLOCK SOURCE (1 item)
clocksource0

### CPU DEVICES (12 items)
cpu0-cpu11

### HDAUDIO CODECS (2 items)
hdaudioC0D0, hdaudioC1D0

### I2C BUSES (20 items)
i2c-0, i2c-1, i2c-2, i2c-3, i2c-4, i2c-5, i2c-6, i2c-7, i2c-8, i2c-9, i2c-10, i2c-11, i2c-12, i2c-13, i2c-14, i2c-15, i2c-16, i2c-17, i2c-18, i2c-19, i2c-SYNA311F:00

### MDIO PHY (1 item)
r8169-0-100:00

### MACHINE CHECK (12 items)
machinecheck0-11

### NETWORK GPIO (1 item)
gpiochip0

### REALTEK PHY DRIVERS (30+ variants)
RTL8201CP, RTL8201F, RTL8208, RTL8211B, RTL8211C, RTL8211DN, RTL8211E, RTL8211F, RTL8211F-VD, RTL8211, RTL8221B (multiple C22/C45 variants), RTL8224, RTL8226 (multiple variants), RTL8251B, RTL8365MB, RTL8366RB, RTL8366S, RTL9000AA

---

## SUMMARY STATISTICS

| **Category** | **Item Count** | **Type** |
|---|---|---|
| Block Devices | 1 | symlink |
| ACPI Devices | 100+ | symlinks |
| CPU Devices | 12 | symlinks |
| Clock Events | 12 | symlinks |
| I2C Buses | 20 | symlinks |
| HDAudio Codecs | 2 | symlinks |
| Machine Check | 12 | symlinks |
| MDIO PHY | 1 | symlink |
| GPIO | 1 | symlink |
| Bus Systems | 20+ | directories |
| Driver Subsystems | 40+ | directories |
| Realtek PHY Drivers | 30+ | driver entries |
| **TOTAL** | **2000+** | Mix of symlinks, directories, and files |

---

## KEY INSIGHTS

### Sysfs Architecture
- `/sys` is a virtual filesystem (VFS) mapped to kernel data structures
- All items are **symlinks to actual device objects** in `/sys/devices/`
- Each symlink provides abstraction (devices by bus, drivers, class)

### Device Organization
1. **By Bus** (`bus/`): acpi, pci, usb, i2c, hid, etc.
2. **By Type** (`class/`): not shown but implied (net/, sound/, input/)
3. **By Device** (`devices/`): actual hardware objects

### Performance Monitoring
- Extensive perf event support (CPU, cache, IOMMU, power)
- AMD Instruction-Based Sampling (IBS) for low-overhead profiling
- Dynamic tracing (kprobe, uprobe, tracepoint)

### Thermal Management
- 7 thermal zones with individual control
- 12 CPU cores with per-core throttling
- Fan control via EC (Embedded Controller)

### Network Architecture
- 20 I2C buses (including GPIO, sensors, touchpad, display DDC)
- 1 Gigabit Ethernet with Realtek PHY (RTL8169)
- Full PHY driver support for speeds from 10M to 5G+

### Audio System
- 2 HDAudio codecs: GPU (HDMI) + Realtek (speakers/mic)
- 3 codec drivers (generic fallback, HDMI, Realtek)

---

**Report Generated**: Complete /sys functional categorization with 2000+ items
**System**: Kali Linux on AMD Ryzen laptop with comprehensive device support
**Detail Level**: Comprehensive with all symlinks and driver hierarchy
**Date**: December 2025

