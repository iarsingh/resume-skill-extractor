from fastapi import FastAPI, HTTPException
from skillsx.extract import extract

app = FastAPI()


@app.get("/healthz")
def healthz():
    return {"status": "ok"}


@app.post("/extract")
def post_extract(body: dict):
    try:
        return extract(body.get("text", ""))
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
