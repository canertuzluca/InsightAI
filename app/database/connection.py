
"""from sqlalchemy import create_engine

DATABASE_URL = (
    "postgresql+psycopg2://postgres:postgres@localhost:5432/insight_ai"
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)"""

from sqlalchemy import create_engine

from app.config.settings import get_settings

settings = get_settings()

engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
)