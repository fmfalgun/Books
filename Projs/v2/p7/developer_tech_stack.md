# Project 7: Developer's Technical Stack & Resources Guide
## Complete Resource Allocation for AWS Red Team Toolkit Implementation

---

## EXECUTIVE SUMMARY

**Project Duration:** 4 months (16-17 weeks)  
**Team Size:** 1 developer (you) with optional external contributions  
**Tech Stack:** Python 3.11+, Docker, PostgreSQL/DynamoDB, asyncio, boto3  
**Deployment:** AWS EC2/ECS + GitHub Actions CI/CD  
**Target:** 18 modules, 80%+ code coverage, production-ready toolkit

---

## 1. PROGRAMMING LANGUAGES & FRAMEWORKS

### Primary Language: Python 3.11+

| Aspect | Specification | Justification |
|--------|---------------|---------------|
| **Language** | Python 3.11 (or 3.12) | AWS SDK (boto3) native; async/await support; rich ecosystem |
| **Version** | 3.11.x minimum | Latest async improvements, type hints, performance gains |
| **Package Manager** | Poetry (recommended) or pip | Poetry: dependency lock files, virtual env management |
| **Virtual Environment** | venv or Poetry | Isolation, reproducible builds, CI/CD compatibility |
| **Testing Framework** | pytest 7.4+ | Industry standard; fixtures; parametrization; coverage plugins |
| **Code Quality** | Black + isort + flake8 + mypy | Formatting, sorting, linting, type checking |
| **Documentation** | Sphinx + reStructuredText | Professional documentation generation |
| **Async Runtime** | asyncio (built-in) | Python's async event loop for concurrent AWS API calls |

### Core Libraries & Dependencies

#### AWS Integration
```
boto3==1.34.x              # AWS SDK for Python
aioboto3==12.x             # Async wrapper for boto3 (CRITICAL for performance)
botocore==1.34.x           # Boto3 dependency
```

**Why aioboto3?**  
- Standard boto3 uses blocking IO → serial execution (slow)
- aioboto3 uses async/await → concurrent execution (3-5x faster)
- Drop-in replacement for boto3 in async contexts
- Example: Enumerating 1000 resources → 2 hours (serial) vs 20 minutes (async)

#### Async & Concurrency
```
asyncio                    # Built-in async runtime
aiohttp==3.9.x            # Async HTTP client (for external API calls)
concurrent.futures        # Thread pool for mixed async/sync operations
```

**Performance Pattern:**
```python
# ❌ SLOW (serial enumeration)
regions = ['us-east-1', 'us-west-2', 'eu-west-1', ...]
for region in regions:
    client = boto3.client('ec2', region_name=region)
    instances = client.describe_instances()  # Waits for response
    # Total time: 5-10 seconds per region × 14+ regions = 70-140 seconds

# ✅ FAST (concurrent enumeration)
async def enum_all_regions():
    tasks = [enum_region(region) for region in regions]
    results = await asyncio.gather(*tasks)  # Parallel execution
    # Total time: 5-10 seconds (largest single request blocks)
```

#### Data Processing & Analysis
```
pandas==2.1.x              # Data aggregation, CSV export
numpy==1.24.x              # Numerical operations
PyYAML==6.0.x              # YAML parsing (attack scenarios)
```

#### Logging & Monitoring
```
loguru==0.7.x              # Structured logging (better than logging module)
python-json-logger==2.x    # JSON logs for parsing
prometheus-client==0.18.x  # Metrics collection (optional, for monitoring)
```

**Loguru Benefits:**
- Automatic log rotation
- Colored terminal output
- Structured logging (JSON)
- Async-safe logging
- File/handler management

#### CLI & Configuration
```
click==8.1.x               # Command-line interface (better than argparse)
python-dotenv==1.0.x       # Environment variable loading
pydantic==2.x              # Data validation (config, API responses)
typer==0.9.x               # Modern CLI (alternative to Click)
```

#### Security & Secrets
```
cryptography==41.x         # Encryption for sensitive data
python-cryptography==41.x  # Additional crypto utilities
pyyaml==6.0.x              # Secure YAML parsing
```

**Key Pattern - Secure Credential Handling:**
```python
from pydantic import SecretStr
from cryptography.fernet import Fernet

class AWSCredentials(BaseModel):
    access_key: SecretStr  # Auto-masked in logs
    secret_key: SecretStr
    
    def __repr__(self):
        return f"AWSCredentials(access_key={self.access_key}***)"
```

#### Testing & Mocking
```
pytest==7.4.x              # Test framework
pytest-asyncio==0.21.x     # Pytest plugin for async tests
pytest-cov==4.1.x          # Coverage reporting
moto==4.2.x                # Mock AWS services
responses==0.24.x          # Mock HTTP requests
faker==20.x                # Fake data generation
hypothesis==6.x            # Property-based testing
```

#### Reporting & Export
```
jinja2==3.1.x              # Template engine for HTML/PDF reports
matplotlib==3.8.x          # Charts and graphs
plotly==5.17.x             # Interactive visualizations (optional)
fpdf2==2.7.x               # PDF generation
openpyxl==3.1.x            # Excel export
```

#### Network Tools
```
nmap==0.0.1                # Python wrapper for nmap
python-nmap==0.7.x         # Alternative nmap wrapper
scapy==2.5.x               # Packet crafting (optional)
requests==2.31.x           # HTTP client
paramiko==3.3.x            # SSH client (for EC2 access)
pywinrm==0.4.x             # Windows RPC (for RDP)
```

#### Vulnerability & Exploit Modules
```
pwntools==4.x              # Exploit development
```

---

## 2. DATABASE & DATA STORAGE

### Primary Database: PostgreSQL 15+

| Use Case | Database | Justification |
|----------|----------|---------------|
| **Findings Storage** | PostgreSQL 15+ | ACID, JSON support, complex queries, scalability |
| **Real-time Metrics** | DynamoDB (AWS-native) | Low-latency key-value, serverless, auto-scaling |
| **Temporary State** | Redis (optional) | In-memory cache for session/execution state |
| **Document Storage** | S3 (AWS-native) | Reports, logs, large artifacts (not DB suitable) |
| **Time-Series** | DynamoDB + TTL | Attack timeline, event history with auto-cleanup |

### PostgreSQL 15+ Setup

```sql
-- Findings table
CREATE TABLE findings (
    id UUID PRIMARY KEY,
    toolkit_run_id UUID NOT NULL,
    module_name VARCHAR(255),
    severity ENUM('CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'INFO'),
    title VARCHAR(255),
    description TEXT,
    affected_resource VARCHAR(255),
    remediation TEXT,
    mitre_tactics JSONB,  -- MITRE ATT&CK mapping
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP,
    INDEX (toolkit_run_id, severity, module_name)
);

-- Execution metadata
CREATE TABLE executions (
    id UUID PRIMARY KEY,
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    status ENUM('RUNNING', 'SUCCESS', 'FAILED', 'PARTIAL'),
    modules_executed JSONB,
    total_findings INT,
    created_at TIMESTAMP
);

-- Evidence storage
CREATE TABLE evidence (
    id UUID PRIMARY KEY,
    finding_id UUID REFERENCES findings(id),
    evidence_type VARCHAR(50),  -- 'screenshot', 'api_response', 'log'
    data BYTEA,  -- Binary data
    created_at TIMESTAMP
);
```

**Why PostgreSQL?**
- ✅ JSONB columns for flexible finding storage
- ✅ Full-text search on finding descriptions
- ✅ Complex queries across multiple findings
- ✅ Transaction support for data consistency
- ✅ Open-source, widely deployed in enterprises
- ✅ Better than MongoDB for relational queries

**Python ORM: SQLAlchemy 2.0+**
```python
from sqlalchemy import create_engine, Column, String, DateTime, JSON
from sqlalchemy.orm import declarative_base, Session

Base = declarative_base()

class Finding(Base):
    __tablename__ = "findings"
    
    id: Mapped[str] = mapped_column(primary_key=True)
    title: Mapped[str]
    severity: Mapped[str]
    mitre_tactics: Mapped[dict] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
```

### DynamoDB (Optional Secondary DB)

**When to use DynamoDB:**
- ✅ Real-time metrics/telemetry during toolkit execution
- ✅ Auto-scaling attack state across Lambda functions
- ✅ Global tables for multi-region red team operations
- ✅ Already in AWS account (no external DB needed)

**DynamoDB vs PostgreSQL Tradeoff:**
```
PostgreSQL: Better for reporting, historical analysis, complex queries
DynamoDB:  Better for real-time metrics, event streaming, auto-scaling
Decision:  PostgreSQL (primary) + DynamoDB (metrics only)
```

### Caching Layer: Redis (Optional)

```python
# Use Redis for:
# 1. Session state during long-running attacks
# 2. Rate limit tracking (avoid AWS API throttling)
# 3. Credential rotation tokens
# 4. Temporary findings cache

import redis

cache = redis.Redis(host='localhost', port=6379, decode_responses=True)
cache.set('execution_state:run_123', json.dumps(state), ex=3600)
```

**Deployment Option:** AWS ElastiCache (managed Redis)

---

## 3. CONTAINERIZATION & ORCHESTRATION

### Containerization: Docker

#### Dockerfile (Development)
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    nmap \
    git \
    build-essential \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY pyproject.toml poetry.lock ./

# Install Python dependencies
RUN pip install poetry && \
    poetry install --no-dev

# Copy source code
COPY src/ ./src/
COPY tests/ ./tests/

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)"

ENTRYPOINT ["python", "-m", "src.orchestrator"]
CMD ["--help"]
```

#### Docker Compose (Local Development)
```yaml
version: '3.9'

services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: redteam
      POSTGRES_USER: developer
      POSTGRES_PASSWORD: dev_password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U developer"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  toolkit:
    build: .
    environment:
      AWS_PROFILE: redteam_test
      DATABASE_URL: postgresql://developer:dev_password@postgres:5432/redteam
      REDIS_URL: redis://redis:6379
      LOG_LEVEL: DEBUG
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    volumes:
      - ./src:/app/src
      - ./tests:/app/tests
      - ~/.aws:/root/.aws:ro  # AWS credentials
    ports:
      - "8000:8000"  # API server (optional)

volumes:
  postgres_data:
```

**Docker Advantages:**
- ✅ Reproducible environment (same on all machines)
- ✅ Isolation from host system
- ✅ Easy CI/CD integration
- ✅ Cloud deployment (ECS, EKS)
- ✅ Includes all dependencies (nmap, kali tools, etc.)

### Orchestration: Kubernetes (Optional for Large Deployments)

**When to use Kubernetes:**
- ✅ Running 100+ concurrent red team simulations
- ✅ Multi-team, multi-region operations
- ✅ Complex attack chains requiring service mesh
- ✅ High availability requirements

**When to use Docker Compose/ECS:**
- ✅ Single red team operator (YOU)
- ✅ Solo project or small team
- ✅ Simpler deployment (1-5 containers)
- ✅ Development and testing focus

**Recommendation:** Start with Docker Compose → Scale to ECS → Graduate to EKS if needed

#### ECS (Elastic Container Service) - Recommended for AWS

```yaml
# Simplified ECS task definition
{
  "family": "red-team-toolkit",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "2048",
  "memory": "4096",
  "containerDefinitions": [
    {
      "name": "toolkit",
      "image": "your-registry.dkr.ecr.us-east-1.amazonaws.com/red-team-toolkit:latest",
      "essential": true,
      "portMappings": [
        {"containerPort": 8000, "hostPort": 8000}
      ],
      "environment": [
        {"name": "LOG_LEVEL", "value": "INFO"}
      ],
      "secrets": [
        {"name": "DB_PASSWORD", "valueFrom": "arn:aws:secretsmanager:..."}
      ]
    }
  ]
}
```

---

## 4. DEVELOPMENT TOOLS & IDE SETUP

### IDE: VS Code (Recommended) or PyCharm Professional

#### VS Code Setup

```json
// .vscode/settings.json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "python.linting.mypyEnabled": true,
  "python.formatting.provider": "black",
  "python.formatting.blackArgs": ["--line-length=100"],
  "[python]": {
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.organizeImports": true
    }
  },
  "python.testing.pytestEnabled": true,
  "python.testing.pytestArgs": ["tests"],
  "editor.rulers": [100],
  "editor.wordWrap": "on"
}
```

#### Essential VS Code Extensions
1. **Python** (Microsoft) - IntelliSense, debugging, linting
2. **Pylance** - Advanced type checking
3. **Black Formatter** - Code formatting
4. **isort** - Import sorting
5. **Pytest** - Test runner integration
6. **Docker** - Docker file syntax highlighting
7. **AWS Toolkit** - AWS service integration
8. **GitLens** - Git visualization
9. **SQLTools** - Database client (PostgreSQL)
10. **Thunder Client** - API testing (alternative to Postman)

### Version Control: Git + GitHub

```bash
# Initialize repository
git init
git config user.email "your@email.com"
git config user.name "Your Name"

# Create .gitignore
cat > .gitignore << 'EOF'
.env
.env.local
.venv/
__pycache__/
*.pyc
*.pyo
*.egg-info/
dist/
build/
.pytest_cache/
.coverage
htmlcov/
.mypy_cache/
.idea/
.vscode/settings.json  # Personal settings
AWS_CREDENTIALS  # Never commit!
findings/
reports/
EOF
```

### Pre-commit Hooks (Prevent Bad Commits)

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: detect-private-key

  - repo: https://github.com/psf/black
    rev: 23.10.0
    hooks:
      - id: black
        language_version: python3.11

  - repo: https://github.com/PyCQA/isort
    rev: 5.12.0
    hooks:
      - id: isort

  - repo: https://github.com/PyCQA/flake8
    rev: 6.1.0
    hooks:
      - id: flake8
        args: ['--max-line-length=100']

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.6.1
    hooks:
      - id: mypy
        additional_dependencies: ['types-all']
```

---

## 5. SECURITY & PENETRATION TESTING TOOLS

### System-Level Tools (Install in Docker/System)

| Tool | Purpose | Version | Installation |
|------|---------|---------|--------------|
| **nmap** | Network scanning, service discovery | 7.93+ | `apt install nmap` |
| **masscan** | Fast port scanning (parallel) | 1.3+ | `apt install masscan` |
| **metasploit** | Exploitation framework | 6.3+ | Pre-installed in Kali image |
| **wireshark** | Packet analysis | 4.0+ | `apt install tshark` (CLI version) |
| **tshark** | CLI Wireshark | 4.0+ | `apt install tshark` |
| **curl/wget** | HTTP requests | latest | Pre-installed |
| **jq** | JSON parsing | 1.6+ | `apt install jq` |
| **aws-cli** | AWS command-line | 2.x | `pip install awscli-v2` |
| **ssm-session-manager** | AWS Systems Manager | latest | Via aws-cli |

### Python-Based Security Tools (pip install)

```
# AWS-specific
pacu==master              # AWS exploitation framework (integrate)
pmapper==v2.x             # AWS IAM privilege escalation mapping
cloudmapper==main         # AWS infrastructure visualization
aws-recon==latest         # AWS resource enumeration
prowler-cloud==main       # AWS security auditing (integrate)
stratus-red-team==latest  # AWS attack simulation

# General penetration testing
pwntools==4.x             # Exploit development toolkit
scapy==2.5.x              # Packet manipulation
impacket==0.11.x          # Network protocol implementation
paramiko==3.3.x           # SSH client/server
fabric==3.2.x             # Remote execution
requests==2.31.x          # HTTP library

# Reverse engineering & analysis
pefile==2023.x            # PE file analysis
capstone==5.x             # Disassembly framework
keystone==0.9.x           # Assembler framework
unicorn==2.1.x            # CPU emulation
pyelftools==0.29.x        # ELF binary analysis
```

### Docker Image with Security Tools

```dockerfile
# Use security-focused base image
FROM kalilinux/kali-rolling

# Install security tools
RUN apt-get update && apt-get install -y \
    python3-pip \
    nmap \
    masscan \
    metasploit-framework \
    wireshark \
    tshark \
    aircrack-ng \
    hashcat \
    john \
    sqlmap \
    nikto \
    && rm -rf /var/lib/apt/lists/*

# Install Python 3.11
RUN apt-get update && apt-get install -y python3.11 python3.11-venv

# Copy toolkit
COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt
```

---

## 6. CI/CD PIPELINE & AUTOMATION

### GitHub Actions Workflow

```yaml
# .github/workflows/test-build-deploy.yml
name: Test, Build, Deploy

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_DB: test_redteam
          POSTGRES_USER: test_user
          POSTGRES_PASSWORD: test_pass
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python 3.11
        uses: actions/setup-python@v4
        with:
          python-version: 3.11

      - name: Cache dependencies
        uses: actions/cache@v3
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('**/pyproject.toml') }}

      - name: Install dependencies
        run: |
          pip install poetry
          poetry install

      - name: Lint with Black
        run: black --check src/ tests/

      - name: Type check with mypy
        run: mypy src/

      - name: Run tests with pytest
        run: |
          poetry run pytest tests/ \
            --cov=src \
            --cov-report=xml \
            --cov-report=html

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage.xml

      - name: Security scan with bandit
        run: bandit -r src/

      - name: SAST scan with semgrep
        run: |
          pip install semgrep
          semgrep --config=p/security-audit src/

  build:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'

    steps:
      - uses: actions/checkout@v3

      - name: Set up Docker buildx
        uses: docker/setup-buildx-action@v2

      - name: Login to ECR
        run: |
          aws ecr get-login-password --region us-east-1 | \
            docker login --username AWS --password-stdin ${{ secrets.ECR_REGISTRY }}

      - name: Build and push Docker image
        uses: docker/build-push-action@v4
        with:
          context: .
          push: true
          tags: |
            ${{ secrets.ECR_REGISTRY }}/red-team-toolkit:latest
            ${{ secrets.ECR_REGISTRY }}/red-team-toolkit:${{ github.sha }}

  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'

    steps:
      - uses: actions/checkout@v3

      - name: Deploy to AWS ECS
        run: |
          aws ecs update-service \
            --cluster red-team \
            --service toolkit \
            --force-new-deployment \
            --region us-east-1
```

### Local Development Workflow

```bash
# Setup
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
poetry install

# Run tests
pytest tests/ --cov=src

# Format code
black src/ tests/
isort src/ tests/

# Type check
mypy src/

# Run linter
flake8 src/ tests/

# Build Docker image
docker build -t red-team-toolkit:latest .

# Run locally
docker-compose up
```

---

## 7. MONITORING & LOGGING INFRASTRUCTURE

### Logging Stack

#### Option A: AWS CloudWatch (Recommended)

```python
import logging
import watchtower

# Configure CloudWatch logging
handler = watchtower.CloudWatchLogHandler(
    log_group='/aws/redteam/toolkit',
    stream_name='execution_logs'
)
logger = logging.getLogger(__name__)
logger.addHandler(handler)

# Usage
logger.info("Attack started", extra={
    'execution_id': run_id,
    'module': 'iam_privesc_module',
    'severity': 'HIGH'
})
```

**Benefits:**
- ✅ Centralized logging in AWS
- ✅ Full-text search
- ✅ Metrics and alarms
- ✅ Integration with Splunk/DataDog
- ✅ Automatic retention policies

#### Option B: ELK Stack (Local/Self-Hosted)

```yaml
# docker-compose-elk.yml
version: '3.9'

services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.10.0
    environment:
      - xpack.security.enabled=false
      - discovery.type=single-node
    ports:
      - "9200:9200"
    volumes:
      - elasticsearch_data:/usr/share/elasticsearch/data

  logstash:
    image: docker.elastic.co/logstash/logstash:8.10.0
    ports:
      - "5000:5000/udp"
    config:
      input:
        udp:
          port: 5000
          codec: json
      output:
        elasticsearch:
          hosts: ["elasticsearch:9200"]

  kibana:
    image: docker.elastic.co/kibana/kibana:8.10.0
    ports:
      - "5601:5601"

volumes:
  elasticsearch_data:
```

### Metrics & Monitoring

```python
# prometheus metrics
from prometheus_client import Counter, Histogram, Gauge

attack_attempts = Counter(
    'redteam_attack_attempts_total',
    'Total attack attempts',
    ['module', 'status']
)

attack_duration = Histogram(
    'redteam_attack_duration_seconds',
    'Attack execution time',
    ['module']
)

findings_discovered = Gauge(
    'redteam_findings_total',
    'Total findings discovered',
    ['severity']
)
```

---

## 8. DEPLOYMENT ARCHITECTURE

### AWS Infrastructure Stack

```
┌─────────────────────────────────────────────────────────┐
│                     AWS Account                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │         ECS / Fargate Cluster                    │  │
│  │  (Toolkit execution environment)                 │  │
│  └──────────────────────────────────────────────────┘  │
│           ↓                      ↓                      │
│  ┌──────────────────┐    ┌──────────────────┐          │
│  │ RDS PostgreSQL   │    │ ElastiCache Redis│          │
│  │ (Findings DB)    │    │ (Session cache)  │          │
│  └──────────────────┘    └──────────────────┘          │
│           ↓                      ↓                      │
│  ┌──────────────────────────────────────────────────┐  │
│  │    CloudWatch Logs / Metrics                     │  │
│  │    (Logging & monitoring)                        │  │
│  └──────────────────────────────────────────────────┘  │
│                                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │  S3 Buckets                                      │  │
│  │  - Reports storage                               │  │
│  │  - Log archive                                   │  │
│  │  - Evidence storage                              │  │
│  └──────────────────────────────────────────────────┘  │
│                                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Secrets Manager                                 │  │
│  │  - AWS credentials rotation                      │  │
│  │  - Database passwords                            │  │
│  │  - API keys                                      │  │
│  └──────────────────────────────────────────────────┘  │
│                                                         │
└─────────────────────────────────────────────────────────┘
         ↓
┌──────────────────────────────────────────────────────┐
│  GitHub Actions CI/CD Pipeline                      │
│  - Test → Build → Push to ECR → Deploy to ECS      │
└──────────────────────────────────────────────────────┘
```

### CloudFormation Template (Infrastructure as Code)

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: Red Team Toolkit Infrastructure

Resources:
  # RDS PostgreSQL
  RedTeamDB:
    Type: AWS::RDS::DBInstance
    Properties:
      DBInstanceIdentifier: redteam-findings
      Engine: postgres
      EngineVersion: 15.4
      DBInstanceClass: db.t3.micro  # Development
      AllocatedStorage: 100
      StorageType: gp3
      MasterUsername: admin
      MasterUserPassword: !Sub '{{resolve:secretsmanager:redteam/db/password}}'
      BackupRetentionPeriod: 30
      PreferredBackupWindow: 03:00-04:00
      EnableCloudwatchLogsExports:
        - postgresql
      VpcSecurityGroupIds:
        - !Ref DBSecurityGroup

  # ElastiCache Redis
  RedTeamCache:
    Type: AWS::ElastiCache::CacheCluster
    Properties:
      CacheNodeType: cache.t3.micro
      Engine: redis
      NumCacheNodes: 1
      Port: 6379
      VpcSecurityGroupIds:
        - !Ref CacheSecurityGroup

  # ECS Cluster
  RedTeamCluster:
    Type: AWS::ECS::Cluster
    Properties:
      ClusterName: red-team

  # S3 Bucket for Reports
  ReportsBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Sub 'redteam-reports-${AWS::AccountId}'
      VersioningConfiguration:
        Status: Enabled
      ServerSideEncryptionConfiguration:
        - ServerSideEncryptionByDefault:
            SSEAlgorithm: AES256
      PublicAccessBlockConfiguration:
        BlockPublicAcls: true
        BlockPublicPolicy: true
        IgnorePublicAcls: true
        RestrictPublicBuckets: true
```

---

## 9. DEVELOPMENT WORKFLOW

### Project Structure

```
red-team-toolkit/
├── src/
│   ├── __init__.py
│   ├── orchestrator.py          # Main entry point
│   ├── config.py                # Configuration management
│   ├── models/
│   │   ├── finding.py           # Finding data model
│   │   ├── execution.py         # Execution metadata
│   │   └── aws_resource.py      # AWS resource model
│   ├── modules/
│   │   ├── __init__.py
│   │   ├── base_module.py       # Abstract base module
│   │   ├── core/
│   │   │   ├── orchestrator.py
│   │   │   ├── credential_manager.py
│   │   │   └── logging_system.py
│   │   ├── reconnaissance/
│   │   │   ├── aws_enum_module.py
│   │   │   ├── iam_enum_module.py
│   │   │   └── ...
│   │   ├── exploitation/
│   │   │   ├── ec2_exploit_module.py
│   │   │   ├── s3_exploit_module.py
│   │   │   └── ...
│   │   ├── post_exploitation/
│   │   │   ├── persistence_module.py
│   │   │   └── ...
│   │   └── evasion/
│   │       ├── guardduty_evasion_module.py
│   │       └── ...
│   ├── database/
│   │   ├── models.py            # SQLAlchemy ORM
│   │   ├── connection.py        # DB connection management
│   │   └── migrations/          # Alembic migrations
│   ├── reporting/
│   │   ├── report_generator.py
│   │   ├── templates/
│   │   │   ├── executive_summary.html.j2
│   │   │   └── technical_report.html.j2
│   │   └── exporters.py         # PDF, CSV, JSON
│   ├── utils/
│   │   ├── aws_utils.py         # AWS helper functions
│   │   ├── crypto.py            # Encryption utilities
│   │   └── validators.py        # Input validation
│   └── exceptions.py            # Custom exceptions
├── tests/
│   ├── __init__.py
│   ├── conftest.py              # Pytest fixtures
│   ├── unit/
│   │   ├── test_models.py
│   │   ├── test_modules.py
│   │   └── ...
│   ├── integration/
│   │   ├── test_aws_enum.py
│   │   ├── test_exploitation_chain.py
│   │   └── ...
│   └── fixtures/
│       ├── mock_aws_responses.py
│       └── test_data.py
├── docker/
│   ├── Dockerfile
│   ├── Dockerfile.dev
│   └── requirements-docker.txt
├── scripts/
│   ├── setup_db.py
│   ├── migrate_db.py
│   └── generate_reports.py
├── docs/
│   ├── index.md
│   ├── installation.md
│   ├── usage.md
│   ├── module_development.md
│   └── api_reference.md
├── config/
│   ├── config.yaml              # Main config
│   ├── attack_scenarios.yaml    # Attack definitions
│   └── mitre_mapping.yaml       # MITRE ATT&CK map
├── .github/
│   └── workflows/
│       ├── test.yml
│       ├── build.yml
│       └── deploy.yml
├── pyproject.toml              # Poetry dependencies
├── pytest.ini                  # Pytest config
├── .pre-commit-config.yaml     # Pre-commit hooks
├── Dockerfile                  # Production image
├── docker-compose.yml          # Local dev stack
├── README.md
├── LICENSE
└── .gitignore
```

---

## 10. TOTAL RESOURCE ALLOCATION

### Software/Tools Summary

| Category | Tools/Versions | Cost | Installation |
|----------|---|------|---|
| **Languages** | Python 3.11+ | Free | apt/brew |
| **Databases** | PostgreSQL 15, Redis 7 | Free | Docker/managed AWS |
| **Containers** | Docker, Docker Compose | Free | docker.com |
| **AWS Services** | RDS, ECS, CloudWatch, S3 | $50-200/month | AWS account |
| **CI/CD** | GitHub Actions | Free (public repo) | Built-in GitHub |
| **IDE** | VS Code + Extensions | Free | code.visualstudio.com |
| **Security Tools** | Nmap, Metasploit, AWS CLI | Free | Docker image |
| **Monitoring** | CloudWatch or ELK | $20-100/month | AWS or Docker |
| **Version Control** | GitHub | Free | github.com |
| **Total First Year** | - | $500-2000 | - |

### Hardware Requirements

| Component | Minimum | Recommended | Notes |
|-----------|---------|------------|-------|
| **CPU** | 4 cores | 8+ cores | Async tasks benefit from parallelism |
| **RAM** | 8 GB | 16+ GB | Docker + PostgreSQL + Redis |
| **Disk** | 50 GB | 200+ GB | Docker images, reports, artifacts |
| **Network** | 10 Mbps | 100+ Mbps | AWS API calls + downloads |

### Timeline & Phases

| Phase | Duration | Key Setup |
|-------|----------|-----------|
| **Phase 1: Environment** | 3-5 days | Python, Docker, PostgreSQL, GitHub |
| **Phase 2: Core Framework** | 2-3 weeks | Orchestrator, DB, logging, CI/CD |
| **Phase 3-6: Development** | 2-3 months | Module implementation |
| **Phase 7-8: Testing & Deployment** | 2-3 weeks | Tests, ECS, production hardening |

---

## 11. QUICK START COMMAND SEQUENCE

```bash
# 1. Clone and setup
git clone <your-repo>
cd red-team-toolkit
python -m venv .venv
source .venv/bin/activate
pip install poetry
poetry install

# 2. Setup local environment
cp .env.example .env
docker-compose up -d  # Start PostgreSQL, Redis

# 3. Initialize database
poetry run python scripts/setup_db.py

# 4. Run tests
poetry run pytest tests/ --cov=src

# 5. Run toolkit in development
poetry run python -m src.orchestrator --help

# 6. Build Docker image
docker build -t red-team-toolkit:latest .

# 7. Push to AWS ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account>.dkr.ecr.us-east-1.amazonaws.com
docker tag red-team-toolkit:latest <account>.dkr.ecr.us-east-1.amazonaws.com/red-team-toolkit:latest
docker push <account>.dkr.ecr.us-east-1.amazonaws.com/red-team-toolkit:latest

# 8. Deploy to ECS
aws ecs update-service --cluster red-team --service toolkit --force-new-deployment
```

---

## 12. RECOMMENDED TECH STACK SUMMARY

### Final Tech Stack Selection

```
LANGUAGE:           Python 3.11+ (primary)
ASYNC:              asyncio + aioboto3 (concurrent AWS calls)
DATABASE:           PostgreSQL 15 (findings) + DynamoDB (optional metrics)
ORM:                SQLAlchemy 2.0+
CACHE:              Redis 7 (via ElastiCache)
CONTAINERIZATION:   Docker + Docker Compose
ORCHESTRATION:      ECS Fargate (not Kubernetes - overkill for solo dev)
CI/CD:              GitHub Actions (free, integrated with GitHub)
MONITORING:         CloudWatch (AWS-native) + optional ELK
TESTING:            pytest + pytest-asyncio + moto
CODE QUALITY:       Black + isort + mypy + flake8
IDE:                VS Code + Python extensions
VERSION CONTROL:    Git + GitHub
DOCUMENTATION:      Sphinx + markdown
SECURITY TOOLS:     Docker image with nmap, metasploit, aws-cli
SECRETS MGMT:       AWS Secrets Manager + python-dotenv
```

### Why These Choices?

1. **Python**: AWS SDK native, async-capable, rich security library ecosystem
2. **asyncio + aioboto3**: 3-5x faster than serial boto3 calls (CRITICAL for reconnaissance)
3. **PostgreSQL**: Better than MongoDB for findings (relational queries, ACID)
4. **Docker**: Reproducible environment, includes security tools, cloud-ready
5. **ECS**: Simpler than Kubernetes for solo dev, still enterprise-grade
6. **GitHub Actions**: Free for public repos, integrated with GitHub, sufficient for CI/CD
7. **CloudWatch**: AWS-native, no additional costs, integrated with ECS logs

---

## CRITICAL PERFORMANCE OPTIMIZATION

### Async/Concurrent Execution Pattern

```python
# ❌ SLOW: 14 regions × 5-10 seconds each = 70-140 seconds
for region in REGIONS:
    ec2 = boto3.client('ec2', region_name=region)
    instances = ec2.describe_instances()  # Blocking call

# ✅ FAST: Max(individual requests) = 5-10 seconds total
async def scan_all_regions():
    tasks = [enum_region(region) for region in REGIONS]
    results = await asyncio.gather(*tasks)  # Concurrent execution
```

**Expected Performance Gains:**
- Account enumeration: 2 hours → 15 minutes (8x speedup)
- IAM analysis: 30 minutes → 3 minutes (10x speedup)
- Full reconnaissance: 8 hours → 45 minutes (10x speedup)

---

**Total Development Resource Summary:**  
✅ **Programming Time**: 4 months (full-time equivalent)  
✅ **Infrastructure Cost**: $500-2000/year  
✅ **Tools & Dependencies**: All open-source or AWS-managed  
✅ **Team Size**: 1 developer (scalable via Git for collaboration)  

You're ready to start building! Let me know if you need clarification on any tool or resource. 🚀

