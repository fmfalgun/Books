# Initrd, PXE, and Netboot for a Custom OS: Deep-Dive README

> End-to-end guide to designing a **custom OS**, building its **initrd/initramfs**, and booting it over the network using **PXELINUX/syslinux and GRUB (UEFI)**. Focused on low-level understanding suitable for OS dev, infra, and offensive security work.

---

## 1. Big Picture: What You Are Building

In this project you will:

1. **Build your own OS image** (from-scratch or via a minimal Linux base).
2. **Create an initrd/initramfs** that knows how to:
   - Bring up the network
   - Fetch or mount your root filesystem (NFS, iSCSI, HTTP, NBD, SquashFS+overlay)
   - Pivot to your custom OS userspace
3. **Serve kernel + initrd + configs over the network** via **PXE** for BIOS and **GRUB EFI** for UEFI.
4. Understand in depth the roles of:
   - `pxelinux.0`
   - `vesamenu.c32`
   - `ldlinux.c32`
   - `libutil.c32`
   - `libcom32.c32`
   - `grubx64.efi`
   - `pxelinux.cfg/default` ("default file")
   - `initrd` (initramfs)
   - `filesystem.squashfs`

The rest of this README is written as a **design+implementation doc** you can directly follow.

---

## 2. Boot Architecture Overview (BIOS vs UEFI)

### 2.1 BIOS PXE Path (PXELINUX/syslinux)

High-level flow (classic PXE):

1. NIC PXE ROM does **DHCP** and learns:
   - IP address of the client
   - `next-server` (TFTP server IP)
   - `filename` (e.g., `pxelinux.0`)
2. Client downloads `pxelinux.0` from TFTP.
3. `pxelinux.0` loads **ldlinux** core (`ldlinux.c32`/`ldlinux.sys`).
4. Core loader loads additional *.c32 modules (`vesamenu.c32`, `libcom32.c32`, `libutil.c32`, etc.).
5. PXELINUX searches for config files in `pxelinux.cfg/`:
   - MAC-specific, IP-specific, then finally `pxelinux.cfg/default`.
6. Config file instructs PXELINUX which **kernel** and **initrd** to load and what kernel command line (e.g., root=NFS, IP=dhcp, etc.).
7. Kernel + initrd are loaded into RAM and executed.
8. Initrd script mounts the real root filesystem (e.g., `filesystem.squashfs`, NFS, etc.) and pivots to it.

### 2.2 UEFI PXE Path (GRUB EFI)

For UEFI systems:

1. UEFI firmware does PXE (or HTTP boot) and downloads an EFI binary (e.g., `grubx64.efi`) from TFTP/HTTP.
2. `grubx64.efi` runs, reads its configuration (`grub.cfg`).
3. GRUB downloads kernel + initrd from TFTP/HTTP/NFS etc.
4. GRUB passes the kernel command line and hands off to the kernel.
5. Kernel + initrd perform early userspace steps and mount real root.

Your netboot infra will likely support **both** paths.

---

## 3. Syslinux/PXELINUX Components: File-by-File Deep Dive

This section explains each file you listed and how it fits into the PXE stack.

### 3.1 `pxelinux.0`

**What it is:**

- A **PXE-specific loader** from the **Syslinux** family.
- First-stage bootloader provided by the TFTP server to BIOS PXE clients.

**Key roles:**

- Implements the PXE boot protocol on top of the NIC firmware.
- Downloads its core support file (`ldlinux.c32` or `ldlinux.sys` depending on version).
- Locates and parses configuration in `pxelinux.cfg/`.
- Loads and runs the Linux kernel and initrd specified in config.

**Where it lives (TFTP tree example):**

```text
/srv/tftp/
  pxelinux.0
  ldlinux.c32
  libcom32.c32
  libutil.c32
  vesamenu.c32
  pxelinux.cfg/
    default
  vmlinuz
  initrd.img
```

You usually obtain it from your distribution's `syslinux`/`pxelinux` package.

---

### 3.2 `ldlinux.c32`

**What it is:**

- The **core runtime module** for Syslinux-family bootloaders.
- Implements common logic used by PXELINUX, ISOLINUX, EXTLINUX, etc.

**Key roles:**

- Provides core services: filesystem drivers, config parsing, COM32 API.
- Loaded immediately by `pxelinux.0`.
- Think of it as the “runtime library” for Syslinux.

Without `ldlinux.c32`, `pxelinux.0` will usually fail with an error like *"No COM32R image"* or similar.

---

### 3.3 `libcom32.c32`

**What it is:**

- A **shared library module** providing COM32 API helpers.
- Used by other `.c32` modules written using the COM32 interface.

**Key roles:**

- Provides runtime routines used by menu modules and other Syslinux extensions.
- Many `.c32` modules link against it.

If missing, you will typically see errors when trying to run `.c32`-based menus or modules.

---

### 3.4 `libutil.c32`

**What it is:**

- Another **utility library module** for Syslinux COM32 applications.

**Key roles:**

- Provides generic utility functions (string handling, console I/O, etc.) used by modules like `vesamenu.c32` and `menu.c32`.

This file is not executed by itself; it is **loaded on demand** when a dependent module starts.

---

### 3.5 `vesamenu.c32`

**What it is:**

- A **graphical menu module** for Syslinux/PXELINUX.
- Provides a VESA-based graphical menu with backgrounds, colors, and keybindings.

**Key roles:**

- Renders a full-screen menu of boot entries defined in `pxelinux.cfg/default`.
- Supports:
  - Timeouts
  - Passwords
  - Hidden entries
  - Graphical backgrounds

**Minimal example usage in `pxelinux.cfg/default`:**

```cfg
DEFAULT vesamenu.c32
PROMPT 0
TIMEOUT 100

MENU TITLE Netboot Menu

LABEL myos
  MENU LABEL ^My Custom OS (netboot)
  KERNEL /vmlinuz-myos
  APPEND initrd=/initrd-myos.img root=/dev/nfs nfsroot=192.168.1.10:/exports/myos ip=dhcp
```

If you do not need UI, you can skip `vesamenu.c32` and directly boot a label or `linux` with no menus.

---

## 4. GRUB UEFI Components

### 4.1 `grubx64.efi`

**What it is:**

- The **64-bit UEFI GRUB loader**.
- An EFI binary that UEFI firmware can execute directly (via PXE or HTTP boot or from disk).

**Key roles:**

- Reads `grub.cfg` from a known location (e.g. from TFTP or an EFI partition).
- Provides a powerful scripting language and modular design.
- Loads kernel and initrd from network or local storage.

**TFTP tree example for UEFI PXE:**

```text
/srv/tftp/
  EFI/
    BOOT/
      grubx64.efi
      grub.cfg
  vmlinuz-myos
  initrd-myos.img
```

**Minimal `grub.cfg` for netbooting your OS:**

```cfg
set default=0
set timeout=5

menuentry "My Custom OS (netboot)" {
    linux /vmlinuz-myos \
        ip=dhcp \
        root=/dev/nfs \
        nfsroot=192.168.1.10:/exports/myos,nolock,vers=3 \
        rw console=ttyS0
    initrd /initrd-myos.img
}
```

---

## 5. The "default file": `pxelinux.cfg/default`

This is the main configuration file for PXELINUX.

### 5.1 Search Order

PXELINUX looks for configs in this order:

1. `pxelinux.cfg/01-xx-xx-xx-xx-xx-xx` (MAC-specific)
2. `pxelinux.cfg/<IP in hex>` (e.g., `C0A80164` for 192.168.1.100)
3. Prefix-truncated IP filenames
4. Finally `pxelinux.cfg/default`

So `default` is the **catch-all configuration**.

### 5.2 Example `pxelinux.cfg/default` for your custom OS

```cfg
DEFAULT vesamenu.c32
PROMPT 0
TIMEOUT 50
ONTIMEOUT myos

MENU TITLE My Netboot Environment

LABEL myos
  MENU LABEL ^My Custom OS (SquashFS netboot)
  KERNEL /vmlinuz-myos
  APPEND initrd=/initrd-myos.img \
         ip=dhcp \
         boot=live \
         root=/dev/nfs \
         nfsroot=192.168.1.10:/exports/myos-root,nolock,vers=3 \
         console=ttyS0

LABEL debug
  MENU LABEL My Custom OS (debug initrd shell)
  KERNEL /vmlinuz-myos
  APPEND initrd=/initrd-myos-debug.img \
         ip=dhcp \
         rd.debug break=init console=ttyS0
```

You can add more labels for installers, rescue images, etc.

---

## 6. Initrd / Initramfs: Design and Implementation

### 6.1 Conceptual Role

**Initrd / initramfs** is the **early userspace** that runs as PID 1 right after the kernel
is decompressed. For a network-booted custom OS, it must:

1. Mount `/proc`, `/sys`, `/dev` (and possibly `/run`).
2. Load required kernel modules (network, filesystem, NFS, etc.).
3. Bring up the network (DHCP/static).
4. Discover or fetch the root filesystem (NFS, HTTP, iSCSI, SquashFS image, etc.).
5. Switch to the final root (via `switch_root` or `pivot_root`) and execute your real `init`.

### 6.2 Minimal Initramfs Layout

```text
initrd-root/
  init                 # PID 1 script/binary
  bin/
    busybox
  sbin/
  lib/
    modules/$(uname -r)/...
  dev/
  proc/
  sys/
  run/
  mnt/
    root/
```

### 6.3 Example `init` for NFS-root custom OS

```sh
#!/bin/busybox sh

# Early initrd script (PID 1)

mount -t proc proc /proc
mount -t sysfs sysfs /sys
mount -t devtmpfs devtmpfs /dev 2>/dev/null || mount -t tmpfs tmpfs /dev

# Diagnostics
echo "[initrd] Booting..."
cat /proc/cmdline

# Load network-related modules (adjust names for your kernel)
modprobe e1000e 2>/dev/null || modprobe e1000 2>/dev/null
modprobe nfs

# Bring up the network
ip link set eth0 up
udhcpc -i eth0 -t 5 -T 3 || echo "[initrd] DHCP failed"

# Mount NFS root (customize IP/path)
mkdir -p /mnt/root
mount -t nfs -o nolock,vers=3 192.168.1.10:/exports/myos-root /mnt/root || {
    echo "[initrd] NFS mount failed, dropping to shell"
    exec /bin/sh
}

# Switch to real root
cd /mnt/root
exec switch_root /mnt/root /sbin/init
```

### 6.4 Building the initramfs image

```bash
#!/bin/bash
set -e

KVER=$(uname -r)
ROOT=/tmp/initrd-root
OUT=/srv/tftp/initrd-myos.img

rm -rf "$ROOT"
mkdir -p "$ROOT"/{bin,sbin,lib,dev,proc,sys,run,mnt/root}

# Busybox
cp /bin/busybox "$ROOT/bin/"
( cd "$ROOT/bin" && for app in sh mount ip udhcpc modprobe; do ln -s busybox "$app"; done )

# Kernel modules (tweak for your NIC / FS)
mkdir -p "$ROOT/lib/modules/$KVER"
cp -a /lib/modules/$KVER/kernel/drivers/net "$ROOT/lib/modules/$KVER/kernel/" || true
cp -a /lib/modules/$KVER/kernel/fs/nfs* "$ROOT/lib/modules/$KVER/kernel/fs/" || true
cp /lib/modules/$KVER/modules.* "$ROOT/lib/modules/$KVER/" || true

# Init script
cat > "$ROOT/init" << 'EOF'
#!/bin/busybox sh
# (same as init script above)
EOF
chmod +x "$ROOT/init"

# Create cpio archive
cd "$ROOT"
find . -print0 | cpio -0o -H newc -R 0:0 | gzip > "$OUT"

ls -lh "$OUT"
```

You now have `initrd-myos.img` ready for PXE/GRUB.

---

## 7. `filesystem.squashfs` and Read-Only OS Root

### 7.1 What is SquashFS?

- A **compressed read-only filesystem**.
- Perfect for:
  - Live systems
  - Stateless diskless clients
  - Immutable OS images

You typically create it from a prepared root filesystem directory.

### 7.2 Creating `filesystem.squashfs`

```bash
# Assume /tmp/myos-root contains your final OS root filesystem
mksquashfs /tmp/myos-root /srv/tftp/filesystem.squashfs -comp xz -b 1M -Xbcj x86
```

### 7.3 Booting SquashFS via initrd (OverlayFS)

Common pattern:

- `filesystem.squashfs` is mounted read-only from NFS or HTTP (or directly from TFTP if small).
- `tmpfs` is used as the writable upper layer.
- `overlayfs` is used to merge them into a unified root.

Example init script snippet:

```sh
# After network up
mkdir -p /mnt/{squash,upper,work,root}

# Fetch image if using HTTP (example)
wget -O /tmp/filesystem.squashfs http://192.168.1.10/images/filesystem.squashfs

mount -t squashfs -o loop /tmp/filesystem.squashfs /mnt/squash
mount -t tmpfs tmpfs /mnt/upper
mkdir -p /mnt/work

mount -t overlay overlay \
    -o lowerdir=/mnt/squash,upperdir=/mnt/upper,workdir=/mnt/work \
    /mnt/root

exec switch_root /mnt/root /sbin/init
```

You can swap HTTP with NFS, iSCSI, etc.

---

## 8. Building Your Own OS Root

You have several options depending on how deep you want to go.

### 8.1 From Scratch with Buildroot

- Configure Buildroot to:
  - Build your kernel
  - Build a minimal rootfs
  - Optionally directly produce an initramfs or a SquashFS root
- You then plug kernel + initramfs/SquashFS into PXE/GRUB flows.

This gives you almost full control over **userspace**, libraries, and features.

### 8.2 Using Minimal Distro (Alpine/Debian Minimal)

- Create a minimal chroot (e.g., debootstrap, `apk` rootfs).
- Customize systemd/openrc/init, services, etc.
- Use that as `/tmp/myos-root` when building `filesystem.squashfs`.

### 8.3 Fully Custom Userspace

- Write your own init, services, and even custom libc if you want to go full OS-dev.
- Use the same netboot pipeline, just change what `filesystem.squashfs` or NFS root contains.

---

## 9. Netboot Server Setup (DHCP + TFTP + Optional NFS/HTTP)

### 9.1 DHCP (ISC dhcpd example)

`/etc/dhcp/dhcpd.conf`:

```cfg
subnet 192.168.1.0 netmask 255.255.255.0 {
    range 192.168.1.100 192.168.1.200;
    option routers 192.168.1.1;
    option domain-name-servers 8.8.8.8;

    # BIOS PXE
    next-server 192.168.1.10;        # TFTP server
    filename "pxelinux.0";          # For BIOS clients

    # Optional: arch-based decisions for UEFI
    # if option client-architecture = 00:07 {
    #     filename "EFI/BOOT/grubx64.efi";
    # }
}
```

### 9.2 TFTP Server

```bash
sudo apt-get install tftpd-hpa
sudo mkdir -p /srv/tftp

# Copy syslinux files
cp /usr/lib/PXELINUX/pxelinux.0 /srv/tftp/       # path depends on distro
cp /usr/lib/syslinux/modules/bios/ldlinux.c32 /srv/tftp/
cp /usr/lib/syslinux/modules/bios/libutil.c32 /srv/tftp/
cp /usr/lib/syslinux/modules/bios/libcom32.c32 /srv/tftp/
cp /usr/lib/syslinux/modules/bios/vesamenu.c32 /srv/tftp/

# Your kernel/initrd
cp vmlinuz-myos /srv/tftp/
cp initrd-myos.img /srv/tftp/

mkdir -p /srv/tftp/pxelinux.cfg
cp pxelinux-default.cfg /srv/tftp/pxelinux.cfg/default
```

`/etc/default/tftpd-hpa` example:

```cfg
TFTP_USERNAME="tftp"
TFTP_DIRECTORY="/srv/tftp"
TFTP_ADDRESS="0.0.0.0:69"
TFTP_OPTIONS="--secure"
```

Then:

```bash
sudo systemctl restart tftpd-hpa
```

### 9.3 NFS Server (if using NFS root)

`/etc/exports`:

```cfg
/exports/myos-root 192.168.1.0/24(ro,no_subtree_check,no_root_squash)
```

```bash
sudo exportfs -ra
sudo systemctl restart nfs-server
```

---

## 10. From Power-On to Your OS: End-to-End Flow

1. **Client powers on** with network boot first.
2. **BIOS PXE path**:
   - NIC PXE → DHCP → get `pxelinux.0` and TFTP server
   - Download `pxelinux.0` → loads `ldlinux.c32`
   - Loads `vesamenu.c32`, `libcom32.c32`, `libutil.c32`
   - Reads `pxelinux.cfg/default`
   - User selects menu entry (or timeout)
   - PXELINUX downloads kernel (`vmlinuz-myos`) + `initrd-myos.img`
   - Kernel runs and unpacks initrd → init script executes
   - Init script configures network, mounts root (`filesystem.squashfs` or NFS)
   - `switch_root` to final root → your OS `init` runs

3. **UEFI PXE path**:
   - UEFI firmware → DHCP (possibly via UEFI PXE) → downloads `grubx64.efi`
   - `grubx64.efi` reads `grub.cfg`
   - Loads kernel + initrd from TFTP/HTTP/NFS
   - Same initrd-based early userspace → same root mounting logic → your OS.

You now own the entire chain.

---

## 11. Next Steps and Extensions

- Add **TLS** to the initrd for authenticated image download.
- Implement **per-device provisioning** using MAC-based configs and per-device images.
- Integrate **TPM measurements** or remote attestation for high-assurance boot.
- Build multiple OS variants (e.g. attacker toolkit, forensic toolkit, lab OS) all sharing the same netboot infra.

This README is intended as the core artifact for your project. You can now:

- Drop it into a repo as `README.md`.
- Add subdirectories for `initrd/`, `pxe-config/`, `rootfs/`, etc.
- Start iterating on your own OS and boot stack with full visibility into each component.
