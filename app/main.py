from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from .db import Destination, SessionLocal, init_db
from .scoring import score


@asynccontextmanager
async def lifespan(app):
    init_db()
    yield


app = FastAPI(title="Access Risk API", lifespan=lifespan)


class ScoreRequest(BaseModel):
    destination_id: int
    needs: dict[str, int] = Field(examples=[{"wheelchair": 3, "medical": 2}])


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/destinations")
def destinations():
    with SessionLocal() as s:
        return [{"id": d.id, "name": d.name} for d in s.query(Destination).order_by(Destination.id)]


@app.post("/score")
def score_destination(req: ScoreRequest):
    with SessionLocal() as s:
        d = s.get(Destination, req.destination_id)
        if d is None:
            raise HTTPException(404, "destination not found")
        try:
            result = score(req.needs, d.features)
        except ValueError as e:
            raise HTTPException(422, str(e)) from e
        return {"destination": d.name, **result}


@app.get("/rank")
def rank(wheelchair: int = 0, low_vision: int = 0, hearing: int = 0, medical: int = 0, dietary: int = 0):
    """Rank every destination from safest to riskiest for one traveler profile."""
    profile = {"wheelchair": wheelchair, "low_vision": low_vision, "hearing": hearing,
               "medical": medical, "dietary": dietary}
    needs = {k: v for k, v in profile.items() if v}
    with SessionLocal() as s:
        rows = [{"destination": d.name, **score(needs, d.features)} for d in s.query(Destination)]
    return sorted(rows, key=lambda r: r["risk"])
