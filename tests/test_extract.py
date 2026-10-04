from fastapi.testclient import TestClient
from skillsx.main import app

client = TestClient(app)


def test_extracts_known_skills():
    payload = client.post("/extract", json={"text": 'Built FastAPI services on Kubernetes and Terraform for GCP.'}).json()
    assert "kubernetes" in payload["skills"]


def test_empty_is_refused():
    assert client.post("/extract", json={"text": ""}).status_code == 422
