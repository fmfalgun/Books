Here are the commands to manually assign an IP address to your system:

## Basic IP Assignment

```bash
# Assign IP with subnet mask
sudo ip addr add 10.0.5.42/16 dev eth0

# Bring interface up
sudo ip link set eth0 up
```

---

## Complete Network Configuration

```bash
# Step 1: Assign IP address
sudo ip addr add 10.0.5.42/16 dev eth0

# Step 2: Set default gateway
sudo ip route add default via 10.0.0.1 dev eth0

# Step 3: Add DNS (optional)
echo "nameserver 8.8.8.8" | sudo tee /etc/resolv.conf

# Step 4: Verify configuration
ip addr show eth0
ip route show
```

---

## Different Subnet Mask Examples

```bash
# /24 subnet (255.255.255.0)
sudo ip addr add 10.0.5.42/24 dev eth0

# /16 subnet (255.255.0.0) - What we used
sudo ip addr add 10.0.5.42/16 dev eth0

# /8 subnet (255.0.0.0)
sudo ip addr add 10.0.5.42/8 dev eth0
```

---

## Alternative Method: Using ifconfig (Old Style)

```bash
# Assign IP
sudo ifconfig eth0 10.0.5.42 netmask 255.255.0.0 up

# Add gateway
sudo route add default gw 10.0.0.1 eth0
```

---

## Remove/Flush IP Configuration

```bash
# Remove specific IP
sudo ip addr del 10.0.5.42/16 dev eth0

# Remove ALL IPs from interface
sudo ip addr flush dev eth0
```

---

## Quick Reference Table

| Task | Command |
|------|---------|
| Add IP | `sudo ip addr add 10.0.5.42/16 dev eth0` |
| Remove IP | `sudo ip addr del 10.0.5.42/16 dev eth0` |
| Flush all IPs | `sudo ip addr flush dev eth0` |
| Set gateway | `sudo ip route add default via 10.0.0.1 dev eth0` |
| Interface up | `sudo ip link set eth0 up` |
| Interface down | `sudo ip link set eth0 down` |
| View config | `ip addr show eth0` |

---

## Complete Setup Script

```bash
#!/bin/bash

# Configuration
INTERFACE="eth0"
IP_ADDRESS="10.0.5.42"
SUBNET="/16"
GATEWAY="10.0.0.1"

# Apply configuration
echo "[*] Configuring $INTERFACE..."
sudo ip addr add ${IP_ADDRESS}${SUBNET} dev $INTERFACE
sudo ip link set $INTERFACE up
sudo ip route add default via $GATEWAY dev $INTERFACE

# Verify
echo "[+] Configuration complete!"
ip addr show $INTERFACE | grep inet
ip route show
```

The key command you need is:
```bash
sudo ip addr add 10.0.5.42/16 dev eth0
```

This assigns IP `10.0.5.42` with subnet mask `/16` (255.255.0.0) to interface `eth0`. 🎯
