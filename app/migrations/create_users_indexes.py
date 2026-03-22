async def run(db):
    await db.users.create_index("email", unique=True)