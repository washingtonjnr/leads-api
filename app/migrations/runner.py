from app.core.database import get_database

from . import (
    create_leads_indexes,
)

MIGRATIONS = [
    create_leads_indexes,
]

async def run_migrations():
    db = get_database()

    for migration in MIGRATIONS:
        await migration.run(db)