from database.mongo_singleton import ConexionMongoDB

NOMBRE_COLECCION_RESULTADOS = "resultados_prediccion"

def guardar_resultados(resultados):
    with ConexionMongoDB() as conexion:
        coleccion_resultados = conexion.cliente['ChallengeMLOPS'][NOMBRE_COLECCION_RESULTADOS]
        coleccion_resultados.insert_many(resultados)
