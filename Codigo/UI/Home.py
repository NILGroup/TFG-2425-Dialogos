
from flet_route import Params, Basket
import flet as ft
from story.StoryLibrary import StoryLibrary
from UI.Theme import HISTORIAS_THEME as th

class Home:
    def __init__(self):
        pass

    def view(self, page: ft.Page, params: Params, basket: Basket):
        usuario = page.session.get("usuario")
        page.theme_mode = ft.ThemeMode.LIGHT
        library = StoryLibrary()

        historias = library.obtener_historias(usuario)

        filtro = ft.TextField(
            hint_text="Buscar historia...",
            prefix_icon=ft.Icons.SEARCH,
            width=400,
            on_change=lambda e: page.update()
        )

        def progreso_texto(h):
            if h["total"] < 0:
                return f'Sin comenzar  -  modo: {h["modo"]}'
            return  f'{h["completadas"]}/{h["total"]} secciones completadas  -  modo: {h["modo"]}'

        def cargar_historia(nombre, modo):
            def handler(e):
                print(f"Cargando historia: {nombre} ({modo})")
                page.session.set("nombre_bd", nombre)
                page.session.set("modo", modo)
                if modo == "detallado":
                    page.go("/cargar_historia")
                elif modo == "rapido":
                    page.go("/nueva_historia_rapida")
            return handler

        
        def eliminar_historia(nombre):
            def handler(e):
                library.delete_story(usuario, nombre)
                print(f"Historia '{nombre}' eliminada")
                page.update()
            return handler

        def historias_filtradas():
            texto = filtro.value.lower() if filtro.value else ""
            return [
                h for h in historias
                if texto in h["nombre"]
            ]

        def lista_historias():
            historias_lista = historias_filtradas()
            ultimas = historias_lista[-3:] if len(historias_lista) > 3 else historias_lista
            anteriores = historias_lista[:-3] if len(historias_lista) > 3 else []
            items = []
            # Mostrar las 3 últimas (más recientes) primero
            for h in reversed(ultimas):
                items.append(
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.Icons.MENU_BOOK, size=48, color=ft.Colors.BLUE_GREY_700),
                            ft.Column([
                                ft.Text(h["nombre"], size=18, weight=ft.FontWeight.BOLD),
                                ft.Text(progreso_texto(h), size=14, color=ft.Colors.BLUE_GREY_600),
                            ], spacing=2, alignment=ft.MainAxisAlignment.CENTER),
                            ft.Container(
                                ft.Row([
                                    ft.IconButton(ft.Icons.DELETE, on_click=eliminar_historia(h["nombre"]), icon_color=ft.Colors.RED_400),
                                    ft.ElevatedButton("Cargar", on_click=cargar_historia(h["nombre"], h["modo"]), bgcolor=th["NARANJA"], color=ft.Colors.WHITE),
                                ], spacing=4),
                                alignment=ft.alignment.center_right,
                                margin=ft.margin.only(left=10)
                            )
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        padding=30,
                        margin=ft.margin.symmetric(vertical=4),
                        #bgcolor=th["WARNING"],
                        #bgcolor=ft.Colors.WHITE,
                        bgcolor=th["LISTA_HISTORIAS"],
                        border_radius=10,
                        border=ft.border.all(2, ft.Colors.BLACK12),
                        width=560
                    )
                )
            # El resto, con scroll
            if anteriores:
                items.append(
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Más historias", size=14, color=ft.Colors.BLUE_GREY_400),
                            ft.Column([
                                ft.Container(
                                    content=ft.Row([
                                        ft.Icon(ft.Icons.MENU_BOOK, size=32, color=ft.Colors.BLUE_GREY_700),
                                        ft.Column([
                                            ft.Text(h["nombre"], size=18, weight=ft.FontWeight.BOLD),
                                            ft.Text(progreso_texto(h), size=14, color=ft.Colors.BLUE_GREY_600),
                                        ], spacing=2, alignment=ft.MainAxisAlignment.CENTER),
                                        ft.Container(
                                            ft.TextButton("Cargar", on_click=cargar_historia(h["nombre"], h["modo"]), style=ft.ButtonStyle(color=ft.Colors.BLUE_400)),
                                            alignment=ft.alignment.center_right,
                                            margin=ft.margin.only(left=10)
                                        )
                                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                                    padding=30,
                                    margin=ft.margin.symmetric(vertical=4),
                                    bgcolor=ft.Colors.WHITE,
                                    border_radius=8,
                                    border=ft.border.all(1, ft.Colors.BLUE_GREY_100),
                                    width=420
                                ) for h in reversed(anteriores)
                            ], scroll=ft.ScrollMode.AUTO, height=180)
                        ])
                    )
                )
            return items

        # Tarjetas de creación de historia
        card_rapido = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.FLASH_ON, color=th["NARANJA"], size=32),
                    ft.Text("Modo rápido", size=20, weight=ft.FontWeight.BOLD)
                ], spacing=10),
                ft.Text("Crea una historia en segundos con pocos datos", size=15, color=ft.Colors.BLUE_GREY_600),
                ft.ElevatedButton("Empezar rápido", bgcolor=th["NARANJA"], color=ft.Colors.WHITE, on_click=lambda e: page.open(dlg_rapido))
            ], spacing=10),
            padding=20,
            bgcolor=ft.Colors.WHITE,
            border_radius=12,
            border=ft.border.all(2, color=th["PRIMARY"]),
            width=350
        )

        card_detallado = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.EDIT, color=th["SECONDARY"], size=32),
                    ft.Text("Modo detallado", size=20, weight=ft.FontWeight.BOLD)
                ], spacing=10),
                ft.Text("Personaliza paso a paso cada aspecto de tu historia", size=15, color=ft.Colors.BLUE_GREY_600),
                ft.ElevatedButton("Empezar detallado", bgcolor=ft.Colors.GREEN_400, color=ft.Colors.WHITE, on_click=lambda e: page.open(dlg_detallado))
            ], spacing=10),
            padding=20,
            bgcolor=ft.Colors.WHITE,
            border_radius=12,
            border=ft.border.all(2, color=th["PRIMARY"]),
            width=350
        )

        # Diálogos para crear historia
        nombre_input = ft.TextField(label="Nombre de la historia", autofocus=True, expand=True)
        def confirmar_rapido(e):
            print(f"Crear historia rápida: {nombre_input.value}")
            page.session.set("nombre_bd", nombre_input.value.replace(" ", "_"))
            page.session.set("modo", "rapido")
            library.create_story(usuario, nombre_input.value.replace(" ", "_"), "rapido", estado_secciones={})
            #page.close(dlg_rapido)
            page.go("/nueva_historia_rapida")

        dlg_rapido = ft.AlertDialog(
            modal=True,
            title=ft.Text("Nueva historia rápida"),
            content=nombre_input,
            actions=[ft.TextButton("Cancelar", on_click=lambda e: page.close(dlg_rapido)),
                    ft.TextButton("Crear", on_click=confirmar_rapido)],
            actions_alignment=ft.MainAxisAlignment.END
        )

        def confirmar_detallado(e):
            print(f"Crear historia detallada: {nombre_input.value}")
            page.session.set("nombre_bd", nombre_input.value.replace(" ", "_"))
            page.session.set("modo", "detallado")
            library.create_story(usuario, nombre_input.value.replace(" ", "_"), "detallado", estado_secciones={})
            #page.close(dlg_detallado)
            page.go("/nueva_historia")

        dlg_detallado = ft.AlertDialog(
            modal=True,
            title=ft.Text("Nueva historia detallada"),
            content=nombre_input,
            actions=[ft.TextButton("Cancelar", on_click=lambda e: page.close(dlg_detallado)),
                    ft.TextButton("Crear", on_click=confirmar_detallado)],
            actions_alignment=ft.MainAxisAlignment.END
        )

        return ft.View(
            route="/home",
            controls=[
                ft.Row(
                    [
                        # Columna izquierda: historias (se queda como la tenías)
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Text(
                                        "Mis historias",
                                        size=52,
                                        weight=ft.FontWeight.BOLD,
                                        color=ft.Colors.BLUE_GREY_900,
                                    ),
                                    filtro,
                                    ft.Container(
                                        content=ft.Column(lista_historias()),
                                        bgcolor=ft.Colors.WHITE,
                                        border_radius=16,
                                        border=ft.border.all(2, color=th["PRIMARY"]),
                                        padding=16,
                                        width=600,
                                        height=750,  # esta altura marca el alto de la fila
                                    ),
                                ],
                                spacing=20,
                            ),
                            margin=ft.margin.only(left=150, top=30, bottom=30, right=0),
                        ),

                        # Separador central
                        ft.Container(width=160),

                        # Columna derecha: crear nueva historia — centrada en eje Y
                        ft.Container(
                            alignment=ft.alignment.center,           # 👈 centra el contenido en su propio alto
                            expand=True,                              # 👈 ocupa el alto de la fila
                            margin=ft.margin.only(right=40),          # sin top/bottom para que el centro sea puro
                            content=ft.Column(
                                [
                                    ft.Text(
                                        "Crear nueva historia",
                                        size=32,
                                        weight=ft.FontWeight.BOLD,
                                        color=ft.Colors.BLUE_GREY_900,
                                    ),
                                    card_rapido,
                                    card_detallado,
                                ],
                                spacing=20,
                                alignment=ft.MainAxisAlignment.CENTER,        # centra hijos en la columna
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            ),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.START,             # X como lo tenías
                    vertical_alignment=ft.CrossAxisAlignment.START,   # la izquierda sigue arriba
                    expand=True,                                      # 👈 la fila ocupa todo el alto de la vista
                )
            ],
            bgcolor=th["FONDO"],
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
