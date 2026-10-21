import os

from sqlalchemy import JSON, Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./local.db")
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


class Destination(Base):
    __tablename__ = "destinations"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    features = Column(JSON, nullable=False)


# Synthetic sample data only; no real sponsor data.
FEATURES = ["step_free_access", "tactile_signage", "visual_alerts", "hospital_within_10km", "allergen_labeling"]
SEED = [
    ("Harbor City Museum", [1, 1, 1, 1, 0]),
    ("Old Town Walking Tour", [0, 0, 0, 1, 0]),
    ("Lakeside Resort", [1, 0, 1, 0, 1]),
    ("Mountain Cable Car", [1, 0, 0, 0, 0]),
]


def init_db():
    Base.metadata.create_all(engine)
    with SessionLocal() as s:
        if not s.query(Destination).first():
            s.add_all(Destination(name=n, features=dict(zip(FEATURES, map(bool, f), strict=True))) for n, f in SEED)
            s.commit()
