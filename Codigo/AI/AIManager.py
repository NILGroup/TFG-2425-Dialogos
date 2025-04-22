import re
from groq import Groq
import AI.Utils as Utils
import json

groqKey = "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"
client = Groq(api_key="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")

PROMPT_INICIAL = Utils.PROMPT_INICIAL
PROMPT_JSON = Utils.PROMPT_JSON
PROMPT_INCIAL_RAPIDO = Utils.PROMP_ESCRITURA_RAPIDA
PROMP_TEXTO = Utils.PROMPT_TEXTO
PROMPT_SECCION = Utils.PROMPT_SECCION

def clean_ai_response(response:str)->str:
    """Elimina etiquetas <think>...</think> del texto."""
    return re.sub(r"<think>.*?</think>", "", response, flags=re.DOTALL).strip()

def get_ai_response(messages:str)->str:
    """Obtiene la respuesta de Groq AI y la limpia antes de mostrarla."""
    # Agregar mensaje del sistema
    messages.insert(0, {
        "role": "system",
        "content": PROMPT_INICIAL
    })

    completion = client.chat.completions.create(
        model="deepseek-r1-distill-llama-70b",
        messages=messages,
        temperature=0.8,
        max_tokens=4096,
    )
    
    # Obtener la respuesta sin <think>...</think>
    raw_response = completion.choices[0].message.content
    return clean_ai_response(raw_response)


def get_ai_response_fast(messages: str)->str:
    """Obtiene la respuesta de Groq AI y la limpia antes de mostrarla."""
    # Agregar mensaje del sistema solo una vez
    if not any(m["role"] == "system" for m in messages):
        messages.insert(0, {
            "role": "system",
            "content": PROMPT_INCIAL_RAPIDO
        })

    completion = client.chat.completions.create(
        model="deepseek-r1-distill-llama-70b",
        messages=messages,
        temperature=0.7,
        max_tokens=4096,
        stream=False,
    )
    
    # Obtener la respuesta sin <think>...</think>
    raw_response = completion.choices[0].message.content
    return clean_ai_response(raw_response)

def get_ai_response_others(messages):
    completion = client.chat.completions.create(
        model="deepseek-r1-distill-llama-70b",
        messages=messages,
        temperature=0.7,
        max_tokens=4096,
        stream=False,
    )
    
    # Obtener la respuesta sin <think>...</think>
    raw_response = completion.choices[0].message.content
    return clean_ai_response(raw_response)

def contar_tokens(texto):
    """Aproxima la cantidad de tokens en un mensaje (1 palabra ≈ 1.3 tokens)."""
    return int(len(texto.split()) * 1.5)  # Multiplicamos por 1.3 para ser más precisos

def detectar_seccion(texto: str, seccion: str, estado_secciones: dict) -> str:
    """
    Clasifica el texto del usuario en una sección narrativa utilizando un modelo de lenguaje.

    Parameters:
        texto (str): Entrada del usuario que se desea clasificar.
        seccion (str): Sección actual estimada o en curso.
        estado_secciones (dict): Estado de avance de todas las secciones narrativas.

    Returns:
        str: Nombre de la sección detectada por la IA.
    """
    # Definir las secciones posibles
    seccion_prompt = [
        {"role": "system", "content": f"{PROMPT_SECCION} \n\n Estado de las secciones: {json.dumps(estado_secciones, indent=2)}"},
        {"role": "user", "content": f"Seccion actual: {seccion} -> {texto}"}
    ]

    detectar_seccion = get_ai_response_others(seccion_prompt)
    return detectar_seccion


def generar_JSON_mongo(ai_response:str)->str:
    """Convertir la respuesta de la IA a formato JSON para poder añadirlo a Mongo"""
        # 📌 Llamar a la IA para resumir el texto
    JSON_prompt = [
        {"role": "system", "content": PROMPT_JSON
        },
        {"role": "user", "content": ai_response}
    ]

    mongo_JSON = get_ai_response(JSON_prompt)

    return mongo_JSON