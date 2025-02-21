import flet as ft
from pymongo import MongoClient


client = MongoClient("mongodb://localhost:27017/")  
db = client["gerenciador_senhas"]  
users_collection = db["usuarios"]  
passwords_collection = db["senhas"] 


def main(page: ft.Page):
    page.title = "Gerenciador de Senhas"
    page.theme_mode = "dark"
    page.window_width = 500
    page.window_height = 700
    page.window_maximizable = False
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"

    mensagem = ft.Text("", color=ft.colors.WHITE)


    def login():
        page.controls.clear()

        def validar_login(e):
            username = campo_usuario.value
            password = campo_senha.value
            user = users_collection.find_one({"username": username, "password": password})
            if user:
                senhas(username)
            else:
                mensagem.value = "Login ou senha incorretos!"
            page.update()


        titulo = ft.Text("Login", size=30)
        campo_usuario = ft.TextField(label="Usuário", text_align=ft.TextAlign.LEFT)
        campo_senha = ft.TextField(label="Senha", text_align=ft.TextAlign.LEFT, password=True)
        btn_entrar = ft.ElevatedButton("Entrar", on_click=validar_login)
        btn_voltar = ft.ElevatedButton("Voltar", on_click=lambda e: main(page))

        page.add(
            titulo,
            campo_usuario,
            campo_senha,
            btn_entrar,
            btn_voltar,
            mensagem
        )
        page.update()    


    def cadastrar(e):
        page.controls.clear()

        titulo = ft.Text("Cadastrar:", size=30)
        username = ft.TextField(label="Usuário", text_align=ft.TextAlign.LEFT)
        password = ft.TextField(label="Senha", text_align=ft.TextAlign.LEFT, password=True)
        
        def cadastrar_usuario(e):
            if username.value and password.value:
                if users_collection.find_one({"username": username.value}):
                    mensagem.value = "Usuário já existe!"
                else:
                    users_collection.insert_one({"username": username.value, "password": password.value})
                    mensagem.value = "Usuário cadastrado com sucesso!"
                page.update()
            else:
                mensagem.value = "Preencha todos os campos!"
                page.update()

        btn_cadastrar = ft.ElevatedButton("Cadastrar", on_click=cadastrar_usuario)
        btn_voltar = ft.ElevatedButton("Voltar", on_click=lambda e: main(page))
        
        page.add(
            titulo,
            username,
            password,
            btn_cadastrar,
            btn_voltar,
            mensagem
        )
        page.update()

    
    def senhas(username):
        user = users_collection.find_one({"username": username})

        if not user:
            mensagem.value = "Usuário ou senha incorretos!"
            page.update()
            return

        page.controls.clear()
        page.vertical_alignment = "top"

        titulo = ft.Text(f"Bem-vindo, {username}", size=30)
        salvar = ft.TextField(label="Nova senha", text_align=ft.TextAlign.LEFT)
        
        def salvar_mensagem(e):
            if salvar.value:
                passwords_collection.insert_one({"username": username, "password": salvar.value})
                carregar_senhas()
                salvar.value = ""
                page.update()

        def carregar_senhas():
            senhas = passwords_collection.find({"username": username})
            lista_senhas.controls.clear()
            for senha in senhas:
                lista_senhas.controls.append(ft.Text(senha["password"]))
            page.update()

        lista_senhas = ft.Column()
        carregar_senhas()

        btn_salvar = ft.ElevatedButton("Salvar", on_click=salvar_mensagem)
        btn_voltar = ft.ElevatedButton("Sair", on_click=lambda e: main(page))
    
        page.add(
              ft.Column(
            [
                ft.Row(
                    [btn_voltar],
                    alignment=ft.MainAxisAlignment.START,  
                )
            ],
            alignment=ft.MainAxisAlignment.START,  
        ),
            titulo,
            salvar,
            btn_salvar,
            lista_senhas,

        )
        page.update()


    
    senhas_titulo = ft.Text("Gerenciador de Senhas", size=30)
    

    btn_login = ft.ElevatedButton("Login", width=150, height=30, on_click=lambda e: login())
    btn_cadas = ft.ElevatedButton("Cadastre-se", width=150, height=30, on_click=cadastrar)
    
    page.controls.clear()
    page.add(
        senhas_titulo,
        btn_login,
        btn_cadas,
        mensagem,
       
    )
    page.update()


ft.app(target=main)

