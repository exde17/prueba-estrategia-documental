from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

class MongoDB:
    client: AsyncIOMotorClient = None
    database = None

    async def connect(self):
        """conexión con la db."""
        self.client = AsyncIOMotorClient(settings.MONGODB_URI)
        self.database = self.client[settings.DATABASE_NAME]
        print(f"Conectado a MongoDB: {settings.MONGODB_URI}")

    async def close(self):
        """Cierra la conexión con la db."""
        if self.client:
            self.client.close()
            print("Conexión a MongoDB cerrada.")

db = MongoDB()

async def get_database():
    """Dependencia para obtener la instancia de la base de datos."""
    return db.database