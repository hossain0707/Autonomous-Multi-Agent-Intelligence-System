<div align="center">

# Autonomous Multi-Agent Intelligence System

### Production-oriented orchestration for specialized AI agents, real tools, persistent intelligence and human-controlled automation

[![Live Demo](https://img.shields.io/badge/Live_Demo-Launch-00C7E6?style=for-the-badge&logo=github)](https://hossain0707.github.io/Autonomous-Multi-Agent-Intelligence-System/)
![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-2.0_API-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

**10 specialists · tool permissions · scheduler · approval queue · persistent events · controlled collaboration · priority notifications · REST API**

[Launch Demo](https://hossain0707.github.io/Autonomous-Multi-Agent-Intelligence-System/) · [Run It](#quick-start) · [Real-World Tasks](#running-real-world-tasks) · [API](#api-reference)

</div>

---

## What this project is

This repository is a production-oriented foundation for running specialized AI agents behind a central control plane. Agents do not receive unrestricted access to every integration. Each agent has an explicit tool allow-list; requests flow through the orchestrator; activity is persisted; recurring work can be scheduled; and sensitive write actions have an approval-queue foundation.

The **GitHub Pages demo** visualizes the architecture. The **FastAPI backend** is the executable runtime.

## Architecture

```text
                    API / USER / SCHEDULE
                            │
                            ▼
                 ┌─────────────────────┐
                 │ CENTRAL ORCHESTRATOR│
                 │ validate · route    │
                 └─────────┬───────────┘
                           │
                  ┌────────┴────────┐
                  ▼                 ▼
              TASK QUEUE      APPROVAL QUEUE
                  │            sensitive writes
                  ▼
        ┌───────────────────────┐
        │  SPECIALIST AGENT     │
        │ role + tool allowlist │
        └──────────┬────────────┘
                   ▼
              TOOL REGISTRY
          ┌────────┼─────────┐
          ▼        ▼         ▼
        GitHub    HTTPS     Runtime
          │        │         │
          └────────┼─────────┘
                   ▼
             RESULT / EVENT
                   │
          ┌────────┴─────────┐
          ▼                  ▼
   PERSISTENT MEMORY    IMPORTANCE FILTER
                              │
                              ▼
                         NOTIFICATION
```

### Safety boundary

Read-only tools can execute only when they are explicitly assigned to the selected agent. Write/action tools are designed to go through an approval workflow rather than being silently executed. This is the key boundary between useful autonomy and uncontrolled automation.

## Specialist Agents

| ID | Agent | Domain | Current tool access |
|:--:|---|---|---|
| A1 | AI / LLM Research | models, training, inference | HTTPS JSON |
| A2 | Research Papers | literature/scientific analysis | HTTPS JSON |
| A3 | GitHub Monitor | repositories, issues, Actions | GitHub activity |
| A4 | Career Intelligence | roles/career signals | HTTPS JSON |
| A5 | Market Intelligence | competitive signals | HTTPS JSON |
| A6 | GPU / Infrastructure | compute, serving, reliability | HTTPS JSON, runtime health |
| A7 | Project Manager | planning/dependencies/delivery | reasoning |
| A8 | Email / Documents | communication/documents | reasoning; connector adapter pending |
| A9 | Knowledge Research | research/synthesis | HTTPS JSON |
| A10 | Security Monitor | operational/security risk | GitHub activity, runtime health |

> Tool access is intentionally narrow. Add provider-specific adapters rather than giving every agent arbitrary network or shell access.

## Implemented runtime capabilities

- central task orchestration and bounded priority validation
- ten specialist agent identities and specialties
- per-agent tool allow-lists
- read-only GitHub repository activity adapter
- restricted HTTPS JSON retrieval adapter
- runtime health tool
- optional model-backed generation with demo fallback
- controlled cross-agent delegation
- SQLite event persistence
- recurring interval scheduler persisted in SQLite
- approval request/decision persistence for sensitive actions
- importance-based notification promotion
- Docker Compose runtime with persistent data volume and health check
- REST/OpenAPI interface
- GitHub Actions CI
- separate interactive GitHub Pages visualization

## Quick Start

```bash
git clone https://github.com/hossain0707/Autonomous-Multi-Agent-Intelligence-System.git
cd Autonomous-Multi-Agent-Intelligence-System
cp .env.example .env
docker compose up --build
```

Open **http://localhost:8000/docs** for the interactive API console and **http://localhost:8000/health** for health status.

To enable model-generated responses, set `OPENAI_API_KEY` in `.env`. To let the GitHub tool access private repositories or higher API limits, set a least-privilege `GITHUB_TOKEN`.

## Running real-world tasks

### 1. Run A3 against a real GitHub repository

```bash
curl -X POST http://localhost:8000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "target":"a3",
    "objective":"Review repository activity and identify anything requiring attention.",
    "priority":75,
    "payload":{
      "tool_calls":[{
        "name":"github.repo_activity",
        "args":{"repo":"hossain0707/Autonomous-Multi-Agent-Intelligence-System"}
      }]
    }
  }'
```

The agent receives live issue, pull-request and Actions data, then analyzes the returned tool evidence.

### 2. Schedule the monitor

```bash
curl -X POST http://localhost:8000/api/schedules \
  -H "Content-Type: application/json" \
  -d '{
    "name":"Repository health review",
    "target":"a3",
    "objective":"Review repository activity and flag important changes.",
    "priority":75,
    "interval_seconds":3600,
    "payload":{
      "tool_calls":[{
        "name":"github.repo_activity",
        "args":{"repo":"hossain0707/Autonomous-Multi-Agent-Intelligence-System"}
      }]
    }
  }'
```

The schedule is persisted in SQLite and evaluated by the application scheduler while the service is running.

### 3. Controlled collaboration

```bash
curl -X POST http://localhost:8000/api/collaborate \
  -H "Content-Type: application/json" \
  -d '{"requester":"a1","helper":"a6","objective":"Assess infrastructure implications of this workload.","priority":70}'
```

### 4. Create an approval request

```bash
curl -X POST http://localhost:8000/api/approvals \
  -H "Content-Type: application/json" \
  -d '{"agent":"a3","tool":"github.write","arguments":{"action":"example"},"reason":"A repository-changing operation requires human approval."}'
```

Approval records can then be reviewed and explicitly approved or rejected. The current repository deliberately does **not** ship a generic destructive write executor.

## API Reference

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | runtime status |
| GET | `/api/agents` | agents and permitted tools |
| POST | `/api/tasks` | execute one agent task |
| POST | `/api/collaborate` | controlled agent delegation |
| GET | `/api/history` | persistent task/result/error events |
| GET | `/api/notifications` | priority-promoted results |
| POST | `/api/schedules` | create recurring work |
| GET | `/api/schedules` | list schedules |
| POST | `/api/approvals` | request human approval |
| GET | `/api/approvals` | list approval records |
| POST | `/api/approvals/{id}/decision` | approve/reject a pending request |

## Configuration

```env
APP_NAME=Autonomous Multi-Agent Intelligence System
ENVIRONMENT=development
NOTIFY_THRESHOLD=70
OPENAI_API_KEY=
OPENAI_MODEL=gpt-5-mini
GITHUB_TOKEN=
GITHUB_REPOSITORIES=
SCHEDULER_ENABLED=true
SCHEDULER_TICK_SECONDS=30
APPROVAL_REQUIRED_FOR_WRITES=true
```

Never commit `.env` or production credentials.

## Project Structure

```text
app/
├── agents.py        # agent identities + tool allow-lists
├── config.py        # environment-backed settings
├── main.py          # FastAPI API
├── models.py        # task/result contracts
├── orchestrator.py  # routing, collaboration, approvals
├── provider.py      # optional model provider
├── scheduler.py     # persistent recurring execution
├── storage.py       # SQLite events/schedules/approvals
└── tools.py         # tool registry + real read adapters
docs/
└── index.html       # interactive GitHub Pages demo
```

## Production deployment

The repository now contains the core control-plane patterns, but production readiness depends on the deployment environment. For an Internet-facing, multi-user installation, add an identity-aware gateway, TLS, per-user authorization, a managed PostgreSQL database, Redis/durable workers, distributed scheduling/locking, rate limits, centralized secrets, tracing/metrics/log aggregation, backups, and provider-specific connector adapters.

Do **not** expose the unrestricted HTTPS adapter to untrusted users without an outbound allow-list/proxy. Do **not** attach generic shell execution or broad cloud credentials to agents.

## Extending tools

A production connector should be implemented as a narrow tool with:

1. a typed input contract,
2. least-privilege credentials,
3. an explicit `read` or `write` mode,
4. bounded output,
5. audit events,
6. retries/timeouts,
7. approval for consequential writes.

Then assign that tool only to agents that require it.

## Security

Secrets are environment-backed and excluded from source control. Cross-agent calls pass through the orchestrator, tools are allow-listed by agent, and approval records provide a foundation for human control of consequential actions. Review [SECURITY.md](SECURITY.md) before deployment.

## Roadmap

Next production layers include PostgreSQL/Redis, durable distributed workers, OAuth connector onboarding, webhook/event ingestion, notification providers, per-user workspaces/RBAC, retry and dead-letter queues, OpenTelemetry observability, and provider-specific write executors tied to the approval engine.

## License

MIT — see [LICENSE](LICENSE).

---

<div align="center">

### Hossain Md Najmul
**AI Research Engineer · LLM Training · Multi-Agent Systems · AI Infrastructure**

[Interactive Demo](https://hossain0707.github.io/Autonomous-Multi-Agent-Intelligence-System/) · [GitHub](https://github.com/hossain0707)

</div>
