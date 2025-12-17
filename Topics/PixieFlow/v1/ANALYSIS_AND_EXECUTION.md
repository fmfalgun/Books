# Netboot File Analysis & Execution: Deep Technical Manual

> A comprehensive guide to understanding, analyzing, extracting, debugging, and instrumenting netboot artifacts. Includes tools, methods, and workflows for security researchers, OS developers, and infrastructure engineers.

---

## Table of Contents

1. [Overview: Why Analyze These Files](#overview)
2. [Bootloader Binaries: pxelinux.0 & grubx64.efi](#bootloader-binaries)
3. [Syslinux COM32 Modules (.c32)](#syslinux-modules)
4. [The Configuration Files: default, grub.cfg](#config-files)
5. [Initramfs/Initrd: Extraction & Analysis](#initramfs-analysis)
6. [Squashfs: Inspection & Modification](#squashfs-analysis)
7. [Runtime Execution & Tracing](#runtime-execution)
8. [Network Boot Flow Debugging](#netboot-debugging)
9. [Security Analysis & Threat Modeling](#security-analysis)
10. [Lab Environment Setup](#lab-setup)

---

## 1. Overview: Why Analyze These Files?

### The Need

When developing or deploying custom netboot OS infrastructure, you need to:

- **Verify integrity** of bootloaders and kernel images.
- **Debug boot failures** by tracing module loading sequence.
- **Inspect filesystem contents** without booting the system.
- **Modify configs** for per-device/per-role customization.
- **Test security controls** (Secure Boot, measured boot, TPM).
- **Optimize boot time** by profiling module loads and init script execution.
- **Analyze attack surface** (e.g., what happens if TFTP server is compromised?).

### The Use Cases

- **Offensive**: Inject custom payloads into TFTP-served initramfs for in-network attacks.
- **Defensive**: Verify boot chain integrity and detect tampering.
- **Development**: Iterate on custom OS root and netboot configs.
- **Incident Response**: Extract and analyze forensic images captured via netboot.

---

## 2. Bootloader Binaries: `pxelinux.0` and `grubx64.efi`

### 2.1 Understanding Binary Format

#### `pxelinux.0` Structure

```
pxelinux.0 file format:

Position 0x0000-0x0200   | MBR-like header (compatibility)
Position 0x0200+         | PXE stub (implements PXE protocol)
Position varies          | Embedded support modules (may include ldlinux.c32)
```

**Key properties:**

- **Arch**: x86 real mode + protected mode code
- **Size**: Typically 20-50 KB
- **Execution**: Runs in real mode initially, then transitions to protected mode
- **Dependencies**: Requires `ldlinux.c32` at runtime (unless statically linked)

#### `grubx64.efi` Structure

```
grubx64.efi file format:

EFI Header (PE32+)
  ├── DOS header
  ├── PE signature
  ├── COFF header
  ├── Optional header (64-bit)
  └── Sections (.text, .data, .reloc, etc.)
```

**Key properties:**

- **Arch**: x86-64 EFI binary
- **Size**: Typically 100-500 KB (varies with embedded modules)
- **Execution**: Runs in UEFI protected mode directly
- **Dependencies**: May embed or reference modules at runtime

### 2.2 Binary Analysis Tools

#### File Type Detection

```bash
# Identify binary type
file pxelinux.0
# Expected: pxelinux.0: Linux x86 boot sector

file grubx64.efi
# Expected: grubx64.efi: PE32+ executable (EFI application) x86-64

# More detailed inspection
hexdump -C pxelinux.0 | head -20
# Look for: boot sector magic (0xaa55 at offset 0x1fe)

objdump -p grubx64.efi | head -30
# Shows PE header details, sections, entry point
```

#### Size & Entropy Analysis

```bash
# Check size and compression ratio (indicates if embedded code)
du -h pxelinux.0 grubx64.efi

# Analyze entropy (high entropy = likely compressed/encrypted sections)
python3 << 'EOF'
import sys
from collections import Counter

with open('pxelinux.0', 'rb') as f:
    data = f.read()

byte_freq = Counter(data)
entropy = 0.0
for count in byte_freq.values():
    freq = count / len(data)
    entropy -= freq * (freq ** 0.5)  # Simplified Shannon entropy
    
print(f"File size: {len(data)} bytes")
print(f"Entropy: {entropy:.2f} (0=low, 8=high)")
print(f"Unique bytes: {len(byte_freq)}/256")
EOF
```

#### String Extraction & Analysis

```bash
# Extract readable strings (indicates debug symbols, error messages, etc.)
strings pxelinux.0 | head -30
# Look for: DHCP info, module names, error strings

strings grubx64.efi | grep -i "error\|fail\|load"
# Understand error paths and capabilities

# Strings with offsets
strings -t x pxelinux.0 | head -20
# Offsets help correlate with disassembly
```

#### Disassembly & Code Analysis

```bash
# For pxelinux.0 (x86 real + protected mode)
objdump -D -b binary -m i386 -M intel pxelinux.0 | head -50

# For grubx64.efi (x86-64 EFI)
objdump -D -m x86-64 -M intel grubx64.efi | head -50

# With source annotations (if debug symbols present)
objdump -S grubx64.efi | head -50

# Find specific functions or boot entry point
nm grubx64.efi | grep -i "main\|entry\|_start"
readelf -l grubx64.efi | grep -i "entry"
```

#### Hex Dump & Low-Level Inspection

```bash
# First 1 KB of bootloader
hexdump -C pxelinux.0 | head -40

# Search for patterns (e.g., "GRUB" magic)
hexdump -C grubx64.efi | grep "GRUB\|EFI\|UEFI"
od -c -Ad pxelinux.0 | grep -E "DHCP|PXE|boot"

# Find relocatable sections or import tables
readelf -r grubx64.efi | head -20
```

### 2.3 Runtime Behavior (QEMU Tracing)

```bash
# Boot pxelinux.0 with serial logging
qemu-system-x86_64 \
    -machine pc \
    -rom /path/to/pxelinux.0 \
    -boot n \
    -net nic,model=e1000 \
    -net user,tftp=/srv/tftp \
    -serial stdio \
    -d int,exec,guest_errors \
    2>&1 | tee boot.log

# Parse the log for:
# - DHCP discovery
# - TFTP file requests
# - Module loading sequence

# Boot grubx64.efi in UEFI mode
qemu-system-x86_64 \
    -machine pc,acpi=on \
    -bios /usr/share/OVMF/OVMF_CODE.fd \
    -net nic,model=e1000 \
    -net user,tftp=/srv/tftp \
    -serial stdio \
    2>&1 | tee uefi_boot.log
```

---

## 3. Syslinux COM32 Modules: `*.c32` Analysis

### 3.1 COM32 Module Format

COM32 is a simple object format used by Syslinux:

```
*.c32 file format:

Offset 0x0000-0x0003  | Magic: 0x00140001 (version, reversed byte order)
Offset 0x0004-0x0007  | Descriptor offset (points to metadata)
Offset 0x0008+        | Actual code/data segments
Descriptor section:
  ├── Module name
  ├── Dependencies (list of other .c32 files required)
  ├── Code section info
  └── Data section info
```

### 3.2 Module Inspection Tools

#### Identify Module Type & Dependencies

```bash
# Extract COM32 metadata (custom tool needed, using hexdump as fallback)
hexdump -C ldlinux.c32 | head -5
# Look for magic at offset 0x0000

# Check file type
file ldlinux.c32
file libcom32.c32
# Expected: COM32 module or similar

# Extract strings to understand module purpose
strings ldlinux.c32 | grep -i "module\|require\|load"
strings vesamenu.c32 | grep -i "menu\|vesa\|video"
```

#### Dependency Tree Analysis

Syslinux modules have dependencies. Example tree for netboot:

```
pxelinux.0
  ├── requires: ldlinux.c32
  
ldlinux.c32 (core runtime)
  ├── provides: COM32 API
  
vesamenu.c32 (graphical menu)
  ├── requires: libcom32.c32
  ├── requires: libutil.c32
  
libcom32.c32 (library)
  ├── provides: common utilities
  
libutil.c32 (library)
  ├── provides: utility functions
```

To verify dependencies are present:

```bash
# Create a tool to parse COM32 metadata
cat > check_modules.sh << 'EOF'
#!/bin/bash
# List all .c32 modules and their dependencies

TFTP_DIR="${1:-/srv/tftp}"

echo "=== Syslinux Modules in $TFTP_DIR ==="
ls -lh "$TFTP_DIR"/*.c32 2>/dev/null || echo "No .c32 files found"

echo ""
echo "=== String-based Dependency Hints ==="

# vesamenu needs these
for mod in libcom32.c32 libutil.c32 vesamenu.c32; do
    if [ -f "$TFTP_DIR/$mod" ]; then
        echo "$mod: $(strings $TFTP_DIR/$mod | wc -l) strings"
    fi
done

echo ""
echo "=== Common Issues ==="
# Check if ldlinux is present (required for pxelinux)
[ -f "$TFTP_DIR/ldlinux.c32" ] && echo "✓ ldlinux.c32 present" || echo "✗ MISSING: ldlinux.c32"

# Check if lib files are present (required for vesamenu)
[ -f "$TFTP_DIR/libcom32.c32" ] && echo "✓ libcom32.c32 present" || echo "✗ MISSING: libcom32.c32"
[ -f "$TFTP_DIR/libutil.c32" ] && echo "✓ libutil.c32 present" || echo "✗ MISSING: libutil.c32"
EOF

chmod +x check_modules.sh
./check_modules.sh /srv/tftp
```

#### Version Checking

```bash
# Syslinux version determines module compatibility
# Cross-version mixing often fails

# Get syslinux package version
dpkg -l | grep syslinux

# Check module timestamps
ls -la /srv/tftp/*.c32 | awk '{print $6, $7, $NF}'
# All should have similar dates (from same syslinux release)

# Verify by comparing module sizes to official version
# Official syslinux 6.04:
#   ldlinux.c32 ~ 150 KB
#   libcom32.c32 ~ 30 KB
#   vesamenu.c32 ~ 45 KB

du -h /srv/tftp/*.c32
```

#### Module Patching & Modification

```bash
# COM32 modules are not easily patched (unlike shell scripts)
# Instead, create custom wrapper or menu configuration

# Example: Override menu title without modifying vesamenu.c32
cat /srv/tftp/pxelinux.cfg/default

# Modify the MENU TITLE line
sed -i 's/MENU TITLE.*/MENU TITLE My Custom Netboot/' /srv/tftp/pxelinux.cfg/default
```

---

## 4. Configuration Files: `default` and `grub.cfg`

### 4.1 `pxelinux.cfg/default` Analysis

#### File Structure

```cfg
# /srv/tftp/pxelinux.cfg/default

# Bootloader settings
DEFAULT vesamenu.c32        # Default display module
PROMPT 0                    # 0=no prompt, 1=show boot:
TIMEOUT 50                  # Timeout in 0.1 second units (50 = 5 seconds)
ONTIMEOUT myos              # Label to boot on timeout

# UI configuration
MENU TITLE My Netboot Environment
MENU COLOR sel 7 0 #ffffff #000000

# Boot labels
LABEL myos
  MENU LABEL My Custom OS (netboot)
  KERNEL /vmlinuz-myos
  APPEND initrd=/initrd-myos.img root=/dev/nfs nfsroot=192.168.1.10:/exports/myos ip=dhcp

LABEL debug
  MENU LABEL Emergency Shell
  KERNEL /vmlinuz-myos
  APPEND initrd=/initrd-debug.img break=init
```

#### Parsing & Validation

```bash
# Syntax check for pxelinux config
cat > validate_pxelinux_cfg.sh << 'EOF'
#!/bin/bash

CFG="${1:-/srv/tftp/pxelinux.cfg/default}"

echo "=== Validating PXELINUX Config ==="

# Check required keywords
for keyword in DEFAULT MENU; do
    grep -q "^$keyword" "$CFG" && echo "✓ $keyword defined" || echo "✗ MISSING: $keyword"
done

# Parse LABEL entries
echo ""
echo "=== Boot Labels Found ==="
grep -E "^LABEL " "$CFG" | awk '{print "  - " $2}'

# Check referenced files exist
echo ""
echo "=== Checking Referenced Files ==="
KERNEL_DIR="/srv/tftp"

grep -E "^\s+(KERNEL|APPEND)" "$CFG" | grep -oE "/([\w\-\.]+)" | while read file; do
    if [ -f "$KERNEL_DIR$file" ]; then
        echo "✓ $file ($(du -h $KERNEL_DIR$file | cut -f1))"
    else
        echo "✗ MISSING: $file"
    fi
done

echo ""
echo "=== Kernel Command Line Parameters ==="
grep "APPEND" "$CFG" | sed 's/.*APPEND //' | tr ' ' '\n' | sort -u
EOF

chmod +x validate_pxelinux_cfg.sh
./validate_pxelinux_cfg.sh
```

#### Common Configuration Patterns

```cfg
# Pattern 1: NFS Root
APPEND initrd=/initrd.img root=/dev/nfs nfsroot=server:/path ip=dhcp

# Pattern 2: SquashFS from NFS + OverlayFS
APPEND initrd=/initrd.img boot=live root=/dev/nfs nfsroot=server:/squash ro

# Pattern 3: iSCSI Root
APPEND initrd=/initrd.img root=/dev/iscsi iscsi_initiator=iqn.2025.netboot:client

# Pattern 4: HTTP-fetched filesystem
APPEND initrd=/initrd.img root=/dev/http http_url=http://server/images/root.squashfs

# Pattern 5: RAM-only (testing/debugging)
APPEND initrd=/initrd.img root=/dev/ram0 console=ttyS0
```

### 4.2 `grub.cfg` Analysis

#### File Structure

```cfg
# /srv/tftp/grub.cfg (or /boot/efi/EFI/BOOT/grub.cfg)

set default=0
set timeout=5

# Variable definitions
set root=(tftp,192.168.1.10)

menuentry "My Custom OS (netboot)" {
    set root=(tftp,192.168.1.10)
    linux /vmlinuz-myos \
        ip=dhcp \
        root=/dev/nfs \
        nfsroot=192.168.1.10:/exports/myos,nolock,vers=3 \
        rw console=ttyS0
    initrd /initrd-myos.img
}

menuentry "Debug Shell" {
    linux /vmlinuz-myos root=/dev/ram0 console=ttyS0 rw
    initrd /initrd-debug.img
}
```

#### Parsing & Validation

```bash
# GRUB config syntax check
grub-script-check /boot/grub/grub.cfg

# Extract kernel command lines from GRUB config
cat > extract_grub_cmdlines.sh << 'EOF'
#!/bin/bash

CFG="${1:-/srv/tftp/grub.cfg}"

echo "=== GRUB Boot Entries ==="

awk '
/^menuentry/ {
    match($0, /"([^"]+)"/, entry)
    print "Entry: " entry[1]
}
/^\s+linux\s/ {
    match($0, /linux\s+([^ ]+)(.*)/, linux_info)
    print "  Kernel: " linux_info[1]
    print "  Cmdline: " linux_info[2]
}
/^\s+initrd/ {
    match($0, /initrd\s+(.+)/, initrd_info)
    print "  Initrd: " initrd_info[1]
}
/^\s*\}/ {
    print ""
}
' "$CFG"
EOF

chmod +x extract_grub_cmdlines.sh
./extract_grub_cmdlines.sh
```

#### GRUB vs PXELINUX: Comparison

| Feature | PXELINUX | GRUB |
|---------|----------|------|
| **Menu System** | Simple text/graphical (vesamenu) | Complex, multi-OS aware |
| **Configuration** | Text-based, simple syntax | Text-based, scripting-capable |
| **Module Loading** | .c32 modules | ELF-based modules |
| **Network Support** | TFTP, PXE built-in | TFTP, HTTP, NFS via modules |
| **Security** | Limited | Secure Boot support |
| **Flexibility** | Less flexible | Very flexible |

---

## 5. Initramfs/Initrd: Extraction & Deep Analysis

### 5.1 Initramfs Format Overview

Modern initramfs uses **CPIO** archive format (not ext2/ext3 as in older initrd):

```
Initramfs structure:

[CPIO Header] [File metadata] [File content]
[CPIO Header] [File metadata] [File content]
... (repeated for each file)
[CPIO Trailer] [Optional padding]
```

**Typical compression**: gzip (most common), xz, bzip2

### 5.2 Extraction Methods

#### Method 1: Simple Extraction (gzip+cpio)

```bash
# Extract gzip-compressed initramfs
gunzip -c /boot/initramfs-5.15.0-generic.img | cpio -ivd -D /tmp/initramfs-extract/

# Or in one command
zcat /boot/initramfs-5.15.0-generic.img | cpio -idmv > /tmp/initramfs-extract/

# List without extracting
zcat /boot/initramfs-5.15.0-generic.img | cpio -t
```

#### Method 2: Using `lsinitrd` (Debian/Ubuntu/Fedora)

```bash
# List initramfs content
lsinitrd /boot/initramfs-5.15.0-generic.img

# Extract to directory
lsinitrd -x /tmp/initramfs-extract /boot/initramfs-5.15.0-generic.img

# Show dependencies
lsinitrd -k /boot/initramfs-5.15.0-generic.img | grep ".ko"
```

#### Method 3: Using `unmkinitramfs` (Debian-specific)

```bash
# Modern Debian initramfs can have multiple CPIO sections
unmkinitramfs /boot/initramfs-5.15.0-generic.img /tmp/initramfs-extract/

# Lists extracted sections
ls -la /tmp/initramfs-extract/
```

#### Method 4: Manual Inspection with `file` & `dd`

```bash
# Determine compression type
file /boot/initramfs-5.15.0-generic.img

# If file has early CPIO before compression, skip to it
hexdump -C /boot/initramfs-5.15.0-generic.img | head -10
# Look for: "070701" (newc CPIO magic)

# Extract CPIO section (if not gzipped at file start)
dd if=/boot/initramfs-5.15.0-generic.img bs=1 skip=OFFSET | zcat | cpio -idmv
# (OFFSET is the byte offset where gzip or CPIO starts)
```

### 5.3 Content Analysis

#### What's Inside an Initramfs?

```bash
# Extract and explore
zcat /boot/initramfs-5.15.0-generic.img | cpio -idmv

# List directory structure
tree /tmp/initramfs-extract/ --dirsfirst

# Find init scripts
find /tmp/initramfs-extract/ -name "init*" -type f

# Count kernel modules
find /tmp/initramfs-extract/ -name "*.ko" | wc -l

# List all executables
find /tmp/initramfs-extract/ -type f -executable
```

#### Analyzing Init Script

```bash
# Read the main init script
cat /tmp/initramfs-extract/init
cat /tmp/initramfs-extract/init.real (if present)

# Check for busybox
file /tmp/initramfs-extract/bin/busybox
strings /tmp/initramfs-extract/bin/busybox | head -20

# Analyze init flow
bash -x /tmp/initramfs-extract/init 2>&1 | head -100
# (Don't actually execute; just trace syntax)

# Look for network initialization
grep -r "DHCP\|dhcp\|ifconfig\|ip link" /tmp/initramfs-extract/
```

#### Module Dependencies

```bash
# List all kernel modules
find /tmp/initramfs-extract/lib/modules -name "*.ko" | sort

# Show module info
modinfo /tmp/initramfs-extract/lib/modules/$(uname -r)/kernel/drivers/net/e1000/e1000.ko

# Check module dependencies
modprobe -l | grep nfs
cat /tmp/initramfs-extract/lib/modules/$(uname -r)/modules.dep | grep nfs
```

### 5.4 Modifying Initramfs

```bash
#!/bin/bash
# Modify and rebuild initramfs

ORIGINAL="/boot/initramfs-5.15.0-generic.img"
EXTRACT_DIR="/tmp/initramfs-custom"
OUTPUT="/boot/initramfs-5.15.0-generic-custom.img"

# Extract
mkdir -p "$EXTRACT_DIR"
cd "$EXTRACT_DIR"
zcat "$ORIGINAL" | cpio -idmv

# Modify init script
cat > init.patch << 'EOF'
#!/bin/sh
# Add custom logging
exec >/dev/console 2>&1
echo "[CUSTOM INIT] Booting..."

# Original init commands follow...
EOF

# Replace init
cp init.patch init
chmod +x init

# Rebuild
cd "$EXTRACT_DIR"
find . -print0 | cpio -0o -H newc -R 0:0 | gzip > "$OUTPUT"

echo "New initramfs: $OUTPUT"
ls -lh "$OUTPUT"
```

### 5.5 Boot-Time Inspection

```bash
# Add break point to initramfs via kernel command line
# (if your init script supports it)

KERNEL_CMDLINE="break=init root=/dev/nfs ..."
# Kernel param 'break' will drop to shell before pivot_root

# Or modify init to always drop to shell
sed -i 's|exec switch_root|exec /bin/sh|' /tmp/initramfs-custom/init
```

---

## 6. SquashFS: Inspection & Modification

### 6.1 SquashFS Overview

SquashFS is a compressed read-only filesystem used for:

- Live systems (Live USB, Live CD)
- Netboot immutable roots
- Container images

**Characteristics:**

- Highly compressed (xz, zstd compression available)
- Read-only (prevents accidental modification during boot)
- Fast extraction (random access to files)

### 6.2 Inspection

#### Mount and Inspect

```bash
# Mount SquashFS (read-only)
mkdir -p /mnt/squash
mount -t squashfs filesystem.squashfs /mnt/squash

# List contents
ls -la /mnt/squash/

# Search for files
find /mnt/squash -name "passwd" -type f
find /mnt/squash -name "*.so" -type f | head -20

# Check disk usage
du -sh /mnt/squash/
du -sh /mnt/squash/* | sort -h

# Unmount
umount /mnt/squash
```

#### Direct Extraction (Without Mount)

```bash
# Extract entire SquashFS
unsquashfs -d /tmp/squash-extract filesystem.squashfs

# Extract specific files
unsquashfs -e "etc/passwd" filesystem.squashfs

# List without extracting
unsquashfs -l filesystem.squashfs | head -50

# Check compression ratio
ls -lh filesystem.squashfs
du -sh /tmp/squash-extract
```

#### Metadata Analysis

```bash
# Detailed SquashFS info
unsquashfs -s filesystem.squashfs

# Output example:
# Found a valid SQUASHFS 4:0 superblock on filesystem.squashfs.
# Creation or last append time Tue Jan 01 00:00:00 2025
# Filesystem size 245.96 MBytes
# Compression xz
# Block size 1048576
# Number of inodes 12345
# Number of fragments 234
# Number of regular files 5000
# Number of directories 1234
```

### 6.3 Modification Workflow

SquashFS is read-only, but you can create a new one:

```bash
#!/bin/bash
# Modify OS root and create new SquashFS

ORIGINAL="/path/to/filesystem.squashfs"
WORK_DIR="/tmp/squash-work"
OUTPUT="/srv/tftp/filesystem-modified.squashfs"

# Extract
mkdir -p "$WORK_DIR"
unsquashfs -d "$WORK_DIR/root" "$ORIGINAL"

# Make modifications
echo "127.0.0.1 myhost.local" >> "$WORK_DIR/root/etc/hosts"
echo "export CUSTOM_VAR=1" >> "$WORK_DIR/root/etc/profile"

# Rebuild with xz compression
mksquashfs "$WORK_DIR/root" "$OUTPUT" -comp xz -b 1M -Xbcj x86

ls -lh "$OUTPUT"
```

### 6.4 Performance Analysis

```bash
# Compare compression methods
for comp in gzip xz zstd; do
    echo "Testing $comp compression..."
    time mksquashfs /tmp/squash-root \
        /tmp/test-$comp.squashfs \
        -comp $comp -b 1M -progress
done

# Results: xz = smaller but slower, zstd = faster but larger
ls -lh /tmp/test-*.squashfs
```

---

## 7. Runtime Execution & Tracing

### 7.1 QEMU-based Netboot Testing

#### Setup Virtual Network Boot

```bash
#!/bin/bash

# Directory with netboot files
TFTP_DIR="/srv/tftp"

# Start QEMU with netboot
qemu-system-x86_64 \
    -machine pc \
    -m 1024 \
    -enable-kvm \
    -boot n \
    -net nic,model=e1000 \
    -net user,tftp=$TFTP_DIR,bootfile=pxelinux.0 \
    -serial stdio \
    -nographic \
    2>&1 | tee qemu_netboot.log
```

#### Serial Console Capture & Analysis

```bash
# Boot with serial output logging
qemu-system-x86_64 \
    -boot n \
    -net user,tftp=/srv/tftp \
    -serial file:qemu_serial.log \
    ...

# Analyze boot log
grep -i "tftp\|dhcp\|loading\|error" qemu_serial.log

# Timeline analysis
cat > analyze_boot_log.py << 'EOF'
#!/usr/bin/env python3
import re
from datetime import datetime

log_file = "qemu_serial.log"
patterns = {
    'dhcp': re.compile(r'DHCP|dhcp'),
    'tftp': re.compile(r'TFTP|tftp'),
    'kernel': re.compile(r'Kernel|kernel|vmlinuz'),
    'initrd': re.compile(r'initrd|initramfs'),
    'boot': re.compile(r'Booting|booting|Starting'),
    'error': re.compile(r'ERROR|Error|error|failed|Failed'),
}

with open(log_file) as f:
    for i, line in enumerate(f, 1):
        for event, pattern in patterns.items():
            if pattern.search(line):
                print(f"[Line {i}] {event.upper()}: {line.rstrip()}")
EOF

python3 analyze_boot_log.py
```

#### Module Loading Trace

```bash
# Instrument init script to trace module loads
cat > /tmp/initramfs-custom/init << 'EOF'
#!/bin/sh
exec >/dev/console 2>&1

# Enable trace
set -x

mount -t proc proc /proc
mount -t sysfs sysfs /sys

# Trace module loading
for mod in e1000 nfs; do
    echo "[TRACE] Loading module: $mod"
    modprobe $mod
    echo "[TRACE] Module loaded: $mod (exit=$?)"
done

set +x
# Continue with rest of init...
EOF

# Boot with this modified init to see exact sequence
```

### 7.2 Live Debugging (Target Machine)

#### Emergency Shell / Initramfs Break

```bash
# Add kernel parameter to drop to shell in initramfs
# (if init script supports it)

# In pxelinux.cfg/default:
APPEND initrd=/initrd.img root=/dev/nfs ... \
        rd.break break=init

# Or modify init script directly
sed -i 's/^mount -t nfs/exec \/bin\/sh/' /tmp/initramfs-custom/init
```

#### Post-Boot Inspection

```bash
# After OS boots, inspect netboot artifacts
mount | grep nfs       # Check NFS mounts
df -h                 # Disk/mount status
ip addr               # Network config
ip route              # Routing table
cat /proc/cmdline     # Kernel command line

# Check loaded modules
lsmod | grep -E "nfs|e1000|ahci"

# Verify root filesystem
mount | grep "root\|/"
```

---

## 8. Network Boot Flow Debugging

### 8.1 DHCP/TFTP Packet Capture

```bash
# Capture netboot traffic on server side
sudo tcpdump -i eth0 -w netboot.pcap "port 67 or port 68 or port 69"

# Analyze with Wireshark
wireshark netboot.pcap

# Command-line analysis
tshark -r netboot.pcap -Y "dhcp or tftp"

# Filter for specific events
tshark -r netboot.pcap -Y "dhcp.option.vendor_class_id" -T fields -e dhcp.option.vendor_class_id
```

### 8.2 Server-Side Logging

#### TFTP Server Logs

```bash
# Enable TFTP debug logging
sudo systemctl stop tftpd-hpa
sudo /usr/sbin/in.tftpd -vvv -l -u tftp -s /srv/tftp > /tmp/tftp.log 2>&1 &

# Trigger boot, then review
tail -f /tmp/tftp.log

# Expected output:
# RRQ from 192.168.1.100 filename pxelinux.0
# Sending pxelinux.0
# RRQ from 192.168.1.100 filename pxelinux.cfg/01-aa-bb-cc-dd-ee-ff
# ...
```

#### DHCP Server Logs

```bash
# Check ISC DHCP logs
grep "dhcpd" /var/log/syslog | tail -20

# Or from systemd journal
journalctl -u isc-dhcp-server -f

# Filter for specific client
grep "aa:bb:cc:dd:ee:ff" /var/log/syslog
```

### 8.3 Client-Side Tracing

```bash
# From client machine (if accessible via serial console)

# Trace network initialization
dmesg | grep -i "dhcp\|eth\|network"

# Show all loaded modules
lsmod

# Network interface status
ip link show
ip addr show

# DHCP lease info (if using dhclient)
cat /var/lib/dhcp/dhclient.eth0.leases
```

---

## 9. Security Analysis & Threat Modeling

### 9.1 Netboot Attack Surface

```
Potential attack points:

1. DHCP Spoofing
   ├── Attacker sends rogue DHCP response
   ├── Points client to malicious TFTP/bootloader
   └── Mitigation: DHCP snooping, MAC filtering

2. TFTP Man-in-the-Middle
   ├── Intercept TFTP traffic (unencrypted)
   ├── Substitute bootloader, initrd, kernel
   └── Mitigation: TFTP checksum validation, signed images

3. Malicious Bootloader
   ├── Compromised pxelinux.0 or grubx64.efi
   ├── Injects malicious code before OS boot
   └── Mitigation: Secure Boot, measured boot (TPM)

4. Initramfs Tampering
   ├── Modified init script or kernel modules
   ├── Intercepts root filesystem mounting
   └── Mitigation: Cryptographic verification, signed archives

5. SquashFS Substitution
   ├── Attacker provides modified filesystem
   ├── OS runs with injected malicious files
   └── Mitigation: Image checksums, digital signatures
```

### 9.2 Verification Checklist

```bash
#!/bin/bash
# Security verification script

echo "=== Netboot Security Audit ==="

TFTP_DIR="/srv/tftp"

# 1. Check file permissions (should be world-readable for TFTP)
echo "1. File Permissions:"
ls -la "$TFTP_DIR"/pxelinux.0
ls -la "$TFTP_DIR"/grubx64.efi

# 2. Verify checksums
echo "2. File Integrity (MD5):"
md5sum "$TFTP_DIR"/*.0
md5sum "$TFTP_DIR"/*.efi
md5sum "$TFTP_DIR"/vmlinuz*
md5sum "$TFTP_DIR"/initrd*

# 3. Check for suspicious strings in bootloaders
echo "3. Bootloader Strings (audit for tampering):"
strings "$TFTP_DIR"/pxelinux.0 | grep -i "malware\|backdoor\|shell" || echo "Clean"

# 4. Verify module versions match
echo "4. Syslinux Module Versions:"
file "$TFTP_DIR"/*.c32 | sort -u

# 5. Check DHCP configuration
echo "5. DHCP Configuration:"
grep "next-server\|filename" /etc/dhcp/dhcpd.conf

# 6. Analyze pxelinux config
echo "6. PXELINUX Config:"
cat "$TFTP_DIR"/pxelinux.cfg/default | head -20
EOF

chmod +x audit_netboot_security.sh
./audit_netboot_security.sh
```

### 9.3 Signed Boot / Secure Boot

```bash
# Generate signing key (optional, for high-security deployments)
openssl genrsa -out netboot_key.pem 4096
openssl req -new -x509 -key netboot_key.pem -out netboot_cert.pem

# Sign kernel image
pesign -n /etc/pki/pesign/nci-keys \
    -c /etc/pki/pesign/nci-cert \
    -i vmlinuz-myos \
    -o vmlinuz-myos.signed

# Verify Secure Boot status (on UEFI client)
# From client: efivar -l | grep SecureBoot
```

---

## 10. Lab Environment Setup

### 10.1 Complete Lab in VirtualBox/KVM

```bash
#!/bin/bash
# Set up netboot lab environment

LAB_DIR="/tmp/netboot-lab"
mkdir -p "$LAB_DIR"/{tftp,vm,logs}

# 1. Create DHCP + TFTP server (on Linux host)
echo "Setting up server..."

# Copy syslinux files
cp /usr/lib/PXELINUX/pxelinux.0 "$LAB_DIR/tftp/"
cp /usr/lib/syslinux/modules/bios/*.c32 "$LAB_DIR/tftp/"

# Build minimal kernel + initrd (or use existing)
cp /boot/vmlinuz-* "$LAB_DIR/tftp/vmlinuz"
cp /boot/initrd.img-* "$LAB_DIR/tftp/initrd.img"

# Create config
mkdir -p "$LAB_DIR/tftp/pxelinux.cfg"
cat > "$LAB_DIR/tftp/pxelinux.cfg/default" << 'EOF'
DEFAULT vesamenu.c32
PROMPT 0
TIMEOUT 50

MENU TITLE Lab Netboot
LABEL lab
  MENU LABEL Lab OS
  KERNEL /vmlinuz
  APPEND initrd=/initrd.img root=/dev/ram0 console=ttyS0
EOF

# 2. Start DHCP server
echo "Starting DHCP..."
# (setup as described earlier)

# 3. Start TFTP server
echo "Starting TFTP..."
sudo systemctl start tftpd-hpa

# 4. Boot client VM
echo "Starting QEMU client..."
qemu-system-x86_64 \
    -machine pc \
    -m 512 \
    -boot n \
    -net nic,model=e1000 \
    -net user,tftp=$LAB_DIR/tftp,bootfile=pxelinux.0 \
    -serial stdio \
    -nographic &

echo "Lab started in $LAB_DIR"
```

### 10.2 Analysis Workbench

Create a complete analysis environment:

```bash
# Directory structure
~/netboot-analysis/
├── bootloaders/       # pxelinux.0, grubx64.efi
├── configs/          # pxelinux.cfg/default, grub.cfg
├── initramfs-raw/    # Original initramfs files
├── initramfs-extract/ # Extracted contents
├── squashfs-raw/     # Original SquashFS
├── squashfs-extract/  # Extracted contents
├── scripts/          # Analysis & extraction scripts
│   ├── extract_initramfs.sh
│   ├── extract_squashfs.sh
│   ├── audit_netboot_security.sh
│   └── analyze_boot_log.py
└── logs/            # Boot traces, tcpdump, logs

# Quick alias for analysis
alias netboot-analyze='cd ~/netboot-analysis && ls -la'
```

---

## Conclusion

This manual provides a complete toolkit for understanding, analyzing, and debugging netboot infrastructure:

- **Binary analysis**: objdump, strings, hexdump, file type inspection
- **Module inspection**: dependency trees, version checking, compatibility
- **Config parsing**: extraction, validation, parameter analysis
- **Initramfs**: extraction, modification, init script analysis
- **SquashFS**: mount, extract, modify, performance analysis
- **Runtime tracing**: QEMU, serial console, packet capture
- **Security auditing**: attack surface, verification, signed boot

Use these techniques to develop secure, efficient, and maintainable netboot infrastructure for your custom OS deployments.
