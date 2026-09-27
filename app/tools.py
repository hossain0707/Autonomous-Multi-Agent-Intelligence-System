import asyncio, json, urllib.parse, urllib.request
from dataclasses import dataclass
from typing import Awaitable, Callable
from .config import settings

ToolHandler = Callable[[dict], Awaitable[dict]]

@dataclass(frozen=True)
class Tool:
    name: str
    description: str
    mode: str
    handler: ToolHandler

class ToolRegistry:
    def __init__(self):
        self._tools: dict[str, Tool] = {}
    def register(self, tool: Tool):
        self._tools[tool.name] = tool
    def get(self, name: str) -> Tool:
        if name not in self._tools:
            raise ValueError(f"Unknown tool: {name}")
        return self._tools[name]
    def describe(self, names):
        return [{"name": self.get(n).name, "description": self.get(n).description, "mode": self.get(n).mode} for n in names]

async def _http_json(url: str, headers=None):
    def run():
        req = urllib.request.Request(url, headers=headers or {"User-Agent": "multi-agent-system"})
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read().decode("utf-8"))
    return await asyncio.to_thread(run)

async def github_repo_activity(args: dict):
    repo = str(args.get("repo", "")).strip()
    if not repo or "/" not in repo:
        raise ValueError("repo must be owner/name")
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "multi-agent-system"}
    if settings.github_token:
        headers["Authorization"] = f"Bearer {settings.github_token}"
    base = f"https://api.github.com/repos/{repo}"
    issues, pulls, runs = await asyncio.gather(
        _http_json(base + "/issues?state=open&per_page=10", headers),
        _http_json(base + "/pulls?state=open&per_page=10", headers),
        _http_json(base + "/actions/runs?per_page=10", headers),
    )
    return {
        "repository": repo,
        "open_issues": [{"number": x["number"], "title": x["title"], "url": x["html_url"]} for x in issues if "pull_request" not in x],
        "open_pull_requests": [{"number": x["number"], "title": x["title"], "url": x["html_url"]} for x in pulls],
        "workflow_runs": [{"name": x["name"], "status": x["status"], "conclusion": x.get("conclusion"), "url": x["html_url"]} for x in runs.get("workflow_runs", [])],
    }

async def fetch_json_url(args: dict):
    url = str(args.get("url", "")).strip()
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme != "https":
        raise ValueError("Only HTTPS URLs are allowed")
    return await _http_json(url)

async def system_health(args: dict):
    return {"status": "ok", "scheduler_enabled": settings.scheduler_enabled, "environment": settings.environment}

registry = ToolRegistry()
registry.register(Tool("github.repo_activity", "Read open issues, pull requests and recent Actions runs for a GitHub repository.", "read", github_repo_activity))
registry.register(Tool("http.fetch_json", "Read JSON from an HTTPS endpoint. Use only trusted endpoints.", "read", fetch_json_url))
registry.register(Tool("system.health", "Read local runtime health/configuration state.", "read", system_health))
