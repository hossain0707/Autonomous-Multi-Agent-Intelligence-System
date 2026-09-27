<div align="center">

# Autonomous Multi-Agent Intelligence System

### Orchestrated specialist agents for research, engineering, intelligence, operations, and secure collaboration

[![Live Demo](https://img.shields.io/badge/Live_Demo-Launch-00C7E6?style=for-the-badge&logo=github)](https://hossain0707.github.io/Autonomous-Multi-Agent-Intelligence-System/)
![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

**10 specialist agents · central orchestration · persistent event memory · controlled collaboration · priority-aware notifications · REST API · interactive dashboard**

[Launch Demo](https://hossain0707.github.io/Autonomous-Multi-Agent-Intelligence-System/) · [Architecture](#architecture) · [Quick Start](#quick-start) · [API](#api-reference)

</div>

---

## Overview

**Autonomous Multi-Agent Intelligence System** is an experimental platform for coordinating specialized AI agents through a central orchestration layer. Tasks and collaboration requests pass through a controlled routing point for validation, priority handling, persistence, and notification decisions instead of unrestricted recursive agent calls.

The repository combines a **FastAPI backend**, **10 specialist agents**, optional model-backed generation, **SQLite event history**, Docker deployment, REST/OpenAPI interfaces, health checks, CI, and an interactive browser experience.

> **Demo vs. backend:** the GitHub Pages application is an interactive visualization of the system concept. The FastAPI service runs separately when this repository is deployed locally or on infrastructure.

## 🚀 Interactive Demo

<div align="center">

[![Launch Interactive Multi-Agent System](https://img.shields.io/badge/▶_LAUNCH_INTERACTIVE_SYSTEM-00C7E6?style=for-the-badge&logo=github&logoColor=white)](https://hossain0707.github.io/Autonomous-Multi-Agent-Intelligence-System/)

</div>

Run individual agents, start Autonomous Mode, simulate scheduled events, change priority, and visualize controlled agent-to-agent collaboration across the orchestrator, event bus, notification layer, and persistent memory.

## Architecture

```text
                         ┌──────────────────────────┐
                         │          USER            │
                         └────────────┬─────────────┘
                                      ▲
                         ┌────────────┴─────────────┐
                         │    NOTIFICATION LAYER    │
                         │   filter · rank · alert  │
                         └────────────┬─────────────┘
                                      ▲
                    ┌─────────────────┴─────────────────┐
                    │       CENTRAL ORCHESTRATOR        │
                    │ routing · validation · priority   │
                    └─────────────────┬─────────────────┘
                                      ↕
                    ┌─────────────────┴─────────────────┐
                    │        EVENT / MESSAGE BUS        │
                    └─────┬─────┬─────┬─────┬─────┬───┘
                          ↕     ↕     ↕     ↕     ↕
                         A1    A2    A3    ...   A10
                                      ↕
                         ┌────────────┴─────────────┐
                         │    PERSISTENT MEMORY     │
                         │     events · results     │
                         └──────────────────────────┘
```

**Execution path:** Request → validation → orchestrator → queue → specialist agent → result/event → persistent store → importance filter → notification.

Cross-agent delegation is deliberately routed through the orchestrator rather than allowing uncontrolled recursive calls.

## Specialist Agents

| ID | Specialist | Responsibility |
|:--:|---|---|
| **A1** | AI / LLM Research | Models, training, inference |
| **A2** | Research Papers | Literature and scientific analysis |
| **A3** | GitHub Monitor | Repositories, issues, releases |
| **A4** | Career Intelligence | Roles and career signals |
| **A5** | Market Intelligence | Competitive signals |
| **A6** | GPU / Infrastructure | Compute, serving, reliability |
| **A7** | Project Manager | Planning, dependencies, delivery |
| **A8** | Email / Documents | Communication and documents |
| **A9** | Knowledge Research | Research and synthesis |
| **A10** | Security Monitor | Security and operational risk |

## Core Capabilities

- **Central orchestration** — validates targets and coordinates task execution through a shared queue.
- **Controlled collaboration** — specialists request help through the orchestrator with requester/helper validation.
- **Persistent event history** — tasks and results are stored in SQLite with timestamps, importance values, and metadata.
- **Priority-aware notifications** — results meeting the configured threshold are promoted to the notification stream.
- **Optional model provider** — model-backed responses can be enabled with an API key; safe demo fallback remains available without one.
- **REST + OpenAPI** — task, collaboration, agent, notification, history, and health interfaces.
- **Containerized runtime** — Docker Compose includes persistent storage, restart policy, and health checking.
- **Interactive visualization** — GitHub Pages provides the animated multi-agent control-center experience.

## Technology Stack

| Layer | Technology |
|---|---|
| Application/API | Python 3.12 · FastAPI |
| Validation/config | Pydantic · pydantic-settings |
| ASGI server | Uvicorn |
| Persistence | SQLite |
| Model integration | Optional OpenAI Responses API adapter |
| Deployment | Docker · Docker Compose |
| CI | GitHub Actions |
| Demo hosting | GitHub Pages |
| API documentation | OpenAPI · Swagger UI |

## Quick Start

### Docker

```bash
git clone https://github.com/hossain0707/Autonomous-Multi-Agent-Intelligence-System.git
cd Autonomous-Multi-Agent-Intelligence-System
cp .env.example .env
docker compose up --build
```

Then open **http://localhost:8000**. Swagger/OpenAPI documentation is available at **http://localhost:8000/docs** and the health endpoint at **http://localhost:8000/health**.

### Local Python

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

## Configuration

Copy `.env.example` to `.env`:

```env
APP_NAME=Autonomous Multi-Agent Intelligence System
ENVIRONMENT=development
NOTIFY_THRESHOLD=70
OPENAI_API_KEY=
OPENAI_MODEL=gpt-5-mini
```

The API key is optional for demo mode. Never commit `.env`, API keys, tokens, passwords, or production credentials.

## API Reference

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/health` | Status, agent count, queue depth |
| `GET` | `/api/agents` | List specialist agents |
| `POST` | `/api/tasks` | Submit a task |
| `POST` | `/api/collaborate` | Submit a controlled cross-agent request |
| `GET` | `/api/notifications` | Read recent promoted results |
| `GET` | `/api/history?limit=50` | Read persistent event history |
| `GET` | `/docs` | Swagger/OpenAPI documentation |

### Submit a task

```bash
curl -X POST http://localhost:8000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"target":"a1","objective":"Analyze model-training findings","payload":{},"priority":75}'
```

### Request collaboration

```bash
curl -X POST http://localhost:8000/api/collaborate \
  -H "Content-Type: application/json" \
  -d '{"requester":"a1","helper":"a6","objective":"Assess infrastructure implications","priority":70}'
```

## Project Structure

```text
.
├── app/
│   ├── agents.py          # specialist definitions
│   ├── config.py          # environment configuration
│   ├── main.py            # FastAPI routes + backend dashboard
│   ├── models.py          # task/result models
│   ├── orchestrator.py    # routing, queue, collaboration, notifications
│   ├── provider.py        # optional model provider
│   └── storage.py         # SQLite event store
├── docs/
│   └── index.html         # GitHub Pages interactive demo
├── .github/workflows/
│   └── ci.yml             # continuous integration
├── .env.example
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── SECURITY.md
└── LICENSE
```

## Persistence & Notification Logic

Submitted tasks and completed results are persisted as events. History retrieval is bounded by the API, while result importance determines whether an item is promoted to the notification stream. The default `NOTIFY_THRESHOLD` is **70** and is configurable through the environment.

## Security & Production Deployment

The repository intentionally ships without real credentials. Use environment variables or a secrets manager and least-privilege credentials for integrations.

Before exposing the backend publicly, add **HTTPS, authentication/authorization, rate limiting, centralized logs/metrics, and a production database architecture**. See [SECURITY.md](SECURITY.md) for security guidance.

## Production Roadmap

For larger multi-user or multi-instance deployments, the next engineering layers include durable background workers and scheduling, PostgreSQL/Redis, identity and per-user workspaces, connector permission management, retries/idempotency/dead-letter handling, observability and tracing, approval gates for sensitive actions, configurable notification channels, and richer agent lifecycle management.

## Design Principles

**Controlled autonomy** — orchestration boundaries govern collaboration.  
**Specialization** — each agent owns a defined intelligence domain.  
**Traceability** — task/result events create an inspectable history.  
**Progressive deployment** — start in demo mode and enable model/infrastructure capabilities as needed.

## License

Released under the [MIT License](LICENSE).

---

<div align="center">

### MD NAJMUL HOSSAIN 

**AI Research Engineer · LLM & Multi-Agent Systems**

[Live Demo](https://hossain0707.github.io/Autonomous-Multi-Agent-Intelligence-System/) · [GitHub Profile](https://github.com/hossain0707)

</div>
