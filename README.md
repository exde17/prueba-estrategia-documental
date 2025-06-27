# API Bancaria - FastAPI + MongoDB

Prueba técnica Desarrollador Backend Python - ED Software y Desarrollo SAS.

## Características

-  **CRUD completo** de cuentas bancarias
-  **Actualización flexible** de nombre del titular y saldo
-  **Validaciones personalizadas** en español
-  **Pruebas unitarias** completas (10/10 tests)
-  **Documentación interactiva** con Swagger UI
-  **Containerización** con Docker y Docker Compose
-  **Mensajes de error** personalizados en español
-  **Arquitectura limpia** con separación de responsabilidades

##  Inicio Rápido

### Opción 1: Con Docker (Recomendado)

```bash
# 1. Asegúrate de que Docker Desktop esté ejecutándose
# 2. Construir y ejecutar todos los servicios
docker-compose up --build

# Para ejecutar en segundo plano
docker-compose up --build -d

# 3. Accede a la aplicación
# API: http://localhost:8001
# Documentación: http://localhost:8001/documentacion
# Mongo Express: http://localhost:8081
```

### Opción 2: Desarrollo Local

```bash
# 1. Instalar dependencias
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate     # Windows

pip install -r requirements.txt

# 2. Configurar MongoDB (debe estar ejecutándose en localhost:27017)

# 3. Ejecutar la aplicación
uvicorn app.main:app --reload

# 4. Ejecutar pruebas
pytest tests/ -v
```

## Endpoints de la API

| `POST` | `/accounts` | Crear nueva cuenta |
| `GET` | `/accounts` | Listar todas las cuentas |
| `PATCH` | `/accounts/{id}` | Actualizar cuenta (nombre y/o saldo) |

### Ejemplos de Uso

#### Crear cuenta
```http
POST http://localhost:8001/accounts
Content-Type: application/json

{
  "account_number": "PATCH-TEST-001",
  "account_type": "checking", 
  "customer_name": "jose contreras",
  "document_type": "CC",
  "document_number": "87654321",
  "phone": "555-9876",
  "email": "patch@example.com",
  "address": "Calle Patch 456",
  "balance": 750.0
}
```

#### Actualizar solo el nombre
```http
PATCH http://localhost:8001/accounts/{account_id}
Content-Type: application/json

{
  "customer_name": "Juan Carlos Pérez"
}
```

#### Actualizar solo el saldo
```http
PATCH http://localhost:8001/accounts/{account_id}
Content-Type: application/json

{
  "amount": 250.0
}
```

#### Actualizar nombre y saldo
```http
PATCH http://localhost:8001/accounts/{account_id}
Content-Type: application/json

{
  "customer_name": "Juan Carlos Pérez",
  "amount": -100.0
}
```

## Pruebas

### Ejecutar todas las pruebas
```bash
# Desarrollo local
pytest tests/ -v

# En Docker
docker-compose exec api python -m pytest tests/ -v
```

### Cobertura de pruebas
-  Creación de cuentas
-  Listado de cuentas
-  Actualización de saldo
-  Actualización de nombre del titular
-  Actualización combinada (nombre + saldo)
-  Validación de datos inválidos
-  Manejo de errores (cuentas inexistentes, IDs inválidos)
-  Mensajes de error en español

## Arquitectura

```
app/
├── api/
│   └── endpoints/      # Controladores REST
├── core/
│   ├── config.py      # Configuración
│   └── database.py    # Conexión a MongoDB
├── crud/
│   └── account.py     # Operaciones de base de datos
├── models/
│   └── account.py     # Modelos de datos
├── schemas/
│   └── account.py     # Esquemas de validación
├── services/
│   └── account_service.py  # Lógica de negocio
└── main.py           # Punto de entrada
```

## Docker

La aplicación incluye configuración completa para Docker:


## Configuración

### Variables de entorno
```bash
MONGODB_URI=mongodb://localhost:27017/bank_db
DATABASE_NAME=bank_db
```

## Validaciones

La API incluye validaciones completas:

- **Número de cuenta**: Formato válido requerido
- **Tipo de cuenta**: "savings" o "checking"
- **Nombre del cliente**: Mínimo 3 caracteres, máximo 100
- **Tipo de documento**: CC, CE, TI, PP, NIT, RUT, RC
- **Número de documento**: Mínimo 5 caracteres
- **Teléfono**: Mínimo 7 caracteres
- **Email**: Formato de email válido
- **Dirección**: Mínimo 5 caracteres
- **Saldo**: No puede ser negativo
- **Actualizaciones**: Al menos un campo debe ser proporcionado
- **IDs**: Validación de formato ObjectId de MongoDB


## Monitoreo

### Logs de Docker
```bash
docker-compose logs -f
docker-compose logs api
docker-compose logs mongodb
```

### Health Checks
```bash
curl http://localhost:8001/documentacion  # Documentación
curl http://localhost:8001/accounts  # Endpoint de prueba
```

## Comandos Útiles

```bash
# Docker
docker-compose up --build -d    # Iniciar servicios
docker-compose down             # Detener servicios
docker-compose down -v          # Detener y eliminar volúmenes
docker-compose logs -f          # Ver logs en tiempo real

# Desarrollo
uvicorn app.main:app --reload   # Servidor de desarrollo

```

---

**Prueba Técnica Completada** 
- API REST funcional
- Pruebas unitarias completas
- Dockerización completa
- Documentación detallada
