# MoneySense

**MoneySense** is an early-stage financial literacy project built with **Python, FastAPI, and the Model Context Protocol (MCP)**. It exposes a small financial terminology dictionary to MCP-compatible clients so they can look up and search banking and finance terms.

> **Status:** Prototype (application version `0.1.0`). The current dictionary contains three sample entries and is stored in Python code. This repository is not yet a production-ready financial advice service.

## Features

- **MCP tools** for retrieving and searching financial terms.
- **Case-insensitive term lookup** by abbreviation.
- **Substring search** across code, English and Russian names, category, and description.
- **HTTP API** powered by FastAPI with basic root and health endpoints.
- **Docker** and Docker Compose configuration.

### MCP tools

| Tool | Input | Output |
| --- | --- | --- |
| `get_financial_term` | `term: str` | A matching term or a `found: false` response |
| `search_financial_terms` | `query: str` | A list of matching terms |

Currently included terms:

| Code | English name | Russian name | Category |
| --- | --- | --- | --- |
| EIR | Effective Interest Rate | Эффективная процентная ставка | lending |
| PD | Probability of Default | Вероятность дефолта | risk |
| LGD | Loss Given Default | Убыток при дефолте | risk |

Example successful `get_financial_term(term="PD")` result:

```json
{
  "found": true,
  "code": "PD",
  "name": "Probability of Default",
  "name_ru": "Вероятность дефолта",
  "category": "risk",
  "description": "Вероятность того, что заемщик перейдет в состояние дефолта за определенный период."
}
```

For an unknown abbreviation, the tool returns:

```json
{
  "found": false,
  "query": "UNKNOWN",
  "message": "Financial term not found"
}
```

## Technology stack

- Python 3.12 (Docker image)
- FastAPI
- MCP Python SDK (`mcp[cli]`)
- Uvicorn
- Pydantic
- Docker / Docker Compose

Dependencies are specified in `requirements.txt` without pinned versions.

## Project layout

```text
MoneySense/
├── app/
│   ├── main.py                       # FastAPI application and MCP mount
│   ├── mcp_server.py                 # MCP server configuration
│   ├── schemas/
│   │   └── term.py                   # FinancialTerm schema
│   ├── services/
│   │   └── dictionary_service.py     # Built-in terms and lookup/search logic
│   └── tools/
│       └── dictionary.py             # MCP tool registration
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Run locally

Requires Python 3.12 or a compatible Python version.

```bash
git clone https://github.com/Antonshk2013/MoneySense.git
cd MoneySense

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

On Windows, activate the environment using `.venv\\Scripts\\activate` in Command Prompt or `.venv\\Scripts\\Activate.ps1` in PowerShell.

## Run with Docker Compose

```bash
docker compose up --build -d
docker compose logs -f moneysense
```

Stop the service:

```bash
docker compose down
```

The current Compose configuration publishes port **8000** on the host (`8000:8000`). Do not deploy this configuration to a public server without reviewing network exposure and adding appropriate access controls.

## HTTP endpoints

The FastAPI application declares these routes:

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/` | Application information |
| GET | `/health` | Basic health status |
| MCP | `/mcp` | Streamable HTTP transport for MCP clients (intended mount) |

Check health locally:

```bash
curl http://127.0.0.1:8000/health
```

Expected response from the declared health handler:

```json
{
  "status": "ok",
  "service": "moneysense-mcp",
  "version": "0.1.0"
}
```

**Implementation note:** `app/main.py` mounts the MCP ASGI application under `/`. Verify the effective MCP URL and SDK compatibility against the installed `mcp` package before configuring a client; the routes and startup have not been integration-tested as part of this documentation update.

## How to extend the dictionary

Add a `FinancialTerm` entry to `TERMS` in `app/services/dictionary_service.py`:

```python
"apr": FinancialTerm(
    code="APR",
    name="Annual Percentage Rate",
    name_ru="Годовая процентная ставка",
    category="lending",
    description="Годовая процентная ставка по кредиту.",
),
```

`get_financial_term` resolves the dictionary key after trimming spaces and converting to lowercase; `search_financial_terms` searches the text fields using case-insensitive substring matching. Restart the application after making changes.

## Roadmap

Possible next steps (not yet implemented):

- Expand and externalize the financial glossary.
- Add Ukrainian and other language support.
- Add unit/integration tests and automated CI checks.
- Pin dependency versions and verify MCP SDK API compatibility.
- Add deployment configuration, authentication, and rate limiting.
- Add more tools for financial education and calculations.

## Disclaimer

MoneySense is an educational prototype. Its terminology explanations are not financial, legal, or investment advice.
