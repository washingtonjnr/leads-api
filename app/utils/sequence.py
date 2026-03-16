from app.core.types import IODatabase

async def get_next_sequence(db: IODatabase, sequence_name: str) -> int:
    result = await db.sequences.find_one_and_update(
        {"_id": sequence_name},
        {"$inc": {"value": 1}},
        upsert=True,
        return_document=True
    )
    return result["value"]
