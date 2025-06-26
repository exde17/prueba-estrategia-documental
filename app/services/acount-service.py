from typing import List, Optional
from app.crud.account import AccountCRUD
from app.models.account import Account
from app.schemas.account import AccountCreate

class AccountService:
    def __init__(self, account_crud: AccountCRUD):
        self.account_crud = account_crud

    async def create_new_account(self, account_data: AccountCreate) -> Account:
        """Crea una nueva cuenta bancaria."""
        return await self.account_crud.create_account(account_data)

    async def retrieve_all_accounts(self) -> List[Account]:
        """Obtiene todas las cuentas bancarias."""
        return await self.account_crud.get_all_accounts()

    async def retrieve_account_by_id(self, account_id: str) -> Optional[Account]:
        """Obtiene una cuenta por su ID."""
        return await self.account_crud.get_account_by_id(account_id)

    async def update_account_balance_service(self, account_id: str, amount: float) -> Optional[Account]:
        """Actualiza el saldo de una cuenta."""
        return await self.account_crud.update_account_balance(account_id, amount)