# resume-skill-extractor — project architecture

[README](README.md) · [Interview questions and answers](INTERVIEW_QA.md)

## Purpose and scope

Extract known skills from resume text. Empty text is refused.

This document describes files and symbols in this checkout. Deployment templates and statements in the original overview are distinguished from a verified running environment.

## Component diagram

```mermaid
flowchart LR
    M0["src/skillsx/__init__.py"]
    M1["src/skillsx/extract.py"]
    M2["src/skillsx/main.py"]
    M2 -->|imports| M1
```

For Python repositories, arrows show resolved local imports, not network calls or deployment order. Otherwise the diagram is a repository component map; containment arrows do not assert runtime integration.

## Components and responsibilities

| Component | Responsibility |
| --- | --- |
| [`src/skillsx/main.py`](src/skillsx/main.py) | HTTP handlers: `GET /healthz`, `POST /extract` |
| [`src/skillsx/extract.py`](src/skillsx/extract.py) | Functions: `extract` |
| [`requirements.txt`](requirements.txt) | Implementation or supporting configuration |
| [`src/skillsx/__init__.py`](src/skillsx/__init__.py) | Implementation or supporting configuration |
| [`tests/test_extract.py`](tests/test_extract.py) | Executable checks and regression examples |
| [`.github/workflows/ci.yml`](.github/workflows/ci.yml) | GitHub Actions job definitions |
| [`README.md`](README.md) | Project explanations or operating notes |

## Request interface

| Method and path | Handler | Source |
| --- | --- | --- |
| `GET /healthz` | `healthz` | [`src/skillsx/main.py`](src/skillsx/main.py#L8) |
| `POST /extract` | `post_extract` | [`src/skillsx/main.py`](src/skillsx/main.py#L13) |

The table lists literal route decorators found in the inspected Python modules. Router prefixes and middleware can add behavior; check the linked handler and application setup before calling an endpoint.

## Implementation walkthrough

### `extract(text)`

Source: [`src/skillsx/extract.py`](src/skillsx/extract.py#L6).

Calls visible in this function: `ValueError`, `isinstance`, `len`, `re.findall`, `set`, `sorted`, `text.lower`, `text.strip`.

```python
def extract(text):
    if not isinstance(text, str) or not text.strip():
        raise ValueError("text is empty")
    tokens = set(re.findall(r"[a-z0-9+.#]+", text.lower()))
    found = sorted(skill for skill in SKILLS if skill in tokens or skill in text.lower())
    return {"skills": found, "count": len(found)}
```

## Validation and failure paths

| Explicit exception | Source |
| --- | --- |
| `ValueError('text is empty')` | [`src/skillsx/extract.py`](src/skillsx/extract.py#L8) |
| `HTTPException(status_code=422, detail=str(exc))` | [`src/skillsx/main.py`](src/skillsx/main.py#L17) |

These are explicit exceptions in the inspected source, rather than a claim that every failure is handled. Follow the calling handler to see whether the exception becomes an HTTP response or propagates.

## Data and state

- [`src/skillsx/extract.py`](src/skillsx/extract.py) defines module-level containers: `SKILLS`.

Module-level dictionaries/lists live in a Python process. They can be fixtures or mutable state; inspect writes before treating them as persistent storage. A production extension would need to define persistence and concurrency behavior explicitly.

## Data flow and design decisions

### What is the input-to-output contract of `extract`

In [`src/skillsx/extract.py`](src/skillsx/extract.py#L6), `extract(text)` receives the inputs. The function computes these intermediate values:

- `tokens = set(re.findall('[a-z0-9+.#]+', text.lower()))`
- `found = sorted((skill for skill in SKILLS if skill in tokens or skill in text.lower()))`

Its result is defined by:

- `{'skills': found, 'count': len(found)}`

### Which decision rules or boundary conditions should an interviewer challenge

The implementation in [`src/skillsx/extract.py`](src/skillsx/extract.py#L6) branches on:

- `not isinstance(text, str) or not text.strip()`

A useful extension is a table-driven test that covers each condition just below, at, and above its boundary where applicable. These expressions are the current rules; changing them changes behavior and should be justified by the project’s acceptance criteria.

## Setup and verification

The following commands are derived from the checked-in dependency/test contracts. Execute them from the repository root; the block prepares a local environment, not a cloud deployment.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -q
```

Python dependencies: [`requirements.txt`](requirements.txt).

Test entry points: [`tests/test_extract.py`](tests/test_extract.py).

Automation definitions: [`.github/workflows/ci.yml`](.github/workflows/ci.yml). Read their triggers and job steps to determine what CI actually runs.

## Operating boundaries and design review

Before turning this checkout into a customer deployment, establish the input contract, data ownership, access controls, failure response, evaluation criteria, and rollback owner. Repository fixtures and unit tests demonstrate local behavior; they do not establish throughput, uptime, compliance, or business impact.

A useful architecture review starts with the linked implementation: identify where input enters, where a decision is made, which state can change, and which external dependency can fail. Add a deployment view only for infrastructure that is actually configured and exercised.

## Request flow

The decision flow for `POST /extract` is in [docs/PROCESS_FLOW.md](docs/PROCESS_FLOW.md).

```mermaid
flowchart LR
  C["Client JSON"] --> A["FastAPI src/skillsx/main.py"]
  A --> H["POST /extract"]
  H --> D["extract.py"]
  D --> R["JSON result or HTTP 422"]
```

