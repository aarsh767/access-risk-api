from fastapi.testclient import TestClient

from app.main import app


def test_end_to_end():
    with TestClient(app) as c:
        assert c.get("/health").json() == {"status": "ok"}
        dests = c.get("/destinations").json()
        assert len(dests) == 4
        r = c.post("/score", json={"destination_id": 2, "needs": {"wheelchair": 3}}).json()
        assert r["destination"] == "Old Town Walking Tour" and r["gaps"] == ["step_free_access"]
        assert c.post("/score", json={"destination_id": 99, "needs": {}}).status_code == 404
        assert c.post("/score", json={"destination_id": 1, "needs": {"x": 1}}).status_code == 422
        ranked = c.get("/rank", params={"wheelchair": 3, "medical": 2}).json()
        assert ranked[0]["destination"] == "Harbor City Museum"
