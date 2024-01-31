import pytest
from database.mongo_singleton import crear_cliente_mongodb
from loguru import logger
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection


def test_database_operations():
    # Crear cliente MongoDB y obtener instancias de base de datos y colección
    mongo_client: MongoClient = crear_cliente_mongodb()
    mongo_database: Database = mongo_client.ChallengeMLOPS
    mongo_collection: Collection = mongo_database.get_collection('resultados_prediccion')
    
    # Asegurar que son instancias válidas
    assert isinstance(mongo_client, MongoClient), "No es una instancia de MongoClient."
    assert isinstance(mongo_database, Database), "No es una instancia válida de una base de datos."
    assert isinstance(mongo_collection, Collection), "No es una instancia válida de una colección de MongoDB."
    
    # Crear una colección para logs
    log_collection = mongo_database.get_collection('test_logs')

    # CRUD - Create
    log_entry = {"message": "Prueba de log", "level": "INFO"}
    result = log_collection.insert_one(log_entry)
    assert result.inserted_id is not None, "Error al crear el log."

    # CRUD - Read
    logs_count = log_collection.count_documents({})
    assert logs_count > 0, "Error al leer los logs."

    # CRUD - Update (actualizar el primer log)
    updated_log_entry = {"$set": {"message": "Log actualizado"}}
    update_result = log_collection.update_one({"_id": result.inserted_id}, updated_log_entry)
    assert update_result.modified_count == 1, "Error al actualizar el log."

    # CRUD - Read (nuevamente para ver la actualización)
    updated_log = log_collection.find_one({"_id": result.inserted_id})
    assert updated_log["message"] == "Log actualizado", "Error al leer el log actualizado."

    # CRUD - Delete (eliminar el primer log)
    delete_result = log_collection.delete_one({"_id": result.inserted_id})
    assert delete_result.deleted_count == 1, "Error al eliminar el log."

    # Cerrar la conexión al finalizar
    mongo_client.close()
