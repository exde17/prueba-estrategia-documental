from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.database import get_database
from app.crud.account import AccountCRUD
from app.services.account_service import AccountService
from app.schemas.account import AccountCreate, AccountUpdate, AccountResponse



router = APIRouter()

# Dependencia para obtener una instancia de accountService
async def get_account_service(db: AsyncIOMotorDatabase = Depends(get_database)) -> AccountService:
    crud = AccountCRUD(db)
    service = AccountService(crud)
    return service

@router.post("/accounts", response_model=AccountResponse, status_code=status.HTTP_201_CREATED)
async def create_bank_account(
    account_data: AccountCreate,
    account_service: AccountService = Depends(get_account_service)
):
    """
    Crea una nueva cuenta bancaria.
    - **account_number**: Número de cuenta único.
    - **account_type**: Tipo de cuenta (savings, checking, etc.).
    - **customer_name**: Nombre del cliente titular de la cuenta.
    - **document_type**: Tipo de documento del cliente.
    - **document_number**: Número de documento del cliente.
    - **phone**: Teléfono del cliente.
    - **email**: Email del cliente.
    - **address**: Dirección del cliente.
    - **balance**: Saldo inicial (opcional, por defecto 0.0).
    """
    new_account = await account_service.create_new_account(account_data)
    # Convertir el modelo account a accountResponse
    return AccountResponse(
        id=new_account.id,
        account_number=new_account.account_number,
        account_type=new_account.account_type,
        customer_name=new_account.customer_name,
        document_type=new_account.document_type,
        document_number=new_account.document_number,
        phone=new_account.phone,
        email=new_account.email,
        address=new_account.address,
        balance=new_account.balance
    )

@router.patch("/accounts/{account_id}", response_model=AccountResponse)
async def update_account(
    account_id: str,
    update_data: AccountUpdate,
    account_service: AccountService = Depends(get_account_service)
):
    """
    Actualiza una cuenta existente.
    - **account_id**: ID de la cuenta a actualizar.
    - **account_number**: Nuevo número de cuenta (opcional).
    - **account_type**: Nuevo tipo de cuenta (opcional).
    - **customer_name**: Nuevo nombre del cliente (opcional).
    - **document_type**: Nuevo tipo de documento (opcional).
    - **document_number**: Nuevo número de documento (opcional).
    - **phone**: Nuevo teléfono (opcional).
    - **email**: Nuevo email (opcional).
    - **address**: Nueva dirección (opcional).
    - **balance**: Nuevo saldo (opcional).
    
    Al menos uno de los campos debe ser proporcionado.
    """
    updated_account = await account_service.update_account_service(account_id, update_data)
    if not updated_account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cuenta no encontrada o ID inválido")
    # Convertir el modelo account a accountResponse
    return AccountResponse(
        id=updated_account.id,
        account_number=updated_account.account_number,
        account_type=updated_account.account_type,
        customer_name=updated_account.customer_name,
        document_type=updated_account.document_type,
        document_number=updated_account.document_number,
        phone=updated_account.phone,
        email=updated_account.email,
        address=updated_account.address,
        balance=updated_account.balance
    )

@router.get("/accounts", response_model=List[AccountResponse])
async def list_all_accounts(
    account_service: AccountService = Depends(get_account_service)
):
    """
    Lista todas las cuentas bancarias con toda su información.
    """
    accounts = await account_service.retrieve_all_accounts()
    # Convertir cada account a accountResponse
    return [AccountResponse(
        id=account.id,
        account_number=account.account_number,
        account_type=account.account_type,
        customer_name=account.customer_name,
        document_type=account.document_type,
        document_number=account.document_number,
        phone=account.phone,
        email=account.email,
        address=account.address,
        balance=account.balance
    ) for account in accounts]