import flet as ft
from flet_route import Params, Basket
import threading
from controller.StoryController import StoryController
import re
import time
import pyperclip
from UI.Theme import HISTORIAS_THEME as th


class NuevaHistoria:
    def __init__(self):
        self.ultimo_prompt = ""
        self.ultima_respuesta = ""
        self.promto_usuario = ""
        self.seccion_actual = "trama_e_hilo_simbolico"
        self.seccion_pendiente = None
        self.mock_idx = 0
        self.mock_items = []  # la llenamos al entrar en ver_seccion()
        self.tipo_actual = None
        self.items_actuales = []
        self.capitulo_actual = 1

    def view(self, page: ft.Page, params:Params, basket:Basket):
        controller = StoryController(page, True)
        usuario = page.session.get("username")

        page.theme_mode = ft.ThemeMode.LIGHT         # o ft.ThemeMode.DARK                 
        SIZE_BODY = 18       # tamaño del texto de detalle
        SIZE_HEADING = 20    # títulos de sección (si quieres subirlos)


        SECCION_TITULOS = {
            "trama_e_hilo_simbolico": "Trama e hilo simbólico",
            "descripcion_del_mundo": "Descripción del mundo",
            "personajes_principales": "Personajes principales",
            "descripcion_de_escenarios": "Descripción de escenarios",
            "estructura_de_capitulos": "Estructura de capítulos",
            "escritura": "Escritura de capítulos",
        }
        def titulo_seccion_text(key: str) -> str:
            return SECCION_TITULOS.get(key, key.replace("_", " ").title())


        def button_back(e):
            page.go("/home")
            page.update()

        #Boton para ir hacia atras
        btn_back = ft.IconButton(
            icon=ft.Icons.CHEVRON_LEFT,
            on_click=button_back
        )

        

        # confirm_tittle = ft.AlertDialog(
        #     modal=True,
        #     title=ft.Text("Confirmar nombre"),
        #     content=ft.Text("¿Quieres guardar la historia con este nombre?"),
        #     actions=[
        #         ft.TextButton("Aceptar", on_click=button_accept),
        #         ft.TextButton("Cancelar", on_click=lambda e: page.close(confirm_tittle)),
        #     ],
        #     actions_alignment=ft.MainAxisAlignment.END
        # )

        nombre_historia = page.session.get("nombre_bd")
        print(f"Nombre de la historia: {nombre_historia}")

        titulo = ft.Container(
            content=ft.Text(
                value=nombre_historia,
                size=26,
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.CENTER,
            ),
            # padding=ft.padding.symmetric(horizontal=20, vertical=10),
            # alignment=ft.alignment.center
        )



        #Campo para que el usuario ponga nombre para guardar la historia
        # titulo = ft.TextField(
        #     text="Nueva historia (Personalizar)",
        #     value="",
        #     border=ft.InputBorder.OUTLINE,
        #     filled=True,
        #     border_radius=10,
        #     text_align=ft.TextAlign.CENTER,
        #     text_style=ft.TextStyle(size=20, weight=ft.FontWeight.BOLD),
        #     content_padding=ft.Padding(10, 10, 10, 10),
        #     suffix_icon=ft.IconButton(
        #         icon=ft.Icons.EDIT,
        #         tooltip="Editar título",
        #         on_click=lambda e: page.open(confirm_tittle),
        #     ),
        #     expand=True
        # )

        dlg = ft.AlertDialog(
            title=ft.Text("Se ha guardado la historia"),
            on_dismiss=lambda e: page.add(ft.Text("Non-modal dialog dismissed")),
        )

    

        confirm_save = ft.AlertDialog(
            modal=True,
            title=ft.Text("Guardar historia"),
            content=ft.Text("¿Estás seguro que quieres guardar?"),
            actions=[
                ft.TextButton("Aceptar", on_click=lambda e: page.open(dlg)),
                ft.TextButton("Cancelar", on_click=lambda e: page.close(confirm_save)),
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )

        def copiar_historia(e):
            # Recolectar todo el texto de los mensajes
            texto_total = []
            for ctrl in mensajes.controls:
                if isinstance(ctrl, ft.Text):
                    linea = ""
                    # Manejar texto con formato (spans)
                    if ctrl.spans:
                        for span in ctrl.spans:
                            linea += span.text
                    else:  # Texto simple
                        linea = ctrl.value or ""
                    
                    if linea.strip():  # Ignorar líneas vacías
                        texto_total.append(linea)
            
            # Unir todo el texto y copiar al portapapeles
            texto_final = "\n".join(texto_total)
            pyperclip.copy(texto_final)


            
        btn_copy = ft.IconButton(
            icon=ft.Icons.CONTENT_COPY,
            tooltip="Copiar historia",
            on_click=copiar_historia
        )




        # def copiar_historia():
        #     texto_total = "\n".join(
        #         ctrl.value for ctrl in mensajes.controls if isinstance(ctrl, ft.Text)
        #     )
        #     pyperclip.copy(texto_total)

        def toggle_theme(e):
            page.theme_mode = (
                ft.ThemeMode.DARK if page.theme_mode == ft.ThemeMode.LIGHT else ft.ThemeMode.LIGHT
            )
            page.update()

        
        def handle_close(e):
            page.close(dlg_modal)
            page.add(ft.Text(f"Modal dialog closed with action: {e.control.text}"))

        dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Instrucciones de uso"),
            content=ft.Text(
                        "El modo detallado te guiará por las siguientes secciones preestablecidas:\n\n"
                        "    1. Trama e hilo simbólico\n"
                        "    2. Descripción del mundo\n"
                        "    3. Personajes principales\n"
                        "    4. Personajes secundarios\n"
                        "    5. Descripción de escenarios\n"
                        "    6. Análisis de la historia: planteamiento, nudo y desenlace\n"
                        "    7. Estructura de capítulos\n"
                        "    8. Escritura de capítulos\n\n"
                        "Comenzarás planteando una premisa o idea sobre tu historia y la IA te generará su trama e hilo simbólico.\n\n"
                        "Tras esto puedes hacer 3 cosas:\n"
                        "- Modificar algún aspecto de la respuesta o pedir que genere una nueva.\n"
                        "- Avanzar a la siguiente sección con mensajes de confirmación (sí, vale, sigamos, ok...)\n"
                        "- Avanzar a la sección que quieras indicando el nombre.\n",
                        size=14,
                        text_align=ft.TextAlign.JUSTIFY,
                    ),
            actions=[
                ft.TextButton("Yes", on_click=handle_close),
                ft.TextButton("No", on_click=handle_close),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            on_dismiss=lambda e: page.add(
                ft.Text("Modal dialog dismissed"),
            ),
        )

        def boton_instrucciones(e):
            print("INSTRUCCIONES")

        ajustes_user = ft.PopupMenuButton(
            icon=ft.Icons.PERSON,
            #offset=ft.Offset(0, 40),  # 👈 desplaza el menú hacia abajo
            items=[
                ft.PopupMenuItem(
                    text="Ajustes",
                    icon=ft.Icons.SETTINGS,
                    on_click=lambda e: print("Ajustes")
                ),
                ft.PopupMenuItem(
                    text="Cerrar sesión",
                    icon=ft.Icons.LOGOUT,
                    on_click=lambda e: page.go("/")
                ),
                ft.PopupMenuItem(
                    icon=ft.Icons.BRIGHTNESS_6, 
                    text="Cambiar tema", 
                    on_click=toggle_theme
                ),
                ft.PopupMenuItem(
                    icon=ft.Icons.INFO,
                    text="Instrucciones",
                    on_click=lambda e: page.open(dlg_modal)
                )
            ]
        )



        mi_usuario = ft.TextField(
            value=usuario,  # 👈 asegúrate que `usuario` es texto (str)
            #suffix_icon=ft.Icons.PERSON,
            suffix_icon=ajustes_user,
            width=100,
            read_only=True,  # opcional, si no quieres que lo editen
            text_style=ft.TextStyle(size=14),
            content_padding=ft.Padding(5, 5, 5, 5)
        )

        page.appbar = ft.AppBar(
            leading=btn_back,
            leading_width=40,
            title=titulo,
            center_title=True,
            actions=[
                mi_usuario,
            ],  # 👈 se muestra a la derecha
            bgcolor=th["FONDO"]
        )
        
        # def send_message(e):
        #     if escritura.value != "":
        #         print(f"Mensaje enviado: {escritura.value}")
        #         escritura.value = ""
        #         page.update()

        def corregir_estilos_linea(linea: str) -> str:
            # Si hay un número impar de asteriscos dobles, añade los de cierre al final
            if linea.count("**") % 2 != 0:
                linea += "**"
            if linea.count("*") % 2 != 0 and "**" not in linea:  # solo si no es parte de negrita
                linea += "*"
            return linea



        def convertir_a_richtext(texto: str) -> ft.Text:
            """
            Convierte texto con Markdown simulado (*, **, ***) en spans formateados.
            """
            partes = re.split(r'(\*\*\*.*?\*\*\*|\*\*.*?\*\*|\*.*?\*)', texto)
            spans = []

            for parte in partes:
                if not parte:
                    continue

                style = ft.TextStyle()
                if parte.startswith("***") and parte.endswith("***"):
                    contenido = parte[3:-3]
                    style.weight = ft.FontWeight.BOLD
                    style.italic = True
                elif parte.startswith("**") and parte.endswith("**"):
                    contenido = parte[2:-2]
                    style.weight = ft.FontWeight.BOLD
                elif parte.startswith("*") and parte.endswith("*"):
                    contenido = parte[1:-1]
                    style.italic = True
                else:
                    contenido = parte

                spans.append(ft.TextSpan(contenido, style=style))

            return ft.Text(spans=spans, selectable=True, size=30)  # <-- Añade o cambia el parámetro size aquí

        def parse_respuesta_md(respuesta: str) -> list[ft.Text]:
            """
            Procesa una respuesta Markdown simulada y devuelve una lista de componentes Flet.
            Detecta encabezados tipo ### Título o **# Título** y formatea negrita/cursiva.
            """
            elementos = []
            for linea in respuesta.split("\n"):
                linea = linea.strip()
                if not linea:
                    continue

                linea = corregir_estilos_linea(linea)
                # Encabezado tipo ### Título o ### **Título**
                if re.match(r"^(#{3,6})\s+(.*?)(\s+#{3,6})?$", linea):
                    nivel, contenido = re.findall(r"^(#{3,6})\s+(.*?)(\s+#{3,6})?$", linea)[0][:2]
                    contenido = re.sub(r"\*\*(.*?)\*\*", r"\1", contenido)  # 👈 elimina negrita Markdown
                    tamaño = {3: 42, 4: 38, 5: 34, 6: 30}.get(len(nivel), 25)  # Cambia aquí
                    elementos.append(
                        ft.Text(contenido, weight=ft.FontWeight.BOLD, size=tamaño, selectable=True)
                    )

                else:
                    elementos.append(convertir_a_richtext(linea))

            return elementos


        def send_message(e, prompt_override=None, accion="crear", seccion="trama_e_hilo_simbolico"):
            deshabilitar_botones_secciones()
            prompt_usuario = entrada.value.strip()
            prompt = prompt_override if prompt_override is not None else prompt_usuario

            # Guardar solo si es prompt del usuario
            if accion == "crear" and prompt_override is None:
                self.ultimo_prompt = prompt_usuario
            print(f"Mensaje enviado: {prompt}")
            scroll_marker = ft.Text("", key="scroll-target")
            mensajes.controls.append(scroll_marker)
         
            entrada.value = ""

            zona_carga.visible = True
            panel_entrada.visible = False
            btn_copy.disabled = True
            lista_btn.visible = False
            mensajes.controls.append(ft.Text(f"Tu: {prompt}"))
            page.update()
            threading.Thread(target=procesar_en_segundo_plano, args=(prompt,accion,seccion,)).start()

        def procesar_en_segundo_plano(prompt, accion, seccion):
            print("Estoy procesando la respuesta")

            respuesta = controller.procesar_mensaje(prompt, self.ultimo_prompt, accion, seccion)
            #self.ultimo_prompt = prompt
            print("AHORA TOCA GUARDAR LOS DATOS\n")
            #controller.guardar_datos(respuesta)
            print("\n\n\n ----------------------\n\n\n")
            page.run_thread(lambda: (mostrar_respuesta(respuesta, seccion), page.update()))
            

        def mostrar_respuesta(respuesta, seccion=None):
            habilitar_botones_secciones()
            btn_send.disabled = False
            zona_carga.visible = False
            btn_copy.disabled = False
            lista_btn.visible = True
            self.ultima_respuesta = respuesta

            mensajes.controls.append(ft.Text("🤖 IA:", weight=ft.FontWeight.BOLD, selectable=True))
            for elem in parse_respuesta_md(respuesta):
                mensajes.controls.append(elem)

            # ← Aquí actualizamos el título una vez todo ha terminado
            if seccion:
                # Si el controller ha decidido otra sección internamente, respétala:
                nueva = getattr(controller, "seccion", None) or seccion
                self.seccion_actual = nueva
                #titulo_dinamico.value = titulo_seccion_text(nueva)

            actualizar_boton_escritura()
            page.update()
            mensajes.scroll_to(key="scroll-target", duration=300)


            

        btn_send = ft.IconButton(
            icon=ft.Icons.SEND,
            on_click=send_message
        )



        mensajes = ft.Column(
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            spacing=10
        )

        # mensajes.controls.append(
        #     ft.Text("### Trama e hilo simbólico", weight=ft.FontWeight.BOLD, size=28, selectable=True)
        # )
        # mensajes.controls.append(
        #     ft.Text(
        #         "Lucía, una niña curiosa y valiente, vive en un pequeño pueblo rodeado de montañas. Su mayor deseo es descubrir el mundo más allá de su hogar. Un día, tras ayudar a un pájaro herido, recibe una pluma dorada mágica que le permite volar y explorar lugares desconocidos. "
        #         "Durante su viaje, Lucía encuentra un valle oculto donde las flores brillan en la oscuridad y los animales hablan. Allí, aprende que la verdadera magia reside en la bondad y el coraje de ayudar a los demás.\n\n"
        #         "El hilo simbólico de la historia es el crecimiento personal de Lucía: su viaje representa el paso de la infancia a la madurez, guiada por la empatía y la generosidad. La pluma dorada simboliza la recompensa de actuar con el corazón, y el valle secreto, los tesoros que se descubren cuando uno se atreve a soñar y a cuidar de los demás.",
        #         size=20,
        #         selectable=True
        #     )
        # )
        cargando = ft.Column([
            ft.ProgressRing(),
                #ft.Text("La IA está escribiendo...", italic=True)
            ], 
            spacing=10,
            alignment=ft.MainAxisAlignment.CENTER
        )
        
        zona_carga = ft.Container(
            content=cargando,
            alignment=ft.alignment.center,
            bgcolor=ft.Colors.with_opacity(0.5, ft.Colors.SURFACE),  # fondo semi-transparente
            visible=False,  # 👈 solo visible durante carga
            expand=True
        )

        zona_historia = ft.Container(
            content=mensajes,
            border_radius=15,
            padding=20,
            alignment=ft.alignment.center,
            width=None,
            bgcolor=ft.Colors.GREY_200,
            #bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
            border=ft.border.all(2, ft.Colors.OUTLINE),
            visible=True,
            expand=True
        )

        entrada = ft.TextField(
            hint_text="Escribe tu historia aquí",
            multiline=False,
            autofocus=True,
            border=ft.InputBorder.OUTLINE,
            border_radius=28,
            content_padding=ft.Padding(22, 20, 22, 20),  # más espacio interno
            focused_border_color=th["TEXT"],
            suffix_icon=btn_send,
            width=800,                # más ancho
            height=70,                # fuerza altura mayor
            text_size=20,              # aumenta tamaño de la letra
            on_submit=send_message,
        )


        # campo_modificar = ft.TextField(
        #     hint_text="¿Que cambio quieres hacer en la sección?",
        #     multiline=False,
        #     autofocus=True,
        #     border=ft.InputBorder.OUTLINE,
        #     suffix_icon=btn_send,
        #     width=400,
        #     #on_submit=send_message
        # )

        # def button_accept(e):
        #     page.close(modificar_dialog)
        #     mensaje = campo_modificar.value.strip()  # Limpiar el campo de entrada
        #     continuar_capitulo(e, prompt_override=mensaje, accion="modificar")

        # modificar_dialog = ft.AlertDialog(
        #     modal=True,
        #     title=ft.Text("Modificar"),
        #     content=ft.Container(
        #         campo_modificar,
        #         width=520,
        #     ),
        #     actions=[
        #         ft.TextButton("Cancelar", on_click=lambda e: page.close(modificar_dialog)),
        #         ft.TextButton("Aceptar", on_click=button_accept), 
        #     ],
        #     actions_alignment=ft.MainAxisAlignment.END
        # )

        # def modificar_historia(e):
        #     print("Modificar historia")
        #     campo_modificar.value = ""  # Limpiar el campo de entrada
        #     page.open(modificar_dialog)  # Abrir el diálogo de modificación
        #     # Aquí puedes implementar la lógica para modificar la historia



        def reescribir_historia(e):
            nuevo_prompt = (
                "No me ha gustado la respuesta anterior. A continuación te paso la seccion que has generado. "
                "Por favor escribe otra sección distinta pero manteniendo la coherencia de la propuesta inicial.\n\n"
            )
            send_message(e, prompt_override=nuevo_prompt, accion="reescribir", seccion=self.seccion_actual)

        def button_no(e):
            print("Continuamos con la historia")
            page.close(confirm_tittle)
            send_message(e, accion="crear")

        def button_accept(e):
            print("Añadiendo ideas o preferencias")
            page.close(confirm_tittle)
            entrada.disabled = False
            page.update()
            # Aquí puedes implementar la lógica para añadir ideas o preferencias
            #send_message(prompt_override="Añadir ideas o preferencias", accion="normal")

        confirm_tittle = ft.AlertDialog(
            modal=True,
            title=ft.Text("Continuar"),
            content=ft.Text("¿Quieres añadir alguna idea o preferencia para la siguiente sección?"),
            actions=[
                ft.TextButton("Sí", on_click=button_accept),
                ft.TextButton("No", on_click=button_no),
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )

        

        panel_entrada = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        "¿Cómo quieres que sea la historia de hoy?",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color=th["TEXT"],
                    ),
                    entrada],
                spacing=10,
                alignment=ft.MainAxisAlignment.CENTER
            ),
            padding=12,
            border_radius=24,
        )


        def continuar_historia(e):
            print("Continuar con la historia")
            page.open(confirm_tittle)
            # Aquí puedes implementar la lógica para continuar la historia

        # btn_modificar = ft.ElevatedButton("Modificar", on_click=lambda e: mostrar_popup_modificar(self.seccion_actual)),
        # btn_reescribir = ft.ElevatedButton("Reescribir", on_click=lambda e: reescribir_historia(e)),

        btn_modificar = ft.ElevatedButton("Modificar", on_click=lambda e: mostrar_popup_modificar(self.seccion_actual))
        btn_reescribir = ft.ElevatedButton("Reescribir", on_click=lambda e: reescribir_historia(e))

        lista_btn = ft.Row(
            [btn_modificar, btn_reescribir],
            spacing=10,
            alignment=ft.MainAxisAlignment.START,
            visible=False
        )

        # helper para que las celdas tengan el mismo ancho
        def cell(ctrl): 
            return ft.Container(content=ctrl, expand=1)

        zona_stack = ft.Stack(
            alignment=ft.alignment.center,   # centra a los hijos no posicionados
            controls=[
                zona_historia,               # capa base (ocupa todo)
                panel_entrada,               # solo ocupa su propio ancho -> no bloquea el scroll
                zona_carga,                  # overlay de carga por encima
            ],
            expand=True,
        )


        # titulo_dinamico = ft.Text(titulo_seccion_text(self.seccion_actual), weight=ft.FontWeight.BOLD, size=16)
        # acciones_seccion = ft.Row(
        #     controls=[
        #         ft.TextButton("Configurar / Generar…", icon=ft.Icons.TUNE, on_click=lambda e: mostrar_popup_caracteristicas(self.seccion_actual)),
        #         ft.IconButton(icon=ft.Icons.REFRESH, tooltip="Refrescar", on_click=lambda e: cargar_seccion_ui(self.seccion_actual)),
        #     ],
        #     spacing=8
        # )
        # contenedor_seccion = ft.Column(spacing=8)

        # --- BOTONES "VER" (no generan nada, solo muestran la sección debajo del divider)

                # Texto que cambia según el mock seleccionado
        # Texto que muestra el detalle del item actual
        # Estado para edición
        edit_fields: dict[str, ft.TextField] = {}
        edit_form = ft.Column(visible=False, spacing=10)

        detalle_texto = ft.Text("", size=SIZE_BODY, selectable=True)
        # Área con scroll para el contenido largo
        detalle_area = ft.Column(
            [detalle_texto],
            expand=True,
            scroll=ft.ScrollMode.AUTO
        )

        btn_edit = ft.OutlinedButton("Editar", icon=ft.Icons.EDIT, visible=True)
        btn_save = ft.ElevatedButton("Guardar", icon=ft.Icons.SAVE, visible=False)
        btn_cancel = ft.TextButton("Cancelar", visible=False)


        # Fila de navegación rápida (se rellena con botones por item)
        quick_nav_row = ft.Row(spacing=4)

        # === Helpers de formato (Punto 2) ===
        def format_personaje(p: dict) -> str:
            desc = p.get("Descripción") or p.get("Descripcion") or "—"  # ← aquí la magia
            rel  = p.get("Relaciones")
            rel_txt = ", ".join(rel) if isinstance(rel, list) else (rel or "—")

            return (
                f"**Nombre:** {p.get('Nombre','—')}\n"
                f"**Rol:** {p.get('Rol','—')}\n"
                f"**Edad/sexo:** {p.get('Edad y sexo','—')}\n"
                f"**Personalidad:** {p.get('Personalidad','—')}\n"
                f"**Descripción:** {desc}\n"
                f"**Historia:** {p.get('Historia','—')}\n"
                f"**Desarrollo personal:** {p.get('Desarrollo personal','—')}\n"
                f"**Relaciones:** {rel_txt}"
            )


        def format_escenario(e: dict) -> str:
            # Formatea la lista de eventos como viñetas
            eventos = e.get("Eventos importantes")
            if isinstance(eventos, list):
                eventos_txt = "\n" + "\n".join(f"- {x}" for x in eventos)
            else:
                eventos_txt = eventos if eventos else "—"

            return (
                f"**Nombre:** {e.get('Nombre','—')}\n"
                f"**Localización:** {e.get('Localización','—')}\n"
                f"**Descripción:** {e.get('Descripción','—')}\n"
                f"**Importancia en la historia:** {e.get('Importancia en la historia','—')}\n"
                f"**Historia y trasfondo:** {e.get('Historia y trasfondo','—')}\n"
                f"**Eventos importantes:** {eventos_txt}"
            )

        def format_bloque(b: dict) -> str:
            return f"{b.get('titulo','—')}\n\n{b.get('texto','—')}"
        def set_detalle(idx: int):
            self.mock_idx = idx % len(self.mock_items)
            texto = self.mock_items[self.mock_idx]

            # convertir el markdown (**...**) a spans con estilos
            rt = convertir_a_richtext(texto)         # ← ya la tenías
            detalle_texto.spans = rt.spans           # reutilizamos el mismo control
            detalle_texto.value = None               # borra el value plano
            detalle_texto.size = SIZE_BODY           # aplica tu tamaño
            page.update()

        # === Esquema reutilizable para edición/visualización ===
        SCHEMAS = {
            "personajes": [
                {"label": "Nombre", "key": "Nombre", "multiline": False},
                {"label": "Rol", "key": "Rol", "multiline": False},
                {"label": "Edad y sexo", "key": "Edad y sexo", "multiline": False},
                {"label": "Personalidad", "key": "Personalidad", "multiline": True},
                {"label": "Descripcion", "key": "Descripcion", "multiline": True},
                {"label": "Historia", "key": "Historia", "multiline": True},
                {"label": "Desarrollo personal", "key": "Desarrollo personal", "multiline": True},
                {"label": "Relaciones (una por línea)", "key": "Relaciones", "multiline": True, "is_list": True, "sep": "\n"},
            ],
            "escenarios": [
                {"label": "Nombre", "key": "Nombre", "multiline": False},
                {"label": "Localización", "key": "Localización", "multiline": False},
                {"label": "Descripción", "key": "Descripción", "multiline": True},
                {"label": "Importancia en la historia", "key": "Importancia en la historia", "multiline": True},
                {"label": "Historia y trasfondo", "key": "Historia y trasfondo", "multiline": True},
                {"label": "Eventos importantes (una por línea)", "key": "Eventos importantes", "multiline": True, "is_list": True, "sep": "\n"},
            ],
        }

        # === Estado para edición (reutilizable) ===
        tipo_actual = None
        items_actuales = []
        edit_mode = False
        edit_fields: dict[str, ft.TextField] = {}
        edit_form = ft.Column(visible=False, spacing=10)

        def build_form(tipo, item, edit_fields, edit_form):
            edit_fields.clear()
            edit_form.controls.clear()
            for f in SCHEMAS.get(tipo, []):
                label = f["label"]; key = f["key"]
                val = item.get(key, "")
                if f.get("is_list") and isinstance(val, list):
                    val = (f.get("sep") or "\n").join(map(str, val))
                tf = ft.TextField(label=label, value=str(val) if val is not None else "", multiline=f["multiline"], dense=True)
                edit_fields[label] = tf
                edit_form.controls.append(tf)

        def collect_form(tipo, edit_fields):
            nuevo = {}
            for f in SCHEMAS.get(tipo, []):
                label = f["label"]; key = f["key"]
                raw = (edit_fields[label].value or "")
                if f.get("is_list"):
                    sep = f.get("sep") or "\n"
                    nuevo[key] = [x.strip() for x in raw.split(sep) if x.strip()]
                else:
                    nuevo[key] = raw.strip()
            return nuevo



        def navegar_mock(delta: int):
            if not self.mock_items:
                return
            set_detalle(self.mock_idx + delta)

        def navegar_mock_to(i: int):
            if not self.mock_items:
                return
            set_detalle(i)

        def volver_panel(e=None):
            panel_detalle.visible = False
            panel_main.visible = True
            page.update()


        def enter_edit_mode():
            # Usa self.tipo_actual + self.items_actuales + self.mock_idx
            if not self.items_actuales:
                return
            item = self.items_actuales[self.mock_idx]
            build_form(self.tipo_actual, item, edit_fields, edit_form)
            detalle_area.controls = [edit_form]
            edit_form.visible = True
            detalle_texto.visible = False
            btn_edit.visible = False
            btn_save.visible = True
            btn_cancel.visible = True
            page.update()

        def cancel_edit(e=None):
            detalle_area.controls = [detalle_texto]
            edit_form.visible = False
            detalle_texto.visible = True
            btn_save.visible = False
            btn_cancel.visible = False
            btn_edit.visible = True
            page.update()

        def save_edit():
            if not self.items_actuales:
                cancel_edit()
                return

            idx = self.mock_idx
            tipo = self.tipo_actual
            item_nuevo = collect_form(tipo, edit_fields)

            # === 3.A Persistencia en BD ===
            ok = True
            if tipo in ("personajes", "escenarios"):
                # Mapea al nombre de colección real que usas en BD
                seccion_real = "personajes_principales" if tipo == "personajes" else "descripcion_de_escenarios"
                ok = controller.actualizar_item(seccion_real, idx, item_nuevo)
            elif tipo == "mundo":
                titulo_bloque = self.items_actuales[idx].get("titulo", "")
                texto_nuevo = item_nuevo.get("texto", "")
                ok = controller.actualizar_mundo_bloque(titulo_bloque, texto_nuevo)

            # === 3.B Actualiza la UI como ya hacías ===
            self.items_actuales[idx] = item_nuevo
            if tipo == "personajes":
                self.mock_items[idx] = format_personaje(item_nuevo)
                try:
                    btn = quick_nav_row.controls[idx]
                    if hasattr(btn, "text"):
                        btn.text = item_nuevo.get("Nombre", f"Item {idx+1}")
                except Exception:
                    pass
            elif tipo == "escenarios":
                self.mock_items[idx] = format_escenario(item_nuevo)
                try:
                    btn = quick_nav_row.controls[idx]
                    if hasattr(btn, "text"):
                        btn.text = item_nuevo.get("Nombre", f"Item {idx+1}")
                except Exception:
                    pass
            elif tipo == "mundo":
                self.mock_items[idx] = format_bloque(item_nuevo)
                try:
                    btn = quick_nav_row.controls[idx]
                    if hasattr(btn, "text"):
                        btn.text = item_nuevo.get("titulo", f"Bloque {idx+1}")
                except Exception:
                    pass

            cancel_edit()
            set_detalle(idx)

            # Feedback
            msg = "Guardado correctamente en la base de datos." if ok else "No se pudo guardar en la base de datos."
            page.snack_bar = ft.SnackBar(ft.Text(msg))
            page.snack_bar.open = True


        # después de definir enter_edit_mode(), cancel_edit() y save_edit():
        btn_edit.on_click = lambda e: enter_edit_mode()
        btn_cancel.on_click = cancel_edit
        btn_save.on_click = lambda e: save_edit()




        def ver_seccion(seccion: str):
            self.seccion_actual = seccion
            titulo_dinamico.value = titulo_seccion_text(seccion)

            # Loader en el panel derecho
            detalle_texto.value = "Cargando..."
            quick_nav_row.controls = []
            panel_main.visible = False
            panel_detalle.visible = True
            deshabilitar_botones_secciones()
            page.update()

            def worker():
                try:
                    datos = controller.cargar_seccion(seccion)
                    print("DEBUG tipo:", datos.get("tipo"))
                    if datos.get("items"):
                        print("DEBUG claves del primer escenario:", list(datos["items"][0].keys()))

                except Exception as ex:
                    datos = {"tipo": "texto", "items": [{"titulo": "Error", "texto": str(ex)}]}
                    page.snack_bar = ft.SnackBar(ft.Text(f"Error al cargar {seccion}: {ex}"))
                    page.snack_bar.open = True

                def pintar():
                    self.tipo_actual = datos.get("tipo")
                    self.items_actuales = datos.get("items") or []
                    items = self.items_actuales
                    tipo = self.tipo_actual

                    if not items:
                        self.mock_items = [f"No hay contenido guardado todavía para {titulo_seccion_text(seccion)}."]
                        quick_nav_row.controls = []
                        set_detalle(0)
                    else:
                        if tipo == "personajes":
                            self.mock_items = [format_personaje(p) for p in items]
                            quick_nav_row.controls = [
                                ft.TextButton(p.get("Nombre", f"Item {i+1}"), on_click=lambda e, i=i: navegar_mock_to(i))
                                for i, p in enumerate(items)
                            ]
                        elif tipo == "escenarios":
                            self.mock_items = [format_escenario(x) for x in items]
                            quick_nav_row.controls = [
                                ft.TextButton(x.get("Nombre", f"Item {i+1}"), on_click=lambda e, i=i: navegar_mock_to(i))
                                for i, x in enumerate(items)
                            ]
                        else:  # trama / mundo / texto
                            self.mock_items = [format_bloque(b) for b in items]
                            quick_nav_row.controls = [
                                ft.TextButton(b.get("titulo", f"Bloque {i+1}"), on_click=lambda e, i=i: navegar_mock_to(i))
                                for i, b in enumerate(items)
                            ]
                        set_detalle(0)

                    habilitar_botones_secciones()
                    page.update()

                # Volvemos al hilo de UI para pintar
                try:
                    page.invoke_later(pintar)
                except AttributeError:
                    pintar()

            threading.Thread(target=worker, daemon=True).start()




        def cell(ctrl): 
            return ft.Container(content=ctrl, expand=1)

        # --- BOTONES "VER"
        btn_mundo_ver       = ft.ElevatedButton("Mundo",       icon=ft.Icons.VISIBILITY, on_click=lambda e: ver_seccion("descripcion_del_mundo"),       disabled=False, height=44)
        btn_personajes_ver  = ft.ElevatedButton("Personajes",  icon=ft.Icons.VISIBILITY, on_click=lambda e: ver_seccion("personajes_principales"),     disabled=False, height=44)
        btn_escenarios_ver  = ft.ElevatedButton("Escenarios",  icon=ft.Icons.VISIBILITY, on_click=lambda e: ver_seccion("descripcion_de_escenarios"),  disabled=False, height=44)
        btn_estructura_ver  = ft.ElevatedButton("Estructura",  icon=ft.Icons.VISIBILITY, on_click=lambda e: ver_seccion("estructura_de_capitulos"),    disabled=False, height=44)

        # --- BOTONES "GENERAR" (tu flujo previo)
        btn_mundo_gen       = ft.ElevatedButton("Mundo",       icon=ft.Icons.TUNE, on_click=lambda e: mostrar_popup_caracteristicas("descripcion_del_mundo"),       disabled=True, height=44)
        btn_personajes_gen  = ft.ElevatedButton("Personajes",  icon=ft.Icons.TUNE, on_click=lambda e: mostrar_popup_caracteristicas("personajes_principales"),     disabled=True, height=44)
        btn_escenarios_gen  = ft.ElevatedButton("Escenarios",  icon=ft.Icons.TUNE, on_click=lambda e: mostrar_popup_caracteristicas("descripcion_de_escenarios"),  disabled=True, height=44)
        btn_estructura_gen  = ft.ElevatedButton("Estructura",  icon=ft.Icons.TUNE, on_click=lambda e: mostrar_popup_caracteristicas("estructura_de_capitulos"),    disabled=True, height=44)
        btn_escritura = ft.ElevatedButton(
            "Escritura",
            icon=ft.Icons.TUNE,
            on_click=lambda e: page.open(confirm_escritura),   # ← abre confirm
            disabled=True,
            height=44,
            expand=True,
        )

        # --- BOTONES CAPITULOS
        btn_continuar_historia = ft.ElevatedButton("Continuar", visible=False, icon=ft.Icons.TUNE, on_click=lambda e:  continuar_capitulo(e),  disabled=True, height=44)
        # btn_capitulo_1 = ft.ElevatedButton("Capitulo 1", visible=False, icon=ft.Icons.VISIBILITY, on_click=lambda e:  continuar_capitulo(e),  disabled=True, height=44)
        # btn_capitulo_2 = ft.ElevatedButton("Capitulo 2", visible=False, icon=ft.Icons.VISIBILITY, on_click=lambda e:  continuar_capitulo(e),  disabled=True, height=44)
        # btn_capitulo_3 = ft.ElevatedButton("Capitulo 3", visible=False, icon=ft.Icons.VISIBILITY, on_click=lambda e:  continuar_capitulo(e),  disabled=True, height=44)
        # btn_capitulo_4 = ft.ElevatedButton("Capitulo 4", visible=False, icon=ft.Icons.VISIBILITY, on_click=lambda e:  continuar_capitulo(e),  disabled=True, height=44)
        btn_fin_historia = ft.ElevatedButton(
            "Finalizar",
            visible=False,
            icon=ft.Icons.FLAG,
            disabled=True,
            height=44,
            on_click=lambda e: abrir_confirm_fin(e)
        )

        # --- POPUP de finalización ---
        def abrir_confirm_fin(e):
            page.open(confirm_fin)

        def guardar_y_salir(e):
            # cierra el popup
            page.close(confirm_fin)
            # ⇩ guarda (ajusta al método real de tu controller)
            try:
                nombre_pdf = f"{nombre_historia}.pdf"
                controller.guardar_en_pdf(nombre_pdf)
                # Ejemplos posibles: elige el que tengas implementado
                # controller.guardar_historia_completa()
                # controller.exportar_historia(nombre_historia)
                # controller.cerrar_y_guardar(self.capitulo_actual)
                pass
                page.snack_bar = ft.SnackBar(ft.Text("Historia guardada correctamente."))
            except Exception as ex:
                page.snack_bar = ft.SnackBar(ft.Text(f"No se pudo guardar: {ex}"))
            page.snack_bar.open = True
            page.update()
            page.go("/home")  # volver a inicio

        def salir_sin_guardar(e):
            page.close(confirm_fin)
            page.go("/home")

        confirm_fin = ft.AlertDialog(
            modal=True,
            title=ft.Text("Finalizar historia"),
            content=ft.Text("¿Deseas guardar la historia antes de salir?"),
            actions=[
                ft.ElevatedButton("Guardar y salir", icon=ft.Icons.SAVE, on_click=guardar_y_salir),
                ft.TextButton("Salir sin guardar", icon=ft.Icons.EXIT_TO_APP, on_click=salir_sin_guardar),
                ft.TextButton("Cancelar", on_click=lambda e: page.close(confirm_fin)),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )


        def mostrar_fin():
            page.snack_bar = ft.SnackBar(ft.Text("¡Has terminado la historia!"))
            page.snack_bar.open = True
            page.update()




        # Título y zona dinámica que ya tenías
        titulo_dinamico = ft.Text(titulo_seccion_text(self.seccion_actual), weight=ft.FontWeight.BOLD, size=SIZE_HEADING)
        contenedor_instrucciones = ft.Column(
            controls=[
                ft.Text("📖 Instrucciones básicas", weight=ft.FontWeight.BOLD, size=22),
                ft.ListTile(leading=ft.Icon(ft.Icons.LIGHTBULB), title=ft.Text("Introduce una idea inicial o temática.")),
                ft.ListTile(leading=ft.Icon(ft.Icons.CATEGORY), title=ft.Text("Genera las secciones principales de la historia.")),
                ft.ListTile(leading=ft.Icon(ft.Icons.CATEGORY), title=ft.Text("Una vez completadas, activa la opción Escritura para comenzar los capítulos.")),
                ft.ListTile(leading=ft.Icon(ft.Icons.BOOK), title=ft.Text("Avanza capítulo a capítulo con 'Continuar'.")),
                ft.ListTile(leading=ft.Icon(ft.Icons.EDIT), title=ft.Text("Usa 'Modificar' o 'Reescribir' para hacer cambios.")),
                ft.ListTile(leading=ft.Icon(ft.Icons.FLAG), title=ft.Text("Finaliza la historia en el capítulo 4.")),
            ],
            spacing=4
        )


        # --- Vista principal (main) del panel derecho
        panel_main = ft.Column([
            ft.Text("SECCIONES", weight=ft.FontWeight.BOLD, size=18),

            ft.Text("Ver", size=12, color=ft.Colors.ON_SURFACE_VARIANT),
            ft.Row([cell(btn_mundo_ver),      cell(btn_personajes_ver)], spacing=10),
            ft.Row([cell(btn_escenarios_ver), cell(btn_estructura_ver)], spacing=10),
            # ft.Row([cell(btn_capitulo_1),      cell(btn_capitulo_2)], spacing=10),
            # ft.Row([cell(btn_capitulo_3), cell(btn_capitulo_4)], spacing=10),

            ft.Container(height=8),
            ft.Text("Generar", size=12, color=ft.Colors.ON_SURFACE_VARIANT),
            ft.Row([cell(btn_mundo_gen),      cell(btn_personajes_gen)], spacing=10),
            ft.Row([cell(btn_escenarios_gen), cell(btn_estructura_gen)], spacing=10),
            # Solo muestra btn_escritura si no es el capítulo 4, y btn_fin_historia si es el capítulo 4
            ft.Row([cell(btn_escritura), cell(btn_continuar_historia)], spacing=10),
            # y mantén btn_fin_historia en otra celda o en la misma fila:
            ft.Row([cell(btn_fin_historia)], spacing=10),
            ft.Divider(height=16, thickness=1, color=ft.Colors.OUTLINE),
            contenedor_instrucciones,
        ], spacing=10)

                # Qué secciones hacen falta para habilitar "Escritura"
        SECCIONES_REQUERIDAS = [
            "trama_e_hilo_simbolico",
            "descripcion_del_mundo",
            "personajes_principales",
            "descripcion_de_escenarios",
            # si quieres exigir estructura, descomenta:
            "estructura_de_capitulos",
        ]

        def secciones_requeridas_completas() -> bool:
            completas = all(controller.estado_secciones.get(s, False) for s in SECCIONES_REQUERIDAS)
            if completas:
                self.seccion_actual = "escritura"
            return completas

        def actualizar_boton_escritura():
            habilitado = secciones_requeridas_completas()
            btn_escritura.disabled = not habilitado
            btn_escritura.tooltip = (
                "Completa Trama, Mundo, Personajes y Escenarios para habilitar"
                if not habilitado else "Configurar escritura"
            )
            page.update()


        # --- Vista de detalle (oculta al inicio)
        panel_detalle = ft.Container(
            content=ft.Column([
                titulo_dinamico,
                detalle_area,
                ft.Row([
                    ft.ElevatedButton("Atrás", icon=ft.Icons.ARROW_BACK, on_click=volver_panel),
                    ft.OutlinedButton("Anterior", icon=ft.Icons.CHEVRON_LEFT, on_click=lambda e: navegar_mock(-1)),
                    ft.OutlinedButton("Siguiente", icon=ft.Icons.CHEVRON_RIGHT, on_click=lambda e: navegar_mock(1)),
                    
                ], spacing=8),
                ft.Row([
                    btn_edit, btn_save, btn_cancel,  # ← aquí
                ], spacing=8),
                quick_nav_row,
            ], spacing=12, expand=True),
            visible=False,
            padding=10,
            expand=True
        )



        panel_secciones = ft.Container(
            ft.Column([
                panel_main,
                panel_detalle,  # se alternan con visible True/False
            ]),
            border=ft.border.all(1),
            border_radius=15,
            padding=20,
            width=320,
            expand=1,
            bgcolor=ft.Colors.GREY_300
        )

        # Coloca el panel a la derecha
        zona_stack_row = ft.Row(
            [
                ft.Container(zona_stack, expand=3),
                panel_secciones,
            ],
            expand=True
        )

        # ...existing code...
                # Contenedor donde irán las acciones de la sección (configurar/generar, refrescar…)
        # acciones_seccion = ft.Row(
        #     controls=[
        #         ft.TextButton("Configurar / Generar…", icon=ft.Icons.TUNE, on_click=lambda e: mostrar_popup_caracteristicas(self.seccion_actual)),
        #         ft.IconButton(icon=ft.Icons.REFRESH, tooltip="Refrescar", on_click=lambda e: cargar_seccion_ui(self.seccion_actual)),
        #     ],
        #     spacing=8
        # )

        # Aquí se dibuja la lista de items de la sección o el estado vacío
        


        campo_caracteristicas = ft.TextField(
            hint_text="¿Qué características especiales quieres para esta sección?",
            multiline=True,
            width=400,
            autofocus=True
        )

        def mostrar_popup_caracteristicas(seccion):
            self.seccion_pendiente = seccion
            campo_caracteristicas.value = ""
            campo_caracteristicas.label = f"Características para {titulo_seccion_text(seccion)}"
            popup_caracteristicas.data = seccion
            page.open(popup_caracteristicas)

        def on_text_change(e):
            campo_modificar2.value = e.control.value

        campo_modificar2 = ft.TextField(
            hint_text="¿Que modificación quieres realizar?",
            multiline=True,
            width=400,
            autofocus=True,
            on_change=on_text_change
        )

        def mostrar_popup_modificar(seccion):
            campo_modificar2.value = ""
            campo_modificar2.label = f"Modificar {titulo_seccion_text(seccion)}"
            popup_modificar.data = seccion
            page.open(popup_modificar)


        def aceptar_modificacion(e):
            modificacion = ""
            seccion = popup_modificar.data
            modificacion = campo_modificar2.value.strip()
            page.close(popup_modificar)

            # Enviamos y PASAMOS 'seccion' para actualizar el título al final
            send_message(e, prompt_override=modificacion, accion="modificar", seccion=seccion)

        popup_modificar = ft.AlertDialog(
            modal=True,
            title=ft.Text("Modificar sección"),
            content=campo_modificar2,
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: page.close(popup_modificar)),
                ft.TextButton("Aceptar", on_click=lambda e: aceptar_modificacion(e)),
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )

        def aceptar_caracteristicas(e):
            seccion = self.seccion_pendiente or popup_caracteristicas.data
            caracteristicas = ""
            caracteristicas = campo_caracteristicas.value.strip()
            page.close(popup_caracteristicas)

            # prompt = f"Quiero trabajar la sección '{seccion}'."
            # if caracteristicas:
            #     prompt += f" Características especiales: {caracteristicas}"

            # Enviamos y PASAMOS 'seccion' para actualizar el título al final
            send_message(e, prompt_override=caracteristicas, seccion=seccion)

        def actualizar_boton_fin():
            # Estamos en modo escritura y queremos que, si cap==4, aparezca "Finalizar"
            if self.capitulo_actual >= 4:
                self.capitulo_actual = 4  # por si alguien intenta pasar de 4
                btn_continuar_historia.visible = False
                btn_continuar_historia.disabled = True

                btn_fin_historia.visible = True
                btn_fin_historia.disabled = False
            else:
                btn_fin_historia.visible = False
                btn_fin_historia.disabled = True

                btn_continuar_historia.visible = True
                btn_continuar_historia.disabled = False
            page.update()


        def aceptar_escritura(e):
            #seccion = self.seccion_actual
            btn_escenarios_gen.visible = False
            btn_mundo_gen.visible = False
            btn_personajes_gen.visible = False
            btn_estructura_gen.visible = False
            btn_modificar.visible = False
            btn_reescribir.visible = False
            btn_continuar_historia.visible = True
            
            actualizar_boton_fin()
            prompt = f"Vamos a escribir el capitulo {self.capitulo_actual}"
            send_message(e, prompt_override=prompt, seccion="escritura")

        def continuar_capitulo(e):
            self.capitulo_actual += 1
            if self.capitulo_actual == 4:
                btn_continuar_historia.visible = False
                btn_fin_historia.visible = True
            actualizar_boton_fin()
            aceptar_escritura(e)

        # crea el diálogo una sola vez (pégalo cerca de donde defines btn_save)
        confirm_escritura = ft.AlertDialog(
            modal=True,
            title=ft.Text("¿Configurar escritura?"),
            content=ft.Text("Se generará la historia con las caracteristicas que has indicado."),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: page.close(confirm_escritura)),
                ft.ElevatedButton(
                    "Continuar",
                    on_click=lambda e: (page.close(confirm_escritura),
                                        setattr(self, "seccion_actual", "escritura"),
                                        aceptar_escritura(e))
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        popup_caracteristicas = ft.AlertDialog(
            modal=True,
            title=ft.Text("Características especiales"),
            content=campo_caracteristicas,
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: page.close(popup_caracteristicas)),
                ft.TextButton("Aceptar", on_click=lambda e: aceptar_caracteristicas(e)),
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )


        def deshabilitar_botones_secciones():
            for b in [
                btn_mundo_ver, btn_personajes_ver, btn_escenarios_ver, btn_estructura_ver,
                btn_mundo_gen, btn_personajes_gen, btn_escenarios_gen, btn_estructura_gen,
                btn_escritura, btn_continuar_historia, 
                #btn_capitulo_1, btn_capitulo_2, btn_capitulo_3, btn_capitulo_4
            ]:
                b.disabled = True
            page.update()


        def habilitar_botones_secciones():
            for b in [
                btn_mundo_ver, btn_personajes_ver, btn_escenarios_ver, btn_estructura_ver,
                btn_mundo_gen, btn_personajes_gen, btn_escenarios_gen, btn_estructura_gen, btn_continuar_historia,
                #btn_capitulo_1, btn_capitulo_2, btn_capitulo_3, btn_capitulo_4
            ]:
                b.disabled = False
            page.update()
        actualizar_boton_escritura()

        return ft.View(
            route="/nueva_historia",
            controls=[
                page.appbar,
                ft.Column(
                    expand=True,
                    spacing=10,
                    controls=[
                        #zona_historia,
                        zona_stack_row,
                        lista_btn,  # Botones de acción
                    ]
                )
            ],
            bgcolor=th["MORADO_HISTORIA"]
        )
