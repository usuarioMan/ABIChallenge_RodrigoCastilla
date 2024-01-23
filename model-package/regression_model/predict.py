import typing as t

import numpy as np
import pandas as pd

from regression_model import __version__ as _version
from regression_model.config.core import config
from regression_model.processing.data_manager import load_pipeline
from regression_model.processing.validation import validate_inputs

# Nombre del archivo del pipeline
pipeline_file_name = f"{config.app_config.pipeline_save_file}{_version}.pkl"
# Cargar el pipeline guardado
_price_pipe = load_pipeline(file_name=pipeline_file_name)

def make_prediction(
    *,
    input_data: t.Union[pd.DataFrame, dict],
) -> dict:
    """Realizar una predicción utilizando un pipeline de modelo guardado."""

    data = pd.DataFrame(input_data)
    # Validar los datos de entrada
    validated_data, errors = validate_inputs(input_data=data)
    results = {"predictions": None, "version": _version, "errors": errors}

    if not errors:
        # Realizar las predicciones
        predictions = _price_pipe.predict(
            X=validated_data[config.model_config.features]
        )
        results = {
            "predictions": [np.exp(pred) for pred in predictions],  # tipo: ignorar
            "version": _version,
            "errors": errors,
        }

    return results
