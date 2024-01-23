# ABIChallenge_RodrigoCastilla

## Descripción General

Este proyecto muestra la implementación de un modelo de aprendizaje automático utilizando CircleCI y Railway. La aplicación desplegada está disponible en [famed-board-production.up.railway.app](https://famed-board-production.up.railway.app/).

### Estructura del Proyecto

```
ABIChallenge_RodrigoCastilla
│
├── CICIDOverview.png
├── Dockerfile
├── README.md
├── architecture.png
├── house-prices-api
│   ├── Procfile
│   ├── app
│   ├── database
│   ├── mypi.ini
│   ├── requirements.txt
│   ├── run.sh
│   ├── test_requirements.txt
│   ├── tox.ini
│   └── typing_requirements.txt
├── model-package
│   ├── MANIFEST.in
│   ├── mypy.ini
│   ├── publish_model.sh
│   ├── pyproject.toml
│   ├── regression_model
│   ├── requirements
│   ├── setup.py
│   ├── tests
│   └── tox.ini
└── sonar-project.properties
```

### Despliegue con Docker

El archivo `Dockerfile` se utiliza para implementar el proyecto en Railway. Para ejecutarlo localmente, utiliza los siguientes comandos:

```bash
docker build --build-arg PIP_EXTRA_INDEX_URL=https://fYApnWWSSLnRz6fKfxEU@push.fury.io/usuarioman/ -t house-prices-api:latest .
docker run -p 8001:8001 -e PORT=8001 house-prices-api
```

### house-prices-api

Este directorio contiene el código de la API que expone el modelo de aprendizaje automático.

### model-package

Este directorio contiene el paquete con el modelo de regresión.

## Configuración y Despliegue con CircleCI

Este proyecto utiliza CircleCI para pruebas, despliegues y otras tareas del ciclo de vida de desarrollo. A continuación, se explican las configuraciones clave y el proceso de implementación.

### Configuración General

El archivo principal de configuración de CircleCI es `.circleci/config.yml`. Define la versión de la configuración, configura esferas (orbs) y especifica trabajos y pasos.

#### Trabajos y Pasos

1. **test_app**: Realiza pruebas en la aplicación utilizando Tox para gestionar entornos de prueba y ejecutar pruebas definidas en el proyecto.

2. **deploy_app_to_railway**: Implementa la aplicación en Railway, un servicio para el despliegue de aplicaciones. Utiliza Railway CLI para gestionar el despliegue.

3. **test_and_upload_regression_model**: Realiza pruebas y carga el modelo de regresión. Utiliza Tox para gestionar entornos de prueba y ejecutar pruebas definidas en el paquete del modelo.

4. **deploy_app_container_via_railway**: Este trabajo utiliza Docker de forma remota en el entorno de ejecución de CircleCI. Construye y ejecuta el Dockerfile utilizando Railway para desplegar la aplicación en un entorno de producción.

### Flujo de Trabajo

El flujo de trabajo principal se llama `deploy_pipeline` y consiste en varios trabajos que se ejecutan de manera secuencial o paralela, según dependencias y condiciones.

1. **test_app**: Se ejecuta con cada cambio en las ramas principales (`main` y `dev`).

2. **test_and_upload_regression_model**: Se ejecuta solo cuando se crean etiquetas en Git. Realiza pruebas y carga el modelo de regresión. Esto es útil para generar versiones del proyecto mediante lanzamientos y etiquetas de Git.

3. **deploy_app_container_via_railway**: Se ejecuta solo en cambios en las ramas principales (`main` y `dev`). Construye y ejecuta el Dockerfile utilizando Railway para desplegar la aplicación en un entorno de producción.

### Tox y Pruebas

Tox se utiliza para gestionar entornos virtuales y ejecutar pruebas en diferentes configuraciones. Los comandos `tox -e fetch_data` y `tox -e publish_model` realizan tareas específicas, como obtener datos y publicar el modelo en Gemfury.
