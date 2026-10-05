# Resume Skill Extractor: process flows

## Domain request

Endpoint: `POST /extract`. Stages summarize [src/skillsx/extract.py](../src/skillsx/extract.py). This is in-process Python, not a hosted model or production apply.

```mermaid
flowchart TD
  A["POST /extract"] --> B{"Valid input?"}
  B -->|"No"| E["HTTP 422"]
  B -->|"Yes: Non-empty text"| C["Domain function in extract.py"]
  C --> O["closed-lexicon skills list"]
  O --> X["No production side effect"]
```

See [INTERVIEW_QA.md](../INTERVIEW_QA.md) for fixture walkthroughs and [PROJECT_ARCHITECTURE.md](../PROJECT_ARCHITECTURE.md) for the component map.
