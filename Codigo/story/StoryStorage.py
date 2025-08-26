from BD.ConnectionMongo import ConexionMongoDB
import unicodedata
import difflib
import os
from fpdf import FPDF

class StoryStorage:
    def __init__(self, nombre_historia: str):
        self.mongo = ConexionMongoDB(nombre_historia)

        self.dependencias = {
            "trama_e_hilo_simbolico": [],
            "descripcion_del_mundo": ["trama_e_hilo_simbolico"],
            "personajes_principales": ["trama_e_hilo_simbolico"],
            "descripcion_de_escenarios": ["trama_e_hilo_simbolico", "descripcion_del_mundo"],
            "estructura_de_capitulos": ["trama_e_hilo_simbolico", "personajes_principales", "descripcion_de_escenarios"],
            "escritura": ["trama_e_hilo_simbolico", "descripcion_del_mundo"],
        }

    def parse_seccion(self, seccion: str)->str:
        if seccion == "trama_e_hilo_simbólico":
            return "trama_e_hilo_simbolico"
        elif seccion == "descripción_del_mundo":
            return "descripcion_del_mundo"
        elif seccion == "descripción_de_escenarios":
            return "descripcion_de_escenarios"
        elif seccion == "estructura_de_capítulos":
            return "estructura_de_capitulos"
        else:
            return seccion

    def nombre_sinopsis_capitulo(self, capitulo: str):
        self.mongo.seleccionar_coleccion("estructura_de_capitulos")
        estructura_capitulo = self.mongo.buscar("Seccion", "estructura_de_capitulos")
        nombre = estructura_capitulo["Capitulos"][capitulo - 1]["Nombre"]
        sinopsis = estructura_capitulo["Capitulos"][capitulo - 1]["Sinopsis"]
        return nombre, sinopsis

    def personajes_capitulo(self, capitulo: int):
        self.mongo.seleccionar_coleccion("estructura_de_capitulos")
        estructura_capitulo = self.mongo.buscar("Seccion", "estructura_de_capitulos")
        personajes = estructura_capitulo["Capitulos"][capitulo - 1]["Personajes"]
        print("\nPERSOANJES PARTICIPANTES: ", personajes)
        return personajes
    


    def normalizar(self, texto):
        """Convierte texto a minúsculas y elimina acentos."""
        texto = texto.lower()
        texto = unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('utf-8')
        return texto


    def buscar_personajes(self, personajes: list):
        self.mongo.seleccionar_coleccion("personajes_principales")
        doc = self.mongo.buscar("Seccion", "personajes_principales")

        if doc is None:
            print("⚠️ No se encontró la colección de personajes.")
            return []

        personajes_disponibles = doc.get("Personajes", [])
        indexado = {p["Nombre"]: p for p in personajes_disponibles}
        nombres_disponibles = list(indexado.keys())

        encontrados = []

        for nombre in personajes:
            # 1. Coincidencia exacta
            if nombre in indexado:
                encontrados.append(indexado[nombre])
                continue

            # 2. Coincidencia parcial
            parciales = [p for n, p in indexado.items() if nombre in n]
            if parciales:
                print(f"🔍 Coincidencia parcial para '{nombre}' → '{[n for n in indexado if nombre in n][0]}'")
                encontrados.append(parciales[0])
                continue

            # 3. Sugerencia aproximada
            sugerencia = difflib.get_close_matches(nombre, nombres_disponibles, n=1)
            if sugerencia:
                print(f"❌ '{nombre}' no encontrado. ¿Querías decir: '{sugerencia[0]}'?")
                encontrados.append(indexado[sugerencia[0]])
            else:
                print(f"❌ Personaje '{nombre}' no encontrado y no hay coincidencias cercanas.")

        return encontrados


        
    def escenarios_capitulo(self, capitulo: int):
        self.mongo.seleccionar_coleccion("estructura_de_capitulos")
        estructura_capitulo = self.mongo.buscar("Seccion", "estructura_de_capitulos")
        escenarios = estructura_capitulo["Capitulos"][capitulo - 1]["Escenarios"]
        print("\n✅ ESCENARIOS DEL CAPÍTULO:", escenarios)
        return escenarios


    def buscar_escenarios(self, escenarios: list):
        self.mongo.seleccionar_coleccion("descripcion_de_escenarios")
        doc = self.mongo.buscar("Seccion", "descripcion_de_escenarios")

        if doc is None:
            print("⚠️ No se encontró la colección de escenarios.")
            return []

        escenarios_disponibles = doc.get("Escenarios", [])
        indexado = {e["Nombre"]: e for e in escenarios_disponibles}
        nombres_disponibles = list(indexado.keys())

        encontrados = []

        for nombre in escenarios:
            # 1. Coincidencia exacta
            if nombre in indexado:
                encontrados.append(indexado[nombre])
                continue

            # 2. Coincidencia parcial: nombre incluido dentro de algún nombre disponible
            parciales = [e for n, e in indexado.items() if nombre in n]
            if parciales:
                print(f"🔍 Coincidencia parcial encontrada para '{nombre}' → '{[n for n in indexado if nombre in n][0]}'")
                encontrados.append(parciales[0])
                continue

            # 3. Sugerencia aproximada
            sugerencia = difflib.get_close_matches(nombre, nombres_disponibles, n=1)
            if sugerencia:
                print(f"❌ '{nombre}' no encontrado. ¿Querías decir: '{sugerencia[0]}'?")
                encontrados.append(indexado[sugerencia[0]])
            else:
                print(f"❌ Escenario '{nombre}' no encontrado y no hay coincidencias cercanas.")

        return encontrados


    def buscar_resumen_capitulos(self):
        """
        Devuelve un texto con los resúmenes (o snippet del contenido) de capitulo_1..capitulo_4,
        usando solo los métodos públicos de ConexionMongoDB (sin acceder a .collection.find()).
        """
        self.mongo.seleccionar_coleccion("escritura")

        capitulos_txt = []
        for i in range(1, 5):  # TIENE QUE TENER 4 CAPITULOS
            seccion = f"capitulo_{i}"
            doc = self.mongo.buscar("Seccion", seccion)  # usa el wrapper, no .find directo

            if not doc:
                # Si falta el capítulo, lo saltamos (o añade un marcador si prefieres)
                continue

            titulo = doc.get("Titulo") or seccion
            resumen = doc.get("Resumen")

            if not resumen:
                contenido = (doc.get("Contenido") or "").strip()
                # si no hay Resumen, usamos un snippet del Contenido
                if contenido:
                    resumen = contenido[:500] + ("…" if len(contenido) > 500 else "")
                else:
                    resumen = "(Sin resumen ni contenido disponible)"

            capitulos_txt.append(f"[{seccion}] {titulo}\n{resumen}")

        return "\n\n".join(capitulos_txt)


        
    def buscar_capitulos(self, capitulo):
        contexto = ""
        self.mongo.seleccionar_coleccion("escritura")
        for i in range(1, capitulo):
            num_capitulo = f"capitulo_{i}"
            texto = self.mongo.buscar_capitulos_fast(num_capitulo)
            if texto:
                contexto += f"\n[Capítu(lo {i}]\n{texto}\n"
        return contexto.strip()
    
    def capitulo_fast(self, capitulo):
        self.mongo.seleccionar_coleccion("capitulos")
        num_capitulo = f"capitulo_{capitulo}" 
        contenido = self.mongo.buscar_capitulos_fast(num_capitulo)
        return contenido

    def contexto_capitulo_rapido(self, capitulo: int):
        contexto = ""
        self.mongo.seleccionar_coleccion("capitulos")
        for i in range(1, capitulo):
            num_capitulo = f"capitulo_{i}"
            texto = self.mongo.buscar_capitulos_fast(num_capitulo)
            if texto:
                contexto += f"\n[Capítulo {i}]\n{texto}\n"
        return contexto.strip()

    def crear_contexto_capitulo(self, capitulo: int):
        dependencias = self.buscar_dependencias_bd("escritura") #Añado trama y descripcion
        nombre, sinopsis = self.nombre_sinopsis_capitulo(capitulo)
        lista_personajes = self.personajes_capitulo(capitulo)
        lista_escenarios = self.escenarios_capitulo(capitulo)
        personajes = self.buscar_personajes(lista_personajes)
        escenarios = self.buscar_escenarios(lista_escenarios)
        capitulos = self.buscar_capitulos(capitulo)
        #capitulos = self.buscar_resumen_capitulos()
        contexto = f"{dependencias} \n\n Capitulo: {capitulo} \n Nombre: {nombre} \n {sinopsis}\n Personajes: {personajes} \n Escenarios: {escenarios} \n Resumen capitulos: {capitulos}"
        return contexto.replace("\n", " ")
    
    def obtener_contenido_seccion(self, seccion: str):
        self.mongo.seleccionar_coleccion(seccion)
        return self.mongo.buscar("Seccion", seccion)
    
    def obtener_resumen(self, seccion):
        self.mongo.seleccionar_coleccion("resumen")
        if seccion == "trama_y_hilo_simbolico":
            seccion == "trama_e_hilo_simbolico"
        return self.mongo.buscar("Seccion", seccion)

    def eliminar_seccion_json(self, json_formateado):
        json_formateado.pop("Seccion", None)
        return json_formateado

    def listas_bd(self, seccion):
        if seccion == "descripcion_de_escenarios":
            return "Escenarios"
        elif seccion == "personajes_principales":
            return "Personajes"
        return None

    def cargar_info_historia(self, usuario: str):
        self.mongo.seleccionar_coleccion("info")
        return self.mongo.buscar("Usuario", usuario)
            
    # Suponiendo que estado_secciones es un diccionario ordenado (como en Python 3.7+)
    def primera_seccion_no_completada(self, estado_secciones):
        for seccion, valor in estado_secciones.items():
            if not valor:
                return seccion
        return None  # Si todas están completadas
    
    def ultima_seccion(self, estado_secciones):
        """
        Devuelve la clave anterior al primer False en el diccionario.
        Si el primer elemento es False, devuelve None.
        Si todos son True, devuelve la última clave.
        """
        anterior = None
        for seccion, valor in estado_secciones.items():
            if not valor:
                return anterior
            anterior = seccion
        return anterior  # Si todos son True, devuelve el último


    def guardar_info_historia(self, usuario: str, modo: str, estado_secciones: dict):
        self.mongo.seleccionar_coleccion("info")
        if not self.mongo.hay_documentos():
            info = {
                "Usuario": usuario,
                "Modo": modo
            }
            self.mongo.insertar(info)

    def guardar_usuario(self, usuario: str):
        self.mongo.seleccionar_coleccion("info")
        if not self.mongo.hay_documentos():
            self.mongo.insertar({"Usuario": usuario})

    def guardar_resumen(self, resumen, seccion):
        self.mongo.seleccionar_coleccion("resumen")
        if seccion != "escritura":
            print(f"\n----------Seccion: {seccion}----------\n")
            # Si hay un documento con la sección indicada, eliminarlo antes de insertar el nuevo
            if self.mongo.buscar("Seccion", seccion):
                self.mongo.eliminar("Seccion", seccion)
        self.mongo.insertar(resumen)

    def guardar_historia(self):
        self.mongo.seleccionar_coleccion("escritura")
        historia = ""
        for i in range(1, 5):  # Aseguramos que haya 4 capítulos
            num_capitulo = f"capitulo_{i}"
            capitulo = self.mongo.buscar_capitulo_guardar(num_capitulo)
            historia += f"Capitulo {i}\nTitulo: {capitulo['Titulo']}\nContenido: {capitulo['Contenido']}\n\n\n"
        return historia.strip()


    def historia_a_pdf(self, nombre_archivo):
        texto = self.guardar_historia()
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, texto)
        pdf.output(nombre_archivo)

    def eliminar_historia(self, usuario, nombre_historia):
        self.mongo.seleccionar_coleccion()

    def buscar_dependencias_bd(self, seccion_actual: str) -> str:
        secciones_necesarias = self.dependencias.get(seccion_actual, [])
        print("Dependencias necesarias:", secciones_necesarias)
        contexto = ""
        self.mongo.seleccionar_coleccion("contexto")
        if self.mongo.hay_documentos():
            for seccion in secciones_necesarias:
                texto = self.mongo.buscar_contexto_seccion(seccion)
                contexto += texto
        return contexto.replace("\n", " ")

    def guardar_estado_secciones(self, estado_secciones: dict):

        self.mongo.seleccionar_coleccion("estados_secciones")
        if self.mongo.hay_documentos():
            self.mongo.eliminar_todos_documentos()
        estado = {
            "Estado_secciones": estado_secciones
        }
        self.mongo.insertar(estado)

    def guardar_modo(self, modo: dict):
        self.mongo.seleccionar_coleccion("info")
        if not self.mongo.hay_documentos():
            self.mongo.insertar(modo)

    def seleccionar_modo(self):
        self.mongo.seleccionar_coleccion("info")
        return self.mongo.buscar_modo()

    def guardar_texto(self, texto: dict):
        self.mongo.seleccionar_coleccion("contexto")
        # Elimina el documento previo con la misma sección, si existe
        if "Seccion" in texto:
            self.mongo.eliminar("Seccion", texto["Seccion"])
        self.mongo.insertar(texto)

    def guardar_capitulo(self, capitulo):
        self.mongo.seleccionar_coleccion("capitulos")
        num_capitulo = f"capitulo_{capitulo}"
        if self.mongo.buscar("Seccion", num_capitulo):
            self.mongo.eliminar("Seccion", num_capitulo)
        self.mongo.insertar(capitulo)



    def guardar_doc(self, json_mongo, seccion):
        if seccion == "trama_e_hilo_simbolico":
            print("Seccion: ", seccion)
            print("\n\n////////////////////\n\n")
            self.mongo.seleccionar_coleccion("trama_e_hilo_simbolico")
            if self.mongo.hay_documentos():
                self.mongo.eliminar("Seccion", "trama_e_hilo_simbolico")
            self.mongo.insertar(json_mongo)
        elif seccion is None:
            self.mongo.seleccionar_coleccion("otros")
            self.mongo.insertar(json_mongo)
        elif seccion in ["descripcion_de_escenarios", "personajes_principales"]:
            self.mongo.seleccionar_coleccion(seccion)
            if self.mongo.hay_documentos():
                formateado = self.eliminar_seccion_json(json_mongo)
                #self.mongo.nuevo_escenario_personaje("Seccion", seccion, self.listas_bd(seccion), formateado)
            else:
                self.mongo.insertar(json_mongo)
        elif seccion == "resumen" or "escritura":
            self.mongo.seleccionar_coleccion(seccion)
            self.mongo.insertar(json_mongo)
        else:
            self.mongo.seleccionar_coleccion(seccion)

            if self.mongo.hay_documentos():
                self.mongo.eliminar("Seccion", seccion)
            self.mongo.insertar(json_mongo)

    def guardar_respuesta_ai(self, capitulo: str, archivo="historia.txt", carpeta="Capitulos"):
        import os

        # Crear la carpeta si no existe
        os.makedirs(carpeta, exist_ok=True)

        # Ruta completa del archivo
        ruta = os.path.join(carpeta, archivo)

        try:
            # Añadir el contenido al final del archivo
            with open(ruta, "a", encoding="utf-8") as f:
                f.write(f"\n\n{capitulo.strip()}\n")  # Añade separación entre respuestas
            print(f"✅ Respuesta de la IA guardada en '{ruta}'")
        except Exception as e:
            print(f"❌ Error al guardar respuesta de la IA: {e}")


    def guardar_info_usuarios(self, usuario, nombre_historia, modo, estado_secciones):
        self.mongo.info_usuario(usuario, nombre_historia, modo, estado_secciones)

    def actualizar_estado_secciones(self, usuario, nombre_historia, nuevo_estado):
        self.mongo.actualizar_estado_secciones(usuario, nombre_historia, nuevo_estado)

    def actualizar_info(self, usuario, estado_secciones):
        self.mongo.seleccionar_coleccion("info")
        self.mongo.actualizar_info(usuario, estado_secciones)

    # def historias_usuario(self, usuario):
    #     historia =  self.mongo.buscar_historias_usuario(usuario)
    #     print("Historias del usuario:", historia)
    #     return historia

    def update_item_in_list(self, seccion: str, idx: int, nuevo_item: dict) -> bool:
        """
        Actualiza atómicamente el elemento 'idx' de la lista de la sección dada.
        - personajes_principales -> Personajes.<idx>
        - descripcion_de_escenarios -> Escenarios.<idx>
        """
        self.mongo.seleccionar_coleccion(seccion)
        if seccion == "personajes_principales":
            campo = "Personajes"
        elif seccion == "descripcion_de_escenarios":
            campo = "Escenarios"
        else:
            return False

        # Necesitamos un update_one en la conexión. Si tu ConexionMongoDB no lo tiene,
        # crea un wrapper que llame a coleccion.update_one(...)
        res = self.mongo.update_one(
            {"Seccion": seccion},
            {"$set": {f"{campo}.{idx}": nuevo_item}},
            upsert=False,
        )
        # PyMongo devuelve result.modified_count
        return getattr(res, "modified_count", 0) == 1


    # def update_mundo_field(self, titulo_bloque: str, nuevo_texto: str) -> bool:
    #     """
    #     Mapea el título mostrado en UI al campo real de 'descripcion_del_mundo'
    #     y hace un $set sobre ese campo.
    #     """
    #     titulo_a_key = {
    #         "Geografía / Regiones": "Geografia",
    #         "Sociedad / Cultura": "Sociedad",
    #         "Política / Facciones": "Politica",
    #         "Tecnología / Magia": "TecnologiaOMagia",
    #         "Economía / Recursos": "Economia",
    #         "Historia / Mitología": "Historia",
    #         "Reglas del mundo": "Reglas",
    #     }
    #     key = titulo_a_key.get(titulo_bloque)
    #     if not key:
    #         return False

    #     self.mongo.seleccionar_coleccion("descripcion_del_mundo")
    #     res = self.mongo.update_one(
    #         {"Seccion": "descripcion_del_mundo"},
    #         {"$set": {key: nuevo_texto}},
    #         upsert=False,
    #     )
    #     return getattr(res, "modified_count", 0) == 1



