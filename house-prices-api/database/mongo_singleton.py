import os
import pymongo
from loguru import logger
from dotenv import load_dotenv


load_dotenv()
MONGODBURI = os.getenv('MONGODBURI')

class ConexionMongoDB:
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super(ConexionMongoDB, cls).__new__(cls)
            cls._instancia.cliente = pymongo.MongoClient(MONGODBURI)
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
