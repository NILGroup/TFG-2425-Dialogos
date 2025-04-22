import json
from BD.ConnectionMongo import ConexionMongoDB

    
def JSON_formateado(texto_ia:str)->json:
    try:
        return json.loads(texto_ia)  #Devuelve el JSON
    except json.JSONDecodeError as e:
        print("❌ Error al decodificar JSON:", e)
        return {}  #Si no se puede decodificar, devuelve un diccionario vacío
    

def json_texto(texto:str, seccion:str)->json:
    """Convierte el texto de la IA a un formato JSON para MongoDB."""
    return{ "Seccion": seccion, "texto": texto.strip() }