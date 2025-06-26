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
        "/api/v1/cuentas",
        json={"account_holder_name": "Alice Smith", "balance": 500.0}
    )
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["account_holder_name"] == "Alice Smith"
    assert data["balance"] == 500.0
    # Verifica que la cuenta existe en la base de datos
    account_in_db = await db.database.acount.find_one({"_id": ObjectId(data["id"])})
    assert account_in_db is not None
    assert account_in_db["account_holder_name"] == "Alice Smith"

# Prueba para listar todas las cuentas
@pytest.mark.asyncio
async def test_list_all_accounts(async_client: AsyncClient):
    # Crea algunas cuentas de prueba
    await async_client.post("/api/v1/cuentas", json={"account_holder_name": "Bob Johnson", "balance": 100.0})
    await async_client.post("/api/v1/cuentas", json={"account_holder_name": "Charlie Brown", "balance": 200.0})

    response = await async_client.get("/api/v1/cuentas")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert any(acc["account_holder_name"] == "Bob Johnson" for acc in data)
    assert any(acc["account_holder_name"] == "Charlie Brown" for acc in data)

# Prueba para actualizar el saldo de una cuenta
@pytest.mark.asyncio
async def test_update_account_balance(async_client: AsyncClient):
    # Crea una cuenta primero
    create_response = await async_client.post(
        "/api/v1/cuentas",
        json={"account_holder_name": "David Lee", "balance": 1000.0}
    )
    account_id = create_response.json()["id"]

    # Actualiza el saldo (agrega)
    update_response_add = await async_client.patch(
        f"/api/v1/cuentas/{account_id}",
        json={"amount": 200.0}
    )
    assert update_response_add.status_code == 200
    updated_data_add = update_response_add.json()
    assert updated_data_add["id"] == account_id
    assert updated_data_add["balance"] == 1200.0

    # Actualiza el saldo (resta)
    update_response_subtract = await async_client.patch(
        f"/api/v1/cuentas/{account_id}",
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
        f"/api/v1/cuentas/{non_existent_id}",
        json={"amount": 50.0}
    )
    assert response.status_code == 404
    assert "Cuenta no encontrada o ID inválido" in response.json()["detail"]

# Prueba para actualizar el saldo con ID inválido
@pytest.mark.asyncio
async def test_update_invalid_id(async_client: AsyncClient):
    invalid_id = "invalid_id_format"
    response = await async_client.patch(
        f"/api/v1/cuentas/{invalid_id}",
        json={"amount": 50.0}
    )
    assert response.status_code == 404 # Se maneja como "no encontrada o ID inválido"
    assert "Cuenta no encontrada o ID inválido" in response.json()["detail"]

# Prueba para crear una cuenta con datos inválidos
@pytest.mark.asyncio
async def test_create_account_invalid_data(async_client: AsyncClient):
    response = await async_client.post(
        "/api/v1/cuentas",
        json={"account_holder_name": "A", "balance": -100.0} # Nombre muy corto, balance negativo
    )
    assert response.status_code == 422 # Unprocessable Entity por validación de Pydantic
    data = response.json()
    assert "detail" in data
    # Los mensajes de error ahora están en español
    error_messages = [err["msg"] for err in data["detail"]]
    assert any("al menos 3 caracteres" in msg for msg in error_messages)
    assert any("no puede ser negativo" in msg for msg in error_messages)

# Prueba para actualizar solo el nombre del titular
@pytest.mark.asyncio
async def test_update_account_holder_name_only(async_client: AsyncClient):
    # Crea una cuenta primero
    create_response = await async_client.post(
        "/api/v1/cuentas",
        json={"account_holder_name": "Juan Pérez", "balance": 500.0}
    )
    account_id = create_response.json()["id"]
    
    # Actualiza solo el nombre
    update_response = await async_client.patch(
        f"/api/v1/cuentas/{account_id}",
        json={"account_holder_name": "Juan Carlos Pérez"}
    )
    assert update_response.status_code == 200
    updated_data = update_response.json()
    assert updated_data["id"] == account_id
    assert updated_data["account_holder_name"] == "Juan Carlos Pérez"
    assert updated_data["balance"] == 500.0  # El saldo no debe cambiar

# Prueba para actualizar nombre y saldo al mismo tiempo
@pytest.mark.asyncio
async def test_update_account_name_and_balance(async_client: AsyncClient):
    # Crea una cuenta primero
    create_response = await async_client.post(
        "/api/v1/cuentas",
        json={"account_holder_name": "María González", "balance": 1000.0}
    )
    account_id = create_response.json()["id"]
    
    # Actualiza nombre y saldo
    update_response = await async_client.patch(
        f"/api/v1/cuentas/{account_id}",
        json={"account_holder_name": "María Elena González", "amount": 250.0}
    )
    assert update_response.status_code == 200
    updated_data = update_response.json()
    assert updated_data["id"] == account_id
    assert updated_data["account_holder_name"] == "María Elena González"
    assert updated_data["balance"] == 1250.0  # 1000 + 250

# Prueba para validar que se requiere al menos un campo para actualizar
@pytest.mark.asyncio
async def test_update_account_no_fields(async_client: AsyncClient):
    # Crea una cuenta primero
    create_response = await async_client.post(
        "/api/v1/cuentas",
        json={"account_holder_name": "Pedro Martínez", "balance": 300.0}
    )
    account_id = create_response.json()["id"]
    
    # Intenta actualizar sin proporcionar campos
    update_response = await async_client.patch(
        f"/api/v1/cuentas/{account_id}",
        json={}
    )
    assert update_response.status_code == 422
    data = update_response.json()
    error_messages = [err["msg"] for err in data["detail"]]
    assert any("al menos el nombre del titular o una cantidad" in msg for msg in error_messages)

# Prueba para validar nombre del titular inválido en actualización
@pytest.mark.asyncio
async def test_update_account_invalid_name(async_client: AsyncClient):
    # Crea una cuenta primero
    create_response = await async_client.post(
        "/api/v1/cuentas",
        json={"account_holder_name": "Ana López", "balance": 200.0}
    )
    account_id = create_response.json()["id"]
    
    # Intenta actualizar con nombre muy corto
    update_response = await async_client.patch(
        f"/api/v1/cuentas/{account_id}",
        json={"account_holder_name": "A"}
    )
    assert update_response.status_code == 422
    data = update_response.json()
    error_messages = [err["msg"] for err in data["detail"]]
    assert any("al menos 3 caracteres" in msg for msg in error_messages)