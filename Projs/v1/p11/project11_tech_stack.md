# Project 11: Automated Endpoint Security Posture Management (AESPM)
## Technology Stack Deep Dive & Tool Integration

---

## Part 1: Complete Technology Matrix

### Backend Services

| Service | Technology | Version | Purpose | Justification | Alternatives |
|---------|-----------|---------|---------|---------------|---------------|
| **Collection Agent** | Go (Golang) | 1.21+ | Lightweight endpoint agent | Cross-platform binary, low memory | Rust, Python |
| **API Server** | FastAPI | 0.100+ | REST API + async processing | Native async, great for I/O | Django, Flask, Gin |
| **Message Queue** | Apache Kafka | 3.5+ | High-throughput event streaming | Fault-tolerant, distributed | RabbitMQ, Redis Streams |
| **Cache Layer** | Redis | 7.0+ | In-memory caching | Low-latency, excellent for queries | Memcached, DynamoDB |
| **Time-Series DB** | TimescaleDB | 2.10+ | Historical config storage | PostgreSQL extension, native compression | InfluxDB, VictoriaMetrics |
| **Search Engine** | Elasticsearch | 8.10+ | Full-text search, indexing | Powerful queries, aggregations | Solr, Meilisearch |
| **Task Queue** | Celery | 5.3+ | Async job processing | Distributed, reliable | RQ, APScheduler |
| **LLM API** | OpenAI API | Latest | GPT-4 integration | State-of-the-art models | Anthropic, DeepSeek, Local Ollama |
| **Database** | PostgreSQL | 14+ | Relational data storage | ACID compliance, TimescaleDB extension | MySQL, MariaDB |

### Frontend Technologies

| Layer | Technology | Version | Purpose | Justification | Alternatives |
|-------|-----------|---------|---------|---------------|---------------|
| **Framework** | React | 18.2+ | UI component library | Ecosystem, performance, adoption | Vue.js, Angular, Svelte |
| **Language** | TypeScript | 5.0+ | Type safety | Catch errors at compile time | JavaScript, Flow |
| **State Mgmt** | Redux Toolkit | 1.9+ | Predictable state management | DevTools, middleware system | Zustand, Context API, Jotai |
| **HTTP Client** | Axios | 1.4+ | API communication | Promise-based, interceptors | Fetch API, Superagent |
| **WebSocket** | Socket.IO | 4.5+ | Real-time updates | Fallback support, rooms | Native WebSocket, ws |
| **Visualization** | D3.js | 7.0+ | Complex interactive charts | Fine-grained control | Plotly, Recharts, Vega |
| **UI Components** | Material-UI | 5.12+ | Pre-built components | Comprehensive, accessible | Tailwind, Bootstrap, Chakra |
| **Build Tool** | Vite | 4.4+ | Fast module bundling | 10x faster than Webpack | Webpack, Parcel, esbuild |
| **Testing** | Jest + RTL | Latest | Unit + component tests | React-focused, great DX | Vitest, Testing Library |

### Infrastructure & DevOps

| Component | Technology | Version | Purpose | Justification | Alternatives |
|-----------|-----------|---------|---------|---------------|---------------|
| **Containerization** | Docker | 24.0+ | Container images | Industry standard | Podman, Containerd |
| **Orchestration** | Kubernetes | 1.27+ | Production deployment | Scalable, reliable, cloud-native | Docker Swarm, Nomad |
| **Helm** | Helm | 3.12+ | Kubernetes package manager | Template-based deployments | Kustomize, Helmsman |
| **CI/CD** | GitHub Actions | Latest | Automated testing/deployment | Integrated with GitHub, free | GitLab CI, Jenkins, CircleCI |
| **Container Registry** | Docker Hub / ECR | - | Image storage | Easy distribution, authentication | Quay.io, Harbor, JFrog |
| **Monitoring** | Prometheus | 2.45+ | Metrics collection | Pull-based, time-series | Grafana Loki, InfluxDB |
| **Visualization** | Grafana | 10.0+ | Dashboards and alerting | Rich dashboards, alerting | DataDog, New Relic, Splunk |
| **Logging** | ELK Stack | 8.10+ | Centralized logging | Powerful search, free | Splunk, Datadog, CloudWatch |
| **Secret Mgmt** | HashiCorp Vault | 1.14+ | Secure credential storage | Dynamic secrets, audit trail | AWS Secrets Manager, Azure Vault |

---

## Part 2: Installation & Configuration Guide

### Development Environment Setup

```bash
# Prerequisites (macOS/Linux)
brew install go python node docker docker-compose

# Go 1.21+
go version  # should be 1.21+

# Python 3.10+
python3 --version

# Node 18+
node --version

# Docker
docker --version
docker-compose --version
```

### Backend Service Installation

#### 1. PostgreSQL + TimescaleDB
```bash
# Docker approach (recommended)
docker run -d \
  --name timescaledb \
  -e POSTGRES_PASSWORD=secure_password \
  -p 5432:5432 \
  -v timescaledb_data:/var/lib/postgresql/data \
  timescale/timescaledb:latest-pg15

# Verify
psql -h localhost -U postgres -d postgres
```

#### 2. Apache Kafka
```bash
# Docker Compose
docker-compose up -d kafka zookeeper

# Create topics
docker exec kafka kafka-topics.sh --create \
  --topic endpoint.windows.config \
  --bootstrap-server localhost:9092 \
  --partitions 10 \
  --replication-factor 3
```

#### 3. Redis
```bash
# Docker
docker run -d \
  --name redis \
  -p 6379:6379 \
  redis:7.0 \
  redis-server --appendonly yes

# Verify
redis-cli ping
```

#### 4. Elasticsearch
```bash
# Docker
docker run -d \
  --name elasticsearch \
  -e discovery.type=single-node \
  -e xpack.security.enabled=false \
  -p 9200:9200 \
  docker.elastic.co/elasticsearch/elasticsearch:8.10.0

# Verify
curl http://localhost:9200/
```

### Python Backend Setup

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
cat > requirements.txt << EOF
fastapi==0.100.0
uvicorn==0.23.0
pydantic==2.0.0
sqlalchemy==2.0.0
psycopg2-binary==2.9.0
kafka-python==2.0.2
redis==5.0.0
celery==5.3.0
elasticsearch==8.10.0
openai==0.28.0
anthropic==0.7.0
requests==2.31.0
python-dotenv==1.0.0
pytest==7.4.0
pytest-asyncio==0.21.0
EOF

pip install -r requirements.txt
```

### Go Backend Setup

```bash
# Initialize Go module
go mod init github.com/username/aespm

# Add Go dependencies
go get github.com/go-chi/chi/v5
go get github.com/go-chi/cors
go get github.com/segmentio/kafka-go
go get github.com/redis/go-redis/v9
go get github.com/lib/pq
go get github.com/joho/godotenv

# Build agent
go build -o bin/agent-windows cmd/agent-windows/main.go
go build -o bin/agent-macos cmd/agent-macos/main.go
go build -o bin/agent-linux cmd/agent-linux/main.go
```

### Frontend Setup

```bash
# Create React project
npm create vite@latest aespm-dashboard -- --template react-ts

# Install dependencies
cd aespm-dashboard
npm install

# Key dependencies
npm install \
  redux @reduxjs/toolkit react-redux \
  axios socket.io-client \
  react-router-dom \
  @mui/material @emotion/react @emotion/styled \
  d3 recharts chart.js \
  jest @testing-library/react

# Run development server
npm run dev  # http://localhost:5173
```

---

## Part 3: Docker Compose Stack

```yaml
# docker-compose.yml - Local development stack
version: '3.9'

services:
  # PostgreSQL + TimescaleDB
  timescaledb:
    image: timescale/timescaledb:latest-pg15
    container_name: aespm-postgres
    environment:
      POSTGRES_PASSWORD: postgres_password
      POSTGRES_USER: aespm_user
      POSTGRES_DB: aespm_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init-db.sql:/docker-entrypoint-initdb.d/init.sql
    networks:
      - aespm-network

  # Apache Kafka
  zookeeper:
    image: confluentinc/cp-zookeeper:7.5.0
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
    networks:
      - aespm-network

  kafka:
    image: confluentinc/cp-kafka:7.5.0
    depends_on:
      - zookeeper
    ports:
      - "9092:9092"
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka:29092,PLAINTEXT_HOST://localhost:9092
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT
      KAFKA_INTER_BROKER_LISTENER_NAME: PLAINTEXT
      KAFKA_AUTO_CREATE_TOPICS_ENABLE: "true"
    networks:
      - aespm-network

  # Redis Cache
  redis:
    image: redis:7.0-alpine
    container_name: aespm-redis
    ports:
      - "6379:6379"
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    networks:
      - aespm-network

  # Elasticsearch
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.10.0
    container_name: aespm-elasticsearch
    environment:
      discovery.type: single-node
      xpack.security.enabled: "false"
    ports:
      - "9200:9200"
    volumes:
      - elasticsearch_data:/usr/share/elasticsearch/data
    networks:
      - aespm-network

  # Kibana
  kibana:
    image: docker.elastic.co/kibana/kibana:8.10.0
    container_name: aespm-kibana
    depends_on:
      - elasticsearch
    ports:
      - "5601:5601"
    networks:
      - aespm-network

  # FastAPI Backend
  api:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: aespm-api
    depends_on:
      - timescaledb
      - kafka
      - redis
      - elasticsearch
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://aespm_user:postgres_password@timescaledb:5432/aespm_db
      KAFKA_BROKER: kafka:29092
      REDIS_URL: redis://redis:6379
      ELASTICSEARCH_URL: http://elasticsearch:9200
      OPENAI_API_KEY: ${OPENAI_API_KEY}
    volumes:
      - ./backend:/app
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    networks:
      - aespm-network

  # Celery Worker
  celery:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: aespm-celery
    depends_on:
      - redis
    environment:
      CELERY_BROKER: redis://redis:6379
      DATABASE_URL: postgresql://aespm_user:postgres_password@timescaledb:5432/aespm_db
    volumes:
      - ./backend:/app
    command: celery -A app.tasks worker --loglevel=info
    networks:
      - aespm-network

  # React Dashboard
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: aespm-frontend
    ports:
      - "3000:3000"
    environment:
      REACT_APP_API_URL: http://localhost:8000
      REACT_APP_WS_URL: ws://localhost:8000
    volumes:
      - ./frontend:/app
    command: npm run dev
    networks:
      - aespm-network

  # Prometheus
  prometheus:
    image: prom/prometheus:latest
    container_name: aespm-prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
    networks:
      - aespm-network

  # Grafana
  grafana:
    image: grafana/grafana:latest
    container_name: aespm-grafana
    depends_on:
      - prometheus
    ports:
      - "3001:3000"
    environment:
      GF_SECURITY_ADMIN_PASSWORD: admin
    volumes:
      - grafana_data:/var/lib/grafana
    networks:
      - aespm-network

volumes:
  postgres_data:
  redis_data:
  elasticsearch_data:
  prometheus_data:
  grafana_data:

networks:
  aespm-network:
    driver: bridge
```

**Start the stack:**
```bash
docker-compose up -d

# View logs
docker-compose logs -f api
```

---

## Part 4: Key Integration Points

### Agent ↔ API Communication
```python
# Agent sends config data
POST /api/agents/{agent_id}/config
Content-Type: application/json
Authorization: Bearer {mTLS_certificate}

{
  "timestamp": "2024-01-15T10:30:00Z",
  "os_type": "windows",
  "os_version": "Server 2022",
  "configs": {
    "registry": [{...}],
    "wmi": [{...}],
    "gpo": [{...}]
  }
}
```

### API ↔ Kafka Integration
```python
# Send to Kafka topics
producer.send(
  topic='endpoint.windows.config',
  value=normalized_config,
  key=endpoint_id.encode()
)
```

### API ↔ LLM Integration
```python
# Query OpenAI for analysis
response = openai.ChatCompletion.create(
  model="gpt-4-turbo",
  messages=[
    {"role": "system", "content": SYSTEM_PROMPT},
    {"role": "user", "content": f"Analyze: {config_deviation}"}
  ],
  max_tokens=500,
  temperature=0.3
)
```

### API ↔ Redis Caching
```python
# Cache remediation suggestions
cache_key = f"remediation:{rule_id}:{config_hash}"
cached = redis_client.get(cache_key)
if not cached:
  remediation = generate_remediation(...)
  redis_client.setex(cache_key, 604800, remediation)  # 7 days TTL
```

---

## Part 5: Deployment Checklist

- [ ] All services running and healthy
- [ ] Database migrations applied
- [ ] Kafka topics created
- [ ] Redis persistence enabled
- [ ] Elasticsearch indices created
- [ ] Environment variables configured
- [ ] API endpoints tested
- [ ] Frontend accessible
- [ ] Monitoring dashboards loaded
- [ ] Backup procedures tested

