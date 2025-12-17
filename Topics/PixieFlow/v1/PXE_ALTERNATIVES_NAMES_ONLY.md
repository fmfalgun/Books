# PXE Alternatives - Quick Reference (Names Only)

## CORE BOOTLOADERS (15)

1. **iPXE** - Modern PXE with HTTP/HTTPS
2. **PXELINUX** - Classic BIOS PXE
3. **GRUB2** - Unified BIOS+UEFI bootloader
4. **Syslinux** - Family of lightweight bootloaders
5. **U-Boot** - Embedded systems bootloader
6. **Das U-Boot** - Extended U-Boot
7. **GNU GRUB** - Legacy GRUB version
8. **EXTLINUX** - SYSLINUX for ext filesystems
9. **ISOLINUX** - SYSLINUX for CD/DVD
10. **shim** - UEFI Secure Boot enabler
11. **systemd-boot** - Simple UEFI bootloader
12. **EFISTUB** - Kernel acts as bootloader
13. **rEFInd** - UEFI boot manager
14. **Clover** - UEFI bootloader (macOS/multi-OS)
15. **coreboot** - Open source BIOS replacement

---

## USB/MEDIA BOOT SOLUTIONS (7)

16. **Ventoy** - USB multiboot for BIOS+UEFI
17. **Easy2Boot (E2B)** - USB multiboot manager
18. **UNetbootin** - Universal bootable USB creator
19. **Wimboot** - Windows WIM file bootloader
20. **SeaBIOS** - Open source BIOS with netboot
21. **netboot.xyz** - Simplified iPXE menu system
22. **Serva** - Windows PXE server (DHCP+TFTP)

---

## IMAGING & CLONING TOOLS (6)

23. **Clonezilla** - Disk imaging/cloning
24. **FOG Project** - Full deployment + imaging
25. **Rescuezilla** - Modern Clonezilla fork
26. **Macrium Reflect** - Commercial imaging (both legacy+modern)
27. **Acronis True Image** - Enterprise imaging
28. **Paragon Backup & Recovery** - Commercial backup/imaging

---

## AUTOMATED INSTALLATION (6)

29. **Kickstart** - RedHat/CentOS automation
30. **Preseed** - Debian/Ubuntu automation
31. **FAI** - Fully Automated Installation
32. **cloud-init** - Modern instance provisioning
33. **Ignition** - Container OS provisioning
34. **WDS** - Windows Deployment Services

---

## PROVISIONING PLATFORMS (8)

35. **Cobbler** - Provisioning with Kickstart/Preseed
36. **MAAS** - Ubuntu bare-metal provisioning
37. **Foreman** - Infrastructure provisioning + config management
38. **Razor** - Policy-based bare-metal provisioning
39. **OpenStack Ironic** - Cloud bare-metal service
40. **MDT** - Microsoft Deployment Toolkit
41. **TritonDS** - Container infrastructure platform
42. **Canonical Landscape** - Ubuntu system management

---

## DHCP/TFTP SERVICES (4)

43. **ISC DHCP Server** - Standard DHCP implementation
44. **dnsmasq** - Lightweight DHCP+DNS+PXE
45. **Kea** - Modern ISC DHCP replacement
46. **Tftpd32** - Windows TFTP/DHCP server

---

## BOOT METHODS (Storage-based) (5)

47. **NFS Boot** - Network filesystem root
48. **iSCSI Boot** - Network storage boot
49. **HTTP Boot** - Modern UEFI HTTP boot
50. **HTTPS Boot** - Encrypted HTTP boot
51. **SAN Boot** - Storage area network boot

---

## HYPERVISOR NETBOOT (5)

52. **VirtualBox Network Boot** - VirtualBox VM provisioning
53. **KVM Network Boot** - Linux KVM VM provisioning
54. **Xen Network Boot** - Xen hypervisor netboot
55. **Hyper-V Network Boot** - Microsoft Hyper-V netboot
56. **Proxmox Network Boot** - Proxmox infrastructure provisioning

---

## MODERN OS ALTERNATIVES (6)

57. **Flatcar Linux** - Container-optimized with Ignition
58. **RancherOS** - Container-centric OS (cloud-init)
59. **MicroOS** - Immutable container OS (Ignition)
60. **Kairos** - Immutable Linux for edge/containers
61. **Bottlerocket** - AWS container OS
62. **Talos Linux** - Kubernetes-native minimal OS

---

## QUICK SUMMARY (Most Used)

**Best Overall Alternatives (Most compatible with legacy):**
1. iPXE
2. GRUB2
3. Ventoy
4. Clonezilla
5. FOG Project
6. MAAS
7. Cobbler
8. cloud-init

**Names Only - All 55+ Alternatives:**

iPXE | PXELINUX | GRUB2 | Syslinux | U-Boot | Das U-Boot | GNU GRUB | EXTLINUX | ISOLINUX | shim | systemd-boot | EFISTUB | rEFInd | Clover | coreboot | Ventoy | Easy2Boot | UNetbootin | Wimboot | SeaBIOS | netboot.xyz | Serva | Clonezilla | FOG Project | Rescuezilla | Macrium Reflect | Acronis True Image | Paragon | Kickstart | Preseed | FAI | cloud-init | Ignition | WDS | Cobbler | MAAS | Foreman | Razor | OpenStack Ironic | MDT | TritonDS | ISC DHCP | dnsmasq | Kea | Tftpd32 | NFS Boot | iSCSI Boot | HTTP Boot | HTTPS Boot | SAN Boot | VirtualBox | KVM | Xen | Hyper-V | Proxmox | Flatcar Linux | RancherOS | MicroOS | Kairos | Bottlerocket | Talos Linux

---

## ALTERNATIVES BY CATEGORY

**Legacy BIOS Only:** PXELINUX, ISOLINUX, EXTLINUX, GNU GRUB, SeaBIOS

**UEFI Only:** systemd-boot, EFISTUB, Clover (macOS)

**Both BIOS + UEFI:** iPXE, GRUB2, Ventoy, Easy2Boot, FOG Project, Clonezilla, coreboot, Serva, MAAS, Cobbler

**USB Multiboot:** Ventoy, Easy2Boot, UNetbootin

**Disk Imaging:** Clonezilla, FOG Project, Rescuezilla, Macrium Reflect

**Automation:** Kickstart, Preseed, FAI, cloud-init, Ignition

**Enterprise:** Cobbler, MAAS, Foreman, OpenStack Ironic

**Open Source:** All Linux alternatives except Macrium Reflect, Acronis, Paragon, MDT

**Free:** All except Macrium Reflect, Acronis, Paragon (commercial versions)

---

## TOP 15 MOST RECOMMENDED

1. **iPXE** - Best modern PXE with legacy support
2. **GRUB2** - Unified bootloader
3. **Ventoy** - Easiest USB multiboot
4. **Clonezilla** - Best disk imaging
5. **FOG Project** - Enterprise imaging + provisioning
6. **MAAS** - Cloud infrastructure provisioning
7. **Cobbler** - Enterprise provisioning automation
8. **cloud-init** - Modern instance configuration
9. **Serva** - Lightweight PXE server
10. **dnsmasq** - Minimal DHCP+PXE
11. **Rescuezilla** - Modern cloning alternative
12. **OpenStack Ironic** - Cloud bare-metal
13. **Easy2Boot** - Flexible USB multiboot
14. **coreboot** - Open source firmware
15. **Kickstart** - Linux automation standard

---

## FOR YOUR USE CASE: Legacy System Support with Modern Alternative

**Best Choices:**

**Option 1: Network Boot (PXE Alternative)**
- Use: **iPXE** (best compatibility, legacy + modern)
- Or: **GRUB2** (unified approach)
- Or: **netboot.xyz** (pre-configured iPXE)

**Option 2: USB Boot (Physical Media)**
- Use: **Ventoy** (easiest, supports everything)
- Or: **Easy2Boot** (more control)
- Or: **Clonezilla** (if imaging)

**Option 3: Full Deployment Platform**
- Use: **FOG Project** (imaging + provisioning)
- Or: **MAAS** (modern infrastructure)
- Or: **Cobbler** (enterprise automation)

**Option 4: Simple DHCP+TFTP Server**
- Use: **dnsmasq** (lightweight, simple)
- Or: **Serva** (Windows-based)
- Or: **ISC DHCP + in.tftpd** (standard)

**Recommendation for Legacy System Support:**
→ **iPXE** as bootloader (works with old + new hardware)
→ Combined with **dnsmasq** or **ISC DHCP** as backend
→ **Clonezilla** or **FOG Project** for imaging

