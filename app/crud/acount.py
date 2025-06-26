from typing import List, Optional
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.models.account import Account
from app.schemas.account import AccountCreate

class AccountCRUD:
    def __init__(self, database: AsyncIOMotorDatabase):
        self.collection = database.accounts # Accede a la colección 'accounts'

    async def create_account(self, account: AccountCreate) -> Account:
        """Crea una nueva cuenta bancaria."""
        account_dict = account.model_dump()
        result = await self.collection.insert_one(account_dict)
        created_account = await self.collection.find_one({"_id": result.inserted_id})
        return Account(**created_account)

    async def get_all_accounts(self) -> List[Account]:
        """Obtiene todas las cuentas bancarias."""
        accounts = []
        async for account in self.collection.find():
            accounts.append(Account(**account))
        return accounts

    async def get_account_by_id(self, account_id: str) -> Optional[Account]:
        """Obtiene una cuenta por su ID."""
        if not ObjectId.is_valid(account_id):
            return None # O raise ValueError
        account = await self.collection.find_one({"_id": ObjectId(account_id)})
        return Account(**account) if account else None

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
        return Account(**result) if result else None