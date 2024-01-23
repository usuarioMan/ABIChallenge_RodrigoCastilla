import json
from typing import Any

import numpy as np
import pandas as pd
from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from loguru import logger
from regression_model import __version__ as model_version
from regression_model.predict import make_prediction

from app import __version__, schemas
from app.config import settings

# Crear un router para la API
api_router = APIRouter()

# Endpoint para verificar la salud de la aplicación
@api_router.get("/health", response_model=schemas.Health, status_code=200)
def health() -> dict:
    """
    Ruta de raíz para verificar la salud de la aplicación
    """
    health = schemas.Health(
        name=settings.PROJECT_NAME, api_version=__version__, model_version=model_version
    )

    return health.dict()

# Endpoint para realizar predicciones de precios de casas
@api_router.post("/predict", response_model=schemas.PredictionResults, status_code=200)
async def predict(input_data: schemas.MultipleHouseDataInputs) -> Any:
    """
    Realizar predicciones de precios de casas con el modelo de regresión TID
    """

    # Convertir los datos de entrada a un DataFrame de pandas
    input_df = pd.DataFrame(jsonable_encoder(input_data.inputs))

    # TODO: Mejorar el rendimiento de la API convirtiendo la función
    # `make_prediction` en una función asíncrona y utilizando await aquí.
    logger.info(f"Haciendo predicción con inputs: {input_data.inputs}")
    results = make_prediction(input_data=input_df.replace({np.nan: None}))

    # Manejar errores de validación en las predicciones
    if results["errors"] is not None:
        logger.warning(f"Error de validación en la predicción: {results.get('errors')}")
        raise HTTPException(status_code=400, detail=json.loads(results["errors"]))

    logger.info(f"Resultados de la predicción: {results.get('predictions')}")

    return results
