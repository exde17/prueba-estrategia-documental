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

## Arquitectura y Patrones de Desarrollo

### Arquitectura Implementada

**Arquitectura Hexagonal (Ports and Adapters)**

La aplicación sigue los principios de la arquitectura hexagonal, también conocida como arquitectura de puertos y adaptadores, que proporciona:

- **Separación de responsabilidades**: Cada capa tiene una función específica
- **Independencia de frameworks**: La lógica de negocio no depende de detalles de implementación
- **Testabilidad**: Facilita las pruebas unitarias y de integración
- **Mantenibilidad**: Código más limpio y fácil de modificar

### Capas de la Arquitectura

```
┌─────────────────────────────────────────────────────────┐
│                    API Layer                            │
│              (FastAPI Endpoints)                        │
└─────────────────────┬───────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────┐
│                Service Layer                            │
│              (Business Logic)                           │
└─────────────────────┬───────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────┐
│                 CRUD Layer                              │
│            (Data Access Logic)                          │
└─────────────────────┬───────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────┐
│              Database Layer                             │
│                (MongoDB)                                │
└─────────────────────────────────────────────────────────┘
```

### Patrones de Desarrollo Utilizados

#### 1. **Patrón de repositorio**
- **Ubicación**: `app/crud/account.py`
- **Propósito**: Abstrae el acceso a datos
- **Beneficios**: Facilita el testing y permite cambiar la implementación de base de datos sin afectar la lógica de negocio

```python
class AccountRepository:
    async def create(self, account_data: dict) -> Account
    async def get_all(self) -> List[Account]
    async def update(self, account_id: str, update_data: dict) -> Account
```

#### 2. **Patrón de capa de servicio**
- **Ubicación**: `app/services/account_service.py`
- **Propósito**: Encapsula la lógica de negocio
- **Beneficios**: Centraliza las reglas de negocio y coordina operaciones entre diferentes repositorios

#### 3. **Patrón de objeto de transferencia de datos (DTO)**
- **Ubicación**: `app/schemas/account.py`
- **Propósito**: Define contratos de datos entre capas
- **Beneficios**: Validación automática, documentación de API, y separación entre modelos de dominio y de presentación

```python
class AccountCreate(BaseModel):  # DTO para creación
class AccountUpdate(BaseModel):  # DTO para actualización
class AccountResponse(BaseModel): # DTO para respuesta
```

#### 4. **Patrón de inyección de dependencia**
- **Ubicación**: `app/core/database.py`
- **Propósito**: Inyección de dependencias (base de datos, servicios)
- **Beneficios**: Desacoplamiento, testabilidad, y configuración centralizada

#### 5. **Patrón de fábrica**
- **Ubicación**: `app/core/config.py`
- **Propósito**: Creación de objetos de configuración
- **Beneficios**: Configuración centralizada y gestión de entornos

#### 6. **Patrón de fachada**
- **Ubicación**: `app/api/endpoints/accounts.py`
- **Propósito**: Simplifica la interfaz de los endpoints
- **Beneficios**: Oculta la complejidad de las operaciones internas

### Principios SOLID Aplicados

#### **S - Principio de responsabilidad única**
- Cada clase tiene una única responsabilidad
- `AccountRepository`: Solo maneja persistencia
- `AccountService`: Solo maneja lógica de negocio
- `AccountEndpoints`: Solo maneja HTTP

#### **O - Principio Abierto/Cerrado**
- Extensible sin modificar código existente
- Nuevos tipos de validación se pueden agregar sin cambiar esquemas existentes

#### **L - Principio de sustitución de Liskov**
- Las abstracciones pueden ser sustituidas por sus implementaciones
- Los esquemas Pydantic pueden ser intercambiados

#### **I - Principio de segregación de interfaz**
- Interfaces específicas para cada funcionalidad
- Esquemas separados para Create, Update, y Response

#### **D - Principio de inversión de dependencia**
- Dependencias de abstracciones, no de concreciones
- La lógica de negocio no depende de detalles de MongoDB

### Patrones de Configuración

#### **Environment-based Configuration**
```python
# Configuración por entorno
MONGODB_URL = "mongodb://localhost:27017/bank_db"  # Desarrollo
MONGODB_URL = "mongodb://user:pass@prod-db:27017/bank_db"  # Producción
```

#### **Graceful Degradation**
- Manejo de errores sin interrumpir el servicio
- Mensajes de error informativos en español
- Logs estructurados para debugging

### Ventajas de la Arquitectura Elegida

1. **Mantenibilidad**: Código organizado y fácil de modificar
2. **Testabilidad**: Cada capa se puede probar independientemente
3. **Escalabilidad**: Fácil agregar nuevas funcionalidades
4. **Flexibilidad**: Cambiar implementaciones sin afectar otras capas
5. **Reutilización**: Componentes reutilizables en diferentes contextos

### Estructura del Proyecto

```
app/
├── api/
│   └── endpoints/          #    Capa de Presentación (Controllers)
│       └── accounts.py     #    - Manejo de HTTP requests/responses
│                           #    - Validación de entrada
│                           #    - Serialización de salida
├── core/
│   ├── config.py          #   Configuración centralizada
│   └── database.py        #  Conexión y gestión de base de datos
├── crud/
│   └── account.py         #   Capa de Acceso a Datos (Repository)
│                          #    - Operaciones CRUD
│                          #    - Abstracción de base de datos
├── models/
│   └── account.py         #   Modelos de Dominio
│                          #    - Entidades de negocio
│                          #    - Reglas de dominio
├── schemas/
│   └── account.py         #  Data Transfer Objects (DTOs)
│                          #    - Contratos de API
│                          #    - Validaciones Pydantic
├── services/
│   └── account_service.py #  Capa de Lógica de Negocio
│                          #    - Reglas de negocio
│                          #    - Coordinación entre repositorios
└── main.py                #  Punto de entrada y configuración
```

### Patrones de Validación y Manejo de Errores

#### **Validation Pattern**
```python
# Validaciones en cascada
1. Pydantic Schema Validation (Entrada)
2. Business Logic Validation (Servicio)
3. Database Constraint Validation (Repository)
```

#### **Error Handling Strategy**
- **HTTP Exception Handling**: Respuestas HTTP apropiadas
- **Logging Strategy**: Logs estructurados para debugging
- **User-Friendly Messages**: Mensajes en español para el usuario final

### Patrones de Testing

#### **Implementación de la pirámide de prueba**
```
    E2E Tests (Integration)
    - Test completos de API
    Unit Tests (Isolated)
    - Test de cada componente
```

#### **Patrones de prueba utilizados**
- **Arrange-Act-Assert (AAA)**: Estructura clara de tests
- **Test Fixtures**: Datos de prueba reutilizables
- **Mocking**: Aislamiento de dependencias externas
- **Async Testing**: Pruebas para código asíncrono

### Consideraciones de Escalabilidad

#### **Escalamiento horizontal listo**
- Stateless API design
- Database connection pooling
- Container-based deployment

#### **Patrones de rendimiento**
- **Database Indexing**: Índices en campos frecuentemente consultados
- **Connection Pooling**: Reutilización de conexiones de base de datos
- **Async Operations**: Operaciones no bloqueantes

Esta arquitectura proporciona una base sólida para el crecimiento y mantenimiento de la aplicación bancaria, siguiendo las mejores prácticas de desarrollo de software moderno.

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
