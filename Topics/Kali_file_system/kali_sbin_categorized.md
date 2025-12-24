# Kali Linux /sbin Binaries - Complete Categorization

## Table of Contents
1. [Wireless Security & Network Analysis](#wireless-security--network-analysis)
2. [Network Configuration & Firewalls](#network-configuration--firewalls)
3. [Filesystem & Disk Management](#filesystem--disk-management)
4. [System Administration & User Management](#system-administration--user-management)
5. [Cryptography & Encryption](#cryptography--encryption)
6. [Password & Authentication](#password--authentication)
7. [Exploitation & Penetration Testing](#exploitation--penetration-testing)
8. [Web Servers & Services](#web-servers--services)
9. [DNS & DHCP Services](#dns--dhcp-services)
10. [AppArmor & SELinux Security](#apparmor--selinux-security)
11. [Boot & System Control](#boot--system-control)
12. [Flash Memory & NAND Tools](#flash-memory--nand-tools)
13. [VPN & Tunneling](#vpn--tunneling)
14. [SMB/CIFS & Windows Integration](#smbcifs--windows-integration)
15. [I2C & Hardware Communication](#i2c--hardware-communication)
16. [Auditing & Logging](#auditing--logging)
17. [Package & Software Management](#package--software-management)
18. [Locale & Text Configuration](#locale--text-configuration)
19. [Miscellaneous System Tools](#miscellaneous-system-tools)

---

## 1. Wireless Security & Network Analysis

| **Category** | **Binaries & Directories** | **Explanation** |
|---|---|---|
| **Aircrack-ng Suite** | `airbase-ng`, `aireplay-ng`, `airmon-ng`, `airodump-ng`, `airodump-ng-oui-update`, `airserv-ng`, `airtun-ng`, `airventriloquist-ng`, `easside-ng`, `wesside-ng`, `tkiptun-ng` | Advanced WiFi cracking toolkit for capturing, analyzing, and exploiting WPA/WPA2/WEP encryption with airmon monitoring mode and packet injection |
| **WiFi Testing** | `hostapd`, `hostapd_cli`, `hostapd-mana`, `hostapd-mana_cli`, `hostapd-wpe`, `hostapd-wpe_cli`, `wifite`, `besside-ng` | Rogue AP creation, credential capture, and automated WiFi penetration testing |
| **Wireless Utilities** | `iw`, `iwconfig`, `iwevent`, `iwgetid`, `iwlist`, `iwpriv`, `iwspy`, `rfkill`, `mdk3`, `mdk4` | WiFi device management, channel switching, and RF kill control for wireless security testing |
| **Network Analysis Tools** | `netsniff-ng`, `flowtop`, `ifpps`, `bpfc`, `trafgen`, `mausezahn` | Packet sniffer, network traffic analysis, and payload generation for protocol testing |
| **Packet Capture & Analysis** | `tcpick`, `tcptraceroute`, `trafgen`, `netdiscover` | Advanced packet capture, traffic monitoring, and network topology discovery |

---

## 2. Network Configuration & Firewalls

| **Category** | **Binaries & Directories** | **Explanation** |
|---|---|---|
| **Firewall Rules** | `iptables`, `iptables-legacy`, `iptables-legacy-restore`, `iptables-legacy-save`, `iptables-nft`, `iptables-nft-restore`, `iptables-nft-save`, `iptables-restore`, `iptables-restore-translate`, `iptables-save`, `iptables-translate`, `iptables-apply`, `ip6tables`, `ip6tables-legacy`, `ip6tables-legacy-restore`, `ip6tables-legacy-save`, `ip6tables-nft`, `ip6tables-nft-restore`, `ip6tables-nft-save`, `ip6tables-restore`, `ip6tables-restore-translate`, `ip6tables-save`, `ip6tables-translate`, `ip6tables-apply` | Netfilter firewall rules configuration for IPv4/IPv6 packet filtering and network address translation |
| **ARP Management** | `arptables`, `arptables-nft`, `arptables-nft-restore`, `arptables-nft-save`, `arptables-restore`, `arptables-save`, `arptables-translate`, `arp`, `arpd`, `arp-fingerprint`, `arping`, `arp-scan` | Address Resolution Protocol manipulation, ARP spoofing detection, and network reconnaissance |
| **Bridge Tools** | `bridge`, `brctl`, `ebtables`, `ebtables-nft`, `ebtables-nft-restore`, `ebtables-nft-save`, `ebtables-restore`, `ebtables-save`, `ebtables-translate` | Layer 2 bridge management and Ethernet frame filtering |
| **Advanced Routing** | `ip`, `route`, `iptunnel`, `tc`, `rtacct`, `rtmon`, `devlink`, `nft`, `nftldump` | Complex routing configuration, quality-of-service, and network flow control |
| **Network Interface Config** | `ifconfig`, `ifup`, `ifdown`, `ifquery`, `ipmaddr`, `plipconfig`, `slattach`, `nameif`, `mii-tool`, `ethtool` | Network interface configuration, link status monitoring, and Ethernet negotiation |

---

## 3. Filesystem & Disk Management

| **Category** | **Binaries & Directories** | **Explanation** |
|---|---|---|
| **Partition Management** | `fdisk`, `cfdisk`, `sfdisk`, `parted`, `partprobe`, `gdisk`, `cgdisk`, `sgdisk`, `fixparts` | MBR/GPT partition table manipulation and disk layout management |
| **Filesystem Creation** | `mkfs`, `mkfs.ext2`, `mkfs.ext3`, `mkfs.ext4`, `mke2fs`, `mkfs.fat`, `mkfs.msdos`, `mkfs.vfat`, `mkdosfs`, `mkfs.minix`, `mkfs.cramfs`, `mkfs.jffs2`, `mkfs.ubifs`, `mkfs.exfat`, `mkntfs`, `mkfs.bfs` | Filesystem creation across all major formats |
| **Filesystem Repair** | `fsck`, `fsck.ext2`, `fsck.ext3`, `fsck.ext4`, `e2fsck`, `fsck.fat`, `fsck.msdos`, `fsck.vfat`, `fsck.minix`, `fsck.cramfs`, `fsck.ubifs`, `fsck.exfat`, `dosfsck`, `e2scrub`, `e2scrub_all` | Filesystem integrity checking and repair for all supported formats |
| **EXT Filesystem Tools** | `dumpe2fs`, `tune2fs`, `resize2fs`, `e2image`, `e2label`, `e2mmpstatus`, `e2undo`, `e2freefrag`, `filefrag`, `e2fsck`, `mke2fs`, `mklost+found`, `debugfs` | Extended filesystem optimization, metadata inspection, and recovery |
| **Disk Operations** | `blockdev`, `blkid`, `blkdiscard`, `blkpr`, `findfs`, `fstrim`, `swaplabel`, `fsfreeze` | Low-level block device operations and storage management |
| **Volume Management** | `losetup`, `dmsetup`, `dmstats`, `blkdeactivate`, `lvm`, `pvcreate`, `pvremove`, `pvdisplay`, `vgcreate`, `vgremove`, `vgdisplay`, `lvcreate`, `lvremove`, `lvdisplay` | Device mapper and LVM configuration for logical volume management |
| **NTFS Tools** | `ntfsclone`, `ntfscp`, `ntfslabel`, `ntfsresize`, `ntfsundelete`, `scrounge-ntfs`, `mount.ntfs`, `mount.ntfs-3g`, `mount.lowntfs-3g` | NTFS filesystem forensics and recovery |
| **ExFAT Tools** | `mkfs.exfat`, `fsck.exfat`, `tune.exfat`, `dump.exfat`, `exfatlabel`, `exfat2img` | ExFAT filesystem utilities |
| **UBIFS/JFFS2 Tools** | `ubiattach`, `ubiblock`, `ubicrc32`, `ubidetach`, `ubiformat`, `ubihealthd`, `ubimkvol`, `ubinfo`, `ubinize`, `ubirename`, `ubirmvol`, `ubirsvol`, `ubiscan`, `ubiupdatevol`, `fsck.ubifs`, `mkfs.ubifs`, `jffs2dump`, `jffs2reader`, `jffs2dump` | Flash memory filesystem management |
| **Swap Management** | `mkswap`, `swapon`, `swapoff`, `swaplabel` | Virtual memory swap space configuration |

---

## 4. System Administration & User Management

| **Category** | **Binaries & Directories** | **Explanation** |
|---|---|---|
| **User Management** | `useradd`, `userdel`, `usermod`, `adduser`, `deluser`, `addgroup`, `delgroup`, `newusers`, `pwck`, `grpck`, `pwconv`, `pwunconv`, `grpconv`, `grpunconv`, `chpasswd`, `chgpasswd` | User account creation, modification, and group management |
| **Password & Shadow** | `pwhistory_helper`, `faillock` | Password history enforcement and failed login tracking |
| **Shell Management** | `add-shell`, `remove-shell` | System shell registration for user login shells |
| **System Information** | `dmidecode`, `vpddecode`, `biosdecode` | BIOS and hardware information extraction |
| **Run Control** | `service`, `invoke-rc.d`, `update-rc.d`, `debian-update-rc.d` | SysVinit service management and startup script control |
| **System Limits & Power** | `sysctl`, `rtcwake`, `hwclock`, `ctrlaltdel` | System parameter tuning, wake timers, and power control |
| **Locale Configuration** | `locale-gen`, `update-locale`, `validlocale` | System locale and timezone configuration |

---

## 5. Cryptography & Encryption

| **Category** | **Binaries & Directories** | **Explanation** |
|---|---|---|
| **Disk Encryption** | `cryptsetup`, `cryptdisks_start`, `cryptdisks_stop`, `integritysetup`, `veritysetup`, `luksformat` | LUKS/dm-crypt encryption setup and management for full-disk encryption |
| **Certificate Management** | `update-ca-certificates`, `make-ssl-cert`, `c_rehash` | SSL/TLS certificate installation and configuration |
| **Encryption Keys** | `request-key`, `key.dns_resolver` | Kernel key management and DNS resolver cache |

---

## 6. Password & Authentication

| **Category** | **Binaries & Directories** | **Explanation** |
|---|---|---|
| **John Converters** | `base64conv`, `bitlocker2john`, `dmg2john`, `eapmd5tojohn`, `gpg2john`, `hccap2john`, `keepass2john`, `putty2john`, `racf2john`, `rar2john`, `uaf2john`, `vncpcap2john`, `wpapcap2john`, `zip2john` | Password hash extraction from Windows, encryption, and capture formats |
| **Unshadow & Helpers** | `unshadow`, `unique`, `undrop`, `unafs` | Password file utilities for offline cracking preparation |
| **Cracklib Tools** | `cracklib-check`, `cracklib-format`, `cracklib-packer`, `cracklib-unpacker`, `create-cracklib-dict`, `update-cracklib` | Strong password validation and dictionary building |
| **PAM Authentication** | `pam_getenv`, `pam_namespace_helper`, `pam_timestamp_check`, `pam-auth-update`, `unix_chkpwd`, `unix_update` | Pluggable Authentication Module tools |
| **Authentication Helpers** | `mkhomedir_helper`, `pwhistory_helper` | Home directory and password history management |

---

## 7. Exploitation & Penetration Testing

| **Category** | **Binaries & Directories** | **Explanation** |
|---|---|---|
| **Packet Crafting & Injection** | `hping3`, `mausezahn`, `trafgen`, `curvetun`, `ptunnel` | Custom packet generation and tunnel creation for advanced network attacks |
| **DNS Tools** | `iodine`, `iodine-client-start`, `iodined` | DNS tunneling for covert data exfiltration and command & control |
| **Protocol Exploits** | `responder`, `responder-DHCP_Auto`, `dnsmasq`, `mdk3`, `mdk4` | LLMNR/NBT-NS poisoning and WiFi deauthentication attacks |
| **Credential Capture** | `SIPdump` | SIP protocol credential harvesting |

---

## 8. Web Servers & Services

| **Category** | **Binaries & Directories** | **Explanation** |
|---|---|---|
| **Apache Web Server** | `apache2`, `apache2ctl`, `apachectl`, `a2enmod`, `a2dismod`, `a2ensite`, `a2dissite`, `a2enconf`, `a2disconf`, `a2query`, `httxt2dbm` | HTTP/HTTPS web server configuration and module management |
| **Lighttpd Web Server** | `lighttpd`, `lighttpd-angel`, `lighty-enable-mod`, `lighty-disable-mod`, `lighttpd-enable-mod`, `lighttpd-disable-mod` | Lightweight high-performance web server |
| **Nginx Web Server** | `nginx` | High-performance reverse proxy and web server |
| **PHP Configuration** | `phpenmod`, `phpdismod`, `phpquery` | PHP module and extension management |

---

## 9. DNS & DHCP Services

| **Category** | **Binaries & Directories** | **Explanation** |
|---|---|---|
| **DNS Services** | `dnsmasq`, `nfsconf` | DNS server, DHCP server, and network configuration |
| **DNS Utilities** | `iconvconfig` | DNS configuration conversion tools |
| **DHCP Utilities** | `dhcpcd`, `dhcpd`, `dhcp-lease-list` | DHCP client and server configuration |

---

## 10. AppArmor & SELinux Security

| **Category** | **Binaries & Directories** | **Explanation** |
|---|---|---|
| **AppArmor** | `aa-load`, `aa-remove-unknown`, `aa-status`, `aa-teardown`, `apparmor_parser`, `apparmor_status` | Mandatory Access Control enforcement and profile management |
| **SELinux Tools** | `selinux_check_access`, `selinux_check_securetty_context`, `selinuxenabled`, `selinuxexeccon`, `semodule`, `setenforce`, `getenforce`, `getsebool`, `setsebool`, `togglesebool`, `setfiles`, `restorecon`, `restorecon_xattr`, `matchpathcon`, `getfilecon`, `setfilecon`, `getconlist`, `getdefaultcon`, `getseuser`, `validatetrans`, `genhostedcon`, `genl`, `checkpolicy`, `dispol` | SELinux security context management and policy enforcement |
| **SELinux Labeling** | `sefcontext_compile`, `selabel_compare`, `selabel_digest`, `selabel_get_digests_all_partial_matches`, `selabel_lookup`, `selabel_lookup_best_match`, `selabel_partial_match`, `fixfiles` | SELinux file context and label management |

---

## 11. Boot & System Control

| **Category** | **Binaries & Directories** | **Explanation** |
|---|---|---|
| **GRUB Configuration** | `grub-install`, `grub-mkconfig`, `grub-mkdevicemap`, `grub-probe`, `grub-reboot`, `grub-set-default`, `grub-macbless`, `update-grub`, `update-grub2` | GRUB2 bootloader installation and configuration |
| **System Control** | `systemctl`, `halt`, `reboot`, `poweroff`, `shutdown`, `init`, `sulogin` | System startup, shutdown, and runlevel management |
| **Kernel Boot** | `installkernel`, `mkinitramfs`, `update-initramfs` | Kernel installation and initial ramdisk creation |

---

## 12. Flash Memory & NAND Tools

| **Category** | **Binaries & Directories** | **Explanation** |
|---|---|---|
| **NAND Flash Tools** | `nanddump`, `nandflipbits`, `nandtest`, `nandwrite`, `mtd_debug`, `mtdinfo`, `mtdpart`, `jffs2dump`, `jffs2reader`, `sumtool` | Low-level NAND flash memory access and testing |
| **MTD Utilities** | `flashcp`, `flash_erase`, `flash_eraseall`, `flash_lock`, `flash_otp_dump`, `flash_otp_erase`, `flash_otp_info`, `flash_otp_lock`, `flash_otp_write`, `flash_unlock`, `ftl_check`, `ftl_format`, `nftl_format`, `rfdformat`, `rfddump` | Memory Technology Device management and flash programming |
| **Firmware Tools** | `flashrom`, `cbfstool`, `cbfs-compression-tool`, `cbmem`, `fmaptool`, `ifdtool`, `ifittool`, `intelmetool`, `inteltool`, `intelvbttool`, `nvramtool`, `pmh7tool`, `rmodtool`, `superiotool`, `bucts` | BIOS, firmware, and system memory tools for x86 systems |

---

## 13. VPN & Tunneling

| **Category** | **Binaries & Directories** | **Explanation** |
|---|---|---|
| **OpenVPN** | `openvpn` | TLS-based virtual private network implementation |
| **IPSec & L2TP** | `ipsec`, `kl2tpd`, `ql2tpd`, `pppoe-discovery`, `pptp`, `pptpsetup` | IPSec, L2TP, and PPPoE tunneling protocols |
| **PPTP & PPP** | `pppd`, `pppoe-discovery`, `pppstats`, `pppdump` | Point-to-Point Protocol implementation and debugging |
| **OpenConnect** | `openconnect` | Cisco AnyConnect and Juniper SSL VPN client |
| **VPN Utilities** | `vpnc`, `vpnc-connect`, `vpnc-disconnect` | Cisco VPN client implementation |

---

## 14. SMB/CIFS & Windows Integration

| **Category** | **Binaries & Directories** | **Explanation** |
|---|---|---|
| **Samba SMB Server** | `smbd`, `nmbd`, `winbindd` | SMB/CIFS file and print sharing server with Windows domain integration |
| **Mount SMB** | `mount.cifs`, `mount.smb3`, `umount.nfs`, `umount.nfs4` | CIFS/SMB filesystem mounting for Windows share access |
| **Samba Utilities** | `samba-gpupdate`, `sampasswd`, `samunlock`, `samusrgrp`, `eventlogadm` | Samba administrative tools for Windows integration |

---

## 15. I2C & Hardware Communication

| **Category** | **Binaries & Directories** | **Explanation** |
|---|---|---|
| **I2C Tools** | `i2cdetect`, `i2cdump`, `i2cget`, `i2cset`, `i2c-stub-from-dump`, `i2ctransfer` | I2C bus device enumeration, register access, and communication |
| **Hardware Sensors** | `sensors-detect`, `isadump`, `isaset` | ISA/I2C sensor detection and configuration |

---

## 16. Auditing & Logging

| **Category** | **Binaries & Directories** | **Explanation** |
|---|---|---|
| **Linux Audit** | `auditctl`, `auditd`, `augenrules`, `aureport`, `ausearch`, `avcstat` | System call auditing and security event logging |
| **Audit Dispatcher** | `audisp-af_unix`, `audisp-filter`, `audisp-syslog` | Audit event filtering and routing |
| **System Logging** | `logrotate`, `logsave`, `split-logfile` | Log rotation and retention management |

---

## 17. Package & Software Management

| **Category** | **Binaries & Directories** | **Explanation** |
|---|---|---|
| **APT Configuration** | `dpkg-preconfigure`, `dpkg-reconfigure` | Debian package preconfiguration and reconfiguration |
| **Dictionary Management** | `ispell-autobuildhash`, `aspell-autobuildhash`, `pg_updatedicts`, `select-default-ispell`, `select-default-wordlist`, `remove-default-ispell`, `remove-default-wordlist`, `update-default-ispell`, `update-default-wordlist`, `update-dictcommon-aspell`, `update-dictcommon-hunspell` | Spell checker and dictionary database management |
| **Documentation Installation** | `install-docs`, `install-sgmlcatalog`, `update-catalog` | Documentation and SGML catalog installation |
| **TeX/LaTeX Management** | `update-texmf`, `update-texmf-config`, `update-tl-stacked-conffile`, `update-fmtutil`, `update-updmap`, `pg_updatedicts` | TeX Live package and format management |
| **Font Management** | `update-fonts-alias`, `update-fonts-dir`, `update-fonts-scale`, `update-gsfontmap` | System font installation and cache updates |
| **Icon Cache** | `update-icon-caches` | Desktop icon cache generation |
| **Java Alternatives** | `update-java-alternatives` | Java compiler and runtime selection |
| **IEEE Data** | `update-ieee-data`, `get-oui` | IEEE OUI database updates for MAC address resolution |
| **Command Not Found** | `update-command-not-found` | Command suggestions database updates |
| **Network Protocols** | `update-inetd` | Internet daemon service configuration |

---

## 18. Locale & Text Configuration

| **Category** | **Binaries & Directories** | **Explanation** |
|---|---|---|
| **Locale Configuration** | `locale-gen`, `update-locale`, `validlocale` | System language and character encoding setup |
| **Timezone Configuration** | `zic` | Timezone database compilation |
| **Text Encodings** | `iconvconfig` | Character encoding conversion database |

---

## 19. Miscellaneous System Tools

| **Category** | **Binaries & Directories** | **Explanation** |
|---|---|---|
| **Process Management** | `killall5`, `start-stop-daemon` | Process termination and daemon lifecycle management |
| **File System Stats** | `readprofile` | Kernel profiling statistics analysis |
| **System Time** | `vcstime` | Version control system time synchronization |
| **Module Management** | `depmod`, `insmod`, `modinfo`, `modprobe`, `rmmod`, `lsmod` | Kernel module loading, unloading, and dependency management |
| **Capabilities** | `getcap`, `setcap`, `getpcaps` | Linux capability management for privilege separation |
| **Print Spooler** | `cupsd` | CUPS print server daemon |
| **Service Discovery** | `avahi-daemon` | mDNS/DNS-SD service discovery daemon |
| **Device Management** | `usbmuxd`, `usb_modeswitch`, `usb_modeswitch_dispatcher` | USB device mode switching and iTunes sync |
| **Bluetooth** | `bluetoothd`, `pcscd` | Bluetooth and smartcard daemon services |
| **Network Services** | `rpcbind`, `rpc.statd`, `rpc.gssd`, `rpc.idmapd`, `rpc.svcgssd`, `rpc.svcgssd`, `rpcdebug`, `rpcctl`, `showmount`, `mountstats`, `nfsconf`, `nfsidmap`, `nfsiostat`, `nfsstat` | NFS, RPC, and network file system services |
| **Display Manager** | `lightdm`, `lightdm-gtk-greeter`, `plymouthd`, `plymouth-set-default-theme` | Display and login manager services |
| **Power Management** | `haveged`, `rtkitctl`, `on_ac_power` | Entropy generation and power state management |
| **Paper Configuration** | `paperconfig` | Paper size and printing configuration |
| **GPU/Video** | `setvesablank`, `vbetool`, `intel-virtual-output` | Video mode and GPU configuration |
| **System Monitoring** | `rdma`, `vdpa` | RDMA and vDPA device monitoring |
| **Remote Desktop** | `xrdp`, `xrdp-chansrv`, `xrdp-sesman` | RDP remote desktop protocol server |
| **SSH Server** | `sshd` | Secure shell daemon for remote access |
| **SSL Proxy** | `sslh`, `sslh-ev`, `sslh-select` | SSL/TLS connection multiplexer |
| **Backup & Recovery** | `tarcat`, `recv_image`, `serve_image` | Backup image transmission and recovery |
| **Privilege Control** | `sudo_logsrvd`, `sudo_sendlog` | Sudo command logging service |
| **Run User** | `runuser` | Execute command with different user privileges |
| **System Tools** | `system-tools-backends` | System administration backend services |
| **GNUPG Home** | `addgnupghome`, `applygnupgdefaults` | GnuPG home directory initialization |
| **User Access DB** | `accessdb` | User/group database for access control |
| **NFS/RPC Debugging** | `rpcdebug`, `rpcctl`, `rpcinf` | Remote Procedure Call debugging |
| **OpenVAS Security** | `openvas`, `gvmd` | Vulnerability scanner daemon and manager |
| **SNMP Services** | `snmpd` | SNMP monitoring daemon |
| **Smart Monitoring** | `smartctl`, `smartd`, `update-smart-drivedb` | Disk SMART health monitoring |
| **Dynamic Linking** | `ldconfig` | Shared library cache configuration |
| **Scan Media** | `saned` | SANE scanner access daemon |
| **Reset System** | `fstab-decode` | Filesystem table decoding for mount operations |

---

## Summary Statistics

| Metric | Count |
|--------|-------|
| **Total Binaries/Directories** | 660 |
| **Wireless Security Tools** | 40+ |
| **Network & Firewall Tools** | 80+ |
| **Filesystem Management** | 100+ |
| **User & System Admin** | 50+ |
| **Cryptography & Auth** | 60+ |
| **Penetration Testing** | 30+ |
| **Web Servers** | 20+ |
| **Services & Daemons** | 100+ |
| **Package Management** | 50+ |

---

## Key Insights: Why Kali Includes So Many /sbin Tools

The `/sbin` directory contains **system administration and security-critical binaries** essential for penetration testing:

### Penetration Testing Coverage
1. **Network Attack Surface** - Wireless exploitation, ARP spoofing, packet crafting
2. **System Compromise** - User account manipulation, authentication bypass, privilege escalation
3. **Persistence & Evasion** - Boot modification, firewall rules, rootkit/MAC prevention
4. **Evidence Removal** - Filesystem manipulation, log clearing, secure deletion
5. **Infrastructure Testing** - DNS poisoning, DHCP attacks, protocol fuzzing

### System Administration for Red Teamers
- Boot access and kernel parameters
- Firewall rule crafting for command & control
- User creation for persistence
- Encryption setup for data exfiltration
- Network service configuration for attack infrastructure

### Credential Harvesting
- 14+ hash converters for offline cracking
- Password file utilities for shadow synchronization
- Authentication bypass techniques
- Windows credential extraction tools

The comprehensive /sbin suite enables both offensive operations and defensive hardening during security assessments.
