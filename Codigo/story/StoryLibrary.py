from BD.ConnectionMongo import ConexionMongoDB

class StoryLibrary:
    def __init__(self):
        self.mongo = ConexionMongoDB("info_usuarios")  # Solo una BD general para todas las historias

    def obtener_historias(self, usuario):
        historias = []
        historias_usuario = self.mongo.buscar_historias_usuario(usuario)
        for h in historias_usuario:
            estado = h.get("Estado_secciones", {})
            total = len(estado)-1
            completadas = sum(1 for x in estado.values() if x)
            historias.append({
                "nombre": h["Nombre_historia"],
                "completadas": completadas-1,
                "total": total,
                "modo": h["Modo"]
            })
        return historias
    
    def create_story(self, usuario, nombre_historia, modo, estado_secciones):
        self.mongo.info_usuario(usuario, nombre_historia, modo, estado_secciones)

    def load_story(self, usuario, nombre_historia):
        self.mongo.seleccionar_coleccion(nombre_historia)
