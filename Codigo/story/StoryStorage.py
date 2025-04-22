from BD.ConnectionMongo import ConexionMongoDB
from enum import Enum

mongo = ConexionMongoDB("Nueva_Prueba2")

class SeccionHistoria(Enum):
    TRAMA = "TRAMA E HILO SIMBOLICO"
    MUNDO = "DESCRIPCION DEL MUNDO"
    ESCENARIOS = "DESCRIPCION DE ESCENARIOS"
    PERSONAJES_P = "PERSONAJES PRINCIPALES"
    PERSONAJES_S = "PERSONAJES SECUNDARIOS"
    ANALISIS = "ANALISIS DE LA HISTORIA"
    CAPITULOS = "ESTRUCTURA DE CAPITULOS"
    ESCRITURA = "ESCRITURA DE CAPITULOS"
    UPDATE = "UPDATE"

dependencias = {
    "TRAMA E HILO SIMBOLICO": [],
    "DESCRIPCION DEL MUNDO": ["TRAMA E HILO SIMBOLICO"],
    "PERSONAJES PRINCIPALES": ["TRAMA E HILO SIMBOLICO"],
    "PERSONAJES SECUNDARIOS": ["TRAMA E HILO SIMBOLICO", "PERSONAJES PRINCIPALES"],
    "DESCRIPCION DE ESCENARIOS": ["TRAMA E HILO SIMBOLICO", "DESCRIPCION DEL MUNDO"],
    "ANALISIS DE LA HISTORIA": ["TRAMA E HILO SIMBOLICO", "DESCRIPCION DEL MUNDO", "PERSONAJES PRINCIPALES"],
    "ESTRUCTURA DE CAPITULOS": ["TRAMA E HILO SIMBOLICO", "ANALISIS DE LA HISTORIA"]
}


def eliminar_seccion_json(json_formateado):
    """Elimina la sección del JSON formateado para poder insertarlo en MongoDB."""
    json_formateado.pop("Seccion", None)
    return json_formateado

def listas_bd(seccion):
    """Creo el nombre de las listas de la seccion para la base de datos"""
    if seccion == SeccionHistoria.ESCENARIOS.value:
        return "Escenarios"
    elif seccion == SeccionHistoria.PERSONAJES_P.value or seccion == SeccionHistoria.PERSONAJES_S.value:
        return "Personajes"
    else:
        return None

def guardar_resumen(resumen):
    mongo.seleccionar_coleccion("RESUMEN")
    mongo.insertar(resumen, "RESUMEN")


def buscar_dependencias_bd(seccion_actual: str) -> str:
    """Busca en la base de datos las secciones necesarias para el contexto."""
    secciones_necesarias = dependencias.get(seccion_actual, [])
    print(f"SECCIONES: {secciones_necesarias}")
    contexto = ""
    mongo.seleccionar_coleccion("CONTEXTO")
    if mongo.hay_documentos():
        for seccion in secciones_necesarias:
            texto = mongo.devolver_documentos(seccion)
            contexto += texto
    text = contexto.replace("\n", " ")
    return text

def guardar_texto(texto: dict):
    mongo.seleccionar_coleccion("CONTEXTO")
    mongo.insertar(texto, "CONTEXTO")

def guardar_doc(json_mongo, seccion):
    if seccion == SeccionHistoria.UPDATE:
        mongo.seleccionar_coleccion("UPDATE")
        mongo.insertar(json_mongo, seccion)
    elif seccion == None:
        mongo.seleccionar_coleccion("OTROS")
        mongo.insertar(json_mongo, "OTROS")
    elif seccion == SeccionHistoria.ESCENARIOS.value or seccion == SeccionHistoria.PERSONAJES_P.value or seccion == SeccionHistoria.PERSONAJES_S.value:
        mongo.seleccionar_coleccion(seccion)
        if mongo.hay_documentos():
            print(f"Estoy modficando '{seccion}'")
            formateado = eliminar_seccion_json(json_mongo)
            print(formateado)
            mongo.nuevo_escenario_personaje("Seccion", seccion, listas_bd(seccion), formateado)
        else:
            mongo.insertar(json_mongo, seccion)
    else:
        mongo.seleccionar_coleccion(seccion)
        if mongo.hay_documentos():
            doc_previo = mongo.buscar("Seccion", seccion)   #Busco ese documento
            mongo.seleccionar_coleccion("UPDATE")   #Me muevo a la coleccion de UPDATE
            mongo.insertar(doc_previo, seccion) #Lo inserto en la coleccion de UPDATE
            mongo.seleccionar_coleccion(seccion)    #Cambio a la coleccion actual
            mongo.eliminar("Seccion", seccion)  #Elimino el documento antiguo
        mongo.insertar(json_mongo, seccion)