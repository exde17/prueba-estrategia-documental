from typing import List, Optional
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.models.account import Account
from app.schemas.account import AccountCreate

class AccountCRUD:
    def __init__(self, database: AsyncIOMotorDatabase):
        self.collection = database.acount # Accede a la colección 'acount'

    async def create_account(self, account: AccountCreate) -> Account:
        """Crea una nueva cuenta bancaria."""
        account_dict = account.model_dump()
        result = await self.collection.insert_one(account_dict)
        created_account = await self.collection.find_one({"_id": result.inserted_id})
        # Convertir ObjectId a string para Pydantic
        created_account["_id"] = str(created_account["_id"])
        return Account(**created_account)

    async def get_all_accounts(self) -> List[Account]:
        """Obtiene todas las cuentas bancarias."""
        accounts = []
        async for account in self.collection.find():
            # Convertir ObjectId a string para Pydantic
            account["_id"] = str(account["_id"])
            accounts.append(Account(**account))
        return accounts

    async def get_account_by_id(self, account_id: str) -> Optional[Account]:
        """Obtiene una cuenta por su ID."""
        if not ObjectId.is_valid(account_id):
            return None # O raise ValueError
        account = await self.collection.find_one({"_id": ObjectId(account_id)})
        if account:
            # Convertir ObjectId a string para Pydantic
            account["_id"] = str(account["_id"])
            return Account(**account)
        return None

    async def update_account_balance(self, account_id: str, amount: float) -> Optional[Account]:
        """Actualiza el saldo de una cuenta. Agrega o resta la cantidad."""
        if not ObjectId.is_valid(account_id):
            return None
        
        # Incrementar/Decrementar el saldo actual
        result = await self.collection.find_one_and_update(
            {"_id": ObjectId(account_id)},
            {"$inc": {"balance": amount}}, # $inc para incrementar/decrementar
            return_document=True # Devuelve el documento después de la actualización
        )
        if result:
            # Convertir ObjectId a string para Pydantic
            result["_id"] = str(result["_id"])
            return Account(**result)
        return None

    async def update_account(self, account_id: str, account_holder_name: Optional[str] = None, amount: Optional[float] = None) -> Optional[Account]:
        """Actualiza los campos especificados de una cuenta."""
        if not ObjectId.is_valid(account_id):
            return None
        
        # Construir el documento de actualización dinámicamente
        update_doc = {}
        
        # Si se proporciona un nuevo nombre, actualizar
        if account_holder_name is not None:
            update_doc["$set"] = {"account_holder_name": account_holder_name}
        
        # Si se proporciona una cantidad, incrementar/decrementar el saldo
        if amount is not None:
            update_doc["$inc"] = {"balance": amount}
        
        # Si no hay nada que actualizar, devolver None
        if not update_doc:
            return None
        
        result = await self.collection.find_one_and_update(
            {"_id": ObjectId(account_id)},
            update_doc,
            return_document=True # Devuelve el documento después de la actualización
        )
        if result:
            # Convertir ObjectId a string para Pydantic
            result["_id"] = str(result["_id"])
            return Account(**result)
        return None