# /var Directory - Quick Reference & Navigation Guide

## 📋 Three-Document Suite Overview

You now have **3 comprehensive markdown files** analyzing the `/var` directory:

### Document 1: `var_analysis_1.md` ⭐ START HERE
- **16 detailed category tables** (backups, cache, logs, lib, run, spool, etc.)
- 3-column format: Category | All Items | Explanation
- **Grouping conventions explained** at the beginning
- Best for: Understanding what each item does
- Length: ~3000 words

### Document 2: `var_statistics.md`
- **Summary statistics** (2000+ items total, 15-50 GB typical)
- **Directory hierarchy** with visual tree
- **Risk assessment** (high/medium/low security impact)
- **Professional recommendations** by role
- **Compliance mappings** (NIST, CIS, PCI-DSS, HIPAA, SOC 2, GDPR)
- Best for: Executive summaries, compliance reports
- Length: ~2000 words

### Document 3: `var_usecases.md`
- **8 detailed professional use cases** with step-by-step analysis
- Real-world attack scenarios and defenses
- Forensic procedures and recovery techniques
- Privilege escalation vectors
- Supply chain security analysis
- Best for: Penetration testing, incident response, compliance audits
- Length: ~3500 words

---

## 🎯 How to Use These Documents

### If You're a **System Administrator**
1. Read: `var_statistics.md` sections on "Major Use Cases" and "Directory Hierarchy"
2. Focus: `/var/log/`, `/var/backups/`, `/var/lib/`
3. Action: Implement log retention, backup rotation, disk monitoring

### If You're a **Security Researcher/Penetration Tester**
1. Read: `var_usecases.md` - USE CASE 7 (Privilege Escalation)
2. Read: `var_statistics.md` - Risk Assessment section
3. Focus: `/tmp/`, `/var/tmp/`, `/var/cache/docker/`, `/var/cache/apt/`
4. Tools: `find`, symlink attacks, LD_PRELOAD techniques

### If You're a **Compliance/Audit Professional**
1. Read: `var_statistics.md` - Compliance Mappings section
2. Read: `var_usecases.md` - USE CASE 5 (Compliance & Audit)
3. Focus: `/var/log/` retention, `/var/backups/` preservation
4. Action: Generate audit reports, verify backup integrity

### If You're a **Incident Response / Forensic Analyst**
1. Read: `var_usecases.md` - USE CASE 2 (Security Incident Response)
2. Read: `var_analysis_1.md` - /var/log/ and /var/backups/ sections
3. Focus: Timeline reconstruction from logs, data recovery
4. Tools: `logparse`, `strings`, `ar` (for .deb), overlay2 analysis

### If You're a **DevOps / Container Engineer**
1. Read: `var_usecases.md` - USE CASE 4 (Docker Container Analysis)
2. Read: `var_analysis_1.md` - /var/cache/docker/ section
3. Focus: Image layer analysis, cache management, secrets scanning
4. Tools: `docker inspect`, layer diffs, vulnerability scanners

---

## 📊 Quick Statistics Reference

| Metric | Value | Source |
|---|---|---|
| Total Items Analyzed | 2000+ | var_statistics.md |
| Major Categories | 15 | var_analysis_1.md |
| Backup Files | 42 | var_analysis_1.md, Table 1 |
| AppArmor Profiles | 100+ | var_analysis_1.md, Table 2 |
| APT Packages (Cache) | 1000+ | var_analysis_1.md, Table 3 |
| Log Streams | 50+ | var_analysis_1.md, Table 11 |
| Docker Layers | 100+ | var_analysis_1.md, Table 16 |
| Locale Variants | 25+ | var_analysis_1.md, Table 8 |
| Typical Size | 15-50 GB | var_statistics.md |

---

## 🔍 Finding Information by Topic

### Backups & Recovery
- **Quick Overview**: var_analysis_1.md, Table 1
- **Statistics**: var_statistics.md, Data Retention & Lifecycle
- **Procedures**: var_usecases.md, USE CASE 8
- **Key Files**: `/var/backups/dpkg.status.*`, `apt.extended_states.*`, `alternatives.tar.*`

### Security & Threat Detection
- **Overview**: var_analysis_1.md, Table 2 (AppArmor), Table 11 (Logs)
- **Risk Assessment**: var_statistics.md, Risk Assessment section
- **Attack Vectors**: var_usecases.md, USE CASE 7
- **Log Analysis**: var_usecases.md, USE CASE 2

### Docker & Containers
- **Structure**: var_analysis_1.md, Table 16
- **Security**: var_usecases.md, USE CASE 4
- **Statistics**: var_statistics.md, Summary Table
- **Key Files**: `/var/cache/docker/overlay2/`

### Logs & Auditing
- **Categories**: var_analysis_1.md, Table 11 (complete breakdown)
- **Retention**: var_statistics.md, Data Retention & Lifecycle
- **Analysis**: var_usecases.md, USE CASE 1, USE CASE 2
- **Compliance**: var_statistics.md, Compliance & Standards Mapping

### Application State & Libraries
- **Overview**: var_analysis_1.md, Table 9
- **Statistics**: var_statistics.md, Directory Hierarchy
- **Use Cases**: var_usecases.md, USE CASE 1, USE CASE 6
- **Key Directories**: `/var/lib/dpkg/`, `/var/lib/docker/`, `/var/lib/postgresql/`

### Performance Optimization
- **Caching Strategy**: var_analysis_1.md, Tables 3-9
- **Management**: var_statistics.md, Data Retention & Lifecycle
- **Troubleshooting**: var_usecases.md, USE CASE 6
- **Key Files**: `/var/cache/fontconfig/`, `/var/cache/locale/`, `/var/cache/apt/`

### Compliance & Standards
- **Framework Mapping**: var_statistics.md, Compliance & Standards Mapping
- **Audit Procedures**: var_usecases.md, USE CASE 5
- **Statistics**: var_statistics.md, Quick Statistics, Professional Recommendations
- **Key Evidence**: `/var/log/`, `/var/backups/`

### Penetration Testing
- **Attack Surface**: var_analysis_1.md, Table 9 (/var/lib/), Table 14 (/tmp/)
- **Escalation**: var_usecases.md, USE CASE 7
- **Evidence Destruction**: var_usecases.md, Forensic Analysis (destroying evidence)
- **Key Targets**: `/tmp/`, `/var/tmp/`, `/var/cache/docker/`, SUID binaries

---

## 🔐 Security Risk Quick Reference

### 🔴 CRITICAL Risk (Immediate Attention)
| Item | Risk | Mitigation | Doc Reference |
|---|---|---|---|
| `/tmp/`, `/var/tmp/` | SUID race conditions, privilege escalation | Sticky bit, tmpwatch | var_usecases.md, USE CASE 7 |
| `/var/log/auth.log` | Login/password attempt leakage | Encryption, centralized logging | var_usecases.md, USE CASE 2 |
| `/var/cache/docker/` | Secrets in layers, base OS vulns | Image scanning, layer inspection | var_usecases.md, USE CASE 4 |
| `/var/spool/mail/` | Email content, credentials | Encryption, access control | var_statistics.md, High-Risk |
| `/var/www/` | Source code exposure, injection attacks | Web app firewall, code review | var_statistics.md, High-Risk |

### 🟠 MEDIUM Risk (Regular Monitoring)
| Item | Risk | Mitigation | Doc Reference |
|---|---|---|---|
| `/var/cache/apt/` | Malicious package installation | GPG verification, origin checks | var_usecases.md, USE CASE 3 |
| `/var/lib/` | Unencrypted databases, state corruption | Encryption at rest, backups | var_analysis_1.md, Table 9 |
| `/var/log/` (general) | Information disclosure from logs | Log aggregation, retention limits | var_statistics.md, Medium-Risk |
| `/var/cache/apparmor/` | Policy escape on compromised system | Regular policy review | var_analysis_1.md, Table 2 |

### 🟢 LOW Risk (Preventive Maintenance)
| Item | Risk | Mitigation | Doc Reference |
|---|---|---|---|
| `/var/cache/locale/`, `/var/cache/fontconfig/` | Non-sensitive metadata | Regular cache cleanup | var_analysis_1.md, Tables 7-8 |
| `/var/run/` | PID files, socket info | File permissions verification | var_analysis_1.md, Table 12 |
| `/var/backups/` | Old configs (still sensitive) | Secure deletion on disposal | var_analysis_1.md, Table 1 |
| `/var/lock/` | Lock file manipulation | File permissions, monitoring | var_analysis_1.md, Table 10 |

---

## 📝 Key Takeaways by Role

### System Administrators
✓ Monitor `/var/log/` growth and configure logrotate  
✓ Verify `/var/backups/` rotation working correctly  
✓ Set alerts for `/var/spool/` exceeding thresholds  
✓ Plan for `/var/` disk space (15-50 GB typical)  

### Security Teams
✓ Centralize `/var/log/auth.log` to SIEM  
✓ Scan `/var/cache/docker/` for vulnerabilities  
✓ Review `/var/cache/apparmor/` policies quarterly  
✓ Monitor `/tmp/` and `/var/tmp/` for SUID binaries  

### DevOps/Container Teams
✓ Implement `docker image prune` for layer cleanup  
✓ Use named volumes instead of `/var/lib/` bind mounts  
✓ Scan base images in `/var/cache/docker/` pre-deployment  
✓ Centralize logs from `/var/log/` to logging platform  

### Forensic/Incident Response
✓ Archive `/var/log/` immediately on suspected breach  
✓ Extract `/var/backups/dpkg.status.*` for timeline  
✓ Analyze `/var/cache/docker/overlay2/` for artifacts  
✓ Preserve `/var/spool/` for email recovery  

### Penetration Testers
✓ Check `/tmp/`, `/var/tmp/` for world-writable vulnerabilities  
✓ Scan `/var/cache/apt/` for weak dependencies  
✓ Test `/var/cache/docker/` layer tampering  
✓ Identify SUID binaries as escalation targets  

---

## 🚀 Getting Started

### For Quick Understanding
**Start here**: `var_statistics.md` → Quick Statistics + Directory Hierarchy

### For Complete Knowledge
**Path**: `var_analysis_1.md` (Tables 1-16) → `var_statistics.md` → `var_usecases.md`

### For Specific Tasks

#### "I need to set up audit compliance"
→ `var_statistics.md`: Compliance & Standards Mapping  
→ `var_usecases.md`: USE CASE 5  
→ `var_analysis_1.md`: Table 11 (Logs)

#### "I need to analyze a security incident"
→ `var_usecases.md`: USE CASE 2  
→ `var_analysis_1.md`: Table 11 (Logs)  
→ `var_analysis_1.md`: Table 1 (Backups)

#### "I need to scan Docker containers for vulnerabilities"
→ `var_usecases.md`: USE CASE 4  
→ `var_analysis_1.md`: Table 16  
→ `var_statistics.md`: High-Risk Directories

#### "I need to perform penetration testing"
→ `var_usecases.md`: USE CASE 7  
→ `var_statistics.md`: Risk Assessment  
→ `var_analysis_1.md`: Tables 12-14

---

## 📎 File Reference Guide

### All Items Listed (Using Grouping Convention)

**Items WITH numbers (grouped)**:
- `alternatives.tar.[0-6]` = 7 items
- `dpkg.status.[0-6]` = 7 items
- `apt.extended_states.[0-6]` = 7 items
- `firmware-*_[20250808-1, 20251111-1]_all.deb` = 2 versions
- `locale/[25+ language codes]/LC_MESSAGES` = 1000+ files

**Total count**: 2000+ individual files across all categories

---

## 💾 Practical Usage Examples

### Command: Find all backup files older than 7 days
```bash
find /var/backups -name "*.gz" -mtime +7 -ls
# Then archive to external storage
```

### Command: Analyze AppArmor profiles for policy violations
```bash
cat /var/log/syslog | grep DENIED | tail -100
# Check /var/cache/apparmor/ for corresponding profiles
```

### Command: Scan Docker image for embedded secrets
```bash
cd /var/cache/docker/overlay2/
for dir in */diff; do
  strings "$dir"/* | grep -E 'password|api_key|secret'
done
```

### Command: Generate compliance audit report
```bash
# Extract from /var/backups/
tar -tzf /var/backups/dpkg.status.3.gz
# Parse /var/log/auth.log
grep "sudo" /var/log/auth.log | tail -100
# Report generation
```

---

## 📞 Support & Questions

### Questions About...
- **Specific /var files?** → Check `var_analysis_1.md` for your category
- **Security implications?** → Check `var_statistics.md` Risk Assessment
- **How to use for security work?** → Check `var_usecases.md`
- **Statistics/metrics?** → Check `var_statistics.md` Quick Statistics
- **Professional recommendations?** → Check `var_statistics.md` Recommendations
- **Attack scenarios?** → Check `var_usecases.md` USE CASE 7

---

**Complete /var directory documentation suite ready for reference, analysis, and professional use**

