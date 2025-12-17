# Complete Guide to initrd Files: Development and Netboot

## What is initrd?

The initial RAM disk (initrd) is a temporary filesystem loaded into memory by the bootloader before the real root filesystem is mounted. It serves as a bridge between the kernel and the real root filesystem, handling hardware detection, driver loading, and filesystem setup during the early boot process.

Think of initrd as the operating system's emergency toolkit—it contains just enough to get your system bootstrapped before the full OS takes over.

## Why initrd Matters for Netboot

In traditional booting, the kernel can mount the root filesystem directly because the hardware and drivers are typically known. In netboot scenarios, you're booting over a network where:

- You don't know the exact network hardware until runtime
- Root filesystems are remote (NFS, iSCSI, HTTP, etc.)
- You need to load network drivers dynamically
- You require tools to configure networking and mount remote storage

The initrd solves these problems by providing a minimal environment that can discover hardware, load necessary drivers, and set up network connectivity before handing over to the real OS.

## Architecture and Components

### 1. The Boot Sequence

```
1. Bootloader (GRUB, PXE, etc.)
   ↓
2. Loads Kernel Image
   ↓
3. Loads initrd into memory
   ↓
4. Kernel executes → Mounts initrd as temp root
   ↓
5. initrd runs init script (pivot_root)
   ↓
6. Real root filesystem mounted
   ↓
7. System initialization (systemd, init)
```

### 2. initrd File Formats

There are two main formats:

**Legacy initrd (rarely used now):**
- A gzip-compressed filesystem image
- Created with `genromfs` or similar tools
- Mounted directly by kernel

**Modern initramfs (current standard):**
- A gzip-compressed cpio archive
- Can include compiled-in drivers
- More flexible, supports microcode loading
- Standard for most distributions

The kernel treats both similarly at boot time, but initramfs is preferred because it's more modular and efficient.

### 3. Internal Structure

A typical initramfs contains:

```
initramfs.img (after extraction)
├── bin/
│   ├── sh
│   ├── mount
│   ├── umount
│   ├── ip
│   ├── dhclient
│   └── other essential tools
├── sbin/
│   ├── init (or linuxrc)
│   ├── insmod
│   ├── modprobe
│   └── other utilities
├── lib/ or lib64/
│   ├── modules/
│   │   └── kernel drivers (.ko files)
│   ├── libc.so.6
│   └── other shared libraries
├── etc/
│   ├── modprobe.conf
│   └── config files
├── sys/
│   └── (virtual filesystem mount point)
├── proc/
│   └── (virtual filesystem mount point)
├── dev/
│   └── (device nodes)
├── mnt/ or /root/
│   └── (mount point for real filesystem)
└── init
    └── (main boot script)
```

## How initrd Boot Process Works

### Phase 1: Kernel Initialization
- Kernel decompresses initramfs from memory
- Sets up virtual filesystems (tmpfs)
- Mounts initramfs as root (/)

### Phase 2: Early Init
- Kernel executes `/init` or `/linuxrc` (traditionally in shell)
- Creates essential device nodes
- Mounts /sys and /proc

### Phase 3: Hardware Detection and Driver Loading
```bash
# Typical early-boot steps
mkdir -p /proc /sys /dev /mnt/root

# Mount sysfs for device discovery
mount -t sysfs sysfs /sys

# Load necessary drivers
modprobe e1000          # Network driver
modprobe raid1          # RAID support if needed

# Set up device mapper for LUKS, LVM, etc.
modprobe dm_crypt
```

### Phase 4: Network Configuration (for Netboot)
```bash
# Bring up network interface
ip link set eth0 up

# Configure IP (DHCP or static)
dhclient eth0
# or
ip addr add 192.168.1.100/24 dev eth0
ip route add default via 192.168.1.1

# Test connectivity
ping -c 1 remote.server
```

### Phase 5: Mount Real Root Filesystem

**NFS:**
```bash
mount -t nfs -o tcp remote.server:/export/root /mnt/root
```

**iSCSI:**
```bash
iscsiadm -m discovery -t sendtargets -p target.server
iscsiadm -m node --login
# Then mount the discovered block device
mount /dev/sda1 /mnt/root
```

**HTTP (using special tools):**
```bash
# Custom tools to download filesystem image
wget http://server/rootfs.tar.gz -O /mnt/root.tar
cd /mnt/root && tar xzf /mnt/root.tar
```

### Phase 6: Switch Root (pivot_root)
```bash
# Move current root out of the way
pivot_root /mnt/root /mnt/root/old_root

# Change to new environment
cd /

# Unmount old initramfs
umount -l /old_root
exec chroot . /sbin/init
```

This transfers control to the real system's init process.

## Creating a Custom initramfs for Netboot

### Method 1: Using dracut (Recommended for Modern Systems)

Dracut is the modern standard for generating initramfs with netboot support:

```bash
# Install dracut
sudo apt install dracut dracut-network  # Debian/Ubuntu
sudo yum install dracut dracut-network   # RHEL/CentOS

# Generate netboot-capable initramfs
sudo dracut -H -f --add network \
  --include /etc/dhcp /etc/dhcp \
  /boot/initramfs-netboot.img

# For PXE with specific network drivers
sudo dracut -H -f --add network --add-drivers "e1000 bnx2" \
  -o "plymouth" /boot/initramfs-netboot.img
```

Key dracut modules for netboot:
- `network`: Network device discovery and configuration
- `nfs`: NFS support
- `iscsi`: iSCSI support
- `cifs`: CIFS/SMB support

### Method 2: Using mkinitramfs (Debian/Ubuntu)

```bash
# Install necessary packages
sudo apt install initramfs-tools busybox

# Edit configuration
sudo nano /etc/initramfs-tools/initramfs.conf
# Add: MODULES=netboot
# Add: BUSYBOX=y

# Generate initramfs
sudo mkinitramfs -o /boot/initramfs-netboot.img 5.10.0-generic
```

### Method 3: Manual Construction from Scratch

For maximum control:

```bash
#!/bin/bash
# Create minimal netboot initramfs

WORKDIR=$(mktemp -d)
mkdir -p $WORKDIR/{bin,sbin,lib,etc,sys,proc,dev,mnt,root}

# Copy essential binaries
for bin in sh mount umount ip dhclient modprobe insmod udevadm; do
  cp /bin/$bin $WORKDIR/bin/ 2>/dev/null || \
  cp /sbin/$bin $WORKDIR/sbin/ 2>/dev/null
done

# Copy libraries
ldd /sbin/modprobe | grep "=>" | awk '{print $3}' | while read lib; do
  [ -n "$lib" ] && cp "$lib" $WORKDIR/lib/
done

# Create init script
cat > $WORKDIR/init << 'INITSCRIPT'
#!/bin/sh
mount -t proc proc /proc
mount -t sysfs sysfs /sys
mount -t tmpfs tmpfs /dev

# Load network driver
modprobe e1000

# Bring up network
ip link set eth0 up
ip addr add 192.168.1.100/24 dev eth0
ip route add default via 192.168.1.1

# Mount NFS root
mount -t nfs -o tcp 192.168.1.1:/export/root /mnt/root

# Switch root
cd /mnt/root
pivot_root . old_root
exec chroot . /sbin/init
INITSCRIPT

chmod +x $WORKDIR/init

# Create initramfs cpio archive
cd $WORKDIR
find . | cpio -H newc -o | gzip > /boot/initramfs-custom.img

cd /
rm -rf $WORKDIR
```

## Debugging and Testing Initramfs

### Extract and Inspect

```bash
# Extract cpio archive
cd /tmp/initramfs-debug
gunzip -c /boot/initramfs-netboot.img | cpio -idm

# List contents
ls -la
```

### Boot with Kernel Messages

Add to bootloader (GRUB):
```
linux /vmlinuz-5.10 root=/dev/nfs initrd=/initramfs-netboot.img \
  rd.debug rd.shell
```

The `rd.shell` parameter drops you into a shell if boot fails, allowing debugging.

### Verify Network Configuration in initramfs

```bash
# In dracut-generated initramfs
/usr/lib/dracut/modules.d/90network/: Check network setup scripts
# Look for dhclient, ip command execution logs
```

### Common Boot Parameters for Netboot

```
# NFS root
root=/dev/nfs nfsroot=server:/path ip=dhcp

# iSCSI
iscsi_initiator=iqn.1991-05.com.example iscsi_target_name=iqn.target \
  iscsi_target_ip=192.168.1.50

# Debugging
rd.debug rd.shell rd.break=pre-mount
```

## Performance Optimization for Netboot

1. **Reduce initramfs Size:**
   - Remove unnecessary drivers and modules
   - Use `strip` on binaries
   - Minimize initramfs in dracut config

2. **Parallel Driver Loading:**
   - Configure modprobe to load drivers in parallel

3. **Pre-cache DNS:**
   - Include hostname resolution in boot parameters

4. **Network Optimization:**
   - Use TCP for NFS (faster than UDP over WAN)
   - Consider compression for filesystem transfer

## Common Issues and Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| Network not detected | Missing drivers | Add `--add-drivers` to dracut |
| Mount fails | NFS server unreachable | Check server, firewall, boot params |
| pivot_root fails | Permissions or mounts | Ensure dev, sys, proc unmounted first |
| Script syntax errors | Shell incompatibility | Use `#!/bin/sh` and POSIX syntax |
| Out of memory | Initramfs too large | Compress, remove unused modules |

## Production Netboot Workflow

1. **Build initramfs** with dracut/mkinitramfs
2. **Configure PXE server** (dnsmasq/ISC-DHCP)
3. **Host kernel and initramfs** via TFTP
4. **Export root filesystem** via NFS/iSCSI
5. **Test on client machine** with debugging enabled
6. **Monitor boot logs** via serial console or syslog
7. **Optimize** based on performance metrics
8. **Deploy** to production infrastructure

This approach ensures reliable, debuggable, and maintainable netboot environments across your target machines.