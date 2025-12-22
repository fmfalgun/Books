# Project 11: AESPM - n8n Workflow Automation Guide
## Building AI-Powered Automation Workflows

---

## Overview: n8n Workflows for AESPM

This guide covers automating Project 11 tasks using **n8n** - a visual workflow automation platform. Each workflow includes:

1. **Data collection** from endpoints
2. **AI agent processing** (Claude/GPT/DeepSeek)
3. **Action execution** (remediation, alerts, reporting)
4. **Monitoring & feedback loops**

---

## Workflow 1: Daily Compliance Report Generation

```
Trigger (Cron: 6 AM daily)
    ↓
Fetch all endpoints from API
    ↓
[Branch: Windows | macOS | Linux]
    ↓
Query TimescaleDB for config history
    ↓
Calculate compliance scores
    ↓
Feed to Claude (AI) → "Generate executive summary"
    ↓
Create PDF report
    ↓
Email to stakeholders
    ↓
Log to Slack
```

**n8n Node Configuration:**

```json
{
  "nodes": [
    {
      "name": "Cron Trigger",
      "type": "n8n-nodes-base.cron",
      "position": [100, 100],
      "parameters": {
        "interval": [1],
        "unit": "day",
        "hour": 6,
        "minute": 0
      }
    },
    {
      "name": "Fetch Endpoints",
      "type": "n8n-nodes-base.httpRequest",
      "position": [300, 100],
      "parameters": {
        "url": "{{ $secrets.API_URL }}/api/endpoints",
        "method": "GET",
        "authentication": "bearerToken",
        "nodeCredentialType": "httpHeaderAuth"
      }
    },
    {
      "name": "Split by OS",
      "type": "n8n-nodes-base.itemLists",
      "position": [500, 100],
      "parameters": {
        "operation": "splitOutItems",
        "fieldToSplit": "os_type"
      }
    },
    {
      "name": "Query Compliance Data",
      "type": "n8n-nodes-base.postgres",
      "position": [700, 100],
      "parameters": {
        "operation": "executeQuery",
        "query": "SELECT endpoint_id, os_type, AVG(compliance_score) FROM configs WHERE timestamp > NOW() - INTERVAL '24 hours' GROUP BY endpoint_id, os_type"
      }
    },
    {
      "name": "AI Analysis - Claude",
      "type": "n8n-nodes-langchain.llmClaude",
      "position": [900, 100],
      "parameters": {
        "model": "claude-3-opus",
        "prompt": "Analyze this endpoint compliance data and provide executive summary:\\n{{ JSON.stringify($node['Query Compliance Data'].json) }}",
        "temperature": 0.3
      }
    },
    {
      "name": "Generate PDF",
      "type": "n8n-nodes-base.fileTemplate",
      "position": [1100, 100],
      "parameters": {
        "template": "html",
        "content": "<html><body><h1>Daily Compliance Report</h1><p>{{ $node['AI Analysis - Claude'].json.text }}</p></body></html>",
        "fileName": "compliance_report_{{ new Date().toISOString().split('T')[0] }}.pdf"
      }
    },
    {
      "name": "Send Email",
      "type": "n8n-nodes-base.emailSend",
      "position": [1300, 100],
      "parameters": {
        "fromEmail": "reports@aespm.company.com",
        "toEmail": "{{ $secrets.REPORT_RECIPIENTS }}",
        "subject": "Daily Endpoint Compliance Report",
        "attachments": "{{ $node['Generate PDF'].json.data }}"
      }
    },
    {
      "name": "Log to Slack",
      "type": "n8n-nodes-base.slack",
      "position": [1500, 100],
      "parameters": {
        "channel": "#security-reports",
        "message": "✅ Daily compliance report generated and sent to stakeholders\\n📊 Total endpoints: {{ $node['Fetch Endpoints'].json.length }}\\n⚠️ Critical issues: {{ $node['AI Analysis - Claude'].json.critical_count }}"
      }
    }
  ],
  "connections": {
    "Cron Trigger": { "main": [["Fetch Endpoints"]] },
    "Fetch Endpoints": { "main": [["Split by OS"]] },
    "Split by OS": { "main": [["Query Compliance Data"]] },
    "Query Compliance Data": { "main": [["AI Analysis - Claude"]] },
    "AI Analysis - Claude": { "main": [["Generate PDF"]] },
    "Generate PDF": { "main": [["Send Email"]] },
    "Send Email": { "main": [["Log to Slack"]] }
  }
}
```

---

## Workflow 2: Real-Time Vulnerability Remediation

```
Endpoint sends config error
    ↓
Webhook receives event
    ↓
Extract deviation details
    ↓
Query rule database
    ↓
Send to GPT-4 → "Generate remediation steps"
    ↓
[Decision: Critical? → Auto-apply : Manual approval]
    ↓
Execute remediation script
    ↓
Verify remediation
    ↓
Create Jira ticket (if failed)
    ↓
Notify Slack
```

**n8n Webhook Workflow:**

```json
{
  "nodes": [
    {
      "name": "Webhook",
      "type": "n8n-nodes-base.webhook",
      "position": [100, 100],
      "parameters": {
        "path": "remediation-webhook",
        "method": "POST",
        "responseMode": "responseNode"
      }
    },
    {
      "name": "Parse Webhook Data",
      "type": "n8n-nodes-base.code",
      "position": [300, 100],
      "parameters": {
        "jsCode": "return { endpoint_id: $input.body.endpoint_id, rule_id: $input.body.rule_id, severity: $input.body.severity, current_value: $input.body.current_value };"
      }
    },
    {
      "name": "Query Rule Details",
      "type": "n8n-nodes-base.postgres",
      "position": [500, 100],
      "parameters": {
        "operation": "executeQuery",
        "query": "SELECT * FROM compliance_rules WHERE rule_id = '{{ $node['Parse Webhook Data'].json.rule_id }}'"
      }
    },
    {
      "name": "LLM Remediation - GPT-4",
      "type": "n8n-nodes-langchain.llmOpenAI",
      "position": [700, 100],
      "parameters": {
        "model": "gpt-4",
        "prompt": "Generate step-by-step remediation for this security deviation:\\nRule: {{ $node['Query Rule Details'].json[0].name }}\\nCurrent: {{ $node['Parse Webhook Data'].json.current_value }}\\nExpected: {{ $node['Query Rule Details'].json[0].expected_value }}",
        "temperature": 0.2
      }
    },
    {
      "name": "Check Severity",
      "type": "n8n-nodes-base.if",
      "position": [900, 100],
      "parameters": {
        "conditions": {
          "boolean": [
            {
              "value1": "{{ $node['Parse Webhook Data'].json.severity }}",
              "operation": "equals",
              "value2": "CRITICAL"
            }
          ]
        }
      }
    },
    {
      "name": "Auto-Execute (Critical)",
      "type": "n8n-nodes-base.ssh",
      "position": [1100, 50],
      "parameters": {
        "host": "{{ $node['Parse Webhook Data'].json.endpoint_id }}",
        "command": "# Run remediation script\\n{{ $node['LLM Remediation - GPT-4'].json.text }}"
      }
    },
    {
      "name": "Request Approval (Non-Critical)",
      "type": "n8n-nodes-base.slackCreate",
      "position": [1100, 150],
      "parameters": {
        "channel": "#security-approvals",
        "message": "⚠️ Remediation required for {{ $node['Parse Webhook Data'].json.endpoint_id }}\\n{{ $node['LLM Remediation - GPT-4'].json.text }}"
      }
    },
    {
      "name": "Verify Remediation",
      "type": "n8n-nodes-base.httpRequest",
      "position": [1300, 100],
      "parameters": {
        "url": "{{ $secrets.API_URL }}/api/endpoints/{{ $node['Parse Webhook Data'].json.endpoint_id }}/verify",
        "method": "POST",
        "body": "{{ $node['Auto-Execute (Critical)'].json }}"
      }
    },
    {
      "name": "Create Jira Ticket (if failed)",
      "type": "n8n-nodes-base.jira",
      "position": [1500, 100],
      "parameters": {
        "operation": "create",
        "project": "SEC",
        "issueType": "Task",
        "summary": "Failed remediation for {{ $node['Parse Webhook Data'].json.endpoint_id }}",
        "description": "Automatic remediation failed. Manual intervention needed.\\n{{ $node['Verify Remediation'].json.error }}"
      }
    },
    {
      "name": "Slack Notification",
      "type": "n8n-nodes-base.slack",
      "position": [1700, 100],
      "parameters": {
        "channel": "#security-alerts",
        "message": "{{ $node['Verify Remediation'].json.success ? '✅ Remediation successful' : '❌ Remediation failed - Jira ticket created' }}"
      }
    }
  ]
}
```

---

## Workflow 3: Agent Health Monitoring & Auto-Repair

```
Cron: Every 5 minutes
    ↓
Query agent heartbeat table
    ↓
Identify stale agents (>10 min no heartbeat)
    ↓
[Per stale agent:]
    ↓
Ping endpoint via SSH
    ↓
Check agent process status
    ↓
[If crashed] → Restart agent
    ↓
[If endpoint offline] → Mark as offline
    ↓
Create incident ticket
    ↓
Alert ops team
```

**Health Check Workflow:**

```json
{
  "nodes": [
    {
      "name": "Health Check Timer",
      "type": "n8n-nodes-base.cron",
      "parameters": {
        "interval": [5],
        "unit": "minutes"
      }
    },
    {
      "name": "Query Stale Agents",
      "type": "n8n-nodes-base.postgres",
      "parameters": {
        "query": "SELECT * FROM agents WHERE last_heartbeat < NOW() - INTERVAL '10 minutes' AND status = 'active'"
      }
    },
    {
      "name": "Iterate Stale Agents",
      "type": "n8n-nodes-base.itemLists",
      "parameters": {
        "operation": "splitOutItems"
      }
    },
    {
      "name": "SSH Health Check",
      "type": "n8n-nodes-base.ssh",
      "parameters": {
        "host": "{{ $item.json.endpoint_ip }}",
        "command": "systemctl status aespm-agent"
      }
    },
    {
      "name": "Process Status",
      "type": "n8n-nodes-base.if",
      "parameters": {
        "conditions": {
          "string": [
            {
              "value1": "{{ $node['SSH Health Check'].json.stdout }}",
              "operation": "contains",
              "value2": "active (running)"
            }
          ]
        }
      }
    },
    {
      "name": "Restart Agent",
      "type": "n8n-nodes-base.ssh",
      "position": [800, 50],
      "parameters": {
        "host": "{{ $item.json.endpoint_ip }}",
        "command": "sudo systemctl restart aespm-agent"
      }
    },
    {
      "name": "Mark Offline",
      "type": "n8n-nodes-base.postgres",
      "position": [800, 150],
      "parameters": {
        "operation": "executeQuery",
        "query": "UPDATE agents SET status = 'offline' WHERE agent_id = '{{ $item.json.agent_id }}'"
      }
    },
    {
      "name": "Create Incident",
      "type": "n8n-nodes-base.jira",
      "parameters": {
        "operation": "create",
        "project": "OPS",
        "issueType": "Incident",
        "summary": "Agent offline: {{ $item.json.endpoint_name }}",
        "priority": "High"
      }
    },
    {
      "name": "Alert Ops",
      "type": "n8n-nodes-base.slack",
      "parameters": {
        "channel": "#ops-alerts",
        "message": "🚨 Agent offline: {{ $item.json.endpoint_name }}\\nIncident: {{ $node['Create Incident'].json.key }}"
      }
    }
  ]
}
```

---

## Workflow 4: Weekly Trend Analysis & Prediction

```
Cron: Every Monday 8 AM
    ↓
Query 4-week compliance history
    ↓
Feed to Claude → ML trend analysis
    ↓
[Output: Predictions, patterns, anomalies]
    ↓
Generate trend report (HTML)
    ↓
Compare to SLA targets
    ↓
[If below SLA] → Create action items
    ↓
Send to Slack + Email
```

---

## Workflow 5: Configuration Change Detection & Audit

```
Webhook: Config change detected
    ↓
Extract old vs new values
    ↓
Calculate impact score
    ↓
Query DeepSeek → "Is this change authorized?"
    ↓
[Authorized] → Log and continue
    ↓
[Unauthorized] → Alert security team
    ↓
Create audit record
    ↓
Revert if critical
```

---

## Workflow 6: Automated Compliance Report Generation (Multi-Format)

```
Trigger: Report request from dashboard
    ↓
Query database (filters applied)
    ↓
Generate PDF (ReportLab)
    ↓
Generate Excel (openpyxl)
    ↓
Generate JSON export
    ↓
Upload to S3
    ↓
Send download link via email
```

---

## Workflow 7: Integration Testing & Validation

```
Cron: Daily 3 AM
    ↓
Simulate 100 config deviations
    ↓
Feed to AI agents
    ↓
Verify response quality
    ↓
Track metrics (latency, cost, accuracy)
    ↓
[If degradation detected] → Alert
    ↓
Generate quality report
```

---

## n8n Deployment

```bash
# Docker Compose for n8n
docker run -d \
  --name n8n \
  -p 5678:5678 \
  -e N8N_HOST=localhost \
  -e N8N_PORT=5678 \
  -e N8N_PROTOCOL=http \
  -e WEBHOOK_TUNNEL_URL=https://n8n.company.com \
  -v n8n_data:/home/node/.n8n \
  n8nio/n8n

# Access: http://localhost:5678
```

---

## Integration Points with AESPM

| Workflow | Trigger | AI Agent | Action |
|----------|---------|----------|--------|
| 1 | Cron (6 AM) | Claude | Email report |
| 2 | Webhook | GPT-4 | SSH remediation |
| 3 | Cron (5 min) | No AI | SSH restart |
| 4 | Cron (Mon 8 AM) | Claude | Slack update |
| 5 | Webhook | DeepSeek | Audit log |
| 6 | Manual/API | No AI | S3 upload |
| 7 | Cron (3 AM) | All | Quality report |

---

This completes the 7 distinct artifacts for Project 11! Each provides a different perspective:

1. **Project Overview** - High-level architecture
2. **Implementation Checklist** - Step-by-step tasks
3. **Technology Stack** - Tools and installation
4. **Interview Guide** - Talking points and scenarios
5. **Kubernetes Deployment** - Production infrastructure
6. **n8n Workflows** - Automation and AI integration
7. **Resume Points** (interview guide) - Career positioning

All artifacts are interconnected and provide complete coverage for implementing Project 11!

