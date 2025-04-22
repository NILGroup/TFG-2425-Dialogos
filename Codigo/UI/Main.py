import flet as ft
from flet_route import Routing, path


#Importamos las pantallas
from UI.Home import Home
from UI.Login import Login
from UI.Register import Register
from UI.NewHistory import NuevaHistoria


def main(page:ft.Page):
    page.title="Creador de historias"
    app_routes = [
        path(url="/", clear=True, view=Login().view),
        path(url="/register", clear=True, view=Register().view),
        path(url="/home", clear=True, view=Home().view),
        path(url="/nueva_historia", clear=True, view=NuevaHistoria().view)
        #path(url="/", clear=True, view=NuevaHistoria().view),
    ]

    Routing(page=page, app_routes=app_routes)
    page.go(page.route)

ft.app(target=main)