import logging

from regression_model.config.core import PACKAGE_ROOT, config

# Se recomienda encarecidamente que no se agreguen manejadores de registro
# distintos de NullHandler a los registradores de su biblioteca. Esto se debe
# a que la configuración de los manejadores es tarea del desarrollador de la
# aplicación que utiliza su biblioteca.
# https://docs.python.org/3/howto/logging.html#configuring-logging-for-a-library
logging.getLogger(config.app_config.package_name).addHandler(logging.NullHandler())

# Abre el archivo "VERSION" ubicado en el directorio PACKAGE_ROOT y lee el número
# de versión, luego elimina cualquier espacio en blanco alrededor.
with open(PACKAGE_ROOT / "VERSION") as version_file:
    __version__ = version_file.read().strip()
