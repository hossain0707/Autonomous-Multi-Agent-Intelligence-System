# Autonomous Multi-Agent Intelligence System

Production-oriented event-driven multi-agent platform with 10 specialist agents, central orchestration, shared memory, controlled agent-to-agent delegation, priority scoring, notifications, API, animated dashboard, and Docker deployment.

## Flow
Scheduler/Webhooks -> Orchestrator -> Message Bus -> Specialist Agents -> Shared Memory -> Notification Intelligence -> User

## Quick start
1. Copy `.env.example` to `.env`
2. Run `docker compose up --build`
3. Open `http://localhost:8000`
4. API docs: `http://localhost:8000/docs`

The included workers run in deterministic demo mode. Add your chosen LLM/search/GitHub/email adapters to `app/agents.py` for live autonomous intelligence.