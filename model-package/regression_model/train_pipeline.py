import numpy as np
from config.core import config
from pipeline import price_pipe
from processing.data_manager import load_dataset, save_pipeline
from sklearn.model_selection import train_test_split


def run_training() -> None:
    """Entrenar el modelo."""

    # Leer los datos de entrenamiento
    data = load_dataset(file_name=config.app_config.training_data_file)

    # Dividir en conjuntos de entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(
        data[config.model_config.features],  # predictores
        data[config.model_config.target],
        test_size=config.model_config.test_size,
        # Configurando la semilla aleatoria aquí
        # para reproducibilidad
        random_state=config.model_config.random_state,
    )
    y_train = np.log(y_train)

    # Ajustar el modelo
    price_pipe.fit(X_train, y_train)

    # Persistir el modelo entrenado
    save_pipeline(pipeline_to_persist=price_pipe)


if __name__ == "__main__":
    run_training()
