import flet as ft
from pymongo import MongoClient

def main(page: ft.Page):
    page.title = "To do List"
    page.theme_mode = "dark"
    page.window_width = 500
    page.window_height = 700
    page.window_maximizable = False
    page.horizontal_alignment = "center"
    page.vertical_alignment = "top"

    mensagem = ft.Text("", color=ft.colors.WHITE, size=25)

    lista_mensagens = ft.Column()

    def salvar_mens(e):
        if afazeres.value.strip():
            lista_mensagens.controls.append(
                ft.Text(afazeres.value, color=ft.colors.WHITE, size=15)
            )
            afazeres.value = "" 
            page.update()

    def limpar_tudo(e):
        lista_mensagens.controls.clear()
        page.update()

    def apagar_ultimo(e):
        afazeres.value = ""
        page.update()

    titulo = ft.Text("To do List", size= 35)
    afazeres = ft.TextField(label="Digite aqui")
    salvar = ft.ElevatedButton("Salvar", on_click=salvar_mens)
    limpar = ft.ElevatedButton("Limpar", on_click=limpar_tudo)
    apagar = ft.ElevatedButton("Apagar", on_click=apagar_ultimo)



    page.add(
        ft.Column(
            [
                ft.Row(
                    [limpar],
                    alignment=ft.MainAxisAlignment.START,
                )
            ],
            alignment=ft.MainAxisAlignment.START
        ),
        ft.Column(
            [
                ft.Row(
                    [apagar],
                    alignment=ft.MainAxisAlignment.START,
                )
            ],
            alignment=ft.MainAxisAlignment.START
        ),
        titulo,
        afazeres,
        salvar,
        lista_mensagens
    )
    page.update



ft.app(target=main)