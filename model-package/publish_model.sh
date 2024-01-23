#!/bin/bash

# Construir paquetes y subirlos a un repositorio Gemfury

GEMFURY_URL=$GEMFURY_PUSH_URL # La URL del repositorio Gemfury se pasa como variable de entorno
echo "URL de Gemfury: $GEMFURY_URL"

set -e # Terminar el script si hay algún error

DIRS="$@"        # Directorios a construir (se pueden pasar como argumentos)
BASE_DIR=$(pwd)  # Directorio base del script
SETUP="setup.py" # Archivo de configuración de Python

warn() {
    echo "$@" 1>&2 # Función para imprimir mensajes de advertencia
}

die() {
    warn "$@" # Función para imprimir mensajes de error y salir del script
    exit 1
}

build() {
    DIR="${1/%\//}" # Eliminar la barra al final del nombre del directorio
    echo "Verificando el directorio $DIR"
    cd "$BASE_DIR/$DIR"
    [ ! -e $SETUP ] && warn "No hay archivo $SETUP, omitiendo" && return # Si no existe el archivo de configuración, omitir
    PACKAGE_NAME=$(python $SETUP --fullname)                             # Obtener el nombre completo del paquete desde el archivo de configuración
    echo "Paquete $PACKAGE_NAME"
    python "$SETUP" sdist bdist_wheel || die "Error al construir el paquete $PACKAGE_NAME"
    for X in $(ls dist); do
        curl -F package=@"dist/$X" "$GEMFURY_URL" || die "Error al subir el paquete $PACKAGE_NAME en el archivo dist/$X"
    done
}

# Si se proporcionan directorios como argumentos, construir solo esos directorios
if [ -n "$DIRS" ]; then
    for dir in $DIRS; do
        build $dir
    done
else
    # Si no se proporcionan argumentos, construir todos los directorios en el directorio actual
    ls -d */ | while read dir; do
        build $dir
    done
fi
