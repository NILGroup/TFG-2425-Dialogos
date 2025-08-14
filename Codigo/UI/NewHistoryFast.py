import flet as ft
from flet_route import Params, Basket
import threading
from controller.StoryController import StoryController
import re

class NuevaHistoriaRapida:
    def __init__(self):
        self.capitulo = 1

    def view(self, page: ft.Page, params: Params, basket: Basket):
        controller = StoryController(page, True)
        usuario = page.session.get("username")
        
        def button_back(e):
            page.go("/home")
            page.update()

        #Boton para ir hacia atras
        btn_back = ft.IconButton(
            icon=ft.Icons.CHEVRON_LEFT,
            on_click=button_back
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

        def toggle_theme(e):
            page.theme_mode = (
                ft.ThemeMode.DARK if page.theme_mode == ft.ThemeMode.LIGHT else ft.ThemeMode.LIGHT
            )
            page.update()


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

        # Estado de la vista
        estado = {"pantalla": "cuestionario"}  # cuestionario | cargando | resultado
        historia_generada = {"titulo": "", "texto": ""}

        seleccion = ft.Text(value="Elige algo...")

        def on_change(e):
            seleccion.value = f"Has elegido: {e.control.value}"
            page.update()


        # Campos del formulario

        tema = ft.TextField(
            label="Tema",
            hint_text="Ej: Historia de amor, aventura épica",
            #prefix_icon=ft.Icons.THEME,
            width=400
        )
        genero = ft.TextField(
            label="Género",
            hint_text="Ej: Fantasía, Ciencia Ficción, Terror",
            prefix_icon=ft.Icons.BOOK,   # Usa leading_icon
            width=400
        )
        ambientacion = ft.TextField(
            label="Ambientación",
            hint_text="Ej: Medieval, Futurista, Espacial",
            prefix_icon=ft.Icons.APARTMENT,
            width=400
        )
        protagonista = ft.TextField(
            label="Protagonista principal",
            hint_text="Ej: Nombre, edad, breve descripción",
            prefix_icon=ft.Icons.PERSON,
            width=400
        )
        tono = ft.TextField(
            label="Tono",
            hint_text="Ej: Triste, Alegre, Misterioso",
            prefix_icon=ft.Icons.EMOJI_EMOTIONS,
            width=400
        )
        tamaño = ft.Dropdown(
            label="Longitud de la historia",
            hint_text="Selecciona la longitud deseada",
            options=[
                ft.dropdown.Option("Corta"),
                ft.dropdown.Option("Larga"),
                ft.dropdown.Option("Muy larga"),
            ],
            value=None,              # o un valor por defecto
            on_change=on_change,
            width=400,
            dense=False,             # más alto/bajo
            filled=True,             # fondo según tema
        )

        # Botón para enviar el formulario
        def generar_historia(e):
            # Ocultar cuestionario, mostrar cargando
            estado["pantalla"] = "cargando"
            actualizar_vista()
            datos_encuesta = (
                f"Tema: {tema.value}\n"
                f"Género: {genero.value}\n"
                f"Ambientación: {ambientacion.value}\n"
                f"Protagonista: {protagonista.value}\n"
                f"Tono: {tono.value}\n"
                f"Tamaño: {tamaño.value}\n"
                "Crea una historia a partir de estos datos."
            )
            # Lanzar la generación en segundo plano
            threading.Thread(target=procesar_en_segundo_plano, args=(datos_encuesta,)).start()

        btn_generar = ft.ElevatedButton(
            text="¡Generar historia!",
            icon=ft.Icons.AUTO_STORIES,
            on_click=generar_historia,
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.BLUE_500,
                color=ft.Colors.WHITE,
                padding=20,
                shape=ft.RoundedRectangleBorder(radius=15)
            ),
            width=400,
            height=55
        )

        # Pantalla de cuestionario
        cuestionario = ft.Column(
            [
                ft.Text(
                    "Crea tu historia en segundos",
                    size=32,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLUE_GREY_900,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Text(
                    "Completa solo lo imprescindible y déjate sorprender",
                    size=16,
                    color=ft.Colors.BLUE_GREY_700,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Container(
                    ft.Column(
                        [
                            tema,
                            genero,
                            ambientacion,
                            protagonista,
                            tono,
                            tamaño,
                            ft.Container(height=10),
                            btn_generar,
                        ],
                        spacing=16,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    border_radius=18,
                    bgcolor=ft.Colors.WHITE,
                    padding=30,
                    margin=ft.Margin(0, 0, 0, 0),
                    shadow=ft.BoxShadow(
                        spread_radius=1,
                        blur_radius=12,
                        color=ft.Colors.with_opacity(0.10, ft.Colors.BLACK)
                    ),
                    width=450,
                ),
            ],
            spacing=30,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True,
        )

        # Pantalla de carga
        zona_carga = ft.Column(
            [
                ft.ProgressRing(),
                ft.Text("La IA está creando tu historia...", size=20, text_align=ft.TextAlign.CENTER),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
        )

        def siguiente_capitulo(e):
            self.capitulo += 1
            generar_historia(e)  # Reutiliza la lógica de generación


        # Pantalla de resultado (tarjeta)
        def resultado_historia():
            cabecera = ft.Row(
                [
                    ft.Icon(ft.Icons.MENU_BOOK, size=36, color=ft.Colors.ORANGE_400),
                    ft.Text(historia_generada["titulo"], size=26, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_GREY_900),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            )

            # ancho “cómodo” similar al que ves en NewHistory (ajusta si lo quieres más ancho/estrecho)
            ANCHO_BOX = 950

            zona_historia_fast = ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(
                            historia_generada["texto"],
                            size=18,
                            color=ft.Colors.BLACK,
                            selectable=True,
                            text_align=ft.TextAlign.LEFT,
                        )
                    ],
                    scroll=ft.ScrollMode.ALWAYS,  # scroll en el Column
                    spacing=0,
                    expand=True,
                ),
                width=ANCHO_BOX,                        # <- ancho fijo
                border_radius=15,
                padding=20,
                alignment=ft.alignment.top_left,
                bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                border=ft.border.all(1, ft.Colors.OUTLINE),
            )

            fila_centrada = ft.Row([zona_historia_fast], alignment=ft.MainAxisAlignment.CENTER, expand=True)

            botones = ft.Row(
                [
                    ft.ElevatedButton(
                        "Reescribir",
                        icon=ft.Icons.CONTENT_COPY,
                        on_click=lambda e: page.set_clipboard(historia_generada["texto"])
                    ),
                    ft.ElevatedButton(
                        "Modificar",
                        icon=ft.Icons.ARROW_BACK,
                        style=ft.ButtonStyle(bgcolor=ft.Colors.ORANGE_400, color=ft.Colors.WHITE),
                        on_click=lambda e: reiniciar()
                    ),
                    ft.ElevatedButton(
                        "Continuar",
                        icon=ft.Icons.AUTO_STORIES,
                        on_click=lambda e: continuar_capitulo(e)
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=16,
            )

            def continuar_capitulo(e):
                self.capitulo += 1
                datos_encuesta = (
                    f"Tema: {tema.value}\n"
                    f"Género: {genero.value}\n"
                    f"Ambientación: {ambientacion.value}\n"
                    f"Protagonista: {protagonista.value}\n"
                    f"Tono: {tono.value}\n"
                    f"Tamaño: {tamaño.value}\n"
                    f"Capítulo: {self.capitulo}\n"
                    "Continúa la historia a partir de lo anterior."
                )
                estado["pantalla"] = "cargando"
                actualizar_vista()
                threading.Thread(target=procesar_en_segundo_plano, args=(datos_encuesta,)).start()

            return ft.Column(
                [cabecera, ft.Container(height=12), fila_centrada, ft.Container(height=12), botones],
                expand=True,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )


        # Lógica para procesar la IA y actualizar el resultado
        def procesar_en_segundo_plano(datos_encuesta):
            # --- Aquí llamas a tu IA/servicio de generación ---
            respuesta = controller.procesar_mensaje_rapido(datos_encuesta, self.capitulo)
            print(respuesta)
            # Guarda la respuesta en la variable de estado
            historia_generada["texto"] = respuesta
            historia_generada["titulo"] = "Historia generada"  # Puedes extraer un título si lo tienes
            estado["pantalla"] = "resultado"
            # Actualiza la vista en el hilo principal
            page.run_thread(actualizar_vista)


        # Función para mostrar/ocultar cada parte según el estado
        principal = ft.Column(expand=True)
        def actualizar_vista():
            principal.controls.clear()
            if estado["pantalla"] == "cuestionario":
                principal.controls.append(cuestionario)
            elif estado["pantalla"] == "cargando":
                principal.controls.append(zona_carga)
            elif estado["pantalla"] == "resultado":
                print("\n\nESTO ES LO QUE SE MUESTRA EN RESULTADO\n\n")
                principal.controls.append(resultado_historia())
            page.update()

        # Reinicia el flujo para generar otra historia
        def reiniciar():
            tema.value = ""
            genero.value = ""
            ambientacion.value = ""
            protagonista.value = ""
            tono.value = ""
            tamaño.value = None
            estado["pantalla"] = "cuestionario"
            actualizar_vista()

        # Mostrar el cuestionario al cargar
        actualizar_vista()

        return ft.View(
            route="/nueva_historia_rapida",
            controls=[
                page.appbar,
                principal,
                      ],
            bgcolor=ft.Colors.AMBER_50,
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
