# Se utiliza la imagen base de Python 3.11
FROM python:3.11

# Se crea el usuario que ejecutará la aplicación
RUN adduser --disabled-password --gecos '' ml-api-user

# Se establece el directorio de trabajo para la aplicación
WORKDIR /opt/house-prices-api

# Se define un argumento para el índice extra de pip el servidor de paquetes Gemfury
ARG PIP_EXTRA_INDEX_URL

# Se copian los archivos de la aplicación al directorio de trabajo
ADD ./house-prices-api /opt/house-prices-api/

# Se actualiza pip y se instalan las dependencias definidas en requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /opt/house-prices-api/requirements.txt

# Se otorgan permisos de ejecución al script de inicio
RUN chmod +x /opt/house-prices-api/run.sh

# Se cambia el propietario de los archivos al usuario creado anteriormente
RUN chown -R ml-api-user:ml-api-user ./

# Se establece el usuario que ejecutará la aplicación
USER ml-api-user

# Se expone el puerto 8001
EXPOSE 8001

# Se define el comando que se ejecutará al iniciar el contenedor
CMD ["bash", "./run.sh"]
