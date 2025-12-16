# Project 2: Developer-Centric Resource Stack
## Complete Technology & Tools Guide (Development → Deployment)

**Document Version:** 1.0  
**Last Updated:** December 16, 2025  
**Audience:** Security Researchers, DevOps Engineers, Systems Engineers

---

## Table of Contents

1. [Languages & Runtimes](#languages--runtimes)
2. [Databases & Data Storage](#databases--data-storage)
3. [Containerization & Orchestration](#containerization--orchestration)
4. [Development & Testing Tools](#development--testing-tools)
5. [Security & Penetration Testing Tools](#security--penetration-testing-tools)
6. [Wireless Protocol Analysis Tools](#wireless-protocol-analysis-tools)
7. [Monitoring, Logging & Observability](#monitoring-logging--observability)
8. [CI/CD & Deployment Pipelines](#cicd--deployment-pipelines)
9. [Cloud Infrastructure](#cloud-infrastructure)
10. [Development Environment Setup](#development-environment-setup)
11. [Production Deployment Architecture](#production-deployment-architecture)
12. [Cost Estimation & Licensing](#cost-estimation--licensing)

---

## 1. Languages & Runtimes

### Primary Language: Python

| **Component** | **Technology** | **Version** | **Purpose** | **Rationale** | **License** |
|---|---|---|---|---|---|
| **Runtime** | Python | 3.11+ (LTS recommended) | Core language for all modules | Fast iteration, extensive security libs, ML ecosystem | PSF (Open) |
| **Package Manager** | pip | Latest | Dependency management | Standard, mature, integrates with PyPI | MIT |
| **Virtual Environment** | venv (stdlib) | Built-in | Project isolation | No external deps, built into Python 3.3+ | PSF |
| **Poetry** (Optional) | Poetry | 1.8+ | Advanced dependency management | Lock files, monorepo support, better reproducibility | MIT |
| **Conda** (Alternative) | Miniconda | Latest | Scientific Python distribution | Better for ML/data science, conda-forge packages | BSD |

### Secondary Languages

| **Component** | **Technology** | **Version** | **Purpose** | **Use Case** | **License** |
|---|---|---|---|---|---|
| **Performance Critical** | Cython | 3.0+ | C-level optimization | Crypto ops, packet processing loops | Apache 2.0 |
| **GPU Compute** | CUDA C/C++ | 12.4+ | GPU acceleration | Optional fuzzing speedup, ML training | Proprietary (NVIDIA) |
| **Embedded Firmware** | C/C++ | C++17 | Device firmware mocking | nRF52 test harness, mock protocol stacks | Varies |
| **Scripting** | Bash | 5.0+ | Automation scripts | Build scripts, CI/CD orchestration | GPL v3 |
| **Configuration** | YAML / TOML | Modern | Config files | Docker Compose, Poetry config, CI/CD | N/A |
| **Data Format** | JSON/Protobuf | Standard | Serialization | API responses, vulnerability reports | N/A |

### Runtime Environment

```
Development (Local):
├── Python 3.11.x (primary workstation)
├── pyenv (Python version manager)
│   └── Manage multiple Python versions seamlessly
├── direnv (environment variables)
│   └── Auto-load .env files per project
└── virtualenv (project isolation)
    └── Separate venv per project

Testing (Docker):
├── Python 3.11-slim (minimal base image)
├── Python 3.10 (compatibility testing)
└── Python 3.12 (future compatibility)

Production (Cloud):
├── Python 3.11 (AWS Lambda)
├── Python 3.12 (Kubernetes pods)
└── PyPy 7.3+ (Optional: 2-4x performance improvement)
```

**Installation Priorities:**
1. Python 3.11 LTS (guaranteed support until 2027)
2. pyenv for version management
3. Poetry for reproducible builds
4. pre-commit hooks (automated code quality checks)

---

## 2. Databases & Data Storage

### Time Series Data (Packet Captures)

| **Database** | **Format** | **Scale** | **Latency** | **Pros** | **Cons** | **Cost** | **License** | **Recommendation** |
|---|---|---|---|---|---|---|---|---|
| **InfluxDB OSS** | Time series | 10M events/sec | <10ms queries | Fast, lightweight, single binary, edge-ready, flux language | Limited clustering (OSS), memory-intensive for large datasets, proprietary cloud version | Free (OSS) / $45-$299/mo (Cloud) | AGPL v3 / Proprietary | ✅ **FIRST CHOICE** for edge packet storage |
| **InfluxDB Cloud** | Time series | Unlimited | <5ms queries | Managed, auto-scaling, multi-region, retention policies | Vendor lock-in, cost scales with ingestion, requires cloud account | Pay-per-use ($0.005/million reads) | Proprietary | ✅ **For production centralized hub** |
| **TimescaleDB** | PostgreSQL extension | 100k events/sec | <50ms | SQL compatibility, powerful aggregations, compression, hypertables | Requires PostgreSQL knowledge, setup complexity, slower than InfluxDB for metrics | Free (OSS) / $600/mo+ (Cloud) | AGPL v3 / Proprietary | ✅ **If PostgreSQL already in stack** |
| **Prometheus** | In-memory + disk | 1M samples/sec | <1s scrape | Simple setup, pull-based, built-in alerting, excellent for metrics | Not ideal for high-volume packet data, 15-day default retention | Free | Apache 2.0 | ⚠️ **Metrics only, not packets** |
| **Cassandra** | Distributed key-value | 1M+ writes/sec | <10ms | Highly scalable, fault-tolerant, write-optimized | Complex ops, overkill for single-team research, steep learning curve | Free | Apache 2.0 | ❌ **Overkill for research project** |
| **HDF5** (File-based) | Binary + metadata | 10GB+ single file | <100ms per query | Excellent compression, scientific standard, hierarchical, supports 1TB+ files | Not a database (file format), requires custom Python code for queries, no concurrent writes | Free | Custom (BSD-like) | ✅ **For offline PCAP storage alongside InfluxDB** |
| **SQLite** | Embedded SQL | 10M rows | <100ms | Zero setup, serverless, excellent for testing, local caching | Not suitable for high-throughput streaming, single-writer limitation | Free | Public Domain | ✅ **For development/testing only** |
| **MongoDB** | NoSQL document | 100k ops/sec | <50ms | Flexible schema, JSON-native, good for metadata, horizontal scaling | Overkill for time series, slower than InfluxDB for metrics | Free (Community) / $57+/mo (Cloud) | SSPL / Proprietary | ⚠️ **For metadata only, not time series** |

### Recommended Hybrid Approach

**Architecture:**
```
Development Environment:
├── SQLite (local testing)
├── HDF5 files (small packet datasets)
└── InfluxDB OSS (if testing time series)

Edge Deployment (Raspberry Pi):
├── InfluxDB OSS (packet storage)
│   └── ~500MB memory for 1M packets
├── HDF5 dumps (long-term archive)
└── Telegraf (optional data collection)

Production (Cloud):
├── InfluxDB Cloud (centralized time series)
│   ├── Real-time packet ingestion
│   ├── Flux queries for analysis
│   └── Auto-retention policies
├── PostgreSQL (TimescaleDB) (optional: rich queries)
├── S3/Azure Blob (archive old data)
└── Elasticsearch (optional: full-text search on metadata)
```

### Database Sizing Calculator

| **Scenario** | **Packet Rate** | **Duration** | **Storage** | **DB Choice** |
|---|---|---|---|---|
| Local testing | 100 pkt/sec | 1 hour | 360MB | SQLite + HDF5 |
| Small device test | 1K pkt/sec | 8 hours | 28GB | InfluxDB OSS |
| Large-scale fuzz | 10K pkt/sec | 24 hours | 864GB | InfluxDB Cloud + S3 archive |
| Production hub | 1M pkt/sec | 30 days | 2.5TB | InfluxDB Cloud + TimescaleDB + S3 |

---

## 3. Containerization & Orchestration

### Container Runtime

| **Technology** | **Version** | **Purpose** | **Pros** | **Cons** | **License** | **Use Case** |
|---|---|---|---|---|---|---|
| **Docker** | 25.0+ | Standard container runtime | Industry standard, excellent tooling, large ecosystem | Slightly slower than containerd, more resource overhead | Apache 2.0 / Commercial | ✅ **Development & Testing** |
| **containerd** | 1.7+ | Lightweight runtime | Faster startup, lower overhead, CNCF project, Kubernetes-native | Less user-friendly, fewer tools | Apache 2.0 | ✅ **Production (Kubernetes)** |
| **Podman** | 5.0+ | Rootless containers | No daemon process, rootless-by-default, Docker-compatible CLI | Newer (less community), fewer advanced features | Apache 2.0 | ⚠️ **Linux-only alternative** |

### Container Orchestration

| **Platform** | **Scale** | **Complexity** | **Setup Time** | **Pros** | **Cons** | **License** | **Recommendation** |
|---|---|---|---|---|---|---|---|
| **Docker Compose** | Single host | Low | <30 min | Simple, perfect for dev/test, official Docker support | Only local/single-host, no clustering | Apache 2.0 | ✅ **Development & small tests** |
| **Kubernetes (K3s)** | Multi-host | High | 2-4 hours | Production-grade, auto-scaling, self-healing, CNCF standard | Steep learning curve, overkill for small team, resource-intensive | Apache 2.0 | ✅ **Production multi-site deployment** |
| **Kubernetes (EKS)** | Cloud-managed | Medium | 1 hour | Fully managed, AWS-integrated, auto-patching, high availability | AWS vendor lock-in, costs scale quickly, IAM complexity | Proprietary | ✅ **Production on AWS** |
| **Docker Swarm** | Multi-host | Medium | 1-2 hours | Simple distributed setup, Docker CLI-native, low overhead | Less mature than K8s, smaller ecosystem, declining adoption | Apache 2.0 | ⚠️ **If K8s too complex** |
| **OpenShift** | Enterprise | Very High | 8+ hours | Enterprise Kubernetes, enhanced security, Red Hat support | Very expensive, vendor lock-in, over-featured for research | Proprietary | ❌ **Overkill for research** |

### Recommended Container Stack

**Development (Local):**
```yaml
docker-compose.yml:
  ├── wireless-analyzer (main app service)
  │   └── Python 3.11 slim + dependencies
  ├── influxdb (time series database)
  │   └── InfluxDB OSS
  ├── postgres (optional: metadata)
  │   └── PostgreSQL 15
  ├── redis (caching/job queue)
  │   └── Redis 7.0+
  └── monitor (optional: observability)
      └── Prometheus + Grafana
```

**Production (Cloud/Edge):**
```yaml
Kubernetes Deployment:
  ├── wireless-analyzer pod (multi-replica)
  │   ├── Resource limits: 2CPU, 2GB RAM
  │   ├── Horizontal pod autoscaler
  │   └── Rolling update strategy
  ├── influxdb statefulset
  │   ├── Persistent volume (storage class)
  │   └── Backup sidecar
  ├── network policies
  │   ├── Ingress from load balancer only
  │   └── Egress: restricted to APIs
  └── monitoring (Prometheus + Loki)
      ├── Scrape endpoints
      └── Log aggregation
```

### Container Image Best Practices

```dockerfile
# Development Image (debug-friendly)
FROM python:3.11-slim as dev
# Includes: pytest, ipython, debugging tools
# Size: ~500MB
# Use: docker compose up

# Production Image (optimized)
FROM python:3.11-slim as prod
# Minimal: only runtime dependencies
# Multi-stage build (slim down to ~200MB)
# Health checks included
# Non-root user (security)
# Use: Kubernetes manifests
```

---

## 4. Development & Testing Tools

### Code Quality & Linting

| **Tool** | **Purpose** | **Integration** | **Config File** | **Speed** | **License** | **Priority** |
|---|---|---|---|---|---|---|
| **black** | Code formatter (PEP 8) | Pre-commit hook, CI | pyproject.toml | Fast | MIT | ✅ MUST |
| **isort** | Import sorter | Pre-commit hook, CI | pyproject.toml | Very fast | MIT | ✅ MUST |
| **ruff** | Fast linter (Pylint replacement) | Pre-commit hook, CI | pyproject.toml | Very fast (100x faster) | MIT | ✅ MUST |
| **mypy** | Static type checker | Pre-commit hook, CI | mypy.ini | Medium | MIT | ✅ MUST |
| **pylint** | Thorough linting | CI only (slower) | .pylintrc | Slow | GPL v2 | ⚠️ OPTIONAL |
| **bandit** | Security linter | CI pipeline | .bandit | Fast | Apache 2.0 | ✅ MUST |
| **semgrep** | Semantic code analysis | CI pipeline | .semgrep.yml | Medium | LGPL v2.1 | ✅ MUST |
| **SonarQube** | Code quality dashboard | CI pipeline | sonar-project.properties | Slow | AGPL v3 / Commercial | ⚠️ OPTIONAL |

**Recommended Configuration (.pre-commit-config.yaml):**
```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 24.1.1
    hooks:
      - id: black
  - repo: https://github.com/PyCQA/isort
    rev: 5.13.2
    hooks:
      - id: isort
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.9
    hooks:
      - id: ruff
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.5
    hooks:
      - id: bandit
```

### Testing Framework

| **Tool** | **Type** | **Features** | **Speed** | **Syntax** | **License** | **Priority** |
|---|---|---|---|---|---|---|
| **pytest** | Unit/Integration | Fixtures, plugins, parametrized tests, coverage | Fast | Simple decorators | MIT | ✅ MUST |
| **pytest-cov** | Coverage | Line/branch coverage, HTML reports | Fast | Plugin to pytest | MIT | ✅ MUST |
| **hypothesis** | Property-based | Auto test case generation, shrinking | Medium | Function decoration | MPL 2.0 | ✅ RECOMMENDED |
| **pytest-benchmark** | Performance | Latency tracking, regression detection | Medium | Plugin to pytest | MIT | ✅ RECOMMENDED |
| **pytest-asyncio** | Async testing | Async/await support | Fast | Plugin to pytest | MIT | ⚠️ IF ASYNC |
| **tox** | Multi-environment | Test across Python 3.10/3.11/3.12 | Slow | tox.ini config | MIT | ✅ RECOMMENDED |
| **coverage.py** | Coverage tracking | Detailed HTML/XML reports, branch coverage | Fast | Standalone + pytest plugin | Apache 2.0 | ✅ MUST |
| **locust** | Load testing | Distributed load generation, web UI | Medium | Python DSL | MIT | ⚠️ FOR STRESS TESTING |

**Test Organization:**
```
tests/
├── unit/                          # Fast, isolated tests
│   ├── test_parser.py
│   ├── test_crypto.py
│   └── test_fuzzer.py
├── integration/                   # Slower, component tests
│   ├── test_e2e_capture.py
│   └── test_hardware_integration.py
├── performance/                   # Benchmarks
│   └── test_throughput.py
├── fixtures/                      # Test data
│   ├── pcap_samples/
│   └── mock_responses/
└── conftest.py                    # Pytest configuration
```

### Debugging & Profiling

| **Tool** | **Purpose** | **Usage** | **Overhead** | **License** | **Use Case** |
|---|---|---|---|---|---|
| **pdb** (stdlib) | Python debugger | CLI breakpoints, step through code | Low | PSF | ✅ **Development** |
| **ipdb** | Enhanced pdb | Better UI, syntax highlighting | Low | BSD | ✅ **Development** |
| **breakpoint()** (stdlib) | Built-in debug entry | Python 3.7+ feature | Low | PSF | ✅ **Code injection** |
| **pudb** | Full-screen debugger | TUI-based debugging | Low | MIT | ✅ **SSH debugging** |
| **cProfile** (stdlib) | Performance profiling | Function-level timing | Low | PSF | ✅ **Optimization** |
| **py-spy** | Live profiler | Non-intrusive sampling profiler | Very low | Apache 2.0 | ✅ **Production debugging** |
| **memory_profiler** | Memory tracking | Line-by-line memory consumption | High | BSD | ✅ **Memory leaks** |
| **tracemalloc** (stdlib) | Memory snapshot | Top memory allocations | Low | PSF | ✅ **Memory debugging** |

**Profiling Command:**
```bash
# Function-level timing
python -m cProfile -s cumulative script.py

# Memory profiling
python -m memory_profiler script.py

# Live profiling (no code changes)
py-spy record -o profile.svg -- python script.py

# Flamegraph generation
py-spy record -o profile.json -- python script.py
# (convert with https://www.speedscope.app/)
```

---

## 5. Security & Penetration Testing Tools

### Wireless Security Tools

| **Tool** | **Category** | **Protocol** | **Platform** | **Price** | **License** | **Use in Project** |
|---|---|---|---|---|---|---|
| **Ubertooth One** | Hardware sniffer | BLE | Linux/Windows/Mac | $60 hardware | GPL v2 (firmware) | ✅ **Primary BLE capture** |
| **ApiMote v4** | Hardware sniffer | 802.15.4/Zigbee | Linux/Windows | $150 hardware | GPL v2 (firmware) | ✅ **Primary Zigbee capture** |
| **nRF52840 DK** | Dev kit | BLE + Zigbee | Linux/Windows/Mac | $100-200 | Nordic License | ✅ **Fuzzing target + analysis** |
| **Nordic nRF Connect** | BLE suite | BLE | Linux/Windows/Mac/Web | Free (basic) / $400+ (pro) | Proprietary | ✅ **BLE analysis + dev** |
| **Wireshark + Plugins** | Protocol analyzer | Multi-protocol | Linux/Windows/Mac | Free | GPL v2 | ✅ **PCAP visualization** |
| **tshark** | CLI packet analyzer | Multi-protocol | Linux/Windows/Mac | Free | GPL v2 | ✅ **Automated packet analysis** |
| **tcpdump** | Packet capture tool | Network protocols | Linux/Mac | Free | BSD | ⚠️ **Low-level debugging** |
| **Scapy** | Python library | Multi-protocol | Cross-platform | Free | GPL v2 | ✅ **Packet crafting/fuzzing** |
| **Burp Suite Community** | Web proxy | HTTP/HTTPS | Linux/Windows/Mac | Free | Proprietary | ⚠️ **API testing only** |
| **OWASP ZAP** | Security scanner | Web | Linux/Windows/Mac | Free | Apache 2.0 | ⚠️ **API security scanning** |

### Kali Linux Tools (Pre-installed)

| **Category** | **Tools** | **Usage in Project** |
|---|---|---|
| **Sniffer/Analyzer** | Wireshark, tshark, tcpdump | ✅ Packet analysis |
| **Wireless** | airmon-ng, airodump-ng, aircrack-ng | ⚠️ WiFi (optional) |
| **Packet Craft** | Scapy, hping3, packetgen | ✅ Packet generation |
| **Exploitation** | Metasploit, sqlmap, nikto | ❌ Not needed |
| **Reverse Engineering** | radare2, ghidra, objdump | ⚠️ Firmware analysis |
| **Reporting** | fluxion, beef | ❌ Not needed |

**Recommended:** Use **Kali Linux VM** in VirtualBox/Proxmox for isolated testing, NOT as primary workstation.

### Vulnerability Scanning

| **Tool** | **Scope** | **Input** | **Output** | **License** | **Use** |
|---|---|---|---|---|---|
| **Bandit** | Python code | Source code | JSON/CSV | Apache 2.0 | ✅ **Pre-commit** |
| **Trivy** | Container images | Docker images | JSON/SARIF | Apache 2.0 | ✅ **Build pipeline** |
| **Grype** | Dependencies | SBOM/packages | JSON/Table | Apache 2.0 | ✅ **Dependency scan** |
| **OWASP Dependency-Check** | Dependencies | Project files | HTML/XML | Apache 2.0 | ✅ **Dependency audit** |
| **Snyk** | Full stack | Code + dependencies | Web dashboard | Proprietary (Free tier) | ⚠️ **Optional** |
| **SonarQube** | Code quality + security | Source code | Web dashboard | AGPL v3 (Community) | ⚠️ **CI pipeline** |

---

## 6. Wireless Protocol Analysis Tools

### BLE-Specific Tools

| **Tool** | **Purpose** | **Language** | **Setup** | **License** | **In Project** |
|---|---|---|---|---|---|
| **BLEAK** | Python BLE library | Python | pip install | MIT | ✅ **MOD-002** |
| **Bettercap** | Wireless framework | Go | Single binary | GPL v3 | ✅ **Analysis** |
| **BTStackProfiler** | BLE profiling | C | Compiled | Proprietary | ⚠️ **Timing analysis** |
| **Nordic DevZone** | Community tools | Various | Web-based | Proprietary | ⚠️ **Reference** |

### Zigbee-Specific Tools

| **Tool** | **Purpose** | **Language** | **Setup** | **License** | **In Project** |
|---|---|---|---|---|---|
| **KillerBee** | Zigbee penetration | Python | pip install | GPL v3 | ✅ **MOD-001/004** |
| **Scapy ZigBee** | Zigbee packets | Python | Scapy layer | GPL v2 | ✅ **MOD-002** |
| **Z3c** | Zigbee frame parser | Python | pip install | MIT | ✅ **MOD-002** |
| **Zigbee2MQTT** | Zigbee bridge | Node.js | Docker | AGPL v3 | ⚠️ **Test devices** |

### Protocol Definition Languages

| **Tool** | **Format** | **Purpose** | **License** | **Use** |
|---|---|---|---|---|
| **Scapy Layers** | Python classes | Packet definitions | GPL v2 | ✅ **MOD-002** |
| **Construct** | DSL | Binary format parsing | MIT | ✅ **Alternative parser** |
| **Kaitai Struct** | YAML | Binary format spec | MIT | ✅ **Parser generation** |
| **Protobuf** | .proto files | Message serialization | Apache 2.0 | ✅ **Config/metadata** |

---

## 7. Monitoring, Logging & Observability

### Application Monitoring

| **Component** | **Tool** | **Purpose** | **Data** | **License** | **Cost** | **Use** |
|---|---|---|---|---|---|---|
| **Metrics Collection** | Prometheus | Time series metrics | CPU, memory, custom | Apache 2.0 | Free | ✅ **System metrics** |
| **Metrics Collection** | Telegraf | Data collector | Multi-source | AGPL v3 | Free | ✅ **IoT device metrics** |
| **Metrics Visualization** | Grafana | Dashboard creation | Prometheus/InfluxDB data | AGPL v3 | Free (OSS) / $29+/mo (Cloud) | ✅ **Dashboards** |
| **Alerting** | AlertManager | Alert routing | Prometheus alerts | Apache 2.0 | Free | ✅ **Incident alerts** |
| **Tracing** | Jaeger | Distributed tracing | Request traces | Apache 2.0 | Free | ⚠️ **Advanced debugging** |
| **APM** | DataDog | Full observability | All telemetry | Proprietary | $15+/host/month | ⚠️ **Enterprise only** |

### Logging & Log Aggregation

| **Component** | **Tool** | **Purpose** | **Processing** | **License** | **Cost** | **Use** |
|---|---|---|---|---|---|---|
| **Log Aggregation** | Loki | Log aggregation | Label-based indexing | AGPL v3 | Free | ✅ **Container logs** |
| **Log Shipper** | Promtail | Send logs to Loki | Parse and ship | AGPL v3 | Free | ✅ **Pod logs** |
| **Full Stack** | ELK Stack | Elasticsearch + Logstash + Kibana | Full-text search | AGPL v3 (Elasticsearch) | Free (OSS) / $55+/mo (Cloud) | ✅ **Production logging** |
| **Alternative** | Splunk | Centralized logging | Advanced indexing | Proprietary | $100+/GB/day | ⚠️ **Enterprise only** |
| **Log Parser** | Fluent Bit | Lightweight log collection | JSON/parsing | Apache 2.0 | Free | ✅ **Edge devices** |
| **Structured Logs** | structlog | Python logging library | JSON output | MIT / Apache 2.0 | Free | ✅ **Application logs** |

### Recommended Observability Stack (Dev → Prod)

**Development (Local Docker Compose):**
```yaml
monitoring:
  prometheus:        # Metrics scraping
  grafana:           # Dashboards
  loki:              # Log aggregation
  promtail:          # Log shipper
```

**Production (Kubernetes):**
```yaml
monitoring-stack:
  prometheus:        # Multi-target scraping
  grafana:           # Cross-cluster dashboards
  loki:              # Centralized logs
  promtail:          # Pod log collection
  alertmanager:      # Alert routing
  jaeger:            # Distributed tracing (optional)
```

---

## 8. CI/CD & Deployment Pipelines

### CI/CD Platform

| **Platform** | **Integration** | **Pricing** | **Complexity** | **License** | **Recommendation** |
|---|---|---|---|---|---|
| **GitHub Actions** | Native GitHub | Free (2000 min/month) | Low | Proprietary | ✅ **FIRST CHOICE** |
| **GitLab CI/CD** | GitLab native | Free (10 min/month) | Medium | MIT (Community) | ✅ **If GitLab** |
| **Jenkins** | Self-hosted | Free | High | MIT | ⚠️ **If on-prem only** |
| **CircleCI** | Multi-VCS | $75+/month | Low | Proprietary | ⚠️ **Optional** |
| **Travis CI** | GitHub/GitLab | $150+/month | Low | Proprietary | ❌ **Too expensive** |
| **Tekton** | Kubernetes-native | Free | Very High | Apache 2.0 | ⚠️ **If K8s heavy** |

### Recommended CI/CD Pipeline (GitHub Actions)

```yaml
# .github/workflows/ci.yml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.10, 3.11, 3.12]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
      
      # Linting
      - run: pip install black isort ruff mypy bandit
      - run: black --check src/
      - run: isort --check src/
      - run: ruff check src/
      - run: mypy src/
      - run: bandit -r src/
      
      # Testing
      - run: pip install -e .[dev]
      - run: pytest -v --cov=src/ tests/
      - run: coverage report --fail-under=85
      
      # Security scan
      - run: pip install trivy grype
      - run: trivy image --severity HIGH $(docker images -q)
      
      # Build & push (on main)
      - if: github.ref == 'refs/heads/main'
        uses: docker/build-push-action@v5
        with:
          push: true
          tags: ${{ secrets.DOCKER_REGISTRY }}/wireless-analyzer:latest
```

### Deployment Tools

| **Tool** | **Target** | **Configuration** | **License** | **Use** |
|---|---|---|---|---|
| **Docker CLI** | Container registry | YAML | Apache 2.0 | ✅ **Build & push** |
| **kubectl** | Kubernetes cluster | YAML manifests | Apache 2.0 | ✅ **K8s deployment** |
| **Helm** | Kubernetes packages | Helm charts | Apache 2.0 | ✅ **K8s package management** |
| **ArgoCD** | GitOps | Git repository | Apache 2.0 | ✅ **Production sync** |
| **Terraform** | Infrastructure as Code | .tf files | MPL 2.0 | ✅ **Cloud infrastructure** |
| **Ansible** | Server provisioning | .yml playbooks | GPL v3 | ⚠️ **If on-prem** |
| **CloudFormation** | AWS-specific | JSON/YAML | AWS proprietary | ✅ **If AWS-only** |

---

## 9. Cloud Infrastructure

### Cloud Provider Options

| **Provider** | **Ideal For** | **Pricing Model** | **Free Tier** | **Recommendation** |
|---|---|---|---|---|
| **AWS** | Enterprise, scalability | Per-service pay-as-you-go | 12 months free ($100 value) | ✅ **Recommended** |
| **Google Cloud** | ML/data-heavy | Per-service + sustained discounts | $300 credit 90 days | ✅ **If heavy ML** |
| **Azure** | Microsoft ecosystem | Per-service + Microsoft licensing | $200 credit 30 days | ⚠️ **If enterprise** |
| **DigitalOcean** | Simplicity + cost | Flat-rate App Platform | $200 credit | ✅ **Budget option** |
| **Linode** | Simple compute | Flat rates | $100 credit | ✅ **Budget option** |
| **Self-hosted** | Data sovereignty | Upfront hardware + ops | None | ⚠️ **On-prem only** |

### AWS Services (Recommended Stack)

| **Service** | **Purpose** | **Tier** | **Cost/Month** | **Integration** |
|---|---|---|---|---|
| **ECR** | Container registry | Included | ~$5/GB stored | Docker push/pull |
| **ECS/EKS** | Container orchestration | ECS free tier / EKS $0.10/hour | $0-200 | K8s deployment |
| **RDS** | Managed PostgreSQL | db.t3.micro free 12mo | $10-100 | TimescaleDB option |
| **Lambda** | Serverless compute | 1M requests free/month | $0.20/1M requests | Event-driven processing |
| **S3** | Object storage | 5GB free tier | $0.023/GB | Packet archive |
| **CloudWatch** | Monitoring + logs | Partial free tier | $0.50-5 logs/GB | Observability |
| **InfluxDB Cloud** | Time series | Free tier | $45-300/month | Managed time series |
| **SageMaker** | ML model training | On-demand pricing | $0.10-1/hour | Optional: ML training |

**Estimated Monthly Cost (Development → Production):**
- **Dev (single EC2):** $10-20/month
- **Staging (RDS + ECS):** $50-100/month
- **Production (K8s + monitoring):** $200-500/month

---

## 10. Development Environment Setup

### Local Workstation Setup

**Operating System:** Arch Linux (Garuda XFCE) / Ubuntu 24.04 LTS / macOS

```bash
# 1. Python Setup
curl https://pyenv.run | bash  # Install pyenv
pyenv install 3.11.9
pyenv global 3.11.9

# 2. Project Setup
git clone <repo>
cd wireless-protocol-security-analysis
python -m venv venv
source venv/bin/activate
pip install --upgrade pip setuptools wheel

# 3. Dependencies
pip install -r requirements-dev.txt
# Includes: pytest, black, isort, ruff, mypy, bandit, sphinx, jupyter

# 4. Pre-commit Hooks
pip install pre-commit
pre-commit install
pre-commit run --all-files  # Validate setup

# 5. Hardware Setup (if available)
# Ubertooth: Follow ubertooth-utils installation
# ApiMote: Follow River Loop Security documentation
# nRF: Install nRF Command Line Tools

# 6. Docker Setup
docker --version  # Verify Docker installed
docker-compose --version
docker pull python:3.11-slim
```

### IDE Configuration (VS Code)

```json
// .vscode/settings.json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/venv/bin/python",
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": false,
  "python.linting.flake8Enabled": true,
  "python.formatting.provider": "black",
  "python.formatting.blackArgs": ["--line-length", "100"],
  "[python]": {
    "editor.formatOnSave": true,
    "editor.defaultFormatter": "ms-python.python",
    "editor.codeActionsOnSave": {
      "source.organizeImports": true
    }
  },
  "pylance.analysis.extraPaths": ["./src"],
  "mypy-type-checker.reportGeneralTypeIssues": "warning"
}
```

### Docker Setup (for testing)

```dockerfile
# Dockerfile (development)
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    libssl-dev \
    libusb-1.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy dependencies
COPY requirements.txt requirements-dev.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt -r requirements-dev.txt

# Copy source
COPY src/ src/
COPY tests/ tests/

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import wireless_protocol_analyzer; print('OK')"

CMD ["pytest", "-v"]
```

### Development Workflow Commands

```bash
# Code quality check (pre-commit)
pre-commit run --all-files

# Run tests
pytest -v --cov=src/ tests/

# Specific test category
pytest tests/unit/ -v                    # Unit tests only
pytest tests/integration/ -v             # Integration tests
pytest tests/ -k "crypto" -v             # Tests matching pattern

# Generate coverage report
coverage report -m
coverage html  # Open htmlcov/index.html

# Profile code
python -m cProfile -s cumulative script.py

# Debug with ipdb
pytest --pdb tests/test_parser.py

# Build Docker image
docker build -t wireless-analyzer:dev .

# Run Docker container
docker-compose up  # Full stack
docker-compose up -d analyzer  # Single service

# Interactive shell in container
docker exec -it <container_id> bash
```

---

## 11. Production Deployment Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Edge Devices (Raspberry Pi)               │
│  ┌──────────────┐        ┌──────────────┐                   │
│  │ Ubertooth    │───────▶│ Analyzer Pod │                   │
│  └──────────────┘        └──────┬───────┘                   │
│  ┌──────────────┐               │                           │
│  │ ApiMote      │───────────────┘                           │
│  └──────────────┘         │                                 │
│                      ┌────▼────┐                            │
│                      │InfluxDB  │                           │
│                      │OSS (Edge)│                           │
│                      └────┬─────┘                           │
│                           │ (HTTP sync)                     │
└───────────────────────────┼──────────────────────────────────┘
                            │
                    ┌───────▼────────┐
                    │   VPN Tunnel   │
                    │   (WireGuard)  │
                    └───────┬────────┘
                            │
      ┌─────────────────────┼─────────────────────┐
      │          AWS Cloud (Production)           │
      │  ┌───────────────────────────────────────┐│
      │  │    Load Balancer (Application LB)     ││
      │  └───────────────┬───────────────────────┘│
      │                 │                         │
      │  ┌──────────────▼────────────────────────┐│
      │  │    Kubernetes Cluster (EKS)          ││
      │  │  ┌────────────┐  ┌────────────┐     ││
      │  │  │Analyzer Pod│  │Analyzer Pod│ ... ││
      │  │  └────────────┘  └────────────┘     ││
      │  │  ┌────────────────────────────────┐ ││
      │  │  │ InfluxDB StatefulSet (Cloud)   │ ││
      │  │  └────────────────────────────────┘ ││
      │  └──────────────────────────────────────┘│
      │                                          │
      │  ┌───────────────────────────────────────┤
      │  │    S3 (Archive)                       │
      │  │    + Backup (cross-region)            │
      │  └───────────────────────────────────────┤
      │                                          │
      │  ┌───────────────────────────────────────┤
      │  │    Monitoring Stack (Prometheus)      │
      │  │    Logging (Loki) + Dashboards        │
      │  └───────────────────────────────────────┤
      │                                          │
      └──────────────────────────────────────────┘
```

### Kubernetes Deployment Files

**Namespace & RBAC:**
```yaml
# k8s/00-namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: wireless-analyzer
  labels:
    name: wireless-analyzer
---
# k8s/01-rbac.yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: analyzer
  namespace: wireless-analyzer
```

**Deployment:**
```yaml
# k8s/02-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: wireless-analyzer
  namespace: wireless-analyzer
spec:
  replicas: 3
  selector:
    matchLabels:
      app: wireless-analyzer
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  template:
    metadata:
      labels:
        app: wireless-analyzer
    spec:
      containers:
      - name: analyzer
        image: 123456789.dkr.ecr.us-east-1.amazonaws.com/wireless-analyzer:v1.0.0
        imagePullPolicy: IfNotPresent
        ports:
        - containerPort: 8000
          name: http
        resources:
          requests:
            cpu: 500m
            memory: 512Mi
          limits:
            cpu: 2000m
            memory: 2Gi
        env:
        - name: INFLUXDB_URL
          value: http://influxdb:8086
        - name: LOG_LEVEL
          value: INFO
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 5
        securityContext:
          runAsNonRoot: true
          runAsUser: 1000
          readOnlyRootFilesystem: true
          allowPrivilegeEscalation: false
      securityContext:
        fsGroup: 1000
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchExpressions:
                - key: app
                  operator: In
                  values:
                  - wireless-analyzer
              topologyKey: kubernetes.io/hostname
```

**Service:**
```yaml
# k8s/03-service.yaml
apiVersion: v1
kind: Service
metadata:
  name: wireless-analyzer
  namespace: wireless-analyzer
spec:
  type: LoadBalancer
  selector:
    app: wireless-analyzer
  ports:
  - port: 80
    targetPort: 8000
    protocol: TCP
    name: http
```

**HPA (Auto-scaling):**
```yaml
# k8s/04-hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: wireless-analyzer
  namespace: wireless-analyzer
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: wireless-analyzer
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

### Infrastructure as Code (Terraform)

```hcl
# terraform/main.tf
provider "aws" {
  region = var.aws_region
}

# VPC & Networking
module "vpc" {
  source = "./modules/vpc"
  cidr_block = var.vpc_cidr
}

# EKS Cluster
module "eks" {
  source = "./modules/eks"
  vpc_id = module.vpc.id
  cluster_version = "1.29"
}

# RDS (TimescaleDB)
module "rds" {
  source = "./modules/rds"
  vpc_security_group_ids = [aws_security_group.rds.id]
  db_instance_class = "db.t3.micro"
}

# S3 Bucket (archive)
resource "aws_s3_bucket" "packet_archive" {
  bucket = "wireless-analyzer-archive-${var.environment}"
  
  lifecycle_rule {
    id = "archive"
    transition {
      days = 30
      storage_class = "GLACIER"
    }
  }
}

# CloudWatch (monitoring)
module "monitoring" {
  source = "./modules/monitoring"
  cluster_name = module.eks.cluster_name
}
```

---

## 12. Cost Estimation & Licensing

### Development Phase (0-3 months)

| **Resource** | **Type** | **Quantity** | **Unit Cost** | **Monthly** | **Total** |
|---|---|---|---|---|---|
| Developer (1 FTE) | Labor | 1 | $4,000 | $4,000 | $12,000 |
| Laptop / Workstation | Hardware | 1 | $0 | $0 | $0 |
| GitHub Pro | Software | 1 seat | $4/mo | $4 | $12 |
| Docker Desktop | Software | 1 seat | $0 (free) | $0 | $0 |
| Wireless Hardware | Hardware | $430 total | $0 | $0 | $430 |
| AWS Dev Tier | Infrastructure | $100 credit | -$100 | ~$50 (after credit) | $150 |
| **Total (3 months)** | | | | **$4,054/mo** | **$12,592** |

### Testing Phase (3-6 months)

| **Resource** | **Type** | **Quantity** | **Unit Cost** | **Monthly** | **Total |
|---|---|---|---|---|---|
| Developer (1 FTE) | Labor | 1 | $4,000 | $4,000 | $12,000 |
| CI/CD (GitHub Actions) | Software | Unlimited | Free | $0 | $0 |
| InfluxDB Cloud | Database | 10M points/month | $45 | $45 | $135 |
| AWS (small EC2 + data) | Infrastructure | t3.small | ~$30 | $30 | $90 |
| Container Registry (ECR) | Infrastructure | $5/month | $5 | $5 | $15 |
| **Total (3 months)** | | | | **$4,080/mo** | **$12,240** |

### Production Phase (6 months+)

| **Resource** | **Type** | **Quantity** | **Unit Cost** | **Monthly** | **Recurring** |
|---|---|---|---|---|---|
| Developer (Maintenance) | Labor | 0.5 FTE | $2,000 | $2,000 | $24,000/yr |
| Kubernetes (EKS) | Infrastructure | 3 nodes | $0.10/hr + instance cost | $150-300 | Ongoing |
| InfluxDB Cloud | Database | 100M points/month | $299 | $299 | Ongoing |
| RDS (db.t3.small) | Database | 1 instance | $0.025/hr + storage | $20-50 | Ongoing |
| S3 (100GB storage) | Storage | 100GB | $0.023/GB | $2-5 | Ongoing |
| Data Transfer | Networking | 1TB/month | $0.09/GB out | $90 | Ongoing |
| Monitoring (CloudWatch) | Observability | Pay-per-use | ~$50 | $50 | Ongoing |
| **Total (Monthly Production)** | | | | **$2,610-2,800** | **~$31,000-33,600/yr** |

### Open-Source Licensing Analysis

| **Component** | **License** | **Commercial Use** | **Proprietary Code** | **Issue** |
|---|---|---|---|---|---|
| **Scapy** | GPL v2 | ✅ Yes | ❌ Must release | Copyleft |
| **Wireshark** | GPL v2 | ✅ Yes | ❌ Must release | Copyleft |
| **InfluxDB OSS** | AGPL v3 | ✅ Yes (if SaaS) | ❌ Must release | Strong copyleft |
| **Python** | PSF | ✅ Yes | ✅ Proprietary OK | Permissive |
| **Docker** | Apache 2.0 | ✅ Yes | ✅ Proprietary OK | Permissive |
| **Kubernetes** | Apache 2.0 | ✅ Yes | ✅ Proprietary OK | Permissive |

**Recommendation:** Publish under **Apache 2.0** for maximum compatibility + commercial appeal.

---

## Summary: Recommended Tech Stack

### MUST-HAVE (Non-negotiable)

```
Development:
├── Python 3.11 LTS
├── pytest + pytest-cov (testing)
├── Docker + docker-compose (environment)
├── GitHub + GitHub Actions (CI/CD)
├── Scapy + custom protocols (packet crafting)
└── InfluxDB OSS (time series)

Hardware:
├── Ubertooth One ($60)
├── ApiMote v4 ($150)
└── nRF52840 DK ($100-200)

Tools:
├── Wireshark (analysis)
├── Kali Linux VM (testing)
└── VS Code (IDE)
```

### RECOMMENDED (Strongly advised)

```
Development:
├── mypy + ruff (code quality)
├── pre-commit (quality gates)
├── hypothesis (property testing)
├── Poetry (reproducible builds)
└── Sphinx + MkDocs (documentation)

Infrastructure:
├── Docker for local testing
├── AWS free tier (development)
├── Kubernetes for production
└── Prometheus + Grafana (monitoring)

Tools:
├── Bandit (security scanning)
├── Trivy (container scanning)
└── py-spy (performance debugging)
```

### OPTIONAL (If time/budget permits)

```
Development:
├── SonarQube (code dashboard)
├── Locust (load testing)
└── Snyk (dependency scanning)

Infrastructure:
├── RDS + TimescaleDB (rich queries)
├── S3 + CloudFront (content delivery)
├── ArgoCD (GitOps deployment)
└── ELK Stack (advanced logging)

Hardware:
├── NVIDIA Jetson Orin (GPU acceleration)
├── Saleae Logic Analyzer (timing validation)
└── LoRA dongle (Thread/Matter analysis)
```

---

**Procurement Checklist:**

- [ ] GitHub Pro ($4/mo)
- [ ] Wireless hardware ($430 one-time)
- [ ] AWS account setup
- [ ] Docker Desktop installation
- [ ] Code editor (VS Code)
- [ ] Kali Linux ISO (free)
- [ ] Network equipment (managed switch optional)
- [ ] Virtual machine hypervisor (VirtualBox free)

**Timeline to Production Readiness:**
- **Weeks 1-2:** All MUST-HAVE tools
- **Weeks 3-5:** RECOMMENDED tools
- **Weeks 6+:** OPTIONAL infrastructure

---

**Document End**

**Questions to Clarify (if any)?**

1. **AWS account setup:** Do you have existing AWS credits or enterprise account?
2. **Hardware constraints:** Do you have budget for all wireless hardware ($430)?
3. **Team size:** Is this solo development or team-based?
4. **Data residency:** Any specific geographic/legal data storage requirements?
5. **Performance targets:** Any throughput/latency SLAs for production?
6. **Compliance:** Any HIPAA/PCI/GDPR requirements?
