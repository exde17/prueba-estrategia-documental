# API Bancaria - FastAPI + MongoDB

Prueba técnica Desarrollador Backend Python - ED Software y Desarrollo SAS.

## Características

- ✅ **CRUD completo** de cuentas bancarias
- ✅ **Actualización flexible** de nombre del titular y saldo
- ✅ **Validaciones personalizadas** en español
- ✅ **Pruebas unitarias** completas (10/10 tests)
- ✅ **Documentación interactiva** con Swagger UI
- ✅ **Containerización** con Docker y Docker Compose
- ✅ **Mensajes de error** personalizados en español
- ✅ **Arquitectura limpia** con separación de responsabilidades

## 🚀 Inicio Rápido

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

## 📋 Endpoints de la API

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `POST` | `/api/v1/cuentas` | Crear nueva cuenta |
| `GET` | `/api/v1/cuentas` | Listar todas las cuentas |
| `PATCH` | `/api/v1/cuentas/{id}` | Actualizar cuenta (nombre y/o saldo) |

### Ejemplos de Uso

#### Crear cuenta
```http
POST /api/v1/cuentas
Content-Type: application/json

{
  "account_holder_name": "Juan Pérez",
  "balance": 1000.0
}
```

#### Actualizar solo el nombre
```http
PATCH /api/v1/cuentas/{account_id}
Content-Type: application/json

{
  "account_holder_name": "Juan Carlos Pérez"
}
```

#### Actualizar solo el saldo
```http
PATCH /api/v1/cuentas/{account_id}
Content-Type: application/json

{
  "amount": 250.0
}
```

#### Actualizar nombre y saldo
```http
PATCH /api/v1/cuentas/{account_id}
Content-Type: application/json

{
  "account_holder_name": "Juan Carlos Pérez",
  "amount": -100.0
}
```

## 🧪 Pruebas

### Ejecutar todas las pruebas
```bash
# Desarrollo local
pytest tests/ -v

# En Docker
docker-compose exec api python -m pytest tests/ -v
```

### Cobertura de pruebas
- ✅ Creación de cuentas
- ✅ Listado de cuentas
- ✅ Actualización de saldo
- ✅ Actualización de nombre del titular
- ✅ Actualización combinada (nombre + saldo)
- ✅ Validación de datos inválidos
- ✅ Manejo de errores (cuentas inexistentes, IDs inválidos)
- ✅ Mensajes de error en español

## 🏗️ Arquitectura

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

## 🐳 Docker

La aplicación incluye configuración completa para Docker:

- **Dockerfile**: Imagen optimizada de Python
- **docker-compose.yml**: Orquestación con MongoDB
- **Persistencia de datos**: Volúmenes para MongoDB
- **Documentación específica**: Ver DOCKER_README.md para detalles técnicos

## 🔧 Configuración

### Variables de entorno
```bash
MONGODB_URI=mongodb://localhost:27017/bank_db
DATABASE_NAME=bank_db
```

### Desarrollo
```bash
# Copiar archivo de configuración
cp .env.example .env
# Editar según necesidades
```

## 📝 Validaciones

La API incluye validaciones completas:

- **Nombre del titular**: Mínimo 3 caracteres, máximo 100
- **Saldo**: No puede ser negativo
- **Actualizaciones**: Al menos un campo debe ser proporcionado
- **IDs**: Validación de formato ObjectId de MongoDB

## 🌍 Internacionalización

Todos los mensajes de error están en español:
- Validaciones de Pydantic personalizadas
- Mensajes de error HTTP descriptivos
- Documentación en español

## 🔍 Monitoreo

### Logs de Docker
```bash
docker-compose logs -f
docker-compose logs api
docker-compose logs mongodb
```

### Health Checks
```bash
curl http://localhost:8001/docs  # Documentación
curl http://localhost:8001/api/v1/cuentas  # Endpoint de prueba
```

## 🛠️ Comandos Útiles

```bash
# Docker
docker-compose up --build -d    # Iniciar servicios
docker-compose down             # Detener servicios
docker-compose down -v          # Detener y eliminar volúmenes
docker-compose logs -f          # Ver logs en tiempo real

# Desarrollo
uvicorn app.main:app --reload   # Servidor de desarrollo
pytest tests/ -v --cov=app     # Pruebas con cobertura
```

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

---

**Prueba Técnica Completada** ✅
- API REST funcional
- Pruebas unitarias completas
- Dockerización completa
- Documentación detallada
