# Security
Do not commit API keys, tokens, passwords, private documents, or production credentials.
Use environment variables or a secrets manager. The application intentionally routes cross-agent requests through the orchestrator to reduce uncontrolled delegation. Before exposing the service publicly, place it behind HTTPS and an identity-aware reverse proxy/API gateway.
Report security issues privately to the repository owner rather than opening a public issue.
