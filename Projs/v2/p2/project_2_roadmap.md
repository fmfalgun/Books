# Project 2: Advanced Wireless Protocol Security Analysis (Zigbee/BLE)
## Implementation Roadmap & Comprehensive Guide

**Project Duration:** 2-4 months | **Complexity:** High | **Target Companies:** NVIDIA, Intel, AMD, Samsung, Apple

---

## Table of Contents
1. [Executive Summary](#executive-summary)
2. [Existing Solutions Competitive Analysis](#existing-solutions-competitive-analysis)
3. [Custom Module Architecture](#custom-module-architecture)
4. [Implementation Phases & Timeline](#implementation-phases--timeline)
5. [Technology Stack](#technology-stack)
6. [Development Workflow](#development-workflow)
7. [Testing & Validation Strategy](#testing--validation-strategy)
8. [Publication & Deliverables](#publication--deliverables)
9. [Risk Mitigation](#risk-mitigation)
10. [References](#references)

---

## Executive Summary

This project extends your existing expertise in BLE/Zigbee protocol analysis into a **production-grade security analysis framework** that demonstrates:

- **Advanced offensive capabilities:** Packet crafting, protocol fuzzing, state machine analysis
- **Deep protocol understanding:** Stack-layer vulnerabilities, cryptographic weaknesses, timing attacks
- **Practical research:** Real-world device testing, CVE discovery, publication-ready findings
- **Industry alignment:** Targets NVIDIA, Intel, AMD, Samsung security roles

**Expected Outcomes:**
- Open-source GitHub repository with 1000+ lines of custom Python/C code
- 2-3 security vulnerabilities discovered in commercial devices
- Conference paper (DEF CON / Black Hat submission ready)
- Portfolio piece demonstrating enterprise-grade security engineering

---

## Existing Solutions Competitive Analysis

### Table 1: Open-Source Tools & Frameworks

| **Tool Name** | **Category** | **Primary Focus** | **Advantages** | **Drawbacks** | **Limitations** | **Cost** | **License** | **BLE** | **Zigbee** | **Packet Gen** | **Fuzzing** | **Traffic Analysis** | **Scalability** |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **Ubertooth One** | HW + OS | BLE sniffing & analysis | Low-cost (~$60), open-source firmware, excellent Wireshark integration, large community | Limited to BLE only, range ~100m, cannot jam/replay out-of-box | No Zigbee/Z-Wave, single-channel capture, packet drops at high rates | $60 hardware | GPL v2 | ✅ Excellent | ❌ Not supported | ⚠️ Limited (via Scapy) | ⚠️ Basic | ✅ Excellent | ⚠️ Single device |
| **KillerBee** | Python Framework | 802.15.4 penetration testing | Supports multiple hardware platforms (ApiMote, RZUSBStick), packet crafting, wardrive capability, Scapy integration | Steep learning curve, limited documentation, not actively maintained (last update 2019) | No firmware-level access, basic fuzzing, requires custom hardware | Free | GPL v3 | ❌ Requires adapter | ✅ Native | ✅ Excellent (Scapy) | ✅ Native | ⚠️ Manual | ✅ Good |
| **Wireshark + Plugins** | Analysis Tool | Multi-protocol packet analysis | Industry-standard, excellent UI, dissector plugins for BLE/Zigbee, real-time capture | Not designed for active testing/exploitation, limited fuzzing, proprietary plugin ecosystem | Passive analysis only, steep plugin development curve | Free | GPL v2 | ✅ With plugins | ✅ With plugins | ❌ Not native | ❌ Not native | ✅ Excellent | ✅ Excellent |
| **RFQuack** | Unified Toolkit | Wireless protocol analysis | Hardware-agnostic (USRP, HackRF), Python-based, powerful packet manipulation, research-grade | Complex setup (requires USRP/HackRF), steep learning curve, sparse documentation | Requires expensive hardware ($400+), not protocol-specific, experimental code quality | Free | AGPL v3 | ✅ Possible | ✅ Possible | ✅ Excellent | ✅ Excellent | ✅ Excellent | ✅ Excellent |
| **Scapy** | Python Library | Packet crafting & generation | Language-agnostic protocol definition, extensive protocol library, powerful manipulation | Not wireless-specific, requires low-level socket access for some operations, steep learning curve | Limited BLE/Zigbee protocol definition out-of-box, no GUI | Free | GPL v2 | ⚠️ Custom | ⚠️ Custom | ✅ Excellent | ✅ Excellent (with custom fuzzers) | ⚠️ With extensions | ✅ Excellent |
| **bluescan** | Python Tool | BLE reconnaissance | Automated device discovery, RSSI mapping, CLI tool, minimal dependencies | Limited to scanning/enumeration, no exploitation, outdated (last update 2020) | No packet crafting, basic analysis only, no Zigbee | Free | MIT | ✅ Basic | ❌ Not supported | ❌ Not supported | ❌ Not supported | ⚠️ Limited | ⚠️ Limited |
| **Z-Fuzzer** | Fuzzing Framework | Zigbee protocol fuzzing | Specialized Zigbee fuzzing, mutation-based approach, CVE discovery track record | Limited to Zigbee, requires custom hardware setup, experimental code | No BLE support, sparse documentation, no active maintenance | Free | Custom (Research) | ❌ Not supported | ✅ Excellent | ⚠️ Fuzzing-focused | ✅ Excellent | ⚠️ Fuzzing-focused | ⚠️ Limited |
| **Bleah** | Python Tool | BLE scanning & enumeration | Simple CLI tool, basic device discovery, GATT enumeration | Very limited scope, no exploitation, no fuzzing, minimal features | No packet crafting, basic analysis only, unmaintained | Free | MIT | ✅ Basic | ❌ Not supported | ❌ Not supported | ❌ Not supported | ⚠️ Limited | ❌ Limited |
| **BtleJuice** | Framework | BLE MITM & testing | Man-in-the-middle framework, packet injection, device simulation | Requires specific hardware setup, complex configuration, outdated | Limited to BLE, no Zigbee, sparse community support, unmaintained | Free | Apache 2.0 | ✅ MITM-focused | ❌ Not supported | ✅ Injection | ⚠️ Limited | ✅ MITM-focused | ⚠️ Limited |
| **Bluetooth Stack Analysis** | Research Project | BLE stack vulnerabilities | Deep stack-layer analysis, state machine modeling, formal verification potential | Academic project quality, limited practical tools, research-focused | No commercial-grade tooling, steep implementation curve | Free | Various | ✅ Research | ⚠️ Limited | ⚠️ Research | ⚠️ Research | ✅ State-based | ⚠️ Research |

### Table 2: Commercial & Semi-Commercial Tools

| **Tool Name** | **Category** | **Primary Focus** | **Advantages** | **Drawbacks** | **Limitations** | **Cost** | **License** | **BLE** | **Zigbee** | **Packet Gen** | **Fuzzing** | **Traffic Analysis** | **Scalability** |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **PANalyzr** | Commercial | Comprehensive protocol analysis | Professional UI, multi-protocol support, technical support, enterprise features | Expensive ($5K-$20K+), limited customization, vendor lock-in | Limited to supported protocols, no source code access, closed ecosystem | $5,000+ | Proprietary | ✅ Full | ✅ Full | ✅ Full | ✅ Full | ✅ Full | ✅ Enterprise |
| **Ellisys BluetoothViz** | Commercial | BLE visualization & analysis | Professional tool, excellent visualization, multi-device support, technical support | Expensive ($2,500-$10,000), limited customization, Windows-only initially | No Zigbee, limited fuzzing, no source code, proprietary format | $2,500+ | Proprietary | ✅ Excellent | ❌ Not supported | ⚠️ Limited | ⚠️ Limited | ✅ Excellent | ✅ Good |
| **Spirent Landslide** | Commercial | Protocol testing & validation | Production-grade, extensive test libraries, support, automation | Very expensive ($20K+), overkill for research, requires training | Enterprise-only, limited to supported protocols, vendor lock-in | $20,000+ | Proprietary | ✅ Yes | ✅ Yes | ✅ Full | ✅ Full | ✅ Full | ✅ Enterprise |
| **Frontline Protocol Analyzer** | Commercial | Multi-wireless analysis | Professional quality, multi-protocol, good analysis features | Expensive ($3K-$15K), limited updates, decreasing market relevance | Windows-focused, proprietary format, limited community | $3,000+ | Proprietary | ✅ Full | ✅ Full | ⚠️ Limited | ⚠️ Limited | ✅ Full | ✅ Good |
| **Apptis ZigBee Analyzer** | Commercial | Zigbee-specific | Specialized for Zigbee, good analysis, compliance testing | Expensive, limited updates, Zigbee-only | No BLE, no fuzzing, closed ecosystem | $5,000+ | Proprietary | ❌ Not supported | ✅ Excellent | ⚠️ Limited | ❌ Not supported | ✅ Excellent | ⚠️ Limited |
| **Nordic nRF Connect** | Semi-Commercial | BLE development tool | Free tier available, professional features optional, good community | Limited fuzzing, requires Nordic hardware for full features, proprietary backend | Limited customization, no Zigbee, restricted advanced features | Free - $500+ | Proprietary (Free tier) | ✅ Good | ❌ Not supported | ⚠️ Limited | ⚠️ Limited | ✅ Good | ⚠️ Good |
| **Teledyne LeCroy Wireless Protocol Suite** | Commercial | Enterprise protocol analysis | Professional grade, extensive features, technical support | Very expensive ($15K-$50K+), enterprise focus only, vendor lock-in | Limited to supported protocols, no source code, closed ecosystem | $15,000+ | Proprietary | ✅ Full | ✅ Full | ✅ Full | ✅ Full | ✅ Full | ✅ Enterprise |

### Comparative Analysis Summary

**Best Open-Source Stack for This Project:**
- **Packet Capture:** Ubertooth One ($60) + custom firmware
- **Packet Crafting & Fuzzing:** Scapy + custom Python modules
- **Protocol Analysis:** Wireshark with custom dissectors
- **802.15.4 Testing:** KillerBee + ApiMote hardware
- **Hardware-Agnostic:** RFQuack with USRP B210

**Key Insight:** No single open-source tool provides complete functionality. **The project goal is to bridge this gap** by creating an integrated framework that combines the strengths of existing tools while adding novel analysis capabilities.

---

## Custom Module Architecture

### Table 3: Core Module Specifications

| **Module ID** | **Module Name** | **Goal/Objective** | **Scope** | **Permissions/Constraints** | **Key Process** | **Required Resources** | **Dependencies** | **Testing Approach** | **Success Metrics** |
|---|---|---|---|---|---|---|---|---|---|
| **MOD-001** | **Packet Sniffer Engine** | Unified BLE/Zigbee packet capture abstraction layer | Capture packets from multiple hardware platforms (Ubertooth, ApiMote, nRF dongle), normalize format, timestamp accuracy | Must maintain <1% packet loss at max channel bandwidth; encrypted traffic must be capturable (key extraction optional); no hardware-specific socket manipulation allowed | 1. Initialize hardware dongle (USB enumeration) → 2. Set channel/frequency mode → 3. Capture raw packets → 4. Parse link-layer headers → 5. Normalize to unified format → 6. Write to PCAP/HDF5 | Python 3.9+ with libusb, pyusb, scapy, h5py; Ubertooth/ApiMote hardware | libusb, pyusb, scapy base | Unit tests: 10k packet round-trip fidelity; Integration: 1hr continuous capture, compare against Wireshark PCAP | 99.5% packet recovery rate, <5ms timestamp accuracy, support ≥2 simultaneous devices |
| **MOD-002** | **Protocol Parser & Dissector** | Build extensible dissector stack for BLE & Zigbee protocol layers | Parse L2/L3/L4 protocol headers (BLE LL/L2CAP/GATT/ATT; Zigbee MAC/NWK/APL), extract fields, build packet tree representation, detect malformed packets | PDU parsing must be RFC/spec-compliant; no assumption of well-formed packets; must handle fragmentation/reassembly; endianness correctness mandatory | 1. Define protocol state machine (finite automaton) → 2. Build packet parser using Scapy layers → 3. Implement reassembly buffers → 4. Create dissector tree → 5. Validate against known captures → 6. Log parse errors | Python 3.9+, scapy, struct module, custom state machine library (enum-based) | MOD-001 (packet input), RFC 4.2 specs, protocol RFCs | Unit tests: >500 real packet samples; Property tests: fuzz parser with malformed input; Regression: protocol update validation | Parse 100% of known-good packets correctly, detect & log 95% of malformed packets, <50ms/1000 packet latency |
| **MOD-003** | **Cryptographic Analysis Module** | Detect & analyze crypto operations, extract/crack weak keys, identify protocol weaknesses | Analyze AES-CCM (BLE), AES-128 (Zigbee), ECDH key exchange, replay attack surfaces, nonce reuse patterns | Cannot perform brute-force on production keys >128 bit (legal/ethical); analysis limited to research devices; must log all cryptanalysis attempts | 1. Identify encrypted payloads in packet stream → 2. Extract IV/nonce/ciphertext → 3. Detect weak key patterns (Bluetooth fixed randomness bugs) → 4. Optional: attempt dictionary attacks on weak keys → 5. Build crypto vulnerability database | Python 3.9+, cryptography library, PyCryptodome, custom ECC implementation (or libgcrypt bindings), GPU acceleration (CUDA/OpenCL) optional | MOD-002 (parsed packets), research-grade crypto libs, NIST ECC curve definitions | Unit tests: known-plaintext attacks on test vectors; Integration: analyze captured TLS/BLE LE SC exchanges; Fuzzing: intentional weak key generation | Detect all documented BLE/Zigbee crypto bugs with 100% precision, <100ms analysis per packet, GPU speedup ≥5x |
| **MOD-004** | **Fuzzing & Mutation Engine** | Generate malformed protocol-compliant packets to discover state machine bugs/crashes | Generate test cases with various mutation strategies (bit-flip, boundary values, field shuffling, replay modifications) for BLE/Zigbee | Fuzzing only against research hardware/simulators, never production devices; no denial-of-service fuzzing on shared networks; logging mandatory | 1. Define protocol templates (valid protocol PDU structure) → 2. Apply mutation operators (bit-flip, repeat, truncate, swap fields) → 3. Generate test cases (strategy: coverage-guided or grammar-based) → 4. Feed to device under test (DUT) → 5. Monitor for crashes/unexpected behavior → 6. Correlate crashes to input mutations | Python 3.9+, custom fuzzer framework (Radamsa/AFL integration optional), hardware test rigs (Raspberry Pi + dev kits) | libFuzzer or AFL++ (optional C backend), harness code for DUT, GDB for crash analysis | Unit tests: corpus generation validates RFC spec; Integration: crash detection accuracy vs. manual testing; Regression: stability of mutation operators | Generate ≥1000 test cases/sec, achieve 85%+ branch coverage on DUT state machine, discover ≥2 novel vulnerabilities |
| **MOD-005** | **State Machine Analyzer** | Map out protocol state machines, detect state confusion / race conditions / implicit assumptions | Extract state transitions from packet sequences, build directed graph of allowed states, identify unreachable/dead-end states, detect missing transitions | Analysis must be based on passive observation (captured traffic); state model must be validated against RFC; no modification of device firmware without explicit logging | 1. Parse packet sequence from PCAP → 2. Cluster packets by connection/session ID → 3. Extract state transitions (packet type A → state S → packet type B) → 4. Build state transition graph (directed graph) → 5. Detect anomalies: unreachable states, improper transitions, race conditions → 6. Generate formal model (Promela/TLA+) | Python 3.9+, networkx (graph library), custom state machine DSL, pygraphviz optional | MOD-002 (parsed packets), graphviz, optional TLA+ model checker | Unit tests: known state machines (BLE connection setup); Property tests: model checker verification; Fuzzing: inject out-of-order packets | Build state graphs from 100% of packet sequences, detect ≥80% of known protocol state confusion bugs, formal model runs in <5min |
| **MOD-006** | **Traffic Pattern Analysis & ML** | Identify device behavior patterns, anomaly detection, fingerprinting based on traffic characteristics | Extract features: packet timing, size distribution, frequency patterns, protocol negotiation sequences; train ML models (isolation forest, autoencoders) to detect anomalies | ML model must be trained only on openly available traffic; no proprietary device fingerprints; model accuracy vs. false positive trade-off must be documented | 1. Extract feature vectors from normalized packet streams → 2. Perform unsupervised clustering (isolation forest / DBSCAN) → 3. Train anomaly detection models → 4. Test on unseen traffic → 5. Calculate metrics (precision/recall/F1) → 6. Generate reports | Python 3.9+, scikit-learn, numpy, pandas, optional TensorFlow/PyTorch for deep learning | MOD-001/MOD-002 (packet input), public datasets (CICIDS, NSL-KDD adapted), labeled traffic samples | Unit tests: synthetic anomalies detection; Benchmark: compare vs. statistical baselines; Cross-validation: 5-fold validation on captured datasets | Detect 85%+ of injected anomalies, <3% false positive rate, model training <2hr on 10M packets |
| **MOD-007** | **Vulnerability Assessment Report Generator** | Aggregate findings, generate actionable security recommendations, produce publication-ready reports | Categorize vulnerabilities by CVSS score, create remediation guidance, format findings for academic paper / bug bounty / vendor disclosure | Report must follow responsible disclosure guidelines; no exploit code in public repo; CVE/CWE mappings must be accurate; legal review required before publication | 1. Aggregate all vulnerability findings from MOD-003/004/005/006 → 2. Score each finding using CVSS 3.1 calculator → 3. Cross-reference against known CVE database → 4. Generate remediation recommendations → 5. Format report (markdown/PDF/LaTeX) → 6. Highlight novel findings | Python 3.9+, jinja2 (templating), reportlab (PDF generation), latex, vulnerability databases (NVD API, CAPEC) | MOD-003/004/005/006 (vulnerability data), CVSS 3.1 scoring rubric, ethical guidelines template | Unit tests: sample vulnerability scoring; Integration: end-to-end report generation | Generate reports in <10min, CVSS score accuracy 100%, remediation guidance applicable to ≥80% of findings |
| **MOD-008** | **Hardware Integration Layer** | Abstract hardware-specific interfaces (Ubertooth, ApiMote, Nordic nRF), provide unified API | Support multiple sniffer platforms with minimal code duplication, handle platform-specific quirks, provide fallback/graceful degradation | Must support at least 3 hardware platforms; backward compatible with new hardware additions; no breaking API changes | 1. Define hardware abstraction interface (BaseHardware class) → 2. Implement per-platform drivers (Ubertooth, ApiMote, nRF52) → 3. Provide unified configuration API → 4. Handle connection errors & timeouts → 5. Provide device capability queries | Python 3.9+, pyusb, libusb, platform-specific SDKs, threading/asyncio | MOD-001 (packet interface), hardware documentation (datasheets), firmware binaries | Unit tests: mock hardware drivers; Integration: live device test per platform; Regression: driver update validation | Support ≥3 platforms, add new platform in <2 hours, zero cross-platform regression bugs |
| **MOD-009** | **Interactive CLI & Visualization** | User-friendly command-line interface + optional web dashboard for live analysis | Provide CLI commands for capture, analysis, filtering, reporting; support live protocol tree visualization; export results in multiple formats | CLI must be scriptable (non-interactive mode); web dashboard is optional/secondary; accessibility for non-expert users | 1. Design CLI command structure (commands: capture, analyze, fuzz, report) → 2. Implement argparse-based argument parsing → 3. Add interactive shell (IPython integration optional) → 4. Build web API (Flask/FastAPI) → 5. Develop minimal UI for dashboard → 6. Add export formats (PCAP, JSON, CSV) | Python 3.9+, click/argparse, Flask/FastAPI, jinja2, optional: rich (TUI), plotly (visualization) | All MOD-* (data sources), UI/UX guidelines, accessibility standards | Unit tests: command parsing & execution; Integration: end-to-end workflow via CLI; Usability: user testing with security researchers | CLI supports ≥20 commands, <100ms response time, web dashboard loads in <2sec, exports to ≥5 formats |
| **MOD-010** | **Documentation & Publication** | Comprehensive technical documentation, research paper, tutorial walkthroughs | Create: README, API docs (Sphinx/MkDocs), tutorial notebooks, research paper for conference submission, video walkthrough | Documentation must be kept in sync with code; paper must meet conference standards (IEEE/ACM format); no proprietary device details in public docs | 1. Write README with project overview, setup, quick-start → 2. Generate API docs (docstrings + Sphinx) → 3. Create Jupyter notebooks with examples → 4. Write research paper (methodology, findings, impact) → 5. Record video tutorial → 6. Submit to conferences (DEF CON, Black Hat, IEEE S&P) | Python 3.9+, sphinx, jupyter, pandoc, latex, youtube/video tools | All MOD-* (source code), research findings, academic paper templates | Unit tests: docs build without errors; Link validation: all URLs live; Usability: user tests on setup/tutorial docs | Docs cover 95% of API, paper passes peer review, 100+ GitHub stars, ≥500 views first month |

---

## Implementation Phases & Timeline

### Phase 1: Foundation (Weeks 1-2)

**Objective:** Set up development environment, create architecture blueprints, gather requirements.

**Deliverables:**
- [ ] Project repository initialized (GitHub) with CI/CD pipeline (GitHub Actions)
- [ ] Development environment: Docker containers for isolated testing
- [ ] Architecture design document (C4 diagrams, component interactions)
- [ ] Hardware procurement list & setup instructions
- [ ] Threat model & security considerations document
- [ ] Roadmap with weekly milestones & risk register

**Key Activities:**
1. Create comprehensive project plan with stakeholder input (if applicable)
2. Set up hardware: Ubertooth One, ApiMote, nRF52840 dongle
3. Design unified packet format (schema definition)
4. Plan module integration points & data flow
5. Establish code review process & testing standards

---

### Phase 2: Core Packet Capture & Parsing (Weeks 3-5)

**Objective:** Build MOD-001, MOD-002, MOD-008 (hardware abstraction + parsing).

**Deliverables:**
- [ ] **MOD-001:** Packet sniffer engine capturing from ≥2 hardware platforms
- [ ] **MOD-002:** Protocol dissector for BLE LL/L2CAP/GATT and Zigbee MAC/NWK/APL layers
- [ ] **MOD-008:** Hardware abstraction layer (unified API)
- [ ] Unit test suite: ≥90% code coverage
- [ ] Integration tests: capture validation against Wireshark
- [ ] Documentation: API reference, hardware setup guide

**Key Activities:**
1. Implement USB enumeration & device initialization
2. Build packet parsing state machine (recursive descent parser)
3. Test against 100+ known-good packet samples
4. Validate against Wireshark dissectors
5. Optimize for low-latency (<1ms latency per packet)

---

### Phase 3: Analysis & Vulnerability Detection (Weeks 6-9)

**Objective:** Build MOD-003, MOD-004, MOD-005, MOD-006.

**Deliverables:**
- [ ] **MOD-003:** Crypto analysis module (detect weak keys, extract nonces)
- [ ] **MOD-004:** Fuzzing engine with ≥1000 test cases/sec throughput
- [ ] **MOD-005:** State machine analyzer with formal model generation
- [ ] **MOD-006:** ML-based anomaly detection (trained on 100k+ packets)
- [ ] Vulnerability database schema & initial findings
- [ ] First set of discovered vulnerabilities (target: ≥2 novel findings)

**Key Activities:**
1. Analyze BLE/Zigbee crypto implementations against known attacks
2. Build mutation testing framework with coverage-guided strategy
3. Extract state machines from real device captures
4. Train ML models on captured traffic patterns
5. Run fuzzing campaigns on research hardware (≥100 hours runtime)
6. Categorize & prioritize discovered vulnerabilities

---

### Phase 4: Integration & Reporting (Weeks 10-12)

**Objective:** Integrate modules, create user interface, generate reports, prepare publication.

**Deliverables:**
- [ ] **MOD-009:** CLI tool + optional web dashboard (all core commands working)
- [ ] **MOD-007:** Automated vulnerability report generation (CVSS scoring, remediation)
- [ ] Complete technical documentation (Sphinx docs, README, tutorials)
- [ ] Research paper draft (methodology section complete, findings documented)
- [ ] Public GitHub repository (anonymized if needed for responsible disclosure)
- [ ] Conference submission (DEF CON, Black Hat, IEEE S&P) with video abstract

**Key Activities:**
1. Integrate all modules into unified CLI
2. Implement end-to-end workflows (capture → analyze → report)
3. Create comprehensive documentation with code examples
4. Write research paper (target length: 8-10 pages IEEE format)
5. Prepare responsible disclosure for discovered vulnerabilities
6. Submit to ≥2 conferences
7. Prepare video walkthrough (5-10 minutes)

---

### Weekly Breakdown Chart

```
Week 1-2:   [████████] Foundation & Setup
Week 3-5:   [████████] Core Capture & Parsing (MOD-001/002/008)
Week 6-9:   [████████] Analysis & Vulnerability Detection (MOD-003/004/005/006)
Week 10-12: [████████] Integration, Reporting & Publication (MOD-007/009/010)
```

**Critical Path:** MOD-001 → MOD-002 → MOD-003/004/005 → MOD-007/009
**Parallel Work:** MOD-006 (training), MOD-010 (documentation)

---

## Technology Stack

### Software Stack

| **Layer** | **Component** | **Technology** | **Rationale** | **Version** |
|---|---|---|---|---|
| **Core Language** | Runtime | Python 3.9+ | Cross-platform, extensive security libraries, rapid development | 3.11+ (LTS) |
| **Packet Handling** | Protocol Library | Scapy 2.5+ | Industry-standard packet crafting, extensible protocol definitions, active maintenance | 2.5.0+ |
| **Wireless Hardware** | USB Interface | PyUSB 1.2+ | Cross-platform USB device access, no kernel drivers needed | 1.2.1+ |
| **Protocol Parsing** | BLE Dissector | Custom (inspired by BLEAK) | Ubertooth integration, custom protocol support | Custom |
| **Protocol Parsing** | Zigbee Dissector | KillerBee libs + custom | Mature Zigbee parsing, community-tested | KillerBee 2.x |
| **Cryptography** | Algorithms | cryptography 41.0+ | NIST-approved ciphers, modern API, audited code | 41.0.0+ |
| **Cryptography** | GPU Acceleration | PyCUDA / CuPy | Optional GPU fuzzing acceleration (CUDA-capable GPUs) | Latest |
| **ML/Statistics** | Data Science | scikit-learn 1.3+ | Isolation forests, clustering, mature library | 1.3.0+ |
| **ML/Statistics** | Numerics | NumPy 1.24+ | Fast array operations, FFT for timing analysis | 1.24.0+ |
| **ML/Statistics** | Data Handling | Pandas 2.0+ | Structured data manipulation, feature engineering | 2.0.0+ |
| **ML/Statistics** | Visualization | Matplotlib 3.7+ | Publication-quality plots, protocol timeline visualization | 3.7.0+ |
| **State Machine** | Modeling | NetworkX 3.1+ | Graph algorithms, state transition modeling | 3.1+ |
| **State Machine** | Formal Methods | TLA+ / Promela | Optional: formal verification of state machines | Latest |
| **Testing** | Unit Testing | pytest 7.4+ | Parametrized tests, fixtures, plugin ecosystem | 7.4.0+ |
| **Testing** | Code Coverage** | coverage.py 7.2+ | Branch coverage reporting, HTML reports | 7.2.0+ |
| **Testing** | Property Testing | Hypothesis 6.80+ | Property-based testing, coverage-guided shrinking | 6.80.0+ |
| **Testing** | Mocking** | unittest.mock (stdlib) | Built-in mocking for hardware abstraction | stdlib |
| **Testing** | Fuzzing** | AFL++ / libFuzzer | Optional: coverage-guided fuzzing backend | Latest |
| **Documentation** | API Docs | Sphinx 7.0+ | Professional documentation generation, multiple format export | 7.0.0+ |
| **Documentation** | Notebooks | Jupyter 7.0+ | Interactive tutorial notebooks with live code | 7.0.0+ |
| **Documentation** | ReadTheDocs | ReadTheDocs | Automatic docs hosting, version management | Cloud |
| **CLI** | Command Framework | Click 8.1+ | Intuitive CLI creation, automatic help generation | 8.1.0+ |
| **CLI** | Terminal UI | Rich 13.5+ | Beautiful TUI output, progress bars, syntax highlighting | 13.5.0+ |
| **Web Dashboard** | Framework | FastAPI 0.100+ | Async Python web framework, auto-generated OpenAPI docs | 0.100.0+ |
| **Web Dashboard** | Frontend** | Vue.js 3.3+ / React | Optional: interactive real-time visualization | Latest |
| **Reporting** | PDF Generation | ReportLab 4.0+ | Programmatic PDF creation, charts, custom layouts | 4.0.0+ |
| **Reporting** | Template Engine | Jinja2 2.11+ | Dynamic report templates, flexible formatting | 2.11.0+ |
| **Database** | Logging | HDF5 / SQLite | Efficient storage of multi-GB packet captures, query capability | Latest |
| **CI/CD** | Testing & Deployment | GitHub Actions | Native GitHub integration, free for public repos | Native |
| **CI/CD** | Container** | Docker / Docker Compose | Reproducible environments, hardware simulation | Latest |
| **Version Control** | Repository | Git | Source code management | Core |
| **Version Control** | Hosting | GitHub | Community collaboration, issue tracking | Cloud |

### Hardware Stack

| **Component** | **Model** | **Purpose** | **Quantity** | **Cost** | **Notes** |
|---|---|---|---|---|---|
| **BLE Sniffer** | Ubertooth One | BLE 4.0-5.x packet capture | 2 | $120 | Primary BLE analysis, swap crystals for frequency hopping |
| **802.15.4 Sniffer** | ApiMote v4 | Zigbee/802.15.4 packet capture | 1 | $150 | Primary Zigbee analysis, supports fuzz harness |
| **BLE Dev Kit** | Nordic nRF52840 DK | Protocol implementation testing, fuzzing target | 2 | $200 | Target device for fuzzing, state machine analysis |
| **Test Harness** | Raspberry Pi 4B (8GB RAM) | Packet processing, ML model training | 1 | $60 | High-speed packet processing, GPU optional |
| **GPU Acceleration** | NVIDIA Jetson Orin | Optional: crypto brute-force, ML training | Optional | $300+ | Speedup 10-50x for crypto analysis |
| **Logic Analyzer** | Saleae Logic Pro 16 | Timing/protocol validation, trigger analysis | 1 (Optional) | $500 | Ground truth for protocol timing validation |
| **Network Switch** | PoE Managed Switch | Test harness interconnection | 1 | $100 | Controlled network segmentation |
| **Power Supply** | Multi-port USB Hub | Hardware power management | 2 | $40 | Reliable power distribution, debugging interface |

---

## Development Workflow

### Repository Structure

```
wireless-protocol-security-analysis/
├── README.md                    # Project overview, quick-start guide
├── CONTRIBUTING.md              # Contribution guidelines, code of conduct
├── LICENSE                      # MIT or Apache 2.0
├── .github/
│   ├── workflows/
│   │   ├── ci.yml              # CI/CD pipeline (tests, linting, coverage)
│   │   └── publish.yml         # PyPI package publishing
│   └── ISSUE_TEMPLATE/          # Bug reports, feature requests
├── setup.py                     # Package metadata, dependencies
├── requirements.txt             # Python dependencies (pip)
├── requirements-dev.txt         # Dev dependencies (pytest, sphinx, etc.)
├── docker/
│   ├── Dockerfile              # Container with all dependencies
│   └── docker-compose.yml       # Multi-container test environment
├── src/
│   └── wireless_protocol_analyzer/
│       ├── __init__.py
│       ├── core/
│       │   ├── __init__.py
│       │   ├── sniffer.py              # MOD-001: Packet sniffer
│       │   ├── parser.py               # MOD-002: Protocol parser
│       │   └── hardware.py             # MOD-008: Hardware abstraction
│       ├── analysis/
│       │   ├── __init__.py
│       │   ├── crypto.py               # MOD-003: Crypto analysis
│       │   ├── fuzzer.py               # MOD-004: Fuzzing engine
│       │   ├── state_machine.py        # MOD-005: State machine analyzer
│       │   └── anomaly_detector.py     # MOD-006: ML-based detection
│       ├── reporting/
│       │   ├── __init__.py
│       │   ├── vulnerability.py        # MOD-007: Vuln report generation
│       │   └── templates/              # Report templates (Jinja2)
│       ├── cli/
│       │   ├── __init__.py
│       │   └── main.py                 # MOD-009: CLI interface
│       ├── web/
│       │   ├── __init__.py
│       │   ├── app.py                  # FastAPI application
│       │   └── static/                 # Frontend assets
│       └── utils/
│           ├── __init__.py
│           ├── logging.py              # Custom logging setup
│           ├── constants.py            # Protocol constants
│           └── decorators.py           # Utility decorators
├── tests/
│   ├── unit/
│   │   ├── test_sniffer.py
│   │   ├── test_parser.py
│   │   ├── test_crypto.py
│   │   ├── test_fuzzer.py
│   │   └── ...
│   ├── integration/
│   │   ├── test_e2e_capture_analyze.py
│   │   ├── test_hardware_platforms.py
│   │   └── ...
│   ├── fixtures/
│   │   ├── pcap_samples/             # Real packet captures (100+)
│   │   ├── device_responses/         # Mock device responses
│   │   └── known_vulnerabilities/    # Ground truth test cases
│   └── conftest.py                   # Pytest configuration
├── docs/
│   ├── index.md                 # Documentation home
│   ├── getting-started.md       # Setup & installation guide
│   ├── api-reference.md         # Module API docs (Sphinx)
│   ├── protocols/
│   │   ├── ble-protocol.md      # BLE spec notes
│   │   └── zigbee-protocol.md   # Zigbee spec notes
│   ├── tutorials/
│   │   ├── basic-capture.ipynb
│   │   ├── crypto-analysis.ipynb
│   │   └── fuzzing-guide.ipynb
│   └── conf.py                  # Sphinx configuration
├── notebooks/
│   ├── 01_bumblebee_capture.ipynb    # Live capture examples
│   ├── 02_vulnerability_hunting.ipynb # Fuzzing workflow
│   └── 03_data_analysis.ipynb        # Statistical analysis
├── data/
│   ├── pcap/                    # Sample PCAP files (gitignored)
│   ├── vulnerability_db.json    # Discovered vulnerabilities
│   └── ml_models/               # Trained ML models (gitignored)
├── research/
│   ├── paper.md / paper.tex     # Research paper (IEEE format)
│   ├── findings.md              # Key findings summary
│   └── presentations/           # Conference presentations
└── .gitignore                   # Ignore large files, credentials
```

### Code Quality Standards

**Linting & Formatting:**
```bash
black .                    # Code formatter (PEP 8)
isort .                    # Import sorting
flake8 src/               # Linting (E501 line length exemption for protocols)
mypy src/                 # Type checking (strict mode)
pylint src/               # Additional linting
```

**Testing Standards:**
- **Minimum Coverage:** 85% (critical path 95%)
- **Test Categories:** Unit (60%), Integration (30%), End-to-End (10%)
- **Test Execution:** `pytest -v --cov=src/ tests/`
- **Mutation Testing:** Use `mutmut` to validate test quality

**Documentation Standards:**
- All public functions must have docstrings (Google style)
- Type hints required for all function signatures
- README for each major module
- API documentation auto-generated via Sphinx

---

## Testing & Validation Strategy

### Table 4: Test Plan

| **Test Category** | **Test Case** | **Objective** | **Input/Setup** | **Expected Output** | **Pass Criteria** | **Automation** |
|---|---|---|---|---|---|---|
| **Unit: MOD-001** | Packet parsing fidelity | Verify packets parsed correctly without loss | 1000 real BLE packets from Wireshark capture | Parsed packets match original headers byte-for-byte | 100% match rate | pytest ✓ |
| **Unit: MOD-001** | Multi-device capture | Ensure simultaneous capture from 2+ devices | Ubertooth + ApiMote connected, both transmitting | Packets from both devices captured, timestamps differ | 0% packet loss, <5ms timestamp error | pytest ✓ |
| **Unit: MOD-002** | Protocol dissector - BLE | Parse BLE LL/L2CAP/GATT headers correctly | 500 BLE advertisement packets | Parsed fields match RFC 4.1 spec | 100% RFC compliance | pytest ✓ |
| **Unit: MOD-002** | Protocol dissector - Zigbee | Parse Zigbee MAC/NWK frames | 300 Zigbee network traffic samples | All frame types correctly identified | 100% field accuracy | pytest ✓ |
| **Unit: MOD-002** | Malformed packet handling | Detect & gracefully handle truncated packets | Truncated packets (80% → 20% length) | Parse errors logged, no crashes | 0 segfaults, 100% error detection | pytest ✓ |
| **Unit: MOD-003** | Weak key detection | Identify known weak BLE keys | Traffic from devices with zero-key initialization | Weak keys flagged with specific CVE | 100% detection of known weak keys | pytest ✓ |
| **Unit: MOD-003** | Nonce extraction | Extract initialization vectors from encrypted payloads | 200 encrypted BLE LE SC packets | IVs extracted and validated | 100% IV recovery (when present) | pytest ✓ |
| **Unit: MOD-004** | Mutation coverage | Generate mutations with >80% branch coverage | Valid BLE Connect Request template | 1000+ mutant packets generated | 85%+ branch coverage achieved | pytest + coverage.py ✓ |
| **Unit: MOD-004** | Fuzzer throughput | Achieve ≥1000 packets/sec mutation rate | Fuzzer running on Raspberry Pi | Measure packets/sec generated | ≥1000 pkts/sec sustained | pytest benchmark ✓ |
| **Unit: MOD-005** | State machine extraction | Map BLE connection state machine from traffic | Captured BLE pairing sequence (20 packets) | State graph with ≥8 nodes | Graph matches RFC spec | pytest + networkx ✓ |
| **Unit: MOD-005** | Anomaly state detection | Identify out-of-order protocol transitions | Fuzzer output with invalid state transitions | Anomalies flagged with packet indices | 95%+ anomaly detection rate | pytest ✓ |
| **Unit: MOD-006** | Anomaly detection accuracy | Detect injected anomalies in traffic | 1M packet trace + 100 synthetic anomalies | Anomalies flagged, precision/recall/F1 | F1 ≥0.85, FPR <3% | pytest + sklearn metrics ✓ |
| **Unit: MOD-006** | Model training time | ML model trains in reasonable time | 10M packet feature vectors | Model ready for inference | Training <2 hours on Pi | pytest benchmark ✓ |
| **Integration: MOD-001+002+008** | End-to-end capture & parse | Full pipeline: capture → parse → output | Ubertooth capturing real BLE traffic | PCAP file with parsed packet tree | Matches Wireshark output | Shell script ✓ |
| **Integration: MOD-001+003+007** | Vulnerability detection pipeline | Capture → crypto analysis → report | 2-hour traffic capture on test device | CSV report with vulnerabilities scored | Report generated in <5min | Shell script ✓ |
| **Integration: MOD-004+005+002** | Fuzzing with state analysis | Generate fuzz inputs, execute on device, analyze | nRF52 dev kit as target, 1hr fuzzing campaign | Crashes categorized by state machine location | ≥2 novel crash types | Custom harness ✓ |
| **Integration: MOD-001/002/003/004/005+006** | Full analysis pipeline | Complete workflow: capture → all analyses → ML | 1-hour capture from mixed BLE/Zigbee environment | JSON report with all analysis results | No pipeline errors, <5min runtime | Shell script ✓ |
| **E2E: CLI** | CLI capture command | Execute `cli capture -d ubertooth -t 10s` | CLI installed, Ubertooth connected | PCAP file created with 10s traffic | PCAP valid, >100 packets | Shell script ✓ |
| **E2E: CLI** | CLI analysis command | Execute `cli analyze capture.pcap --full` | PCAP from above | HTML report generated | Report loads, all sections present | Shell script ✓ |
| **E2E: Regression** | No breaking changes | Run full test suite on code changes | Git pre-push hook | All tests pass | 100% test pass rate | GitHub Actions ✓ |
| **Performance: Scalability** | 100M packet analysis | Process large PCAP files | 100M packet HDF5 file (≥10 GB) | Analysis completes, ML models train | <4 hours runtime on Pi+GPU | Custom benchmark ✓ |
| **Security: Fuzzing** | Parser robustness | Fuzz protocol parser with AFL++ | 10K+ mutated packet samples | Parser never crashes, errors logged | 0 crashes / 10K mutations | AFL++ integrated ✓ |
| **Security: Crypto** | Cryptanalysis validation | Verify crypto findings against test vectors | Known-plaintext attacks on test keys | Match published attack results | 100% match to published results | pytest ✓ |

### Continuous Integration Pipeline

**GitHub Actions Workflow (`.github/workflows/ci.yml`):**
```yaml
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install -r requirements-dev.txt
      - name: Lint (black, isort, flake8, mypy)
        run: |
          black --check src/
          isort --check src/
          flake8 src/
          mypy src/
      - name: Run unit tests
        run: pytest tests/unit -v --cov=src
      - name: Upload coverage
        uses: codecov/codecov-action@v3
      - name: Run integration tests
        run: pytest tests/integration -v
      - name: Build docs
        run: sphinx-build -W -b html docs/ docs/_build/
```

---

## Publication & Deliverables

### Research Paper Outline (IEEE Format, 8-10 pages)

**Title:** "Advanced Wireless Protocol Security Analysis: Automated Vulnerability Discovery in BLE and Zigbee Implementations"

**Abstract** (150 words)
- Problem: BLE/Zigbee vulnerabilities often go undetected due to lack of accessible analysis tools
- Contribution: Open-source framework combining packet capture, fuzzing, state machine analysis, and ML-based anomaly detection
- Key findings: ≥2 novel vulnerabilities discovered in commercial devices
- Impact: Published as open-source, conference presentation, responsible disclosure

**1. Introduction & Motivation** (1 page)
- Importance of BLE/Zigbee in IoT ecosystem
- Existing gap between academic research and practical security assessment
- Paper's research questions & objectives

**2. Background & Related Work** (1.5 pages)
- BLE/Zigbee protocol stack overview
- State of prior work (KillerBee, Ubertooth, RFQuack, etc.)
- Why existing tools alone are insufficient (gap analysis)

**3. Methodology** (2 pages)
- Architecture overview (module diagram)
- Module descriptions: packet capture, parsing, fuzzing, state machine analysis, ML anomaly detection
- Threat model & assumptions

**4. Implementation** (2 pages)
- Technology stack & hardware setup
- Key implementation challenges & solutions
- Performance optimizations (e.g., GPU acceleration, async processing)

**5. Evaluation & Findings** (2.5 pages)
- Experimental setup (test devices, traffic samples, dataset size)
- Discovered vulnerabilities (CVE descriptions, CVSS scores)
- Performance metrics (throughput, accuracy, comparison vs. existing tools)
- Results table: tools comparison, vulnerability discovery rates

**6. Lessons Learned & Responsible Disclosure** (0.5 pages)
- Legal/ethical considerations
- Vendor communication timeline
- Open-source community feedback

**7. Conclusion & Future Work** (0.5 pages)
- Recap contributions
- Future directions (Thread, Matter, 6LoWPAN support)
- Call to action for security research community

**8. References** (20-30 citations)

### Conference Submission Targets

| **Conference** | **Deadline** | **Format** | **Track** | **Expected Topics** |
|---|---|---|---|---|
| **DEF CON 33** | April 2026 | Talk (40 min) + Workshop (4 hr) | Security Research, IoT/Embedded | Live demos, protocol analysis, vulnerability walkthrough |
| **Black Hat USA 2026** | June 2025 | Talk (50 min) + Arsenal | IoT & Wireless, Offensive Security | Deep-dive technical session, tool open-sourcing announcement |
| **IEEE S&P 2026** | December 2025 | Paper (12 pages) | Wireless Security, Protocol Analysis | Academic paper with peer review, formal methods angle |
| **ACM CCS 2026** | May 2026 | Paper (14 pages) | Security, Privacy, System Security | Strong empirical evaluation, novel vulnerability classes |
| **USENIX Security 2026** | February 2026 | Paper (14 pages) | Systems & Network Security | Practical tools, large-scale analysis, reproducibility |

### Open-Source Release Strategy

**GitHub Repository:**
- **URL:** `https://github.com/your-username/wireless-protocol-security-analysis`
- **License:** Apache 2.0 (or MIT)
- **README:** Complete quick-start guide, setup instructions, example workflows
- **Releases:** Semantic versioning (v0.1.0 for alpha, v1.0.0 production-ready)
- **Community:** Issues for bug reports, discussions for feature requests

**PyPI Package:**
```bash
pip install wireless-protocol-analyzer
```

**Documentation Hosting:**
- ReadTheDocs: Auto-builds from Sphinx docs
- GitHub Pages: Supplementary tutorials & blog posts

**Social Media & Outreach:**
- Twitter/X thread announcing release
- LinkedIn post targeting security engineers
- HackerNews submission (if appropriate)
- Security reddit communities (r/security, r/ECE, r/wireless)

---

## Risk Mitigation

### Table 5: Risk Register & Mitigation

| **Risk ID** | **Risk** | **Probability** | **Impact** | **Mitigation Strategy** | **Owner** |
|---|---|---|---|---|---|
| **R-001** | Hardware compatibility issues (driver crashes, USB enumeration failures) | Medium | High | Virtualize hardware in Docker, test on 3+ platforms early (Ubuntu, Fedora, macOS), maintain hardware compatibility matrix | MOD-008 owner |
| **R-002** | Protocol spec misinterpretation (incorrect packet parsing) | Medium | High | Validate against RFC, cross-reference with Wireshark dissectors, unit tests with 500+ real packets, peer code review | MOD-002 owner |
| **R-003** | Vulnerability research discovers no novel findings | Medium | Medium | Plan fallback: reproduce known CVEs, analyze protocol design flaws, performance comparison against existing tools | Project lead |
| **R-004** | Fuzzing runs ineffectively (low crash rates, coverage plateau) | Medium | Medium | Use coverage-guided fuzzing (libFuzzer), employ state machine awareness, fuzz multiple protocol layers, hire fuzzing expert if needed | MOD-004 owner |
| **R-005** | ML model overfits on training data (poor anomaly detection in wild) | Medium | Medium | Use rigorous cross-validation (k-fold, time-series split), validate on out-of-distribution data, ensemble methods, hyperparameter tuning | MOD-006 owner |
| **R-006** | Legal issues from responsible disclosure (vendor non-response, unauthorized publication) | Low | High | Follow coordinated disclosure guidelines (90-day embargo), consult legal team before publication, document all communication, engage CERT/CC if needed | Project lead |
| **R-007** | Scope creep (more features, platforms, protocols) | High | Medium | Lock scope at Phase 1 end, prioritize MVP, track feature requests separately, enforce change control process | Project manager |
| **R-008** | Hardware procurement delays (supply chain issues) | Low | Medium | Order hardware early, identify backup suppliers (Digi-Key, Mouser), use cloud-based simulation as interim solution | Hardware owner |
| **R-009** | Key team member unavailable (illness, job change) | Low | High | Document code thoroughly, maintain wiki of setup procedures, cross-train on critical modules, maintain public milestones | HR/Lead |
| **R-010** | Performance bottleneck discovered late (analysis too slow to be practical) | Medium | Medium | Profile code early (Week 3), use benchmarking tools (pytest-benchmark), optimize hotspots (Cython, numba for Python), consider GPU acceleration | Performance owner |

---

## References

[1] Ubertooth Project. (2024). Ubertooth One Documentation. Retrieved from https://ubertooth.readthedocs.io/

[2] Ryan, M. (2013). "Bluetooth: With Low Energy Comes Low Security." WOOT 13. USENIX.

[3] Spill, D., & Baines, R. (2010). "Capturing and Decoding NFC Frames." Retrieved from http://www.codeproject.com/Articles/216328/Bluetooth-Stack-Smashing.

[4] Seeber, S., Wagner, P., & Sorniotti, G. (2013). "KillerBee: Practical Zigbee Exploitation." DEF CON 21.

[5] Fenton, C. "RFQuack: A Universal Hardware-Software Toolkit for Wireless Protocol (Security) Analysis and Research." arXiv preprint arXiv:2104.05247 (2021).

[6] Blu, A., White, M., & Thompson, J. (2024). "MQTTactic: Security Analysis and Verification for Logic Flaws in MQTT Implementations." IEEE IoT Journal.

[7] Bluetooth SIG. (2024). Bluetooth Core Specification v5.4. Retrieved from https://www.bluetooth.com/

[8] Zigbee Alliance. (2020). Zigbee Specification v3.0. Retrieved from https://zigbeealliance.org/

[9] IEEE. (2020). IEEE 802.15.4-2020: Standard for Low-Rate Wireless Personal Area Networks. Retrieved from https://standards.ieee.org/

[10] Scikit-Learn Developers. (2024). scikit-learn Machine Learning Library. Retrieved from https://scikit-learn.org/

[11] Scapy Project. (2024). Scapy: Interactive Packet Manipulation. Retrieved from https://scapy.readthedocs.io/

[12] Wireshark Foundation. (2024). Wireshark Network Protocol Analyzer. Retrieved from https://www.wireshark.org/

[13] NIST. (2023). Cybersecurity Framework v2.0. Retrieved from https://nvlpubs.nist.gov/nistpubs/

[14] MITRE ATT&CK. (2024). Enterprise ATT&CK Framework. Retrieved from https://attack.mitre.org/

[15] CWE Top 25. (2024). CWE/SANS Top 25 Software Weaknesses. Retrieved from https://cwe.mitre.org/top25/

[16] CVE Details. (2024). Bluetooth Protocol Vulnerabilities. Retrieved from https://www.cvedetails.com/

[17] BlueSWAT Project. (2024). "A Lightweight State-Aware Security Framework for Bluetooth Low Energy." arXiv:2405.17987.

[18] ZLeaks Research. (2021). "Passive Inference Attacks on Zigbee based Smart Homes." arXiv:2107.10830.

[19] Neural ISS Lab. (2024). "ATLAS: An IoT Architecture for Secure Networking." arXiv:2212.10289.

[20] Garman, C., Kaptchuk, G., Juels, A., & Sirer, E. G. (2016). "Dancing with Devils: Cryptanalysis of HaLo." Proceedings of IEEE Security & Privacy.

[21] Stattner, P., & Collard, M. (2014). "Social Relation Networks for Semantic Disambiguation of Wikipedia Concepts." Computational Linguistics Research.

[22] Shostack, A. (2014). "Threat Modeling: Designing for Security." John Wiley & Sons.

[23] Brandes, U. (2008). "On Variants of Shortest-Path Betweenness Centrality and Their Generic Computation." Social Networks, 30(2), 136-145.

[24] Newman, M. E. J. (2003). "The Structure and Function of Complex Networks." SIAM Review, 45(2), 167-256.

[25] Grover, A., & Leskovec, J. (2016). "node2vec: Scalable Feature Learning for Networks." Proceedings of ACM SIGKDD.

[26] Müller, T., Rauli, P., & Sigwart, M. (2020). "Evaluating Wireless Protocol Security: A Systematic Review." Journal of Information Security Applications, 54, 102537.

[27] RFC 6090. (2011). Fundamentals of Integer Arithmetic over Finite Fields. IETF.

[28] RFC 3394. (2002). Advanced Encryption Standard (AES) Key Wrap Algorithm. IETF.

[29] NIST SP 800-56B. (2019). Recommendation for Pair-Wise Key Establishment Schemes Using Discrete Logarithm Cryptography. NIST.

[30] Rogaway, P., Bellare, M., Black, R., & Krovetz, T. (2001). "OCB: A Block-Cipher Mode of Operation for Efficient Authenticated Encryption." Proceedings of ACM CCS.

---

**Document Version:** 1.0  
**Last Updated:** December 16, 2025  
**Author:** Security Research Team  
**Status:** Active - Ready for Implementation

---

### Quick Reference: Key Commands & Links

**Setup & Installation:**
```bash
git clone https://github.com/your-username/wireless-protocol-security-analysis.git
cd wireless-protocol-security-analysis
python -m venv venv
source venv/bin/activate
pip install -r requirements-dev.txt
python -m pytest tests/ -v --cov=src/
```

**Hardware Setup:**
- Ubertooth: `ubertooth-util -fu ~/path/to/ubertooth.dfu`
- ApiMote: Refer to River Loop Security documentation
- nRF52840: Flashing via J-Link or DAPLink

**Run CLI:**
```bash
python -m wireless_protocol_analyzer capture -d ubertooth -t 60 -o capture.pcap
python -m wireless_protocol_analyzer analyze capture.pcap --full
python -m wireless_protocol_analyzer report capture.pcap --format html
```

**Project Links:**
- GitHub Repository: [Your GitHub URL]
- Documentation: [ReadTheDocs URL]
- Issue Tracker: [GitHub Issues]
- Discussions: [GitHub Discussions]
- Paper Preprint: [arXiv or Academia.edu]
