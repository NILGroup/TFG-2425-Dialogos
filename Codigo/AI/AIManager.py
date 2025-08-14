import re
from groq import Groq
import AI.Utils as Utils
import json

groqKey = "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"
client = Groq(api_key="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")

PROMPT_INICIAL = Utils.PROMPT_INICIAL
PROMPT_JSON = Utils.PROMPT_JSON
PROMPT_INCIAL_RAPIDO = Utils.PROMPT_ESCRITURA_RAPIDA
PROMP_TEXTO = Utils.PROMPT_TEXTO
PROMPT_CAPITULOS = Utils.PROMPT_CAPITULOS
PROMPT_ESCRITURA_JSON = Utils.PROMPT_ESCRITURA_JSON
PROMPT_RESUMEN_CAPITULO = Utils.PROMPT_RESUMEN_CAPITULO
PROMPT_RESUMEN = Utils.PROMPT_RESUMEN
PROMPT_CAPITULO_A_JSON = Utils.PROMPT_CAPITULO_A_JSON

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
        model="llama3-70b-8192",
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
        model="llama3-70b-8192",
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
        model="llama3-70b-8192",
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



def generar_JSON_mongo(ai_response:str)->str:
    """Convertir la respuesta de la IA a formato JSON para poder añadirlo a Mongo"""
        # 📌 Llamar a la IA para resumir el texto
    JSON_prompt = [
        {"role": "system", "content": PROMPT_JSON
        },
        {"role": "user", "content": ai_response}
    ]

    mongo_JSON = get_ai_response_others(JSON_prompt)

    return mongo_JSON

def generar_capitulo(ai_response:str)->str:
    """Convertir la respuesta de la IA a formato JSON para poder añadirlo a Mongo"""
        # 📌 Llamar a la IA para resumir el texto
    promtp = [
        {"role": "system", "content": PROMPT_CAPITULOS
        },
        {"role": "user", "content": ai_response}
    ]

    capitulo = get_ai_response_others(promtp)

    return capitulo

def generar_JSON_capitulo_mongo(ai_response:str)->str:
    """Convertir la respuesta de la IA a formato JSON para poder añadirlo a Mongo"""
        # 📌 Llamar a la IA para resumir el texto
    JSON_prompt = [
        {"role": "system", "content": PROMPT_CAPITULO_A_JSON
        },
        {"role": "user", "content": ai_response}
    ]

    mongo_JSON = get_ai_response_others(JSON_prompt)

    return mongo_JSON

def generar_resumen_capitulo(ai_response:str)->str:
    """Convertir la respuesta de la IA a formato JSON para poder añadirlo a Mongo"""
        # 📌 Llamar a la IA para resumir el texto
    resumen_prompt = [
        {"role": "system", "content": PROMPT_RESUMEN_CAPITULO
        },
        {"role": "user", "content": ai_response}
    ]

    resumen_JSON = get_ai_response_others(resumen_prompt)
    return resumen_JSON


def generar_resumen(ai_response:str)->str:
        # 📌 Llamar a la IA para resumir el texto
    print("\nGENERANDO RESUMEN\n")
    resumen_prompt = [
        {"role": "system", "content": PROMPT_RESUMEN
        },
        {"role": "user", "content": ai_response}
    ]

    resumen_JSON = get_ai_response_others(resumen_prompt)

    return resumen_JSON