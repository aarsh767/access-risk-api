# Access Risk API

A small containerized service that scores how risky a destination is for a traveler with
specific accessibility needs (wheelchair, low vision, hearing, medical, dietary), and explains
which missing features drove the score. All data is synthetic.

Built to practice CI/CD with Docker and GitHub Actions.

## Run it
```bash
docker compose up --build
# then open http://localhost:8000/docs
```

## Try it
```bash
curl "localhost:8000/rank?wheelchair=3&medical=2"
curl -X POST localhost:8000/score -H "Content-Type: application/json" \
     -d '{"destination_id": 2, "needs": {"wheelchair": 3}}'
```

## Pipeline (`.github/workflows/ci.yml`)
| Job | Runs on | What it does |
|---|---|---|
| `test` | every push and PR | ruff lint + pytest (unit and API tests) |
| `integration` | after `test` | `docker compose up` with real Postgres, smoke-tests the running container over HTTP |
| `publish` | pushes to `main` only | builds the image and pushes it to GitHub Container Registry |

## Run tests locally
```bash
pip install -r requirements-dev.txt
pytest -v
```
