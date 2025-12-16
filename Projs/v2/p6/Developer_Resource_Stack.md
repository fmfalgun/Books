# Project 6: Developer Resource & Tool Stack
## Complete Developer Guide from Development to Deployment

---

## TABLE OF CONTENTS
1. [Programming Languages & Runtimes](#1-programming-languages--runtimes)
2. [Cryptography & Security Libraries](#2-cryptography--security-libraries)
3. [Blockchain Development Tools](#3-blockchain-development-tools)
4. [Databases](#4-databases)
5. [Containerization & Orchestration](#5-containerization--orchestration)
6. [Testing & Quality Assurance](#6-testing--quality-assurance)
7. [Monitoring & Logging](#7-monitoring--logging)
8. [Network Security Tools](#8-network-security-tools)
9. [CI/CD & Deployment](#9-cicd--deployment)
10. [Development Environment Setup](#10-development-environment-setup)
11. [Hardware Requirements](#11-hardware-requirements)

---

## 1. PROGRAMMING LANGUAGES & RUNTIMES

### 1.1 PYTHON (Primary Language - 70% of Project)

| Aspect | Details |
|--------|---------|
| **Version** | Python 3.10+ (3.12 recommended) |
| **Primary Uses** | Kerberos core, Ethereum adapter, evaluation framework, VANET simulation integration |
| **Installation** | `sudo apt install python3.12 python3.12-venv python3.12-dev` (Linux) or brew install python@3.12 (macOS) |
| **Virtual Environment** | `python3.12 -m venv venv && source venv/bin/activate` |
| **Package Manager** | pip 24.0+ (included with Python 3.10+) |
| **Dependency Management** | `pip freeze > requirements.txt` for reproducibility |

**Key Python Packages for Project 6:**

```
Core Cryptography:
  - cryptography==46.0.0+        (PyCA - HIGH SECURITY)
  - pycryptodome==3.23.0+        (AES, RSA, HKDF, HPKE support)
  - PyNaCl==1.6.1+               (libsodium wrapper - Ed25519)

Kerberos Implementation:
  - python-kerberos==1.3.0        (KRB5 bindings, optional)
  - pyasn1==0.4.8+                (ASN.1 parsing for Kerberos tickets)
  - six==1.16.0+                  (Python 2/3 compatibility)

Ethereum/Web3:
  - web3.py==7.0.0+               (Ethereum JSON-RPC client)
  - eth-account==0.13.0+          (Account management)
  - eth-keys==0.6.1+              (Key derivation)
  - eth-utils==4.2.0+             (Ethereum utilities)
  - rlp==3.1.0+                   (RLP encoding)

Smart Contract Development:
  - brownie==1.21.0+              (Python framework for Solidity)
  - solcx==0.1.35+                (Solidity compiler)

Hyperledger Fabric:
  - fabric-sdk-py==0.8.1+         (Fabric Python SDK)
  - grpcio==1.66.0+               (gRPC for Fabric communication)
  - protobuf==5.27.0+             (Protocol Buffers)

Testing & QA:
  - pytest==8.0.0+                (Unit testing)
  - pytest-cov==5.0.0+            (Code coverage)
  - pytest-asyncio==0.24.0+       (Async testing)
  - hypothesis==6.100.0+          (Property-based testing)
  - paramiko==3.4.0+              (SSH for remote testing)

Performance & Profiling:
  - locust==2.20.0+               (Load testing)
  - memory-profiler==0.61.0+      (Memory profiling)
  - py-spy==0.3.14+               (CPU profiling)
  - psutil==5.9.8+                (System resource monitoring)

Data Processing:
  - pandas==2.2.0+                (Data analysis)
  - numpy==1.26.0+                (Numerical computing)
  - matplotlib==3.9.0+            (Visualization)
  - seaborn==0.13.0+              (Statistical visualization)

Utilities:
  - requests==2.32.0+             (HTTP client)
  - python-dotenv==1.0.0+         (Environment variables)
  - colorama==0.4.6+              (Colored terminal output)
  - tqdm==4.66.0+                 (Progress bars)
```

**installation:**
```bash
# Create virtual environment
python3.12 -m venv project6_env
source project6_env/bin/activate

# Install core dependencies
pip install --upgrade pip setuptools wheel
pip install cryptography==46.0.0 pycryptodome==3.23.0 PyNaCl==1.6.1

# Install blockchain dependencies
pip install web3.py==7.0.0 eth-account==0.13.0 brownie==1.21.0

# Install testing tools
pip install pytest==8.0.0 pytest-cov==5.0.0 locust==2.20.0

# Install remaining packages
pip freeze > requirements.txt
```

---

### 1.2 GO (Secondary Language - 20% of Project)

| Aspect | Details |
|--------|---------|
| **Version** | Go 1.22+ (1.23 latest) |
| **Primary Uses** | Hyperledger Fabric chaincode, performance-critical modules |
| **Installation** | Download from https://golang.org/dl or `apt install golang-1.22` |
| **GOPATH** | Set to `$HOME/go` or project-specific path |
| **Module Mode** | Always use `go mod init` for dependency management |

**Key Go Packages for Project 6:**

```
Hyperledger Fabric:
  - github.com/hyperledger/fabric-contract-api-go/v2  (Chaincode framework)
  - github.com/hyperledger/fabric-chaincode-go/v2      (Chaincode base)

Cryptography:
  - crypto/aes, crypto/sha256, crypto/hmac            (Standard library)
  - golang.org/x/crypto/sha3                           (KECCAK-256 for Ethereum)
  - crypto/ecdsa                                       (Elliptic curve crypto)

Blockchain Interaction:
  - github.com/ethereum/go-ethereum                    (Go Ethereum - Geth)
  - github.com/ethereum/go-ethereum/crypto            (Ethereum crypto)

JSON-RPC & Web:
  - encoding/json                                      (Standard library)
  - net/http                                           (HTTP server/client)

Testing:
  - testing                                            (Standard library)
  - github.com/stretchr/testify                        (Assertions)

Logging:
  - log                                                (Standard library)
  - github.com/sirupsen/logrus                         (Advanced logging)

CLI:
  - flag, cobra                                        (CLI frameworks)
```

**go.mod template:**
```go
module blockchain-enhanced-kerberos

go 1.23

require (
  github.com/hyperledger/fabric-contract-api-go/v2 v2.5.0
  github.com/ethereum/go-ethereum v1.15.0
  github.com/stretchr/testify v1.10.0
)
```

---

### 1.3 SOLIDITY (Smart Contracts - 5% of Project)

| Aspect | Details |
|--------|---------|
| **Version** | Solidity 0.8.19+ (0.8.26 latest) |
| **Compiler** | solc or solcx (Python wrapper) |
| **IDE** | Remix IDE (online) or VS Code + Hardhat/Foundry (offline) |
| **Primary Uses** | Ethereum smart contract for authentication verification |

**Solidity Contract Structure:**

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract AuthenticationVerifier {
    // Kerberos authenticator structure
    struct Authenticator {
        bytes32 hashValue;
        uint256 timestamp;
        address submittedBy;
        bool verified;
    }
    
    // State variables
    mapping(bytes32 => Authenticator) public authenticators;
    address public owner;
    
    // Events for verification log
    event AuthenticatorSubmitted(bytes32 indexed hash, uint256 timestamp);
    event VerificationComplete(bytes32 indexed hash, bool verified);
    
    // Constructor
    constructor() {
        owner = msg.sender;
    }
    
    // Core functions (to be implemented)
    function submitAuthenticator(bytes32 hash) external payable { }
    function verifyAuthenticator(bytes32 hash) external view returns (bool) { }
    function getAuthenticatorLog(bytes32 hash) external view returns (Authenticator) { }
}
```

---

### 1.4 SHELL/BASH (Deployment Scripts - 3% of Project)

| Aspect | Details |
|--------|---------|
| **Uses** | Deployment automation, environment setup, Docker orchestration |
| **Shebang** | `#!/bin/bash` for bash-specific features, `#!/bin/sh` for POSIX |
| **Best Practices** | Always use `set -e` for error handling, quote variables, use functions |

**Example deployment script structure:**
```bash
#!/bin/bash
set -euo pipefail

# Configuration
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENVIRONMENT="${ENVIRONMENT:-development}"
LOG_DIR="${PROJECT_ROOT}/logs"

# Logging functions
log_info() { echo "[INFO] $(date '+%Y-%m-%d %H:%M:%S') $*" | tee -a "${LOG_DIR}/deploy.log"; }
log_error() { echo "[ERROR] $(date '+%Y-%m-%d %H:%M:%S') $*" | tee -a "${LOG_DIR}/deploy.log"; exit 1; }

# Main deployment functions
setup_environment() {
    log_info "Setting up environment: $ENVIRONMENT"
    mkdir -p "${LOG_DIR}"
    source "${PROJECT_ROOT}/.env.${ENVIRONMENT}"
}

build_docker_images() {
    log_info "Building Docker images..."
    docker-compose build --no-cache
}

# Main execution
main() {
    setup_environment
    build_docker_images
    log_info "Deployment complete"
}

main "$@"
```

---

## 2. CRYPTOGRAPHY & SECURITY LIBRARIES

### 2.1 CRYPTOGRAPHY (PyCA - PRIMARY)

| Feature | Details |
|---------|---------|
| **Library** | `cryptography` (PyCA/cryptography) |
| **Current Version** | 46.0.0+ (updated 2025) |
| **Repository** | https://github.com/pyca/cryptography |
| **Documentation** | https://cryptography.io |
| **Security Audits** | Regularly audited by Trail of Bits |

**Supported Algorithms:**

```python
# Symmetric Encryption
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
aes_cipher = Cipher(algorithms.AES(key), modes.CBC(iv))  # AES-128/256-CBC
chacha_cipher = Cipher(algorithms.ChaCha20(key, nonce))  # ChaCha20-Poly1305

# Asymmetric Encryption
from cryptography.hazmat.primitives.asymmetric import rsa, ec, ed25519
rsa_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)  # RSA-2048
ec_key = ec.generate_private_key(ec.SECP256R1())  # ECDSA

# Hash Functions
from cryptography.hazmat.primitives import hashes
h = hashes.Hash(hashes.SHA256())  # SHA-256
h = hashes.Hash(hashes.BLAKE2b(64))  # BLAKE2b

# HMAC & MACs
from cryptography.hazmat.primitives import hmac
h = hmac.HMAC(key, hashes.SHA256())  # HMAC-SHA256

# Key Derivation
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
hkdf = HKDF(algorithm=hashes.SHA256(), length=32, salt=None, info=b'')  # RFC 5869
pbkdf2 = PBKDF2(hashes.SHA256(), salt, iterations=480000, length=32)  # Argon2-like

# X.509 Certificate Handling
from cryptography import x509
cert = x509.load_pem_x509_certificate(cert_data)  # Load certificates
builder = x509.CertificateBuilder()  # Build self-signed certs

# High-Level Encryption (Fernet)
from cryptography.fernet import Fernet
f = Fernet(key)
encrypted = f.encrypt(data)
decrypted = f.decrypt(encrypted)
```

**Installation & Verification:**
```bash
pip install cryptography==46.0.0
python -c "from cryptography.hazmat.primitives.ciphers import algorithms; print('✓ Cryptography installed correctly')"
```

---

### 2.2 PYCRYPTODOME (ALTERNATIVE - HIGH PERFORMANCE)

| Feature | Details |
|---------|---------|
| **Library** | `pycryptodome` (modern replacement for PyCrypto) |
| **Current Version** | 3.23.0+ (May 2025 - with HPKE support) |
| **New Features** | HPKE (RFC 9180), Key Wrap (NIST SP 800-38F) |
| **Performance** | ~30% faster than cryptography for some operations |

**Usage:**
```python
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256, HMAC
from Crypto.Protocol.KDF import HKDF
from Crypto.Random import get_random_bytes

# AES Encryption
key = get_random_bytes(32)
cipher = AES.new(key, AES.MODE_GCM)
ciphertext, tag = cipher.encrypt_and_digest(plaintext)

# RSA Key Generation
key = RSA.generate(2048)
public_key = key.publickey()
cipher = PKCS1_OAEP.new(public_key)
encrypted = cipher.encrypt(data)

# HKDF Key Derivation (NEW in 3.23.0)
derived_key = HKDF(master_secret, key_len=32, salt=None, hashmod=SHA256, info=b'')
```

---

### 2.3 PYNACL (LIBSODIUM WRAPPER)

| Feature | Details |
|---------|---------|
| **Library** | `PyNaCl` (wrapper around libsodium) |
| **Current Version** | 1.6.1+ (2025) |
| **Strength** | Misuse-resistant high-level functions |
| **Key Algorithms** | Ed25519 signatures, Curve25519 key agreement, ChaCha20-Poly1305 |

**Usage for Kerberos Signing:**
```python
import nacl.signing
import nacl.public
import nacl.secret
import nacl.utils

# Sign Kerberos messages with Ed25519
signing_key = nacl.signing.SigningKey.generate()
verify_key = signing_key.verify_key
signed_message = signing_key.sign(message)
verified_message = verify_key.verify(signed_message)

# Authenticated encryption (for session keys)
secret_box = nacl.secret.SecretBox(key)
encrypted = secret_box.encrypt(plaintext)
decrypted = secret_box.decrypt(encrypted)

# Ephemeral key exchange
private_key = nacl.public.PrivateKey.generate()
public_key = private_key.public_key
box = nacl.public.Box(private_key, peer_public_key)
```

---

## 3. BLOCKCHAIN DEVELOPMENT TOOLS

### 3.1 ETHEREUM DEVELOPMENT STACK

#### A. HARDHAT (Comprehensive Environment)

| Feature | Details |
|---------|---------|
| **Framework** | JavaScript/TypeScript-based Ethereum development environment |
| **Website** | https://hardhat.org |
| **Installation** | `npm install --save-dev hardhat` |
| **Key Features** | Local blockchain (Hardhat Network), testing, debugging, plugin ecosystem |
| **Best For** | Complex dApps, full Ethereum ecosystem integration |

**Hardhat Setup:**
```bash
# Initialize Hardhat project
npm init -y
npm install --save-dev hardhat @nomicfoundation/hardhat-toolbox
npx hardhat init

# Hardhat Network (local blockchain) - starts automatically
npx hardhat node  # In separate terminal

# Deploy smart contract
npx hardhat run scripts/deploy.js --network localhost

# Run tests
npx hardhat test

# Compile contracts
npx hardhat compile
```

**Hardhat Configuration (hardhat.config.js):**
```javascript
require("@nomicfoundation/hardhat-toolbox");

module.exports = {
  solidity: "0.8.19",
  networks: {
    localhost: {
      url: "http://127.0.0.1:8545"
    },
    sepolia: {
      url: `https://sepolia.infura.io/v3/${process.env.INFURA_KEY}`,
      accounts: [process.env.PRIVATE_KEY]
    },
    mainnet: {
      url: `https://mainnet.infura.io/v3/${process.env.INFURA_KEY}`,
      accounts: [process.env.PRIVATE_KEY]
    }
  }
};
```

---

#### B. FOUNDRY (Solidity-Native)

| Feature | Details |
|---------|---------|
| **Framework** | Pure Solidity development toolkit (Rust-based) |
| **Website** | https://getfoundry.sh |
| **Installation** | `curl -L https://foundry.paradigm.xyz \| bash && foundryup` |
| **Key Features** | Forge (testing), Cast (CLI), Anvil (local chain), Chisel (REPL) |
| **Speed** | 10-100x faster than Hardhat for Solidity-only projects |
| **Best For** | Smart contract development, rapid iteration, performance-critical code |

**Foundry Setup:**
```bash
# Initialize Foundry project
forge init blockchain-enhanced-kerberos
cd blockchain-enhanced-kerberos

# Start local blockchain (Anvil - Rust-based alternative to Ganache)
anvil --host 0.0.0.0 --port 8545

# Deploy smart contract
forge create src/AuthenticationVerifier.sol:AuthenticationVerifier \
  --rpc-url http://localhost:8545 \
  --private-key $PRIVATE_KEY

# Run tests
forge test --match "test.*" -v

# Gas profiling
forge test --gas-report

# Solidity REPL (Chisel)
chisel  # Interactive Solidity environment
```

**Foundry.toml Configuration:**
```toml
[profile.default]
src = 'src'
out = 'out'
libs = ['lib']
solc = "0.8.19"
optimizer = true
optimizer_runs = 200

[profile.test]
optimizer_runs = 100

[rpc_endpoints]
sepolia = "https://sepolia.infura.io/v3/${INFURA_KEY}"
mainnet = "https://mainnet.infura.io/v3/${INFURA_KEY}"
```

---

#### C. GANACHE CLI (Local Blockchain)

| Feature | Details |
|---------|---------|
| **Tool** | Local Ethereum blockchain simulator |
| **Installation** | `npm install -g ganache-cli` or `ganache` (new version) |
| **Port** | 8545 (customizable) |
| **Key Features** | Deterministic accounts, fast block generation, state snapshots |

**Usage:**
```bash
# Start with default configuration
ganache-cli

# With custom options
ganache-cli --accounts 20 --gasLimit 8000000 --port 8545 --deterministic

# With balance specification
ganache-cli --account="0xPRIVATE_KEY,100000000000000000000"  # 100 ETH

# Snapshot and revert for testing
curl -X POST http://localhost:8545 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"evm_snapshot","id":1}'

curl -X POST http://localhost:8545 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"evm_revert","params":["0xSNAPSHOT_ID"],"id":1}'
```

---

### 3.2 WEB3.PY (ETHEREUM PYTHON CLIENT)

| Feature | Details |
|--------|---------|
| **Library** | `web3.py` - Python library for Ethereum JSON-RPC interaction |
| **Version** | 7.0.0+ (2025) |
| **Repository** | https://github.com/ethereum/web3.py |
| **Documentation** | https://web3py.readthedocs.io |

**Installation & Basic Usage:**
```python
from web3 import Web3

# Connect to Ethereum (Infura as provider)
w3 = Web3(Web3.HTTPProvider('https://sepolia.infura.io/v3/YOUR_INFURA_KEY'))
assert w3.is_connected()

# Account management
from eth_account import Account
account = Account.from_key(private_key)
print(f"Address: {account.address}")

# Contract interaction
from web3 import ContractFunction
contract_abi = json.load(open('abi.json'))
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# Read function (view/pure)
result = contract.functions.verifyAuthenticator(hash_value).call()

# Write function (state-changing)
tx_hash = contract.functions.submitAuthenticator(hash_value).transact({
    'from': account.address,
    'gas': 200000,
    'gasPrice': w3.eth.gas_price
})
receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

# Event monitoring
event_filter = contract.events.AuthenticatorSubmitted.create_filter(from_block='latest')
for event in event_filter.get_new_entries():
    print(f"Authenticator submitted: {event['args']['hash']}")
```

---

### 3.3 BROWNIE (PYTHON SMART CONTRACT FRAMEWORK)

| Feature | Details |
|--------|---------|
| **Framework** | `brownie` - Full-stack Ethereum development in Python |
| **Installation** | `pip install eth-brownie` |
| **Benefits** | Python-based testing, contract deployment, gas profiling |
| **Integration** | Built on web3.py, supports Hardhat Network/Ganache/Infura |

**Brownie Project Structure:**
```
brownie-project/
├── contracts/
│   └── AuthenticationVerifier.sol
├── scripts/
│   └── deploy.py
├── tests/
│   └── test_verifier.py
└── brownie-config.yaml
```

**brownie-config.yaml:**
```yaml
dependencies:
  - OpenZeppelin/openzeppelin-contracts@4.9.3

networks:
  default: sepolia
  sepolia:
    host: https://sepolia.infura.io/v3/$INFURA_KEY
  localhost:
    host: http://127.0.0.1:8545
```

**Deployment Script (scripts/deploy.py):**
```python
from brownie import AuthenticationVerifier, accounts, network

def main():
    # Deploy contract
    acct = accounts.load('my_account')
    contract = AuthenticationVerifier.deploy({'from': acct})
    print(f"Deployed at: {contract.address}")
    
    # Interact
    contract.submitAuthenticator(hash_value, {'from': acct})
    verified = contract.verifyAuthenticator(hash_value)
    print(f"Verified: {verified}")
```

---

### 3.4 INFURA (ETHEREUM RPC PROVIDER)

| Feature | Details |
|--------|---------|
| **Service** | Hosted Ethereum node provider |
| **Website** | https://infura.io |
| **Networks** | Ethereum mainnet, Sepolia, Goerli, Arbitrum, Polygon, Optimism |
| **Plan** | Free tier: 100K requests/day, Paid: unlimited |
| **API** | JSON-RPC compatible |

**Setup:**
```bash
# Get free API key from https://infura.io
# Store in .env file
INFURA_KEY=your_project_id

# Use in web3.py
from web3 import Web3
w3 = Web3(Web3.HTTPProvider(f'https://sepolia.infura.io/v3/{os.getenv("INFURA_KEY")}'))
```

---

## 4. DATABASES

### 4.1 REDIS (SESSION STATE - PRIMARY)

| Feature | Details |
|--------|---------|
| **Type** | In-memory key-value store |
| **Primary Use** | Kerberos session state, ticket cache, authentication cache |
| **Installation** | `apt install redis-server` (Linux) or `brew install redis` (macOS) |
| **Version** | 7.0+ (2024) |
| **Port** | 6379 (default) |

**Installation & Configuration:**
```bash
# Install
sudo apt install redis-server

# Start service
sudo systemctl start redis-server
sudo systemctl enable redis-server  # Enable on boot

# Verify
redis-cli ping  # Should return PONG

# Check version
redis-cli --version
```

**Python Integration:**
```python
import redis
import json
import hashlib

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# Store Kerberos session
session_key = f"session:{client_id}:{ticket_id}"
session_data = {
    'client_id': client_id,
    'service_id': service_id,
    'session_key': session_key.hex(),
    'timestamp': int(time.time()),
    'ttl': 28800  # 8 hours
}
r.setex(session_key, session_data['ttl'], json.dumps(session_data))

# Retrieve session
session = r.get(session_key)
if session:
    session_data = json.loads(session)
    
# Delete on logout
r.delete(session_key)

# Monitor with TTL
ttl = r.ttl(session_key)  # Returns seconds until expiration
```

**Configuration File (/etc/redis/redis.conf):**
```ini
# Network
bind 127.0.0.1 ::1
port 6379
timeout 0

# Persistence
save 900 1
save 300 10
save 60 10000
appendonly yes
appendfsync everysec

# Memory
maxmemory 2gb
maxmemory-policy allkeys-lru

# Logging
loglevel notice
logfile ""

# Authentication (optional)
requirepass your_redis_password
```

---

### 4.2 POSTGRESQL (LONG-TERM STORAGE - OPTIONAL)

| Feature | Details |
|--------|---------|
| **Type** | Relational database (ACID compliance) |
| **Primary Use** | Long-term audit logs, user profiles, event history |
| **Installation** | `apt install postgresql postgresql-contrib` |
| **Version** | 15+ (2024) |
| **Port** | 5432 (default) |

**Installation:**
```bash
# Install
sudo apt install postgresql postgresql-contrib

# Start service
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Access psql
sudo -u postgres psql

# Create database and user
CREATE DATABASE kerberos_audit;
CREATE USER kerberos_user WITH PASSWORD 'secure_password';
ALTER ROLE kerberos_user SET client_encoding TO 'utf8';
ALTER ROLE kerberos_user SET default_transaction_isolation TO 'read committed';
GRANT ALL PRIVILEGES ON DATABASE kerberos_audit TO kerberos_user;
```

**Python Integration (SQLAlchemy):**
```python
from sqlalchemy import create_engine, Column, String, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Database connection
engine = create_engine('postgresql://kerberos_user:password@localhost:5432/kerberos_audit')
Session = sessionmaker(bind=engine)

# ORM Model for audit logs
Base = declarative_base()

class AuthenticationLog(Base):
    __tablename__ = 'authentication_logs'
    
    id = Column(Integer, primary_key=True)
    client_id = Column(String(255))
    service_id = Column(String(255))
    timestamp = Column(DateTime, default=datetime.utcnow)
    status = Column(String(50))  # success, failed
    authenticator_hash = Column(String(256))
    blockchain_tx_hash = Column(String(256), nullable=True)

# Create tables
Base.metadata.create_all(engine)

# Log authentication event
session = Session()
log_entry = AuthenticationLog(
    client_id='client1',
    service_id='service1',
    status='success',
    authenticator_hash=hash_value
)
session.add(log_entry)
session.commit()
```

---

### 4.3 MONGODB (OPTIONAL - FOR DOCUMENT STORAGE)

| Feature | Details |
|--------|---------|
| **Type** | NoSQL document database |
| **Primary Use** | Flexible schema for Kerberos message storage |
| **Installation** | `apt install -y mongodb-org` or Docker image |
| **Version** | 7.0+ (2024) |
| **Port** | 27017 (default) |

**Python Integration (PyMongo):**
```python
from pymongo import MongoClient
import json
from datetime import datetime

# Connect
client = MongoClient('mongodb://localhost:27017/')
db = client['kerberos_db']
authenticators = db['authenticators']

# Store Kerberos authenticator
auth_doc = {
    'client_id': 'client1',
    'authenticator_hash': hash_value,
    'timestamp': datetime.utcnow(),
    'blockchain_verified': False,
    'tx_hash': None
}
result = authenticators.insert_one(auth_doc)

# Query
doc = authenticators.find_one({'authenticator_hash': hash_value})

# Update after blockchain verification
authenticators.update_one(
    {'_id': result.inserted_id},
    {'$set': {'blockchain_verified': True, 'tx_hash': tx_hash}}
)
```

---

## 5. CONTAINERIZATION & ORCHESTRATION

### 5.1 DOCKER (CONTAINER RUNTIME)

| Feature | Details |
|--------|---------|
| **Type** | Container runtime (lightweight virtualization) |
| **Installation** | https://docs.docker.com/install |
| **Current Version** | 27.0+ (2024) |
| **Key Concepts** | Image, Container, Volume, Network |

**Installation (Ubuntu/Debian):**
```bash
# Add Docker repository
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Verify
docker --version
docker run hello-world
```

**Dockerfile for Project 6:**
```dockerfile
# Multi-stage build for Kerberos + Blockchain
FROM python:3.12-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Final stage
FROM python:3.12-slim

WORKDIR /app

# Copy Python packages from builder
COPY --from=builder /root/.local /home/appuser/.local

# Create app user
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

USER appuser

# Set Python path
ENV PATH=/home/appuser/.local/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Copy application code
COPY --chown=appuser:appuser . .

# Expose ports
EXPOSE 5000 6379

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5000/health')"

# Run application
CMD ["python", "main.py"]
```

**Build and Run:**
```bash
# Build image
docker build -t blockchain-kerberos:latest .

# Run container
docker run -d \
  --name kerberos-app \
  -p 5000:5000 \
  -p 6379:6379 \
  -e ETHEREUM_RPC_URL="https://sepolia.infura.io/v3/YOUR_KEY" \
  blockchain-kerberos:latest

# View logs
docker logs -f kerberos-app

# Execute commands in container
docker exec -it kerberos-app python -c "import cryptography; print(cryptography.__version__)"

# Stop and remove
docker stop kerberos-app && docker rm kerberos-app
```

---

### 5.2 DOCKER COMPOSE (MULTI-CONTAINER ORCHESTRATION)

| Feature | Details |
|--------|---------|
| **Type** | Container orchestration for development/testing |
| **Installation** | Included with Docker Desktop or `sudo apt install docker-compose` |
| **Primary Use** | Local Kerberos + Redis + PostgreSQL + Ethereum node stack |

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  # Kerberos Core Service
  kerberos-server:
    build: .
    container_name: kerberos-server
    ports:
      - "5000:5000"  # Kerberos API
      - "5001:5001"  # TGS port
    environment:
      - REDIS_URL=redis://redis:6379
      - POSTGRES_URL=postgresql://kerberos_user:password@postgres:5432/kerberos_audit
      - ETHEREUM_RPC_URL=http://anvil:8545
      - ENV=development
    depends_on:
      - redis
      - postgres
      - anvil
    volumes:
      - ./logs:/app/logs
      - ./configs:/app/configs:ro
    networks:
      - kerberos-network
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
      interval: 30s
      timeout: 3s
      retries: 3

  # Redis for session state
  redis:
    image: redis:7-alpine
    container_name: kerberos-redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    networks:
      - kerberos-network
    command: redis-server --appendonly yes --maxmemory 2gb --maxmemory-policy allkeys-lru
    restart: unless-stopped

  # PostgreSQL for long-term storage
  postgres:
    image: postgres:15-alpine
    container_name: kerberos-postgres
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_DB=kerberos_audit
      - POSTGRES_USER=kerberos_user
      - POSTGRES_PASSWORD=secure_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - kerberos-network
    restart: unless-stopped

  # Local Ethereum blockchain (Anvil)
  anvil:
    image: ghcr.io/foundry-rs/foundry:latest
    container_name: kerberos-anvil
    ports:
      - "8545:8545"
    command: anvil --host 0.0.0.0 --port 8545 --chain-id 1337 --accounts 20
    networks:
      - kerberos-network
    restart: unless-stopped

  # Optional: Hyperledger Fabric orderer (for enterprise variant)
  fabric-orderer:
    image: hyperledger/fabric-orderer:2.5
    container_name: orderer.kerberos.local
    ports:
      - "7050:7050"
    environment:
      - FABRIC_LOGGING_SPEC=INFO
      - ORDERER_GENERAL_LISTENADDRESS=0.0.0.0
      - ORDERER_GENERAL_LISTENPORT=7050
      - ORDERER_GENERAL_LOCALMSPID=OrdererMSP
      - ORDERER_GENERAL_LOCALMSPDIR=/var/hyperledger/orderer/msp
      - ORDERER_GENERAL_TLS_ENABLED=false
    volumes:
      - ./fabric-config/orderer.kerberos.local:/var/hyperledger/orderer/msp
    networks:
      - kerberos-network
    restart: unless-stopped

volumes:
  redis_data:
  postgres_data:

networks:
  kerberos-network:
    driver: bridge
```

**Usage:**
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f kerberos-server

# Stop services
docker-compose down

# Rebuild after code changes
docker-compose up -d --build

# Connect to Redis
docker-compose exec redis redis-cli

# Connect to PostgreSQL
docker-compose exec postgres psql -U kerberos_user -d kerberos_audit
```

---

### 5.3 KUBERNETES (PRODUCTION ORCHESTRATION)

| Feature | Details |
|--------|---------|
| **Type** | Container orchestration for production |
| **Installation** | kubectl + minikube (local) or cloud provider (AWS/GCP/Azure) |
| **Typical Cluster** | 3-5 nodes minimum for HA |
| **Best For** | Production Kerberos + Hyperledger Fabric deployment |

**Kubernetes Deployment Manifest (k8s/kerberos-deployment.yaml):**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: kerberos-server
  namespace: default
spec:
  replicas: 3
  selector:
    matchLabels:
      app: kerberos-server
  template:
    metadata:
      labels:
        app: kerberos-server
    spec:
      containers:
      - name: kerberos-server
        image: blockchain-kerberos:latest
        imagePullPolicy: IfNotPresent
        ports:
        - containerPort: 5000
          name: api
        - containerPort: 5001
          name: tgs
        env:
        - name: REDIS_URL
          value: "redis://redis-service:6379"
        - name: POSTGRES_URL
          valueFrom:
            secretKeyRef:
              name: postgres-secret
              key: connection-string
        - name: ETHEREUM_RPC_URL
          valueFrom:
            configMapKeyRef:
              name: ethereum-config
              key: rpc-url
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 5000
          initialDelaySeconds: 10
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 5000
          initialDelaySeconds: 5
          periodSeconds: 5

---
apiVersion: v1
kind: Service
metadata:
  name: kerberos-service
spec:
  selector:
    app: kerberos-server
  ports:
  - name: api
    port: 5000
    targetPort: 5000
  - name: tgs
    port: 5001
    targetPort: 5001
  type: LoadBalancer

---
apiVersion: v1
kind: ConfigMap
metadata:
  name: ethereum-config
data:
  rpc-url: "https://sepolia.infura.io/v3/YOUR_KEY"

---
apiVersion: v1
kind: Secret
metadata:
  name: postgres-secret
type: Opaque
stringData:
  connection-string: "postgresql://kerberos_user:password@postgres-service:5432/kerberos_audit"
```

**Deploy to Kubernetes:**
```bash
# Create namespace
kubectl create namespace kerberos

# Apply manifests
kubectl apply -f k8s/ -n kerberos

# Check deployment status
kubectl get deployment -n kerberos
kubectl get pods -n kerberos
kubectl describe pod <pod-name> -n kerberos

# View logs
kubectl logs -f deployment/kerberos-server -n kerberos

# Scale replicas
kubectl scale deployment kerberos-server --replicas=5 -n kerberos

# Update image
kubectl set image deployment/kerberos-server kerberos-server=blockchain-kerberos:v1.0.1 -n kerberos

# Port forward for local testing
kubectl port-forward svc/kerberos-service 5000:5000 -n kerberos
```

---

## 6. TESTING & QUALITY ASSURANCE

### 6.1 PYTEST (UNIT & INTEGRATION TESTING)

| Feature | Details |
|--------|---------|
| **Framework** | Python's primary testing framework |
| **Installation** | `pip install pytest==8.0.0 pytest-cov==5.0.0 pytest-asyncio==0.24.0` |
| **Coverage Requirement** | 90%+ for cryptographic code, 80%+ for other modules |

**Test Structure:**
```python
# tests/test_kerberos_core.py
import pytest
from unittest.mock import patch, MagicMock
from project6.kerberos_core import AuthenticationServer, TicketGrantingServer
from project6.crypto_core import SessionKeyGenerator

@pytest.fixture
def auth_server():
    """Fixture for AuthenticationServer instance"""
    return AuthenticationServer()

@pytest.fixture
def tgs():
    """Fixture for TGS instance"""
    return TicketGrantingServer()

class TestAuthenticationServer:
    """Test suite for Kerberos Authentication Server"""
    
    def test_client_authentication_success(self, auth_server):
        """Test successful client authentication"""
        client_id = "client1"
        password = "password123"
        
        result = auth_server.authenticate(client_id, password)
        
        assert result['status'] == 'success'
        assert 'tgt' in result
        assert 'session_key' in result
    
    def test_client_authentication_failure(self, auth_server):
        """Test failed authentication with wrong password"""
        with pytest.raises(AuthenticationException):
            auth_server.authenticate("client1", "wrong_password")
    
    @pytest.mark.asyncio
    async def test_concurrent_authentications(self, auth_server):
        """Test handling of concurrent authentication requests"""
        import asyncio
        tasks = [
            auth_server.authenticate_async(f"client{i}", "password")
            for i in range(100)
        ]
        results = await asyncio.gather(*tasks)
        assert len(results) == 100

class TestEthereumAdapter:
    """Test suite for Ethereum blockchain adapter"""
    
    @patch('web3.Web3.HTTPProvider')
    def test_submit_authenticator_to_blockchain(self, mock_provider):
        """Test submitting authenticator to Ethereum"""
        from project6.ethereum_adapter import EthereumAdapter
        
        adapter = EthereumAdapter("test_contract_address")
        tx_hash = adapter.submit_authenticator(b"authenticator_hash")
        
        assert tx_hash is not None
        assert len(tx_hash) == 66  # 0x + 64 hex chars
    
    def test_gas_cost_calculation(self):
        """Test gas cost optimization"""
        from project6.ethereum_adapter import GasCostOptimizer
        
        optimizer = GasCostOptimizer()
        gas_cost = optimizer.estimate_cost(submit_authenticator)
        
        assert gas_cost < 100000  # Should be <100K gas
        assert gas_cost > 50000   # Should be >50K gas

class TestCryptoCore:
    """Test suite for cryptographic primitives"""
    
    def test_aes_encryption_decryption(self):
        """Test AES-128-CBC encryption/decryption"""
        from project6.crypto_core import AESEncryptor
        
        encryptor = AESEncryptor()
        plaintext = b"This is a secret message"
        
        ciphertext = encryptor.encrypt(plaintext)
        decrypted = encryptor.decrypt(ciphertext)
        
        assert decrypted == plaintext
        assert ciphertext != plaintext
    
    def test_rsa_key_generation(self):
        """Test RSA-2048 key generation"""
        from project6.crypto_core import RSAKeyManager
        
        key_manager = RSAKeyManager()
        public_key, private_key = key_manager.generate_key_pair()
        
        assert public_key is not None
        assert private_key is not None
        assert public_key.key_size == 2048
    
    def test_hash_function_deterministic(self):
        """Test SHA-256 hash determinism"""
        from project6.crypto_core import HashGenerator
        
        hash_gen = HashGenerator()
        data = b"Test data"
        
        hash1 = hash_gen.hash(data)
        hash2 = hash_gen.hash(data)
        
        assert hash1 == hash2  # Same input = same hash

# Run tests with coverage
# pytest --cov=project6 --cov-report=html tests/
```

**Running Tests:**
```bash
# Run all tests
pytest tests/

# Run with verbose output
pytest -v tests/

# Run specific test file
pytest tests/test_kerberos_core.py

# Run specific test class
pytest tests/test_kerberos_core.py::TestAuthenticationServer

# Run with coverage report
pytest --cov=project6 --cov-report=html --cov-report=term tests/

# Run only fast tests (exclude slow ones)
pytest -m "not slow" tests/

# Run with parallel execution (faster)
pytest -n auto tests/
```

---

### 6.2 HYPOTHESIS (PROPERTY-BASED TESTING)

| Feature | Details |
|--------|---------|
| **Framework** | Property-based testing for cryptographic edge cases |
| **Installation** | `pip install hypothesis==6.100.0` |
| **Purpose** | Automatically generate test cases to find edge cases |

**Property-Based Tests:**
```python
from hypothesis import given, strategies as st
from project6.crypto_core import AESEncryptor

class TestCryptographicProperties:
    @given(plaintext=st.binary(min_size=0, max_size=1024))
    def test_encryption_roundtrip(self, plaintext):
        """Property: encrypt(plaintext) then decrypt = plaintext"""
        encryptor = AESEncryptor()
        ciphertext = encryptor.encrypt(plaintext)
        decrypted = encryptor.decrypt(ciphertext)
        assert decrypted == plaintext
    
    @given(st.integers(min_value=1, max_value=10000))
    def test_session_key_length(self, num_iterations):
        """Property: session key always 256 bits (32 bytes)"""
        from project6.crypto_core import SessionKeyGenerator
        
        keygen = SessionKeyGenerator()
        for _ in range(num_iterations):
            key = keygen.generate()
            assert len(key) == 32
            assert isinstance(key, bytes)
```

---

### 6.3 LOAD TESTING (LOCUST)

| Feature | Details |
|--------|---------|
| **Framework** | `locust` - Load testing for authentication systems |
| **Installation** | `pip install locust==2.20.0` |
| **Metrics** | Request/sec, Response time, Latency distribution |

**Load Test Script (locustfile.py):**
```python
from locust import HttpUser, task, between
from random import randint

class KerberosUser(HttpUser):
    wait_time = between(1, 3)  # Wait 1-3 seconds between requests
    
    @task(3)
    def authenticate_client(self):
        """Simulate client authentication (TGT request)"""
        client_id = f"client{randint(1, 1000)}"
        self.client.post(f"/authenticate", json={
            "client_id": client_id,
            "password": "password123"
        })
    
    @task(2)
    def request_service_ticket(self):
        """Simulate service ticket request"""
        tgt = self.client.get("/tgt").json()
        self.client.post(f"/request_ticket", json={
            "tgt": tgt,
            "service_id": f"service{randint(1, 100)}"
        })
    
    @task(1)
    def blockchain_submit(self):
        """Simulate blockchain submission"""
        self.client.post("/blockchain/submit_authenticator", json={
            "authenticator_hash": "0x" + "a" * 64
        })
```

**Run Load Tests:**
```bash
# Start Locust web UI
locust -f locustfile.py --host=http://localhost:5000

# Or run in headless mode
locust -f locustfile.py --host=http://localhost:5000 \
  --users=1000 --spawn-rate=100 --run-time=5m

# Alternative: Python script
from locust import main
main.main(['locustfile.py', '--headless', '-u', '1000', '-r', '100', '-t', '5m'])
```

---

## 7. MONITORING & LOGGING

### 7.1 PROMETHEUS (METRICS COLLECTION)

| Feature | Details |
|--------|---------|
| **Tool** | Time-series metrics database |
| **Port** | 9090 (default) |
| **Scrape Interval** | 15s (default, configurable) |

**Prometheus Configuration (prometheus.yml):**
```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'kerberos-server'
    static_configs:
      - targets: ['localhost:5000']
    metrics_path: '/metrics'
  
  - job_name: 'redis'
    static_configs:
      - targets: ['localhost:6379']
  
  - job_name: 'postgres'
    static_configs:
      - targets: ['localhost:9187']  # postgres_exporter

alerting:
  alertmanagers:
    - static_configs:
        - targets:
            - localhost:9093  # AlertManager
```

**Python Metrics (prometheus_client):**
```python
from prometheus_client import Counter, Histogram, Gauge

# Metrics for Kerberos
auth_attempts = Counter('kerberos_auth_attempts_total', 'Total authentication attempts', ['status'])
auth_latency = Histogram('kerberos_auth_latency_seconds', 'Authentication latency', buckets=(0.1, 0.5, 1, 2, 5))
active_sessions = Gauge('kerberos_active_sessions', 'Number of active sessions')

# Metrics for Blockchain
blockchain_submissions = Counter('blockchain_submissions_total', 'Total blockchain submissions', ['status'])
blockchain_latency = Histogram('blockchain_latency_seconds', 'Blockchain transaction latency')
gas_spent = Counter('blockchain_gas_total', 'Total gas spent', ['transaction_type'])

# Usage in authentication handler
@auth_latency.time()
def authenticate_client(client_id, password):
    try:
        result = auth_logic(client_id, password)
        auth_attempts.labels(status='success').inc()
        active_sessions.inc()
        return result
    except AuthenticationError:
        auth_attempts.labels(status='failed').inc()
        raise
```

---

### 7.2 GRAFANA (VISUALIZATION)

| Feature | Details |
|--------|---------|
| **Tool** | Dashboard visualization for Prometheus metrics |
| **Port** | 3000 (default) |
| **Data Sources** | Prometheus, Loki, Elasticsearch |
| **Installation** | `docker run -d -p 3000:3000 grafana/grafana` |

**Dashboard Configuration (JSON):**
```json
{
  "dashboard": {
    "title": "Project 6 Metrics",
    "panels": [
      {
        "title": "Authentication Attempts/sec",
        "targets": [
          {
            "expr": "rate(kerberos_auth_attempts_total[1m])"
          }
        ]
      },
      {
        "title": "Auth Latency (p95)",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, kerberos_auth_latency_seconds)"
          }
        ]
      },
      {
        "title": "Blockchain Gas Spent",
        "targets": [
          {
            "expr": "increase(blockchain_gas_total[1h])"
          }
        ]
      }
    ]
  }
}
```

---

### 7.3 ELK STACK (CENTRALIZED LOGGING)

| Feature | Details |
|--------|---------|
| **Components** | Elasticsearch (storage), Logstash (processing), Kibana (visualization) |
| **Installation** | Docker images from docker.elastic.co |
| **Log Format** | JSON for easy parsing |

**Logstash Configuration (logstash.conf):**
```
input {
  tcp {
    port => 5000
    codec => json
  }
}

filter {
  if [type] == "kerberos" {
    grok {
      match => { "message" => "%{TIMESTAMP_ISO8601:timestamp} %{LOGLEVEL:level} %{DATA:component}" }
    }
  }
}

output {
  elasticsearch {
    hosts => ["elasticsearch:9200"]
    index => "kerberos-%{+YYYY.MM.dd}"
  }
  
  if [@metadata][index_type] == "alert" {
    elasticsearch {
      hosts => ["elasticsearch:9200"]
      index => "alerts-%{+YYYY.MM.dd}"
    }
  }
}
```

**Python Logging Configuration:**
```python
import logging
import json
from pythonjsonlogger import jsonlogger

# Configure JSON logging
logger = logging.getLogger()
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)

# Usage
logger.info("Authentication successful", extra={
    "client_id": client_id,
    "service_id": service_id,
    "latency_ms": latency,
    "blockchain_tx": tx_hash
})
```

---

## 8. NETWORK SECURITY TOOLS

### 8.1 WIRESHARK (PACKET ANALYSIS)

| Feature | Details |
|--------|---------|
| **Tool** | Network packet capture and analysis |
| **Installation** | `sudo apt install wireshark wireshark-common` |
| **Usage** | Capture and analyze Kerberos protocol traffic |
| **Port** | Kerberos uses UDP/TCP 88 (Authentication) and 749 (Admin) |

**Kerberos Protocol Analysis:**
```bash
# Capture Kerberos traffic
sudo tcpdump -i eth0 -w kerberos.pcap 'port 88 or port 749'

# Open in Wireshark
wireshark kerberos.pcap

# Filter for specific traffic
# Display filter: kerberos
# Display filter: eth.addr == 192.168.1.100
# Display filter: tcp.port == 88

# Export packets for analysis
# Right-click → Export Packet Dissections → as JSON
```

**Kerberos Message Types:**
```
AS-REQ (Authentication Server Request) → port 88
AS-REP (Authentication Server Reply)
TGS-REQ (Ticket Granting Server Request)
TGS-REP (Ticket Granting Server Reply)
AP-REQ (Application Request)
AP-REP (Application Reply)
```

---

### 8.2 SCAPY (PACKET CRAFTING)

| Feature | Details |
|--------|---------|
| **Library** | Python packet crafting and analysis |
| **Installation** | `pip install scapy==2.6.0` |
| **Usage** | Simulate Kerberos attacks for testing |

**Testing Replay Attack Resistance:**
```python
from scapy.all import *

# Capture Kerberos AS-REQ
def capture_kerberos_request():
    packets = sniff(filter="port 88", prn=lambda x: x.show(), count=1)
    return packets[0]

# Replay captured packet (should be rejected)
def test_replay_protection():
    original_packet = capture_kerberos_request()
    
    # Craft replay packet with same authenticator
    replay_packet = original_packet.copy()
    
    # Send replayed packet
    send(replay_packet, iface="eth0")
    
    # System should detect replay and reject
    # Verify: Check authentication logs for replay detection
```

---

### 8.3 NMAP (NETWORK SCANNING)

| Feature | Details |
|--------|---------|
| **Tool** | Network reconnaissance and port scanning |
| **Installation** | `sudo apt install nmap` |
| **Usage** | Verify Kerberos service availability |

```bash
# Scan for Kerberos ports
nmap -p 88,749 localhost

# Service version detection
nmap -sV -p 88 localhost

# UDP/TCP port scan
nmap -p U:88,T:88 localhost

# More aggressive scanning (use with permission only)
nmap -sS -sV -p 88,749 target_host
```

---

## 9. CI/CD & DEPLOYMENT

### 9.1 GITHUB ACTIONS (CI/CD)

| Feature | Details |
|--------|---------|
| **Platform** | GitHub's native CI/CD service |
| **Trigger** | On push, pull request, schedule |
| **Runner** | ubuntu-latest, macos-latest, windows-latest |

**.github/workflows/ci.yml:**
```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]
  schedule:
    - cron: '0 2 * * *'  # Daily at 2 AM UTC

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.10', '3.11', '3.12']
    
    services:
      redis:
        image: redis:7-alpine
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 6379:6379
      
      postgres:
        image: postgres:15-alpine
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
        cache: 'pip'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-cov pytest-asyncio
    
    - name: Lint with flake8
      run: |
        pip install flake8
        flake8 project6 --count --select=E9,F63,F7,F82 --show-source --statistics
    
    - name: Type checking with mypy
      run: |
        pip install mypy
        mypy project6/
    
    - name: Run tests with pytest
      env:
        REDIS_URL: redis://localhost:6379
        POSTGRES_URL: postgresql://postgres:postgres@localhost:5432/test_db
      run: |
        pytest --cov=project6 --cov-report=xml tests/
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        fail_ci_if_error: false
  
  security:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Run Bandit security scan
      run: |
        pip install bandit
        bandit -r project6 -f json -o bandit-report.json
    
    - name: Run Trivy vulnerability scan
      uses: aquasecurity/trivy-action@master
      with:
        scan-type: 'fs'
        scan-ref: '.'
        format: 'sarif'
        output: 'trivy-results.sarif'
    
    - name: Upload Trivy results to GitHub Security
      uses: github/codeql-action/upload-sarif@v2
      if: always()
      with:
        sarif_file: 'trivy-results.sarif'
  
  build-and-push:
    needs: [test, security]
    runs-on: ubuntu-latest
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v2
    
    - name: Login to Docker Hub
      uses: docker/login-action@v2
      with:
        username: ${{ secrets.DOCKER_USERNAME }}
        password: ${{ secrets.DOCKER_PASSWORD }}
    
    - name: Build and push Docker image
      uses: docker/build-push-action@v4
      with:
        context: .
        push: true
        tags: |
          ${{ secrets.DOCKER_USERNAME }}/blockchain-kerberos:latest
          ${{ secrets.DOCKER_USERNAME }}/blockchain-kerberos:${{ github.sha }}
        cache-from: type=registry,ref=${{ secrets.DOCKER_USERNAME }}/blockchain-kerberos:buildcache
        cache-to: type=registry,ref=${{ secrets.DOCKER_USERNAME }}/blockchain-kerberos:buildcache,mode=max
```

---

### 9.2 GITLAB CI/CD (ALTERNATIVE)

| Feature | Details |
|--------|---------|
| **Platform** | GitLab's native CI/CD (similar to GitHub Actions) |
| **Runner** | Self-hosted or GitLab.com runners |
| **Configuration** | `.gitlab-ci.yml` |

**.gitlab-ci.yml:**
```yaml
stages:
  - test
  - security
  - build
  - deploy

variables:
  DOCKER_IMAGE: registry.gitlab.com/$CI_PROJECT_PATH:$CI_COMMIT_SHA

test:
  stage: test
  image: python:3.12
  services:
    - redis:7-alpine
    - postgres:15-alpine
  script:
    - pip install -r requirements.txt pytest pytest-cov
    - pytest --cov=project6 tests/
  coverage: '/TOTAL.*\s+(\d+%)$/'

security:
  stage: security
  image: python:3.12
  script:
    - pip install bandit safety
    - bandit -r project6
    - safety check

docker_build:
  stage: build
  image: docker:latest
  services:
    - docker:dind
  script:
    - docker build -t $DOCKER_IMAGE .
    - docker push $DOCKER_IMAGE
  only:
    - main

deploy:
  stage: deploy
  image: bitnami/kubectl:latest
  script:
    - kubectl set image deployment/kerberos-server kerberos-server=$DOCKER_IMAGE
  environment:
    name: production
    kubernetes:
      namespace: kerberos
  only:
    - main
```

---

## 10. DEVELOPMENT ENVIRONMENT SETUP

### 10.1 IDE SETUP

**VS Code (Recommended):**

```json
// .vscode/settings.json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/venv/bin/python",
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "python.linting.flake8Enabled": true,
  "python.formatting.provider": "black",
  "[python]": {
    "editor.formatOnSave": true,
    "editor.defaultFormatter": "ms-python.python"
  },
  "python.testing.pytestEnabled": true,
  "python.testing.pytestArgs": ["tests"]
}
```

**Extensions:**
- Python (Microsoft)
- Pylance
- Flake8
- Black Formatter
- Solidity (for smart contracts)
- Docker
- Kubernetes
- REST Client

---

### 10.2 GIT WORKFLOW

```bash
# Clone repository
git clone https://github.com/username/blockchain-enhanced-kerberos.git
cd blockchain-enhanced-kerberos

# Create development branch
git checkout -b feature/kerberos-implementation

# Make changes and commit
git add .
git commit -m "feat: implement Kerberos AS-REQ/AS-REP"

# Push and create pull request
git push origin feature/kerberos-implementation

# After review and merge to main
git checkout main
git pull origin main
```

---

## 11. HARDWARE REQUIREMENTS

### Development Machine:
- **CPU:** 4-core (Intel/AMD) minimum, 8-core recommended
- **RAM:** 16GB minimum, 32GB recommended
- **SSD:** 256GB minimum (OS + dependencies + code)
- **Network:** 1Gbps Ethernet or stable WiFi

### Testing Environment (Local):
- **CPU:** 8-core
- **RAM:** 32GB
- **SSD:** 512GB (for Kerberos + Redis + PostgreSQL + Blockchain nodes)
- **Docker:** Docker Engine 27.0+

### Production Deployment (Cloud):
- **AWS EC2:** t3.large (2 vCPU, 8GB RAM) per node × 3 nodes minimum
- **GCP Compute Engine:** n2-standard-2 equivalent
- **Azure VM:** Standard_D2s_v3 equivalent
- **Load Balancer:** AWS ELB, Google Cloud LB, or Azure LB
- **Database:** AWS RDS PostgreSQL, Google Cloud SQL, or Azure Database
- **Blockchain Node:** AWS Lightsail or dedicated server (16GB RAM, 200GB SSD)
- **Backup:** 100GB offsite backup storage minimum

---

**Document Version:** 1.1  
**Last Updated:** December 16, 2025  
**Total Setup Time:** 4-6 hours (experienced developer)
