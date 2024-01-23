from typing import Any

from fastapi import APIRouter, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from loguru import logger

from app.api import api_router
from app.config import settings, setup_app_logging
from database.mongo_singleton import ConexionMongoDB

# Configurar el registro tan pronto como sea posible
setup_app_logging(config=settings)

# Crear instancia de la aplicación FastAPI
app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)


@app.on_event("startup")
async def startup_db_client():
    try:
        logger.info("Iniciando conexion a la base de datos")
        ConexionMongoDB()
        logger.info("Conexion exitosa a la base de datos")
    except Exception as e:
        logger.error(f"Error al conectar a la base de datos: {str(e)}")


# Routers
root_router = APIRouter()


@root_router.get("/")
def index(request: Request) -> Any:
    """Respuesta HTML básica."""
    body = (
        "<html>"
        "<body style='padding: 10px;'>"
        "<h1>Bienvenido a la API</h1>"
        "<div>"
        "Consulte la documentación: <a href='/docs'>aquí</a>"
        "</div>"
        "</body>"
        "</html>"
    )

    return HTMLResponse(content=body)


# Incluir los routers en la aplicación
app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(root_router)

# Configurar los orígenes CORS habilitados
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Ejecutar la aplicación solo en modo de desarrollo
if __name__ == "__main__":
    logger.warning("Ejecutando en modo de desarrollo. No ejecute así en producción.")
    import uvicorn

    uvicorn.run(app, host="localhost", port=8001, log_level="debug")
