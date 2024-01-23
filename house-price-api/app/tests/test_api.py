import math

import numpy as np
import pandas as pd
from fastapi.testclient import TestClient


def test_make_prediction(client: TestClient, test_data: pd.DataFrame) -> None:
    # Given
    # Preparar los datos de prueba en el formato esperado por el modelo
    payload = {
        # Asegurarse de que Pydantic funcione bien con np.nan
        "inputs": test_data.replace({np.nan: None}).to_dict(orient="records")
    }

    # When
    # Enviar la solicitud de predicción al endpoint correspondiente
    response = client.post(
        "http://localhost:8001/api/v1/predict",
        json=payload,
    )

    # Then
    # Verificar que la respuesta tenga el código de estado esperado
    assert response.status_code == 200

    # Extraer los datos de predicción de la respuesta
    prediction_data = response.json()

    # Verificar que se obtuvieron predicciones y no hay errores
    assert prediction_data["predictions"]
    assert prediction_data["errors"] is None

    # Verificar que la predicción está dentro de una tolerancia relativa específica
    assert math.isclose(prediction_data["predictions"][0], 113422, rel_tol=100)
