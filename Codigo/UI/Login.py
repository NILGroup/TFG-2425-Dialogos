import flet as ft
from flet_route import Params, Basket
import users.UserManager as user_manager
from UI.Theme import HISTORIAS_THEME as th

class Login:
    
    def __init__(self):
        pass

    def view(self, page: ft.Page, params: Params, basket: Basket):

        # === Campos de entrada refinados ===
        usuario = ft.TextField(
            label="Usuario",
            prefix_icon=ft.Icon(ft.Icons.PERSON_OUTLINE, th["TEXT"]),
            border_radius=20,
            filled=True,
            bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
            label_style=ft.TextStyle(color=th["TEXT"]),
            color=th["TEXT"],
            width=300
        )


        # Estado para saber si mostrar u ocultar la contraseña
        mostrar_pwd = ft.Ref[bool]()
        mostrar_pwd.value = False

        def alternar_password(e):
            mostrar_pwd.value = not mostrar_pwd.value
            contrasena.password = not mostrar_pwd.value
            contrasena.suffix = ft.IconButton(
                icon=ft.Icons.VISIBILITY if not mostrar_pwd.value else ft.Icons.VISIBILITY_OFF,
                icon_color=th["TEXT"],
                on_click=alternar_password
            )
            page.update()

        contrasena = ft.TextField(
            label="Contraseña",
            prefix_icon=ft.Icon(ft.Icons.LOCK_OUTLINE, color=th["TEXT"]),
            password=True,
            border_radius=20,
            filled=True,
            bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
            label_style=ft.TextStyle(color=th["TEXT"]),
            color=th["TEXT"],
            suffix=ft.IconButton(
                icon=ft.Icons.VISIBILITY,
                icon_color=th["TEXT"],
                on_click=alternar_password
            ),
            width=300
        )

        page.add(contrasena)
        # === Lógica de login ===
        def login(e):
            user = user_manager.buscar_usuario(usuario.value)
            if user:
                if user["password"] == contrasena.value:
                    page.session.set("usuario", usuario.value)
                    page.session.set("email", user["email"])
                    page.go("/home")
                else:
                    error.value = "Usuario o contraseña incorrectos"
            else:
                error.value = "Usuario o contraseña incorrectos"
            page.update()

        # === Elementos visuales ===
        #recordar = ft.Checkbox(label="Recordarme", value=False, fill_color=ft.Colors.WHITE)
        error = ft.Text("", color=th["ERROR"])

        btn_login = ft.ElevatedButton(
            text="Entrar",
            width=300,
            height=45,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=25),
                bgcolor=th["SUCCESS"],
                color=th["TEXT"],
                elevation=8
            ),
            on_click=login
        )

        # adition = ft.Row(
        #     controls=[
        #         recordar,
        #         ft.TextButton("¿Olvidaste tu contraseña?", on_click=lambda e: print("Recuperar")),
        #     ],
        #     alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        #     width=300
        # )

        register = ft.Row(
            controls=[
                ft.Text("¿No tienes cuenta? ", color=th["TEXT"], size=18),
                ft.TextButton(
                    text="Regístrate",
                    style=ft.ButtonStyle(
                        padding=0,
                        overlay_color=ft.Colors.TRANSPARENT,
                        color=th["TEXT"],
                        text_style=ft.TextStyle(decoration=ft.TextDecoration.UNDERLINE)
                    ),
                    on_click=lambda e: page.go("/register")
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )

        # === Caja principal con efecto Glassmorphism ===
        inicio_sesion = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("INICIAR SESIÓN", size=26, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK),
                    ft.Text("Accede para comenzar tu historia", size=14, color=ft.Colors.BLACK),
                    usuario,
                    contrasena,
                    #adition,
                    btn_login,
                    error,
                    register
                ],
                spacing=15,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            width=380,
            padding=30,
            border_radius=20,
            bgcolor=th["BG"],
            #bgcolor=ft.Colors.with_opacity(0.15, ft.Colors.WHITE),
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color=ft.Colors.BLACK26,
                offset=ft.Offset(0, 4)
            ),
            border=ft.border.all(2, ft.Colors.PURPLE),
        )

        # === Descripción lateral ===
        descripcion = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        "Bienvenido a historIAs",
                        size=42,
                        weight=ft.FontWeight.BOLD,
                        color=th["TEXT"]
                    ),
                    ft.Text(
                        "Explora tu imaginación y crea historias inolvidables con la ayuda de la inteligencia artificial. "
                        "Esta herramienta te guía paso a paso para construir mundos, personajes y tramas, desde la idea inicial hasta el capítulo final.",
                        size=24,
                        color=th["TEXT"],
                        width=600
                    )
                ],
                spacing=20,
                alignment=ft.MainAxisAlignment.CENTER
            ),
            alignment=ft.alignment.center_left,
            padding=200,
            expand=True
        )

        # === Contenedor login ===
        ct = ft.Container(
            content=inicio_sesion,
            alignment=ft.alignment.center_right,
            padding=200,
        )

        # === Separador visual ===
        # separador = ft.Container(
        #     width=2,
        #     bgcolor=ft.Colors.AMBER_50,
        #     shadow=ft.BoxShadow(
        #         spread_radius=1,
        #         blur_radius=4,
        #         color=ft.Colors.GREY_500,
        #         offset=ft.Offset(2, 0)
        #     ),
        #     border_radius=ft.border_radius.all(10),
        #     alignment=ft.alignment.center
        # )

        # === Fila central ===
        contenido = ft.Row(
            controls=[
                descripcion,
                #separador,
                ct
            ],
            expand=True,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )

        # === Fondo degradado ===
        return ft.View(
            route="/",
            controls=[
                ft.Container(
                    expand=True,
                    bgcolor = th["FONDO"],
                    content=ft.Stack(
                        expand=True,
                        controls=[
                            contenido
                        ],
                    )
                )
            ]
        )
