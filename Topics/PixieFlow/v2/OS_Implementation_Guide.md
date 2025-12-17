# Complete Custom OS Netboot Implementation Guide

## Table of Contents
1. Building Your Custom OS
2. Creating Bootable Components
3. PXE/UEFI Boot Infrastructure
4. Netboot Process Flow
5. Configuration Files
6. Complete Workflow
7. Testing and Deployment

---

## Part 1: Building Your Custom OS

### Custom OS Structure

```
custom-os/
├── build/
│   ├── kernel/
│   │   ├── src/
│   │   └── build output
│   ├── rootfs/
│   │   ├── bin/
│   │   ├── sbin/
│   │   ├── etc/
│   │   ├── lib/
│   │   ├── usr/
│   │   ├── boot/
│   │   ├── var/
│   │   ├── sys/
│   │   ├── proc/
│   │   ├── dev/
│   │   ├── home/
│   │   └── root/
│   └── initramfs/
├── boot/
│   ├── vmlinuz (kernel image)
│   └── initrd.img
├── iso/
│   ├── isolinux/
│   ├── boot/
│   └── custom-os.iso
└── netboot/
    ├── pxelinux/
    ├── efi/
    └── filesystem images
```

### Building the Kernel

For your custom OS, you'll need to compile a Linux kernel:

```bash
#!/bin/bash
# kernel-build.sh

KERNEL_VERSION="6.1.0"
KERNEL_DIR="/tmp/linux-$KERNEL_VERSION"

# Download kernel source
cd /tmp
wget https://www.kernel.org/releases/linux/v6.x/linux-$KERNEL_VERSION.tar.xz
tar xf linux-$KERNEL_VERSION.tar.xz
cd $KERNEL_DIR

# Create minimal kernel config for netboot
cat > .config << 'EOF'
CONFIG_64BIT=y
CONFIG_X86=y
CONFIG_MODULES=y
CONFIG_NETWORK=y
CONFIG_NET_CORE=y
CONFIG_NETDEVICES=y
CONFIG_NE2K_PCI=m
CONFIG_E1000=m
CONFIG_E1000E=m
CONFIG_R8169=m
CONFIG_VIRTIO_NET=m
CONFIG_EXT4_FS=y
CONFIG_NFS_FS=y
CONFIG_ROOT_NFS=y
CONFIG_UNIX=y
CONFIG_INET=y
CONFIG_MAGIC_SYSRQ=y
CONFIG_PRINTK=y
CONFIG_TMPFS=y
CONFIG_SQUASHFS=y
CONFIG_SQUASHFS_ZSTD=y
CONFIG_DEVTMPFS=y
CONFIG_BLK_DEV_LOOP=y
CONFIG_DM_CRYPT=m
CONFIG_CRYPTO_XTS=m
CONFIG_USB=m
CONFIG_USB_STORAGE=m
CONFIG_AHCI=m
CONFIG_SATA_AHCI=m
CONFIG_MMC=m
CONFIG_MQ_IOSCHED_KYBER=y
EOF

# Build kernel
make -j$(nproc)
make modules

# Install kernel
make INSTALL_PATH=$PWD/boot install
make INSTALL_MOD_PATH=$PWD/modules modules_install

# Output files
ls -la boot/vmlinuz*
ls -la modules/lib/modules/
```

### Building Rootfs

Create a minimal but complete filesystem:

```bash
#!/bin/bash
# rootfs-build.sh

ROOTFS_DIR="./rootfs"
mkdir -p $ROOTFS_DIR

# Create directory structure
for dir in bin sbin lib lib64 etc usr usr/bin usr/sbin var var/log var/cache tmp root home proc sys dev mnt/root boot; do
  mkdir -p $ROOTFS_DIR/$dir
done

# Copy BusyBox (provides many standard utilities)
cp /bin/busybox $ROOTFS_DIR/bin/

cd $ROOTFS_DIR/bin
for cmd in sh ls cat mount umount ip dhclient modprobe insmod rm mv cp mkdir; do
  ln -s busybox $cmd
done
cd /

# Copy essential libraries
LIBS=$(ldd /sbin/init | grep "=>" | awk '{print $3}')
for lib in $LIBS libc.so.6 libm.so.6; do
  [ -f "$lib" ] && cp "$lib" $ROOTFS_DIR/lib64/
done

# Copy kernel modules (compiled earlier)
cp -r ./kernel-build/modules/lib/modules $ROOTFS_DIR/lib/

# Create /etc files
cat > $ROOTFS_DIR/etc/fstab << 'EOF'
# Mount points
proc         /proc        proc    defaults 0 0
sysfs        /sys         sysfs   defaults 0 0
tmpfs        /dev         tmpfs   defaults 0 0
EOF

cat > $ROOTFS_DIR/etc/hostname << 'EOF'
custom-os-node
EOF

cat > $ROOTFS_DIR/etc/resolv.conf << 'EOF'
nameserver 8.8.8.8
nameserver 8.8.4.4
EOF

# Create init script for main OS
cat > $ROOTFS_DIR/sbin/init << 'MAINIT'
#!/bin/sh
mount -t proc proc /proc
mount -t sysfs sysfs /sys
mount -t tmpfs tmpfs /dev
mount -t tmpfs tmpfs /run

# Basic console setup
exec sbin/getty 38400 tty1

MAINIT
chmod +x $ROOTFS_DIR/sbin/init

# Create essential device nodes
mknod $ROOTFS_DIR/dev/console c 5 1
mknod $ROOTFS_DIR/dev/null c 1 3
mknod $ROOTFS_DIR/dev/zero c 1 5
mknod $ROOTFS_DIR/dev/tty c 5 0

echo "Rootfs built at: $ROOTFS_DIR"
```

---

## Part 2: Understanding PXE/UEFI Boot Components

### Legacy BIOS Boot Components

#### **pxelinux.0**

**What it is:** The core PXE bootloader that runs in BIOS mode.

**How it works:**
- BIOS firmware loads this file via PXE ROM on network card
- pxelinux.0 is a 16-bit real-mode program
- It initializes the bootloader, reads configuration
- Loads kernel and initramfs into memory
- Hands control to the kernel

**Technical details:**
```
pxelinux.0 file structure:
- Boot code (16-bit x86 assembly)
- Configuration parser
- File system drivers (TFTP client)
- Memory management
- Kernel/initrd loader

Size: ~64-128 KB
Format: Flat binary executable
```

**Installation:**
```bash
# Copy to TFTP root
cp /usr/lib/syslinux/pxelinux.0 /srv/tftp/

# Create directory structure
mkdir -p /srv/tftp/pxelinux.cfg
```

**Boot flow for pxelinux.0:**
```
BIOS POST
  ↓
Network boot (PXE ROM)
  ↓
DHCP discovery + boot server discovery
  ↓
Download pxelinux.0 via TFTP
  ↓
Load and execute pxelinux.0
  ↓
Read pxelinux.cfg/default (or MAC-specific config)
  ↓
Load kernel image via TFTP
  ↓
Load initrd via TFTP
  ↓
Hand control to kernel with boot parameters
```

---

#### **vesamenu.c32**

**What it is:** A graphical boot menu module for pxelinux with VESA graphics support.

**How it works:**
- Compiled 32-bit module for SYSLINUX/PXELINUX
- Provides a user-friendly boot menu with mouse/keyboard support
- Supports color, graphics, and text rendering
- Communicates with pxelinux.0 via SYSLINUX C32 ABI (Application Binary Interface)

**Technical details:**
```
- Written in C, compiled as COM32 module
- Requires libcom32.c32 and libutil.c32
- Uses VESA video modes for graphics
- Supports menu items, timeouts, and prompts
- Can display images and custom layouts

Size: ~150-250 KB
```

**Features:**
- Visual menu with multiple boot options
- Keyboard and mouse support
- Background images/splash screens
- Default boot selection with countdown
- Menu parameters and layout customization

---

#### **ldlinux.c32**

**What it is:** The "ldlinux" core module that provides core SYSLINUX/PXELINUX functionality when running as COM32 module.

**How it works:**
- Loaded by pxelinux.0 as a COM32 module
- Handles configuration parsing and boot logic
- May be required for certain advanced features
- Some configs chain-load other modules

**Technical details:**
```
- Optional in modern setups
- Required if using certain menu features
- Part of SYSLINUX/PXELINUX suite
- Provides core bootloader functionality in modular form

Size: ~40-80 KB
```

**When needed:**
- Complex menu configurations
- Advanced boot logic
- Chain-loading scenarios

---

#### **libcom32.c32**

**What it is:** A shared library providing the C32 Application Binary Interface (ABI) for COM32 modules.

**How it works:**
- Runtime library for COM32 format programs
- Provides system call interface to pxelinux
- Implements standard library functions (printf, malloc, etc.)
- Allows C-language modules to interact with bootloader

**Technical details:**
```
- Core dependency for all C32 modules
- Provides:
  * Console I/O
  * Memory management
  * File access via bootloader
  * Hardware access (disk, network)
  * Math functions

Size: ~20-50 KB
Dependencies: None (core library)
```

**Function categories:**
```c
// Console operations
void putchar(int c);
int getchar(void);
void printf(const char *fmt, ...);

// Memory
void *malloc(size_t size);
void free(void *ptr);

// File operations
int open(const char *filename, int flags);
int read(int fd, char *buf, int len);
int close(int fd);

// System info
struct biosregs { ... };
int intcall(uint16_t int_no, struct biosregs *regs);
```

---

#### **libutil.c32**

**What it is:** Utility library providing additional functionality for COM32 modules.

**How it works:**
- Extends libcom32.c32 with utility functions
- Provides menu system, UI widgets, and helpers
- Used by vesamenu.c32 and other advanced modules
- Handles graphics rendering, menu logic, input handling

**Technical details:**
```
- Dependency: libcom32.c32
- Provides:
  * Menu/UI rendering
  * Graphics primitives
  * Color management
  * Input handling
  * Key binding

Size: ~30-60 KB
```

**Used by:**
- vesamenu.c32 (graphical menus)
- Simple menu modules
- Advanced boot loaders

---

### UEFI Boot Components

#### **grubx64.efi**

**What it is:** The GRUB 2 bootloader compiled for 64-bit UEFI systems.

**How it works:**
```
UEFI Firmware
  ↓
Looks for EFI System Partition (ESP)
  ↓
Reads EFI boot variables
  ↓
Loads grubx64.efi from ESP
  ↓
GRUB initializes
  ↓
Reads grub.cfg configuration
  ↓
Displays menu or boots default entry
  ↓
Loads kernel + initramfs
  ↓
Hand control to kernel
```

**Technical details:**
```
- 64-bit UEFI PE/COFF executable
- Self-contained bootloader
- Not dependent on libcom32 or other modules
- Can handle FAT32 (ESP requirement)
- Supports various filesystems through plugins

Size: ~1-2 MB
Dependencies: None (fully contained)
Architecture: x86-64 with UEFI calling conventions
```

**Installation (UEFI):**
```bash
# Create ESP (EFI System Partition) if not exists
# Usually mounted at /boot/efi
# Must be FAT32, minimum 100 MB

# Copy GRUB binary
mkdir -p /boot/efi/EFI/BOOT
cp /usr/lib/grub/x86_64-efi/grubx64.efi /boot/efi/EFI/BOOT/

# Or for custom netboot (TFTP)
cp grubx64.efi /srv/tftp/grub/
```

**Advantages over pxelinux for UEFI:**
- Native UEFI support
- Better hardware compatibility
- Support for larger initramfs
- Modern bootloader maintenance
- Can boot from various sources (TFTP, HTTP, local)

---

## Part 3: Configuration Files

### pxelinux Configuration: `/srv/tftp/pxelinux.cfg/default`

**Complete example:**
```
# PXELINUX Configuration for Custom OS Netboot

UI vesamenu.c32
MENU TITLE Custom OS Boot Menu
MENU BACKGROUND /pxelinux/bg.jpg
MENU ROWS 10
MENU COLS 80
TIMEOUT 100
DEFAULT custom-os-install

# Label: Custom OS Install
LABEL custom-os-install
  MENU LABEL Custom OS Live (Netboot)
  KERNEL /boot/vmlinuz-6.1.0
  APPEND root=/dev/nfs nfsroot=192.168.1.1:/export/custom-os \
    ip=dhcp ro console=tty0 console=ttyS0,115200n8 \
    initrd=/boot/initrd-netboot.img
  IPAPPEND 2

# Label: Custom OS Persistent Installation
LABEL custom-os-persistent
  MENU LABEL Custom OS Persistent Root
  KERNEL /boot/vmlinuz-6.1.0
  APPEND root=/dev/nfs nfsroot=192.168.1.1:/export/custom-os-persistent \
    rw ip=dhcp console=tty0 \
    initrd=/boot/initrd-netboot.img

# Label: iSCSI Boot
LABEL custom-os-iscsi
  MENU LABEL Custom OS via iSCSI
  KERNEL /boot/vmlinuz-6.1.0
  APPEND iscsi_initiator=iqn.2024-01.custom-os:client \
    iscsi_target_name=iqn.2024-01.custom-os:target:disk \
    iscsi_target_ip=192.168.1.10 iscsi_target_port=3260 \
    root=/dev/mapper/iscsi-root ip=dhcp rw \
    initrd=/boot/initrd-netboot.img console=tty0

# Label: Local Boot (chainload to local disk)
LABEL localboot
  MENU LABEL Boot from local disk
  LOCALBOOT 0x80

# Label: RAM-based (filesystem.squashfs loaded into RAM)
LABEL custom-os-ramfs
  MENU LABEL Custom OS Live (In-Memory)
  KERNEL /boot/vmlinuz-6.1.0
  APPEND root=/dev/nfs nfsroot=192.168.1.1:/export/custom-os \
    ip=dhcp loop=filesystem.squashfs loopback=iso9660 \
    initrd=/boot/initrd-netboot.img,/boot/filesystem.squashfs \
    console=tty0
  TEXT HELP
    Loads entire OS into RAM memory
  ENDTEXT

# Advanced Options Submenu
LABEL advanced
  MENU LABEL Advanced Options
  KERNEL vesamenu.c32
  APPEND /pxelinux.cfg/advanced.menu

# Diagnostic/Rescue
LABEL diagnostic
  MENU LABEL Diagnostic/Rescue Shell
  KERNEL /boot/vmlinuz-6.1.0
  APPEND root=/dev/nfs nfsroot=192.168.1.1:/export/custom-os \
    ip=dhcp rd.debug rd.shell \
    initrd=/boot/initrd-netboot.img console=tty0
  TEXT HELP
    Boots into shell for debugging
  ENDTEXT

# Hardware Information
LABEL hwinfo
  MENU LABEL Hardware Info (Linux)
  KERNEL /boot/vmlinuz-6.1.0
  APPEND root=/dev/nfs nfsroot=192.168.1.1:/export/custom-os \
    ip=dhcp \
    initrd=/boot/initrd-netboot.img console=tty0

PROMPT 0
ONTIMEOUT custom-os-install
```

**Key Parameters Explained:**
```
UI vesamenu.c32
  → Use graphical menu interface

MENU TITLE Custom OS Boot Menu
  → Title displayed at top

TIMEOUT 100
  → 10 seconds (100 = 10 deciseconds)

DEFAULT custom-os-install
  → Boot this label if timeout

KERNEL /boot/vmlinuz-6.1.0
  → Kernel image path (relative to TFTP root)

APPEND ...
  → Kernel command-line parameters

root=/dev/nfs
  → Use NFS for root filesystem

nfsroot=IP:/path
  → NFS server and export path

ip=dhcp
  → Use DHCP for network configuration

initrd=/boot/initrd-netboot.img
  → Initial ramdisk path

IPAPPEND 2
  → Add kernel parameters from DHCP:
    - IPAPPEND 1: ip=xxx bootserver=xxx
    - IPAPPEND 2: BOOTIF=MAC address
    - IPAPPEND 4: network device info
```

---

### GRUB Configuration: `/boot/grub/grub.cfg` (for UEFI netboot)

**Complete example:**
```bash
# GRUB 2 Configuration for UEFI Netboot

set default="0"
set timeout=10
set gfxmode=1024x768
set gfxpayload=keep

# Load background image
if [ x${feature_platform_search_hint} = xy ]; then
  search --no-floppy --label "BOOT" --set root
else
  search --no-floppy --label "BOOT" --set root
fi

# Load splash image
if [ -f (${root})/grub/splash.png ]; then
  insmod gfxterm
  insmod png
  set theme=(${root})/grub/theme.txt
  export theme
fi

# Main menu entry: Custom OS Live Netboot
menuentry 'Custom OS Live (UEFI Netboot)' {
  set root=(tftp,192.168.1.1)
  
  echo 'Loading Custom OS kernel...'
  linux /boot/vmlinuz-6.1.0 \
    root=/dev/nfs \
    nfsroot=192.168.1.1:/export/custom-os \
    ip=dhcp \
    ro \
    console=tty0 \
    console=ttyS0,115200n8
  
  echo 'Loading initramfs...'
  initrd /boot/initrd-netboot.img
}

# Entry: Persistent NFS Root
menuentry 'Custom OS Persistent (NFS)' {
  set root=(tftp,192.168.1.1)
  
  linux /boot/vmlinuz-6.1.0 \
    root=/dev/nfs \
    nfsroot=192.168.1.1:/export/custom-os-persistent \
    ip=dhcp \
    rw \
    console=tty0
  
  initrd /boot/initrd-netboot.img
}

# Entry: iSCSI Boot
menuentry 'Custom OS via iSCSI' {
  set root=(tftp,192.168.1.1)
  
  linux /boot/vmlinuz-6.1.0 \
    iscsi_initiator=iqn.2024-01.custom-os:client \
    iscsi_target_name=iqn.2024-01.custom-os:target \
    iscsi_target_ip=192.168.1.10 \
    iscsi_target_port=3260 \
    root=/dev/mapper/iscsi-root \
    ip=dhcp \
    rw \
    console=tty0
  
  initrd /boot/initrd-netboot.img
}

# Entry: RAM-based OS (squashfs)
menuentry 'Custom OS Live (In-Memory)' {
  set root=(tftp,192.168.1.1)
  
  echo 'Loading kernel and filesystem into memory...'
  linux /boot/vmlinuz-6.1.0 \
    root=/dev/nfs \
    nfsroot=192.168.1.1:/export/custom-os \
    ip=dhcp \
    loop=filesystem.squashfs \
    loopback=iso9660 \
    console=tty0
  
  echo 'This will load full filesystem into RAM'
  initrd /boot/initrd-netboot.img,/boot/filesystem.squashfs
}

# Entry: Diagnostic/Rescue
menuentry 'Diagnostic Mode (Rescue Shell)' {
  set root=(tftp,192.168.1.1)
  
  linux /boot/vmlinuz-6.1.0 \
    root=/dev/nfs \
    nfsroot=192.168.1.1:/export/custom-os \
    ip=dhcp \
    rd.debug \
    rd.shell \
    console=tty0
  
  initrd /boot/initrd-netboot.img
}

# Entry: Local Boot (if disk present)
menuentry 'Boot from Local Disk' {
  insmod part_msdos
  insmod ext2
  set root=(hd0,msdos1)
  chainloader +1
}

# UEFI Shell (for troubleshooting)
menuentry 'UEFI Shell' {
  insmod part_efi
  chainloader (fw0x0001)
}
```

---

### Initrd Configuration File (dracut-based for netboot)

**`/etc/dracut.conf.d/netboot.conf`:**
```bash
# Dracut netboot configuration

# Netboot-specific modules
add_dracutmodules+=" network nfs dhcp "

# Include these files
add_files+=" /etc/dhcp/dhclient.conf "

# Don't include unnecessary modules
omit_dracutmodules+=" plymouth lvm crypt fcoe multipath "

# Drivers to include
add_drivers+=" e1000 e1000e igb bnx2 bnx2x r8169 virtio_net "

# Filesystem support
add_dracutmodules+=" squash "

# Network boot specific options
hostonly="no"
hostonly_cmdline="no"

# Compression
compress="gzip"

# Early microcode (optional but recommended)
early_microcode="no"

# Output
out="/boot/initrd-netboot.img"
```

**Build netboot initrd:**
```bash
sudo dracut -f --conf /etc/dracut.conf.d/netboot.conf /boot/initrd-netboot.img
```

---

## Part 4: Creating Squashfs Filesystem

### **filesystem.squashfs**

**What it is:** A compressed, read-only filesystem that contains your custom OS.

**Why use it for netboot:**
- Highly compressed (30-50% of original size)
- Fast decompression on boot
- Ideal for network transfer and memory loading
- Perfect for read-only live systems
- All files in single file (easier distribution)

**Technical details:**
```
SquashFS format:
- Inode-based
- Block-based compression
- Multiple compression algorithms (gzip, zstd, xz)
- Read-only filesystem
- Good for embedded/netboot scenarios

Typical compression ratio: 50-70%
```

**Creating squashfs from rootfs:**

```bash
#!/bin/bash
# create-squashfs.sh

ROOTFS_DIR="./rootfs"
OUTPUT="./boot/filesystem.squashfs"

# Basic squashfs creation
mksquashfs $ROOTFS_DIR $OUTPUT \
  -comp zstd \
  -Xcompression-level 22 \
  -b 1048576 \
  -no-xattrs \
  -no-progress

# Verify
ls -lh $OUTPUT
unsquashfs -stat $OUTPUT

echo "SquashFS created: $OUTPUT"
```

**Advanced squashfs (with exclusions and optimization):**

```bash
#!/bin/bash
# create-squashfs-optimized.sh

ROOTFS_DIR="./rootfs"
OUTPUT="./boot/filesystem.squashfs"

# Create exclude file
cat > /tmp/squash-exclude << 'EOF'
.git*
*.tmp
var/log/*
var/cache/*
tmp/*
*.pyc
__pycache__
.cache
.local
EOF

# Create optimized squashfs
mksquashfs $ROOTFS_DIR $OUTPUT \
  -comp zstd \
  -Xcompression-level 22 \
  -b 1048576 \
  -no-xattrs \
  -no-progress \
  -excludes /tmp/squash-exclude \
  -wildcards \
  -threads $(nproc)

# Add to boot directory for netboot
cp $OUTPUT /srv/tftp/boot/filesystem.squashfs

echo "Optimized SquashFS: $OUTPUT"
echo "Size: $(du -h $OUTPUT | cut -f1)"
```

**SquashFS with overlay (for persistence):**

When using squashfs in live systems, often you want a writable overlay:

```bash
# At boot time (handled by initrd):
mount -t tmpfs tmpfs /mnt/overlay

# Mount squashfs
mount -o loop filesystem.squashfs /mnt/roottmp

# Create overlay layers
mkdir -p /mnt/upper /mnt/work /mnt/merged

# Use overlayfs for writable layer
mount -t overlay overlay \
  -o lowerdir=/mnt/roottmp,upperdir=/mnt/upper,workdir=/mnt/work \
  /mnt/merged

# This gives you:
# - Read-only base from squashfs
# - Writable overlay in RAM
# - Changes lost on reboot (live behavior)
```

---

## Part 5: Complete Netboot Directory Structure

```
TFTP Root: /srv/tftp/

/srv/tftp/
│
├── pxelinux.0                      # BIOS PXE bootloader
├── ldlinux.c32                     # SYSLINUX module (optional)
│
├── pxelinux.cfg/
│   ├── default                     # Main pxelinux config
│   ├── advanced.menu               # Advanced options submenu
│   ├── 01-aa-bb-cc-dd-ee-ff        # MAC-specific config (optional)
│   └── README                      # Documentation
│
├── boot/
│   ├── vmlinuz-6.1.0               # Kernel image
│   ├── initrd-netboot.img          # Initramfs for netboot
│   ├── filesystem.squashfs         # Compressed rootfs
│   └── CHECKSUM                    # Integrity check
│
├── grub/
│   ├── grubx64.efi                 # UEFI bootloader (64-bit)
│   ├── grub.cfg                    # GRUB configuration
│   ├── i386-pc/ or x86_64-efi/    # GRUB modules (optional)
│   ├── splash.png                  # Background image
│   └── theme.txt                   # GRUB theme
│
├── pxelinux/
│   ├── vesamenu.c32                # Graphical menu module
│   ├── libcom32.c32                # COM32 library
│   ├── libutil.c32                 # Utility library
│   ├── bg.jpg                      # Menu background
│   └── font.psf                    # Font file
│
├── efi/
│   ├── BOOT/
│   │   └── BOOTX64.EFI             # UEFI bootloader (name for EFI firmware)
│   └── custom-os/
│       └── grubx64.efi             # Alternative UEFI location
│
├── images/
│   ├── splash.png                  # Splash screen
│   ├── logo.png                    # Logo images
│   └── README
│
└── config/
    ├── dhcp.conf                   # DHCP server config
    ├── nfs-exports                 # NFS exports
    ├── README.SETUP               # Setup instructions
    └── CHANGELOG                   # Version history

Additional servers needed:

DHCP Server (dnsmasq or ISC-DHCP):
  - Serves IP addresses
  - Points to boot servers and files
  - PXE option codes (66, 67)

NFS Server (if using NFS root):
  - Exports /custom-os directory
  - Exports /custom-os-persistent
  - Read-only or read-write depending on use case

HTTP Server (optional):
  - Alternative to TFTP for kernel/initrd
  - Faster on high-latency links
  - GRUB native support

Serial Console (optional):
  - Capture boot logs
  - Troubleshooting over network
```

---

## Part 6: Complete Boot Flow Diagram

### BIOS/PXE Boot Flow

```
┌─────────────────────────────────────┐
│ 1. Client Machine Powers On         │
│ - BIOS runs POST                    │
│ - Network card PXE ROM loaded       │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│ 2. DHCP Discovery                   │
│ - DHCP Request broadcast            │
│ - Server responds with:             │
│   * IP address                      │
│   * Gateway                         │
│   * DNS servers                     │
│   * Boot server (option 66)         │
│   * Boot file (option 67)           │
│     → pxelinux.0                    │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│ 3. Download pxelinux.0              │
│ - TFTP download from boot server    │
│ - File: /srv/tftp/pxelinux.0        │
│ - Loaded to memory address 0x7C00   │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│ 4. Execute pxelinux.0               │
│ - Real-mode 16-bit x86 code         │
│ - Initializes bootloader            │
│ - Sets up memory and hardware       │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│ 5. Load pxelinux Configuration      │
│ - Tries: pxelinux.cfg/01-MAC-ADDR   │
│ - Falls back to: pxelinux.cfg/default
│ - Parses menu structure             │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│ 6. Display Boot Menu                │
│ - Load vesamenu.c32 (optional)      │
│ - Display boot options              │
│ - Wait for user selection or timeout│
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│ 7. Load Kernel and Initramfs        │
│ - TFTP: /boot/vmlinuz-6.1.0         │
│ - TFTP: /boot/initrd-netboot.img    │
│ - Load to high memory               │
│ - Prepare boot parameters           │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│ 8. Hand Control to Kernel           │
│ - Switch to protected mode          │
│ - 32/64-bit execution               │
│ - Pass command-line parameters      │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│ 9. Kernel Initialization            │
│ - Decompress initramfs              │
│ - Mount initramfs as root (/)       │
│ - Execute /init script              │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│ 10. Initramfs /init Script          │
│  a) Mount /sys and /proc            │
│  b) Load network drivers (modprobe) │
│  c) Initialize network interface    │
│  d) Configure IP (DHCP)             │
│  e) Mount NFS root filesystem       │
│  f) Perform pivot_root              │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│ 11. Real OS Initialization          │
│ - Execute /sbin/init (systemd)      │
│ - Load system services              │
│ - User shell/login prompt           │
└─────────────────────────────────────┘
```

### UEFI Boot Flow

```
┌─────────────────────────────────────┐
│ 1. Client Powers On (UEFI Firmware) │
│ - UEFI POST runs                    │
│ - Loads boot variables              │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│ 2. DHCP/Boot Server Discovery       │
│ - IPv4 boot protocol or IPv6        │
│ - Discovers boot server URL         │
│ - Typically: tftp://server/         │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│ 3. Download grubx64.efi             │
│ - TFTP or HTTP from boot server     │
│ - File: /boot/grubx64.efi           │
│ - PE/COFF format (UEFI executable)  │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│ 4. Execute grubx64.efi              │
│ - 64-bit UEFI code                  │
│ - Initializes GRUB bootloader       │
│ - Sets up graphics/console          │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│ 5. Load grub.cfg Configuration      │
│ - TFTP: /boot/grub/grub.cfg         │
│ - Parses menu entries               │
│ - Sets default boot entry           │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│ 6. Display GRUB Menu                │
│ - Graphics support (if configured)  │
│ - Boot options                      │
│ - Timeout/default selection         │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│ 7. Load Kernel and Initramfs        │
│ - TFTP: /boot/vmlinuz-6.1.0         │
│ - TFTP: /boot/initrd-netboot.img    │
│ - Allocate memory buffers           │
│ - Verify checksums (optional)       │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│ 8. Hand Control to Kernel           │
│ - Switch from UEFI mode             │
│ - 64-bit execution                  │
│ - Pass command-line and boot params │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│ 9-11. Same as BIOS flow             │
│ (Kernel initialization onwards)     │
└─────────────────────────────────────┘
```

---

## Part 7: Server Setup for Netboot

### DHCP Configuration (dnsmasq)

**`/etc/dnsmasq.conf`:**
```conf
# DHCP Configuration for PXE/Netboot

# DHCP range
dhcp-range=192.168.1.100,192.168.1.254,255.255.255.0,12h

# Gateway
dhcp-option=3,192.168.1.1

# DNS servers
dhcp-option=6,8.8.8.8,8.8.4.4

# NTP servers
dhcp-option=42,time.nist.gov

# BIOS PXE boot
dhcp-option=66,192.168.1.1          # Boot server (TFTP server)
dhcp-option=67,pxelinux.0            # Boot filename

# UEFI PXE boot
dhcp-match=set:efi-x86_64,option:client-arch,7  # UEFI x86-64
dhcp-boot=tag:efi-x86_64,grubx64.efi,192.168.1.1

# TFTP configuration
enable-tftp
tftp-root=/srv/tftp
tftp-port=69

# Logging
log-queries
log-dhcp
log-facility=/var/log/dnsmasq.log

# Interface binding
interface=eth0
bind-dynamic
```

**Alternative: ISC DHCP Server**

**`/etc/dhcp/dhcpd.conf`:**
```
subnet 192.168.1.0 netmask 255.255.255.0 {
  option routers 192.168.1.1;
  option domain-name-servers 8.8.8.8, 8.8.4.4;
  option ntp-servers time.nist.gov;
  
  # IP range
  range 192.168.1.100 192.168.1.254;
  
  # PXE boot for BIOS
  next-server 192.168.1.1;
  filename "pxelinux.0";
  
  # UEFI-specific (using class)
  class "uefi-x86_64" {
    match if option client-architecture-type = 7;
    filename "grubx64.efi";
  }
}
```

### NFS Server Configuration

**`/etc/exports`:**
```
# NFS exports for netboot

# Custom OS live (read-only)
/export/custom-os 192.168.1.0/24(ro,no_root_squash,insecure)

# Persistent custom OS (read-write)
/export/custom-os-persistent 192.168.1.0/24(rw,no_root_squash,insecure)

# Shared home directory
/export/home 192.168.1.0/24(rw,no_root_squash,insecure)
```

**Setup commands:**
```bash
# Create export directories
sudo mkdir -p /export/custom-os
sudo mkdir -p /export/custom-os-persistent

# Copy rootfs
sudo cp -r ./rootfs/* /export/custom-os/

# Make persistent writable
sudo chmod 755 /export/custom-os-persistent

# Reload exports
sudo exportfs -ra

# Verify
showmount -e localhost
```

### TFTP Server Setup

**Using dnsmasq (easiest):**
- Already shown in dnsmasq config above

**Or using tftpd-hpa:**

**`/etc/default/tftpd-hpa`:**
```
TFTP_USERNAME="tftp"
TFTP_DIRECTORY="/srv/tftp"
TFTP_ADDRESS="0.0.0.0:69"
TFTP_OPTIONS="--secure --permissive -vvv"
```

**File layout:**
```bash
mkdir -p /srv/tftp/{pxelinux,pxelinux.cfg,boot,grub,efi,images}

# Copy files
cp /usr/lib/syslinux/pxelinux.0 /srv/tftp/
cp /usr/lib/syslinux/vesamenu.c32 /srv/tftp/pxelinux/
cp /usr/lib/syslinux/libcom32.c32 /srv/tftp/pxelinux/
cp /usr/lib/syslinux/libutil.c32 /srv/tftp/pxelinux/

# Copy custom OS files
cp ./build/kernel /srv/tftp/boot/vmlinuz-6.1.0
cp ./build/initrd-netboot.img /srv/tftp/boot/
cp ./build/filesystem.squashfs /srv/tftp/boot/

# GRUB files (for UEFI)
cp /usr/lib/grub/x86_64-efi/grubx64.efi /srv/tftp/grub/
```

---

## Part 8: Complete Netboot Setup Script

**`setup-netboot-environment.sh`:**

```bash
#!/bin/bash
# Complete netboot infrastructure setup for Custom OS

set -e

TFTP_ROOT="/srv/tftp"
NFS_EXPORT="/export"
CUSTOM_OS_DIR="./custom-os-build"
SERVER_IP="192.168.1.1"

echo "[*] Setting up Custom OS Netboot Environment"

# 1. Create directory structure
echo "[1] Creating directory structure..."
mkdir -p $TFTP_ROOT/{pxelinux,pxelinux.cfg,boot,grub/x86_64-efi,efi/BOOT,images}
mkdir -p $NFS_EXPORT/custom-os
mkdir -p $NFS_EXPORT/custom-os-persistent

# 2. Copy BIOS/UEFI bootloaders
echo "[2] Installing bootloaders..."
cp /usr/lib/syslinux/pxelinux.0 $TFTP_ROOT/
cp /usr/lib/syslinux/vesamenu.c32 $TFTP_ROOT/pxelinux/
cp /usr/lib/syslinux/libcom32.c32 $TFTP_ROOT/pxelinux/
cp /usr/lib/syslinux/libutil.c32 $TFTP_ROOT/pxelinux/

cp /usr/lib/grub/x86_64-efi/grubx64.efi $TFTP_ROOT/grub/
cp /usr/lib/grub/x86_64-efi/grubx64.efi $TFTP_ROOT/efi/BOOT/BOOTX64.EFI

# 3. Copy kernel and initramfs
echo "[3] Copying kernel and initramfs..."
cp $CUSTOM_OS_DIR/boot/vmlinuz-6.1.0 $TFTP_ROOT/boot/
cp $CUSTOM_OS_DIR/boot/initrd-netboot.img $TFTP_ROOT/boot/
cp $CUSTOM_OS_DIR/boot/filesystem.squashfs $TFTP_ROOT/boot/

# 4. Copy rootfs to NFS
echo "[4] Installing NFS root filesystem..."
sudo cp -r $CUSTOM_OS_DIR/rootfs/* $NFS_EXPORT/custom-os/
sudo chmod -R 755 $NFS_EXPORT/custom-os

# 5. Create PXELINUX config
echo "[5] Creating PXELINUX configuration..."
cat > $TFTP_ROOT/pxelinux.cfg/default << 'PXEEOF'
DEFAULT vesamenu.c32
PROMPT 0
TIMEOUT 100
UI vesamenu.c32
MENU TITLE Custom OS Boot Menu

LABEL custom-os
  MENU LABEL Custom OS Live (Netboot)
  KERNEL /boot/vmlinuz-6.1.0
  APPEND root=/dev/nfs nfsroot=192.168.1.1:/export/custom-os \
    ip=dhcp ro console=tty0 initrd=/boot/initrd-netboot.img
  IPAPPEND 2

LABEL localboot
  MENU LABEL Boot from local disk
  LOCALBOOT 0x80
PXEEOF

# 6. Create GRUB config
echo "[6] Creating GRUB configuration..."
cat > $TFTP_ROOT/grub/grub.cfg << 'GRUBEOF'
set default="0"
set timeout=10

menuentry 'Custom OS Live (UEFI)' {
  set root=(tftp,192.168.1.1)
  linux /boot/vmlinuz-6.1.0 root=/dev/nfs \
    nfsroot=192.168.1.1:/export/custom-os ip=dhcp ro console=tty0
  initrd /boot/initrd-netboot.img
}

menuentry 'Boot from Local Disk' {
  chainloader +1
}
GRUBEOF

# 7. Setup NFS exports
echo "[7] Configuring NFS..."
sudo tee /etc/exports > /dev/null << NFSEOF
$NFS_EXPORT/custom-os 192.168.1.0/24(ro,no_root_squash,insecure)
$NFS_EXPORT/custom-os-persistent 192.168.1.0/24(rw,no_root_squash,insecure)
NFSEOF

sudo exportfs -ra

# 8. Configure and start services
echo "[8] Starting services..."

# DHCP (dnsmasq)
sudo systemctl start dnsmasq
sudo systemctl enable dnsmasq

# NFS
sudo systemctl start nfs-server
sudo systemctl enable nfs-server

# TFTP (tftpd-hpa)
sudo systemctl start tftpd-hpa
sudo systemctl enable tftpd-hpa

echo "[✓] Custom OS Netboot Environment Ready!"
echo ""
echo "Server Details:"
echo "  TFTP Root: $TFTP_ROOT"
echo "  NFS Root: $NFS_EXPORT/custom-os"
echo "  Server IP: $SERVER_IP"
echo ""
echo "Next steps:"
echo "  1. Boot client via PXE (BIOS) or UEFI network boot"
echo "  2. Select 'Custom OS Live' from menu"
echo "  3. Watch boot progress in console"
```

---

## Part 9: Testing and Troubleshooting

### Test Boot Flow (with qemu)

```bash
#!/bin/bash
# Test netboot with QEMU

TFTP_ROOT="/srv/tftp"
SERVER_IP="192.168.1.1"

echo "[*] Starting QEMU netboot test..."

# BIOS/Legacy Boot
qemu-system-x86_64 \
  -m 2048 \
  -enable-kvm \
  -bios /usr/share/ovmf/OVMF.fd \
  -net nic,model=e1000 \
  -net user,tftp=$TFTP_ROOT,bootfile=pxelinux.0 \
  -boot n \
  -nographic \
  -serial stdio

# UEFI Boot
# qemu-system-x86_64 \
#   -m 2048 \
#   -enable-kvm \
#   -bios /usr/share/ovmf/OVMF.fd \
#   -net nic,model=e1000 \
#   -net user,tftp=$TFTP_ROOT \
#   -boot n \
#   -nographic \
#   -serial stdio
```

### Boot Log Analysis

Common issues and logs:

```
# Issue: DHCP not working
- Check: dnsmasq/DHCP server running
- Log: sudo journalctl -u dnsmasq -n 50
- Fix: Verify network interface binding

# Issue: pxelinux.0 not found
- Check: File exists in TFTP root
- Fix: chmod 644 /srv/tftp/pxelinux.0
- Test: echo "" | nc -u 127.0.0.1 69

# Issue: Kernel timeout
- Check: TFTP transfer speed
- Fix: Monitor packet loss, verify network
- Log: tcpdump -i eth0 -nn port 69

# Issue: NFS mount fails
- Check: /etc/exports and exportfs -ra
- Fix: Verify client IP in range
- Log: tail -f /var/log/nfs*

# Issue: initramfs broken
- Test: gunzip < initrd | cpio -t | head -20
- Fix: Rebuild with correct dracut config
```

---

## Summary: Custom OS Netboot Checklist

- [ ] Kernel compiled with netboot drivers
- [ ] Rootfs created with essential utilities
- [ ] Initramfs built with network modules
- [ ] Squashfs filesystem created and compressed
- [ ] TFTP files copied and permissions set
- [ ] PXELINUX config created
- [ ] GRUB config created
- [ ] NFS exports configured
- [ ] DHCP/dnsmasq configured
- [ ] Services started and enabled
- [ ] Test boot in QEMU successful
- [ ] Test boot on real hardware successful
- [ ] Boot logs captured for debugging
- [ ] Performance optimized
- [ ] Documentation created for deployment team