
from flet_route import Params, Basket
import flet as ft
from story.StoryLibrary import StoryLibrary

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
                print((f"Eliminar historia: {nombre}"))
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
                                    ft.ElevatedButton("Cargar", on_click=cargar_historia(h["nombre"], h["modo"]), bgcolor=ft.Colors.BLUE_400, color=ft.Colors.WHITE),
                                ], spacing=4),
                                alignment=ft.alignment.center_right,
                                margin=ft.margin.only(left=10)
                            )
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        padding=30,
                        margin=ft.margin.symmetric(vertical=4),
                        bgcolor=ft.Colors.WHITE,
                        border_radius=8,
                        border=ft.border.all(1, ft.Colors.BLUE_GREY_100),
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
                    ft.Icon(ft.Icons.FLASH_ON, color=ft.Colors.BLUE_400, size=32),
                    ft.Text("Modo rápido", size=20, weight=ft.FontWeight.BOLD)
                ], spacing=10),
                ft.Text("Crea una historia en segundos con pocos datos", size=15, color=ft.Colors.BLUE_GREY_600),
                ft.ElevatedButton("Empezar rápido", bgcolor=ft.Colors.BLUE_400, color=ft.Colors.WHITE, on_click=lambda e: page.open(dlg_rapido))
            ], spacing=10),
            padding=20,
            bgcolor=ft.Colors.WHITE,
            border_radius=12,
            border=ft.border.all(1, ft.Colors.BLUE_GREY_100),
            width=350
        )

        card_detallado = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.EDIT, color=ft.Colors.GREEN_400, size=32),
                    ft.Text("Modo detallado", size=20, weight=ft.FontWeight.BOLD)
                ], spacing=10),
                ft.Text("Personaliza paso a paso cada aspecto de tu historia", size=15, color=ft.Colors.BLUE_GREY_600),
                ft.ElevatedButton("Empezar detallado", bgcolor=ft.Colors.GREEN_400, color=ft.Colors.WHITE, on_click=lambda e: page.open(dlg_detallado))
            ], spacing=10),
            padding=20,
            bgcolor=ft.Colors.WHITE,
            border_radius=12,
            border=ft.border.all(1, ft.Colors.BLUE_GREY_100),
            width=350
        )

        # Diálogos para crear historia
        nombre_input = ft.TextField(label="Nombre de la historia", autofocus=True, expand=True)
        def confirmar_rapido(e):
            print(f"Crear historia rápida: {nombre_input.value}")
            page.session.set("nombre_bd", nombre_input.value.replace(" ", "_"))
            page.session.set("modo", "rapido")
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
                ft.Row([
                    # Columna izquierda: historias, bien pegada y con más borde
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Tus historias", size=52, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_GREY_900),
                            filtro,
                            ft.Container(
                                content=ft.Column(lista_historias()),
                                bgcolor=ft.Colors.WHITE,
                                border_radius=16,
                                border=ft.border.all(2, ft.Colors.BLUE_GREY_100),
                                padding=16,
                                width=600,
                                height=750
                            )
                        ], spacing=20),
                        margin=ft.margin.only(left=150, top=30, bottom=30, right=0)
                    ),
                    # Mucho espacio en el centro
                    ft.Container(width=160),
                    # Columna derecha: crear nueva historia, bien a la derecha
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Crear nueva historia", size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_GREY_900),
                            card_rapido,
                            card_detallado
                        ], spacing=20),
                        margin=ft.margin.only(right=40, top=30, bottom=30, left=0)
                    )
                ], alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.START)
            ],
            bgcolor=ft.Colors.AMBER_50,
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )