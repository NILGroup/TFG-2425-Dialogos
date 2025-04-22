from AI.AIManager import get_ai_response, generar_JSON_mongo, get_ai_response_fast, detectar_seccion
import story.StoryStorage as ss
import story.StoryFormatter as sf

from flet import Page

class StoryController:
    def __init__(self):
        self.messages = []
        self.seccion = "INICIO"
        self.contexto = ""
        self.estado_secciones = {
            "INICIO": False,
            "TRAMA E HILO SIMBOLICO": False,
            "DESCRIPCION DEL MUNDO": False,
            "DESCRIPCION DE ESCENARIOS": False,
            "PERSONAJES PRINCIPALES": False,
            "PERSONAJES SECUNDARIOS": False,
            "ANALISIS DE LA HISTORIA": False,
            "ESTRUCTURA DE CAPITULOS": False,
            "ESCRITURA DE CAPITULOS": False
        }


   
    def cambiar_estado_seccion(self, seccion):
        self.estado_secciones[seccion] = not self.estado_secciones[seccion]

    def siguiente_seccion_pendiente(self):
        for seccion, estado in self.estado_secciones.items():
            if not estado:
                return seccion
        return None

    def elegir_modo(self, page:Page):
        modo = page.client_storage.get("modo")
        return modo
    
        
    def procesar_mensaje(self, user_input, page):
        modo = self.elegir_modo(page)
        # self.messages.append({"role": "user", "content": user_input})
        # if modo == "rapido":
        #     ai_response = get_ai_response_fast(self.messages)
        # else:
        #     ai_response = get_ai_response(self.messages)
        # self.messages.append({"role": "assistant", "content": ai_response})


        if modo == "rapido":
            ai_response = get_ai_response_fast([{"role": "user", "content": mensaje}])
        else:
            print(f"Sección actual: {self.seccion}")
            self.estado_secciones[self.seccion] = True

            nueva_seccion = detectar_seccion(user_input, self.seccion, self.estado_secciones)
            print(f"Estado de secciones: {self.estado_secciones}")
            print(f"Nueva seccion: {nueva_seccion}")
            self.seccion = nueva_seccion
            self.contexto = ss.buscar_dependencias_bd(self.seccion)
            print(f"Contexto: {self.contexto}")
            mensaje = f"{self.contexto}\n{user_input}"
            ai_response = get_ai_response([{"role": "user", "content": mensaje}])


        ai_json = generar_JSON_mongo(ai_response)
        formateado = sf.JSON_formateado(ai_json)
        if formateado == "":
            print(ai_json)
        #seccion = formateado.get("Seccion")
        texto = sf.json_texto(ai_response, self.seccion)
        ss.guardar_texto(texto)
        ss.guardar_doc(formateado, self.seccion)
        
        print("\n\n\n ----------------------\n\n\n")
        return ai_response

