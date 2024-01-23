#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path

from setuptools import find_packages, setup

# Metadatos del paquete.
NOMBRE = 'tid-regression-model'
DESCRIPCION = "Ejemplo de paquete de modelo de regresión"
EMAIL = "castilla.ar@gmail.com"
AUTOR = "Rodrigo Castilla"
REQUIERE_PYTHON = ">=3.7.0"

# La descripción larga se establece igual a la descripción corta en este caso.
descripcion_larga = DESCRIPCION

# Cargar el archivo VERSION del paquete como un diccionario.
about = {}
ROOT_DIR = Path(__file__).resolve().parent
REQUIREMENTS_DIR = ROOT_DIR / 'requirements'
PACKAGE_DIR = ROOT_DIR / 'regression_model'
with open(PACKAGE_DIR / "VERSION") as f:
    _version = f.read().strip()
    about["__version__"] = _version

# Función para listar los requisitos del módulo.
def list_reqs(fname="requirements.txt"):
    with open(REQUIREMENTS_DIR / fname) as fd:
        return fd.read().splitlines()

# Configuración del paquete:
setup(
    name=NOMBRE,
    version=about["__version__"],
    description=DESCRIPCION,
    long_description=descripcion_larga,
    long_description_content_type="text/markdown",
    author=AUTOR,
    author_email=EMAIL,
    python_requires=REQUIERE_PYTHON,
    packages=find_packages(exclude=("tests",)),
    package_data={"regression_model": ["VERSION"]},
    install_requires=list_reqs(),
    extras_require={},
    include_package_data=True,
    license="BSD-3",
    classifiers=[
        # Clasificadores Trove
        # Lista completa: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
)
