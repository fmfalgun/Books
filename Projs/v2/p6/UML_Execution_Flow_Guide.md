# Project 6: UML & Execution Flow Documentation
## Complete Module, Tool, and Execution Diagrams

---

## DOCUMENT OVERVIEW

This document provides detailed UML diagrams and execution flow charts showing:
1. **Phase Execution Flow** - 7-phase timeline with activities, tools, and deliverables
2. **Module Architecture** - 6 core modules with dependencies and data flows
3. **Deployment Architecture** - Dev → Testing → Production infrastructure
4. **Tool-to-Module Mapping** - Which tools are used in which modules
5. **Dependency Graph** - Module dependencies and critical path

---

## 1. PHASE EXECUTION FLOW DIAGRAM

### Overview
The project is divided into 7 sequential phases over 12 weeks, with some phases running in parallel.

```
PHASE TIMELINE:

┌─────────────────┬──────────────────┬────────────────┬──────────────────┐
│  Phase 1: R&D   │  Phase 2: Kerb   │  Phase 3: ETH  │  Phase 4: Fabric │
│  Week 1-2       │  Week 3-4        │  Week 5-6      │  Week 7-8        │
│  (Sequential)   │  (Sequential)    │  (Parallel)    │  (Parallel)      │
└─────────────────┴──────────────────┴────────────────┴──────────────────┘
         ↓               ↓                    ↓                ↓
     Phase 1        Phase 2            Phase 3 & 4          ↓
    Validates       Foundation         Both depend on    Dependency
   Approach         for all            Phase 2 (kerb)    meets here
                    blockchain         starting week 5
                    work
```

### Phase 1: Research & Design (Week 1-2)

| Activity | Duration | Tools | Deliverable | Team |
|----------|----------|-------|-------------|------|
| Literature Review | 3 days | Google Scholar, IEEE Xplore, GitHub | Comparison table (6 systems) | 1 person |
| Architecture Design | 2 days | Draw.io, Lucidchart, pen & paper | Architecture diagram, decision tree | 1 person |
| Blockchain Selection | 2 days | Ethereum docs, Hyperledger docs, comparison | Decision matrix (Eth vs Fabric) | 1 person |
| Threat Modeling | 3 days | STRIDE framework, Threat Dragon tool | Threat model, attack surface map | 1 person |
| **Phase 1 Outcome** | **10 days** | **4 tools** | **Full specification (30-40 pages)** | **1 person** |

**Tools Used:**
```
Input:  RFC 4120, academic papers, vendor documentation
↓
Processing: Draw.io (diagramming), STRIDE (threat modeling)
↓
Output: Design specification, threat model, architectural blueprint
```

**Execution Sequence:**
```
START
  ↓
[Literature Review] (Google Scholar, IEEE Xplore)
  ↓
[Analyze Findings] (comparison table)
  ↓
[Architecture Design] (Draw.io, Lucidchart)
  ↓
[Blockchain Decision] (evaluate trade-offs)
  ↓
[Threat Modeling] (STRIDE, Threat Dragon)
  ↓
[Finalize Specification] (30-40 page document)
  ↓
END (Ready for Phase 2)
```

---

### Phase 2: Traditional Kerberos Implementation (Week 3-4)

| Activity | Duration | Tools | Deliverable | Lines of Code |
|----------|----------|-------|-------------|---------------|
| AS Implementation | 3 days | Python 3.12, cryptography, pyasn1 | authentication_server.py | 500+ |
| TGS Implementation | 3 days | Python 3.12, PyNaCl, redis-py | ticket_granting_server.py | 400+ |
| Client Authenticator | 2 days | Python 3.12, Redis client | client_authenticator.py | 300+ |
| Unit Testing | 3 days | pytest, pytest-cov, hypothesis | 90%+ coverage report | 400+ |
| Performance Profiling | 2 days | memory-profiler, py-spy, cProfile | Latency/throughput report | - |
| **Phase 2 Outcome** | **13 days** | **8 tools** | **~1,200 LOC, <10ms latency** | **1,200** |

**Tools Used:**
```
Input:  RFC 4120 specification, crypto-core module
↓
Processing: 
  ├─ Python 3.12 (language)
  ├─ cryptography + pycryptodome (encryption)
  ├─ pyasn1 (ticket parsing)
  ├─ redis-py (session storage)
  ├─ pytest (testing framework)
  └─ memory-profiler (performance)
↓
Output: Working Kerberos AS/TGS implementation, tested <10ms latency
```

**Execution Sequence:**
```
PHASE 1 COMPLETE
  ↓
[Implement AS Logic] (Python, cryptography)
  ↓
[Unit Test AS] (pytest coverage)
  ↓
[Implement TGS Logic] (Python, pyasn1)
  ↓
[Unit Test TGS] (pytest coverage)
  ↓
[Client Authenticator] (redis-py, session mgmt)
  ↓
[Integration Testing] (end-to-end flow)
  ↓
[Performance Profiling] (memory-profiler, py-spy)
  ↓
[Latency Report] (<10ms confirmed)
  ↓
PHASE 2 COMPLETE (Phase 3 & 4 can start)
```

**Dependencies:**
- **Input:** Phase 1 design specification
- **Output:** kerberos-core module (required for phases 3, 4, 5, 6)
- **Blocks:** Phases 3, 4, 5, 6 (all dependent on this)

---

### Phase 3: Ethereum Blockchain Integration (Week 5-6) [PARALLEL with Phase 4]

| Activity | Duration | Tools | Deliverable | Lines of Code |
|----------|----------|-------|-------------|---------------|
| Smart Contract Design | 2 days | Solidity spec, Remix IDE (design) | Contract architecture doc | - |
| Solidity Implementation | 3 days | Solidity 0.8.19, Foundry, truffle-assertions | AuthenticationVerifier.sol | 200-300 |
| Web3.py Adapter | 3 days | Python 3.12, web3.py, eth-account | ethereum_adapter.py | 400+ |
| Testnet Deployment | 2 days | Foundry (forge deploy), Infura, Sepolia | Live contract on Sepolia | - |
| Gas Optimization | 2 days | Foundry gas-report, solc optimizer | Gas cost <100k per TX | - |
| Integration Testing | 2 days | pytest, web3-testing-library, ganache-cli | End-to-end contract + Python tests | 300+ |
| **Phase 3 Outcome** | **14 days** | **10 tools** | **Contract on testnet, <100k gas, <150ms latency** | **500+ (Sol + Py)** |

**Tools Used:**
```
Input:  Kerberos authenticators from Phase 2, crypto-core module
↓
Processing:
  ├─ Solidity 0.8.19 (smart contract language)
  ├─ Foundry (testing: Forge, local chain: Anvil)
  ├─ Remix IDE (contract development IDE)
  ├─ web3.py (Python interaction with Ethereum)
  ├─ eth-account (account management)
  ├─ eth-keys, eth-utils (Ethereum utilities)
  ├─ Infura (Sepolia testnet RPC)
  ├─ pytest (integration testing)
  └─ ganache-cli (local Ethereum simulation)
↓
Output: Deployed smart contract on Sepolia testnet, tested via Python
```

**Execution Sequence:**
```
PHASE 2 COMPLETE (Kerberos ready)
  ↓
[Design Contract] (Remix IDE, Solidity spec)
  ↓
[Implement Contract] (Solidity 0.8.19, Foundry)
  ↓
[Unit Test Contract] (Foundry test framework)
  ↓
[Implement Web3.py Adapter] (Python, web3.py)
  ↓
[Local Integration Tests] (ganache-cli, pytest)
  ↓
[Deploy to Sepolia] (Foundry forge deploy, Infura)
  ↓
[Gas Optimization] (Foundry gas-report analysis)
  ↓
[Finalize Integration] (pytest validation)
  ↓
PHASE 3 COMPLETE
```

**Dependencies:**
- **Input:** Phase 2 (kerberos-core module)
- **Output:** ethereum-adapter module
- **Can run parallel with:** Phase 4 (both start after Phase 2)
- **Both feed into:** Phase 5 (evaluation)

---

### Phase 4: Hyperledger Fabric Integration (Week 7-8) [PARALLEL with Phase 3]

| Activity | Duration | Tools | Deliverable | Lines of Code |
|----------|----------|-------|-------------|---------------|
| Chaincode Design | 2 days | Go style guide, Fabric chaincode spec | Chaincode architecture doc | - |
| Go Chaincode Impl | 4 days | Go 1.23, fabric-contract-api-go, crypto/sha256 | authentication.go | 500+ |
| Fabric Network Setup | 3 days | Docker Compose, Docker, Fabric binaries | docker-compose.yml, network scripts | 200+ |
| Python SDK Integration | 3 days | Python 3.12, fabric-sdk-py, grpcio | hyperledger_adapter.py | 300+ |
| Testing & Validation | 3 days | pytest, fabric-test-utils, Docker | Integration tests, performance report | 250+ |
| **Phase 4 Outcome** | **15 days** | **9 tools** | **Multi-org Fabric network, 1000+ TPS tested** | **800+ (Go + Py)** |

**Tools Used:**
```
Input:  Kerberos authenticators from Phase 2, crypto-core module
↓
Processing:
  ├─ Go 1.23 (chaincode language)
  ├─ fabric-contract-api-go (Fabric chaincode framework)
  ├─ crypto/sha256 (hashing)
  ├─ fabric-sdk-py (Python client SDK)
  ├─ fabric-sdk-go (Go client library)
  ├─ grpcio (gRPC communication)
  ├─ Docker (containerization)
  ├─ Docker Compose (multi-container orchestration)
  └─ pytest (integration testing)
↓
Output: Running Hyperledger Fabric network with Python/Go integration
```

**Execution Sequence:**
```
PHASE 2 COMPLETE (Kerberos ready)
  ↓
[Design Chaincode] (Go style, Fabric architecture)
  ↓
[Implement Chaincode] (Go 1.23, fabric-contract-api-go)
  ↓
[Unit Test Chaincode] (Go testing, assertions)
  ↓
[Design Network] (Org1, Org2, Orderer, CA)
  ↓
[Create Docker Compose] (Fabric images, config)
  ↓
[Start Network] (docker-compose up)
  ↓
[Implement Python SDK] (fabric-sdk-py, grpcio)
  ↓
[Integration Testing] (pytest, invoke chaincode)
  ↓
[Performance Testing] (concurrent submits, latency)
  ↓
PHASE 4 COMPLETE
```

**Dependencies:**
- **Input:** Phase 2 (kerberos-core module)
- **Output:** hyperledger-adapter module
- **Can run parallel with:** Phase 3 (both start after Phase 2)
- **Both feed into:** Phase 5 (evaluation)

---

### Phase 5: Comparative Evaluation (Week 9)

| Activity | Duration | Tools | Deliverable | Metrics |
|----------|----------|-------|-------------|---------|
| Performance Benchmarking | 3 days | Locust, Prometheus, matplotlib, pandas | Latency/throughput/cost report | 100+ metrics |
| Security Analysis | 2 days | Bandit, custom security scripts | Security report, attack vectors | 20+ threats |
| Optimization Recommendations | 1 day | Python data analysis | Optimization guide | 10+ recommendations |
| **Phase 5 Outcome** | **6 days** | **5 tools** | **Comprehensive comparison document** | **40+ pages** |

**Tools Used:**
```
Input:  Ethereum-adapter (Phase 3) + Hyperledger-adapter (Phase 4)
↓
Processing:
  ├─ Locust (load testing framework, 1000+ concurrent users)
  ├─ Prometheus (metrics collection from systems)
  ├─ matplotlib, seaborn (visualization)
  ├─ pandas (data analysis and comparison)
  ├─ Bandit (security vulnerability scanning)
  └─ custom Python scripts (analysis)
↓
Output: Benchmarks, comparison matrix, security analysis report
```

**Execution Sequence:**
```
PHASE 3 & 4 COMPLETE (both adapters ready)
  ↓
[Prepare Test Scenarios] (1000 users, various operations)
  ↓
[Run Load Tests] (Locust against both systems)
  ↓
[Collect Metrics] (Prometheus scraping both systems)
  ↓
[Analyze Performance] (pandas DataFrames comparison)
  ↓
[Calculate Statistics] (p95, p99 latencies, TPS)
  ↓
[Security Scan] (Bandit on all code)
  ↓
[Generate Visualizations] (matplotlib, graphs)
  ↓
[Write Comparison Report] (40+ pages with tables, charts)
  ↓
[Recommendations] (optimization opportunities)
  ↓
PHASE 5 COMPLETE
```

**Dependencies:**
- **Input:** Both blockchain adapters from Phases 3 & 4
- **Output:** Comprehensive comparison report
- **Feeds into:** Phase 6 (validated configurations)

---

### Phase 6: VANET Simulation & Real-World Testing (Week 10)

| Activity | Duration | Tools | Deliverable | Scenarios |
|----------|----------|-------|-------------|-----------|
| OMNeT++ Setup | 2 days | OMNeT++ 6.0, SUMO 1.15, Veins | Simulation environment | - |
| VANET Scenarios | 3 days | Python scripts, OMNeT++ simulations | Vehicle movement, auth events | 50-500 vehicles |
| Handover Testing | 2 days | SUMO traffic, Veins models | Handover latency analysis | <100ms validation |
| Compliance Report | 1 day | Python pandas, matplotlib | Results analysis, graphs | Pass/fail on SLAs |
| **Phase 6 Outcome** | **8 days** | **5 tools** | **VANET simulation validation** | **Handover <100ms** |

**Tools Used:**
```
Input:  Validated configurations from Phase 5
↓
Processing:
  ├─ OMNeT++ 6.0 (network simulator, C++ based)
  ├─ SUMO 1.15 (traffic simulator)
  ├─ Veins (OMNeT++ + SUMO integration)
  ├─ Python (scenario orchestration)
  └─ matplotlib (results visualization)
↓
Output: VANET simulation results, handover latency validation
```

**Execution Sequence:**
```
PHASE 5 COMPLETE (validated configs ready)
  ↓
[Install OMNeT++] (v6.0 compilation and setup)
  ↓
[Install SUMO] (v1.15 traffic simulator)
  ↓
[Install Veins] (OMNeT++ + SUMO bridge)
  ↓
[Design Road Network] (topology file, RSU placement)
  ↓
[Design Vehicle Scenarios] (50, 100, 200, 500 vehicles)
  ↓
[Simulate Scenarios] (OMNeT++ batch runs)
  ↓
[Record Results] (latency, success rate, packet loss)
  ↓
[Analyze Handover] (vehicle-to-vehicle, vehicle-to-RSU)
  ↓
[Validate SLAs] (<100ms latency requirement)
  ↓
[Generate Report] (graphs, tables, compliance)
  ↓
PHASE 6 COMPLETE
```

**Dependencies:**
- **Input:** Phase 5 evaluation results
- **Output:** VANET simulation validation report
- **Feeds into:** Phase 7 (validation for publication)

---

### Phase 7: Documentation & Publication (Week 11-12)

| Activity | Duration | Tools | Deliverable | Pages |
|----------|----------|-------|-------------|-------|
| README & Guides | 2 days | Markdown, GitHub, VS Code | README.md, SETUP.md, API.md | 50+ |
| Deployment Guides | 2 days | Markdown, Docker, Kubernetes docs | DEPLOYMENT.md, K8S guides | 30+ |
| Research Paper | 5 days | LaTeX (Overleaf), BibTeX, figures | Conference paper (NDSS/CCS format) | 15-20 |
| API Reference | 2 days | Sphinx, mkdocs, Python docstrings | Auto-generated API documentation | 40+ |
| Conference Submission | 3 days | Overleaf, GitHub, email | Submitted paper to NDSS/CCS/S&P | 1 paper |
| **Phase 7 Outcome** | **14 days** | **6 tools** | **Publication-ready documentation** | **135+ pages total** |

**Tools Used:**
```
Input:  All previous phases (1-6) deliverables and results
↓
Processing:
  ├─ Markdown (README, guides, architecture docs)
  ├─ LaTeX + Overleaf (research paper formatting)
  ├─ BibTeX (bibliography management)
  ├─ Sphinx (API documentation generation)
  ├─ GitHub Pages (documentation hosting)
  ├─ Matplotlib/TikZ (figures and graphs)
  └─ GitHub (version control, issue tracking)
↓
Output: Publication-ready documentation, conference submission
```

**Execution Sequence:**
```
PHASE 6 COMPLETE (all validation done)
  ↓
[Write README] (project overview, quick start)
  ↓
[Write Setup Guide] (installation instructions)
  ↓
[Write Deployment Guide] (Docker, K8s, cloud)
  ↓
[Write API Reference] (all module functions)
  ↓
[Start Research Paper] (LaTeX template, Overleaf)
  ↓
[Write Introduction] (motivation, context)
  ↓
[Write Methods Section] (our approach)
  ↓
[Write Results Section] (performance data, graphs)
  ↓
[Write Related Work] (citations, comparison)
  ↓
[Write Conclusion] (impact, future work)
  ↓
[Generate Figures] (architecture diagrams, graphs)
  ↓
[Final Review] (grammar, formatting, citations)
  ↓
[Submit to Conference] (NDSS/CCS/IEEE S&P)
  ↓
PHASE 7 COMPLETE
```

**Dependencies:**
- **Input:** All completed phases (1-6)
- **Output:** Publication-quality documentation and research paper
- **Final milestone:** Conference submission accepted/under review

---

## 2. MODULE ARCHITECTURE & DEPENDENCIES

### Complete Module Dependency Graph

```
┌────────────────────────────────────────────────────────────────┐
│                          CRYPTO-CORE                            │
│  (Foundation Layer - No dependencies)                            │
│  Tools: cryptography, pycryptodome, PyNaCl, OpenSSL            │
│  Functions: AES, RSA, SHA-256, HMAC, ECDSA                     │
│  Deliverable: crypto_core/ (600 LOC)                            │
└────────────────────────────────────────────────────────────────┘
    ↑                    ↑                     ↑                  ↑
    │                    │                     │                  │
    │                    │                     │                  │
┌───┴────────────┐  ┌────┴──────────────┐  ┌──┴──────────────┐   │
│ KERBEROS-CORE  │  │ ETHEREUM-ADAPTER  │  │ HYPERLEDGER-    │   │
│                │  │                    │  │ ADAPTER         │   │
│ Tools:         │  │ Tools:             │  │ Tools:          │   │
│ - Python 3.12  │  │ - web3.py          │  │ - Go 1.23       │   │
│ - cryptography │  │ - Foundry          │  │ - Fabric SDK    │   │
│ - pyasn1       │  │ - Solidity         │  │ - Docker        │   │
│ - redis-py     │  │ - Infura           │  │ - Kubernetes    │   │
│                │  │                    │  │                 │   │
│ Duration: 2 wks│  │ Duration: 2 wks    │  │ Duration: 2 wks │   │
│ LOC: 1200      │  │ LOC: 500 (Sol+Py)  │  │ LOC: 800 (Go+Py)│   │
└───┬────────────┘  └────┬───────────────┘  └──┬────────────┘   │
    │                    │                       │                │
    │  (Parallel)        │  (Parallel)           │                │
    │                    │                       │                │
    └────────┬───────────┴───────────────────────┘                │
             │                                                    │
             ↓                                                    │
        ┌─────────────────────────────────────────┐              │
        │         EVALUATION MODULE                │              │
        │                                          │              │
        │ Tools:                                   │              │
        │ - Locust (load testing)                 │              │
        │ - Prometheus (metrics)                  │              │
        │ - matplotlib, pandas (analysis)         │              │
        │ - Bandit (security)                     │              │
        │                                          │              │
        │ Depends on: ALL THREE above modules     │              │
        │ Duration: 1 week                        │              │
        │ Deliverable: Benchmark report           │              │
        └──────────┬─────────────────────────────┘              │
                   │                                             │
                   ↓                                             │
        ┌─────────────────────────────────────────┐              │
        │      SIMULATION MODULE (VANET)          │              │
        │                                          │              │
        │ Tools:                                   │              │
        │ - OMNeT++ 6.0                           │              │
        │ - SUMO 1.15 (traffic)                   │              │
        │ - Veins (OMNeT+SUMO)                    │              │
        │ - Python (orchestration)                │              │
        │                                          │              │
        │ Depends on: Evaluation (validated cfgs) │              │
        │ Duration: 1 week                        │              │
        │ Deliverable: VANET simulation results   │              │
        └─────────────────────────────────────────┘              │
```

### Critical Path Analysis

```
Critical Path (Blocks overall project):
Phase 1 (R&D) → Phase 2 (Kerberos) → Phases 3&4 (in parallel) 
  → Phase 5 (Evaluation) → Phase 6 (VANET) → Phase 7 (Docs)

Total Critical Path Duration: 12 weeks

Non-blocking activities:
- Phase 3 and 4 can run simultaneously (both depend only on Phase 2)
- Phase 1 must complete before Phase 2
- Phase 2 must complete before Phases 3 and 4 start
- Phases 3 and 4 must both complete before Phase 5
- Phase 5 must complete before Phase 6
- Phase 6 must complete before Phase 7
```

---

## 3. TOOL-TO-MODULE MAPPING MATRIX

### Master Tool Usage Chart

| Tool | Module | Phase | Purpose | Version | Installation |
|------|--------|-------|---------|---------|--------------|
| **Python 3.12** | All | All | Primary language | 3.12+ | `apt install python3.12` |
| **cryptography** | crypto-core | 2 | AES, RSA, SHA-256 | 46.0.0+ | `pip install cryptography` |
| **pycryptodome** | crypto-core | 2 | HKDF, ChaCha20 | 3.23.0+ | `pip install pycryptodome` |
| **PyNaCl** | crypto-core | 2 | Ed25519 signatures | 1.6.1+ | `pip install PyNaCl` |
| **pyasn1** | kerberos-core | 2 | ASN.1 parsing | 0.4.8+ | `pip install pyasn1` |
| **redis-py** | kerberos-core | 2 | Session storage | 5.0.0+ | `pip install redis` |
| **pytest** | evaluation | 5 | Unit testing | 8.0.0+ | `pip install pytest` |
| **hypothesis** | evaluation | 5 | Property testing | 6.100.0+ | `pip install hypothesis` |
| **web3.py** | ethereum-adapter | 3 | Ethereum JSON-RPC | 7.0.0+ | `pip install web3.py` |
| **eth-account** | ethereum-adapter | 3 | Account management | 0.13.0+ | `pip install eth-account` |
| **Foundry** | ethereum-adapter | 3 | Smart contract dev | Latest | `curl -L https://foundry.paradigm.xyz \| bash` |
| **Solidity** | ethereum-adapter | 3 | Smart contracts | 0.8.19+ | Installed via Foundry |
| **fabric-sdk-py** | hyperledger-adapter | 4 | Fabric client | 0.8.1+ | `pip install fabric-sdk-py` |
| **Go 1.23** | hyperledger-adapter | 4 | Chaincode language | 1.23+ | `wget go.dev/dl/go1.23.linux-amd64.tar.gz` |
| **fabric-contract-api-go** | hyperledger-adapter | 4 | Fabric chaincode API | 2.5.0+ | `go get github.com/hyperledger/fabric-contract-api-go/v2` |
| **Docker** | All | All | Containerization | 27.0+ | `curl https://get.docker.com \| bash` |
| **Docker Compose** | hyperledger-adapter | 4 | Multi-container orch | Latest | Included with Docker |
| **Kubernetes** | hyperledger-adapter | 4 | Production orch | 1.28+ | `apt install kubectl` |
| **Prometheus** | evaluation | 5 | Metrics collection | Latest | `docker run -d prom/prometheus` |
| **Grafana** | evaluation | 5 | Metrics visualization | Latest | `docker run -d grafana/grafana` |
| **Locust** | evaluation | 5 | Load testing | 2.20.0+ | `pip install locust` |
| **Bandit** | evaluation | 5 | Security scanning | Latest | `pip install bandit` |
| **OMNeT++** | simulation | 6 | Network simulator | 6.0+ | Download from omnetpp.org |
| **SUMO** | simulation | 6 | Traffic simulator | 1.15+ | `apt install sumo` |
| **matplotlib** | evaluation | 5 | Visualization | 3.9.0+ | `pip install matplotlib` |
| **pandas** | evaluation | 5 | Data analysis | 2.2.0+ | `pip install pandas` |
| **LaTeX** | documentation | 7 | Paper writing | TexLive 2024 | `apt install texlive-full` |
| **Overleaf** | documentation | 7 | Online LaTeX editor | Web | overleaf.com |
| **GitHub Actions** | CI/CD | All | CI/CD pipeline | Native | Enabled in GitHub |
| **GitHub** | All | All | Version control | Web | github.com |

---

## 4. DATA FLOW BETWEEN MODULES

### Module Interaction Sequences

#### Sequence 1: Authentication Request Flow

```
Client
  │
  ├─→ kerberos-core.authenticate()
  │   │
  │   ├─→ crypto-core.verify_password() [crypto-core needed]
  │   │
  │   ├─→ crypto-core.generate_session_key() [crypto-core needed]
  │   │
  │   └─→ Redis.store(session) [Session persistence]
  │
  └─→ Response: TGT + Session Key
     │
     └─→ ethereum-adapter.submit_authenticator(TGT hash) [Optional]
         │
         ├─→ web3.py submits to Ethereum smart contract
         │
         └─→ blockchain_verification.create_proof()
```

#### Sequence 2: Service Ticket Request Flow

```
Client (with TGT)
  │
  ├─→ kerberos-core.request_service_ticket(TGT)
  │   │
  │   ├─→ crypto-core.decrypt(TGT) [crypto-core needed]
  │   │
  │   ├─→ crypto-core.validate_ticket() [crypto-core needed]
  │   │
  │   └─→ crypto-core.generate_service_key() [crypto-core needed]
  │
  └─→ Response: Service Ticket
     │
     ├─→ ethereum-adapter.submit_authenticator() [Optional]
     │
     └─→ hyperledger-adapter.submit_authenticator() [Optional]
         │
         └─→ Fabric chaincode.SubmitAuthenticator()
```

#### Sequence 3: Evaluation & Benchmarking Flow

```
evaluation module
  │
  ├─→ Locust generates 1000 concurrent users
  │   │
  │   ├─→ 500 users hit kerberos-core API
  │   │   └─→ Metrics: latency, throughput, errors
  │   │
  │   ├─→ 300 users hit ethereum-adapter API
  │   │   └─→ Metrics: gas cost, blockchain latency
  │   │
  │   └─→ 200 users hit hyperledger-adapter API
  │       └─→ Metrics: TPS, finality time
  │
  ├─→ Prometheus collects metrics from all
  │
  ├─→ pandas aggregates results
  │
  ├─→ matplotlib generates graphs
  │
  └─→ Output: Benchmark report with tables & charts
```

---

## 5. EXECUTION ENVIRONMENT MATRIX

### Where Each Tool Runs

| Tool | Development | Testing (CI/CD) | Production |
|------|-------------|-----------------|------------|
| Python 3.12 | Local machine | GitHub runner | Kubernetes pod |
| cryptography | venv | GitHub runner | Kubernetes pod |
| Redis | Docker Compose | Service in Actions | AWS ElastiCache |
| PostgreSQL | Docker Compose | Service in Actions | AWS RDS |
| Docker | Local | GitHub runner | Container runtime |
| Kubernetes | Minikube (optional) | Build artifact | Production cluster |
| pytest | Local + push | GitHub Actions | Not in prod |
| Prometheus | Docker Compose | Not used | AWS EC2 instance |
| Grafana | Docker Compose | Not used | AWS EC2 instance |
| web3.py | Local (testnet) | Local (testnet) | Infura (mainnet) |
| Foundry | Local | Not used | Not used (post-deploy) |
| Hyperledger | Docker Compose | Not used | Kubernetes cluster |
| OMNeT++ | Local machine | Not used | Not used |
| Overleaf | Web browser | Not used | Not used |

---

## 6. DETAILED EXECUTION TIMELINE

### Week-by-Week Breakdown

**Week 1-2: Phase 1 (Research & Design)**
```
Monday Week 1:
  ├─ Morning: Set up workspace, GitHub repo, documentation
  ├─ Afternoon: Start literature review (Google Scholar, IEEE)
  └─ Tools: Google Scholar, GitHub, draw.io

Tuesday-Wednesday Week 1:
  ├─ Morning: Complete literature review (6 authentication systems)
  ├─ Afternoon: Analysis and comparison table
  └─ Tools: Spreadsheet, github markdown

Thursday-Friday Week 1:
  ├─ Morning: Architecture design (Draw.io)
  ├─ Afternoon: Create diagrams, decision trees
  └─ Tools: Draw.io, lucidchart

Monday-Tuesday Week 2:
  ├─ Morning: Blockchain selection decision
  ├─ Decision: Both Ethereum + Hyperledger (for comparison)
  └─ Tools: Decision matrix, comparison spreadsheet

Wednesday Week 2:
  ├─ Morning: STRIDE threat modeling session
  ├─ Afternoon: Document threats, attack vectors
  └─ Tools: Threat Dragon, STRIDE templates

Thursday-Friday Week 2:
  ├─ Morning: Finalize specification (30-40 pages)
  ├─ Afternoon: Review and sign-off
  └─ Output: Complete specification document
```

**Week 3-4: Phase 2 (Kerberos Core Implementation)**
```
Monday Week 3:
  ├─ Morning: Set up Python venv, install dependencies
  ├─ Afternoon: Begin AS (Authentication Server) implementation
  └─ Tools: Python 3.12, cryptography, VS Code

Tuesday-Wednesday Week 3:
  ├─ All day: Implement AS logic (key generation, ticket creation)
  ├─ End of day: Unit tests for AS
  └─ Tools: pytest, pytest-cov, hypothesis

Thursday-Friday Week 3:
  ├─ Morning: Implement TGS (Ticket Granting Server)
  ├─ Afternoon: Unit tests for TGS
  └─ Tools: pytest, pyasn1 for ASN.1 parsing

Monday Week 4:
  ├─ Morning: Implement client authenticator
  ├─ Afternoon: Redis integration for session storage
  └─ Tools: redis-py, redis-cli

Tuesday Week 4:
  ├─ All day: Integration testing (end-to-end flows)
  └─ Tools: pytest, paramiko for remote testing

Wednesday Week 4:
  ├─ Morning: Performance profiling
  ├─ Afternoon: Memory and CPU analysis
  └─ Tools: memory-profiler, py-spy, cProfile

Thursday-Friday Week 4:
  ├─ Morning: Optimize for latency (target: <10ms)
  ├─ Afternoon: Document results, prepare for Phase 3 & 4
  └─ Output: kerberos-core module (1200 LOC, <10ms latency)
```

**Week 5-6: Phase 3 (Ethereum) + Week 7-8: Phase 4 (Hyperledger) [PARALLEL]**

*These run simultaneously. Both depend only on Phase 2 completion.*

**Phase 3: Ethereum (Week 5-6)**
```
Monday Week 5:
  ├─ Morning: Design smart contract in Remix IDE
  ├─ Afternoon: Set up Foundry environment
  └─ Tools: Remix IDE, Foundry, Solidity

Tuesday-Wednesday Week 5:
  ├─ All day: Implement Solidity contract
  ├─ End: Forge compile and unit tests
  └─ Tools: Foundry forge, solc compiler

Thursday Week 5:
  ├─ Morning: Implement Web3.py adapter
  ├─ Afternoon: Local testing with Ganache/Anvil
  └─ Tools: web3.py, Anvil (Foundry)

Friday Week 5:
  ├─ All day: Integration testing (contract + Python)
  └─ Tools: pytest, web3-testing-library

Monday Week 6:
  ├─ Morning: Deploy to Sepolia testnet
  ├─ Afternoon: Verify contract on Etherscan
  └─ Tools: Foundry forge deploy, Infura

Tuesday-Wednesday Week 6:
  ├─ All day: Gas optimization analysis
  ├─ Target: <100k gas per transaction
  └─ Tools: Foundry gas-report, solc optimizer

Thursday-Friday Week 6:
  ├─ Morning: Final integration tests
  ├─ Afternoon: Documentation
  └─ Output: ethereum-adapter (500 LOC, live on Sepolia)
```

**Phase 4: Hyperledger Fabric (Week 7-8)**
```
Monday Week 7:
  ├─ Morning: Design chaincode architecture
  ├─ Afternoon: Set up Go environment
  └─ Tools: Go 1.23, VSCode, fabric documentation

Tuesday-Wednesday Week 7:
  ├─ All day: Implement Fabric chaincode in Go
  ├─ End: Go build and unit tests
  └─ Tools: Go 1.23, fabric-contract-api-go, testing

Thursday Week 7:
  ├─ Morning: Create Docker Compose for Fabric network
  ├─ Afternoon: Define org structure (Org1, Org2, Orderer, CA)
  └─ Tools: Docker Compose, Fabric binaries

Friday Week 7:
  ├─ All day: Bring up multi-org Fabric network
  └─ Tools: docker-compose, Fabric commands

Monday Week 8:
  ├─ Morning: Implement Python SDK integration
  ├─ Afternoon: Connect to Fabric network
  └─ Tools: fabric-sdk-py, grpcio

Tuesday-Wednesday Week 8:
  ├─ All day: Integration testing (chaincode invocation)
  ├─ Target: >1000 TPS
  └─ Tools: pytest, fabric-test-utils

Thursday-Friday Week 8:
  ├─ Morning: Performance testing and optimization
  ├─ Afternoon: Documentation
  └─ Output: hyperledger-adapter (800 LOC, >1000 TPS)
```

**Week 9: Phase 5 (Evaluation)**
```
Monday-Tuesday Week 9:
  ├─ All day: Prepare load testing scenarios
  ├─ Locust scripts for both systems
  └─ Tools: Locust, Python

Wednesday Week 9:
  ├─ Morning: Run load tests against Ethereum adapter
  ├─ Afternoon: Run load tests against Hyperledger adapter
  └─ Tools: Locust, Prometheus, matplotlib

Thursday Week 9:
  ├─ Morning: Collect and analyze metrics
  ├─ Afternoon: Generate comparison charts
  └─ Tools: Prometheus, pandas, matplotlib

Friday Week 9:
  ├─ Morning: Security analysis (Bandit + custom)
  ├─ Afternoon: Write comprehensive report
  └─ Output: 40-page evaluation report with benchmarks
```

**Week 10: Phase 6 (VANET Simulation)**
```
Monday Week 10:
  ├─ Morning: Install OMNeT++ and SUMO
  ├─ Afternoon: Configure Veins integration
  └─ Tools: OMNeT++, SUMO, Veins

Tuesday Week 10:
  ├─ All day: Design and simulate VANET scenarios
  ├─ 50, 100, 200, 500 vehicles
  └─ Tools: OMNeT++, Python simulation orchestration

Wednesday Week 10:
  ├─ Morning: Run handover scenarios
  ├─ Afternoon: Collect latency data
  └─ Tools: SUMO, OMNeT++ logging

Thursday-Friday Week 10:
  ├─ Morning: Analyze results and validate SLAs
  ├─ Afternoon: Generate visualization and report
  └─ Output: VANET validation report, <100ms confirmed
```

**Week 11-12: Phase 7 (Documentation & Publication)**
```
Monday Week 11:
  ├─ Morning: Write README.md
  ├─ Afternoon: Write SETUP.md
  └─ Tools: Markdown, GitHub

Tuesday Week 11:
  ├─ Morning: Write DEPLOYMENT.md (Docker, K8s, cloud)
  ├─ Afternoon: Write API reference
  └─ Tools: Sphinx, mkdocs

Wednesday Week 11:
  ├─ All day: Begin research paper in Overleaf
  ├─ Structure: Intro, Methods, Results, Related Work, Conclusion
  └─ Tools: LaTeX, Overleaf, BibTeX

Thursday-Friday Week 11:
  ├─ All day: Write paper sections and create figures
  └─ Tools: LaTeX, TikZ, matplotlib

Monday-Tuesday Week 12:
  ├─ All day: Refine paper, citations, formatting
  └─ Tools: Overleaf, BibTeX

Wednesday Week 12:
  ├─ Morning: Final paper review
  ├─ Afternoon: Prepare submission (PDF + cover letter)
  └─ Tools: Overleaf

Thursday Week 12:
  ├─ Morning: Submit to conference (NDSS/CCS/IEEE S&P)
  ├─ Afternoon: Update GitHub with all documentation
  └─ Output: Conference submission, all docs live on GitHub

Friday Week 12:
  ├─ All day: Celebration and planning for next phase!
  └─ Output: Complete project delivery ✓
```

---

## 7. DEPENDENCY CRITICAL PATH

### Blocking Dependencies

```
PHASE 1 BLOCKING:
└─ All other phases blocked until Phase 1 complete (10 days)

PHASE 2 BLOCKING:
├─ Phase 3 (Ethereum) blocked on Phase 2 (day 12/85)
├─ Phase 4 (Hyperledger) blocked on Phase 2 (day 12/85)
├─ Phase 5 (Evaluation) blocked on Phases 3 & 4 (day 40/85)
├─ Phase 6 (VANET) blocked on Phase 5 (day 54/85)
└─ Phase 7 (Docs) blocked on Phase 6 (day 62/85)

PHASE 3 & 4 PARALLEL (No blocking):
├─ Both can run simultaneously after Phase 2
├─ Neither depends on the other
└─ Both are required for Phase 5

PHASE 5 BLOCKING:
└─ Phase 6 blocked on Phase 5 completion (day 54/85)

PHASE 6 BLOCKING:
└─ Phase 7 blocked on Phase 6 completion (day 62/85)
```

### Time-Boxed Activities (Can parallelize within phases)

```
Within Phase 2 (Kerberos):
├─ AS implementation: 3 days (1 person)
├─ TGS implementation: 3 days (can start after AS unit tests)
├─ Client authenticator: 2 days (can start after TGS)
└─ Testing & profiling: 3 days (final step)

Within Phase 3 & 4:
├─ Phase 3 activities: 14 days (can parallelize contract dev + testing)
└─ Phase 4 activities: 15 days (chaincode + network setup parallel)

Within Phase 5 (Evaluation):
├─ Load test execution: 2 days (both can run simultaneously)
├─ Analysis: 2 days
└─ Reporting: 2 days

Within Phase 7 (Documentation):
├─ README/guides: 2 days (parallel with paper)
└─ Paper: 5 days (parallel with guides)
```

---

**Document Version:** 1.0  
**Last Updated:** December 16, 2025  
**Total Pages:** 25+  
**Diagrams:** 3 main UML diagrams + 15+ execution flowcharts
