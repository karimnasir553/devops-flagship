import secrets

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from prometheus_fastapi_instrumentator import Instrumentator
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import Base, engine, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI(title="URL Shortener", version="0.1.0")

# Exposes Prometheus metrics at /metrics
Instrumentator().instrument(app).expose(app)


def _generate_code(length: int = 6) -> str:
    return secrets.token_urlsafe(length)[:length]


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/shorten", response_model=schemas.URLInfo, status_code=201)
def shorten(payload: schemas.URLCreate, db: Session = Depends(get_db)) -> models.URL:
    code = _generate_code()
    while db.query(models.URL).filter_by(short_code=code).first():
        code = _generate_code()
    url = models.URL(short_code=code, target_url=str(payload.target_url))
    db.add(url)
    db.commit()
    db.refresh(url)
    return url


@app.get("/stats/{short_code}", response_model=schemas.URLInfo)
def stats(short_code: str, db: Session = Depends(get_db)) -> models.URL:
    url = db.query(models.URL).filter_by(short_code=short_code).first()
    if url is None:
        raise HTTPException(status_code=404, detail="Short code not found")
    return url


@app.get("/{short_code}")
def redirect(short_code: str, db: Session = Depends(get_db)) -> RedirectResponse:
    url = db.query(models.URL).filter_by(short_code=short_code).first()
    if url is None:
        raise HTTPException(status_code=404, detail="Short code not found")
    url.clicks += 1
    db.commit()
    return RedirectResponse(url.target_url)
