import flet as ft
from pymongo import MongoClient

#sudo mongod --dbpath=/Users/iandias/data/db


client = MongoClient("mongodb://localhost:27017/") 
db = client['cadastro_db']  
colecao = db['usuarios'] 

def main(page: ft.Page):
    page.title = "App de Cadastro"
    page.theme_mode = "dark"
    page.window_width = 500
    page.window_height = 700
    page.window_maximizable = False
    page.horizontal_alignment = "center"
    page.vertical_alignment = 'center'
       

    def trocar_tema(e):
        if page.theme_mode == ft.ThemeMode.LIGHT:
            page.theme_mode = ft.ThemeMode.DARK
            btn_tema.text = "Tema Claro"
        else:
            page.theme_mode = ft.ThemeMode.LIGHT
            btn_tema.text = "Tema Escuro"
        page.update()

   
    page.theme_mode = ft.ThemeMode.DARK

    page.vertical_alignment = ft.MainAxisAlignment.START


    btn_tema = ft.ElevatedButton(
        text="Tema Claro",
        on_click=trocar_tema,
        width=100,
        height=40
    )
  



    
    mensagem = ft.Text("", color=ft.colors.WHITE)



    def realizar_pesquisa():
        page.controls.clear()

        tit_pesquisa = ft.Text("Pesquisar: ", size=17)
        pesq = ft.TextField(label="Pesquise aqui :", text_align=ft.TextAlign.LEFT)


        def pesquisar(e):
            resultado = colecao.find_one({"nome": pesq.value})
            if resultado:
                mensagem.value = f"Encontrado: {resultado['nome']}, {resultado['idade']} anos, {resultado['nacionalidade']}"
            else:
                mensagem.value = "Nenhum resultado encontrado."
            page.update()

        btn_pesquisar = ft.ElevatedButton("Pesquisar", on_click=pesquisar)
        btn_voltar = ft.ElevatedButton("Voltar", on_click=lambda e: main(page))

        page.add(
            btn_voltar,
            tit_pesquisa,
            pesq,
            btn_pesquisar,
            mensagem
        )




    def pagina():
        page.controls.clear()

        tit_nome = ft.Text("Nome: ", size=17)
        nome = ft.TextField(label="Digite seu nome: ", text_align=ft.TextAlign.LEFT)

        tit_idade = ft.Text("Idade :", size=17)
        idade = ft.TextField(label="Digite sua idade", text_align=ft.TextAlign.LEFT)

        tit_nacionalidade = ft.Text("Nacionalidade: ", size=17)
        nacionalidade = ft.TextField(label="Digite sua nacionalidade ", text_align=ft.TextAlign.LEFT)

        def cadastrar(e):
            colecao.insert_one({
                "nome": nome.value,
                "idade": idade.value,
                "nacionalidade": nacionalidade.value
            })
            mensagem.value = "Cadastrado com sucesso!"
            page.update() 


        btn_cadastro = ft.ElevatedButton("Cadastrar", on_click=cadastrar  )
        btn_voltar = ft.ElevatedButton("Voltar", on_click=lambda e: main(page))

        page.add(
            btn_voltar,
            tit_nome,
            nome,
            tit_idade,
            idade,
            tit_nacionalidade,
            nacionalidade,
            btn_cadastro,
            mensagem
        )
        page.update()
   
    cadas = ft.Text("Cadastrar: ", size=30)
    btn_cadas = ft.ElevatedButton("Iniciar Cadastro", on_click=lambda e: pagina())
    buscar = ft.Text("Buscar: ", size=30)
    btn_buscar = ft.ElevatedButton("Buscar", on_click=lambda e: realizar_pesquisa())

    page.controls.clear()
    page.add(
        ft.Row(
            controls=[btn_tema],
            alignment=ft.MainAxisAlignment.END,  # Alinhamento à direita
        ),
        cadas,
        btn_cadas,
        buscar,
        btn_buscar,
    )
    page.update()

   
ft.app(target=main)


