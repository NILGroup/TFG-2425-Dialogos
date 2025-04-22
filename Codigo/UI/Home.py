import flet as ft
from flet_route import Params, Basket
from controller.StoryController import StoryController

class Home:
    def __init__(self):
        pass

    def view(self, page: ft.Page, params:Params, basket:Basket):
        controller = StoryController()
        usuario = page.client_storage.get("username")
        email = page.client_storage.get("email")
        page.theme_mode =  ft.ThemeMode.LIGHT

        def mode_clicked(e):
            e.control.selected = not e.control.selected
            page.theme_mode=ft.ThemeMode.LIGHT if page.theme_mode == ft.ThemeMode.DARK else ft.ThemeMode.DARK
            page.update()

        btn_mode = ft.IconButton(
            icon=ft.Icons.DARK_MODE,
            selected_icon=ft.Icons.LIGHT_MODE,
            on_click=mode_clicked,
            selected=False,
            style=ft.ButtonStyle(
                color={"selected": ft.Colors.WHITE, "": ft.Colors.BLACK},  # Cambia el color del icono
            ),
            
            tooltip="Cambiar tema"
        )

        def disconet_session(e):
            page.client_storage.remove("username")
            page.client_storage.remove("email")
            page.go("/")
            page.update()

        btn_disconect = ft.IconButton(
            icon=ft.Icons.LOGOUT,
            on_click=disconet_session
        )

        header = ft.AppBar(
            actions=[
                btn_mode,
                btn_disconect
            ],
            bgcolor=ft.Colors.AMBER_50,
        )

        # header = ft.Row(
        #     controls=[btn_mode],
        #     alignment=ft.MainAxisAlignment.END
        # )

        titulo = ft.Text("Creador de Historias", size=40, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_GREY_900)
        bienvenida = ft.Text(
            f"Hola, {usuario}! ¿Qué quieres hacer hoy?",
            size=18,
            text_align=ft.TextAlign.CENTER,
            width=500,
            color=ft.Colors.BLUE_GREY_700
        )
        t = ft.Text()   

        def button_detallado(e):
            page.client_storage.set("modo", "detallado")
            page.go("/nueva_historia")

        def button_rapido(e):
            page.client_storage.set("modo", "rapido")
            page.go("/nueva_historia")  

        def button_cargar(e):
            print("Cargar historia")


        btn_cargar = ft.ElevatedButton(
            text="Cargar historia",
            #icon="DRAW",
            on_click=lambda e: controller.button_cargar(page)
        )

        btn_detallado = ft.ElevatedButton(
            text="Modo detallado",
            #icon="DRAW",
            on_click=button_detallado  # Cambia la ruta a la que quieras navegar
        )

        btn_rapido = ft.ElevatedButton(
            text="Modo rápido",
            #icon="FOLDER",
            on_click=button_rapido  # Cambia la ruta a la que quieras navegar
        )


        return ft.View(
            route="/home",
            controls=[
                header,
                titulo,
                ft.Container(height=20),
                bienvenida,
                ft.Container(height=40),
                btn_rapido,
                btn_detallado,
                btn_cargar,
                t
            ],
            bgcolor = ft.Colors.AMBER_50,
            vertical_alignment = ft.MainAxisAlignment.CENTER,
            horizontal_alignment = ft.CrossAxisAlignment.CENTER
        )
