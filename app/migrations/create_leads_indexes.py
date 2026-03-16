async def run(db):
    await db.leads.create_index("email", unique=True)
    await db.leads.create_index("external_id", unique=True)