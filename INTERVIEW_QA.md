# resume-skill-extractor — interview questions and answers

[README](README.md) · [Project architecture](PROJECT_ARCHITECTURE.md)

Answers below use this repository’s files and implementation. They distinguish existing behavior from suggested extensions; source links let you verify each walkthrough.

## 1. What problem does resume-skill-extractor address, and what can you demonstrate?

Extract known skills from resume text. Empty text is refused.

I would demonstrate the linked implementation or examples and distinguish that evidence from any planned production features. Start with [`README.md`](README.md).

## 2. How is this repository organized?

- [`src/skillsx/main.py`](src/skillsx/main.py): Implementation or supporting configuration.
- [`src/skillsx/extract.py`](src/skillsx/extract.py): Implementation or supporting configuration.
- [`requirements.txt`](requirements.txt): Implementation or supporting configuration.
- [`src/skillsx/__init__.py`](src/skillsx/__init__.py): Implementation or supporting configuration.
- [`tests/test_extract.py`](tests/test_extract.py): Executable checks and regression examples.
- [`.github/workflows/ci.yml`](.github/workflows/ci.yml): GitHub Actions job definitions.
- [`README.md`](README.md): Project explanations or operating notes.

[PROJECT_ARCHITECTURE.md](PROJECT_ARCHITECTURE.md) contains the component diagram and the implementation walkthrough.

## 3. Can you walk through `extract` and explain the decision it makes?

The main walkthrough here is `extract(text)` in [`src/skillsx/extract.py`](src/skillsx/extract.py#L6).

```python
def extract(text):
    if not isinstance(text, str) or not text.strip():
        raise ValueError("text is empty")
    tokens = set(re.findall(r"[a-z0-9+.#]+", text.lower()))
    found = sorted(skill for skill in SKILLS if skill in tokens or skill in text.lower())
    return {"skills": found, "count": len(found)}
```

The implementation calls `ValueError`, `isinstance`, `len`, `re.findall`, `set`, `sorted`, `text.lower`, `text.strip`. In an interview, trace those calls in execution order using a fixture input.

## 4. What input validation and failure behavior are implemented?

Explicit failure paths include:

- `ValueError('text is empty')` in [`src/skillsx/extract.py`](src/skillsx/extract.py#L8).
- `HTTPException(status_code=422, detail=str(exc))` in [`src/skillsx/main.py`](src/skillsx/main.py#L17).

I would test both the condition that reaches each exception and the caller that translates it. An explicit raise does not mean every malformed input or dependency failure is handled.

## 5. Which test would you use to demonstrate correctness?

[`tests/test_extract.py`](tests/test_extract.py#L7) contains `test_extracts_known_skills`:

```python
def test_extracts_known_skills():
    payload = client.post("/extract", json={"text": 'Built FastAPI services on Kubernetes and Terraform for GCP.'}).json()
    assert "kubernetes" in payload["skills"]
```

This is a concrete regression example from the repository. Its assertions establish that case; they do not establish behavior for every input or under production load.

## 6. What HTTP interface does the code expose?

- `GET /healthz` → `healthz` in [`src/skillsx/main.py`](src/skillsx/main.py#L8).
- `POST /extract` → `post_extract` in [`src/skillsx/main.py`](src/skillsx/main.py#L13).

These are literal decorators. Application/router prefixes, authentication, and middleware must be checked in the corresponding setup code.

## 7. Where does state live, and what happens with multiple workers?

Module-level containers include `SKILLS` in [`src/skillsx/extract.py`](src/skillsx/extract.py).

These containers belong to a Python process. Inspect which are constant fixtures and which are mutated. Mutable process state needs an explicit shared-storage or synchronization strategy before multiple workers can provide consistent behavior.

## 8. How would another engineer reproduce your walkthrough?

Start from the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -q
```

These commands follow repository manifests; environment setup and command results still need to be checked on the target machine.

## 9. What does automation verify, and what does it not prove?

Inspect [`.github/workflows/ci.yml`](.github/workflows/ci.yml) for triggers, permissions, and job commands. I would name the checks that those definitions run and show the latest run separately. A workflow definition alone does not establish a successful deployment, security review, or production SLO.

## 10. How would you present this project in a Forward Deployed Engineer interview?

Start with the user and operational problem described in [`README.md`](README.md). Explain one constraint that changes the implementation, show the linked code or example, and walk through a success case and a failure case. Agree on a measurable acceptance criterion before expanding the solution, and leave a handoff with data boundaries and rollback ownership. Any proposed production or business metric should be identified as a target until measured.

## 11. What is the input-to-output contract of `extract`?

In [`src/skillsx/extract.py`](src/skillsx/extract.py#L6), `extract(text)` receives the inputs. The function computes these intermediate values:

- `tokens = set(re.findall('[a-z0-9+.#]+', text.lower()))`
- `found = sorted((skill for skill in SKILLS if skill in tokens or skill in text.lower()))`

Its result is defined by:

- `{'skills': found, 'count': len(found)}`

## 12. Which decision rules or boundary conditions should an interviewer challenge?

The implementation in [`src/skillsx/extract.py`](src/skillsx/extract.py#L6) branches on:

- `not isinstance(text, str) or not text.strip()`

A useful extension is a table-driven test that covers each condition just below, at, and above its boundary where applicable. These expressions are the current rules; changing them changes behavior and should be justified by the project’s acceptance criteria.

## Request flow diagram

The mermaid decision tree for `POST /extract` is in [docs/PROCESS_FLOW.md](docs/PROCESS_FLOW.md). Use it in interviews to walk hold/refuse/422 vs a successful lab response without implying a production side effect.

