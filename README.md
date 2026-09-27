# Autonomous Multi-Agent Intelligence System

A user-friendly autonomous multi-agent platform: 10 specialist agents, central orchestration, persistent event history, controlled collaboration, priority-based notifications, REST API, animated dashboard, Docker deployment, health checks and CI.

## ✨ Live Architecture Preview

> **Interactive controls cannot run inside a GitHub README itself** because GitHub strips JavaScript and iframes. The full live experience is therefore provided by the repository's `docs/index.html` app, while the README shows a clean architecture overview.

<table>
<tr>
<td align="center"><b>👤 USER</b><br><sub>Dashboard · Mobile · Alerts</sub></td>
<td align="center">⬆️</td>
<td align="center"><b>🔔 NOTIFICATION INTELLIGENCE</b><br><sub>Filter · Rank · Summarize</sub></td>
</tr>
<tr>
<td></td><td align="center">⬆️</td><td></td>
</tr>
<tr>
<td colspan="3" align="center"><b>🧠 CENTRAL ORCHESTRATOR</b><br><sub>Routing · Permissions · Priority · Retry · Coordination</sub></td>
</tr>
<tr>
<td colspan="3" align="center">↕️<br><b>⚡ EVENT / MESSAGE BUS</b><br><sub>task.created · agent.request · result.ready · alert.detected</sub></td>
</tr>
<tr>
<td align="center">🔬 <b>A1 LLM Research</b><br>📚 <b>A2 Papers</b><br>💻 <b>A3 GitHub</b><br>💼 <b>A4 Career</b><br>📊 <b>A5 Market</b></td>
<td align="center"><b>↔️</b><br><sub>controlled<br>collaboration</sub></td>
<td align="center">🖥️ <b>A6 Infrastructure</b><br>📋 <b>A7 Projects</b><br>📧 <b>A8 Documents</b><br>🌐 <b>A9 Knowledge</b><br>🛡️ <b>A10 Security</b></td>
</tr>
<tr>
<td colspan="3" align="center">⬇️<br><b>💾 PERSISTENT MEMORY</b><br><sub>History · Context · Results</sub></td>
</tr>
</table>

### 🎮 Interactive Demo

The interactive demo is already included at **`docs/index.html`**. Once GitHub Pages is enabled for this repository, visitors can run Autonomous Mode, scheduled events, individual agents, priority-based notifications, and agent-to-agent collaboration directly in their browser.

**Live URL after Pages is enabled:**  
`https://hossain0707.github.io/Autonomous-Multi-Agent-Intelligence-System/`

**Enable it once:** **Repository Settings → Pages → Build and deployment → Deploy from a branch → `main` → `/docs` → Save.**

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
