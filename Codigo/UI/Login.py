import flet as ft
from flet_route import Params, Basket
import users.UserManager as user_manager

class Login:
    
    def __init__(self):
        pass

    def view(self, page: ft.Page, params:Params, basket:Basket):
        page.bgcolor = ft.Colors.GREY_50
        # Campos de entrada
        usuario = ft.TextField(
            label="Username",
            prefix_icon=ft.Icons.PERSON,
            border_radius=ft.border_radius.all(25),
            filled=True,
            width=300
        )
        contrasena = ft.TextField(
            label="Password",
            prefix_icon=ft.Icons.LOCK,
            password=True,
            can_reveal_password=True,
            border_radius=ft.border_radius.all(25),
            filled=True,
            width=300
        )

        # Lógica de login
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

        # Elementos visuales
        recordar = ft.Checkbox(label="Remember me")
        error = ft.Text("", color=ft.Colors.RED)

        btn_login = ft.ElevatedButton(
            text="Login",
            width=300,
            height=45,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=25),
                bgcolor=ft.Colors.WHITE,
                color=ft.Colors.BLACK
            ),
            on_click=login
        )

        adition = ft.Row(
            controls=[
                recordar,
                ft.TextButton("Forgot password?", on_click=lambda e: print("Recuperar")),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            width=300
        )

        register = ft.Row(
            controls=[
                ft.Text("Don’t have an account? "),
                ft.TextButton(
                    text="Register",
                    style=ft.ButtonStyle(
                        padding=0,
                        overlay_color=ft.Colors.TRANSPARENT,
                        color=ft.Colors.BLUE,
                        text_style=ft.TextStyle(
                            decoration=ft.TextDecoration.UNDERLINE
                        )
                    ),
                    on_click=lambda e: page.go("/register")
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )


        #Caja principal estilo “glass”
        incio_sesion = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Login", size=30, weight=ft.FontWeight.BOLD),
                    usuario,
                    contrasena,
                    adition,
                    btn_login,
                    error,
                    register
                ],
                spacing=10,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            border_radius=20,
            width=380,
            height=460,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=[
                    ft.Colors.AMBER_400,
                    ft.Colors.ORANGE_500,
                    ft.Colors.DEEP_ORANGE_600,
                ],
            ),

        )


        descripcion = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        "Bienvenido al Creador de Historias",
                        size=36,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLACK
                    ),
                    ft.Text(
                        "Explora tu imaginación y crea historias inolvidables con la ayuda de la inteligencia artificial. "
                        "Esta herramienta te guía paso a paso para construir mundos, personajes y tramas, desde la idea inicial hasta el capítulo final.",
                        size=18,
                        color=ft.Colors.BLACK,
                        width=400
                    )
                ],
                spacing=20,
                alignment=ft.MainAxisAlignment.CENTER
            ),
            alignment=ft.alignment.center_left,
            padding=200,
            expand=True
        )

        ct = ft.Container(
                content=incio_sesion,
                alignment=ft.alignment.center_right,
                padding=200,
        )   

        separador = ft.Container(
            width=2,  # Ancho de la barra
              # Que se estire verticalmente como las otras columnas
            bgcolor=ft.Colors.AMBER_50,  # Color base de la barra
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=4,
                color=ft.Colors.GREY_500,
                offset=ft.Offset(2, 0)
            ),
            border_radius=ft.border_radius.all(10),  # Opcional para bordes suaves
            alignment=ft.alignment.center
        )


        contenido = ft.Row(
            controls=[
                descripcion,
                separador,
                ct
            ],
            expand=True,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )


        # Fondo con color degradado (puedes reemplazar con imagen si quieres)
        return ft.View(
            route="/",
            controls=[
                ft.Container(  # Contenedor general con fondo
                    expand=True,
                    bgcolor=ft.Colors.AMBER_50,  # 🎨 Cambia el color aquí como prefieras
                    content=ft.Stack(
                        expand=True,
                        controls=[
                            contenido  # Tu Row con descripción e inicio de sesión
                        ],
                    )
                )
            ]
        )

