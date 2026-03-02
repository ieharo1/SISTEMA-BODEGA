from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

client: AsyncIOMotorClient = None
db = None


async def connect_to_mongodb():
    global client, db
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    db = client[settings.DATABASE_NAME]

    await db.users.create_index("email", unique=True)
    await db.products.create_index("sku", unique=True)
    await db.products.create_index("name")
    await db.warehouse_locations.create_index(
        [("percha", 1), ("piso", 1), ("columna", 1)], unique=True
    )


async def close_mongodb_connection():
    global client
    if client:
        client.close()


def get_database():
    return db
