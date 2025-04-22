from pymongo import MongoClient

class ConexionMongoDB:
    def __init__(self, nombre_db):
        """Inicializa la conexión con MongoDB"""
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client[nombre_db]  # Nombre de la base de datos

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


    def hay_documentos(self):
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
    def insertar(self, documento, seccion):
        try:
            self.collection.insert_one(documento)
            print(f"✅ Documento insertado en la seccion: {seccion}")
        except Exception as e:
            print(f"❌ Error al insertar documento: {e}")


    def actualizar(self, campo, valor_actual, valor_nuevo, seccion):
        try:
            filtro = {campo: valor_actual}
            nuevo = {"$set": {campo: valor_nuevo}}
            self.collection.update_one(filtro, nuevo)
            print(f"✅ {campo} actualizado correctamente en '{seccion}'.")
        except Exception as e:
            print(f"❌ No se pudo actualizar: {e}")

        

    def eliminar(self, campo, valor):
        try:
            filtro = {campo: valor}
            if valor:
                coleccion_ref = self.db[valor]
            else:
                coleccion_ref = self.collection
            self.collection.delete_one(filtro)
            print(f"✅ Documento eliminado correctamente en '{coleccion_ref.name}'.")
        except Exception as e:
            print(f"❌ No se pudo eliminar: {e}")

    def buscar(self, campo, valor):
        """Busca documentos según un filtro, en la colección actual o en la que se indique."""
        try:
            filtro = {campo: valor}
            if valor:
                collection_ref = self.db[valor]
            else:
                collection_ref = self.collection

            resultados = collection_ref.find_one(filtro, {"_id":0})
            #print(f"🔍 Se encontraron {len(resultados)} documentos en '{collection_ref.name}'.")
            return resultados
        except Exception as e:
            print(f"❌ Error al buscar documentos: {e}")
            return []
        

    def devolver_documentos(self, seccion):
        doc = self.collection.find_one({"Seccion": seccion}, {"_id": 0, "texto": 1})
        if doc and "texto" in doc:
            return doc["texto"]
        else:
            print(f"❌ No se encontró texto para la sección: {seccion}")
            return ""

    def nuevo_campo(self, campo, valor, coleccion):
        """Añade o actualiza un campo a todos los documentos que coincidan con el filtro."""
        try:
            filtro = {campo: valor}
            collection_ref = self.db[coleccion]
            collection_ref.update_many(filtro, {"$set": {"UPDATE": "True"}})
        except Exception as e:
            print(f"❌ Error al añadir campo: {e}")

    def nuevo_escenario_personaje(self, campo, valor, seccion, nuevo):
        try:
            filtro = {campo: valor}
            self.collection.update_one(filtro, {"$push": {seccion: nuevo}})
            print(f"✅ '{seccion} actualizado correctamente.")
        except Exception as e:
            print(f"❌ No se pudo actualizar: {e}")

    def eliminar_base_datos(self, nombre_bd):
        try:
            self.client.drop_database(nombre_bd)
            print(f"✅ Base de datos '{nombre_bd}' eliminada.")
        except Exception as e:
            print(f"❌ Error al eliminar base de datos: {e}")


    def cerrar_conexion(self):
        self.client.close()