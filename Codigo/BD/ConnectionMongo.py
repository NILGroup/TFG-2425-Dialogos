from pymongo import MongoClient

class ConexionMongoDB:
    def __init__(self, nombre_db):
        """Inicializa la conexión con MongoDB"""
        self.client = MongoClient("mongodb://localhost:27017")
        self.db = self.client[nombre_db]  # Nombre de la base de datos

    def todas_colecciones_usuario(self, usuario):
        """Devuelve la lista de colecciones del usuario"""
        lista_colecciones = []
        for nombre_coleccion in self.db.list_collection_names():
            coleccion = self.db[nombre_coleccion]
            if coleccion.find_one({"Usuario": usuario}):
                lista_colecciones.append(nombre_coleccion)
        return lista_colecciones


    def info_usuario(self, usuario, nombre_historia, modo, estado_secciones):
        bd_info = self.client["info_usuarios"]
        coleccion = bd_info["historias"]
        existe = coleccion.find_one({"Usuario": usuario, "Nombre_historia": nombre_historia})
        # if existe:
        #     raise Exception("La historia ya existe para este usuario.")
        coleccion.insert_one({
            "Usuario": usuario,
            "Nombre_historia": nombre_historia,
            "Modo": modo,
            "Estado_secciones": estado_secciones
        })

    def get_story(self, usuario, nombre_historia):
        # Busca la historia del usuario por nombre
        bd_info = self.client[nombre_historia]
        coleccion = bd_info["info"]
        doc = coleccion.find_one({"Usuario": usuario})
        return doc


    def buscar_historias_usuario(self, usuario):
        bd_info = self.client["info_usuarios"]
        coleccion = bd_info["historias"]
        historias = list(coleccion.find(
            {"Usuario": usuario},
            {"_id": 0, "Nombre_historia": 1, "Estado_secciones": 1, "Modo": 1}
        ))
        return historias



    def seleccionar_coleccion(self, nombre_coleccion):
        """Selecciona una colección en la base de datos"""
        try:
            if nombre_coleccion not in self.db.list_collection_names():
                self.db[nombre_coleccion].insert_one({"temp": "delete"})  # Crea la colección si no existe
                self.db[nombre_coleccion].delete_one({"temp": "delete"})  # Elimina el dato temporal
            self.collection = self.db[nombre_coleccion]
            print(f"✅ Colección seleccionada: {nombre_coleccion}")
        except Exception as e:
            print(f"❌ Error al seleccionar la coleccion: {e}")


    def actualizar_info(self, usuario, estado_secciones):
        self.collection.update_one(
            {"Usuario": usuario},
            {"$set": {"Estado_secciones": estado_secciones}}
        )


    def actualizar_estado_secciones(self, usuario, nombre_historia, nuevo_estado):
        bd_info = self.client["info_usuarios"]
        coleccion = bd_info["historias"]
        resultado = coleccion.update_one(
            {"Usuario": usuario, "Nombre_historia": nombre_historia},
            {"$set": {"Estado_secciones": nuevo_estado}}
        )
        if resultado.matched_count == 0:
            raise Exception("No se encontró la historia para actualizar.")
        

    def hay_documentos(self):
        """Verifica si hay documentos en la colección actual"""
        try:
            doc = self.collection.find_one()
            if doc:
                print(f"✅ La colección contiene al menos un documento.")
                return True
            else:
                print(f"⚠️ La colección está vacía.")
                return False
        except Exception as e:
            print(f"❌ Error al buscar documentos: {e}")
            return False
        
    def insertar(self, documento):
        """Inserta un documento en la colección actual"""
        try:
            self.collection.insert_one(documento)
            print(f"✅ Documento insertado en la seccion")
        except Exception as e:
            print(f"❌ Error al insertar documento: {e}")


    def actualizar(self, campo, valor_actual, valor_nuevo): #No lo uso de momento
        """Actualiza un campo en la colección actual"""
        try:
            filtro = {campo: valor_actual}
            nuevo = {"$set": {campo: valor_nuevo}}
            self.collection.update_one(filtro, nuevo)
            print(f"✅ {campo} actualizado correctamente.")
        except Exception as e:
            print(f"❌ No se pudo actualizar: {e}")

    def update_one(self, filtro: dict, update: dict, upsert: bool = False):
        return self.collection.update_one(filtro, update, upsert=upsert)

    def replace_one(self, filtro: dict, new_doc: dict, upsert: bool = False):
        return self.collection.replace_one(filtro, new_doc, upsert=upsert)


    def eliminar(self, campo, seccion):
        """Elimina un documento de la seccion actual"""
        try:
            filtro = {campo: seccion}
            self.collection.delete_one(filtro)
            print(f"✅ Documento eliminado correctamente en '{seccion}'.")
        except Exception as e:
            print(f"❌ No se pudo eliminar: {e}")


    def buscar(self, campo, valor):
        """Busca documentos según un filtro en la coleccion actual"""
        try:
            filtro = {campo: valor}
            resultados = self.collection.find_one(filtro, {"_id":0})
            return resultados
        except Exception as e:
            print(f"❌ Error al buscar documentos: {e}")
            return []
        
    def buscar_modo(self): #No la uso de momento
        """Busca en la historia seleccionada que modo se ha utilizado (rapido o detallado)"""
        doc = self.collection.find_one({}, {"_id": 0})  # buscamos el último guardado, omitimos el _id
        if doc and "Modo" in doc:
            return doc["Modo"]
        return None  # si no hay modo guardado

    def buscar_contexto_seccion_rapido(self, seccion):
        doc = self.buscar("Seccion", seccion)
        if doc and "Contenido" in doc:
            return doc["Contenido"]
        else:
            print(f"❌ No se encontró texto para la sección: {seccion}")
        return ""

    def buscar_contexto_seccion(self, seccion):
        """Devulve el contexto de la seccion seleccionada"""
        doc = self.collection.find_one({"Seccion": seccion}, {"_id": 0, "texto": 1})
        if doc and "texto" in doc:
            return doc["texto"]
        else:
            print(f"❌ No se encontró texto para la sección: {seccion}")
            return ""

    def nuevo_campo(self, campo, valor, coleccion):#No la uso de momento
        """Añade o actualiza un campo a todos los documentos que coincidan con el filtro."""
        try:
            filtro = {campo: valor}
            collection_ref = self.db[coleccion]
            collection_ref.update_many(filtro, {"$set": {"UPDATE": "True"}})
        except Exception as e:
            print(f"❌ Error al añadir campo: {e}")

    def nuevo_escenario_personaje(self, campo, valor, seccion, nuevo): #No la uso de momento
        """Añade un nuevo escenario o personaje a la sección seleccionada"""
        try:
            filtro = {campo: valor}
            self.collection.update_one(filtro, {"$push": {seccion: nuevo}})
            print(f"✅ '{seccion} actualizado correctamente.")
        except Exception as e:
            print(f"❌ No se pudo actualizar: {e}")

    def buscar_resumenes(self, seccion):
        """Devuelve todos los resumenes hasta el momento"""
        try:
            filtro = {"Seccion": seccion}
            resultados = list(self.collection.find(filtro, {"_id": 0}))
            return resultados
        except Exception as e:
            print(f"❌ Error al buscar varios documentos: {e}")
            return []
        
    def eliminar_todos_documentos(self):
        """Elimina todos los documentos de la colección actual"""
        try:
            resultado = self.collection.delete_many({})
            print(f"✅ Se eliminaron {resultado.deleted_count} documentos de la colección.")
        except Exception as e:
            print(f"❌ Error al eliminar documentos: {e}")
        

    def cerrar_conexion(self):
        self.client.close()