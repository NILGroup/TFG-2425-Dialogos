import json
import os
from datetime import datetime

    
def JSON_formateado(texto_ia):
    try:
        doc = json.loads(texto_ia)
        return doc
    except json.JSONDecodeError as e:
        print(f"❌ Error al decodificar JSON: {e}")
        # 🔍 Mostrar carácter conflictivo
        pos = e.pos
        if 0 <= pos < len(texto_ia):
            char = texto_ia[pos]
            contexto = texto_ia[max(0, pos-30):pos+30].replace("\n", "⏎")  # muestra 30 chars alrededor
            print(f"🔍 Carácter conflictivo: '{char}' (ord: {ord(char)}) en posición {pos}")
            print(f"🔎 Contexto alrededor: ...{contexto}...")
        else:
            print("⚠️ Posición de error fuera de rango")

        guardar_json_fallido(texto_ia, e)
        return {}



def guardar_json_fallido(texto, error):
    """Guarda el texto mal formateado y el error en un archivo para depuración."""
    carpeta_logs = "logs_json_fallidos"
    os.makedirs(carpeta_logs, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nombre_archivo = os.path.join(carpeta_logs, f"json_fallido_{timestamp}.txt")

    with open(nombre_archivo, "w", encoding="utf-8") as f:
        f.write("❌ ERROR DE DECODIFICACIÓN JSON:\n")
        f.write(str(error) + "\n\n")
        f.write("🧾 TEXTO RECIBIDO:\n")
        f.write(texto)

    print(f"📁 JSON inválido guardado en: {nombre_archivo}")

    
def json_seccion(secciones: dict)->json:
    return json.dumps(secciones, ensure_ascii=False)

def json_texto(texto:str, seccion:str)->json:
    """Convierte el texto de la IA a un formato JSON para MongoDB."""
    return{ "Seccion": seccion, "texto": texto.strip() }

def json_modo(modo:str)->json:
    """Convierte el modo a formato JSON para poder guardarlo en la BD"""
    return{ "Modo": modo}