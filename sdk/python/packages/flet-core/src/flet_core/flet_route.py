from flet_core import Page,View
import repath

def path(url: str, clear: bool, view: View):
    return [url, clear, view]



class Routing:
    """
import flet as ft
from flet_core import Routing,path
from settings.routing import Routing

def index_view(page: ft.Page,params={}):
    "/",
    return ft.view(
        controls=[
            ft.Text("This Is Index View")
        ]
    )

def main(page: ft.Page):

    app_routes = [
        path(url="/", clear=True, view=IndexView),
    ]

    Routing(page=page,app_routes=app_routes)
    page.go(page.route)
ft.app(target=main)

    
    
    
    
    
    """
    def __init__(self, page: Page,app_routes:list):
        self.page = page
        self.page.on_route_change = self.change_route
        self.page.on_view_pop = self.view_pop
        self.app_routes = app_routes

    def change_route(self, route):
        for url in self.app_routes:
            path_match = repath.match(url[0],self.page.route)
            if path_match:
                if url[1]:
                    self.page.views.clear()
                self.page.views.append(url[2](page=self.page,params=path_match.groupdict()))
                break
        self.page.update()

    def view_pop(self, view):
        self.page.views.pop()
        top_view = self.page.views[-1]
        self.page.go(top_view.route)
