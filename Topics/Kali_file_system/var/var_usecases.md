# /var Directory - Use Case Deep Dive & Detailed Item Listing

## Document Structure Guide

This document provides detailed use-case mappings for each category with complete item listings following the grouping conventions established in `var_analysis_1.md`:

### Quick Convention Reminder:
- **`[0-6]`** = 7 individual numbered files
- **`*_[amd64|all].deb`** = Multiple architecture variants
- **`[lang-codes]/LC_MESSAGES`** = Multiple language subdirectories
- **`overlay2/[hash]/diff`** = 100+ individual layer directories

---

## USE CASE 1: System Monitoring & Administration

### Primary Location: `/var/log/`

#### Authentication & Access Control
**Items**: `auth.log`, `authpriv.log`, `secure`
- **Purpose**: Every sudo, su, ssh, login attempt recorded
- **Volume**: 10-50 MB/day on busy systems
- **Rotation**: Daily, kept 4-7 days uncompressed, 3+ weeks compressed
- **Analysis Tool**: `grep`, `fail2ban` log parser, SIEM ingest
- **Admin Action**: Monitor for failed login patterns, brute force attempts

#### System Messages & Kernel
**Items**: `syslog`, `messages`, `kern.log`, `dmesg` (real-time)
- **Purpose**: General system events, kernel driver loading, device detection
- **Volume**: 1-5 MB/day typical
- **Critical Events**: Hardware errors, out-of-memory, I/O errors
- **Admin Check**: New devices detected, driver loading, system stability

#### Daemon Activity
**Items**: `daemon.log`, `systemd.log`, `dbus/`
- **Purpose**: Background service state changes, startup/shutdown
- **Services Tracked**: systemd units, D-Bus IPC, service failures
- **Admin Use**: Troubleshooting service failures, startup sequence debugging

#### Package Management Events
**Items**: `/var/log/apt/`, `dpkg.log`, `aptitude.log`
- **Purpose**: Complete package installation history with versions
- **Details**: Upgrade sequences, dependency resolution, error messages
- **Admin Check**: Track when security patches were applied, what version currently installed

---

## USE CASE 2: Security Incident Response & Forensics

### Primary Locations: `/var/log/`, `/var/backups/`, `/var/lib/dpkg/`

#### Investigation Timeline Reconstruction
**Data Sources**: 
- `/var/log/auth.log` - User login timeline
- `/var/log/syslog` - System event timeline  
- `/var/backups/dpkg.status.*` - Software installation timeline
- `/var/log/wtmp` - Binary login database

**Analysis Process**:
1. Parse all logs with consistent timezone
2. Identify suspicious access (failed attempts, off-hours)
3. Cross-reference with system changes (file modifications, package updates)
4. Build attack timeline with root cause analysis

#### Post-Compromise Evidence Preservation
**Actions**:
- Archive `/var/log/` immediately to read-only media
- Extract and compress `/var/backups/` for historical analysis
- Snapshot `/var/lib/` before data is modified
- Preserve log rotation archives in `/var/log/`

#### Lateral Movement Detection
**Log Analysis**:
- `/var/log/auth.log`: Identify compromised user accounts
- `/var/log/syslog`: Detect privilege escalation attempts
- `/var/log/ufw.log` or iptables logs: Suspicious network activity
- Cross-correlation: Which user, when, accessing which system

---

## USE CASE 3: Package Security & Supply Chain

### Primary Location: `/var/cache/apt/archives/`

#### Complete Package Inventory

**System Core Packages**:
```
bash, coreutils, grep, sed, gawk, find, tar, cpio
-> 10 critical utilities - verify versions match security bulletins
```

**Security Packages**:
```
openssl, gnupg, cryptsetup, libgnutls, openfortivpn, openvpn
-> Crypto implementation versions - check for known vulnerabilities
```

**Development Tools** (1000+ packages):
```
gcc-15, clang-18/19, cmake, make, git, gdb
g++, binutils, linux-headers, build-essential
-> Compiler chain vulnerabilities, debugger access risks
```

**Servers & Services** (100+ packages):
```
apache2, nginx, mysql-server, postgresql, openssh-server
-> Service exposure analysis, exploit availability tracking
```

**Firmware & Drivers** (50+ packages):
```
firmware-linux, firmware-amd-graphics, firmware-atheros, firmware-iwlwifi
-> Hardware compromise detection, known firmware vulnerabilities
```

#### Vulnerability Assessment Workflow
1. Extract each `.deb` file: `ar x package.deb`
2. List contents: `tar -t -f data.tar.xz`
3. Cross-reference with vulnerability databases (NVD, CVE, DSAs)
4. Identify if patch applied or vulnerable version still installed

#### Dependency Chain Analysis
1. Parse `.deb` control metadata
2. Build dependency tree (shows what each package needs)
3. Identify abandoned/unsupported libraries
4. Detect library version conflicts (LD_PRELOAD attack surface)

---

## USE CASE 4: Docker Container Security Analysis

### Primary Location: `/var/cache/docker/overlay2/`

#### Layer-by-Layer Image Analysis

**Structure**:
```
overlay2/
├── [sha256_hash1]/
│   ├── committed (metadata)
│   ├── diff/ (actual file modifications)
│   ├── link (symbolic name)
│   ├── lower (parent layer reference)
│   └── work/ (staging directory)
├── [sha256_hash2]/
│   └── ... (repeat for each layer)
└── ... (100+ container layers total)
```

**Layer Analysis Process**:
1. Identify base image from bottommost layer's parent references
2. Inspect each `diff/` directory for file additions/modifications
3. Check for secrets in files (passwords, SSH keys, API tokens)
4. Scan for malware signatures in binaries

#### Forensic Findings Example
```
Layer 1 (Base Ubuntu): baseline libraries
Layer 2 (Dependencies): Python, NodeJS installed
Layer 3 (Application): Web app source code copied
→ FINDING: Hardcoded database password in /etc/config.yml
→ RISK: Container compromise exposes all databases
```

#### Supply Chain Security
- **Base image tracking**: Identify if FROM ubuntu:20.04 or FROM ubuntu:22.04
- **Patch level**: Check if dependencies are latest or outdated
- **Build artifacts**: Detect if intermediate build tools left in final image
- **Secret leakage**: Scan for API keys, certificates in any layer

---

## USE CASE 5: Compliance & Audit Preparation

### Primary Location: `/var/backups/` + `/var/log/`

#### Configuration Baseline Verification
**Backups preserved**:
- `dpkg.status.0` - Current package state
- `dpkg.status.1.gz through .6.gz` - Historical states (7 daily snapshots)
- `alternatives.tar.[0-6]` - System links history
- `apt.extended_states.[0-6]` - Package selection history

**Use for Compliance**: 
- Prove SOC 2 requirement: "Configuration changes were tracked"
- Demonstrate PCI-DSS: "We have 7-day audit trail"
- Support HIPAA: "System baseline and changes documented"

#### Log Retention & Availability
**Audit requirement**: "System must maintain 12 months of logs"
**Implementation**:
1. Daily logrotate compresses yesterday's logs
2. Archive older logs to separate partition/tape
3. Verify retention meets compliance dates
4. Produce audit report from log timestamps

#### Activity Audit Trail
**Extract from `/var/log/auth.log`**:
```
[Full audit] Who logged in, when, from where, success/failure
[Privilege] All sudo invocations with commands executed
[Files] Using auditd/ausearch for file access logs
```

**Generate Compliance Report**:
- "User alice logged in on 2025-01-15 10:23, executed sudo reboot"
- "User bob's account inactive for 90+ days (should be disabled)"
- "Administrator root account used 3 times in audit period"

---

## USE CASE 6: Performance Optimization & Troubleshooting

### Primary Locations: `/var/cache/`, `/var/lib/`, `/var/log/`

#### Cache Effectiveness Monitoring

**APT Package Cache** (`/var/cache/apt/archives/`):
- **Growth monitoring**: Alert if exceeds 500 MB (run `apt clean`)
- **Age analysis**: Remove packages not used in 6 months
- **Bandwidth savings**: Cached installs save 100s MB on reinstall

**Font Cache** (`/var/cache/fontconfig/`):
- **Startup impact**: Pre-computed metrics speed font loading
- **Regeneration**: Automatically rebuilt when fonts installed
- **Troubleshooting**: Clear cache if fonts display incorrectly

**Docker Image Cache** (`/var/cache/docker/overlay2/`):
- **Image reuse**: Shared layers prevent redundant storage
- **Deduplication**: 100 containers may share 80% of base layer
- **Cleanup**: `docker image prune` removes unused layers

#### Log Rotation & Performance

**Problem**: `/var/log/` fills disk, system becomes unresponsive
**Solution implemented in `/var/log/logrotate.d/`**:
1. Daily rotation (move syslog → syslog.1)
2. Compression (gzip oldest logs)
3. Retention (keep 4 weeks)
4. Cleanup (delete logs older than retention)

**Monitoring**: Check `/var/log/logrotate.status` to verify execution

#### Database Performance (`/var/lib/postgresql/`, `/var/lib/mariadb/`)

**Components**:
- **Data files**: `.ibd` (innodb) or `.dat` (postgresql) - raw table storage
- **Transaction logs**: WAL (Write-Ahead Logging) for recovery
- **Indices**: B-tree structures for query acceleration
- **Temporary space**: Query working memory

**Optimization**:
- Monitor disk usage growth (indicates storage bloat)
- Archive old data to reduce active dataset
- Vacuum/analyze to reclaim space and update statistics

---

## USE CASE 7: Privilege Escalation & Attack Surface Analysis

### Primary Locations: `/tmp/`, `/var/tmp/`, `/var/cache/`, `/var/lib/`

#### World-Writable Directory Risks

**Vulnerable Patterns**:
```bash
# /tmp and /var/tmp are world-writable by design
# But this enables race conditions:

# 1. Tmp-race attack
/tmp/script.sh (created by root script)
→ Attacker replaces with malicious code
→ Root executes attacker's payload

# 2. Directory symlink attack
/tmp/config/ → symlink to /etc/
→ Script writes to "config/passwd"
→ Actually modifies /etc/passwd
```

**Security Check**:
```bash
ls -ld /tmp /var/tmp
# Should show: drwxrwxrwt (sticky bit!)
# Sticky bit prevents unprivileged users from deleting others' files
```

#### SUID Binary Discovery

**Attack**: Find world-executable SUID binaries in applications
```bash
find /var/ -perm -4000 -type f 2>/dev/null
# Lists all set-UID binaries (run as owner regardless of who executes)
# Example: /var/www/app/upload_handler (root-owned)
# → Can be exploited to escalate to root
```

#### Cache Poisoning Vectors

**Docker layer tampering** (`/var/cache/docker/overlay2/`):
- If attacker can write to layer directories
- Modify application binaries in earlier layers
- Commit as new image
- All containers from that image compromised

**APT cache attack** (`/var/cache/apt/archives/`):
- Replace .deb files with backdoored versions
- Next `apt install` installs trojanized package
- Mitigation: Verify GPG signatures

#### Library Injection & LD_PRELOAD

**Attack**:
```bash
# In /var/cache/ or world-writable cache
echo '#include <unistd.h>
void _init() {
  setuid(0);
  system("/bin/sh");
}' > /tmp/libhax.c

# Compile: gcc -shared libhax.c -o libhax.so
# Export: LD_PRELOAD=/tmp/libhax.so /usr/bin/sudo whoami
# Result: Shell as root!
```

**Defense**:
- Restrict `/tmp/` write permissions
- Set LD_PRELOAD=""  in systemd unit hardening
- Monitor `/var/cache/` with file integrity checking

---

## USE CASE 8: Backup & Disaster Recovery

### Primary Location: `/var/backups/`

#### Backup Preservation Strategy

**File Rotation**:
```
Daily automated backups create:
Day 1: alternatives.tar.0 (uncompressed, most recent)
Day 2: alternatives.tar.0 compressed→.1.gz, new .0 created
Day 3: .1.gz→.2.gz, .0→.1.gz, new .0 created
...
Day 7: Oldest backup (.6.gz) kept
Day 8: Oldest backup deleted, others shifted down
```

**Retention Benefits**:
- Keep 7-day historical snapshots
- Detect and recover from gradual corruption
- Compare configurations from different dates

#### Recovery Procedure Example

**Scenario**: Package configuration corrupted, need to restore

```bash
# 1. Identify clean backup
tar -tzf /var/backups/dpkg.status.3.gz | head

# 2. Extract to temporary location
mkdir /tmp/recovery
cd /tmp/recovery
tar -xzf /var/backups/dpkg.status.3.gz

# 3. Restore package state
cp /tmp/recovery/var/lib/dpkg/status /var/lib/dpkg/status.corrupt
cp /tmp/recovery/var/lib/dpkg/status /var/lib/dpkg/status

# 4. Verify integrity
dpkg --audit
apt check

# 5. Update package cache
apt update
apt autoremove  # Clean up any inconsistent state
```

#### Off-site Backup Requirement

**Compliance mandate**: "Backups must be stored off-site"
**Implementation**:
1. Compress `/var/backups/` daily
2. Encrypt with GPG
3. Upload to remote storage (S3, rsync, SFTP)
4. Verify restore integrity monthly

---

## Quick Reference: All Items by Category

### Authentication & Privilege (Focus for Security)
- Files: `/var/log/auth.log`, `sudo.log`, `sulog`
- Analysis: Who accessed what, privilege escalation attempts
- Retention: 4 weeks minimum (compliance usually 12 months)

### System State (Focus for Administration)
- Files: `/var/backups/[dpkg.status|alternatives.tar]`
- Retention: 7 versions rolling
- Use: Restore known-good configurations

### Application State (Focus for Forensics)
- Location: `/var/lib/` (100+ application-specific directories)
- Contains: Databases, persistent data, configurations
- Risk: Sensitive data if unencrypted

### Caches (Focus for Performance)
- Types: APT packages, font metadata, locales, Docker layers
- Purpose: Avoid recomputation/re-download
- Management: Automatic cleanup policies or manual `clean` commands

### Security Policies (Focus for Hardening)
- Location: `/var/cache/apparmor/` (100+ MAC profiles)
- Purpose: Restrict what each application can do
- Review: Ensure profiles updated when applications updated

---

## Summary Table: All 15 Categories with Item Counts

| **Category** | **Location** | **Typical Items** | **Primary Use** | **Security Risk Level** |
|---|---|---|---|---|
| Backups | `/var/backups/` | 42 | Recovery, compliance | Medium |
| AppArmor | `/var/cache/apparmor/` | 100+ | MAC enforcement | Low (if enforced) |
| APT Cache | `/var/cache/apt/` | 1000+ | Package installation | Medium |
| Apache Cache | `/var/cache/apache2/` | Variable | HTTP performance | Low |
| Adduser | `/var/cache/adduser/` | Small | User creation | Low |
| Fontconfig | `/var/cache/fontconfig/` | 100s | Font performance | Low |
| Locales | `/var/cache/locale/` | 1000+ | Internationalization | Low |
| Man Pages | `/var/cache/man/` | 100+ | Documentation | Low |
| Libraries | `/var/lib/` | 100s MB | App persistence | High |
| Logs | `/var/log/` | 50+ streams | Auditing, troubleshooting | Critical |
| Runtime | `/var/run/` | Variable | Process state | Medium |
| Spool | `/var/spool/` | Variable | Job queues | Medium |
| Temp Files | `/tmp/`, `/var/tmp/` | Variable | Temporary storage | Critical |
| Web Root | `/var/www/` | Variable | HTTP content | High |
| Docker | `/var/cache/docker/` | 100+ | Containers | High |

---

**Complete analysis of /var directory use cases, item details, and security implications**

