import flet as ft
from flet_route import Params, Basket
import users.UserManager as user_manager
from UI.Theme import HISTORIAS_THEME as th

class Register:
    def __init__(self):
        pass

    def view(self, page:ft.Page, params:Params, basket:Basket):
        #Campos de entrada
        usuario = ft.TextField(
            label="Username",
            prefix_icon=ft.Icons.PERSON,
            border_radius=ft.border_radius.all(25),
            filled=True,
            width=300
        )

        correo = ft.TextField(
            label="E-mail",
            prefix_icon=ft.Icons.EMAIL,
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

        repit_contrasena = ft.TextField(
            label="Repeat Password",
            prefix_icon=ft.Icons.LOCK,
            password=True,
            can_reveal_password=True,
            border_radius=ft.border_radius.all(25),
            filled=True,
            width=300
        )


        def validar_campo(campo, mensaje=None, correct=False):
            if not correct:
                campo.border_color = ft.Colors.RED
                campo.label_style = ft.TextStyle(color=ft.Colors.RED)
                error.value = mensaje
            else:
                campo.border_color = None
                campo.label_style = None
            

        def error_loging_style():
            error = False
            campos = [usuario, correo, contrasena, repit_contrasena]
            for campo in campos:
                validar_campo(
                    campo,
                    "Por favor, completa todos los campos" if campo.value.strip() == "" else None,
                    True if campo.value.strip() != "" else False
                )
                if campo.value.strip() == "":
                    error = True
            return error

        def register(e):  
            correcto = True
            todos_campos = [usuario, correo, contrasena, repit_contrasena]
            for campo in todos_campos:
                validar_campo(campo, "", True)
            if contrasena.value != repit_contrasena.value:
                validar_campo(repit_contrasena,"Las contraseñas no coinciden",False)
                correcto = False
            elif user_manager.buscar_usuario(usuario.value):
                validar_campo(usuario, "El usuario ya existe", False)
                correcto = False
            elif user_manager.buscar_correo(correo.value):
                validar_campo(correo, "El correo ya existe", False)
                correcto = False
            elif error_loging_style():
                correcto = False   
            if correcto and user_manager.registrar_usuario(correo.value, usuario.value, contrasena.value):
                page.go("/home")
            page.update()

        btn_register = ft.ElevatedButton(
            "Registrar",
            icon=ft.Icons.CHECK,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=25),
                bgcolor=th["SUCCESS"],
                color=th["TEXT"],
            ),
            on_click=register
        )

        error = ft.Text("", color=ft.Colors.RED)

        def button_back(e):
            page.go("/")
            page.update()

        #Boton para ir hacia atras
        btn_back = ft.IconButton(
            icon=ft.Icons.CHEVRON_LEFT,
            on_click=button_back
        )

        page.appbar = ft.AppBar(
            leading=btn_back,
            leading_width=40,
            center_title=True,
        )

        return ft.View(
            route="/register",
            controls=[
                page.appbar,
                usuario,
                correo,
                contrasena,
                repit_contrasena,
                btn_register,
                error
            ],
            bgcolor=th["FONDO"],
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )