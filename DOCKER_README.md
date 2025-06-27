# Notas de Implementación Docker

## Hoja de Comandos Operativos

### Flujo de Desarrollo
```bash
# Reconstrucción rápida tras cambios de código
docker-compose up --build

# Ejecución en segundo plano para testing
docker-compose up -d

# Logs específicos por servicio
docker-compose logs -f api
```

### Operaciones de Base de Datos
```bash
# Acceso directo a MongoDB
docker-compose exec mongodb mongo bank_db

# Backup del estado actual
docker-compose exec mongodb mongodump --db bank_db --out /backup

# Reinicio limpio (elimina datos)
docker-compose down -v && docker-compose up
```

### Resolución de Problemas
```bash
# Verificar conectividad entre servicios
docker-compose exec api ping mongodb

# Monitorear uso de recursos
docker stats

# Inspección de red
docker network inspect prueba_estrategia_documental_bank_network
```

## Consideraciones de Producción

## Variables de Entorno

```bash
# Desarrollo
MONGODB_URL=mongodb://mongodb:27017/bank_db

# Producción
MONGODB_URL=mongodb://usuario:password@mongodb:27017/bank_db
ME_CONFIG_BASICAUTH=true
```

La configuración containerizada proporciona entornos consistentes entre desarrollo y producción manteniendo la separación de responsabilidades entre capas de aplicación.
