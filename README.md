# AI-Powered Customer Support Agent

Portfolio-grade reference implementation combining **AI Agents, Tool Calling, RAG and Automation** using Python and Java.

## Architecture

```text
Client
  -> Java 21 / Spring Boot Gateway (:8080)
       -> Python / FastAPI Agent Service (:8000)
            |-> Intent / agent policy
            |-> RAG knowledge-base search
            |-> Customer tool
            |-> Order/tracking tool
            |-> Ticket automation tool
            |-> Refund tool (approval gated)
            `-> Conversation memory
```

The included implementation is deliberately local and deterministic: RAG uses TF-IDF/cosine retrieval so the project runs without API keys. The `SupportAgent` boundary is where an OpenAI/Azure OpenAI/open-source LLM planner can be plugged in while retaining deterministic tool authorization.

## Key capabilities

- Knowledge-base grounded answers with returned sources/scores/excerpts
- Tool calling for customer profile and order status
- Automation for ticket creation and refund requests
- Explicit approval gate for state-changing actions
- Customer/order ownership checks to prevent cross-customer access
- Conversation memory keyed by customer + conversation
- Java gateway suitable for auth/rate limits/enterprise integrations
- Docker Compose and tests

## Run locally

### Python
```bash
cd python-service
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Java
Requires Java 21 and Maven.
```bash
cd java-service
mvn spring-boot:run
```

Then POST to `http://localhost:8080/api/support/chat`.

### Docker
```bash
docker compose up --build
```

## Example
```bash
curl -X POST http://localhost:8080/api/support/chat \
 -H 'Content-Type: application/json' \
 -d '{"customer_id":"cust-1001","message":"Where is ORD-501?","allow_actions":false}'
```

Refund request without approval:
```json
{"customer_id":"cust-1001","message":"Refund ORD-502","allow_actions":false}
```
returns `requires_approval: true`. Re-submit only after an authenticated UI/user approval with `allow_actions: true`.

## Tests
```bash
cd python-service
PYTHONPATH=. pytest -q
```

## Production evolution

For a production portfolio, replace the local stores with PostgreSQL/Redis, TF-IDF with hybrid BM25 + vector retrieval and a reranker, and add an LLM planner with structured tool schemas. Add OAuth/OIDC, per-tool RBAC, policy engine, idempotency keys, durable workflows, Kafka, human-in-the-loop approvals, PII redaction, prompt-injection defenses, OpenTelemetry traces, evaluation datasets, groundedness/tool-call metrics, Kubernetes, autoscaling, circuit breakers and SLO dashboards. Keep the tool execution layer deterministic even when an LLM chooses a tool.
