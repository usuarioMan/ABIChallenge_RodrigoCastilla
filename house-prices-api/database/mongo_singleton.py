import pymongo
from loguru import logger
from decouple import config


MONGODBURI = mongodb_uri = config('MONGODBURI')

def crear_cliente_mongodb():
    try:
        client = pymongo.MongoClient(MONGODBURI)
        client.server_info()
        logger.info("Conexión establecida correctamente.")
        return client
        
    except Exception as e:
        assert False, f"No se pudo conectar a la base de datos. Error: {e}"


class ConexionMongoDB:
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super(ConexionMongoDB, cls).__new__(cls)
            cls._instancia.cliente = crear_cliente_mongodb()
        return cls._instancia

    def __getitem__(self, key):
        # Permite acceder a la base de datos usando corchetes
        return self.cliente[key]

    def __enter__(self):
        # Este método se llama al comienzo del bloque `with`
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # Este método se llama al final del bloque `with`
        self.cliente.close()
