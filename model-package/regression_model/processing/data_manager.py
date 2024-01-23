import typing as t
from pathlib import Path

import joblib
import pandas as pd
from sklearn.pipeline import Pipeline

from regression_model import __version__ as _version
from regression_model.config.core import DATASET_DIR, TRAINED_MODEL_DIR, config

def load_dataset(*, file_name: str) -> pd.DataFrame:
    """Cargar el conjunto de datos."""
    dataframe = pd.read_csv(Path(f"{DATASET_DIR}/{file_name}"))
    dataframe["MSSubClass"] = dataframe["MSSubClass"].astype("O")

    # Renombrar variables que comienzan con números para evitar errores de sintaxis
    transformed = dataframe.rename(columns=config.model_config.variables_to_rename)
    return transformed

def save_pipeline(*, pipeline_to_persist: Pipeline) -> None:
    """Persistir el pipeline."""
    # Preparar el nombre del archivo de guardado versionado
    save_file_name = f"{config.app_config.pipeline_save_file}{_version}.pkl"
    save_path = TRAINED_MODEL_DIR / save_file_name

    # Eliminar pipelines antiguos
    remove_old_pipelines(files_to_keep=[save_file_name])
    # Guardar el pipeline
    joblib.dump(pipeline_to_persist, save_path)

def load_pipeline(*, file_name: str) -> Pipeline:
    """Cargar un pipeline persistido."""
    file_path = TRAINED_MODEL_DIR / file_name
    trained_model = joblib.load(filename=file_path)
    return trained_model

def remove_old_pipelines(*, files_to_keep: t.List[str]) -> None:
    """
    Eliminar pipelines antiguos.
    Esto asegura que haya una correspondencia simple
    entre la versión del paquete y la versión del modelo
    que será importada y utilizada por otras aplicaciones.
    """
    do_not_delete = files_to_keep + ["__init__.py"]
    for model_file in TRAINED_MODEL_DIR.iterdir():
        if model_file.name not in do_not_delete:
            model_file.unlink()
