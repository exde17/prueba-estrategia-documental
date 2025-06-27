# app/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.core.database import db
from app.api.endpoints import acounts

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Maneja los eventos de inicio y cierre de la aplicación."""
    # Startup
    await db.connect()
    yield
    # Shutdown
    await db.close()

app = FastAPI(
    title="API Bancaria",
    description="API RESTful para gestionar cuentas bancarias y sus saldos.",
    version="1.0.0",
    docs_url="/documentacion",
    redoc_url=None,
    lifespan=lifespan
)

app.include_router(acounts.router)

@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    """Redirige la raíz a la documentación de la API."""
    return RedirectResponse(url="/documentacion")