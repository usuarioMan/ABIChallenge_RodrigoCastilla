import logging
import sys
from types import FrameType
from typing import List, cast

from loguru import logger
from pydantic import AnyHttpUrl, BaseSettings

# Configuración para el manejo de registros (logging)
class LoggingSettings(BaseSettings):
    LOGGING_LEVEL: int = logging.INFO  # Los niveles de registro son de tipo int


# Configuración general de la aplicación
class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"

    # Meta
    logging: LoggingSettings = LoggingSettings()

    # BACKEND_CORS_ORIGINS es una lista de orígenes separados por comas
    # Ejemplo: http://localhost,http://localhost:4200,http://localhost:3000
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
        "http://localhost:3000",  # type: ignore
        "http://localhost:8000",  # type: ignore
        "https://localhost:3000",  # type: ignore
        "https://localhost:8000",  # type: ignore
    ]

    PROJECT_NAME: str = "House Price Prediction API"

    class Config:
        case_sensitive = True


# Manejador de registros personalizado para Loguru
class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:  # pragma: no cover
        # Obtener el nivel de Loguru correspondiente si existe
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = str(record.levelno)

        # Encontrar el origen de la llamada de donde se originó el mensaje registrado
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:  # noqa: WPS609
            frame = cast(FrameType, frame.f_back)
            depth += 1

        # Registrar el mensaje utilizando Loguru
        logger.opt(depth=depth, exception=record.exc_info).log(
            level,
            record.getMessage(),
        )


def setup_app_logging(config: Settings) -> None:
    """Preparar el registro personalizado para nuestra aplicación."""

    LOGGERS = ("uvicorn.asgi", "uvicorn.access")
    logging.getLogger().handlers = [InterceptHandler()]
    for logger_name in LOGGERS:
        logging_logger = logging.getLogger(logger_name)
        logging_logger.handlers = [InterceptHandler(level=config.logging.LOGGING_LEVEL)]

    # Configurar Loguru para mostrar registros en la salida estándar de errores (stderr)
    logger.configure(
        handlers=[{"sink": sys.stderr, "level": config.logging.LOGGING_LEVEL}]
    )


# Crear una instancia de Settings para usarla en la aplicación
settings = Settings()
