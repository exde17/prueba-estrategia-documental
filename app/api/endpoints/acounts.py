from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.database import get_database
from app.crud.account import AccountCRUD
from app.services.account_service import AccountService
from app.schemas.account import AccountCreate, AccountUpdate, AccountResponse
# from app.models.account import Account  # Removed because it is unused or the import path is incorrect


router = APIRouter()

# Dependencia para obtener una instancia de AccountService
async def get_account_service(db: AsyncIOMotorDatabase = Depends(get_database)) -> AccountService:
    crud = AccountCRUD(db)
    service = AccountService(crud)
    return service

@router.post("/cuentas", response_model=AccountResponse, status_code=status.HTTP_201_CREATED)
async def create_bank_account(
    account_data: AccountCreate,
    account_service: AccountService = Depends(get_account_service)
):
    """
    Crea una nueva cuenta bancaria.
    - **account_holder_name**: Nombre del titular de la cuenta.
    - **balance**: Saldo inicial (opcional, por defecto 0.0).
    """
    new_account = await account_service.create_new_account(account_data)
    # Convertir el modelo Account a AccountResponse con el alias correcto
    return AccountResponse(
        id=new_account.id,
        account_holder_name=new_account.account_holder_name,
        balance=new_account.balance
    )

@router.patch("/cuentas/{account_id}", response_model=AccountResponse)
async def update_account(
    account_id: str,
    update_data: AccountUpdate,
    account_service: AccountService = Depends(get_account_service)
):
    """
    Actualiza una cuenta existente.
    - **account_id**: ID de la cuenta a actualizar.
    - **account_holder_name**: Nuevo nombre del titular (opcional).
    - **amount**: Cantidad a agregar o restar del saldo actual (opcional).
    
    Al menos uno de los campos debe ser proporcionado.
    """
    updated_account = await account_service.update_account_service(
        account_id, 
        update_data.account_holder_name, 
        update_data.amount
    )
    if not updated_account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cuenta no encontrada o ID inválido")
    # Convertir el modelo Account a AccountResponse con el alias correcto
    return AccountResponse(
        id=updated_account.id,
        account_holder_name=updated_account.account_holder_name,
        balance=updated_account.balance
    )

@router.get("/cuentas", response_model=List[AccountResponse])
async def list_all_accounts(
    account_service: AccountService = Depends(get_account_service)
):
    """
    Lista todas las cuentas bancarias con sus saldos.
    """
    accounts = await account_service.retrieve_all_accounts()
    # Convertir cada Account a AccountResponse con el alias correcto
    return [AccountResponse(
        id=account.id,
        account_holder_name=account.account_holder_name,
        balance=account.balance
    ) for account in accounts]