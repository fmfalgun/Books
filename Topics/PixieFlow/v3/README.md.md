# Deep Dive into initrd: From Basics to Netboot

## Table of Contents
1. [Introduction to initrd](#introduction)
2. [Why initrd Exists](#why-initrd)
3. [initrd vs initramfs](#initrd-vs-initramfs)
4. [Boot Process with initrd](#boot-process)
5. [Internal Structure](#internal-structure)
6. [Creating initrd from Scratch](#creating-initrd)
7. [Customizing for Netboot](#netboot-customization)
8. [Advanced Techniques](#advanced-techniques)
9. [Debugging and Troubleshooting](#debugging)

---

## 1. Introduction to initrd {#introduction}

**initrd** (Initial RAM Disk) is a temporary root filesystem loaded into memory during the Linux boot process. It contains essential tools, drivers, and scripts needed to mount the real root filesystem and transition to it.

### Key Concepts
- **Temporary filesystem**: Lives only in RAM during early boot
- **Bridge**: Connects bootloader to the actual root filesystem
- **Modular**: Allows kernel to be smaller by loading drivers on-demand
- **Essential for**: Network booting, encrypted disks, LVM, RAID, and complex storage configurations

---

## 2. Why initrd Exists {#why-initrd}

### The Chicken-and-Egg Problem

The kernel needs to:
1. Mount the root filesystem (/)
2. But the root filesystem might be on:
   - Network storage (NFS, iSCSI)
   - Encrypted partitions (LUKS)
   - LVM or RAID arrays
   - USB drives or other modules not compiled into kernel

The kernel would need drivers for all possible storage configurations compiled in, making it enormous.

### Solution: initrd

The initrd provides a minimal environment that:
- Contains necessary kernel modules and drivers
- Runs initialization scripts
- Sets up networking, decryption, volume management
- Mounts the real root filesystem
- Pivots to the real root and continues boot

---

## 3. initrd vs initramfs {#initrd-vs-initramfs}

### initrd (Legacy)
- Block device (loop-mounted filesystem image)
- Requires filesystem driver in kernel
- Fixed size
- Uses /linuxrc script

### initramfs (Modern)
- CPIO archive extracted directly into RAM
- No filesystem driver needed
- Dynamic size (grows as needed)
- Uses /init script
- **Most modern systems use initramfs but still call it "initrd"**

For this guide, we'll focus on **initramfs** as it's the current standard.

---

## 4. Boot Process with initrd {#boot-process}

### Complete Boot Sequence

```
1. BIOS/UEFI
   └─> Loads bootloader (GRUB/iPXE)
       └─> Bootloader loads kernel + initrd into RAM
           └─> Kernel decompresses itself
               └─> Kernel extracts initramfs to rootfs
                   └─> Kernel executes /init
                       └─> Init script runs (custom logic here)
                           ├─> Load modules
                           ├─> Setup networking (for netboot)
                           ├─> Mount real root filesystem
                           └─> exec switch_root /real_root /sbin/init
                               └─> Real system init (systemd/sysvinit)
```

### Netboot Specific Flow

```
PXE/iPXE Firmware
└─> DHCP request (gets IP, TFTP server, boot file)
    └─> Download kernel via TFTP/HTTP
        └─> Download initrd via TFTP/HTTP
            └─> Boot kernel with initrd
                └─> initrd /init script:
                    ├─> Configure network
                    ├─> Mount NFS/iSCSI root
                    └─> Switch to network root
```

---

## 5. Internal Structure {#internal-structure}

### Standard Directory Layout

```
initrd/
├── init                    # Main init script (executable)
├── bin/                    # Essential binaries
│   ├── sh                  # Shell (busybox or bash)
│   ├── mount
│   ├── umount
│   └── switch_root
├── sbin/
│   ├── modprobe
│   └── ip
├── lib/                    # Shared libraries
│   ├── ld-linux.so.2
│   └── libc.so.6
├── lib/modules/            # Kernel modules
│   └── 5.15.0/
│       ├── kernel/
│       │   ├── drivers/
│       │   └── net/
│       └── modules.dep
├── etc/                    # Configuration
│   ├── fstab
│   └── modprobe.d/
├── dev/                    # Device nodes
│   ├── console
│   └── null
├── proc/                   # Empty (mounted at runtime)
├── sys/                    # Empty (mounted at runtime)
├── run/                    # Runtime data
└── scripts/                # Helper scripts
    └── init-bottom/
```

### The /init Script

This is the heart of initrd. It's the first process (PID 1) that runs:

```bash
#!/bin/sh
# Minimal init script example

# Mount essential filesystems
mount -t proc proc /proc
mount -t sysfs sysfs /sys
mount -t devtmpfs devtmpfs /dev

# Load necessary modules
modprobe e1000  # Network driver

# Setup networking for netboot
ip link set eth0 up
ip addr add 192.168.1.100/24 dev eth0
ip route add default via 192.168.1.1

# Mount NFS root
mkdir -p /real_root
mount -t nfs 192.168.1.50:/export/root /real_root

# Switch to real root
exec switch_root /real_root /sbin/init
```

---

## 6. Creating initrd from Scratch {#creating-initrd}

### Method 1: Manual Creation (Educational)

```bash
#!/bin/bash
# Build directory structure
mkdir -p initrd/{bin,sbin,etc,proc,sys,dev,lib,lib64,run,real_root}

# Copy essential binaries (using busybox for minimal size)
cp /bin/busybox initrd/bin/
cd initrd/bin
for cmd in sh mount umount ls cat; do
    ln -s busybox $cmd
done
cd ../..

# Copy necessary libraries
cp /lib/x86_64-linux-gnu/ld-linux-x86-64.so.2 initrd/lib64/
cp /lib/x86_64-linux-gnu/libc.so.6 initrd/lib/x86_64-linux-gnu/

# Copy kernel modules
mkdir -p initrd/lib/modules/$(uname -r)
cp -r /lib/modules/$(uname -r)/kernel/drivers/net initrd/lib/modules/$(uname -r)/
depmod -b initrd $(uname -r)

# Create init script
cat > initrd/init << 'EOF'
#!/bin/sh
mount -t proc proc /proc
mount -t sysfs sysfs /sys
mount -t devtmpfs devtmpfs /dev

# Your custom boot logic here

exec /bin/sh  # Drop to shell for testing
EOF

chmod +x initrd/init

# Create device nodes
mknod -m 600 initrd/dev/console c 5 1
mknod -m 666 initrd/dev/null c 1 3

# Package into cpio archive
cd initrd
find . | cpio -o -H newc | gzip > ../custom-initrd.img
cd ..
```

### Method 2: Using mkinitramfs (Debian/Ubuntu)

```bash
# Generate for current kernel
mkinitramfs -o /boot/initrd.img-custom $(uname -r)

# Extract and examine
mkdir extracted
cd extracted
zcat /boot/initrd.img-custom | cpio -idmv

# Modify as needed
# ... make changes ...

# Repackage
find . | cpio -o -H newc | gzip > /boot/initrd.img-modified
```

### Method 3: Using dracut (RHEL/Fedora)

```bash
# Generate with specific modules
dracut --force --add "network nfs" /boot/initrd-netboot.img $(uname -r)

# Add custom script
cat > /etc/dracut.conf.d/netboot.conf << EOF
add_dracutmodules+=" network nfs "
kernel_cmdline="ip=dhcp root=nfs:192.168.1.50:/export/root"
EOF

dracut --force --kver $(uname -r)
```

---

## 7. Customizing for Netboot {#netboot-customization}

### Network Boot Requirements

Your initrd needs:
1. Network drivers (e1000, virtio_net, etc.)
2. Network configuration tools (ip, ifconfig, dhclient)
3. Network filesystem support (NFS client, iSCSI initiator)
4. Optional: Dropbear SSH for remote debugging

### Complete Netboot Init Script

```bash
#!/bin/sh
# Advanced netboot init script

echo "Starting netboot initrd..."

# Mount pseudo-filesystems
mount -t proc proc /proc
mount -t sysfs sysfs /sys
mount -t devtmpfs devtmpfs /dev
mkdir -p /dev/pts
mount -t devpts devpts /dev/pts

# Parse kernel command line
for param in $(cat /proc/cmdline); do
    case "$param" in
        ip=*)
            IP_CONFIG="${param#ip=}"
            ;;
        nfsroot=*)
            NFS_ROOT="${param#nfsroot=}"
            ;;
        netboot.debug)
            DEBUG=1
            ;;
    esac
done

# Debug mode: start shell
if [ "$DEBUG" = "1" ]; then
    echo "Debug mode enabled. Starting shell..."
    exec /bin/sh
fi

# Load network modules
echo "Loading network drivers..."
modprobe e1000
modprobe virtio_net
modprobe 8021q  # VLAN support

# Configure network
echo "Configuring network..."
if [ "$IP_CONFIG" = "dhcp" ]; then
    # Use DHCP
    ip link set eth0 up
    udhcpc -i eth0 -s /bin/udhcpc.script
else
    # Static IP: ip=192.168.1.100::192.168.1.1:255.255.255.0
    IFS=':' read -r IP SERVER GATEWAY NETMASK <<EOF
$IP_CONFIG
EOF
    ip addr add $IP/$NETMASK dev eth0
    ip link set eth0 up
    ip route add default via $GATEWAY
fi

# Wait for network
echo "Waiting for network..."
for i in $(seq 1 30); do
    if ip route get 8.8.8.8 >/dev/null 2>&1; then
        break
    fi
    sleep 1
done

# Mount NFS root
echo "Mounting NFS root from $NFS_ROOT..."
mkdir -p /real_root
mount -t nfs -o nolock,ro $NFS_ROOT /real_root

if [ $? -ne 0 ]; then
    echo "ERROR: Failed to mount NFS root!"
    exec /bin/sh
fi

# Cleanup
umount /dev/pts
umount /dev
umount /sys
umount /proc

# Switch to real root
echo "Switching to real root filesystem..."
exec switch_root /real_root /sbin/init

# If we get here, something went wrong
echo "ERROR: switch_root failed!"
exec /bin/sh
```

### Kernel Command Line Parameters

When booting, pass these parameters:

```
# DHCP + NFS
ip=dhcp nfsroot=192.168.1.50:/export/root

# Static IP + NFS
ip=192.168.1.100::192.168.1.1:255.255.255.0 nfsroot=192.168.1.50:/export/root

# Debug mode
netboot.debug

# Complete example
linux /vmlinuz ip=dhcp nfsroot=192.168.1.50:/export/root console=tty0 console=ttyS0,115200n8
```

---

## 8. Advanced Techniques {#advanced-techniques}

### Adding Dropbear SSH for Remote Debugging

```bash
# In your initrd build process
cp /usr/sbin/dropbear initrd/sbin/
cp -r /etc/dropbear initrd/etc/

# Add to init script (before mounting root)
echo "Starting SSH server..."
mkdir -p /var/run
dropbear -E -p 22 -r /etc/dropbear/dropbear_rsa_host_key

# Generate host key if needed
dropbearkey -t rsa -f /etc/dropbear/dropbear_rsa_host_key
```

### Supporting Multiple Boot Sources

```bash
# Try multiple root sources in order
for root_source in \
    "nfs:192.168.1.50:/export/root1" \
    "nfs:192.168.1.51:/export/root2" \
    "iscsi:192.168.1.100::3260"; do
    
    case "$root_source" in
        nfs:*)
            NFS_PATH="${root_source#nfs:}"
            if mount -t nfs $NFS_PATH /real_root 2>/dev/null; then
                break
            fi
            ;;
        iscsi:*)
            # iSCSI mount logic
            ;;
    esac
done
```

### Caching/Overlay Filesystem

```bash
# Use overlayfs to cache NFS root locally
mount -t nfs $NFS_ROOT /nfs_root
mount -t tmpfs tmpfs /overlay
mkdir -p /overlay/upper /overlay/work
mount -t overlay overlay \
    -o lowerdir=/nfs_root,upperdir=/overlay/upper,workdir=/overlay/work \
    /real_root
```

### Firmware Loading

```bash
# Copy firmware to initrd
mkdir -p initrd/lib/firmware
cp -r /lib/firmware/yourdevice.bin initrd/lib/firmware/

# In init script, ensure firmware is loaded
modprobe -d /lib/modules/$(uname -r) your_driver
```

---

## 9. Debugging and Troubleshooting {#debugging}

### Common Issues and Solutions

#### Issue 1: "Kernel panic - not syncing: No init found"
**Cause**: /init script missing or not executable
**Solution**:
```bash
# Verify init exists and is executable
ls -l initrd/init
chmod +x initrd/init

# Ensure it has correct shebang
head -1 initrd/init  # Should be #!/bin/sh
```

#### Issue 2: "Failed to mount NFS root"
**Debugging steps**:
```bash
# Add to init script before NFS mount
echo "Testing network connectivity..."
ping -c 3 192.168.1.50
echo "Testing NFS server..."
showmount -e 192.168.1.50
```

#### Issue 3: Missing kernel modules
**Solution**:
```bash
# List dependencies for a module
modprobe --show-depends e1000

# Include all dependencies in initrd
cp --parents /lib/modules/$(uname -r)/kernel/drivers/net/ethernet/intel/e1000/*.ko initrd/
```

### Debug Shell

Add this to your init script for interactive debugging:

```bash
debug_shell() {
    echo "=== Debug Shell ==="
    echo "Available commands: mount, ip, lsmod, cat, etc."
    echo "Exit with Ctrl+D to continue boot"
    /bin/sh
}

# Call it at strategic points
debug_shell

# Or check kernel cmdline
if grep -q "debug" /proc/cmdline; then
    debug_shell
fi
```

### Logging

```bash
# Redirect all output to log file
exec > /run/initrd.log 2>&1
set -x  # Enable command tracing

# Later, this log can be accessed from real root
# at /run/initramfs/initrd.log
```

### Testing in QEMU

```bash
# Test your initrd without rebooting
qemu-system-x86_64 \
    -kernel /boot/vmlinuz \
    -initrd /boot/custom-initrd.img \
    -append "console=ttyS0 debug" \
    -nographic \
    -m 512M
```

---

## Practical Example: Complete Netboot Setup

### Server Side (NFS/TFTP)

```bash
# Install services
apt-get install nfs-kernel-server tftpd-hpa

# Setup NFS export
mkdir -p /export/root
debootstrap focal /export/root
echo "/export/root 192.168.1.0/24(ro,sync,no_root_squash,no_subtree_check)" >> /etc/exports
exportfs -ra

# Setup TFTP
cp /boot/vmlinuz-$(uname -r) /var/lib/tftpboot/vmlinuz
cp custom-initrd.img /var/lib/tftpboot/initrd.img
```

### Client Side (PXE Config)

```
# /var/lib/tftpboot/pxelinux.cfg/default
DEFAULT netboot
LABEL netboot
    KERNEL vmlinuz
    APPEND initrd=initrd.img ip=dhcp nfsroot=192.168.1.50:/export/root console=tty0
```

### Build Script

```bash
#!/bin/bash
# complete-netboot-initrd.sh

set -e

INITRD_DIR="initrd-build"
KERNEL_VER=$(uname -r)

rm -rf $INITRD_DIR
mkdir -p $INITRD_DIR/{bin,sbin,etc,lib,lib64,proc,sys,dev,run,real_root}

# Copy busybox
cp /bin/busybox $INITRD_DIR/bin/
for cmd in sh mount umount ip cat ls grep sed; do
    ln -sf busybox $INITRD_DIR/bin/$cmd
done

# Copy libraries
cp /lib/x86_64-linux-gnu/ld-linux-x86-64.so.2 $INITRD_DIR/lib64/
cp /lib/x86_64-linux-gnu/libc.so.6 $INITRD_DIR/lib/x86_64-linux-gnu/

# Copy network modules
mkdir -p $INITRD_DIR/lib/modules/$KERNEL_VER
cp -r /lib/modules/$KERNEL_VER/kernel/drivers/net $INITRD_DIR/lib/modules/$KERNEL_VER/kernel/
cp -r /lib/modules/$KERNEL_VER/kernel/fs/nfs* $INITRD_DIR/lib/modules/$KERNEL_VER/kernel/fs/

# Create init script (use the advanced one from section 7)
cat > $INITRD_DIR/init << 'INITEOF'
[paste the advanced init script here]
INITEOF
chmod +x $INITRD_DIR/init

# Create device nodes
mknod -m 600 $INITRD_DIR/dev/console c 5 1
mknod -m 666 $INITRD_DIR/dev/null c 1 3

# Build the image
cd $INITRD_DIR
find . | cpio -o -H newc | gzip > ../netboot-initrd.img
cd ..

echo "Created netboot-initrd.img"
```

---

## Resources and Next Steps

- **Kernel Documentation**: `/usr/src/linux/Documentation/filesystems/ramfs-rootfs-initramfs.txt`
- **Dracut Documentation**: `man dracut.conf`
- **Busybox**: Minimal userspace for embedded systems
- **iPXE**: Advanced network boot firmware

### Experimentation Ideas

1. Add iSCSI support for SAN boot
2. Implement LUKS encryption in initrd
3. Create a minimal recovery system
4. Build a live USB system with persistence
5. Implement automated hardware detection and driver loading

This guide provides a solid foundation for working with initrd files. Practice by building simple initrds first, then gradually add complexity for your netboot environment.