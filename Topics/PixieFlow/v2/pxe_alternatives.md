# PXE Boot Alternatives - Complete List

---

## LEGACY BIOS & UEFI COMPATIBLE BOOTLOADERS

### **Tier 1: Direct PXE Replacements**

1. **GRUB2** (Grand Unified Bootloader 2)
2. **iPXE** (Open-source PXE firmware)
3. **U-Boot** (Universal Bootloader)
4. **Coreboot** + SeaBIOS
5. **EDK2/OVMF** (UEFI reference implementation)
6. **Das U-Boot**
7. **Libreboot** (Coreboot fork)
8. **BIOS Boot Manager**
9. **rEFInd** (UEFI boot manager)
10. **Clover** (UEFI bootloader)

---

## ADVANCED BOOTLOADERS WITH NETWORK SUPPORT

### **Tier 2: Network-Capable Alternatives**

11. **PXELINUX** (Legacy - SYSLINUX variant)
12. **ISOLINUX** (ISO 9660 bootloader)
13. **EXTLINUX** (Unix partition bootloader)
14. **Gummiboot** (Systemd-boot)
15. **systemd-boot** (Modern UEFI bootloader)
16. **ELILO** (Extensible Firmware Interface Linux Loader)
17. **LILO** (Linux Loader - legacy)
18. **LOADLIN** (MS-DOS PXE alternative)
19. **NTLDR** (Windows boot - for legacy hybrid)
20. **bootmgr** (Windows boot manager)

---

## FULL OS DEPLOYMENT PLATFORMS (PXE Alternative)

### **Tier 3: Complete Netboot Solutions**

21. **Kickstart** (RedHat automated installation)
22. **Preseed** (Debian automated installation)
23. **Cloud-init** (Cloud instance initialization)
24. **Cobbler** (Provisioning orchestration)
25. **Foreman** (Infrastructure lifecycle management)
26. **Satellite** (RedHat infrastructure management)
27. **MAAS** (Metal As A Service - Ubuntu)
28. **Ironic** (OpenStack baremetal provisioning)
29. **DBAN** (Darik's Boot and Nuke)
30. **Clonezilla** (Disk cloning)

---

## OPEN SOURCE PROVISIONING FRAMEWORKS

### **Tier 4: Modern Network Boot Systems**

31. **Canonical MAAS**
32. **OpenStack Ironic**
33. **Proxmox VE** (Virtualization + provisioning)
34. **Canonical LXD**
35. **Docker Container Netboot**
36. **Kubernetes Kubelet** (node boot)
37. **LTSP** (Linux Terminal Server Project)
38. **Thin Client OS**
39. **FAI** (Fully Automatic Installation)
40. **Debian Live Boot**

---

## COMMERCIAL/ENTERPRISE SOLUTIONS

### **Tier 5: Enterprise Alternatives**

41. **VMware ESXi Boot**
42. **Hyper-V Network Boot**
43. **Citrix XenServer** (network boot)
44. **Proxmox Bootable Environment**
45. **RHEL Installation ISO** (network boot)
46. **Windows Deployment Services** (WDS)
47. **SCCM** (System Center Configuration Manager)
48. **Dell/HP iDRAC Boot** (OOB bootloader)
49. **Cisco UCS Boot Manager**
50. **IBM Power Systems Boot**

---

## SPECIALIZED/LIGHTWEIGHT BOOTLOADERS

### **Tier 6: Specialized Solutions**

51. **TinyPXE**
52. **Pogo Linux Boot**
53. **Itus/bootloader**
54. **Memtest86** (Memory testing bootloader)
55. **DBAN Bootable** (Secure wipe)
56. **Freedos** (MS-DOS alternative)
57. **Puppy Linux** (Lightweight netboot)
58. **Porteus** (Lightweight modular)
59. **Slitaz** (Very small netboot)
60. **Tiny Core Linux**

---

## FIRMWARE-LEVEL ALTERNATIVES

### **Tier 7: Firmware Replacements**

61. **LinuxBIOS** (Coreboot predecessor)
62. **OpenFirmware** (PowerPC/SPARC)
63. **OpenBoot** (Sun systems)
64. **SLOF** (Slimline Open Firmware)
65. **qemu-bios** (QEMU bootloader)
66. **SeaBIOS** (x86 BIOS implementation)
67. **TianoCore** (UEFI firmware)
68. **UEFI Shell**
69. **edk2-stable** (EDK2 stable release)
70. **AMI BIOS alternative**

---

## HARDWARE-SPECIFIC BOOTLOADERS

### **Tier 8: OEM/Hardware-Specific**

71. **Raspberry Pi bootloader**
72. **NVIDIA Tegra bootloader**
73. **ARM Trusted Firmware**
74. **Qualcomm MSM bootloader**
75. **MediaTek bootloader**
76. **Samsung Exynos bootloader**
77. **Intel UEFI firmware**
78. **AMD AGESA firmware**
79. **ASPEED BMC firmware**
80. **Intel Edison bootloader**

---

## DISKLESS BOOT SOLUTIONS

### **Tier 9: Diskless/Stateless Systems**

81. **LTSP** (Linux Terminal Server Project)
82. **NComputing** (Virtual display)
83. **NovaScale** (VDI thin client)
84. **FSLogix** (Azure virtual desktops)
85. **Stratodesk NoTouch Desktop**
86. **Citrix Virtual Delivery Agent**
87. **VMware Horizon Agent**
88. **Microsoft RDP Boot**
89. **X11 forwarding netboot**
90. **VNC bootable environment**

---

## CONTAINER/CLOUD-NATIVE BOOT

### **Tier 10: Modern Infrastructure**

91. **Kubernetes PXE Plugin**
92. **Docker Custom Init** (custom bootloader)
93. **Ignition** (CoreOS boot configuration)
94. **Butane** (Ignition generator)
95. **Systemd Bootable Container**
96. **LinuxKit** (Minimal Linux container)
97. **Bottlerocket** (AWS container OS)
98. **Talos Linux** (Kubernetes OS)
99. **Flatcar Container Linux**
100. **RancherOS**

---

## LEGACY/HISTORICAL ALTERNATIVES

### **Tier 11: Old System Support**

101. **LILO** (Linux Loader - 1990s)
102. **LOADLIN** (MS-DOS bootloader - 1990s)
103. **SILO** (SPARC boot - 1990s)
104. **QUIK** (PowerPC boot - 1990s)
105. **Yaboot** (PowerPC boot - 2000s)
106. **BootX** (Mac PowerPC - 2000s)
107. **Parisc-Linux bootloader** (HP-UX)
108. **SRM Console** (Alpha systems)
109. **ARCbios** (MIPS systems)
110. **Forth Boot** (IEEE 1275)

---

## COMPARISON BY LEGACY SUPPORT

| Bootloader | BIOS | UEFI | ARM | PPC | SPARC | x86 |
|---|---|---|---|---|---|---|
| GRUB2 | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ |
| iPXE | ✅ | ✅ | ✅ | ✅ | ⚠️ | ✅ |
| U-Boot | ❌ | ⚠️ | ✅ | ✅ | ❌ | ⚠️ |
| systemd-boot | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |
| LILO | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ |
| Yaboot | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ |
| OpenFirmware | ✅ | ⚠️ | ❌ | ✅ | ✅ | ⚠️ |
| Coreboot | ✅ | ✅ | ⚠️ | ✅ | ⚠️ | ✅ |
| LTSP | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

---

## RECOMMENDED ALTERNATIVES BY USE CASE

### **Best Overall Replacement for PXE**
1. **GRUB2** - Universal, modern, both BIOS & UEFI
2. **iPXE** - Enhanced PXE, better features
3. **MAAS** - Full provisioning system
4. **Cobbler** - Enterprise provisioning

### **Best for Legacy Systems**
1. **LILO** - Ancient x86 systems
2. **Yaboot** - PowerPC Macs
3. **OpenFirmware** - SPARC/PowerPC
4. **U-Boot** - Embedded/ARM legacy

### **Best for Modern Systems**
1. **systemd-boot** - UEFI only modern
2. **Ignition/Butane** - Container-native
3. **Cloud-init** - Cloud deployments
4. **Kubernetes native boot**

### **Best for Hybrid (Old + New)**
1. **GRUB2** - Supports both
2. **Coreboot** - Can do both
3. **iPXE** - Flexible architecture
4. **MAAS** - Works on all systems

---

## QUICK SELECTION MATRIX

```
SCENARIO 1: Legacy x86 + Modern UEFI
→ GRUB2 or iPXE

SCENARIO 2: ARM boards (Raspberry Pi, etc.)
→ U-Boot or Das U-Boot

SCENARIO 3: Enterprise provisioning
→ MAAS, Foreman, Cobbler, or Ironic

SCENARIO 4: Diskless thin clients
→ LTSP or Stratodesk

SCENARIO 5: PowerPC Macs
→ Yaboot or OpenFirmware

SCENARIO 6: Cloud/Containers
→ Ignition, Cloud-init, or Talos Linux

SCENARIO 7: Minimal footprint
→ iPXE, TinyPXE, or Memtest86

SCENARIO 8: Hybrid old/new systems
→ GRUB2, Coreboot + SeaBIOS, or LTSP

SCENARIO 9: Windows + Linux
→ Windows Deployment Services (WDS) or SCCM

SCENARIO 10: IoT/Embedded
→ U-Boot or proprietary OEM bootloaders
```

---

## TOP 5 RECOMMENDATIONS FOR YOUR SETUP

If you want **PXE alternative supporting old systems**:

### **#1: GRUB2** (Recommended)
- ✅ Supports BIOS + UEFI
- ✅ Works with legacy x86 + modern systems
- ✅ Built into most Linux distributions
- ✅ Network boot capable
- ✅ Secure boot compatible

### **#2: iPXE** (Enhanced PXE)
- ✅ Better than standard PXE
- ✅ HTTP/HTTPS support (encrypted)
- ✅ Scripting capabilities
- ✅ All architectures
- ✅ Firmware replacement option

### **#3: MAAS** (Full Solution)
- ✅ Complete provisioning platform
- ✅ Manages netboot + configuration
- ✅ Legacy + modern support
- ✅ Enterprise-grade
- ✅ Open source

### **#4: Cobbler** (Configuration)
- ✅ Simplifies PXE/GRUB configuration
- ✅ Multiple distributions
- ✅ Legacy + modern
- ✅ Automation-focused
- ✅ Red Hat ecosystem

### **#5: Coreboot + SeaBIOS** (Firmware Level)
- ✅ Replace firmware entirely
- ✅ Maximum security control
- ✅ All architectures possible
- ✅ Smallest trusted computing base
- ✅ Maximum legacy support
