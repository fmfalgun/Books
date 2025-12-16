# Project 2: UML Architecture & Execution Flow Diagrams

**Document Version:** 1.0  
**Last Updated:** December 16, 2025

---

## Table of Contents

1. [System Architecture Overview](#system-architecture-overview)
2. [Project Execution Flow (Timeline)](#project-execution-flow-timeline)
3. [Module Dependency Diagram](#module-dependency-diagram)
4. [Tool & Technology Stack Mapping](#tool--technology-stack-mapping)
5. [Data Flow Architecture](#data-flow-architecture)
6. [CI/CD Pipeline Workflow](#cicd-pipeline-workflow)
7. [Deployment Pipeline Sequence](#deployment-pipeline-sequence)
8. [Phase-Wise Tool Allocation Matrix](#phase-wise-tool-allocation-matrix)

---

## 1. System Architecture Overview

### High-Level System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        WIRELESS PROTOCOL SECURITY ANALYZER                  │
│                         (Project 2 - Complete System)                       │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                          INPUT LAYER (Hardware)                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐         │
│  │  Ubertooth One   │  │   ApiMote v4     │  │  nRF52840 DK     │         │
│  │   (BLE Sniffer)  │  │ (Zigbee Sniffer) │  │ (Test Target)    │         │
│  │                  │  │                  │  │                  │         │
│  │  USB Device      │  │  USB Device      │  │  USB/UART Dev    │         │
│  └────────┬─────────┘  └────────┬─────────┘  └────────┬─────────┘         │
│           │                     │                     │                   │
│           └─────────────────────┼─────────────────────┘                   │
│                                 │                                         │
└─────────────────────────────────┼─────────────────────────────────────────┘
                                  │
                    [libusb, PyUSB, serial driver]
                                  │
┌─────────────────────────────────┼─────────────────────────────────────────┐
│                      CAPTURE LAYER (MOD-001/008)                          │
├─────────────────────────────────┼─────────────────────────────────────────┤
│                                 │                                         │
│           ┌───────────────────────────────────────────────┐              │
│           │  MOD-001: Packet Sniffer Engine              │              │
│           │  MOD-008: Hardware Abstraction Layer         │              │
│           │                                               │              │
│           │  - USB enumeration                           │              │
│           │  - Channel/frequency configuration           │              │
│           │  - Raw packet capture (PCAP format)          │              │
│           │  - Timestamp normalization                   │              │
│           │  - Multi-device sync                         │              │
│           └─────────────────────┬───────────────────────┘              │
│                                 │                                         │
│                    [Scapy, pyusb, h5py]                                  │
│                                 │                                         │
└─────────────────────────────────┼─────────────────────────────────────────┘
                                  │
                        Output: PCAP / HDF5 files
                                  │
┌─────────────────────────────────┼─────────────────────────────────────────┐
│                    ANALYSIS LAYER (MOD-002 through MOD-006)               │
├─────────────────────────────────┼─────────────────────────────────────────┤
│                                 │                                         │
│  ┌──────────────────────────────▼──────────────────────────────────────┐ │
│  │  MOD-002: Protocol Parser & Dissector                              │ │
│  │  ├─ Parse BLE LL/L2CAP/GATT/ATT layers                             │ │
│  │  ├─ Parse Zigbee MAC/NWK/APL layers                                │ │
│  │  ├─ Build packet tree (field extraction)                           │ │
│  │  └─ Detect malformed packets                                       │ │
│  │                                                                     │ │
│  │  Tools: [Scapy layers, struct, custom state machine]               │ │
│  └────────────────────┬─────────────────────────────────────────────┘ │
│                       │                                                 │
│         ┌─────────────┼─────────────┐                                  │
│         │             │             │                                  │
│    ┌────▼────┐  ┌────▼────┐  ┌────▼────┐                             │
│    │ MOD-003 │  │ MOD-004 │  │ MOD-005 │                             │
│    │ Crypto  │  │ Fuzzing │  │ State   │                             │
│    │Analysis │  │ Engine  │  │Machine  │                             │
│    │         │  │         │  │Analyzer │                             │
│    ├─Weak key├─ ├─Mutation├─ ├─Graph   │                             │
│    │detect   │  │testing  │  │building │                             │
│    ├─IV extr.├─ ├─Coverage├─ ├─Anomaly │                             │
│    │         │  │-guided  │  │detect   │                             │
│    ├─Nonce   ├─ ├─AFL++   ├─ ├─Formal  │                             │
│    │reuse    │  │libFuzzer│  │model    │                             │
│    └────┬────┘  └────┬────┘  └────┬────┘                             │
│         │             │             │                                  │
│    [crypto lib]  [AFL++,Radamsa]  [NetworkX]                          │
│         │             │             │                                  │
│         └─────────────┼─────────────┘                                  │
│                       │                                                 │
│               Vulnerability findings                                    │
│                       │                                                 │
│    ┌──────────────────▼──────────────────┐                            │
│    │  MOD-006: ML Anomaly Detection      │                            │
│    │  ├─ Feature extraction              │                            │
│    │  ├─ Isolation Forest                │                            │
│    │  ├─ Autoencoders (optional)         │                            │
│    │  └─ Anomaly scoring                 │                            │
│    │                                      │                            │
│    │  Tools: [scikit-learn, numpy, pandas]                            │
│    └──────────────────┬───────────────────┘                            │
│                       │                                                 │
└───────────────────────┼─────────────────────────────────────────────────┘
                        │
            Aggregated vulnerability database
                        │
┌───────────────────────┼─────────────────────────────────────────────────┐
│                 REPORTING LAYER (MOD-007/009/010)                      │
├───────────────────────┼─────────────────────────────────────────────────┤
│                       │                                                 │
│  ┌────────────────────▼─────────────────────────────────────────────┐ │
│  │ MOD-007: Vulnerability Report Generator                         │ │
│  │ ├─ CVSS scoring (CVSS 3.1)                                      │ │
│  │ ├─ CWE/CVE mapping                                              │ │
│  │ ├─ Remediation guidance                                         │ │
│  │ └─ Report formatting (PDF/HTML/Markdown)                        │ │
│  │                                                                  │ │
│  │ Tools: [jinja2, reportlab, CVSS calculator]                     │ │
│  └────────────────┬──────────────────────────────────────────────┘ │
│                   │                                                 │
│  ┌────────────────▼──────────────────────────────────────────────┐ │
│  │ MOD-009: Interactive CLI & Visualization                     │ │
│  │ ├─ Command interface (20+ commands)                          │ │
│  │ ├─ Real-time monitoring dashboard                            │ │
│  │ ├─ Data export (PCAP, JSON, CSV, HTML)                       │ │
│  │ └─ Web API (FastAPI)                                         │ │
│  │                                                               │ │
│  │ Tools: [Click, Rich, FastAPI, Plotly]                        │ │
│  └────────────────┬──────────────────────────────────────────────┘ │
│                   │                                                 │
│  ┌────────────────▼──────────────────────────────────────────────┐ │
│  │ MOD-010: Documentation & Publication                         │ │
│  │ ├─ API docs (Sphinx)                                         │ │
│  │ ├─ Tutorial notebooks (Jupyter)                              │ │
│  │ ├─ Research paper (LaTeX/Markdown)                           │ │
│  │ └─ Conference presentations (video)                          │ │
│  │                                                               │ │
│  │ Tools: [Sphinx, Jupyter, Pandoc, LaTeX]                      │ │
│  └───────────┬───────────────────────────────────────────────────┘ │
│              │                                                     │
└──────────────┼─────────────────────────────────────────────────────┘
               │
        ┌──────▼──────────┐
        │   Deliverables  │
        ├─────────────────┤
        │ • PCAP captures │
        │ • HTML reports  │
        │ • Findings PDF  │
        │ • CLI tool      │
        │ • Research paper│
        │ • Code repo     │
        └─────────────────┘
```

---

## 2. Project Execution Flow (Timeline)

### Phase-Based Execution Diagram

```
WEEK 0                          WEEK 6                          WEEK 12
│                               │                               │
│                               │                               │
┌──────────────────────────────────────────────────────────────────────┐
│ PHASE 1: FOUNDATION (Weeks 1-2)                                      │
├──────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  Step 1: Project Setup                                               │
│  ├─ Tools: Git, GitHub, VS Code, Docker                              │
│  └─ Output: Repository initialized, CI/CD configured                │
│                                                                       │
│  Step 2: Hardware Procurement & Setup                               │
│  ├─ Hardware: Ubertooth One, ApiMote v4, nRF52840                    │
│  ├─ Tools: libusb, pyusb, device drivers                             │
│  └─ Output: All devices USB-enumerable, firmware updated             │
│                                                                       │
│  Step 3: Development Environment Setup                              │
│  ├─ Tools: Python 3.11, pyenv, venv, Poetry                          │
│  ├─ Tools: pre-commit, black, isort, ruff, mypy                      │
│  └─ Output: Local dev environment ready, code quality gates active   │
│                                                                       │
│  Step 4: Docker & Container Setup                                   │
│  ├─ Tools: Docker, Docker Compose                                    │
│  ├─ Tools: python:3.11-slim image                                    │
│  └─ Output: Multi-service docker-compose.yml working                 │
│                                                                       │
└────────────────────────────┬───────────────────────────────────────┘
                             │
                             │ deliverables: project skeleton
                             │
┌──────────────────────────────────────────────────────────────────────┐
│ PHASE 2: CORE PACKET CAPTURE & PARSING (Weeks 3-5)                  │
├──────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  MOD-001 + MOD-008 Development                                       │
│  ├─ Week 3: USB enumeration & hardware abstraction                   │
│  │   Tools: [pyusb, libusb, threading]                               │
│  │   Output: HW abstraction layer (BaseHardware class)               │
│  │                                                                   │
│  ├─ Week 4: Packet capture pipeline                                  │
│  │   Tools: [Scapy, h5py, PCAP format]                               │
│  │   Output: PCAP files with normalized timestamps                   │
│  │                                                                   │
│  └─ Week 5: Multi-device sync + testing                              │
│      Tools: [pytest, Wireshark (comparison)]                         │
│      Output: 99.5% packet recovery rate validated                    │
│                                                                       │
│  MOD-002 Development                                                 │
│  ├─ Week 3-4: Protocol dissector for BLE                             │
│  │   Tools: [Scapy, struct, RFC specs]                               │
│  │   Output: BLE LL → L2CAP → GATT parser chain                      │
│  │                                                                   │
│  ├─ Week 4-5: Protocol dissector for Zigbee                          │
│  │   Tools: [KillerBee, Scapy ZigBee layer, IEEE 802.15.4]          │
│  │   Output: Zigbee MAC → NWK → APL parser chain                     │
│  │                                                                   │
│  └─ Week 5: Validation against Wireshark                             │
│      Tools: [Wireshark, tshark, pytest]                              │
│      Output: 100% RFC compliance verified on 500+ packets            │
│                                                                       │
│  Testing & Integration                                              │
│  ├─ Tools: pytest (unit tests), Docker Compose (integration)         │
│  ├─ Tools: coverage.py (target: 90% coverage)                        │
│  └─ Output: CI/CD green (all tests passing)                          │
│                                                                       │
└────────────────────────────┬───────────────────────────────────────┘
                             │
                             │ deliverables: MOD-001/002/008 working
                             │
┌──────────────────────────────────────────────────────────────────────┐
│ PHASE 3: ANALYSIS & VULNERABILITY DETECTION (Weeks 6-9)             │
├──────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  MOD-003 Development (Crypto Analysis)                              │
│  ├─ Week 6: Weak key detection                                       │
│  │   Tools: [cryptography library, PyCryptodome]                     │
│  │   Output: Detect known weak BLE keys (CVE catalog)                │
│  │                                                                   │
│  ├─ Week 6-7: Nonce/IV extraction                                    │
│  │   Tools: [struct parsing, numpy arrays]                           │
│  │   Output: Extract IVs from encrypted payloads                     │
│  │                                                                   │
│  └─ Week 7: GPU acceleration (optional)                              │
│      Tools: [PyCUDA, CUDA 12.4 (optional)]                           │
│      Output: 5-10x speedup on crypto brute-force                     │
│                                                                       │
│  MOD-004 Development (Fuzzing Engine)                               │
│  ├─ Week 6-7: Mutation framework                                     │
│  │   Tools: [Radamsa, custom mutation operators]                     │
│  │   Output: Mutation strategy (bit-flip, boundary, swap)            │
│  │                                                                   │
│  ├─ Week 7-8: Coverage-guided fuzzing                                │
│  │   Tools: [AFL++, libFuzzer (optional)]                            │
│  │   Output: ≥1000 packets/sec mutation rate                         │
│  │                                                                   │
│  ├─ Week 8: Fuzz harness for target devices                          │
│  │   Tools: [GDB, nRF dev kit]                                       │
│  │   Output: Crash detection & categorization                        │
│  │                                                                   │
│  └─ Week 8-9: Large-scale fuzzing (≥100 hours)                       │
│      Tools: [Raspberry Pi cluster, Kubernetes (optional)]            │
│      Output: Vulnerability database seeded with findings             │
│                                                                       │
│  MOD-005 Development (State Machine Analysis)                       │
│  ├─ Week 6-7: Packet sequence clustering                             │
│  │   Tools: [pandas, sklearn clustering]                             │
│  │   Output: Group packets by session ID                             │
│  │                                                                   │
│  ├─ Week 7: State transition extraction                              │
│  │   Tools: [NetworkX, graph algorithms]                             │
│  │   Output: Directed graph of state transitions                     │
│  │                                                                   │
│  ├─ Week 8: Anomaly detection in FSM                                 │
│  │   Tools: [Custom logic, formal methods (TLA+ optional)]           │
│  │   Output: Out-of-order transitions identified                     │
│  │                                                                   │
│  └─ Week 8-9: Formal model generation                                │
│      Tools: [Promela/TLA+, model checker]                            │
│      Output: Formal FSM model (<5min verification)                   │
│                                                                       │
│  MOD-006 Development (ML Anomaly Detection)                         │
│  ├─ Week 6: Feature engineering                                      │
│  │   Tools: [pandas, numpy, scipy]                                   │
│  │   Output: Timing, size, pattern feature vectors                   │
│  │                                                                   │
│  ├─ Week 7-8: Model training                                         │
│  │   Tools: [scikit-learn, isolation forest, autoencoder]            │
│  │   Output: Trained models (F1 ≥0.85)                               │
│  │                                                                   │
│  └─ Week 8-9: Validation & tuning                                    │
│      Tools: [cross-validation, hyperopt]                             │
│      Output: <3% false positive rate achieved                        │
│                                                                       │
└────────────────────────────┬───────────────────────────────────────┘
                             │
                             │ deliverables: ≥2 vulnerabilities found
                             │
┌──────────────────────────────────────────────────────────────────────┐
│ PHASE 4: INTEGRATION & REPORTING (Weeks 10-12)                      │
├──────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  MOD-007 Development (Report Generation)                            │
│  ├─ Week 10: Vulnerability aggregation                               │
│  │   Tools: [pandas, CVSS 3.1 calculator]                            │
│  │   Output: Scored vulnerability list (CVSS JSON)                   │
│  │                                                                   │
│  ├─ Week 10-11: Report formatting                                    │
│  │   Tools: [jinja2, reportlab, LaTeX]                               │
│  │   Output: HTML, PDF, Markdown reports (<10min generation)         │
│  │                                                                   │
│  └─ Week 11: Remediation guidance                                    │
│      Tools: [CVSS, CVE database API]                                 │
│      Output: Actionable fixes for each vulnerability                 │
│                                                                       │
│  MOD-009 Development (CLI & Dashboard)                              │
│  ├─ Week 10: CLI command framework                                   │
│  │   Tools: [Click, argparse, Rich]                                  │
│  │   Output: 20+ commands (capture, analyze, report, export)         │
│  │                                                                   │
│  ├─ Week 10-11: Web dashboard (optional)                             │
│  │   Tools: [FastAPI, Vue.js/React, Plotly]                          │
│  │   Output: Real-time monitoring dashboard                          │
│  │                                                                   │
│  └─ Week 11: End-to-end workflow testing                             │
│      Tools: [pytest, shell scripts]                                  │
│      Output: Full pipeline functional (capture → report)             │
│                                                                       │
│  MOD-010 Development (Documentation & Publication)                  │
│  ├─ Week 11: Technical documentation                                 │
│  │   Tools: [Sphinx, MkDocs, ReadTheDocs]                            │
│  │   Output: Complete API docs (95% coverage)                        │
│  │                                                                   │
│  ├─ Week 11: Research paper writing                                  │
│  │   Tools: [LaTeX, Pandoc, IEEE template]                           │
│  │   Output: 8-10 page paper (IEEE S&P format)                       │
│  │                                                                   │
│  ├─ Week 11-12: Tutorial notebooks                                   │
│  │   Tools: [Jupyter, nbconvert]                                     │
│  │   Output: 3-5 end-to-end walkthroughs                             │
│  │                                                                   │
│  └─ Week 12: Conference preparation                                  │
│      Tools: [video recording, presentation slides]                   │
│      Output: Ready for DEF CON/Black Hat submission                  │
│                                                                       │
│  Final Integration & Release                                        │
│  ├─ Week 12: Integration testing (all modules)                       │
│  │   Tools: [pytest, docker-compose, CI/CD]                          │
│  │   Output: All systems green, code coverage ≥85%                   │
│  │                                                                   │
│  ├─ Week 12: GitHub release & PyPI package                           │
│  │   Tools: [GitHub Actions, twine]                                  │
│  │   Output: v1.0.0 released (semantic versioning)                   │
│  │                                                                   │
│  └─ Week 12: Responsible disclosure                                  │
│      Tools: [CERT/CC, vendor communication protocol]                 │
│      Output: 90-day embargo process initiated                        │
│                                                                       │
└────────────────────────────┬───────────────────────────────────────┘
                             │
                             │ deliverables: Production-ready system
                             │
                    RELEASE & PUBLICATION
                             │
                ┌────────────────────────────┐
                │  GitHub Repository        │
                │  PyPI Package             │
                │  Conference Papers        │
                │  Blog Posts               │
                │  Video Presentations      │
                └────────────────────────────┘
```

---

## 3. Module Dependency Diagram

### Class & Module Interaction Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         MODULE DEPENDENCY GRAPH                             │
└─────────────────────────────────────────────────────────────────────────────┘

                            ┌──────────────────┐
                            │  Configuration   │
                            │   (YAML/TOML)    │
                            └────────┬─────────┘
                                     │
                                     │ config loader
                                     │
        ┌────────────────────────────┼────────────────────────────┐
        │                            │                            │
        │                            │                            │
   ┌────▼──────────┐         ┌──────▼─────────┐         ┌────────▼────────┐
   │   MOD-008     │         │   MOD-001      │         │   MOD-002       │
   │  Hardware     │◄────────┤   Sniffer      │◄────────┤   Parser        │
   │ Abstraction   │         │   Engine       │         │   Dissector     │
   │               │         │                │         │                 │
   │ - USB access  │         │ - USB device   │         │ - BLE stack     │
   │ - Driver I/O  │         │ - Packet       │         │ - Zigbee stack  │
   │ - Config mgmt │         │   capture      │         │ - Field extract │
   │               │         │ - Timestamps   │         │                 │
   └────┬──────────┘         └──────┬─────────┘         └────────┬────────┘
        │                           │                           │
        │ provides                  │ output                     │ parsed
        │ device API                │ PCAP/HDF5                 │ packets
        │                           │                           │
        └───────────────────────────┼───────────────────────────┘
                                    │
                        ┌───────────┴───────────┐
                        │                       │
              ┌─────────▼───────┐       ┌──────▼──────────┐
              │    Storage      │       │   MOD-003       │
              │  (InfluxDB OSS) │       │   Crypto        │
              │                 │       │   Analysis      │
              │ - Time series   │       │                 │
              │ - Query API     │       │ - Weak keys     │
              │ - Retention mgmt│       │ - Nonce extract │
              │                 │       │ - Crypto bugs   │
              └────────┬────────┘       └────────┬────────┘
                       │                         │
                       │                    ┌────┴────────────┐
                       │                    │                 │
                       │            ┌───────▼───────────┐     │
                       │            │   Vulnerability   │     │
                       │            │   Database        │     │
                       │            │                   │     │
                       │            │ - CVE ID          │     │
                       │            │ - CVSS scores     │     │
                       │            │ - Fixes           │     │
                       │            └───┬───────────────┘     │
                       │                │                     │
              ┌────────▼────────┐       │  ┌──────────────────▼────────┐
              │   MOD-004       │       │  │  Vulnerability data flow   │
              │   Fuzzing       │       │  │                           │
              │   Engine        │       │  │  MOD-003 ───────┐        │
              │                 │       │  │                │        │
              │ - Mutations     │       │  │  MOD-004 ───┬──┤        │
              │ - Coverage      │       │  │             │  │        │
              │ - Crash detect  │       │  │  MOD-005 ───┘  │        │
              │                 │       │  │                │        │
              └────────┬────────┘       │  │  MOD-006 ───────┘        │
                       │                │  │                          │
              ┌────────▼────────┐       │  └──────────┬────────────────┘
              │   MOD-005       │       │             │
              │   State Machine │       │   ┌─────────▼────────┐
              │   Analyzer      │       │   │   MOD-007        │
              │                 │       │   │   Report Gen     │
              │ - FSM building  │       │   │                  │
              │ - Transitions   │       │   │ - CVSS scoring   │
              │ - Anomalies     │       │   │ - PDF/HTML gen   │
              │                 │       │   │ - Remediation    │
              └────────┬────────┘       └──→│   guidance       │
                       │                    │                  │
              ┌────────▼────────┐           └─────────┬────────┘
              │   MOD-006       │                     │
              │   ML Anomaly    │         ┌───────────▼────────┐
              │   Detection     │         │   MOD-009          │
              │                 │         │   CLI & Dashboard  │
              │ - Features      │         │                    │
              │ - Models        │         │ - Commands         │
              │ - Scoring       │         │ - Dashboards       │
              │                 │         │ - Exports          │
              └────────┬────────┘         │                    │
                       │                  └─────────┬──────────┘
                       │                            │
                       └────────────────┬───────────┘
                                        │
                                 ┌──────▼──────────┐
                                 │   MOD-010       │
                                 │   Documentation │
                                 │   & Publishing  │
                                 │                 │
                                 │ - API docs      │
                                 │ - Research paper│
                                 │ - Tutorials     │
                                 │ - GitHub repo   │
                                 └─────────────────┘
```

### Module Sequence Flow

```
User Request
    │
    ▼
[CLI Interface - MOD-009]
    │
    ├─── capture command ─────────▶ [MOD-008] [MOD-001]
    │                                   │       │
    │                                   ▼       ▼
    │                               USB enumeration
    │                                   │
    │                                   ▼
    │                           [PCAP output file]
    │
    ├─── analyze command ─────────▶ [MOD-002]
    │                                   │
    │                                   ▼
    │                           [Parsed packets]
    │                                   │
    │    ┌──────────────┬──────────────┼──────────────┐
    │    │              │              │              │
    │    ▼              ▼              ▼              ▼
    │  [MOD-003]    [MOD-004]      [MOD-005]     [MOD-006]
    │   Crypto      Fuzzing        State FSM      ML Models
    │   Analysis    Engine         Analyzer       Anomaly
    │    │              │              │              │
    │    └──────────────┼──────────────┼──────────────┘
    │                   │
    │                   ▼
    │           [Vulnerability DB]
    │
    ├─── report command ──────────▶ [MOD-007]
    │                                   │
    │                                   ▼
    │                           [CVSS scoring]
    │                                   │
    │                                   ▼
    │                        [HTML/PDF report]
    │
    └─── export command ──────────▶ [Data Formatter]
                                        │
                                        ▼
                                 [JSON/CSV/PCAP]
```

---

## 4. Tool & Technology Stack Mapping

### Tool-to-Module Matrix

```
┌────────────────────────────────────────────────────────────────────────────┐
│                   TOOL ALLOCATION BY MODULE & PHASE                        │
└────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────┬──────────┬──────────┬──────────┬──────────┬──────────┐
│ TOOL / TECHNOLOGY   │ MOD-001  │ MOD-002  │ MOD-003  │ MOD-004  │ MOD-005  │
├─────────────────────┼──────────┼──────────┼──────────┼──────────┼──────────┤
│ Python 3.11         │    ✓     │    ✓     │    ✓     │    ✓     │    ✓     │
│ Scapy               │    ✓     │    ✓     │    ✓     │    ✓     │          │
│ pyusb               │    ✓     │          │          │          │          │
│ libusb              │    ✓     │          │          │          │          │
│ h5py                │    ✓     │          │          │          │          │
│ struct (stdlib)     │          │    ✓     │          │          │          │
│ cryptography lib    │          │          │    ✓     │          │          │
│ PyCryptodome        │          │          │    ✓     │          │          │
│ Radamsa             │          │          │          │    ✓     │          │
│ AFL++               │          │          │          │    ✓     │          │
│ libFuzzer           │          │          │          │    ✓     │          │
│ NetworkX            │          │          │          │          │    ✓     │
│ TLA+ / Promela      │          │          │          │          │    ✓     │
│ pytest              │    ✓     │    ✓     │    ✓     │    ✓     │    ✓     │
│ pytest-cov          │    ✓     │    ✓     │    ✓     │    ✓     │    ✓     │
│ Docker              │    ✓     │    ✓     │    ✓     │    ✓     │    ✓     │
│ GitHub Actions      │    ✓     │    ✓     │    ✓     │    ✓     │    ✓     │
│ GDB (debugger)      │    ✓     │          │          │    ✓     │          │
│ Wireshark           │          │    ✓     │          │          │          │
│ Kali Linux          │          │    ✓     │    ✓     │    ✓     │          │
├─────────────────────┼──────────┼──────────┼──────────┼──────────┼──────────┤
│ TOOL / TECHNOLOGY   │ MOD-006  │ MOD-007  │ MOD-008  │ MOD-009  │ MOD-010  │
├─────────────────────┼──────────┼──────────┼──────────┼──────────┼──────────┤
│ Python 3.11         │    ✓     │    ✓     │    ✓     │    ✓     │    ✓     │
│ scikit-learn        │    ✓     │          │          │          │          │
│ numpy               │    ✓     │          │          │    ✓     │          │
│ pandas              │    ✓     │    ✓     │          │    ✓     │          │
│ matplotlib          │    ✓     │    ✓     │          │          │          │
│ jinja2              │          │    ✓     │          │    ✓     │          │
│ reportlab           │          │    ✓     │          │          │          │
│ Click               │          │          │          │    ✓     │          │
│ Rich                │          │          │          │    ✓     │          │
│ FastAPI             │          │          │          │    ✓     │          │
│ Plotly              │          │          │          │    ✓     │          │
│ Sphinx              │          │          │          │          │    ✓     │
│ Jupyter             │          │          │          │          │    ✓     │
│ Pandoc              │          │          │          │          │    ✓     │
│ LaTeX               │          │    ✓     │          │          │    ✓     │
│ pytest              │    ✓     │    ✓     │    ✓     │    ✓     │    ✓     │
│ Docker              │    ✓     │    ✓     │    ✓     │    ✓     │    ✓     │
│ GitHub Actions      │    ✓     │    ✓     │    ✓     │    ✓     │    ✓     │
└─────────────────────┴──────────┴──────────┴──────────┴──────────┴──────────┘

Legend:
✓ = Primary tool for this module
(blank) = Not used in this module
```

### Database & Storage Mapping

```
┌──────────────────────────────────────────────────────────────┐
│           DATA STORAGE & RETRIEVAL BY PHASE                  │
└──────────────────────────────────────────────────────────────┘

DEVELOPMENT PHASE:
┌─────────────────────────────────────────────────────────────┐
│ Storage Layer          │ Technology        │ Use Case       │
├─────────────────────────────────────────────────────────────┤
│ Local packet cache     │ SQLite            │ Unit testing   │
│ Sample PCAP files      │ HDF5 files        │ Fixtures       │
│ Time series (testing)  │ InfluxDB OSS      │ Dev database   │
│ Configuration          │ YAML/JSON files   │ Parametrization│
└─────────────────────────────────────────────────────────────┘

PRODUCTION PHASE:
┌─────────────────────────────────────────────────────────────┐
│ Storage Layer          │ Technology        │ Use Case       │
├─────────────────────────────────────────────────────────────┤
│ Real-time packets      │ InfluxDB Cloud    │ Live streaming │
│ Historical archive     │ S3 + Glacier      │ Cold storage   │
│ Query database         │ TimescaleDB (RDS) │ Analytics      │
│ Vulnerability data     │ PostgreSQL        │ Reporting      │
│ Logs & tracing         │ Loki + ELK        │ Observability  │
│ Models & artifacts     │ S3 + artifact repo│ ML persistence │
└─────────────────────────────────────────────────────────────┘
```

### Infrastructure-to-Phase Mapping

```
┌──────────────────────────────────────────────────────────────┐
│     INFRASTRUCTURE DEPLOYMENT ACROSS PHASES                  │
└──────────────────────────────────────────────────────────────┘

PHASE 1-2 (Weeks 1-5): DEVELOPMENT
┌─────────────────────────────────────┐
│ Local Workstation                   │
├─────────────────────────────────────┤
│ • Python venv (local)               │
│ • Docker Compose (single host)      │
│ • SQLite (dev DB)                   │
│ • InfluxDB OSS (optional)           │
│ • Kali VM (VirtualBox)              │
│ • GitHub (code repo)                │
│ • GitHub Actions (CI/CD)            │
│ • VS Code + debugging               │
└─────────────────────────────────────┘

PHASE 3-4 (Weeks 6-12): TESTING → PRODUCTION
┌──────────────────────────────────────────────────────────────┐
│ AWS Infrastructure (Recommended)                             │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│ Dev Environment:                  Staging:                  │
│ ├─ t2.micro EC2                  ├─ t3.small EC2            │
│ ├─ RDS db.t3.micro               ├─ RDS db.t3.small         │
│ ├─ InfluxDB OSS                  ├─ InfluxDB Cloud (trial) │
│ ├─ GitHub Actions                ├─ Docker Compose          │
│ └─ $10-20/month                  └─ $50-100/month           │
│                                                              │
│ Production Environment:                                     │
│ ├─ EKS (3-5 nodes)                                           │
│ ├─ InfluxDB Cloud (managed)                                  │
│ ├─ RDS (db.t3.small → db.t3.medium)                         │
│ ├─ S3 (archive storage)                                      │
│ ├─ ECR (container registry)                                  │
│ ├─ CloudWatch (monitoring)                                   │
│ ├─ Loki (log aggregation)                                    │
│ ├─ Prometheus + Grafana (dashboards)                         │
│ └─ $200-500/month                                            │
│                                                              │
└──────────────────────────────────────────────────────────────┘

EDGE DEPLOYMENT (Optional)
┌─────────────────────────────────────┐
│ Raspberry Pi (Edge Device)          │
├─────────────────────────────────────┤
│ • Python 3.11 (ARM64)               │
│ • InfluxDB OSS Edge                 │
│ • Wireless analyzer pod             │
│ • WireGuard VPN (to cloud)          │
│ • Local InfluxDB (sync via HTTP)    │
│ • ~$80-150 (one-time hardware)      │
└─────────────────────────────────────┘
```

---

## 5. Data Flow Architecture

### Complete Data Pipeline Diagram

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                           END-TO-END DATA PIPELINE                           │
└──────────────────────────────────────────────────────────────────────────────┘

INPUT DEVICES                CAPTURE LAYER              STORAGE LAYER
┌──────────────┐            ┌─────────────┐            ┌──────────────┐
│ Ubertooth    │            │   MOD-001   │            │  PCAP Files  │
│ (BLE, USB)   │──pyusb────▶│  Sniffer    │──PCAP──────▶│  (.pcap)     │
└──────────────┘            │  Engine     │            │              │
                            │             │            └────┬─────────┘
┌──────────────┐            │ • USB       │                 │
│ ApiMote v4   │            │   enumeration              HDF5 files
│ (Zigbee, USB)│──pyusb────▶│ • Config    │                 │
└──────────────┘            │ • Capture   │            ┌────▼─────────┐
                            │ • Normalize │            │  InfluxDB    │
┌──────────────┐            │             │            │  (Time       │
│ nRF52840 DK  │            └──────┬──────┘            │   Series)    │
│ (BLE+Zigbee) │──serial──────────┘                    │              │
└──────────────┘                 │                      └──────────────┘
                    ┌────────────▼────────────┐
                    │   MOD-002: Parser       │
                    │                         │
                    │ • RFC validation        │
                    │ • Field extraction      │
                    │ • Reassembly            │
                    │ • Error detection       │
                    └────────┬─────────────┬──┘
                             │             │
                    ┌────────▼──┐   ┌─────▼──────┐
                    │ Parsed    │   │  Malformed │
                    │ packets   │   │ logs       │
                    └────┬──────┘   └─────┬──────┘
                         │                │
        ┌────────────────┼────────────────┼─────────────────┐
        │                │                │                 │
    ┌───▼───┐        ┌───▼───┐       ┌───▼───┐         ┌───▼───┐
    │MOD-003│        │MOD-004│       │MOD-005│         │MOD-006│
    │Crypto │        │Fuzzing│       │State  │         │  ML   │
    │       │        │       │       │Machine│         │       │
    │Extract│ Mutate │Inject │ Parse │ FSM   │ Feature │Anomaly│
    │  IVs  │Test →  │Crashes│Trans. │ Graph │ Extract │Score  │
    │  Keys │  Vuln  │Bugs   │Detect │Build  │Classify │Detect │
    │       │        │       │       │       │         │       │
    └───┬───┘        └───┬───┘       └───┬───┘         └───┬───┘
        │                │               │                │
        │                │               │                │
        └────────────────┼───────────────┼────────────────┘
                         │               │
                    ┌────▼───────────────▼────┐
                    │  Vulnerability DB       │
                    │  ┌────────────────────┐ │
                    │  │ CVE IDs            │ │
                    │  │ CVSS Scores        │ │
                    │  │ Attack vectors    │ │
                    │  │ Findings           │ │
                    │  │ Anomalies          │ │
                    │  │ State violations   │ │
                    │  │ ML anomalies       │ │
                    │  └────────────────────┘ │
                    └────┬────────────────────┘
                         │
                    ┌────▼──────────────┐
                    │  MOD-007:         │
                    │  Report Generator │
                    │                   │
                    │ • CVSS scoring    │
                    │ • CWE mapping     │
                    │ • Remediation     │
                    │ • Format output   │
                    └────┬──────────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
    ┌───▼──┐         ┌───▼──┐        ┌───▼──┐
    │HTML  │         │ PDF  │        │Markdown
    │Report│         │Report│        │Report
    └───┬──┘         └───┬──┘        └───┬──┘
        │                │                │
        └────────────────┼────────────────┘
                         │
                    ┌────▼──────────────┐
                    │  MOD-009: CLI    │
                    │                   │
                    │ • User interface  │
                    │ • Dashboard       │
                    │ • Export options  │
                    │ • API endpoint    │
                    └────┬──────────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
    ┌───▼───┐        ┌───▼────┐     ┌───▼────┐
    │ JSON  │        │  CSV   │     │ PCAP   │
    │Export │        │ Export │     │ Export │
    └───┬───┘        └───┬────┘     └───┬────┘
        │                │              │
        └────────────────┼──────────────┘
                         │
                    ┌────▼────────┐
                    │  Archive    │
                    │ (S3/Glacier)│
                    └─────────────┘
```

---

## 6. CI/CD Pipeline Workflow

### GitHub Actions Pipeline Diagram

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                       CI/CD PIPELINE (GitHub Actions)                        │
└──────────────────────────────────────────────────────────────────────────────┘

Developer commits to GitHub
        │
        ▼
┌───────────────────────────────────────────────────────────────────┐
│ TRIGGER: [push to any branch] or [pull_request]                  │
└───────────────────────────────────────────────────────────────────┘
        │
        ▼
┌──────────────────────────────────┬──────────────────────────────┐
│  Matrix Strategy                 │  Python versions: 3.10, 3.11, 3.12
│  (parallel jobs)                 │  OS: ubuntu-latest
└──────────────────────────────────┴──────────────────────────────┘
        │
        ▼
┌──────────────────────────────────────────────────────────────────┐
│ JOB 1: LINT & QUALITY                                            │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│ Step 1.1: Checkout code                                          │
│ └─ Tool: actions/checkout@v4                                     │
│                                                                  │
│ Step 1.2: Setup Python                                           │
│ └─ Tool: actions/setup-python@v4                                 │
│                                                                  │
│ Step 1.3: Code formatting check (black)                          │
│ └─ Command: black --check src/                                   │
│                                                                  │
│ Step 1.4: Import sorting (isort)                                 │
│ └─ Command: isort --check src/                                   │
│                                                                  │
│ Step 1.5: Fast linting (ruff)                                    │
│ └─ Command: ruff check src/                                      │
│                                                                  │
│ Step 1.6: Type checking (mypy)                                   │
│ └─ Command: mypy src/                                            │
│                                                                  │
│ Step 1.7: Security linting (bandit)                              │
│ └─ Command: bandit -r src/                                       │
│                                                                  │
│ Output: ✓ PASS or ✗ FAIL (stops pipeline if fail)               │
└──────────────────────────────────────────────────────────────────┘
        │
        ├─ if FAIL → Notify developer, stop
        │
        ▼
┌──────────────────────────────────────────────────────────────────┐
│ JOB 2: UNIT TESTS                                                │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│ Step 2.1: Install dependencies                                   │
│ └─ Command: pip install -e .[dev]                                │
│                                                                  │
│ Step 2.2: Run unit tests (pytest)                                │
│ └─ Command: pytest tests/unit/ -v --cov=src/ --cov-report=xml   │
│                                                                  │
│ Step 2.3: Check coverage threshold                               │
│ └─ Command: coverage report --fail-under=85                      │
│                                                                  │
│ Step 2.4: Upload coverage to Codecov                             │
│ └─ Action: codecov/codecov-action@v3                             │
│                                                                  │
│ Output: Test results + coverage report                           │
└──────────────────────────────────────────────────────────────────┘
        │
        ├─ if FAIL → Notify developer, stop
        │
        ▼
┌──────────────────────────────────────────────────────────────────┐
│ JOB 3: INTEGRATION TESTS                                         │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│ Step 3.1: Start Docker Compose services                          │
│ └─ Command: docker-compose up -d                                 │
│                                                                  │
│ Step 3.2: Run integration tests                                  │
│ └─ Command: pytest tests/integration/ -v                         │
│                                                                  │
│ Step 3.3: Stop services                                          │
│ └─ Command: docker-compose down                                  │
│                                                                  │
│ Output: Integration test results                                 │
└──────────────────────────────────────────────────────────────────┘
        │
        ├─ if FAIL → Notify developer, stop
        │
        ▼
┌──────────────────────────────────────────────────────────────────┐
│ JOB 4: SECURITY SCANNING                                         │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│ Step 4.1: Dependency scanning (Grype)                            │
│ └─ Command: grype . --fail-on critical                           │
│                                                                  │
│ Step 4.2: SBOM generation                                        │
│ └─ Command: syft . -o json > sbom.json                           │
│                                                                  │
│ Step 4.3: Upload SBOM                                            │
│ └─ Store as artifact                                             │
│                                                                  │
│ Output: Security scan report                                     │
└──────────────────────────────────────────────────────────────────┘
        │
        ├─ if CRITICAL found → Notify, stop
        │
        ▼
┌──────────────────────────────────────────────────────────────────┐
│ JOB 5: BUILD & PUSH (only on main branch)                        │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│ Condition: if github.ref == 'refs/heads/main'                    │
│                                                                  │
│ Step 5.1: Setup Docker buildx                                    │
│ └─ Action: docker/setup-buildx-action@v2                         │
│                                                                  │
│ Step 5.2: Login to ECR                                           │
│ └─ Action: aws-actions/amazon-ecr-login@v1                       │
│                                                                  │
│ Step 5.3: Build & push image                                     │
│ └─ Action: docker/build-push-action@v5                           │
│    - Image: $REGISTRY/wireless-analyzer:$GIT_SHA                 │
│    - Tags: latest, v${SEMVER}                                    │
│                                                                  │
│ Step 5.4: Container scanning (Trivy)                             │
│ └─ Command: trivy image --severity HIGH $ECR_IMAGE               │
│                                                                  │
│ Output: Docker image pushed to ECR                               │
└──────────────────────────────────────────────────────────────────┘
        │
        ├─ if FAIL → Notify, don't deploy
        │
        ▼
┌──────────────────────────────────────────────────────────────────┐
│ JOB 6: DOCUMENTATION                                             │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│ Step 6.1: Build Sphinx docs                                      │
│ └─ Command: sphinx-build -W -b html docs/ docs/_build/           │
│                                                                  │
│ Step 6.2: Deploy to ReadTheDocs                                  │
│ └─ Automatic (webhook trigger)                                   │
│                                                                  │
│ Output: Documentation deployed                                   │
└──────────────────────────────────────────────────────────────────┘
        │
        ▼
┌──────────────────────────────────────────────────────────────────┐
│ FINAL RESULT                                                     │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│ ✓ ALL CHECKS PASSED:                                             │
│   ├─ Code quality validated                                      │
│   ├─ 85%+ coverage achieved                                      │
│   ├─ Integration tests passed                                    │
│   ├─ Security scan clean                                         │
│   ├─ Docker image built & scanned                                │
│   ├─ Documentation built                                         │
│   │                                                              │
│   └─ Ready for deployment                                        │
│                                                                  │
│ ✗ ANY CHECK FAILED:                                              │
│   ├─ Pipeline halted                                             │
│   ├─ PR marked as "not ready"                                    │
│   ├─ Feedback to developer                                       │
│   └─ Manual review required                                      │
└──────────────────────────────────────────────────────────────────┘
```

---

## 7. Deployment Pipeline Sequence

### Kubernetes Deployment Flow

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                    DEPLOYMENT PIPELINE (Kubernetes/AWS)                      │
└──────────────────────────────────────────────────────────────────────────────┘

Docker Image Pushed to ECR
        │
        ▼
┌──────────────────────────────────────────────────────────────────┐
│ STEP 1: Infrastructure Provisioning (Terraform)                 │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│ terraform apply -var-file=prod.tfvars                            │
│                                                                  │
│ Creates:                                                         │
│ ├─ VPC (Virtual Private Cloud)                                   │
│ ├─ EKS Cluster (3+ nodes)                                        │
│ ├─ RDS Instance (PostgreSQL + TimescaleDB)                       │
│ ├─ S3 Buckets (for archives)                                     │
│ ├─ Security Groups & IAM roles                                   │
│ └─ Load Balancer (Application LB)                                │
│                                                                  │
│ Output: Infrastructure ready                                    │
└──────────────────────────────────────────────────────────────────┘
        │
        ▼
┌──────────────────────────────────────────────────────────────────┐
│ STEP 2: GitOps Sync (ArgoCD) or Manual (kubectl)                │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│ Option A: GitOps (ArgoCD - Recommended)                          │
│ ├─ Git repo push triggers ArgoCD                                 │
│ └─ Auto-sync K8s manifests to cluster                            │
│                                                                  │
│ Option B: Manual (kubectl)                                       │
│ ├─ kubectl apply -f k8s/                                         │
│ └─ Deploy all manifests                                          │
│                                                                  │
│ Deploys:                                                         │
│ ├─ Namespace: wireless-analyzer                                  │
│ ├─ ConfigMaps: application config                                │
│ ├─ Secrets: API keys, credentials                                │
│ ├─ ServiceAccount: RBAC roles                                    │
│ ├─ PersistentVolumes: storage claims                             │
│ └─ Deployments: (see next step)                                  │
└──────────────────────────────────────────────────────────────────┘
        │
        ▼
┌──────────────────────────────────────────────────────────────────┐
│ STEP 3: Application Deployment                                  │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│ A. Deploy Core Services                                          │
│                                                                  │
│    wireless-analyzer Deployment                                  │
│    ├─ Image: $ECR_URL/wireless-analyzer:v1.0.0                   │
│    ├─ Replicas: 3 (initial)                                      │
│    ├─ Resources:                                                 │
│    │  ├─ Request: 500m CPU, 512Mi RAM                            │
│    │  └─ Limit: 2000m CPU, 2Gi RAM                               │
│    │                                                             │
│    ├─ Liveness probe (HTTP GET /health)                          │
│    │  └─ Restart if unhealthy                                    │
│    │                                                             │
│    ├─ Readiness probe (HTTP GET /ready)                          │
│    │  └─ Remove from load balancer if unready                    │
│    │                                                             │
│    ├─ Environment:                                               │
│    │  ├─ INFLUXDB_URL: http://influxdb:8086                      │
│    │  ├─ LOG_LEVEL: INFO                                         │
│    │  └─ DATABASE_URL: postgresql://...                          │
│    │                                                             │
│    └─ Rolling update strategy:                                   │
│       ├─ maxSurge: 1 (add 1 new pod)                             │
│       └─ maxUnavailable: 0 (no downtime)                         │
│                                                                  │
│    InfluxDB StatefulSet                                          │
│    ├─ Image: influxdb:2.7-alpine                                 │
│    ├─ Replicas: 1                                                │
│    ├─ PersistentVolume: 50Gi                                     │
│    ├─ Service (headless for StatefulSet)                         │
│    └─ Backup sidecar (daily snapshots)                           │
│                                                                  │
│    PostgreSQL StatefulSet                                        │
│    ├─ Managed via RDS (external)                                 │
│    ├─ TimescaleDB extension enabled                              │
│    └─ Automated backups (7-day retention)                        │
│                                                                  │
│ Output: All pods running                                        │
└──────────────────────────────────────────────────────────────────┘
        │
        ▼
┌──────────────────────────────────────────────────────────────────┐
│ STEP 4: Service Exposure                                        │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│ wireless-analyzer Service (LoadBalancer)                         │
│ ├─ Type: LoadBalancer (AWS ALB)                                  │
│ ├─ Port: 80 (external) → 8000 (container)                        │
│ └─ DNS: wireless-analyzer.example.com (via Route53)              │
│                                                                  │
│ Ingress Controller                                               │
│ ├─ AWS ALB Ingress Controller                                    │
│ ├─ Path-based routing                                            │
│ ├─ SSL/TLS termination                                           │
│ └─ WAF rules (optional)                                          │
│                                                                  │
│ Output: Service accessible at public endpoint                   │
└──────────────────────────────────────────────────────────────────┘
        │
        ▼
┌──────────────────────────────────────────────────────────────────┐
│ STEP 5: Auto-Scaling Configuration                              │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│ HorizontalPodAutoscaler (HPA)                                    │
│ ├─ Min replicas: 3                                               │
│ ├─ Max replicas: 10                                              │
│ │                                                               │
│ ├─ Metrics:                                                      │
│ │  ├─ CPU: target 70% utilization                                │
│ │  └─ Memory: target 80% utilization                             │
│ │                                                               │
│ ├─ Scale-up: add pod when threshold exceeded                     │
│ └─ Scale-down: remove pod if idle (5min window)                  │
│                                                                  │
│ Pod Disruption Budget                                            │
│ ├─ Min available: 2/3 pods                                       │
│ └─ Ensure availability during updates                            │
│                                                                  │
│ Output: Auto-scaling active                                     │
└──────────────────────────────────────────────────────────────────┘
        │
        ▼
┌──────────────────────────────────────────────────────────────────┐
│ STEP 6: Monitoring & Observability Setup                        │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│ Prometheus                                                       │
│ ├─ Scrape config for wireless-analyzer pods                      │
│ ├─ Scrape interval: 15 seconds                                   │
│ ├─ Metrics: CPU, memory, request latency, errors                 │
│ └─ Retention: 15 days                                            │
│                                                                  │
│ Grafana                                                          │
│ ├─ Data source: Prometheus                                       │
│ ├─ Dashboards:                                                   │
│ │  ├─ Cluster overview                                           │
│ │  ├─ Application performance                                    │
│ │  ├─ Error rates & SLOs                                         │
│ │  └─ Resource utilization                                       │
│ └─ URL: https://grafana.example.com                              │
│                                                                  │
│ Loki (Log Aggregation)                                           │
│ ├─ Promtail: collect pod logs                                    │
│ ├─ Scrape config: all containers                                 │
│ ├─ Labels: app, namespace, pod                                   │
│ └─ Retention: 30 days                                            │
│                                                                  │
│ Alerts (AlertManager)                                            │
│ ├─ High error rate (>5%)                                         │
│ ├─ Pod crash loop (restart >3x/5min)                             │
│ ├─ Memory pressure (>90%)                                        │
│ ├─ API latency (>1s p99)                                         │
│ └─ Notification: Slack, PagerDuty                                │
│                                                                  │
│ Output: Full observability stack running                         │
└──────────────────────────────────────────────────────────────────┘
        │
        ▼
┌──────────────────────────────────────────────────────────────────┐
│ STEP 7: Health Checks & Validation                              │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│ Smoke Tests                                                      │
│ ├─ curl https://wireless-analyzer.example.com/health             │
│ ├─ Expect: {"status": "ok"}                                      │
│ └─ Retry: 3 times with 10s backoff                               │
│                                                                  │
│ Integration Tests                                                │
│ ├─ End-to-end workflow:                                          │
│ │  ├─ /api/capture (start packet capture)                        │
│ │  ├─ Wait 5 seconds                                             │
│ │  ├─ /api/analyze (run analysis)                                │
│ │  └─ /api/report (generate report)                              │
│ └─ Verify output format & content                                │
│                                                                  │
│ Database Connection Tests                                        │
│ ├─ Connect to RDS PostgreSQL                                     │
│ ├─ Query TimescaleDB tables                                      │
│ ├─ Verify schema migrations applied                              │
│ └─ Check connection pool                                         │
│                                                                  │
│ Output: All health checks passed                                 │
└──────────────────────────────────────────────────────────────────┘
        │
        ▼
┌──────────────────────────────────────────────────────────────────┐
│ DEPLOYMENT COMPLETE ✓                                            │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│ Production checklist:                                            │
│ ✓ Infrastructure deployed (Terraform)                            │
│ ✓ K8s manifests applied                                          │
│ ✓ All pods running & healthy                                     │
│ ✓ Services exposed & loadbalanced                                │
│ ✓ Auto-scaling configured                                        │
│ ✓ Monitoring active (Prometheus, Grafana, Loki)                  │
│ ✓ Health checks passing                                          │
│ ✓ End-to-end tests successful                                    │
│ ✓ Database connected & validated                                 │
│ ✓ Rollback plan documented                                       │
│                                                                  │
│ Production system LIVE at:                                      │
│ • API: https://wireless-analyzer.example.com                     │
│ • Dashboards: https://grafana.example.com                        │
│ • Logs: https://loki.example.com                                 │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## 8. Phase-Wise Tool Allocation Matrix

### Comprehensive Tool Usage By Phase & Module

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                   DETAILED TOOL ALLOCATION MATRIX                            │
└──────────────────────────────────────────────────────────────────────────────┘

PHASE 1: FOUNDATION (Weeks 1-2)
┌──────────────────────────────────────┬──────────────────────────────────────┐
│ Infrastructure Setup                 │ Development Setup                    │
├──────────────────────────────────────┼──────────────────────────────────────┤
│ • Git                                │ • Python 3.11                        │
│ • GitHub (repo + Actions)            │ • pyenv (version manager)            │
│ • Docker + Docker Desktop            │ • Poetry (dependency mgmt)           │
│ • Docker Compose                     │ • VS Code + extensions               │
│ • AWS Account + CLI                  │ • pre-commit (git hooks)             │
│ • VirtualBox + Kali ISO              │ • pip-tools (lock files)             │
│ • VPN client (WireGuard/OpenVPN)     │ • black, isort, ruff, mypy           │
│ • Terraform (optional for IaC)       │ • Git workflow (main/dev branches)   │
└──────────────────────────────────────┴──────────────────────────────────────┘

PHASE 2: CORE PACKET CAPTURE & PARSING (Weeks 3-5)
┌──────────────────────────────────────┬──────────────────────────────────────┐
│ MOD-001 & MOD-008 Tools              │ MOD-002 Tools                        │
├──────────────────────────────────────┼──────────────────────────────────────┤
│ Hardware:                            │ Protocol Analysis:                   │
│ ├─ Ubertooth One + firmware          │ ├─ Wireshark (comparison reference) │
│ ├─ ApiMote v4 (optional)             │ ├─ tshark (CLI analysis)            │
│ └─ nRF52840 DK (optional)            │ ├─ tcpdump (packet capture)         │
│                                      │ └─ libpcap (PCAP library)           │
│ Python Libraries:                    │                                      │
│ ├─ pyusb (USB device access)         │ Python Libraries:                   │
│ ├─ libusb (native USB library)       │ ├─ Scapy (packet layers)            │
│ ├─ Scapy (packet format)             │ ├─ struct (binary parsing)          │
│ ├─ h5py (HDF5 file handling)         │ ├─ KillerBee (Zigbee specific)     │
│ ├─ threading (async capture)         │ ├─ BLEAK (BLE library)             │
│ └─ asyncio (async I/O)               │ └─ z3c (Zigbee parser)             │
│                                      │                                      │
│ Testing Tools:                       │ Testing & Validation:               │
│ ├─ pytest (unit tests)               │ ├─ pytest (RFC validation)         │
│ ├─ pytest-cov (coverage)             │ ├─ coverage.py (85%+ target)       │
│ ├─ mock (hardware mocking)           │ ├─ hypothesis (property tests)     │
│ └─ tox (multi-env testing)           │ └─ Docker (isolated testing)        │
│                                      │                                      │
│ Documentation:                       │ Documentation:                      │
│ ├─ docstrings (module docs)          │ ├─ RFC references (spec validation)│
│ └─ Sphinx (API docs)                 │ ├─ Protocol spec sheets            │
│                                      │ └─ Jupyter notebooks (examples)    │
└──────────────────────────────────────┴──────────────────────────────────────┘

PHASE 3: ANALYSIS & VULNERABILITY DETECTION (Weeks 6-9)
┌──────────────────────────────────────┬──────────────────────────────────────┐
│ MOD-003 & MOD-004 Tools              │ MOD-005 & MOD-006 Tools              │
├──────────────────────────────────────┼──────────────────────────────────────┤
│ Cryptography (MOD-003):              │ State Machine (MOD-005):             │
│ ├─ cryptography library              │ ├─ NetworkX (graph algorithms)      │
│ ├─ PyCryptodome                      │ ├─ pandas (data manipulation)       │
│ ├─ hashlib (stdlib)                  │ ├─ scikit-learn (clustering)        │
│ ├─ secrets (randomness)              │ ├─ matplotlib (FSM visualization)   │
│ ├─ struct (binary parsing)           │ ├─ pygraphviz (graph rendering)     │
│ └─ ctypes (native C libs)            │ └─ TLA+/Promela (formal methods)    │
│                                      │                                      │
│ Optional GPU:                        │ ML Anomaly Detection (MOD-006):    │
│ ├─ PyCUDA (CUDA compute)             │ ├─ scikit-learn (isolation forest) │
│ ├─ CuPy (GPU arrays)                 │ ├─ tensorflow (optional deep learn)│
│ └─ NVIDIA Jetson (hardware)          │ ├─ numpy (numerical ops)           │
│                                      │ ├─ pandas (dataframe operations)   │
│ Fuzzing (MOD-004):                   │ ├─ scipy (statistical analysis)    │
│ ├─ AFL++ (coverage-guided)           │ ├─ matplotlib (visualization)      │
│ ├─ libFuzzer (LLVM-based)            │ └─ seaborn (statistical plots)     │
│ ├─ Radamsa (mutation fuzzer)         │                                      │
│ ├─ GDB (debugger for crashes)        │ Testing & Validation:              │
│ ├─ py-spy (profiling)                │ ├─ pytest (model validation)       │
│ └─ custom harness (target device)    │ ├─ cross-validation (k-fold)       │
│                                      │ ├─ hypothesis (property tests)     │
│ Testing & Analysis:                  │ └─ pytest-benchmark (perf tests)   │
│ ├─ pytest (attack vector tests)      │                                      │
│ ├─ hypothesis (fuzz input gen)       │ Optional ML Tools:                  │
│ └─ docker (isolated fuzzing)         │ ├─ MLflow (experiment tracking)    │
│                                      │ ├─ Weights & Biases (monitoring)   │
│                                      │ └─ Neptune (model registry)        │
└──────────────────────────────────────┴──────────────────────────────────────┘

PHASE 4: INTEGRATION & REPORTING (Weeks 10-12)
┌──────────────────────────────────────┬──────────────────────────────────────┐
│ MOD-007 & MOD-009 Tools              │ MOD-010 Tools                        │
├──────────────────────────────────────┼──────────────────────────────────────┤
│ Report Generation (MOD-007):         │ Documentation (MOD-010):             │
│ ├─ jinja2 (templating engine)        │ ├─ Sphinx (API documentation)       │
│ ├─ reportlab (PDF generation)        │ ├─ MkDocs (alternative docgen)      │
│ ├─ LaTeX (PDF typesetting)           │ ├─ ReadTheDocs (auto-build hosting) │
│ ├─ markdown (text formatting)        │ ├─ Jupyter (interactive notebooks)  │
│ ├─ CVSS calculator (3.1 scoring)     │ ├─ nbconvert (notebook to HTML)     │
│ ├─ NVD API (CVE/CWE lookup)          │ ├─ Pandoc (format conversion)       │
│ ├─ pandas (data aggregation)         │ ├─ LaTeX (technical paper writing) │
│ └─ json (data serialization)         │ ├─ Overleaf (online LaTeX editor)   │
│                                      │ └─ git (version control)            │
│ CLI & Dashboard (MOD-009):           │                                      │
│ ├─ Click (command framework)         │ Publication & Conference:           │
│ ├─ argparse (argument parsing)       │ ├─ GitHub (code repository)        │
│ ├─ Rich (TUI formatting)             │ ├─ PyPI (package distribution)     │
│ ├─ FastAPI (REST API)                │ ├─ arXiv (preprint server)         │
│ ├─ Pydantic (data validation)        │ ├─ GitHub Pages (website)          │
│ ├─ Plotly (interactive charts)       │ ├─ Medium (blog posts)             │
│ ├─ matplotlib (static plots)         │ ├─ OBS Studio (video recording)    │
│ ├─ seaborn (statistical visualization) │ ├─ Asciinema (terminal recording)│
│ └─ uvicorn (ASGI server)             │ └─ YouTube (video hosting)         │
│                                      │                                      │
│ Testing & Validation:                │ Quality Assurance:                  │
│ ├─ pytest (CLI & API tests)          │ ├─ Grammarly (writing check)       │
│ ├─ pytest-cov (coverage tracking)    │ ├─ Citation managers (Zotero)      │
│ ├─ locust (load testing CLI)         │ ├─ APA/IEEE formatters             │
│ └─ selenium (web testing - optional) │ └─ Peer review (academic check)    │
│                                      │                                      │
│ Performance Monitoring:              │ Legal & Compliance:                 │
│ ├─ py-spy (CLI profiling)            │ ├─ CERT/CC (responsible disclosure)│
│ ├─ memory_profiler (memory tracking) │ ├─ CLA (contributor agreement)     │
│ └─ cProfile (standard library)       │ ├─ Code of Conduct (community)     │
│                                      │ └─ LICENSE (MIT/Apache 2.0)        │
└──────────────────────────────────────┴──────────────────────────────────────┘

CROSS-CUTTING: DEVOPS & INFRASTRUCTURE
┌──────────────────────────────────────┬──────────────────────────────────────┐
│ CI/CD Pipeline                       │ Deployment & Operations              │
├──────────────────────────────────────┼──────────────────────────────────────┤
│ • GitHub Actions (CI/CD orchestration)                                      │
│ • Docker (containerization)                                                 │
│ • Docker Compose (local multi-service)                                      │
│ • Trivy (container image scanning)                                          │
│ • OWASP Dependency-Check (vuln scan)                                        │
│ • Bandit (Python security scanning)                                         │
│ • semgrep (code patterns)                                                   │
│ • codecov (coverage tracking)                                               │
│                                                                              │
│ Production Deployment:                                                      │
│ • AWS (cloud infrastructure)                                                │
│ • Terraform (Infrastructure as Code)                                        │
│ • Kubernetes / EKS (container orchestration)                                │
│ • Helm (K8s package management)                                             │
│ • ArgoCD (GitOps deployment)                                                │
│ • kubectl (K8s CLI)                                                         │
│ • Prometheus (metrics collection)                                           │
│ • Grafana (visualization dashboards)                                        │
│ • Loki (log aggregation)                                                    │
│ • Promtail (log shipper)                                                    │
│ • AlertManager (alerting)                                                   │
│ • InfluxDB Cloud (managed time series)                                      │
│ • PostgreSQL + TimescaleDB (database)                                       │
│ • S3 (object storage)                                                       │
│ • CloudWatch (AWS monitoring)                                               │
│ • VPC / Security Groups (networking)                                        │
│ • IAM (access control)                                                      │
│ • Route53 (DNS management)                                                  │
│ • ACM (SSL/TLS certificates)                                                │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

**END OF UML DIAGRAMS**

This document provides comprehensive visualization of:
1. ✅ System architecture overview
2. ✅ Phase-based execution flow with timing
3. ✅ Module dependency graph
4. ✅ Tool allocation to each module
5. ✅ Complete data flow pipeline
6. ✅ CI/CD pipeline workflow
7. ✅ Kubernetes deployment sequence
8. ✅ Detailed phase-wise tool matrix

All diagrams are in **ASCII/Text-based UML format** for easy reading and markdown compatibility.
