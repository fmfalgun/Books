# PXE Alternatives: Complete List of Netboot Technologies

## PRIMARY ALTERNATIVES TO PXE (Names Only)

### **1. iPXE**
- Modern PXE implementation with HTTP/HTTPS support
- Enhanced scripting capabilities
- Backward compatible with legacy systems

### **2. PXELINUX**
- Core bootloader component of Syslinux family
- Classic PXE boot over TFTP
- Supports BIOS systems

### **3. GRUB2**
- GNU GRand Unified Bootloader
- Supports both BIOS and UEFI
- Can boot over network via HTTP/TFTP

### **4. Syslinux**
- Family of bootloaders (PXELINUX, ISOLINUX, EXTLINUX)
- Lightweight and flexible
- BIOS-focused

### **5. Ventoy**
- Multi-boot USB solution
- Supports both Legacy BIOS and UEFI
- Drop-and-boot (no extraction needed)

### **6. Easy2Boot (E2B)**
- USB multiboot manager
- Legacy BIOS and UEFI support
- Uses grub4dos, grubfm, Ventoy internally

### **7. UNetbootin**
- Universal netboot installer
- Creates bootable USB drives
- Supports many Linux distributions

### **8. Clonezilla**
- Disk imaging and cloning
- Live bootable environment
- Supports both BIOS and UEFI

### **9. FOG Project**
- Full imaging and deployment suite
- Web-based management interface
- Network-based OS cloning
- Alternative to commercial imaging solutions

### **10. Rescuezilla**
- Disk cloning and imaging tool
- Modern Clonezilla derivative
- BIOS and UEFI compatible
- Free and open-source

### **11. Macrium Reflect**
- Commercial disk cloning solution
- Supports legacy and modern systems
- Comprehensive imaging capabilities

### **12. Acronis True Image**
- Enterprise imaging and backup
- Cross-platform support
- Commercial solution

### **13. Paragon Backup & Recovery**
- Comprehensive backup and recovery
- Legacy system support
- Commercial tool

### **14. netboot.xyz**
- Simplified PXE boot menu system
- Uses iPXE underneath
- Pre-configured for many OSes

### **15. U-Boot**
- Embedded systems bootloader
- Network boot capability
- Used in ARM-based and embedded systems
- Supports PXE-like network boot protocols

### **16. Das U-Boot**
- Extended U-Boot variant
- Better network boot support
- Embedded systems and IoT

### **17. GNU GRUB**
- GRUB (without "2")
- Legacy version
- BIOS systems only
- Minimal network support

### **18. EXTLINUX**
- Extension of SYSLINUX
- Install to ext2/3/4 filesystems
- Simpler than PXELINUX

### **19. ISOLINUX**
- Syslinux variant for CD/DVD
- Can be used with boot-from-USB
- Supports hybrid MBR

### **20. Wimboot**
- Specialized bootloader for Windows WIM files
- Works with iPXE
- Direct WIM boot capability

### **21. shim**
- UEFI bootloader shim
- Enables Secure Boot on Linux
- Bridges UEFI and GRUB

### **22. systemd-boot**
- Simple UEFI bootloader
- Minimal design
- Modern UEFI systems

### **23. EFISTUB**
- Kernel acts as bootloader
- Direct UEFI boot
- Requires UEFI firmware
- No separate bootloader needed

### **24. rEFInd**
- UEFI boot manager
- GUI-based bootloader selection
- Cross-platform (Mac, Linux, Windows)

### **25. Clover**
- UEFI bootloader (primarily for macOS)
- Can boot Linux/Windows via UEFI
- Substitute UEFI BIOS capability

### **26. SeaBIOS**
- Open source BIOS implementation
- Network boot support via DHCP/TFTP
- Used in QEMU and other hypervisors

### **27. coreboot**
- Open source firmware/BIOS replacement
- Supports network boot
- Minimal, lightweight bootloader

### **28. Serva**
- Windows-based PXE server
- Lightweight (~4MB)
- Supports DHCP and TFTP
- Both UEFI and BIOS compatible

### **29. Tftpd32**
- Windows DHCP and TFTP server
- Lightweight PXE server solution
- Legacy and modern system support

### **30. Kickstart**
- Red Hat/CentOS automated installation
- Works with PXE (uses PXE for initial boot)
- Unattended OS deployment

### **31. Preseed**
- Debian/Ubuntu automated installation
- Works with PXE
- Unattended OS deployment

### **32. cloud-init**
- Instance initialization/provisioning
- Works with PXE and other boot methods
- Modern approach to system configuration

### **33. FAI (Fully Automated Installation)**
- Debian-based automated system installation
- Uses PXE but provides full automation
- Enterprise deployment tool

### **34. Cobbler**
- Provisioning and OS deployment
- Builds on Kickstart/Preseed
- Web-based management

### **35. MAAS (Metal as a Service)**
- Ubuntu's bare-metal provisioning
- Uses iPXE and network boot
- Cloud-like infrastructure

### **36. Razor**
- Bare-metal provisioning system
- Policy-based deployment
- Uses PXE with custom logic

### **37. Foreman**
- Infrastructure provisioning platform
- Integrates with Kickstart/Preseed
- PXE + configuration management

### **38. ISC DHCP Server**
- Reference DHCP implementation
- Can serve PXE boot configurations
- Standard in enterprise environments

### **39. dnsmasq**
- Lightweight DHCP and DNS server
- Built-in PXE boot support
- Simpler alternative to full ISC DHCP

### **40. Kea**
- Modern DHCP server from ISC
- Enhanced PXE support
- Next-generation alternative to ISC DHCP

### **41. NFS Boot**
- Network-based root filesystem
- Not a bootloader, but boot method
- Works with PXE for initial kernel load

### **42. iSCSI Boot**
- Network storage boot method
- Works with PXE as initial loader
- Enterprise storage solution

### **43. HTTP Boot**
- Modern UEFI HTTP boot capability
- Does not require TFTP
- Faster, more secure than TFTP

### **44. HTTPS Boot**
- Encrypted HTTP boot
- Modern secure alternative to PXE
- Requires UEFI firmware support

### **45. VirtualBox Network Boot**
- Hypervisor network boot capability
- Uses DHCP/TFTP internally
- For virtual machine deployment

### **46. KVM Network Boot**
- Linux KVM hypervisor network boot
- DHCP/TFTP support
- Virtual machine provisioning

### **47. Xen Network Boot**
- Xen hypervisor network boot
- PXE compatibility
- Virtual infrastructure

### **48. Hyper-V Network Boot**
- Microsoft Hyper-V network boot
- Uses DHCP/TFTP
- Windows-centric VM provisioning

### **49. Proxmox Network Boot**
- Proxmox hypervisor network boot
- PXE-based provisioning
- Virtual machine deployment

### **50. OpenStack Ironic**
- Bare-metal provisioning service
- Part of OpenStack
- Uses PXE + custom logic

### **51. TritonDS (formerly Joyent)**
- Container infrastructure platform
- Network-based provisioning
- Modern cloud approach

### **52. Flatcar Linux**
- Container-optimized OS
- Ignition-based provisioning
- Alternative to PXE-based deployment

### **53. RancherOS**
- Container-centric OS
- Cloud-init provisioning
- Alternative to traditional netboot

### **54. MicroOS**
- Immutable container OS
- Alternative provisioning model
- Modern approach to OS deployment

### **55. Kairos**
- Immutable Linux distribution
- Alternative to traditional netboot
- Container-focused OS

---

## SUMMARY CATEGORIES

### **Pure Bootloaders**
- iPXE, PXELINUX, GRUB2, Syslinux, U-Boot, Das U-Boot
- shim, systemd-boot, EFISTUB, rEFInd, Clover

### **BIOS/Legacy Only**
- PXELINUX, ISOLINUX, EXTLINUX, SeaBIOS
- Vintage bootloaders

### **UEFI Only**
- systemd-boot, EFISTUB, Clover (macOS), rEFInd

### **Both BIOS + UEFI**
- iPXE, GRUB2, Syslinux family, Ventoy, Easy2Boot, Serva, coreboot

### **Imaging/Cloning Tools**
- Clonezilla, FOG Project, Rescuezilla
- Macrium Reflect, Acronis True Image, Paragon

### **Provisioning/Automation**
- Kickstart, Preseed, cloud-init, FAI
- Cobbler, MAAS, Foreman, Kea

### **Deployment Platforms**
- OpenStack Ironic, TritonDS, MAAS
- Razor, Cobbler, Foreman

### **Modern/Cloud Alternatives**
- cloud-init, Ignition, Flatcar Linux, Kairos
- Container-based OS deployment

### **Windows-Specific**
- wimboot, Windows PE, WDS (Windows Deployment Services)
- MDT (Microsoft Deployment Toolkit)

### **Linux-Specific**
- Kickstart, Preseed, FAI, cloud-init
- Dracut, mkinitcpio

### **USB Multiboot Solutions**
- Ventoy, Easy2Boot, UNetbootin
- Hybrid MBR systems

### **Hypervisor-Native**
- VirtualBox, KVM, Xen, Hyper-V, Proxmox
- Hypervisor-specific netboot

### **Enterprise Solutions**
- Cobbler, Foreman, MAAS, OpenStack Ironic
- Commercial alternatives available

### **Open Source / Free**
- All Linux bootloaders and tools
- FOG Project, Clonezilla, Rescuezilla
- Most alternatives except commercial solutions

---

## LEGACY SYSTEM SUPPORT MATRIX

| Alternative | BIOS | UEFI | Legacy Hardware | Modern Hardware |
|---|---|---|---|---|
| **iPXE** | ✓ | ✓ | ✓✓✓ | ✓✓✓ |
| **PXELINUX** | ✓ | ✗ | ✓✓✓ | ✓ |
| **GRUB2** | ✓ | ✓ | ✓✓ | ✓✓✓ |
| **Syslinux** | ✓ | ✗ | ✓✓✓ | ✓ |
| **Ventoy** | ✓ | ✓ | ✓✓ | ✓✓✓ |
| **Easy2Boot** | ✓ | ✓ | ✓✓ | ✓✓✓ |
| **U-Boot** | ✓ | ✗ | ✓✓ | ✓ (ARM) |
| **Clonezilla** | ✓ | ✓ | ✓✓ | ✓✓✓ |
| **FOG Project** | ✓ | ✓ | ✓✓ | ✓✓✓ |
| **Rescuezilla** | ✓ | ✓ | ✓✓ | ✓✓✓ |
| **MAAS** | ✓ | ✓ | ✓ | ✓✓✓ |
| **Cobbler** | ✓ | ✓ | ✓ | ✓✓✓ |
| **cloud-init** | ✓ | ✓ | ✓ | ✓✓✓ |
| **Serva** | ✓ | ✓ | ✓✓ | ✓✓✓ |
| **coreboot** | ✓ | ✓ | ✓✓ | ✓✓✓ |

---

## TOP RECOMMENDATIONS BY USE CASE

### **Hybrid BIOS + UEFI Legacy Support**
1. iPXE
2. GRUB2
3. Ventoy
4. Easy2Boot

### **Enterprise Provisioning**
1. MAAS
2. Cobbler
3. Foreman
4. FOG Project

### **Imaging/Cloning**
1. Clonezilla
2. FOG Project
3. Rescuezilla
4. Macrium Reflect

### **Lightweight DHCP/TFTP Server**
1. dnsmasq
2. Serva
3. Tftpd32
4. ISC DHCP + in.tftpd

### **Modern Cloud Infrastructure**
1. cloud-init
2. OpenStack Ironic
3. MAAS
4. Flatcar Linux + Ignition

### **Fully Open Source + Legacy Support**
1. iPXE
2. Clonezilla
3. FOG Project
4. GRUB2

### **Easiest Legacy System Support**
1. Ventoy (USB)
2. Easy2Boot (USB)
3. Clonezilla (bootable media)
4. iPXE (network)

### **Windows Systems**
1. wimboot (for WIM files)
2. WDS (Windows Deployment Services)
3. MDT (Microsoft Deployment Toolkit)
4. Serva (multi-OS)

---

## QUICK SELECTION GUIDE

**Choose iPXE if:** You want modern PXE with HTTP, scripting, and legacy support
**Choose PXELINUX if:** You need simple, lightweight BIOS-only netboot
**Choose GRUB2 if:** You need unified BIOS + UEFI bootloader
**Choose Ventoy if:** You want USB multiboot without extraction
**Choose Clonezilla if:** You need disk imaging for legacy systems
**Choose FOG Project if:** You need enterprise imaging + PXE provisioning
**Choose MAAS if:** You're building modern cloud infrastructure
**Choose cloud-init if:** You want modern, declarative system configuration
**Choose Cobbler if:** You need full-featured enterprise provisioning
