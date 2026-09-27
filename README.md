# Autonomous Multi-Agent Intelligence System

A user-friendly autonomous multi-agent platform: 10 specialist agents, central orchestration, persistent event history, controlled collaboration, priority-based notifications, REST API, animated dashboard, Docker deployment, health checks and CI.

## 60-second setup
```bash
git clone https://github.com/hossain0707/Autonomous-Multi-Agent-Intelligence-System.git
cd Autonomous-Multi-Agent-Intelligence-System
cp .env.example .env
docker compose up --build
```
Then open **http://localhost:8000**. API documentation is at **http://localhost:8000/docs**.

It works immediately in safe demo mode. To enable model-generated agent responses, put your API key in `.env` as `OPENAI_API_KEY=...` and restart Docker. Never commit the `.env` file.

## Architecture
Scheduler / API / Webhooks → Orchestrator → Specialist Agent → Persistent Memory → Importance Filter → User

Cross-agent delegation always passes through the orchestrator rather than allowing uncontrolled recursive calls.

## Agents
AI/LLM Research · Research Papers · GitHub Monitor · Career Intelligence · Market Intelligence · GPU/Infrastructure · Project Manager · Email/Documents · Knowledge Research · Security Monitor

## Production foundations
- Dockerized FastAPI application
- persistent SQLite event store (Docker volume)
- environment-based secrets
- optional model provider
- health endpoint
- GitHub Actions CI
- input validation and bounded importance scores
- controlled cross-agent delegation
- interactive browser dashboard
- REST API and OpenAPI docs
- security guidance

## Before public Internet deployment
Put the service behind HTTPS and authentication/API gateway, use a managed database for multi-instance deployment, add rate limiting and centralized logs/metrics, and configure external connectors with least-privilege credentials. The repository intentionally does not ship real credentials.
