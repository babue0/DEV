import flet as ft
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/") 
db = client['todolist_simples']  
colecao = db['list'] 

def main(page: ft.Page):
	page.title = "To do List"
	page.theme_mode = "dark"
	page.window_width = 400
	page.window_height = 700
	page.window_maximizable = False
	page.window_resizable = False
	page.horizontal_alignment = "center"
	page.vertical_alignment = "top"

	mensagem = ft.Text("", color=ft.colors.WHITE, size=25)

	lista_mensagens = ft.Column(scroll="auto", height=400)

	scroll_container = ft.Container(
    content=lista_mensagens,
    expand=True  # Garante que o scroll não afete os botões
)

	def salvar_mens(e):
			if afazeres.value.strip():
					row2 = ft.Row(
							controls=[
									ft.Text(afazeres.value, color=ft.colors.WHITE, size=20),
									ft.Container(
											content=ft.FloatingActionButton(
																icon=ft.icons.CHECK, 
																on_click=toggle_check,  
																bgcolor=ft.colors.WHITE,
																data=False,),	
											border_radius=0,
											padding=ft.padding.only(left=30),
									)
							],
							alignment=ft.MainAxisAlignment.CENTER,
							spacing = 20
					)
					lista_mensagens.controls.append(row2)
					afazeres.value = "" 
					page.update()



	def limpar_tudo(e):
			lista_mensagens.controls.clear()
			page.update()

	def apagar_ultimo(e):
			afazeres.value = ""
			page.update()

	def toggle_check(e):
			if e.control.data:  
					e.control.icon = ft.icons.CHECK
					e.control.bgcolor = ft.colors.WHITE
					e.control.data = False  
			else:  
					e.control.icon = ft.icons.CHECK
					e.control.bgcolor = ft.colors.GREEN
					e.control.data = True  
    
			page.update()


	titulo = ft.Text("To do List", size= 35)
	afazeres = ft.TextField(label="Digite aqui", on_submit=salvar_mens)
	salvar = ft.ElevatedButton("Salvar", on_click=salvar_mens)
	limpar = ft.ElevatedButton("Limpar", on_click=limpar_tudo)
	# apagar = ft.ElevatedButton("Apagar", on_click=apagar_ultimo)

	row = ft.Row(
			controls = [scroll_container],
			alignment=ft.MainAxisAlignment.CENTER
	)

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
			# ft.Column(
			#     [
			#         ft.Row(
			#             [apagar],
			#             alignment=ft.MainAxisAlignment.START,
			#         )
			#     ],
			#     alignment=ft.MainAxisAlignment.START
			# ),
			titulo,
			afazeres,
			salvar,
			row 

			
			
	)
	page.update()


ft.app(target=main)