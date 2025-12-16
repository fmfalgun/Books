# Project 7: UML Execution Flow & Tool Integration Architecture
## Complete Module & Phase Dependency Mapping

---

## TABLE OF CONTENTS
1. Component Diagram Overview
2. Phase-by-Phase Execution Flow
3. Module Dependency Graph
4. Tool-to-Module Mapping Matrix
5. Data Flow Specifications
6. Sequence Diagrams
7. Deployment Architecture

---

## 1. COMPONENT DIAGRAM OVERVIEW

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │                    ORCHESTRATOR ENGINE                          │  │
│  │  (Main Entry Point: orchestrator.py)                            │  │
│  │                                                                 │  │
│  │  Dependencies: asyncio, boto3, aioboto3, Click, Pydantic       │  │
│  │  Responsibilities:                                              │  │
│  │    - Parse attack scenarios (YAML)                             │  │
│  │    - Validate preconditions                                    │  │
│  │    - Load & initialize modules                                 │  │
│  │    - Coordinate execution (parallel/sequential)                │  │
│  │    - Aggregate findings                                        │  │
│  │    - Trigger reporting                                         │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│           ↓           ↓           ↓           ↓           ↓           │
│    ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ │
│    │  CORE    │ │  RECON   │ │ EXPLOIT  │ │  POST-   │ │ EVASION  │ │
│    │ MODULES  │ │ MODULES  │ │ MODULES  │ │ EXPLOIT  │ │ MODULES  │ │
│    │  (Layer) │ │  (Layer) │ │  (Layer) │ │  (Layer) │ │  (Layer) │ │
│    └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘ │
│                                                                       │
│  ┌─────────────────────────────────────────────────────────────────┐ │
│  │           INFRASTRUCTURE LAYER (Persistent Storage)             │ │
│  │                                                                 │ │
│  │  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐   │ │
│  │  │ PostgreSQL 15  │  │  Redis Cache   │  │  S3 Buckets    │   │ │
│  │  │  (Findings DB) │  │  (State/Cache) │  │ (Reports/Logs) │   │ │
│  │  └────────────────┘  └────────────────┘  └────────────────┘   │ │
│  │                                                                 │ │
│  │  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐   │ │
│  │  │  CloudWatch    │  │ Secrets Manager│  │ Security Hub   │   │ │
│  │  │  (Logs/Metrics)│  │ (Credentials)  │  │ (Findings Sync)│   │ │
│  │  └────────────────┘  └────────────────┘  └────────────────┘   │ │
│  └─────────────────────────────────────────────────────────────────┘ │
│                                                                       │
│  ┌─────────────────────────────────────────────────────────────────┐ │
│  │             CI/CD & DEPLOYMENT PIPELINE                         │ │
│  │                                                                 │ │
│  │  GitHub Actions → Docker Build → ECR Push → ECS Deploy        │ │
│  └─────────────────────────────────────────────────────────────────┘ │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 2. PHASE-BY-PHASE EXECUTION FLOW

### PHASE 1: FOUNDATION (Weeks 1-2)

```
START
  ↓
┌─────────────────────────────────────────┐
│ 1.1: Environment Setup                  │
│ Duration: 2-3 days                      │
│ Tools: Docker, Python 3.11, Poetry      │
│ Output: .venv + Dockerfile + Compose    │
└─────────────────────────────────────────┘
  ↓
┌─────────────────────────────────────────┐
│ 1.2: AWS Test Infrastructure            │
│ Duration: 3-4 days                      │
│ Tools: CloudFormation, AWS CLI          │
│ Output: Test AWS account ready          │
└─────────────────────────────────────────┘
  ↓
┌─────────────────────────────────────────┐
│ 1.3: MITRE ATT&CK Mapping               │
│ Duration: 2-3 days                      │
│ Tools: MITRE Framework, Python, YAML    │
│ Output: mitre_mapping.yaml              │
└─────────────────────────────────────────┘
  ↓
┌─────────────────────────────────────────┐
│ 1.4: Threat Model Definition            │
│ Duration: 1-2 days                      │
│ Tools: Documentation, config.yaml       │
│ Output: Scope & constraint document     │
└─────────────────────────────────────────┘
  ↓
[PHASE 1 COMPLETE] → PostgreSQL + Redis ready
```

### PHASE 2: CORE FRAMEWORK (Weeks 2-4)

```
[PHASE 1 COMPLETE]
  ↓
┌─────────────────────────────────────────────────────────┐
│ 2.1: Orchestration Engine                              │
│ Duration: 5-7 days                                     │
│ Core Module: orchestrator.py                           │
│ Dependencies:                                          │
│   - asyncio (Python built-in)                          │
│   - Click (CLI framework)                              │
│   - Pydantic (validation)                              │
│   - loguru (structured logging)                        │
│ Responsibilities:                                      │
│   • Load attack scenarios (YAML)                       │
│   • Initialize modules dynamically                     │
│   • Coordinate async/sync execution                    │
│   • Error handling & retry logic                       │
│ Output: orchestrator.py + tests/test_orchestrator.py   │
└─────────────────────────────────────────────────────────┘
  ↓
┌─────────────────────────────────────────────────────────┐
│ 2.2: Logging & Telemetry System                         │
│ Duration: 3-4 days                                     │
│ Core Module: logging_system.py                         │
│ Dependencies:                                          │
│   - loguru (JSON-structured logging)                   │
│   - watchtower (CloudWatch integration)                │
│   - python-json-logger                                 │
│ Output Destinations:                                   │
│   → CloudWatch Logs (production)                       │
│   → Local file (development)                           │
│   → JSON format (machine-readable)                     │
│ Output: logging_system.py + CloudWatch log groups      │
└─────────────────────────────────────────────────────────┘
  ↓
┌─────────────────────────────────────────────────────────┐
│ 2.3: Credential Management                             │
│ Duration: 4-5 days                                     │
│ Core Module: credential_manager.py                     │
│ Dependencies:                                          │
│   - boto3 STS (temporary tokens)                       │
│   - cryptography (encryption)                          │
│   - AWS Secrets Manager (credential storage)           │
│   - python-dotenv (local dev)                          │
│ Features:                                              │
│   • Load AWS credentials (profile/env)                 │
│   • Validate IAM permissions                           │
│   • Request STS tokens (time-limited)                  │
│   • Automatic credential rotation                      │
│   • Secure cleanup on exit                             │
│ Output: credential_manager.py + AWS IAM policies       │
└─────────────────────────────────────────────────────────┘
  ↓
┌─────────────────────────────────────────────────────────┐
│ 2.4: Report Generation Engine                          │
│ Duration: 3-4 days                                     │
│ Core Module: reporting_module.py                       │
│ Dependencies:                                          │
│   - Jinja2 (HTML templates)                            │
│   - matplotlib (charts)                                │
│   - fpdf2 (PDF generation)                             │
│   - openpyxl (Excel export)                            │
│   - pandas (data aggregation)                          │
│ Output Formats:                                        │
│   → HTML (interactive dashboard)                       │
│   → PDF (executive summary)                            │
│   → JSON (machine-readable)                            │
│   → CSV (spreadsheet import)                           │
│ Output: reporting_module.py + report templates         │
└─────────────────────────────────────────────────────────┘
  ↓
[PHASE 2 COMPLETE] → Core framework ready, DB connected
```

### PHASE 3: RECONNAISSANCE (Weeks 4-6)

```
[PHASE 2 COMPLETE]
  ↓
┌──────────────────────────────────────────────────────┐
│ 3.1: AWS Account Enumeration                         │
│ Duration: 4-5 days                                  │
│ Module: aws_enum_module.py                          │
│ Dependencies:                                       │
│   - boto3 (EC2, S3, Lambda, RDS, etc.)             │
│   - aioboto3 (async concurrent calls)              │
│   - asyncio (parallel region scanning)             │
│ Data Sources:                                       │
│   • describe_regions()                              │
│   • describe_instances() / list_buckets()           │
│   • get_user_account_summary()                      │
│ AWS Services Queried:                               │
│   ↓ EC2 (regions, instances, volumes)               │
│   ↓ S3 (buckets, object counts)                     │
│   ↓ Lambda (functions, memory, runtime)             │
│   ↓ RDS (DB instances, snapshots)                   │
│   ↓ IAM (account info)                              │
│ Output Storage:                                     │
│   → PostgreSQL findings table (resource catalog)    │
│   → Redis cache (hot data)                          │
│ Performance: 14 regions × async = ~10-15 seconds    │
│ Output: aws_enum_module.py + resource graph DB      │
└──────────────────────────────────────────────────────┘
  ↓
┌──────────────────────────────────────────────────────┐
│ 3.2: IAM Enumeration & Analysis                     │
│ Duration: 4-5 days                                  │
│ Module: iam_enum_module.py                          │
│ Dependencies:                                       │
│   - boto3 IAM client                                │
│   - policy analysis (custom logic)                  │
│   - networkx (privilege escalation graph)           │
│ Data Extraction:                                    │
│   • list_users() / list_roles()                     │
│   • get_user_policy() / get_role_policy()           │
│   • list_attached_user_policies()                   │
│   • get_assume_role_policy_document()               │
│ Analysis:                                           │
│   ↓ Build trust relationship graph                  │
│   ↓ Identify privilege escalation paths             │
│   ↓ Find permission boundaries                      │
│   ↓ Detect inline vs managed policies               │
│ Output Storage:                                     │
│   → PostgreSQL IAM findings table                   │
│   → Escalation chains JSON                          │
│ MITRE Mapping: T1087 (Account Discovery)            │
│ Output: iam_enum_module.py + privilege paths DB     │
└──────────────────────────────────────────────────────┘
  ↓
┌──────────────────────────────────────────────────────┐
│ 3.3: Network Mapping                                │
│ Duration: 3-4 days                                  │
│ Module: network_enum_module.py                      │
│ Dependencies:                                       │
│   - boto3 EC2 client                                │
│   - nmap (advanced port scanning)                   │
│   - NetworkX (topology graph)                       │
│ Reconnaissance Targets:                             │
│   • VPCs (CIDR ranges, DNS settings)                │
│   • Subnets (public/private, route tables)          │
│   • Security Groups (ingress/egress rules)          │
│   • NACLs (stateless filtering)                     │
│   • ENIs (Elastic Network Interfaces)               │
│ Port Scanning (nmap integration):                   │
│   $ nmap -sV -p- <EC2_PUBLIC_IP>                    │
│ Output Storage:                                     │
│   → PostgreSQL network topology table               │
│   → S3 network diagrams                             │
│ Performance: Parallel scanning per subnet           │
│ Output: network_enum_module.py + network DB         │
└──────────────────────────────────────────────────────┘
  ↓
┌──────────────────────────────────────────────────────┐
│ 3.4: Service Discovery                              │
│ Duration: 4-5 days                                  │
│ Module: service_enum_module.py                      │
│ Dependencies:                                       │
│   - boto3 service clients                           │
│   - aioboto3 (async enumeration)                    │
│   - json/yaml parsing                               │
│ Services Enumerated:                                │
│   ↓ Lambda (functions, layers, env vars)            │
│   ↓ API Gateway (APIs, stages, auth)                │
│   ↓ ECS (clusters, services, tasks)                 │
│   ↓ DynamoDB (tables, GSIs, streams)                │
│   ↓ Secrets Manager (secrets, rotations)            │
│   ↓ Systems Manager (parameters, documents)         │
│   ↓ CloudFormation (stacks, resources)              │
│ Sensitive Data Extraction:                          │
│   • Lambda environment variables                    │
│   • Parameter Store values                          │
│   • Secrets Manager metadata                        │
│ Output Storage:                                     │
│   → PostgreSQL service catalog                      │
│   → S3 enumeration reports                          │
│ Output: service_enum_module.py + service DB         │
└──────────────────────────────────────────────────────┘
  ↓
[PHASE 3 COMPLETE] → Complete infrastructure map ready
```

### PHASE 4: EXPLOITATION (Weeks 6-10)

```
[PHASE 3 COMPLETE]
  ↓
┌──────────────────────────────────────────────────────┐
│ 4.1: IAM Privilege Escalation                       │
│ Duration: 6-7 days                                  │
│ Module: iam_privesc_module.py                       │
│ Dependencies:                                       │
│   - boto3 IAM client                                │
│   - PACU exploitation modules (integrated)          │
│   - Custom escalation logic                         │
│ Escalation Vectors Tested:                          │
│   • CreateAccessKey (current user)                  │
│   • CreateUser (new account)                        │
│   • AttachUserPolicy (permission grant)             │
│   • PutUserPolicy (inline policy)                   │
│   • AssumeRole (cross-account/role)                 │
│   • UpdateAssumeRolePolicy (trust manipulation)     │
│   • PassRole (service-linked role bypass)           │
│   • CreateLoginProfile (console access)             │
│ Attack Flow:                                        │
│   1. Enumerate current user permissions             │
│   2. Identify gaps (permissions NOT granted)        │
│   3. Test CreateUser → AttachPolicy path            │
│   4. If blocked, test AssumeRole chain              │
│   5. Verify admin/root access                       │
│ Output Storage:                                     │
│   → PostgreSQL privilege escalation findings        │
│   → Escalation proof-of-concept commands            │
│ MITRE Mapping: T1087, T1136, T1134                  │
│ Output: iam_privesc_module.py + escalation PoCs     │
└──────────────────────────────────────────────────────┘
  ↓
┌──────────────────────────────────────────────────────┐
│ 4.2: EC2 Exploitation Chain                         │
│ Duration: 5-6 days                                  │
│ Module: ec2_exploit_module.py                       │
│ Dependencies:                                       │
│   - boto3 EC2 client                                │
│   - nmap (port scanning)                            │
│   - paramiko (SSH client)                           │
│   - pywinrm (RDP/WinRM)                             │
│   - pwntools (payload generation)                   │
│ Attack Stages:                                      │
│   Stage 1: Security Group Analysis                  │
│     • Enumerate ingress rules                       │
│     • Identify open ports (22, 3389, 80, 443)       │
│                                                     │
│   Stage 2: Port Scanning                            │
│     $ masscan -p1-65535 <IP_RANGE>                  │
│                                                     │
│   Stage 3: Service Enumeration                      │
│     $ nmap -sV -p 22,3389,80,443 <IP>               │
│                                                     │
│   Stage 4: Access Attempt                           │
│     → SSH (paramiko): Key-based, password-based    │
│     → RDP (pywinrm): WinRM remote execution         │
│     → HTTP (requests): web service exploitation    │
│                                                     │
│   Stage 5: RCE Payload Delivery                     │
│     → Shell commands via SSH/RDP                    │
│     → Reverse shell (netcat, PowerShell)            │
│                                                     │
│   Stage 6: Credential Extraction                    │
│     → /etc/passwd, /etc/shadow (Linux)              │
│     → SAM registry, LSASS dump (Windows)            │
│     → SSH keys, AWS config files                    │
│                                                     │
│   Stage 7: Lateral Movement                         │
│     → Pivot to other instances via VPC              │
│     → Use extracted credentials                     │
│                                                     │
│ Output Storage:                                     │
│   → PostgreSQL EC2 compromise findings              │
│   → S3 shell command outputs                        │
│   → Extracted credentials (encrypted)               │
│ MITRE Mapping: T1021, T1059, T1555                  │
│ Output: ec2_exploit_module.py + compromise PoCs     │
└──────────────────────────────────────────────────────┘
  ↓
┌──────────────────────────────────────────────────────┐
│ 4.3: S3 Exploitation                                │
│ Duration: 5-6 days                                  │
│ Module: s3_exploit_module.py                        │
│ Dependencies:                                       │
│   - boto3 S3 client                                 │
│   - aioboto3 (async object listing)                 │
│   - s3fs (large file operations)                    │
│ Attack Stages:                                      │
│   Stage 1: Bucket Enumeration                       │
│     • list_buckets()                                │
│     • get_bucket_acl()                              │
│     • get_bucket_policy()                           │
│                                                     │
│   Stage 2: Permission Testing                       │
│     • get_object() - test read access               │
│     • put_object() - test write access              │
│     • delete_object() - test delete access          │
│                                                     │
│   Stage 3: Object Listing (async)                   │
│     • list_objects_v2() with pagination             │
│     • Parallel prefix scanning                      │
│     • Size calculation for impact                   │
│                                                     │
│   Stage 4: Sensitive Data Detection                 │
│     • Pattern matching (AWS keys, DB creds)         │
│     • File extension analysis (.pem, .sql, .json)   │
│     • Content analysis (base64 secrets)             │
│                                                     │
│   Stage 5: Data Exfiltration                        │
│     • Download sensitive objects                    │
│     • Create tar.gz of findings                     │
│     • Upload to exfil bucket (in test env)          │
│                                                     │
│ Output Storage:                                     │
│   → PostgreSQL S3 finding table                     │
│   → S3 exfil bucket (simulation)                    │
│   → Evidence files (encrypted)                      │
│ MITRE Mapping: T1526, T1619                         │
│ Output: s3_exploit_module.py + bucket analysis      │
└──────────────────────────────────────────────────────┘
  ↓
┌──────────────────────────────────────────────────────┐
│ 4.4: Lambda/Serverless Exploitation                 │
│ Duration: 6-7 days                                  │
│ Module: lambda_exploit_module.py                    │
│ Dependencies:                                       │
│   - boto3 Lambda client                             │
│   - aioboto3 (async enumeration)                    │
│   - zipfile (code injection)                        │
│ Attack Stages:                                      │
│   Stage 1: Function Enumeration                     │
│     • list_functions()                              │
│     • get_function_configuration()                  │
│     • get_function_code_location()                  │
│                                                     │
│   Stage 2: Environment Variable Extraction          │
│     • Parse environment dict                        │
│     • Extract DB credentials, API keys              │
│     • Store in findings table                       │
│                                                     │
│   Stage 3: Function Code Analysis                   │
│     • download_function_code()                      │
│     • Extract source code                           │
│     • Identify hardcoded secrets/URLs                │
│                                                     │
│   Stage 4: Layer Analysis                           │
│     • list_layers()                                 │
│     • get_layer_version_by_arn()                    │
│     • Inspect layer content                         │
│                                                     │
│   Stage 5: Code Injection                           │
│     • Create malicious Lambda function code         │
│     • Package as ZIP                                │
│     • upload_function_code() + update               │
│     • Alternative: create_function() (backdoor)     │
│                                                     │
│   Stage 6: Invocation Monitoring                    │
│     • CloudWatch Logs query                         │
│     • Capture function output                       │
│     • Extract exfiltrated data                      │
│                                                     │
│ Output Storage:                                     │
│   → PostgreSQL Lambda findings                      │
│   → Extracted env vars (encrypted)                  │
│   → Function code samples (S3)                      │
│ MITRE Mapping: T1552, T1059                         │
│ Output: lambda_exploit_module.py + injected code    │
└──────────────────────────────────────────────────────┘
  ↓
┌──────────────────────────────────────────────────────┐
│ 4.5: Container/ECS Exploitation                     │
│ Duration: 6-7 days                                  │
│ Module: ecs_exploit_module.py                       │
│ Dependencies:                                       │
│   - boto3 ECS, ECR clients                          │
│   - Docker CLI (container escape)                   │
│   - Container escape tools                          │
│ Attack Stages:                                      │
│   Stage 1: Cluster Enumeration                      │
│     • list_clusters()                               │
│     • list_services()                               │
│     • describe_services()                           │
│                                                     │
│   Stage 2: Task Enumeration                         │
│     • list_tasks()                                  │
│     • describe_tasks()                              │
│     • Extract IAM role ARNs                         │
│                                                     │
│   Stage 3: Metadata Service Access                  │
│     • Query ECS task metadata endpoint               │
│     • Extract IAM temporary credentials             │
│                                                     │
│   Stage 4: IAM Role Assumption                      │
│     • Use extracted temporary credentials           │
│     • Assume task's IAM role                        │
│     • Verify permissions gained                     │
│                                                     │
│   Stage 5: Container Image Analysis                 │
│     • describe_repositories()                       │
│     • batch_get_image()                             │
│     • Extract image layers                          │
│     • Scan for secrets (trivy, grype)               │
│                                                     │
│   Stage 6: Container Escape (Optional)              │
│     • Escalate from container → host                │
│     • Use kernel exploits (CVE-based)               │
│     • Access host Docker socket                     │
│                                                     │
│ Output Storage:                                     │
│   → PostgreSQL ECS findings                         │
│   → Extracted credentials                          │
│   → Image analysis reports                         │
│ MITRE Mapping: T1552, T1611                         │
│ Output: ecs_exploit_module.py + container analysis  │
└──────────────────────────────────────────────────────┘
  ↓
┌──────────────────────────────────────────────────────┐
│ 4.6: API Gateway Exploitation                       │
│ Duration: 5-6 days                                  │
│ Module: api_gateway_module.py                       │
│ Dependencies:                                       │
│   - boto3 API Gateway client                        │
│   - requests (API testing)                          │
│   - custom auth bypass logic                        │
│ Attack Stages:                                      │
│   Stage 1: API Enumeration                          │
│     • get_rest_apis()                               │
│     • get_resources()                               │
│     • get_methods()                                 │
│                                                     │
│   Stage 2: Auth Mechanism Detection                 │
│     • Identify authorizers (Lambda, IAM, Cognito)   │
│     • get_authorizer()                              │
│                                                     │
│   Stage 3: Authentication Bypass Attempt            │
│     • Test unauthenticated access                   │
│     • Bypass auth headers (if weakly validated)     │
│     • Token prediction/brute force (if weak)        │
│                                                     │
│   Stage 4: Endpoint Enumeration                     │
│     • Test all discovered endpoints                 │
│     • HTTP method testing (PUT, DELETE if allowed)  │
│     • Parameter fuzzing                             │
│                                                     │
│   Stage 5: Credential Extraction                    │
│     • API key leakage (headers, responses)          │
│     • Backend AWS credential exposure               │
│                                                     │
│ Output Storage:                                     │
│   → PostgreSQL API findings                         │
│   → Bypass technique details                        │
│ MITRE Mapping: T1552, T1021                         │
│ Output: api_gateway_module.py + API exploitation    │
└──────────────────────────────────────────────────────┘
  ↓
┌──────────────────────────────────────────────────────┐
│ 4.7: Database Exploitation                          │
│ Duration: 5-6 days                                  │
│ Module: database_exploit_module.py                  │
│ Dependencies:                                       │
│   - boto3 RDS client                                │
│   - pymysql / psycopg2 (direct connections)         │
│   - custom SQL injection payloads                   │
│ Attack Stages:                                      │
│   Stage 1: RDS Instance Enumeration                 │
│     • describe_db_instances()                       │
│     • Extract endpoints, ports, engine types        │
│                                                     │
│   Stage 2: Network Connectivity Testing             │
│     • Port scanning discovered RDS instances        │
│     • Test from EC2 within VPC                      │
│                                                     │
│   Stage 3: Credential Guessing                      │
│     • Common defaults (admin/password)              │
│     • Use extracted credentials from other modules  │
│                                                     │
│   Stage 4: SQL Injection Testing                    │
│     • Identify injectable parameters                │
│     • Extract database contents                     │
│     • Pivot to OS command execution                 │
│                                                     │
│   Stage 5: DynamoDB Exploitation                    │
│     • scan() without pagination (data exfil)        │
│     • query() with overloaded capacity              │
│                                                     │
│ Output Storage:                                     │
│   → PostgreSQL database findings                    │
│   → Sample data (non-sensitive)                     │
│ MITRE Mapping: T1552, T1021                         │
│ Output: database_exploit_module.py + DB analysis    │
└──────────────────────────────────────────────────────┘
  ↓
[PHASE 4 COMPLETE] → Full exploitation chain functional
```

### PHASE 5: POST-EXPLOITATION (Weeks 10-12)

```
[PHASE 4 COMPLETE]
  ↓
┌──────────────────────────────────────────────────────┐
│ 5.1: Persistence Mechanisms                         │
│ Duration: 5-6 days                                  │
│ Module: persistence_module.py                       │
│ Dependencies:                                       │
│   - boto3 IAM, Lambda, EC2, CloudWatch clients      │
│   - cryptography (cleanup key storage)              │
│ Persistence Methods:                                │
│   Method 1: IAM Backdoor User                       │
│     • create_user(UserName='audit-bot-<random>')    │
│     • create_access_key()                           │
│     • attach_user_policy() → admin policy           │
│     • Store credentials for cleanup                 │
│                                                     │
│   Method 2: Lambda Backdoor                         │
│     • create_function() (hidden function)           │
│     • Trigger via CloudWatch Events                 │
│     • Or trigger via API Gateway                    │
│                                                     │
│   Method 3: EC2 Persistence                         │
│     • CloudWatch Events → Lambda (scheduled)        │
│     • Or: User data script (non-persistent)         │
│                                                     │
│   Method 4: API Gateway C2                          │
│     • create_rest_api()                             │
│     • Integrate Lambda for command execution        │
│                                                     │
│ Cleanup Mechanism:                                  │
│   • Store all created resources in PostgreSQL       │
│   • On exit: delete_user(), delete_function(), etc. │
│   • --persist flag: skip cleanup for red team       │
│                                                     │
│ Output Storage:                                     │
│   → PostgreSQL persistence findings                 │
│   → Cleanup credentials (encrypted)                 │
│ MITRE Mapping: T1098, T1136, T1547                  │
│ Output: persistence_module.py + backdoor catalog    │
└──────────────────────────────────────────────────────┘
  ↓
┌──────────────────────────────────────────────────────┐
│ 5.2: Lateral Movement                               │
│ Duration: 4-5 days                                  │
│ Module: lateral_movement_module.py                  │
│ Dependencies:                                       │
│   - boto3 STS client                                │
│   - Cross-account role analysis                     │
│ Movement Techniques:                                │
│   Technique 1: Cross-Account Role Assumption        │
│     • find_assumable_roles()                        │
│     • Parse trust policies                          │
│     • assume_role() with ExternalId bypass          │
│                                                     │
│   Technique 2: Service-to-Service Compromise        │
│     • Lambda → RDS (via role assumption)            │
│     • EC2 → Lambda (via role assumption)            │
│                                                     │
│   Technique 3: Privilege Escalation Chain           │
│     • Limited role → Intermediate → Admin           │
│     • Use findings from Phase 4.1                   │
│                                                     │
│ Output Storage:                                     │
│   → PostgreSQL lateral movement chain               │
│   → Cross-account access proof                      │
│ MITRE Mapping: T1087, T1526, T1134                  │
│ Output: lateral_movement_module.py + access chains  │
└──────────────────────────────────────────────────────┘
  ↓
┌──────────────────────────────────────────────────────┐
│ 5.3: Data Exfiltration Simulation                   │
│ Duration: 4-5 days                                  │
│ Module: exfiltration_module.py                      │
│ Dependencies:                                       │
│   - boto3 S3, RDS, EBS, Secrets Manager clients     │
│   - Data classification logic                       │
│ Exfiltration Simulation:                            │
│   Stage 1: Sensitive Data Discovery                 │
│     • S3 buckets with PII patterns                  │
│     • RDS databases (sensitive tables)              │
│     • EBS snapshots with logs                       │
│     • Secrets Manager values                        │
│                                                     │
│   Stage 2: Impact Calculation                       │
│     • Calculate total data size                     │
│     • Estimate transfer time (network speed)        │
│     • Classify by sensitivity (PII, PHI, PCI)       │
│                                                     │
│   Stage 3: Exfiltration Simulation (Non-destructive)│
│     • Create tar.gz (don't actually transfer)       │
│     • Log exfil methods (S3, DNS, HTTP)             │
│     • Estimate detection likelihood                 │
│                                                     │
│ Safety Features:                                    │
│   • Dry-run mode (calculate, don't execute)         │
│   • Isolated S3 bucket for test exfil               │
│   • Data encryption before "transfer"               │
│   • Automatic cleanup                               │
│                                                     │
│ Output Storage:                                     │
│   → PostgreSQL exfil findings                       │
│   → Impact analysis report                          │
│ MITRE Mapping: T1537, T1020                         │
│ Output: exfiltration_module.py + impact analysis    │
└──────────────────────────────────────────────────────┘
  ↓
┌──────────────────────────────────────────────────────┐
│ 5.4: Command & Control (C2)                         │
│ Duration: 5-6 days                                  │
│ Module: c2_module.py                                │
│ Dependencies:                                       │
│   - boto3 Lambda, S3, API Gateway, CloudWatch       │
│   - Custom C2 payload generation                    │
│ C2 Channels Implemented:                            │
│   Channel 1: Lambda-based C2                        │
│     • create_function(RunAs hidden function)        │
│     • API Gateway integration                       │
│     • Query: GET /c2?cmd=<base64_command>           │
│     • Response: Lambda output encoded                │
│                                                     │
│   Channel 2: S3 Bucket C2                           │
│     • S3 bucket as command queue                    │
│     • Agent lists /commands/ prefix                 │
│     • Executes files found                          │
│     • Uploads /output/ to bucket                    │
│                                                     │
│   Channel 3: CloudWatch Logs C2                     │
│     • Log group as command channel                  │
│     • Agent queries log streams                     │
│     • Executes commands from log content            │
│     • Writes output as log events                   │
│                                                     │
│   Channel 4: API Gateway C2                         │
│     • RESTful API for command/control               │
│     • JWT auth bypass (if applicable)               │
│     • Bidirectional communication                   │
│                                                     │
│ Evasion Features:                                   │
│   • Randomized naming (audit-<random>)              │
│   • Rate limiting (avoid CloudTrail spam)           │
│   • Payload encryption                              │
│   • Timing randomization                            │
│                                                     │
│ Output Storage:                                     │
│   → PostgreSQL C2 infrastructure                    │
│   → Command/response logs                           │
│ MITRE Mapping: T1071 (Application Layer Protocol)   │
│ Output: c2_module.py + C2 infrastructure            │
└──────────────────────────────────────────────────────┘
  ↓
[PHASE 5 COMPLETE] → Full cyber kill chain operational
```

### PHASE 6: EVASION & DETECTION BYPASS (Weeks 12-14)

```
[PHASE 5 COMPLETE]
  ↓
┌──────────────────────────────────────────────────────┐
│ 6.1: GuardDuty Evasion                              │
│ Duration: 4-5 days                                  │
│ Module: evasion_guardduty_module.py                 │
│ Dependencies:                                       │
│   - boto3 GuardDuty, CloudWatch clients             │
│   - GuardDuty findings knowledge base                │
│ Evasion Techniques:                                 │
│   Technique 1: Rate Limiting                        │
│     • Limit API calls/minute                        │
│     • Spread reconnaissance over time                │
│     • Avoid spike detection                         │
│                                                     │
│   Technique 2: Legitimate API Usage                 │
│     • Use common AWS CLI commands                   │
│     • Mimic normal DevOps workflows                 │
│     • Use session manager (not direct API)          │
│                                                     │
│   Technique 3: Common Port Usage                    │
│     • Avoid unusual port combinations               │
│     • Use 22 (SSH), 443 (HTTPS), 3389 (RDP)         │
│     • Avoid suspicious port scanning                │
│                                                     │
│   Technique 4: Credential Usage Evasion             │
│     • Use legitimate credentials (if compromised)   │
│     • Avoid suspicious permission errors            │
│     • Use assumed roles (not direct keys)           │
│                                                     │
│ Validation:                                         │
│   1. Enable GuardDuty on test account               │
│   2. Execute attacks with evasion enabled           │
│   3. Check GuardDuty findings                       │
│   4. Measure detection rate (goal: <50%)            │
│   5. Iterate evasion techniques                     │
│                                                     │
│ Output Storage:                                     │
│   → PostgreSQL GuardDuty findings (before/after)    │
│   → Evasion effectiveness metrics                   │
│ MITRE Mapping: T1036 (Masquerading)                 │
│ Output: evasion_guardduty_module.py + metrics       │
└──────────────────────────────────────────────────────┘
  ↓
┌──────────────────────────────────────────────────────┐
│ 6.2: CloudTrail Obfuscation                         │
│ Duration: 4-5 days                                  │
│ Module: evasion_cloudtrail_module.py                │
│ Dependencies:                                       │
│   - boto3 CloudTrail, CloudWatch Logs Insights      │
│   - Log analysis patterns                           │
│ Obfuscation Techniques:                             │
│   Technique 1: High-Volume API Calls                │
│     • Generate massive benign logs                  │
│     • Bury malicious calls in noise                 │
│     • Overwhelm log aggregation                     │
│                                                     │
│   Technique 2: Cross-Account Pivoting               │
│     • Assume role in different account              │
│     • CloudTrail credits different account          │
│     • Original account sees no logs                 │
│                                                     │
│   Technique 3: Shared Responsibility                │
│     • Use AWS-managed service actions               │
│     • CloudTrail may not log service-to-service     │
│                                                     │
│   Technique 4: IAM Access Analyzer Bypass           │
│     • Use policy simulator (not reflected in logs)  │
│     • Avoid get_iam_access_analyzer_findings()      │
│                                                     │
│ Validation:                                         │
│   1. Document baseline CloudTrail logs              │
│   2. Execute attacks with obfuscation               │
│   3. Query CloudWatch Logs Insights                 │
│   4. Measure logged vs unlogged actions             │
│   5. Calculate coverage percentage                  │
│                                                     │
│ Output Storage:                                     │
│   → PostgreSQL log coverage analysis                │
│   → Unlogged actions identified                     │
│ MITRE Mapping: T1562 (Indicator Removal)            │
│ Output: evasion_cloudtrail_module.py + analysis     │
└──────────────────────────────────────────────────────┘
  ↓
┌──────────────────────────────────────────────────────┐
│ 6.3: Logging Bypass                                 │
│ Duration: 3-4 days                                  │
│ Module: evasion_logging_module.py                   │
│ Dependencies:                                       │
│   - boto3 EC2, CloudWatch, VPC Flow Logs clients    │
│   - Network traffic analysis                        │
│ Logging Bypass Targets:                             │
│   Target 1: VPC Flow Logs                           │
│     • Log at 5-tuple level (src_ip, dst_ip, port)  │
│     • Bypass: Use internal-only communication       │
│     • Bypass: High-volume traffic (overwhelm)       │
│                                                     │
│   Target 2: CloudWatch Logs                         │
│     • App-level logging                             │
│     • Bypass: Compromise agent (disable logs)       │
│     • Bypass: Saturate log group (quota exceeded)   │
│                                                     │
│   Target 3: AWS Config                              │
│     • Change tracking                               │
│     • Bypass: Disable AWS Config                    │
│     • Bypass: Bypass rule evaluation                │
│                                                     │
│ Validation:                                         │
│   1. Enable all logging services                    │
│   2. Execute attacks with bypass techniques         │
│   3. Query logs for evidence                        │
│   4. Identify logging gaps                          │
│                                                     │
│ Output Storage:                                     │
│   → PostgreSQL logging gaps identified              │
│   → Bypass success metrics                          │
│ MITRE Mapping: T1562 (Indicator Removal)            │
│ Output: evasion_logging_module.py + gap analysis    │
└──────────────────────────────────────────────────────┘
  ↓
┌──────────────────────────────────────────────────────┐
│ 6.4: Detection Validation                           │
│ Duration: 3-4 days                                  │
│ Module: detection_validation_module.py              │
│ Dependencies:                                       │
│   - Prowler integration (execution & parsing)       │
│   - Finding correlation logic                       │
│ Validation Process:                                 │
│   Stage 1: Baseline Scan                            │
│     $ prowler aws -g checklist -c -l                │
│     → Capture all findings                          │
│                                                     │
│   Stage 2: Execute Attacks                          │
│     • Run full exploitation chain                   │
│     • Log all actions performed                     │
│                                                     │
│   Stage 3: Post-Attack Scan                         │
│     $ prowler aws -g checklist -c -l                │
│     → Capture all findings                          │
│                                                     │
│   Stage 4: Comparison & Analysis                    │
│     • Baseline vs Post-attack findings              │
│     • New findings identified                       │
│     • Missed findings identified                    │
│     • False positives counted                       │
│                                                     │
│   Stage 5: Gap Analysis                             │
│     • What attacks were undetected?                 │
│     • What detection rules failed?                  │
│     • What could be improved?                       │
│                                                     │
│ Metrics Calculated:                                 │
│   • Detection rate: % of attacks detected           │
│   • False positive rate: % benign flagged           │
│   • MTTR (Mean Time to Remediation)                 │
│   • Coverage: which services detected               │
│                                                     │
│ Output Storage:                                     │
│   → PostgreSQL detection effectiveness findings     │
│   → Gap analysis recommendations                    │
│ Output: detection_validation_module.py + report     │
└──────────────────────────────────────────────────────┘
  ↓
[PHASE 6 COMPLETE] → Full evasion capability verified
```

### PHASE 7: TESTING & INTEGRATION (Weeks 14-16)

```
[PHASE 6 COMPLETE]
  ↓
┌──────────────────────────────────────────────────────┐
│ 7.1: Unit Testing                                   │
│ Duration: 5-6 days                                  │
│ Framework: pytest 7.4+                              │
│ Test Coverage Target: >85%                          │
│ Tests Per Module:                                   │
│   • Module initialization                           │
│   • Individual function execution                   │
│   • Error handling                                  │
│   • Mock AWS API responses (moto)                   │
│   • Database operations (PostgreSQL test instance)  │
│ Test Structure:                                     │
│   tests/unit/                                       │
│   ├── test_aws_enum_module.py                       │
│   ├── test_iam_privesc_module.py                    │
│   ├── test_ec2_exploit_module.py                    │
│   └── ... (1 test file per module)                  │
│                                                     │
│ Mocking Approach:                                   │
│   • moto library for AWS API mocking                │
│   • responses library for HTTP mocking              │
│   • pytest fixtures for test data                   │
│   • Test database (separate from production)        │
│                                                     │
│ CI Integration:                                     │
│   • GitHub Actions runs pytest on every push        │
│   • Code coverage report generated (pytest-cov)     │
│   • Coverage must be >85% to pass                   │
│   • Coverage report uploaded to codecov.io          │
│                                                     │
│ Output: tests/unit/ directory + codecov report      │
└──────────────────────────────────────────────────────┘
  ↓
┌──────────────────────────────────────────────────────┐
│ 7.2: Integration Testing                            │
│ Duration: 5-6 days                                  │
│ Test Scope: Module interactions & data flow         │
│ Test Scenarios:                                     │
│   Scenario 1: Reconnaissance → Exploitation         │
│     • Enum findings feed into exploit module        │
│     • Verified findings returned to reporting       │
│                                                     │
│   Scenario 2: Full Attack Chain (5 modules)         │
│     • Enum → Privesc → EC2 Exploit → Persist →     │
│     • Lateral Movement                              │
│     • Each stage validated                          │
│                                                     │
│   Scenario 3: Parallel Module Execution             │
│     • Multiple modules run simultaneously            │
│     • No race conditions                            │
│     • PostgreSQL consistency maintained             │
│                                                     │
│   Scenario 4: Error Recovery                        │
│     • Module fails mid-execution                    │
│     • Orchestrator catches error                    │
│     • Partial findings still reported               │
│     • Cleanup still triggered                       │
│                                                     │
│ Test Structure:                                     │
│   tests/integration/                                │
│   ├── test_recon_to_exploit_chain.py                │
│   ├── test_parallel_module_execution.py             │
│   └── test_error_recovery.py                        │
│                                                     │
│ Output: Integration test results + coverage         │
└──────────────────────────────────────────────────────┘
  ↓
┌──────────────────────────────────────────────────────┐
│ 7.3: Red Team Exercise (E2E Test)                   │
│ Duration: 5-6 days                                  │
│ Environment: Dedicated test AWS account             │
│ Scenario 1: Limited Operator (Read-Only IAM)        │
│   • Start with minimal permissions                  │
│   • Enumerate environment                           │
│   • Find privilege escalation path                  │
│   • Escalate to admin                               │
│   • Verify objective achieved                       │
│                                                     │
│ Scenario 2: Insider Threat (Admin Access)           │
│   • Start with admin role                           │
│   • Compromise EC2 instance                         │
│   • Pivot to Lambda, RDS                            │
│   • Establish persistence                           │
│   • Exfiltrate data                                 │
│   • Verify undetectable (with evasion on)           │
│                                                     │
│ Scenario 3: Mixed Attack Path                       │
│   • Compromise EC2 → Pivot to RDS → Escalate IAM   │
│   • Test realistic attack chains                    │
│                                                     │
│ Metrics Captured:                                   │
│   • Total time to root/admin                        │
│   • # of findings discovered                        │
│   • Attack success rate (target/total)              │
│   • Evasion effectiveness                           │
│   • Detection rate (Prowler + GuardDuty)            │
│                                                     │
│ Output: Red team exercise report + metrics          │
└──────────────────────────────────────────────────────┘
  ↓
┌──────────────────────────────────────────────────────┐
│ 7.4: Documentation                                  │
│ Duration: 5-6 days                                  │
│ Documentation Types:                                │
│   1. API Documentation                              │
│      • Module class definitions                     │
│      • Function signatures & parameters             │
│      • Return types & exceptions                    │
│      • Generated via sphinx-autodoc                 │
│                                                     │
│   2. User Guide                                     │
│      • Installation instructions                    │
│      • Configuration guide                          │
│      • Attack scenario YAML examples                │
│      • Troubleshooting                              │
│                                                     │
│   3. Module Development Guide                       │
│      • How to create new modules                    │
│      • Base class interface                         │
│      • Testing requirements                         │
│      • Integration points                           │
│                                                     │
│   4. Deployment Guide                               │
│      • Docker setup                                 │
│      • AWS infrastructure deployment                │
│      • CI/CD configuration                          │
│      • Security hardening checklist                 │
│                                                     │
│   5. Architecture Guide                             │
│      • System design overview                       │
│      • Module interactions                          │
│      • Data flow diagrams                           │
│      • This UML document!                           │
│                                                     │
│ Output: docs/ directory with Sphinx builds          │
└──────────────────────────────────────────────────────┘
  ↓
[PHASE 7 COMPLETE] → Fully tested & documented toolkit
```

### PHASE 8: HARDENING & RELEASE (Weeks 16-17)

```
[PHASE 7 COMPLETE]
  ↓
┌──────────────────────────────────────────────────────┐
│ 8.1: Security Hardening                             │
│ Duration: 3-4 days                                  │
│ Hardening Checks:                                   │
│   Check 1: Secret Detection                         │
│     • Tool: truffleHog / detect-secrets             │
│     $ git log --all --oneline | grep -i secret      │
│     → Ensure NO AWS keys, DB passwords, tokens      │
│                                                     │
│   Check 2: Dependency Vulnerability Scanning        │
│     • Tool: pip-audit / safety                      │
│     $ pip-audit                                     │
│     → Update vulnerable packages                    │
│     → Pin safe versions in pyproject.toml           │
│                                                     │
│   Check 3: Code Security Scanning                   │
│     • Tool: bandit (Python SAST)                    │
│     $ bandit -r src/                                │
│     → Fix hardcoded credentials, SQL injection      │
│                                                     │
│   Check 4: Infrastructure Security                  │
│     • Review IAM policies (least privilege)         │
│     • Enable encryption (S3, RDS, EBS)              │
│     • Enable logging (CloudTrail, CloudWatch)       │
│     • VPC security groups (restrict access)         │
│                                                     │
│   Check 5: Secrets Management                       │
│     • Credentials in AWS Secrets Manager only       │
│     • .env file only for local development          │
│     • Never commit credentials                      │
│     • Rotate test credentials                       │
│                                                     │
│   Check 6: Docker Image Security                    │
│     • Tool: trivy / grype                           │
│     $ trivy image red-team-toolkit:latest           │
│     → Scan for vulnerable base image layers         │
│     → Use minimal base (python:3.11-slim)           │
│                                                     │
│ Output: Security audit report + fixes applied       │
└──────────────────────────────────────────────────────┘
  ↓
┌──────────────────────────────────────────────────────┐
│ 8.2: Performance Optimization                       │
│ Duration: 3-4 days                                  │
│ Optimization Areas:                                 │
│   Optimization 1: Async/Concurrent Execution        │
│     • Ensure all I/O operations are async           │
│     • Use asyncio.gather() for parallelism          │
│     • Benchmark: Target 10-15 second recon          │
│                                                     │
│   Optimization 2: Database Indexing                 │
│     • Add indexes on common query columns           │
│     • PostgreSQL: CREATE INDEX on module_name       │
│     • Test query execution plans                    │
│                                                     │
│   Optimization 3: Caching                           │
│     • Redis caching for enumeration results         │
│     • Cache invalidation strategy                   │
│     • TTL-based cache expiration                    │
│                                                     │
│   Optimization 4: Connection Pooling                │
│     • Database connection pool management           │
│     • boto3 session reuse                           │
│     • Avoid connection exhaustion                   │
│                                                     │
│ Performance Benchmarks:                             │
│   • Account enumeration: < 15 seconds               │
│   • IAM enumeration: < 30 seconds                   │
│   • Full recon: < 5 minutes                         │
│   • Report generation: < 2 minutes                  │
│                                                     │
│ Output: Optimized code + performance benchmarks     │
└──────────────────────────────────────────────────────┘
  ↓
┌──────────────────────────────────────────────────────┐
│ 8.3: GitHub Publication & Release                   │
│ Duration: 2-3 days                                  │
│ Release Steps:                                      │
│   Step 1: Repository Setup                          │
│     • Create GitHub repository (public)             │
│     • README.md with overview & quick start         │
│     • LICENSE (MIT recommended)                     │
│     • CONTRIBUTING.md for contributors              │
│                                                     │
│   Step 2: GitHub Configuration                      │
│     • Enable branch protection (main)               │
│     • Require PR reviews before merge                │
│     • Require CI checks to pass                     │
│     • Enable security alerts                        │
│                                                     │
│   Step 3: CI/CD Pipeline Setup                      │
│     • GitHub Actions workflows active               │
│     • Test → Build → Deploy pipeline working        │
│     • Codecov integration for coverage              │
│                                                     │
│   Step 4: Release Creation                          │
│     • Create GitHub Release (v1.0.0)                │
│     • Tag: git tag -a v1.0.0                        │
│     • Release notes: Features, fixes, docs          │
│     • Attach release artifacts (optional)           │
│                                                     │
│   Step 5: Docker Registry                           │
│     • Push to Docker Hub (optional)                 │
│     • Or: Publish to GitHub Container Registry      │
│     • Add shields/badges to README                  │
│                                                     │
│   Step 6: PyPI Publication (Optional)               │
│     • Build package: poetry build                   │
│     • Publish: poetry publish                       │
│     • Users can: pip install red-team-toolkit       │
│                                                     │
│ Launch Metrics to Track:                            │
│   • GitHub stars (target: 50+ first month)          │
│   • GitHub forks                                    │
│   • Open issues / PRs                               │
│   • Download stats (PyPI, Docker Hub)               │
│                                                     │
│ Post-Launch:                                        │
│   • Write blog post on Medium (project deep-dive)   │
│   • Tweet announcement (@infosec community)         │
│   • Conference talk proposal (DEF CON, Black Hat)   │
│   • Academic paper (publish findings)               │
│                                                     │
│ Output: Live GitHub repository + public release     │
└──────────────────────────────────────────────────────┘
  ↓
[PHASE 8 COMPLETE] → Production-ready toolkit published!
  ↓
END
```

---

## 3. MODULE DEPENDENCY GRAPH

```
ORCHESTRATOR (Main Entry)
    ↓
    ├─→ CREDENTIAL_MANAGER
    │       ├─→ AWS Secrets Manager
    │       └─→ STS (temporary tokens)
    │
    ├─→ LOGGING_SYSTEM
    │       ├─→ CloudWatch Logs
    │       ├─→ Local files
    │       └─→ JSON format
    │
    ├─→ RECONNAISSANCE_LAYER (Parallel Execution)
    │       ├─→ AWS_ENUM_MODULE
    │       │       ├─→ boto3 (EC2, S3, Lambda, RDS)
    │       │       ├─→ aioboto3 (async execution)
    │       │       └─→ PostgreSQL (store results)
    │       │
    │       ├─→ IAM_ENUM_MODULE
    │       │       ├─→ boto3 IAM client
    │       │       ├─→ Policy analysis logic
    │       │       └─→ PostgreSQL (privilege escalation paths)
    │       │
    │       ├─→ NETWORK_ENUM_MODULE
    │       │       ├─→ boto3 EC2 client
    │       │       ├─→ nmap (port scanning)
    │       │       └─→ PostgreSQL (network topology)
    │       │
    │       └─→ SERVICE_ENUM_MODULE
    │               ├─→ boto3 multi-service clients
    │               └─→ PostgreSQL (service catalog)
    │
    ├─→ EXPLOITATION_LAYER (Sequential, dependent on Recon)
    │       ├─→ IAM_PRIVESC_MODULE
    │       │       ├─→ boto3 IAM client
    │       │       ├─→ PACU integration
    │       │       └─→ PostgreSQL (findings)
    │       │
    │       ├─→ EC2_EXPLOIT_MODULE
    │       │       ├─→ boto3 EC2 client
    │       │       ├─→ nmap, paramiko, pywinrm
    │       │       └─→ PostgreSQL (compromises)
    │       │
    │       ├─→ S3_EXPLOIT_MODULE
    │       │       ├─→ boto3 S3 client
    │       │       ├─→ aioboto3 (async listing)
    │       │       └─→ PostgreSQL + S3 (findings)
    │       │
    │       ├─→ LAMBDA_EXPLOIT_MODULE
    │       │       ├─→ boto3 Lambda client
    │       │       ├─→ Custom payloads
    │       │       └─→ PostgreSQL (findings)
    │       │
    │       ├─→ ECS_EXPLOIT_MODULE
    │       │       ├─→ boto3 ECS, ECR clients
    │       │       ├─→ Docker CLI
    │       │       └─→ PostgreSQL (findings)
    │       │
    │       ├─→ API_GATEWAY_MODULE
    │       │       ├─→ boto3 API Gateway client
    │       │       ├─→ requests (HTTP testing)
    │       │       └─→ PostgreSQL (findings)
    │       │
    │       └─→ DATABASE_EXPLOIT_MODULE
    │               ├─→ boto3 RDS, DynamoDB clients
    │               ├─→ pymysql, psycopg2
    │               └─→ PostgreSQL (findings)
    │
    ├─→ POST_EXPLOITATION_LAYER
    │       ├─→ PERSISTENCE_MODULE
    │       │       ├─→ boto3 IAM, Lambda, EC2 clients
    │       │       ├─→ cryptography (key storage)
    │       │       └─→ PostgreSQL (backdoor catalog)
    │       │
    │       ├─→ LATERAL_MOVEMENT_MODULE
    │       │       ├─→ boto3 STS client
    │       │       ├─→ Trust policy analysis
    │       │       └─→ PostgreSQL (access chains)
    │       │
    │       ├─→ EXFILTRATION_MODULE
    │       │       ├─→ boto3 S3, RDS, Secrets Manager
    │       │       ├─→ Data classification
    │       │       └─→ PostgreSQL (impact analysis)
    │       │
    │       └─→ C2_MODULE
    │               ├─→ boto3 Lambda, S3, API Gateway
    │               ├─→ Custom payloads
    │               └─→ PostgreSQL (C2 infrastructure)
    │
    ├─→ EVASION_LAYER
    │       ├─→ EVASION_GUARDDUTY_MODULE
    │       │       ├─→ boto3 GuardDuty client
    │       │       ├─→ Evasion logic
    │       │       └─→ PostgreSQL (effectiveness metrics)
    │       │
    │       ├─→ EVASION_CLOUDTRAIL_MODULE
    │       │       ├─→ boto3 CloudTrail, CloudWatch Logs
    │       │       ├─→ Obfuscation logic
    │       │       └─→ PostgreSQL (coverage analysis)
    │       │
    │       ├─→ EVASION_LOGGING_MODULE
    │       │       ├─→ boto3 VPC Flow Logs, CloudWatch
    │       │       ├─→ Bypass logic
    │       │       └─→ PostgreSQL (gap analysis)
    │       │
    │       └─→ DETECTION_VALIDATION_MODULE
    │               ├─→ Prowler integration
    │               ├─→ Finding comparison
    │               └─→ PostgreSQL (effectiveness report)
    │
    └─→ REPORTING_LAYER
            ├─→ REPORTING_MODULE
            │       ├─→ Jinja2 (template engine)
            │       ├─→ matplotlib (charts)
            │       ├─→ fpdf2 (PDF generation)
            │       ├─→ pandas (data aggregation)
            │       └─→ S3 (report storage)
            │
            └─→ DATA PERSISTENCE
                    ├─→ PostgreSQL (findings, execution metadata)
                    ├─→ Redis (cache, session state)
                    ├─→ S3 (reports, logs, evidence)
                    ├─→ CloudWatch (logs, metrics)
                    └─→ Secrets Manager (credentials)
```

---

## 4. TOOL-TO-MODULE MAPPING MATRIX

| Module | Primary Tool | Secondary Tools | Data Source | Data Sink | AWS Services |
|--------|--------------|-----------------|------------|-----------|--------------|
| **Orchestrator** | asyncio | Click, Pydantic | YAML config | Logs | - |
| **Credential Manager** | boto3 STS | cryptography | AWS config | Secrets Mgr | STS, Secrets Manager |
| **Logging System** | loguru | watchtower | Python code | CloudWatch, File | CloudWatch |
| **Reporting** | Jinja2 | matplotlib, fpdf2 | PostgreSQL | S3, stdout | S3 |
| **AWS Enum** | boto3 | aioboto3 | AWS API | PostgreSQL, Redis | EC2, S3, Lambda, RDS, IAM |
| **IAM Enum** | boto3 IAM | networkx | AWS API | PostgreSQL | IAM |
| **Network Enum** | boto3 EC2 | nmap, NetworkX | AWS API, IP | PostgreSQL, S3 | EC2, VPC |
| **Service Enum** | boto3 | aioboto3 | AWS API | PostgreSQL | Lambda, API Gateway, ECS, DynamoDB |
| **IAM Privesc** | boto3 IAM | PACU | PostgreSQL | PostgreSQL | IAM |
| **EC2 Exploit** | boto3 EC2 | nmap, paramiko, pywinrm | AWS API + Port Scan | PostgreSQL | EC2, CloudWatch |
| **S3 Exploit** | boto3 S3 | aioboto3, s3fs | AWS API | PostgreSQL, S3 | S3 |
| **Lambda Exploit** | boto3 Lambda | zipfile | AWS API | PostgreSQL, Lambda | Lambda, CloudWatch Logs |
| **ECS Exploit** | boto3 ECS | Docker CLI | AWS API | PostgreSQL | ECS, ECR, IAM |
| **API Gateway** | boto3 API GW | requests | AWS API | PostgreSQL | API Gateway, Lambda |
| **Database Exploit** | boto3 RDS | pymysql, psycopg2 | AWS API | PostgreSQL | RDS, DynamoDB |
| **Persistence** | boto3 IAM | - | PostgreSQL | PostgreSQL, IAM, Lambda | IAM, Lambda, EC2, CloudWatch |
| **Lateral Movement** | boto3 STS | networkx | PostgreSQL | PostgreSQL | STS, IAM |
| **Exfiltration** | boto3 S3 | pandas | PostgreSQL, AWS API | PostgreSQL, S3 | S3, RDS, EBS, Secrets Manager |
| **C2** | boto3 | Custom payloads | PostgreSQL | PostgreSQL, Lambda, S3, API GW | Lambda, S3, API Gateway, CloudWatch |
| **GuardDuty Evasion** | boto3 GuardDuty | Rate limiting logic | AWS API | PostgreSQL | GuardDuty, CloudWatch |
| **CloudTrail Obfuscation** | boto3 CloudTrail | CloudWatch Logs Insights | AWS API, Logs | PostgreSQL | CloudTrail, CloudWatch Logs |
| **Logging Bypass** | boto3 EC2 | VPC Flow Logs, CloudWatch | AWS API | PostgreSQL | VPC Flow Logs, CloudWatch |
| **Detection Validation** | Prowler | boto3 | AWS API | PostgreSQL, stdout | Security Hub |

---

## 5. DATA FLOW SPECIFICATIONS

### Execution Flow (Top-Level)

```
┌─────────────────┐
│ YAML Config     │
│ (Attack Plan)   │
└────────┬────────┘
         ↓
┌──────────────────────────────────┐
│  ORCHESTRATOR                    │
│  1. Load config (YAML)           │
│  2. Validate preconditions       │
│  3. Load modules dynamically     │
│  4. Initialize credentials       │
└────────┬─────────────────────────┘
         ↓
┌──────────────────────────────────┐
│  PHASE EXECUTION (Async)         │
│  Phase 1-3 (Parallel Recon)      │
│  Phase 4-6 (Exploit → Evasion)   │
│  Phase 7-8 (Testing → Release)   │
└────────┬─────────────────────────┘
         ↓
    ┌────┴────┐
    ↓         ↓
┌────────┐  ┌──────────────┐
│PostgreSQL │ │ Redis Cache  │
│ Findings  │ │ State/Metrics│
│ Table     │ │              │
└────────┘  └──────────────┘
    ↓         ↓
    └────┬────┘
         ↓
┌──────────────────────────────────┐
│  REPORTING ENGINE                │
│  1. Aggregate findings           │
│  2. Generate charts (matplotlib) │
│  3. Create HTML/PDF report       │
│  4. Export as JSON/CSV           │
└────────┬─────────────────────────┘
         ↓
┌──────────────────────────────────┐
│  S3 BUCKET                       │
│  reports/                        │
│  ├── executive_summary.html      │
│  ├── technical_report.pdf        │
│  └── findings.json               │
└──────────────────────────────────┘
```

### Module Data Flow (Example: IAM Enumeration → Privilege Escalation)

```
┌───────────────────────────┐
│ IAM_ENUM_MODULE           │
│ (Reconnaissance)          │
│                           │
│ list_users()              │
│ list_roles()              │
│ get_user_policies()       │
└──────────┬────────────────┘
           │
           │ Findings:
           │ - Users: 5
           │ - Roles: 10
           │ - Privilege escalation paths: 3
           │
           ↓
┌────────────────────────────────────────┐
│ PostgreSQL escalation_paths TABLE      │
│                                        │
│ id │ user_id │ privilege │ vector     │
├────┼─────────┼───────────┼────────────┤
│ 1  │ user-1  │ admin     │ CreateUser │
│ 2  │ user-1  │ admin     │ AssumeRole │
│ 3  │ user-1  │ admin     │ AttachPolicy│
└────────────────────────────────────────┘
           │
           ↓ (Reading PostgreSQL)
┌────────────────────────────────────┐
│ IAM_PRIVESC_MODULE                 │
│ (Exploitation)                     │
│                                    │
│ For each escalation path:          │
│   1. Test CreateUser → Policy      │
│   2. Test AssumeRole → Verify      │
│   3. Test AttachPolicy → Success?  │
└──────────┬───────────────────────┘
           │
           │ Results:
           │ - CreateUser: SUCCESS (admin)
           │ - AssumeRole: FAILED (denied)
           │ - AttachPolicy: SUCCESS (admin)
           │
           ↓ (Writing PostgreSQL)
┌────────────────────────────────────┐
│ PostgreSQL findings TABLE          │
│                                    │
│ id │ severity │ title    │ status  │
├────┼──────────┼──────────┼─────────┤
│ 101│ CRITICAL │ Priv Esc │ SUCCESS │
│    │          │ CreateUsr│         │
└────────────────────────────────────┘
           │
           ↓ (Reading PostgreSQL)
┌────────────────────────────────────┐
│ REPORTING_MODULE                   │
│ Generate report (Jinja2 template)  │
│ Create charts (matplotlib)         │
│ Export to HTML/PDF                 │
└────────┬───────────────────────────┘
           │
           ↓ (Writing S3)
┌────────────────────────────────────┐
│ S3 reports/ bucket                 │
│                                    │
│ execution_2025-12-16_10-23         │
│ ├── summary.html (interactive)     │
│ ├── full_report.pdf                │
│ └── findings.json                  │
└────────────────────────────────────┘
```

---

## 6. SEQUENCE DIAGRAM: FULL ATTACK EXECUTION

```
Actor      Orchestrator    EnumModule  ExploitModule  Database    Reporting
  │            │              │             │            │           │
  │            │              │             │            │           │
  ├──Load──────→│              │             │            │           │
  │   Config    │              │             │            │           │
  │            │              │             │            │           │
  │            ├──Initialize──→│             │            │           │
  │            │   Recon       │             │            │           │
  │            │              │             │            │           │
  │            │    Enumerate AWS resources (async, parallel)        │
  │            │              │             │            │           │
  │            │              ├──Query──────→│            │           │
  │            │              │   EC2, S3    │            │           │
  │            │              │   Lambda etc │            │           │
  │            │              │             │            │           │
  │            │              ├──Store────────────────────→│          │
  │            │              │   findings   │            │           │
  │            │              │             │            │           │
  │            ├──Initialize──────────────→│            │           │
  │            │   Exploit                │            │           │
  │            │   (read from DB)         │            │           │
  │            │                           │            │           │
  │            │                           ├──Query────→│           │
  │            │                           │   findings │           │
  │            │                           │   (targets)            │
  │            │                           │            │           │
  │            │                           ├──Test─────→│ AWS      │
  │            │                           │   Services │           │
  │            │                           │            │           │
  │            │                           ├──Store────→│          │
  │            │                           │   Exploit  │           │
  │            │                           │   success  │           │
  │            │                           │            │           │
  │            ├──Aggregate─────────────────────────────→│          │
  │            │   all findings  │            │           │           │
  │            │                 │            │           │           │
  │            ├──Generate────────────────────────────────→│         │
  │            │   Report        │            │           │           │
  │            │                 │            │           │           │
  │            │                 │            │           ├──HTML───→ S3
  │            │                 │            │           │   PDF     
  │            │                 │            │           │   JSON    
  │            │                 │            │           │           │
  │←──Report────────────────────────────────────────────────────────│
  │  (S3 URL)  │              │             │            │           │
  │            │              │             │            │           │
```

---

## 7. DEPLOYMENT ARCHITECTURE & TOOL INTEGRATION

```
┌──────────────────────────────────────────────────────────────────┐
│                    DEVELOPER MACHINE                             │
│                                                                  │
│  Git Repository (GitHub)                                         │
│  ├── src/ (Source code)                                          │
│  ├── tests/ (Test suite)                                         │
│  ├── docker/ (Dockerfile, Docker Compose)                        │
│  ├── docs/ (Sphinx documentation)                                │
│  ├── .github/workflows/ (CI/CD pipelines)                        │
│  ├── pyproject.toml (Poetry dependencies)                        │
│  └── README.md                                                   │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Local Development Environment (Docker Compose)           │  │
│  │                                                          │  │
│  │  ┌────────────────┐  ┌────────────────┐               │  │
│  │  │ Python 3.11    │  │  PostgreSQL 15 │               │  │
│  │  │ + Dependencies │  │  (test data)   │               │  │
│  │  └────────────────┘  └────────────────┘               │  │
│  │                          │ Volume                      │  │
│  │        ↓ Mount           ↓ Mount                       │  │
│  │  ┌────────────────┐  ┌────────────────┐               │  │
│  │  │ Code Volume    │  │  Redis Cache   │               │  │
│  │  │ (./src)        │  │  (session)     │               │  │
│  │  └────────────────┘  └────────────────┘               │  │
│  │                                                       │  │
│  │  pytest runs locally                                  │  │
│  │  ├── tests/unit/ (moto mock AWS)                     │  │
│  │  ├── tests/integration/ (real local PostgreSQL)      │  │
│  │  └── coverage report → codecov.io                    │  │
│  │                                                       │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
└──────────────────────────────┬─────────────────────────────────┘
                               │
                        git push main
                               │
                               ↓
┌──────────────────────────────────────────────────────────────────┐
│                  GITHUB CI/CD PIPELINE                           │
│            (GitHub Actions Workflow Triggered)                   │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ JOB 1: TEST                                              │  │
│  │                                                          │  │
│  │ • Setup Python 3.11                                     │  │
│  │ • Install dependencies (Poetry)                         │  │
│  │ • Lint with Black, isort, flake8                        │  │
│  │ • Type check with mypy                                  │  │
│  │ • Run pytest (with PostgreSQL service)                  │  │
│  │ • Collect coverage (pytest-cov)                         │  │
│  │ • Upload to codecov.io                                  │  │
│  │ • Security scan with bandit                             │  │
│  │ • SAST scan with semgrep                                │  │
│  │                                                          │  │
│  │ Status: PASS ✓ (required to proceed)                    │  │
│  └──────────────────────────────────────────────────────────┘  │
│                        ↓ (on success)                           │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ JOB 2: BUILD                                             │  │
│  │                                                          │  │
│  │ • Setup Docker buildx                                   │  │
│  │ • Login to AWS ECR                                      │  │
│  │ • Build Docker image                                    │  │
│  │   FROM python:3.11-slim                                 │  │
│  │   + nmap, metasploit, kali tools                        │  │
│  │ • Tag: latest + git SHA                                 │  │
│  │ • Push to ECR repository                                │  │
│  │                                                          │  │
│  │ Status: PUSH COMPLETE                                   │  │
│  └──────────────────────────────────────────────────────────┘  │
│                        ↓ (on success)                           │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ JOB 3: DEPLOY                                            │  │
│  │                                                          │  │
│  │ • Authenticate to AWS ECS                               │  │
│  │ • Update ECS service with new image                     │  │
│  │ • Rolling deployment (0 downtime)                       │  │
│  │ • Wait for task health checks                           │  │
│  │ • Verify deployment status                              │  │
│  │                                                          │  │
│  │ Status: DEPLOYED ✓                                      │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
└──────────────────────────────┬─────────────────────────────────┘
                               │
                               ↓
┌──────────────────────────────────────────────────────────────────┐
│              AWS PRODUCTION ENVIRONMENT                          │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ ECS FARGATE CLUSTER (Compute)                            │  │
│  │                                                          │  │
│  │ Task Definition: red-team-toolkit:latest                │  │
│  │ ├── 2048 CPU, 4096 Memory                               │  │
│  │ ├── Container image from ECR                            │  │
│  │ ├── Environment variables (LOG_LEVEL, etc.)             │  │
│  │ ├── Secrets (DB_PASSWORD) from Secrets Manager          │  │
│  │ └── CloudWatch log group: /aws/ecs/red-team             │  │
│  │                                                          │  │
│  │ Running: 1+ task instances                              │  │
│  └──────────────────────────────────────────────────────────┘  │
│                  ↓           ↓            ↓                     │
│        ┌─────────────────────────────────────────┐              │
│        │  Data Persistence Tier                  │              │
│        │                                         │              │
│        ├─ RDS PostgreSQL 15 (findings DB)        │              │
│        │  ├── Automated backups (30 days)        │              │
│        │  ├── Multi-AZ failover                  │              │
│        │  └── Encryption at rest                 │              │
│        │                                         │              │
│        ├─ ElastiCache Redis 7 (cache/state)      │              │
│        │  ├── Automatic failover                 │              │
│        │  └── Encryption in transit              │              │
│        │                                         │              │
│        ├─ S3 Buckets (reports, logs)             │              │
│        │  ├── Versioning enabled                 │              │
│        │  ├── Encryption enabled                 │              │
│        │  └── Lifecycle policies (archive)       │              │
│        │                                         │              │
│        └─ Secrets Manager (credentials)          │              │
│           ├── Automatic rotation                 │              │
│           └── Encryption with KMS                │              │
│        │                                         │              │
│        └─────────────────────────────────────────┘              │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ MONITORING & LOGGING                                     │  │
│  │                                                          │  │
│  │ ├── CloudWatch Logs (application logs)                  │  │
│  │ ├── CloudWatch Metrics (execution time, findings)       │  │
│  │ ├── CloudWatch Alarms (errors, high latency)            │  │
│  │ ├── CloudTrail (API calls for audit)                    │  │
│  │ └── X-Ray (distributed tracing, optional)               │  │
│  │                                                          │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## SUMMARY: UML EXECUTION & TOOL INTEGRATION

**Total Complexity: HIGH but ORGANIZED**

- **8 Phases** spanning 16-17 weeks
- **18 Modules** with clear responsibilities
- **50+ Tools/Libraries** integrated systematically
- **3 Data Storage Layers** (PostgreSQL, Redis, S3)
- **Full CI/CD Pipeline** from GitHub to ECS
- **Complete Async/Concurrent Architecture** (3-5x performance boost)

**Key Success Factors:**

1. ✅ **Async-first design** (asyncio + aioboto3) = 10x faster recon
2. ✅ **Clear module separation** = testable, maintainable code
3. ✅ **PostgreSQL + Redis + S3** = robust data persistence
4. ✅ **Docker containerization** = reproducible environment
5. ✅ **GitHub Actions CI/CD** = automated testing + deployment
6. ✅ **Comprehensive testing** = 80%+ code coverage
7. ✅ **Professional documentation** = production-ready quality

**Timeline:**
- Weeks 1-2: Foundation
- Weeks 2-4: Core framework
- Weeks 4-6: Reconnaissance
- Weeks 6-10: Exploitation
- Weeks 10-12: Post-exploitation
- Weeks 12-14: Evasion
- Weeks 14-16: Testing
- Weeks 16-17: Release

**Expected Outcome:**
- Production-ready AWS red team toolkit
- 200-500+ GitHub stars potential
- Resume differentiator for FAANG roles
- Possible conference talk / academic publication

