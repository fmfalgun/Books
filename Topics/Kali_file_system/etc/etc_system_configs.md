# Linux /etc Configuration System Services - Complete Hierarchical Analysis

**Comprehensive categorization of system configuration directories and service configurations for security, networking, and server management.**

---

## Overview

This document analyzes the core system configuration directories in `/etc` that manage critical system services, security policies, and daemon configurations in a Kali Linux penetration testing environment.

---

## 1. Web Server - Apache2 Configuration

| **Category** | **Files/Directories** | **Explanation** |
|---|---|---|
| **Main Config** | `apache2.conf` | Primary Apache2 configuration master file. Loads all modules and site configs |
| **Environment** | `envvars` | Environment variables for Apache2 daemon processes (user, group, ports) |
| **MIME Types** | `magic` | MIME type detection magic file for Apache2 content negotiation |
| **Port Config** | `ports.conf` | Defines listening ports (default: HTTP on 80, HTTPS on 443) |
| **Modules Available** | `mods-available/` (150+ .conf and .load files) | All installable Apache2 modules: authentication, compression, SSL, proxy, DAV, scripting |
| **Modules Enabled** | `mods-enabled/` (35+ symlinks) | Currently enabled modules linked from mods-available. Includes PHP 8.4, SSL, Proxy, Rewrite |
| **Sites Available** | `sites-available/` (2 config files) | Virtual host configurations: `000-default.conf`, `default-ssl.conf` |
| **Sites Enabled** | `sites-enabled/` (1 symlink) | Active virtual host: `000-default.conf → ../sites-available/000-default.conf` |
| **Global Configs** | `conf-available/` (6 conf files) | Optional global configurations: charset, JavaScript, localized errors, security, CGI |
| **Enabled Configs** | `conf-enabled/` (6 symlinks) | Active global configurations linked from conf-available |

**Key Apache Modules Enabled:**
- **Authentication**: auth_basic, authn_core, authn_file, authz_core, authz_host, authz_user
- **Performance**: deflate (compression), filter, mime, negotiation
- **Scripting**: PHP 8.4 (`php8.4.load`, `php8.4.conf`)
- **Proxy**: proxy, proxy_http, proxy_balancer (with health checks)
- **SSL/TLS**: ssl (available, not enabled by default in this config)
- **Utilities**: alias, autoindex, cgi, status, rewrite, headers, env

---

## 2. Web Server - Nginx Configuration

| **Category** | **Files/Directories** | **Explanation** |
|---|---|---|
| **Main Config** | `nginx.conf` | Primary Nginx configuration. Defines worker processes, events, HTTP settings |
| **MIME Types** | `mime.types` | MIME type mapping for Nginx content handling |
| **Character Encodings** | `koi-utf`, `koi-win`, `win-utf` | KOI8 Russian encoding maps and Windows UTF conversions |
| **Modules** | `modules-available/`, `modules-enabled/` | Dynamic module loading directories (typically empty in standard installs) |
| **Virtual Hosts** | `sites-available/default`, `sites-enabled/default → ../sites-available/default` | Default Nginx site configuration |
| **Common Parameters** | `fastcgi_params`, `scgi_params`, `uwsgi_params`, `proxy_params` | Parameter files for FastCGI, SCGI, uWSGI, and proxy backends |
| **Snippets** | `snippets/` (2 files) | `fastcgi-php.conf` (PHP processing), `snakeoil.conf` (self-signed SSL cert) |

**Use Case**: Lightweight alternative to Apache2 for high-traffic scenarios. Default configuration supports reverse proxying.

---

## 3. Database Services - PostgreSQL 18

| **Category** | **Files/Directories** | **Explanation** |
|---|---|---|
| **PostgreSQL Home** | `postgresql/` | PostgreSQL server configuration directory |
| **Version Config** | `postgresql/18/` | Version 18-specific PostgreSQL configurations |
| **Man Pages** | `postgresql/18/man/man1/`, `man7/` | PostgreSQL 18 utility and SQL command documentation (100+ files) |

**Included Utilities Documentation:**
- **Admin Tools**: initdb, pg_ctl, pg_dump, pg_restore, pg_upgrade, createdb, dropdb, createuser, dropuser
- **Backup/Recovery**: pg_basebackup, pg_receivewal, pg_rewind, pg_verifybackup
- **Diagnostics**: pg_amcheck, pg_test_fsync, pg_test_timing, pg_waldump
- **Database Tools**: pgbench, clusterdb, reindexdb, vacuumdb, vacuumlo

**SQL Command Documentation (200+ commands):**
- **DDL**: CREATE/ALTER/DROP (tables, views, indexes, functions, schemas, users, roles, triggers, procedures)
- **DML**: INSERT, UPDATE, DELETE, SELECT, COPY, MERGE
- **DCL**: GRANT, REVOKE
- **Transaction**: BEGIN, COMMIT, ROLLBACK, SAVEPOINT
- **Utility**: ANALYZE, VACUUM, EXPLAIN, LOCK, LISTEN, NOTIFY

---

## 4. Database Services - MySQL/MariaDB

| **Category** | **Files/Directories** | **Explanation** |
|---|---|---|
| **MySQL Config** | `mysql/` | MySQL/MariaDB service configurations |
| **MariaDB Link** | `my.cnf → /etc/mysql/mariadb.cnf` | MySQL config symlink points to MariaDB config (MariaDB is MySQL drop-in replacement) |
| **ODBC Config** | `odbc.ini`, `odbcinst.ini` | ODBC driver configuration for MySQL connectivity |
| **ODBC Sources** | `ODBCDataSources` | Registered ODBC data sources for database access |

---

## 5. Security & Access Control

### 5.1 AppArmor Mandatory Access Control

| **Category** | **Files/Directories** | **Explanation** |
|---|---|---|
| **Parser Config** | `apparmor/parser.conf` | AppArmor profile parser settings (cache, debug modes) |
| **Profile Definitions** | `apparmor.d/` | AppArmor security profiles for applications |
| **ABI Compatibility** | `apparmor.d/abi/` | Kernel ABI definitions for version compatibility (3.0, 4.0, vanilla, out-of-tree) |
| **Abstractions** | `apparmor.d/abstractions/` (100+ files) | Reusable AppArmor policy snippets for common permissions |
| **Application Profiles** | `apparmor.d/` (100+ app profiles) | Individual security profiles: 1password, apache2, dovecot, firefox, nginx, samba, ssh, sudo, systemd, etc. |

**Key Abstractions:**
- **Base System**: base, bash, consoles, authentication, crypto
- **Network**: apache2-common, cups-client, dovecot-common, dbus-network
- **Multimedia**: audio, dri-common, fonts, gtk, gnome
- **Development**: openssl, perl, python, ruby, shells
- **Services**: dconf, freedesktop.org, gio-open, gnupg, gvfs-open

### 5.2 Authentication & Authorization

| **Category** | **Files/Directories** | **Explanation** |
|---|---|---|
| **PAM Config** | `pam.conf` | Pluggable Authentication Modules master configuration |
| **PAM Services** | `pam.d/` (20+ service configs) | PAM configurations for login, SSH, sudo, FTP, cron, LightDM |
| **User Database** | `passwd`, `passwd-`, `group`, `group-`, `shadow`, `shadow-` | User/group account database (current and backup copies) |
| **Sudoers Config** | `sudoers`, `sudoers.d/` (3 additional configs) | Sudo privilege configuration: root grants, ospd-openvas permissions, kali-grant-root |
| **User Subrange** | `subuid`, `subuid-`, `subgid`, `subgid-` | User namespace UID/GID mappings for container isolation |
| **Adduser Config** | `adduser.conf` | Default settings for new user creation (shell, skeleton files, encryption) |

---

## 6. SSH Remote Access

| **Category** | **Files/Directories** | **Explanation** |
|---|---|---|
| **SSH Config** | `ssh/` | SSH server and client configuration directory |
| **SSH Key Exchange** | `ssh/moduli` | Diffie-Hellman parameter file for SSH key exchange |
| **SSH Startup** | `sv/ssh/` | Service startup script directory (runit supervision) |

**Associated Services:**
- **SSH Daemon**: Supervises SSH server with logging and startup control
- **Configuration Files**: Generated from PAM config for authentication

---

## 7. Certificate & Cryptography Management

| **Category** | **Files/Directories** | **Explanation** |
|---|---|---|
| **SSL Certificates** | `ssl/` | System-wide SSL/TLS certificate management |
| **Certificate Authority** | `ssl/certs/` (300+ CA certificates) | Trusted root and intermediate certificate authority certificates |
| **Private Keys** | `ssl/private/ssl-cert-snakeoil.key` | Self-signed testing certificate key pair |
| **OpenSSL Config** | `ssl/openssl.cnf`, `openssl.cnf.original`, `openssl.cnf.dpkg-new`, `kali.cnf` | OpenSSL certificate generation and validation configuration |
| **PKIX Configuration** | `ssl/certs/ca-certificates.crt` | Combined CA certificate bundle for validation |

**CA Types in Store:**
- **Root CAs**: 150+ trusted root authorities
- **Intermediate CAs**: Organization-specific intermediate certificates
- **Standards**: X.509 certificates for SSL/TLS, S/MIME signing

---

## 8. Cryptographic Services - StrongSwan IPSec

| **Category** | **Files/Directories** | **Explanation** |
|---|---|---|
| **StrongSwan Main** | `strongswan.conf` | Main StrongSwan configuration file |
| **Configuration Directory** | `strongswan.d/` | StrongSwan daemon configurations |
| **Charon Daemon** | `strongswan.d/charon.conf` | Main IKE/IPSec daemon configuration |
| **Charon Logging** | `strongswan.d/charon-logging.conf` | Logging settings for charon daemon |
| **Charon Modules** | `strongswan.d/charon/` (25+ module configs) | Individual plugin configurations: AES-NI, OpenSSL, X.509, SSH keys, LDAP auth |
| **Starter Config** | `strongswan.d/starter.conf` | Starter daemon for IPSec connection management |
| **IPTFS Config** | `strongswan.d/iptfs.conf` | IP Traffic Flow Security settings |

**Key StrongSwan Plugins:**
- **Cryptography**: aesni, drbg, gcm, openssl, pkcs1, pkcs7, pkcs8, pem, pubkey, random, sshkey
- **Authentication**: eap-mschapv2, xauth-generic, attr, agent
- **Networking**: kernel-netlink, socket-default, resolve, updown
- **Validation**: constraints, dnskey, revocation, x509
- **Acceleration**: nonce, stroke (CLI communication)

---

## 9. OpenVPN VPN Service

| **Category** | **Files/Directories** | **Explanation** |
|---|---|---|
| **OpenVPN Config** | `openvpn/` | OpenVPN configuration directory |
| **VPN Modes** | `openvpn/client/`, `openvpn/server/` | Separate directories for client and server VPN configs |
| **DNS Update Script** | `openvpn/update-resolv-conf` | Script to update system DNS resolvers when VPN connects |

**Use Case**: For penetration testing, provides VPN tunneling for remote access and anonymity testing.

---

## 10. OpenVAS Vulnerability Scanner

| **Category** | **Files/Directories** | **Explanation** |
|---|---|---|
| **OpenVAS Config** | `openvas/` | OpenVAS vulnerability assessment configuration |
| **Main Config** | `openvas/openvas.conf` | Primary OpenVAS settings (plugins, scan options) |
| **Logging Config** | `openvas/openvas_log.conf` | Logging levels and output configuration |
| **GPG Keys** | `openvas/gnupg/` | GPG keyring for plugin verification and signing |

**Security Features:**
- **Public Keyring**: `pubring.kbx`, `pubring.kbx~` (backup)
- **Trust Database**: `trustdb.gpg` for key trust levels
- **Private Keys**: `private-keys-v1.d/` for scanner signing keys

---

## 11. Network & Firewall Configuration

| **Category** | **Files/Directories** | **Explanation** |
|---|---|---|
| **Hostname Config** | `hostname`, `hosts` | System hostname and IP-to-hostname mapping (/etc/hosts file) |
| **DNS Config** | `resolv.conf`, `resolvconf/` | DNS resolver configuration and management |
| **Network Interface** | `network/interfaces`, `network/interfaces.d/` | Debian network interface configuration |
| **SystemD Network** | `systemd/network/` (2 configs) | SystemD networking: USB network device MAC rules |
| **NSS Switch** | `nsswitch.conf` | Name Service Switch configuration (user/group/host resolution order) |

---

## 12. System Control & Limits

| **Category** | **Files/Directories** | **Explanation** |
|---|---|---|
| **Sysctl Settings** | `sysctl.d/` | Runtime kernel parameter tuning: 30-brave.conf (Brave browser hardening) |
| **PAM Limits** | `security/limits.conf` | Resource limits for user processes (file descriptors, memory, CPU time) |
| **SystemD Settings** | `systemd/journald.conf`, `logind.conf`, `sleep.conf`, `networkd.conf`, `pstore.conf` | SystemD daemon configurations |

---

## 13. Service Supervision (Runit)

| **Category** | **Files/Directories** | **Explanation** |
|---|---|---|
| **Service Scripts** | `sv/` | Runit service supervision directory with run scripts |
| **SSH Service** | `sv/ssh/` | SSH server supervision (run, finish scripts) with logging |
| **DNSMasq Service** | `sv/dnsmasq/` | DNS/DHCP server supervision for network services |
| **PCSC Service** | `sv/pcscd/` | Smart card service supervision with control/exit handlers |

---

## 14. Penetration Testing & Exploitation Tools

| **Category** | **Files/Directories** | **Explanation** |
|---|---|---|
| **Nikto Scanner** | `nikto.conf` | Web vulnerability scanner configuration (plugin paths, output formats) |
| **Sslsplit Proxy** | `sslsplit/sslsplit.conf.sample` | SSL/TLS interception proxy configuration sample |
| **NSIS Installer** | `nsisconf.nsh` | NSIS (Nullsoft Scriptable Install System) configuration for Windows installer creation |

---

## 15. Programming Languages & Development

| **Category** | **Files/Directories** | **Explanation** |
|---|---|---|
| **PHP 8.4 Config** | `php/8.4/` | PHP 8.4 configuration directory with Apache2 and CLI settings |
| **PHP Modules** | `php/8.4/mods-available/` (20+ INI files) | Module configurations: mysqlnd, opcache, pdo, calendar, ctype, exif, ffi, ftp, iconv, mysqli, pdo_mysql, sockets, tokenizer |
| **Apache2 PHP** | `php/8.4/apache2/php.ini` | PHP settings for Apache2 module SAPI |
| **CLI PHP** | `php/8.4/cli/php.ini` | PHP settings for command-line execution |
| **Perl Config** | `perl/Net/libnet.cfg` | Perl Net module configuration (FTP timeout, firewall settings) |

---

## 16. System Logging & Auditing

| **Category** | **Files/Directories** | **Explanation** |
|---|---|---|
| **Audit Framework** | `audit/` | Linux Audit Daemon configuration |
| **Audit Rules** | `audit/audit.rules` | Kernel audit rules for system call tracking and intrusion detection |
| **Syslog Config** | `syslog-ng/` | Syslog-ng logging daemon configuration (if installed) |

---

## 17. Print & Multimedia

| **Category** | **Files/Directories** | **Explanation** |
|---|---|---|
| **CUPS Print Server** | `cups/` | CUPS printing daemon configuration |
| **Paper Specs** | `paperspecs` | Paper size definitions for printing (A4, Letter, Legal, etc.) |
| **OpenAL Audio** | `openal/alsoft.conf` | OpenAL audio library configuration (sample rate, channels, HRTF) |

---

## 18. Database & System Packages

| **Category** | **Files/Directories** | **Explanation** |
|---|---|---|
| **OpenCL Vendors** | `OpenCL/vendors/pocl.icd` | OpenCL ICD (Installable Client Driver) for Portable Computing Language |
| **OpenNI Sensors** | `openni2/OpenNI.ini` | OpenNI 2 sensor framework configuration (Kinect, etc.) |
| **OpenSC Smartcard** | `opensc/opensc.conf` | Smart card middleware configuration (PKCS#11) |

---

## 19. Package Management

| **Category** | **Files/Directories** | **Explanation** |
|---|---|---|
| **APT Config** | `apt/` | Advanced Package Tool configuration directory |
| **APT Sources** | `apt/sources.list`, `apt/sources.list.d/` | Package repository configuration for Debian/Kali packages |
| **KeyRing** | `apt/trusted.gpg.d/` | GPG keys for verifying package authenticity |
| **APT Preferences** | `apt/preferences`, `apt/preferences.d/` | Package version pinning and priority settings |

---

## 20. Session & Environment

| **Category** | **Files/Directories** | **Explanation** |
|---|---|---|
| **Environment Variables** | `environment` | System-wide environment variables |
| **Bash Configuration** | `bash.bashrc`, `bash_completion.d/` | Global Bash shell configuration and command completion scripts |
| **Shell Initialization** | `profile`, `profile.d/` | Login shell initialization (PATH, MANPATH, locale settings) |
| **Login Configuration** | `login.defs` | Login defaults (password encryption, umask, mail directory) |

---

## 21. System Information

| **Category** | **Files/Directories** | **Explanation** |
|---|---|---|
| **OS Release** | `os-release → ../usr/lib/os-release` | Operating system identification (Kali Linux, version, pretty name) |
| **FSTAB** | `fstab` | File system mount table for boot-time mounting |
| **MTAB** | `mtab` | Mounted file systems (runtime, updated by mount command) |

---

## 22. Remote Management Tools

| **Category** | **Files/Directories** | **Explanation** |
|---|---|---|
| **AnyDesk Config** | `anydesk/` | AnyDesk remote desktop service configuration: connection trace, system/service config |
| **RustDesk PAM** | `pam.d/rustdesk` | RustDesk remote desktop PAM authentication configuration |
| **XRdp Session** | `pam.d/xrdp-sesman` | Remote Desktop Protocol session manager PAM authentication |

---

## 23. Miscellaneous Configurations

| **Category** | **Files/Directories** | **Explanation** |
|---|---|---|
| **MIME Types** | `mime.types` | MIME type associations for file extensions |
| **Terminal Config** | `/etc/update-motd.d/` | Message-of-the-day scripts (dynamically generated on login) |
| **Local Modifications** | `/etc/local/` | Administrator's custom local configurations |
| **Default Preferences** | `/etc/default/` | Default settings for various system services and tools |

---

## Security-Critical Directories Summary

| **Directory** | **Security Level** | **Critical Files** | **Purpose** |
|---|---|---|---|
| `/etc/ssl/` | **CRITICAL** | Private keys, CA certificates | Encryption & authentication |
| `/etc/sudoers.d/` | **CRITICAL** | Root privilege grants | Access control |
| `/etc/apparmor.d/` | **HIGH** | Mandatory access control profiles | Security policies |
| `/etc/audit/` | **HIGH** | Audit rules | Intrusion detection |
| `/etc/ssh/` | **HIGH** | SSH server keys, moduli | Remote access security |
| `/etc/pam.d/` | **HIGH** | Authentication modules | User authentication |
| `/etc/strongswan.d/` | **MEDIUM** | VPN IPSec configuration | Encrypted tunneling |
| `/etc/openvpn/` | **MEDIUM** | VPN certificates, keys | Anonymous VPN access |
| `/etc/apache2/` | **MEDIUM** | Virtual host configs, modules | Web server security |

---

## Configuration File Statistics

| **Category** | **Count** |
|---|---|
| **Total Configuration Files** | 1000+ |
| **System Security Configs** | 150+ |
| **Database Configurations** | 100+ |
| **Web Server Configs** | 200+ (Apache2 + Nginx) |
| **Cryptographic Certificates** | 300+ CA certificates |
| **Service Supervision Scripts** | 15+ |
| **Programming Language Configs** | 50+ (PHP, Perl, Python) |

---

**Report Generated**: Complete Linux /etc System Services Configuration Analysis
**System**: Kali Linux Penetration Testing Platform
**Focus Areas**: Security hardening, service configuration, database management, web servers, VPN/tunneling
