import flet as ft
from flet_route import Params, Basket
import threading
from controller.StoryController import StoryController
import re
import time
import pyperclip


class CargarHistoria:
    def __init__(self):
        pass

    def view(self, page: ft.Page, params:Params, basket:Basket):
        controller = StoryController(page, False)
        usuario = page.session.get("username")
        page.theme_mode = ft.ThemeMode.LIGHT


        def button_back(e):
            page.go("/home")
            page.update()

        #Boton para ir hacia atras
        btn_back = ft.IconButton(
            icon=ft.Icons.CHEVRON_LEFT,
            on_click=button_back
        )

        def button_accept(e):
            if titulo.value == "":
                print("Titulos vacio")
            else:
                print(f"Me gusta tu titulo: '{titulo.value}'")
            page.close(confirm_tittle)
            page.update()

        

        confirm_tittle = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirmar nombre"),
            content=ft.Text("¿Quieres guardar la historia con este nombre?"),
            actions=[
                ft.TextButton("Aceptar", on_click=button_accept),
                ft.TextButton("Cancelar", on_click=lambda e: page.close(confirm_tittle)),
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )

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
            ]  # 👈 se muestra a la derecha
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

            return ft.Text(spans=spans, selectable=True)

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
                    tamaño = {3: 22, 4: 20, 5: 18, 6: 16}.get(len(nivel), 14)
                    elementos.append(
                        ft.Text(contenido, weight=ft.FontWeight.BOLD, size=tamaño, selectable=True)
                    )

                else:
                    elementos.append(convertir_a_richtext(linea))

            return elementos


        def send_message(e):
            prompt = entrada.value.strip()
            if prompt == "":
                return
            print(f"Mensaje enviado: {prompt}")
            scroll_marker = ft.Text("", key="scroll-target")
            mensajes.controls.append(scroll_marker)
         
            entrada.value = ""

            zona_carga.visible = True
            entrada.disabled = True
            btn_send.disabled = True
            btn_copy.disabled = True
            mensajes.controls.append(ft.Text(f"Tu: {prompt}"))
            page.update()
            threading.Thread(target=procesar_en_segundo_plano, args=(prompt,)).start()

        def procesar_en_segundo_plano(prompt):
            print("Estoy procesando la respuesta")


            respuesta = controller.procesar_mensaje(prompt)
            print("AHORA TOCA GUARDAR LOS DATOS\n")
            controller.guardar_datos(respuesta)
            print("\n\n\n ----------------------\n\n\n")
            page.run_thread(lambda: (mostrar_respuesta(respuesta), page.update()))
            

        def mostrar_respuesta(respuesta):
            entrada.disabled = False
            btn_send.disabled = False
            zona_carga.visible = False
            btn_copy.disabled = False

                # Mostrar "IA:" seleccionable
            mensajes.controls.append(
                ft.Text("🤖 IA:", weight=ft.FontWeight.BOLD, selectable=True)
            )

            for elem in parse_respuesta_md(respuesta):
                mensajes.controls.append(elem)
            page.update()


            mensajes.scroll_to(key="scroll-target", duration=300)

            

        btn_send = ft.IconButton(
            icon=ft.Icons.SEND,
            on_click=send_message
        )

        entrada = ft.TextField(
            hint_text="Escribe tu historia aquí",
            multiline=False,
            autofocus=True,
            border=ft.InputBorder.OUTLINE,
            suffix_icon=btn_send,
            expand=True,
            on_submit=send_message
        )

        mensajes = ft.Column(
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            spacing=10
        )


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


        zona_carga = ft.Container(
            content=cargando,
            visible=False,
            alignment=ft.alignment.center,
            bgcolor=ft.Colors.with_opacity(0.5, ft.Colors.SURFACE),
            #visible=False,  # 👈 ¡clave!
            expand=True

        )

        zona_historia = ft.Container(
            content=mensajes,
            border_radius=15,
            padding=20,
            alignment=ft.alignment.center,
            width=None,
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
            border=ft.border.all(1, ft.Colors.OUTLINE),
            visible=True,
            expand=True
        )



        zona_stack = ft.Stack(
            controls=[
                zona_historia,  # fondo: contenido
                zona_carga      # capa superior: spinner
            ],
            expand=True
        )

        return ft.View(
            route="/cargar_historia",
            controls=[
                page.appbar,
                ft.Column(
                    expand=True,
                    spacing=10,
                    controls=[
                        #zona_historia,
                        zona_stack,
                        ft.Container(  # campo en la parte inferior
                            padding=10,
                             content=ft.Row(
                                controls=[
                                    entrada,  # Hace que el campo ocupe el máximo espacio posible
                                    btn_copy               # El botón va a la derecha del campo
                                ],
                            ),
                            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST
                        )
                    ]
                )
            ]
        )
