from AI.AIManager import *
from story.StoryStorage import StoryStorage
import story.StoryFormatter as sf
from transformers import AutoTokenizer
import re
import AI.Utils as Utils



#from flet import Page

class StoryController:
    def __init__(self, page, nueva_historia):
        self.messages = []
        self.contexto = ""
        self.page = page

        self.nombre_historia = page.session.get("nombre_bd")
        self.user = page.session.get("usuario")
        self.chapter = 1
        self.storage = StoryStorage(self.nombre_historia)
        if nueva_historia:
            self.estado_secciones = {
                "inicio": True,
                "trama_e_hilo_simbolico": False,
                "descripcion_del_mundo": False,
                "personajes_principales": False,
                "descripcion_de_escenarios": False,
                "estructura_de_capitulos": False,
                "escritura": False,
            }
            self.modo = page.session.get("modo")
            #self.seccion = "inicio"
            self.storage.guardar_info_historia(self.user, self.modo, self.estado_secciones)
        else:
            historia = self.storage.cargar_info_historia(self.user)
            self.modo = historia.get("Modo")
            self.estado_secciones = historia.get("Estado_secciones")
            #self.seccion = self.storage.ultima_seccion(self.estado_secciones)
            print(f"Modo: {self.modo}")
            print(f"Estado_secciones: {self.estado_secciones}")
            #print(f"Seccion: {self.seccion}")
            
    def guardar_en_pdf(self, nombre_archivo):
        self.storage.historia_a_pdf(nombre_archivo)


    def next_chapter(self):
        self.chapter += 1

    def ant_chapter(self):
        self.chapter -= 1

    def contar_tokens(self, texto):
        tokenizer = AutoTokenizer.from_pretrained("deepseek-ai/deepseek-r1-distill-llama-70b")
        
        # Tokenizar
        tokens = tokenizer.tokenize(texto)
        num_tokens = len(tokens)
        
        # Calcular palabras (método robusto)
        palabras = len(re.findall(r'\b\w+\b', texto))  # Usa regex para palabras
        relacion = num_tokens / palabras if palabras > 0 else 0
        
        return num_tokens, palabras, relacion
    
    def guardar_datos(self, ai_response, seccion):
        
        if self.modo == "detallado":
            if seccion == "escritura":
                ai_json = generar_JSON_capitulo_mongo(ai_response)
                resumen_capitulo = generar_resumen_capitulo(ai_response)
                resumen_json = sf.JSON_formateado(resumen_capitulo)
                self.storage.guardar_resumen(resumen_json, seccion)
                #self.storage.guardar_capitulo(ai_json)
                print(f"*************** CAPITULO {self.chapter}*****************\n\n")
                print(ai_json)
                print("***************** FIN ********************")
            else:
                ai_json = generar_JSON_mongo(ai_response)
                resumen_seccion = generar_resumen(ai_response)
                resumen_json = sf.JSON_formateado(resumen_seccion)
                self.storage.guardar_resumen(resumen_json, seccion)
                texto = sf.json_texto(ai_response, seccion)
                self.storage.guardar_texto(texto)
            formateado = sf.JSON_formateado(ai_json)
            intentos = 0
            while formateado == {} and intentos < 3:
                print("JSON vacio, volviendo a pedir respuesta")
                ai_json = generar_JSON_mongo(ai_response)
                formateado = sf.JSON_formateado(ai_json)
                intentos += 1
            self.storage.guardar_doc(formateado, seccion)
            #Quiero guardar en mongo el diccionario estado_secciones
            #self.storage.guardar_estado_secciones(self.estado_secciones)
            self.storage.actualizar_info(self.user, self.estado_secciones)
            self.storage.actualizar_estado_secciones(self.user, self.nombre_historia, self.estado_secciones)
            print("Datos guardados correctamente en la base de datos.")

    def accion_normal(self, user_input, seccion):
        print(f"Sección actual: {seccion}")
        #nueva_seccion = self.storage.primera_seccion_no_completada(self.estado_secciones)
        print(f"Estado de secciones: {self.estado_secciones}")
        if seccion == "escritura":
            self.contexto = self.storage.crear_contexto_capitulo(self.chapter)
            num, palabras, relacion = self.contar_tokens(self.contexto)
            print(f"\n\nTokens: {num}, Palabras: {palabras}, Relación: {relacion:.2f}")
            if self.chapter == 4:
                mensaje = (
                    f"\nLos capítulos anteriores son:\n{self.contexto}\n"
                    f"Los capitulos anteriores son: capitulo 1, capitulo 2 y capitulo 3\n"
                    f"Debes TERMINAR la historia con el CAPÍTULO {self.chapter}. "
                    f"Este capítulo debe ser el FINAL de la historia. "
                    f"No repitas capítulos anteriores ni reinicies desde el 1."
                )
            else:
                mensaje = (
                    f"\nLos capítulos anteriores son:\n{self.contexto}\n"
                    f"El capítulo anterior es el: {self.chapter-1}\n"
                    f"Continúa la historia con el CAPÍTULO {self.chapter}. "
                )
            print("\n\nContexto capitulo: ", mensaje)
            ai_response = generar_capitulo(mensaje)
            self.next_chapter()
        else:
            print("La seccion es: ", seccion)
            self.contexto = self.storage.buscar_dependencias_bd(seccion)
            print("Contexto: ", self.contexto)
            mensaje = f"{self.contexto}\n\nAhora toca hacer la seccion: {seccion}\nCaracteristicas: {user_input}"
            print("Mensaje enviado a la IA: ", mensaje)
            ai_response = get_ai_response([{"role": "user", "content": mensaje}])
            self.estado_secciones[seccion] = True

        return ai_response

    def accion_reescribir(self, user_input, ultimo_prompt, seccion):
        print(f"Sección actual: {seccion}")
        nueva_seccion = seccion
        print(f"Estado de secciones: {self.estado_secciones}")
        print(f"Nueva seccion: {nueva_seccion}")
        nueva_seccion = self.storage.parse_seccion(nueva_seccion)
        if seccion == "escritura":
            print("Esta desactivada la reescritura de capitulos")
            self.contexto = self.storage.crear_contexto_capitulo(self.chapter)
            print("\n\nContexto capitulo: ", self.contexto)
            num, palabras, relacion = self.contar_tokens(self.contexto)
            print(f"\n\nTokens: {num}, Palabras: {palabras}, Relación: {relacion:.2f}")
            ai_response = generar_capitulo(self.contexto)
            self.storage.guardar_capitulo(ai_response)
            self.next_chapter()
        else:
            self.contexto = self.storage.buscar_dependencias_bd(seccion)
            print("Contexto: ", self.contexto)
            resumen_seccion = self.storage.obtener_resumen(seccion)
            mensaje = f"\n\nCONTENIDO DEL MENSAJE\n\n{self.contexto}\n{user_input}\nLa seccion antigua es:{resumen_seccion}\nPrompt:{ultimo_prompt}Cambia la seccion {self.seccion}\n"
            print(mensaje)
            ai_response = get_ai_response([{"role": "user", "content": mensaje}])

        return ai_response

    def accion_actualizar(self, user_input, seccion):
        print(f"Sección actual: {seccion}")
        nueva_seccion = seccion
        print(f"Estado de secciones: {self.estado_secciones}")
        print(f"Nueva seccion: {nueva_seccion}")
        if seccion == "escritura":
            print("Esta desactivada la actualizacion de capitulos")
            self.contexto = self.storage.crear_contexto_capitulo(self.chapter)
            print("\n\nContexto capitulo: ", self.contexto)
            num, palabras, relacion = self.contar_tokens(self.contexto)
            print(f"\n\nTokens: {num}, Palabras: {palabras}, Relación: {relacion:.2f}")
            ai_response = generar_capitulo(self.contexto)
            self.storage.guardar_capitulo(ai_response)
            self.next_chapter()
        else:
            contenido_seccion = self.storage.obtener_contenido_seccion(nueva_seccion)
            mensaje = f"\n\nCONTENIDO DEL MENSAJE\n\n{contenido_seccion}\nQuiero realizar el siguiente cambio: {user_input}\nAhora toca hacer la seccion: {seccion}"
            print("-----------------", mensaje)
            ai_response = get_ai_response([{"role": "user", "content": mensaje}])

        return ai_response

    def procesar_mensaje(self, user_input, ultimo_prompt, accion, seccion):
        if self.modo is None:
            self.modo = self.storage.seleccionar_modo()

        if self.modo == "rapido":
            ai_response = get_ai_response_fast([{"role": "user", "content": user_input}])
        else:
            print(f"Accion: {accion}")
            if accion == "normal":
                print("Accion normal")
                ai_response = self.accion_normal(user_input, seccion)
            elif accion == "reescribir":
                print("Accion reescribir")
                ai_response = self.accion_reescribir(user_input, ultimo_prompt, seccion)
            elif accion == "modificar":
                print("Accion modificar")
                ai_response = self.accion_actualizar(user_input, seccion)
        self.guardar_datos(ai_response, seccion)
        return ai_response
    
    def procesar_mensaje_rapido(self, datos_encuesta, capitulo, accion, user_input):
        if accion == "continuar":
            contexto = self.storage.contexto_capitulo_rapido(capitulo)
            if capitulo == 4:
                mensaje = f"La información de la historia es:\n{datos_encuesta}\nLos capítulos anteriores son:\n{contexto}\nTermina la historia con el capítulo {capitulo}"
            else:
                mensaje = f"La información de la historia es:\n{datos_encuesta}\nLos capítulos anteriores son:\n{contexto}\nContinúa la historia con el capítulo {capitulo}"

            print(f"------------- MENSAJE --------------\n\n{mensaje}")
        elif accion == "modificar":
            capitulo_actual = self.storage.capitulo_fast(capitulo)
            mensaje = f"Este es el capitulo:\n{capitulo_actual}\nQuiero modificar esto:{user_input}\n\nVuelve a escribir el capitulo: {capitulo_actual}\n\n"
        else:
            capitulo_actual = self.storage.capitulo_fast(capitulo)
            mensaje = f"Este es el capitulo:\n{capitulo}\nNo me ha gustado quiero que lo cambies. Escribe el capitulo: {capitulo}\n\n"

        ai_response = get_ai_response_fast([{"role": "user", "content": mensaje}])
        ai_json = generar_JSON_capitulo_mongo(ai_response)
        capitulo_json = sf.JSON_formateado(ai_json)
        intentos = 0
        while capitulo_json == {} and intentos < 3:
            print("JSON vacio, volviendo a pedir respuesta")
            ai_json = generar_JSON_mongo(ai_response)
            capitulo_json = sf.JSON_formateado(ai_json)
            intentos += 1
        self.storage.guardar_capitulo(capitulo_json)
        return ai_response
    

    def _as_list_of_dicts(self, raw):
        # Convierte raw en una lista de dicts cuando es posible (útil para secciones con items)
        if isinstance(raw, list) and raw and isinstance(raw[0], dict):
            return raw
        if isinstance(raw, dict):
            # Busca la primera lista de dicts
            for v in raw.values():
                if isinstance(v, list) and v and isinstance(v[0], dict):
                    return v
        return []

    def cargar_seccion(self, seccion: str):
        raw = self.storage.obtener_contenido_seccion(seccion) or {}

        if seccion == "personajes_principales":
            # Espera: {"Seccion": "...", "Personajes": [ {...}, ... ] }
            return {"tipo": "personajes", "items": raw.get("Personajes", [])}

        # StoryController.cargar_seccion (dentro de la clase)
        if seccion == "descripcion_de_escenarios":
            raw = self.storage.obtener_contenido_seccion(seccion) or {}
            lista = raw.get("Escenarios", [])

            def norm_e(e: dict):
                # Recupera variantes normalizadas sin perder información
                localizacion = (
                    e.get("Localización") or e.get("Localizacion") or e.get("Ubicacion") or e.get("ubicacion")
                )
                descripcion = e.get("Descripción") or e.get("Descripcion")
                importancia = (
                    e.get("Importancia en la historia") or e.get("Importancia_en_la_historia") or e.get("Importancia")
                )
                historia_tf = (
                    e.get("Historia y trasfondo") or e.get("Historia_y_trasfondo") or e.get("Historia") or e.get("Trasfondo")
                )

                # Eventos importantes puede venir como lista, string, o clave normalizada
                eventos_val = e.get("Eventos importantes") or e.get("Eventos_importantes") or e.get("Eventos")
                if isinstance(eventos_val, list):
                    eventos = eventos_val
                elif isinstance(eventos_val, str) and eventos_val.strip():
                    eventos = [eventos_val.strip()]
                else:
                    eventos = []

                return {
                    "Nombre": e.get("Nombre", "—"),
                    # ← devolvemos claves "bonitas" con acentos y espacios
                    "Localización": localizacion or "—",
                    "Descripción": descripcion or "—",
                    "Importancia en la historia": importancia or "—",
                    "Historia y trasfondo": historia_tf or "—",
                    "Eventos importantes": eventos,
                }

            items = [norm_e(x) for x in lista]
            return {"tipo": "escenarios", "items": items}


        if seccion == "descripcion_del_mundo":
            # Espera un doc con estos campos de texto:
            # "Geografia", "Sociedad", "Politica", "TecnologiaOMagia", "Economia", "Historia", "Reglas"
            bloques = []
            m = {
                "Geografía / Regiones": "Geografia",
                "Sociedad / Cultura": "Sociedad",
                "Política / Facciones": "Politica",
                "Tecnología / Magia": "TecnologiaOMagia",
                "Economía / Recursos": "Economia",
                "Historia / Mitología": "Historia",
                "Reglas del mundo": "Reglas",
            }
            for titulo, clave in m.items():
                if raw.get(clave):
                    bloques.append({"titulo": titulo, "texto": raw[clave]})
            if not bloques:
                bloques = [{"titulo": "Mundo", "texto": str(raw)}]
            return {"tipo": "mundo", "items": bloques}

        # if seccion == "trama_e_hilo_simbolico":
        #     # Espera: "Premisa" (str), "Hilo_simbólico" (str), "Conflictos" (list|str), "Actos" (list)
        #     bloques = []
        #     if raw.get("Premisa"):         bloques.append({"titulo": "Premisa", "texto": raw["Premisa"]})
        #     if raw.get("Hilo_simbólico"):  bloques.append({"titulo": "Hilo simbólico", "texto": raw["Hilo_simbólico"]})
        #     if raw.get("Conflictos"):
        #         conf = raw["Conflictos"]
        #         texto = "\n".join(f"- {c}" for c in conf) if isinstance(conf, list) else str(conf)
        #         bloques.append({"titulo": "Conflictos", "texto": texto})
        #     if raw.get("Actos"):
        #         actos = raw["Actos"]
        #         if isinstance(actos, list):
        #             texto = "\n".join(
        #                 f"Acto {i+1}: " + (a.get("Descripcion") or a.get("Descripción") or str(a))
        #                 if isinstance(a, dict) else f"Acto {i+1}: {a}"
        #                 for i, a in enumerate(actos)
        #             )
        #         else:
        #             texto = str(actos)
        #         bloques.append({"titulo": "Estructura (actos)", "texto": texto})
        #     if not bloques:
        #         bloques = [{"titulo": "Trama", "texto": str(raw)}]
        #    return {"tipo": "trama", "items": bloques}

        # Fallback
        return {"tipo": "texto", "items": [{"titulo": seccion, "texto": str(raw)}]}


        # # --- ESCENARIOS ---
        # if seccion == "descripcion_de_escenarios":
        #     def norm_e(e):
        #         if not isinstance(e, dict): return None
        #         return {
        #             "Nombre": e.get("Nombre") or e.get("nombre") or e.get("title") or "—",
        #             "Tipo": e.get("Tipo") or e.get("tipo") or e.get("category") or "—",
        #             "Ubicacion": e.get("Ubicacion") or e.get("ubicacion") or e.get("ubicación") or e.get("location") or "—",
        #             "Descripcion": e.get("Descripcion") or e.get("descripcion") or e.get("description") or "—",
        #             "Elementos": e.get("Elementos") or e.get("elementos") or e.get("props") or [],
        #         }
        #     candidates = []
        #     if isinstance(raw, dict):
        #         for k in ["escenarios", "Escenarios", "lugares", "Locations"]:
        #             if k in raw and isinstance(raw[k], list):
        #                 candidates = raw[k]
        #                 break
        #     if not candidates:
        #         candidates = self._as_list_of_dicts(raw)

        #     items = [x for x in (norm_e(e) for e in candidates) if x]
        #     return {"tipo": "escenarios", "items": items}

        # # --- MUNDO ---
        # if seccion == "descripcion_del_mundo":
        #     # Aplanamos en bloques temáticos para facilitar la UI
        #     bloques = []
        #     if isinstance(raw, dict):
        #         def add(titulo, *keys):
        #             for k in keys:
        #                 if k in raw and raw[k]:
        #                     bloques.append({"titulo": titulo, "texto": raw[k] if isinstance(raw[k], str) else str(raw[k])})
        #                     return
        #         add("Geografía / Regiones", "geografia", "Geografia", "regiones", "Regiones", "Geography", "Regions")
        #         add("Sociedad / Cultura", "sociedad", "Sociedad", "cultura", "Cultura", "Society", "Culture")
        #         add("Política / Facciones", "politica", "Política", "facciones", "Facciones", "Politics", "Factions")
        #         add("Tecnología / Magia", "tecnologia", "Tecnologia", "magia", "Magia", "Technology", "Magic")
        #         add("Economía / Recursos", "economia", "Economia", "recursos", "Recursos", "Economy", "Resources")
        #         add("Historia / Mitología", "historia", "Historia", "mitologia", "Mitologia", "Myth", "History")
        #         add("Reglas del mundo", "reglas", "Reglas", "leyes", "Leyes", "WorldRules")

        #     if not bloques:
        #         # Fallback: convierte raw a un único bloque
        #         texto = raw if isinstance(raw, str) else str(raw)
        #         bloques = [{"titulo": "Mundo", "texto": texto}]

        #     return {"tipo": "mundo", "items": bloques}

        # # --- TRAMA ---
        # if seccion == "trama_e_hilo_simbolico":
        #     bloques = []
        #     if isinstance(raw, dict):
        #         def text_of(*keys):
        #             for k in keys:
        #                 if k in raw and raw[k]:
        #                     return raw[k] if isinstance(raw[k], str) else str(raw[k])
        #             return None

        #         premisa = text_of("premisa", "Premisa")
        #         hilo = text_of("hilo_simbolico", "hilo_simbólico", "Hilo_simbolico", "Hilo_simbólico", "Hilo", "SymbolicThread")
        #         conflictos = raw.get("conflictos") or raw.get("Conflictos")
        #         actos = raw.get("actos") or raw.get("Actos") or raw.get("estructura") or raw.get("Estructura")

        #         if premisa:    bloques.append({"titulo": "Premisa", "texto": premisa})
        #         if hilo:       bloques.append({"titulo": "Hilo simbólico", "texto": hilo})
        #         if conflictos:
        #             if isinstance(conflictos, list):
        #                 texto = "\n".join(f"- {c}" for c in conflictos)
        #             else:
        #                 texto = str(conflictos)
        #             bloques.append({"titulo": "Conflictos", "texto": texto})
        #         if actos:
        #             if isinstance(actos, list):
        #                 texto = "\n".join(
        #                     f"Acto {i+1}: " + (a.get('descripcion') or a.get('Descripción') or a.get('desc') or str(a))
        #                     if isinstance(a, dict) else f"Acto {i+1}: {a}"
        #                     for i, a in enumerate(actos)
        #                 )
        #             else:
        #                 texto = str(actos)
        #             bloques.append({"titulo": "Estructura (actos)", "texto": texto})

        #     if not bloques:
        #         texto = raw if isinstance(raw, str) else str(raw)
        #         bloques = [{"titulo": "Trama", "texto": texto}]

        #     return {"tipo": "trama", "items": bloques}

        # # --- Fallback genérico ---
        # return {"tipo": "texto", "items": [{"titulo": seccion, "texto": raw if isinstance(raw, str) else str(raw)}]}

    # (bug) En accion_reescribir estabas usando self.seccion; usa el parámetro:
    def accion_reescribir(self, user_input, ultimo_prompt, seccion):
        print(f"Sección actual: {seccion}")
        nueva_seccion = seccion
        print(f"Estado de secciones: {self.estado_secciones}")
        print(f"Nueva seccion: {nueva_seccion}")
        nueva_seccion = self.storage.parse_seccion(nueva_seccion)
        if seccion == "escritura":
            ...
        else:
            self.contexto = self.storage.buscar_dependencias_bd(seccion)
            print("Contexto: ", self.contexto)
            resumen_seccion = self.storage.obtener_resumen(seccion)
            mensaje = (
                f"\n\nCONTENIDO DEL MENSAJE\n\n{self.contexto}\n{user_input}\n"
                f"La seccion antigua es:{resumen_seccion}\nPrompt:{ultimo_prompt}"
                f"Cambia la seccion {seccion}\n"
            )
            print(mensaje)
            ai_response = get_ai_response([{"role": "user", "content": mensaje}])
        return ai_response
    

    def actualizar_item(self, seccion: str, idx: int, nuevo_item: dict) -> bool:
        return self.storage.update_item_in_list(seccion, idx, nuevo_item)




