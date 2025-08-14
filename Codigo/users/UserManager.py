import json
import os

USER_FILE = "users/users.json"

def cargar_usuarios():
    try:
        if os.path.exists(USER_FILE):
            with open(USER_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data if isinstance(data, dict) else {}  # Asegurar que sea dict
        return {}  # Si el archivo no existe
    except (json.JSONDecodeError, PermissionError, OSError):
        return {}  # Si hay error de lectura, archivo corrupto o sin permisos

    
def buscar_usuario(username):
    usuarios = cargar_usuarios()
    if not usuarios:
        return None
    return usuarios.get(username) #Si no existe el username retorna None

def buscar_correo(email):
    usuarios = cargar_usuarios()
    for datos in usuarios.values():
        if datos.get("email") == email:
            return True
    return False

def guardar_usuarios(usuarios):
   with open(USER_FILE, 'w', encoding='utf-8') as f:
            json.dump(usuarios, f, indent=2, ensure_ascii=False)

def registrar_usuario(email, username, password):
    usuarios = cargar_usuarios()
    usuario = buscar_usuario(username)
    if usuario:
        return False
    else:
        usuarios[username] = {
            "email": email,
            "password": password
        }
        print(usuarios)
        guardar_usuarios(usuarios)
        return True

def validar_login(username, password):
    usuario = buscar_usuario(username)
    return not usuario and usuario["password"] == password
    
