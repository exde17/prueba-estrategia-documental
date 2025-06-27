import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from app.main import app # Importa la instancia de la aplicación FastAPI
from app.core.database import db # Para limpiar la base de datos de pruebas
from bson import ObjectId

# Fixture para limpiar la base de datos antes de cada prueba
@pytest_asyncio.fixture(autouse=True)
async def clear_db():
    await db.connect() # Asegura que la conexión esté abierta
    await db.database.acount.delete_many({}) # Limpia la colección de cuentas
    yield
    await db.database.acount.delete_many({}) # Limpia de nuevo después de la prueba
    await db.close() # Cierra la conexión

# Fixture para el cliente de prueba HTTP
@pytest_asyncio.fixture
async def async_client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client

# Prueba para crear una cuenta bancaria
@pytest.mark.asyncio
async def test_create_account(async_client: AsyncClient):
    response = await async_client.post(
        "/accounts",
        json={
            "account_number": "123-456-789",
            "account_type": "savings",
            "customer_name": "Alice Smith",
            "document_type": "CC",
            "document_number": "12345678",
            "phone": "555-1234",
            "email": "alice@example.com",
            "address": "123 Main St",
            "balance": 500.0
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["customer_name"] == "Alice Smith"
    assert data["account_number"] == "123-456-789"
    assert data["balance"] == 500.0
    # Verifica que la cuenta existe en la base de datos
    account_in_db = await db.database.acount.find_one({"_id": ObjectId(data["id"])})
    assert account_in_db is not None
    assert account_in_db["customer_name"] == "Alice Smith"

# Prueba para listar todas las cuentas
@pytest.mark.asyncio
async def test_list_all_accounts(async_client: AsyncClient):
    # Crea algunas cuentas de prueba
    await async_client.post("/accounts", json={
        "account_number": "111-222-333",
        "account_type": "checking",
        "customer_name": "Bob Johnson",
        "document_type": "CC",
        "document_number": "11111111",
        "phone": "555-1111",
        "email": "bob@example.com",
        "address": "111 First St",
        "balance": 100.0
    })
    await async_client.post("/accounts", json={
        "account_number": "444-555-666",
        "account_type": "savings",
        "customer_name": "Charlie Brown",
        "document_type": "CC",
        "document_number": "22222222",
        "phone": "555-2222",
        "email": "charlie@example.com",
        "address": "222 Second St",
        "balance": 200.0
    })

    response = await async_client.get("/accounts")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert any(acc["customer_name"] == "Bob Johnson" for acc in data)
    assert any(acc["customer_name"] == "Charlie Brown" for acc in data)

# Prueba para actualizar el saldo de una cuenta
@pytest.mark.asyncio
async def test_update_account_balance(async_client: AsyncClient):
    # Crea una cuenta primero
    create_response = await async_client.post(
        "/accounts",
        json={
            "account_number": "777-888-999",
            "account_type": "savings",
            "customer_name": "David Lee",
            "document_type": "CC",
            "document_number": "33333333",
            "phone": "555-3333",
            "email": "david@example.com",
            "address": "333 Third St",
            "balance": 1000.0
        }
    )
    account_id = create_response.json()["id"]

    # Actualiza el saldo (agrega)
    update_response_add = await async_client.patch(
        f"/accounts/{account_id}",
        json={"amount": 200.0}
    )
    assert update_response_add.status_code == 200
    updated_data_add = update_response_add.json()
    assert updated_data_add["id"] == account_id
    assert updated_data_add["balance"] == 1200.0

    # Actualiza el saldo (resta)
    update_response_subtract = await async_client.patch(
        f"/accounts/{account_id}",
        json={"amount": -100.0}
    )
    assert update_response_subtract.status_code == 200
    updated_data_subtract = update_response_subtract.json()
    assert updated_data_subtract["id"] == account_id
    assert updated_data_subtract["balance"] == 1100.0 # 1200 - 100

# Prueba para actualizar el saldo de una cuenta inexistente
@pytest.mark.asyncio
async def test_update_non_existent_account(async_client: AsyncClient):
    non_existent_id = str(ObjectId()) # Un ID válido pero que no existe
    response = await async_client.patch(
        f"/accounts/{non_existent_id}",
        json={"amount": 50.0}
    )
    assert response.status_code == 404
    assert "Cuenta no encontrada o ID inválido" in response.json()["detail"]

# Prueba para actualizar el saldo con ID inválido
@pytest.mark.asyncio
async def test_update_invalid_id(async_client: AsyncClient):
    invalid_id = "invalid_id_format"
    response = await async_client.patch(
        f"/accounts/{invalid_id}",
        json={"amount": 50.0}
    )
    assert response.status_code == 404 # Se maneja como "no encontrada o ID inválido"
    assert "Cuenta no encontrada o ID inválido" in response.json()["detail"]

# Prueba para crear una cuenta con datos inválidos
@pytest.mark.asyncio
async def test_create_account_invalid_data(async_client: AsyncClient):
    response = await async_client.post(
        "/accounts",
        json={
            "account_number": "A",  # Muy corto
            "account_type": "invalid_type",  # Tipo inválido
            "customer_name": "A",  # Nombre muy corto
            "document_type": "INVALID",  # Tipo de documento inválido
            "document_number": "123",  # Muy corto
            "phone": "123",  # Muy corto
            "email": "invalid-email",  # Email inválido
            "address": "A",  # Muy corta
            "balance": -100.0  # Balance negativo
        }
    )
    assert response.status_code == 422 # Unprocessable Entity por validación de Pydantic
    data = response.json()
    assert "detail" in data

# Prueba para actualizar solo el nombre del cliente
@pytest.mark.asyncio
async def test_update_customer_name_only(async_client: AsyncClient):
    # Crea una cuenta primero
    create_response = await async_client.post(
        "/accounts",
        json={
            "account_number": "555-666-777",
            "account_type": "savings",
            "customer_name": "Juan Pérez",
            "document_type": "CC",
            "document_number": "44444444",
            "phone": "555-4444",
            "email": "juan@example.com",
            "address": "444 Fourth St",
            "balance": 500.0
        }
    )
    account_id = create_response.json()["id"]
    
    # Actualiza solo el nombre
    update_response = await async_client.patch(
        f"/accounts/{account_id}",
        json={"customer_name": "Juan Carlos Pérez"}
    )
    assert update_response.status_code == 200
    updated_data = update_response.json()
    assert updated_data["id"] == account_id
    assert updated_data["customer_name"] == "Juan Carlos Pérez"
    assert updated_data["balance"] == 500.0  # El saldo no debe cambiar

# Prueba para actualizar nombre y saldo al mismo tiempo
@pytest.mark.asyncio
async def test_update_account_name_and_balance(async_client: AsyncClient):
    # Crea una cuenta primero
    create_response = await async_client.post(
        "/accounts",
        json={
            "account_number": "888-999-000",
            "account_type": "checking",
            "customer_name": "María González",
            "document_type": "CC",
            "document_number": "55555555",
            "phone": "555-5555",
            "email": "maria@example.com",
            "address": "555 Fifth St",
            "balance": 1000.0
        }
    )
    account_id = create_response.json()["id"]
    
    # Actualiza nombre y saldo
    update_response = await async_client.patch(
        f"/accounts/{account_id}",
        json={"customer_name": "María Elena González", "amount": 250.0}
    )
    assert update_response.status_code == 200
    updated_data = update_response.json()
    assert updated_data["id"] == account_id
    assert updated_data["customer_name"] == "María Elena González"
    assert updated_data["balance"] == 1250.0  # 1000 + 250

# Prueba para validar que se requiere al menos un campo para actualizar
@pytest.mark.asyncio
async def test_update_account_no_fields(async_client: AsyncClient):
    # Crea una cuenta primero
    create_response = await async_client.post(
        "/accounts",
        json={
            "account_number": "111-000-222",
            "account_type": "savings",
            "customer_name": "Pedro Martínez",
            "document_type": "CC",
            "document_number": "66666666",
            "phone": "555-6666",
            "email": "pedro@example.com",
            "address": "666 Sixth St",
            "balance": 300.0
        }
    )
    account_id = create_response.json()["id"]
    
    # Intenta actualizar sin proporcionar campos
    update_response = await async_client.patch(
        f"/accounts/{account_id}",
        json={}
    )
    assert update_response.status_code == 422
    data = update_response.json()
    error_messages = [err["msg"] for err in data["detail"]]
    assert any("al menos un campo" in msg for msg in error_messages)

# Prueba para validar nombre del cliente inválido en actualización
@pytest.mark.asyncio
async def test_update_account_invalid_name(async_client: AsyncClient):
    # Crea una cuenta primero
    create_response = await async_client.post(
        "/accounts",
        json={
            "account_number": "333-444-555",
            "account_type": "checking",
            "customer_name": "Ana López",
            "document_type": "CC",
            "document_number": "77777777",
            "phone": "555-7777",
            "email": "ana@example.com",
            "address": "777 Seventh St",
            "balance": 200.0
        }
    )
    account_id = create_response.json()["id"]
    
    # Intenta actualizar con nombre muy corto
    update_response = await async_client.patch(
        f"/accounts/{account_id}",
        json={"customer_name": "A"}
    )
    assert update_response.status_code == 422
    data = update_response.json()
    error_messages = [err["msg"] for err in data["detail"]]
    assert any("al menos 3 caracteres" in msg for msg in error_messages)